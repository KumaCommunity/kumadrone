#!/usr/bin/env python3
"""
Measure real CAD volumes of the exported V6 STLs and compute verified masses.
(V6 geometry now compiled/exported with OpenSCAD; density is still an assumption
 LW 0.35 / PETG 1.27 g/cm3 -> see mass range.)
Writes v6/data/v6_stl_mass.csv and prints totals.
"""
import csv
import glob
import os

import numpy as np
import trimesh

HERE = os.path.dirname(__file__)
STLDIR = os.path.join(HERE, "..", "STL")
OUT = os.path.join(HERE, "..", "data", "v6_stl_mass.csv")

LW = 0.35
PETG = 1.27
MAT = {
    "fuselage_0": "LW", "fuselage_1": "LW", "fuselage_2": "LW", "fuselage_3": "LW",
    "fuselage_4": "LW", "fuselage_5": "LW",
    "coupler_0": "PETG", "coupler_1": "PETG", "coupler_2": "PETG", "coupler_3": "PETG",
    "coupler_4": "PETG",
    "wing_center": "LW", "wing_R1": "LW", "wing_R2": "LW", "wing_R3": "LW",
    "wing_L1": "LW", "wing_L2": "LW", "wing_L3": "LW",
    "wing_key": "PETG",
    "tail_R": "LW", "tail_L": "LW", "ruddervator_R": "LW", "ruddervator_L": "LW",
    "tail_saddle": "PETG", "tail_shoe_R": "PETG", "tail_shoe_L": "PETG",
    "saddle_plate": "PETG", "camera_plate": "PETG", "camera_cradle": "PETG",
    "dorsal_fairing": "LW", "battery_tray": "LW", "secured_tray": "PETG",
    "battery_hatch_lid": "LW", "motor_bulkhead": "PETG",
    "wing_saddle_clamp": "LW",  # LW body + PETG pads (pads counted separately)
    "ventral_fin": "LW",
    "centre_spar_joiner": "PETG", "wing_center_spar_sleeve": "PETG",
    "control_horn_R": "PETG", "control_horn_L": "PETG",
    "ruddervator_hinge_R": "PETG", "ruddervator_hinge_L": "PETG",
}
QTY = {"wing_key": 6}
EXCLUDE = {"forward_equipment_tray", "insert_fit_coupon", "camera_plate", "dorsal_fairing"}  # superseded/removed (lightening)
# assembly-only small hardware not exported as its own part (fixed estimates):
ASSEMBLY_ONLY = [("tail_root_spar(carbon)", 3.0), ("tail_root_key", 1.0),
                 ("pushrod_channels(2)", 4.0), ("clamp_PETG_pads", 8.0)]


def main():
    files = sorted(glob.glob(os.path.join(STLDIR, "*.stl")))
    rows = []
    tot_lw = tot_petg = 0.0
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        if name in EXCLUDE:
            continue
        m = trimesh.load(f, force="mesh")
        vol = abs(m.volume) / 1000.0
        mat = MAT.get(name, "?")
        dens = LW if mat == "LW" else PETG if mat == "PETG" else 0.0
        qty = QTY.get(name, 1)
        mass = vol * dens * qty
        bodies = len(m.split(only_watertight=False))
        b = m.bounds
        dims = b[1] - b[0]
        fits = bool(np.all(dims <= np.array([220, 220, 250]) + 1e-6))
        if mat == "LW":
            tot_lw += mass
        elif mat == "PETG":
            tot_petg += mass
        rows.append(dict(part=name, material=mat, qty=qty, volume_cm3=round(vol, 3),
                         mass_g=round(mass, 2), bodies=bodies,
                         dims_mm=f"{dims[0]:.0f}x{dims[1]:.0f}x{dims[2]:.0f}",
                         fits_220=fits))

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    hw = sum(m for _, m in ASSEMBLY_ONLY)
    print(f"{'part':24s}{'mat':5s}{'qty':>4s}{'vol_cm3':>9s}{'mass_g':>8s}{'bodies':>7s}{'fit':>5s}")
    for r in rows:
        print(f"{r['part']:24s}{r['material']:5s}{r['qty']:>4d}{r['volume_cm3']:>9.3f}"
              f"{r['mass_g']:>8.2f}{r['bodies']:>7d}{str(r['fits_220']):>5s}")
    print("-" * 66)
    print(f"  LW-PLA printed total : {tot_lw:8.2f} g")
    print(f"  PETG   printed total : {tot_petg:8.2f} g")
    print(f"  assembly-only hw     : {hw:8.2f} g  {[n for n,_ in ASSEMBLY_ONLY]}")
    printed = tot_lw + tot_petg + hw
    print(f"  PRINTED + HW total   : {printed:8.2f} g")
    purchased = 477.0
    print(f"  purchased (unchanged): {purchased:8.2f} g")
    print(f"  => V6 EMPTY (verified vols, assumed density): {printed+purchased:8.2f} g")
    print("  (estimate used in v6_calcs was 1400 g; update docs if this differs)")
    multi = [r['part'] for r in rows if r['bodies'] > 1]
    over = [r['part'] for r in rows if not r['fits_220']]
    print(f"  multi-body parts ({len(multi)}): {multi}")
    print(f"  over 220 bed ({len(over)}): {over}")


if __name__ == "__main__":
    main()
