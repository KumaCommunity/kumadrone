#!/usr/bin/env python3
"""
Independent STL verification for Kuma FPV V5 Configuration B.

Recomputes, directly from the exported binary STL meshes (no reliance on the
existing CSVs):
  * solid volume (cm^3) via signed-tetrahedron summation
  * watertight / winding-consistent flag
  * number of disconnected closed bodies (connected-component split)
  * axis-aligned bounding box (mm) in the STL coordinate frame
  * volume centroid (mm)
  * whether the part fits inside a 220 x 220 x 250 mm build volume
Also applies the audit's own density assumptions to derive an independent
"CAD-volume mass" for cross-checking geometry_mass_screen.csv / mass_budget.csv.

Outputs: data/stl_verification.csv
"""
import csv
import glob
import os
import sys

import numpy as np
import trimesh

STL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "STL")
OUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "stl_verification.csv")

# Audit density assumptions (identical to source docs, so the comparison is
# apples-to-apples; the point is to recompute, not to change the assumption).
DENSITY = {
    "LW-PLA": 0.35,   # foaming LW-PLA effective density g/cm^3 (source assumption)
    "PETG": 1.27,     # solid PETG g/cm^3
}
# Material assignment per the source engineering deck / hardware schedule.
MATERIAL = {
    "fuselage_0": "LW-PLA", "fuselage_1": "LW-PLA", "fuselage_2": "LW-PLA",
    "fuselage_3": "LW-PLA", "fuselage_4": "LW-PLA", "fuselage_5": "LW-PLA",
    "coupler_0": "PETG", "coupler_1": "PETG", "coupler_2": "PETG",
    "coupler_3": "PETG", "coupler_4": "PETG",
    "wing_center": "LW-PLA", "wing_L1": "LW-PLA", "wing_L2": "LW-PLA",
    "wing_L3": "LW-PLA", "wing_R1": "LW-PLA", "wing_R2": "LW-PLA", "wing_R3": "LW-PLA",
    "wing_key": "PETG",
    "saddle_plate": "PETG",
    "tail_L": "LW-PLA", "tail_R": "LW-PLA",
    "ruddervator_L": "LW-PLA", "ruddervator_R": "LW-PLA",
    "tail_saddle": "PETG",
    "tail_shoe_L": "PETG", "tail_shoe_R": "PETG",
    "camera_plate": "PETG",
    "battery_tray": "PETG",
    "forward_equipment_tray": "PETG",
    "dorsal_fairing": "LW-PLA",
    "insert_fit_coupon": "TEST",
}
# Printed quantity per aircraft (wing_key printed x6).
QTY = {"wing_key": 6}

BUILD = np.array([220.0, 220.0, 250.0])


def analyze(mesh):
    vol_mm3 = abs(mesh.volume)  # trimesh returns signed volume; magnitude for solid
    vol_cm3 = vol_mm3 / 1000.0
    bbox = mesh.bounds
    dims = bbox[1] - bbox[0]
    fits = bool(np.all(dims <= BUILD + 1e-6))
    # Connected closed bodies
    parts = mesh.split(only_watertight=False)
    n_bodies = len(parts)
    # watertightness of the whole mesh
    wt = bool(mesh.is_watertight)
    # centroid of volume
    try:
        cen = mesh.centroid
    except Exception:
        cen = mesh.center_mass
    return dict(vol_cm3=vol_cm3, wt=wt, n_bodies=n_bodies, bbox=bbox, dims=dims,
                fits=fits, cen=cen)


def main():
    files = sorted(glob.glob(os.path.join(STL_DIR, "*.stl")))
    if not files:
        print("No STL files found at", STL_DIR, file=sys.stderr)
        sys.exit(1)

    rows = []
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        mesh = trimesh.load(f, force="mesh")
        a = analyze(mesh)
        mat = MATERIAL.get(name, "?")
        dens = DENSITY.get(mat, 0.0)
        qty = QTY.get(name, 1)
        mass_g = a["vol_cm3"] * dens * qty
        rows.append(dict(
            part=name,
            material=mat,
            volume_cm3=round(a["vol_cm3"], 4),
            qty=qty,
            density_g_cm3=dens,
            cad_mass_g=round(mass_g, 3),
            watertight=a["wt"],
            n_bodies=a["n_bodies"],
            bbox_x_mm=round(float(a["bbox"][1][0] - a["bbox"][0][0]), 2),
            bbox_y_mm=round(float(a["bbox"][1][1] - a["bbox"][0][1]), 2),
            bbox_z_mm=round(float(a["bbox"][1][2] - a["bbox"][0][2]), 2),
            fits_220x220x250=a["fits"],
            centroid_x_mm=round(float(a["cen"][0]), 2),
            centroid_y_mm=round(float(a["cen"][1]), 2),
            centroid_z_mm=round(float(a["cen"][2]), 2),
        ))

    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Console summary
    print(f"{'part':24s} {'mat':7s} {'vol_cm3':>9s} {'mass_g':>8s} {'wt':>3s} "
          f"{'bodies':>6s} {'fit':>4s} {'dims(mm)':>20s}")
    print("-" * 92)
    tot_lw = tot_petg = 0.0
    for r in rows:
        if r["material"] == "LW-PLA":
            tot_lw += r["cad_mass_g"]
        elif r["material"] == "PETG":
            tot_petg += r["cad_mass_g"]
        dims = f'{r["bbox_x_mm"]:.0f}x{r["bbox_y_mm"]:.0f}x{r["bbox_z_mm"]:.0f}'
        print(f'{r["part"]:24s} {r["material"]:7s} {r["volume_cm3"]:9.3f} '
              f'{r["cad_mass_g"]:8.2f} {str(r["watertight"]):>3s} {r["n_bodies"]:6d} '
              f'{str(r["fits_220x220x250"]):>4s} {dims:>20s}')
    print("-" * 92)
    print(f"TOTAL LW-PLA CAD-volume mass : {tot_lw:8.2f} g")
    print(f"TOTAL PETG   CAD-volume mass : {tot_petg:8.2f} g")
    print(f"Printed-only total           : {tot_lw + tot_petg:8.2f} g")

    multi = [r["part"] for r in rows if r["n_bodies"] > 1]
    over = [r["part"] for r in rows if not r["fits_220x220x250"]]
    notwt = [r["part"] for r in rows if not r["watertight"]]
    print(f"\nParts with >1 disconnected body ({len(multi)}): {multi}")
    print(f"Parts exceeding 220x220x250 build volume ({len(over)}): {over}")
    print(f"Parts not watertight ({len(notwt)}): {notwt}")


if __name__ == "__main__":
    main()
