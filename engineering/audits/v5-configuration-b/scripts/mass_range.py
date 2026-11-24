#!/usr/bin/env python3
"""
Mass / CG / load ENVELOPE for Kuma V5 Config B across realistic print variation.

The printed mass is NOT a single number: effective deposited density depends on
filament brand, printer, slicer walls/infill, and foaming ratio. This script
sweeps LW-PLA effective density and PETG density, plus the wing_center material
ambiguity (PETG vs LW-PLA), and reports empty/loaded mass, CG, wing loading and
stall speed as RANGES.

Inputs: mass_budget.csv (part categories, unit masses at 0.35 LW / 1.27 PETG).
Outputs: data/mass_range.csv ; prints envelope.
"""
import csv
import math
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DATADIR = os.path.join(HERE, "..", "data")

RHO_AIR = 1.225
G = 9.80665
S = 0.2275
MAC = 176.19          # mm (CG and LE_MAC are in mm)
LE_MAC = 507.43
BASE_LW = 0.35
BASE_PETG = 1.27
PURCHASED = 477.0      # fixed placeholder total (battery etc.)

# wing_center volume from geometry_mass_screen (if it is PETG, move this volume)
WING_CENTER_VOL_CM3 = 124.209
WING_CENTER_X = 581.4


def load_rows():
    rows = []
    with open(os.path.join(ROOT, "mass_budget.csv")) as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows


def part_volumes():
    """Recover solid volumes per category from geometry_mass_screen.csv."""
    lw_vol = 0.0
    petg_vol = 0.0
    with open(os.path.join(ROOT, "geometry_mass_screen.csv")) as fh:
        for r in csv.DictReader(fh):
            try:
                v = float(r["volume_cm3"])
            except (ValueError, KeyError):
                continue
            mat = r.get("material", "")
            if mat == "LW-PLA":
                lw_vol += v
            elif mat == "PETG":
                petg_vol += v
    return lw_vol, petg_vol


def evaluate(lw_density, petg_density, wing_center_petg, battery_x=410.0,
             extra_g=0.0, extra_x=556.0):
    """Recompute total mass, CG from the part table with scaled densities."""
    rows = load_rows()
    m = 0.0
    mx = 0.0
    for r in rows:
        cat = r["category"]
        mass = float(r["total_mass_g"])
        x = float(r["x_mm"])
        if cat == "LW-PLA":
            mass *= lw_density / BASE_LW
        elif cat == "PETG":
            mass *= petg_density / BASE_PETG
        # wing_center PETG scenario
        if wing_center_petg and r["item"] == "wing_center":
            # remove LW mass already scaled, add PETG-equivalent
            mass = WING_CENTER_VOL_CM3 * petg_density
        m += mass
        mx += mass * x
    if extra_g:
        m += extra_g
        mx += extra_g * extra_x
    cg = mx / m
    wl = m / (S * 100.0)                      # g/dm^2
    vs = math.sqrt(2 * (m / 1000.0) * G / (RHO_AIR * S * 1.0))
    return dict(mass_g=m, cg_mm=cg, cg_pct=(cg - LE_MAC) / MAC * 100,
                wl_g_dm2=wl, vs_m_s=vs)


def main():
    print("=" * 84)
    print("MASS / CG / LOAD ENVELOPE (print-variation range, NOT a point estimate)")
    print("=" * 84)
    lw_vol, petg_vol = part_volumes()
    print(f"Recovered solid volumes: LW-PLA {lw_vol:.1f} cm3, PETG {petg_vol:.1f} cm3")
    print("Considered: LW-PLA 0.20-0.60 g/cm3, PETG 1.20-1.30 g/cm3, and")
    print("wing_center material = LW-PLA (budget) OR PETG (SCAD comment).\n")

    out = []
    print(f"{'scenario':16s} {'LW dens':>8s} {'PETG dens':>9s} {'empty g':>8s} "
          f"{'CG mm':>7s} {'%MAC':>6s} {'WL g/dm2':>9s} {'Vs m/s':>7s}")
    dense = []
    scenarios = []
    for wc_petg in (False, True):
        for lw in (0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60):
            for petg in (1.20, 1.27, 1.30):
                r = evaluate(lw, petg, wc_petg)
                scenarios.append((wc_petg, lw, petg, r))
    # print a compact subset (LW sweep at nominal PETG, both wing_center cases)
    for wc_petg in (False, True):
        tag = "wc=PETG" if wc_petg else "wc=LW-PLA"
        for lw in (0.20, 0.25, 0.35, 0.45, 0.60):
            r = evaluate(lw, 1.27, wc_petg)
            print(f"{tag:16s} {lw:8.2f} {1.27:9.2f} {r['mass_g']:8.1f} "
                  f"{r['cg_mm']:7.1f} {r['cg_pct']:6.1f} {r['wl_g_dm2']:9.1f} "
                  f"{r['vs_m_s']:7.2f}")
            out.append(dict(wing_center=("PETG" if wc_petg else "LW-PLA"),
                            lw_density=lw, petg_density=1.27, extra_g=0,
                            mass_g=round(r["mass_g"], 1), cg_mm=round(r["cg_mm"], 2),
                            cg_pct_MAC=round(r["cg_pct"], 2),
                            wl_g_dm2=round(r["wl_g_dm2"], 1), vs_m_s=round(r["vs_m_s"], 2)))

    # envelope across ALL considered scenarios (empty and +500)
    def env(extra):
        vals = [evaluate(lw, petg, wc, extra_g=extra) for (wc, lw, petg, _) in scenarios]
        m = [v["mass_g"] for v in vals]
        cg = [v["cg_mm"] for v in vals]
        wl = [v["wl_g_dm2"] for v in vals]
        vs = [v["vs_m_s"] for v in vals]
        return (min(m), max(m), min(cg), max(cg), min(wl), max(wl), min(vs), max(vs))

    print("\n" + "-" * 84)
    for label, extra in [("EMPTY", 0.0), ("+500 g", 500.0)]:
        mn, mx, cgmn, cgmx, wlmn, wlmx, vsmn, vsmx = env(extra)
        print(f"{label}: mass {mn:6.0f}-{mx:6.0f} g | CG {cgmn:6.1f}-{cgmx:6.1f} mm "
              f"| WL {wlmn:5.1f}-{wlmx:5.1f} g/dm2 | Vs(CL1.0) {vsmn:5.2f}-{vsmx:5.2f} m/s")

    with open(os.path.join(DATADIR, "mass_range.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("\nWrote data/mass_range.csv")
    print("\nNote: this range is the honest uncertainty. The point design (1.31 kg,")
    print("CG 560) is the middle case (LW 0.35, wing_center LW-PLA). Widen further if")
    print("battery mass/station and slicer infill vary.")


if __name__ == "__main__":
    main()
