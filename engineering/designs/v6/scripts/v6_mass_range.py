#!/usr/bin/env python3
"""
V6 mass / wing-loading / stall ENVELOPE using MEASURED material volumes.
Density is the remaining assumption (slicer/filament), so sweep it.
Base volumes come from verify_v6_stl.py at nominal density (0.35 LW, 1.27 PETG).
"""
import csv
import math
import os

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "data", "v6_mass_range.csv")

RHO, G, S = 1.225, 9.80665, 0.2275
MAC, LE_MAC = 176.19, 507.43
LW_VOL = 559.14 / 0.35        # cm^3 (measured LW material, lightened V6)
PETG_VOL = 308.63 / 1.27      # cm^3 (measured PETG material, lightened V6)
HW = 16.0                     # assembly-only hardware (carbon pins, pads, pushrods)
PURCHASED = 477.0             # example electronics + battery (mass unchanged in V6)


def mass(d_lw, d_petg, extra=0.0):
    return LW_VOL * d_lw + PETG_VOL * d_petg + HW + PURCHASED + extra


def wl(m):
    return m / (S * 100.0)


def vs(m, cl=1.0):
    return math.sqrt(2 * (m / 1000.0) * G / (RHO * S * cl))


def main():
    rows = []
    for d_lw in [0.20, 0.25, 0.30, 0.35, 0.45, 0.55, 0.60]:
        for d_petg in [1.20, 1.27, 1.30]:
            m0 = mass(d_lw, d_petg)
            m5 = mass(d_lw, d_petg, 500.0)
            rows.append(dict(lw_density=d_lw, petg_density=d_petg,
                             empty_g=round(m0, 1), empty_wl=round(wl(m0), 1),
                             empty_vs=round(vs(m0), 2),
                             loaded500_g=round(m5, 1), loaded500_wl=round(wl(m5), 1),
                             loaded500_vs=round(vs(m5), 2)))

    # envelope across all considered densities
    es = [r["empty_g"] for r in rows]
    lws = [r["empty_wl"] for r in rows]
    evs = [r["empty_vs"] for r in rows]
    ls = [r["loaded500_g"] for r in rows]
    lws5 = [r["loaded500_wl"] for r in rows]
    lvs5 = [r["loaded500_vs"] for r in rows]

    print("V6 mass envelope (MEASURED volumes; density swept)")
    print(f"  LW volume {LW_VOL:.1f} cm3, PETG volume {PETG_VOL:.1f} cm3")
    print(f"  EMPTY : {min(es):.0f}-{max(es):.0f} g | WL {min(lws):.1f}-{max(lws):.1f} g/dm2"
          f" | Vs {min(evs):.2f}-{max(evs):.2f} m/s")
    print(f"  +500g : {min(ls):.0f}-{max(ls):.0f} g | WL {min(lws5):.1f}-{max(lws5):.1f} g/dm2"
          f" | Vs {min(lvs5):.2f}-{max(lvs5):.2f} m/s")
    print(f"  nominal (0.35/1.27): empty {mass(0.35,1.27):.1f} g, +500 {mass(0.35,1.27,500):.1f} g")

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("Wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
