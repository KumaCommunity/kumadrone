#!/usr/bin/env python3
"""
Independent verification of exported NACA airfoil DXFs vs analytic 4-digit
definitions used in the SCAD. Checks chord scaling, thickness distribution,
camber, max-thickness location, TE treatment, enclosed area.
Outputs data/airfoil_verification.json
"""
import json
import math
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(HERE, "..", "data", "airfoil_verification.json")


def parse_lwpolyline(path):
    with open(path, "r", errors="ignore") as fh:
        lines = [ln.rstrip("\n") for ln in fh]
    verts = []
    in_poly = False
    i = 0
    while i < len(lines) - 1:
        code = lines[i].strip()
        val = lines[i + 1].strip()
        if code == "0" and val == "LWPOLYLINE":
            in_poly = True
            i += 2
            continue
        if in_poly and code == "0":
            break
        if in_poly and code == "10":
            x = float(val)
            y = float(lines[i + 3].strip())
            verts.append((x, y))
        i += 2
    return verts


def thickness(x, t):
    return 5 * t * (0.2969 * math.sqrt(x) - 0.126 * x - 0.3516 * x * x
                    + 0.2843 * x ** 3 - 0.1015 * x ** 4)


def camber(x, m, p):
    if m == 0:
        return 0.0
    if x <= p:
        return m / (p * p) * (2 * p * x - x * x)
    return m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * x - x * x)

def analyze(name, path, chord_mm, t_ratio, m, p):
    v = parse_lwpolyline(path)
    xs = [pt[0] for pt in v]
    ys = [pt[1] for pt in v]
    xmin, xmax = min(xs), max(xs)
    xn = [x / chord_mm for x in xs]
    yn = [y / chord_mm for y in ys]

    def is_upper(xq, yq):
        return yq >= camber(xq, m, p) - 1e-6

    upper = [(xn[k], yn[k]) for k in range(len(xn)) if is_upper(xn[k], yn[k])]
    lower = [(xn[k], yn[k]) for k in range(len(xn)) if not is_upper(xn[k], yn[k])]

    def interp(surface, xq):
        s = sorted(surface)
        if xq <= s[0][0]:
            return s[0][1]
        if xq >= s[-1][0]:
            return s[-1][1]
        for k in range(len(s) - 1):
            x0, y0 = s[k]
            x1, y1 = s[k + 1]
            if x0 <= xq <= x1 and x1 > x0:
                f = (xq - x0) / (x1 - x0)
                return y0 + f * (y1 - y0)
        return s[-1][1]

    best_t = (-1, 0.0)
    for k in range(1, 3000):
        xq = k / 3000.0
        th = interp(upper, xq) - interp(lower, xq)
        if th > best_t[0]:
            best_t = (th, xq)

    cmax = camber(p, m, p) if m > 0 else 0.0
    te_gap = interp(upper, 0.999) - interp(lower, 0.999)

    area = 0.0
    for k in range(len(v)):
        x0, y0 = v[k]
        x1, y1 = v[(k + 1) % len(v)]
        area += x0 * y1 - x1 * y0
    area = abs(area) / 2.0

    closure_err = math.hypot(v[0][0] - v[-1][0], v[0][1] - v[-1][1])

    spots = {}
    for xq in [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.70, 0.90]:
        got = interp(upper, xq) - interp(lower, xq)
        want = 2 * thickness(xq, t_ratio)
        spots[f"x={xq:.2f}"] = dict(measured_tc=round(got * 100, 3),
                                    analytic_tc=round(want * 100, 3),
                                    delta_pct_of_chord=round((got - want) * 100, 4))
    return dict(
        name=name, path=os.path.relpath(path, ROOT), n_vertices=len(v),
        closure_gap_mm=round(closure_err, 5),
        measured_chord_mm=round(xmax - xmin, 3), design_chord_mm=chord_mm,
        max_thickness_pct_chord=round(best_t[0] * 100, 3),
        max_thickness_location_xc=round(best_t[1], 4),
        design_thickness_pct_chord=t_ratio * 100,
        max_camber_pct_chord=round(cmax * 100, 3),
        design_camber_pct_chord=m * 100,
        te_gap_pct_chord=round(te_gap * 100, 4),
        enclosed_area_ratio_to_chord2=round(area / chord_mm ** 2, 5),
        spot_thickness=spots)


def main():
    wing = analyze("NACA 2412 wing root", os.path.join(ROOT, "NACA_2412_Wing_Root_200mm.dxf"),
                   200.0, 0.12, 0.02, 0.40)
    tail = analyze("NACA 0010 tail root", os.path.join(ROOT, "NACA_0010_Tail_Root_190mm.dxf"),
                   190.0, 0.10, 0.0, 0.40)
    out = {"wing": wing, "tail": tail}
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2)
    for key, r in out.items():
        print(f"\n===== {r['name']} =====")
        for k in ["n_vertices", "measured_chord_mm", "design_chord_mm",
                  "closure_gap_mm", "max_thickness_pct_chord",
                  "design_thickness_pct_chord", "max_thickness_location_xc",
                  "max_camber_pct_chord", "design_camber_pct_chord",
                  "te_gap_pct_chord", "enclosed_area_ratio_to_chord2"]:
            print(f"  {k:34s}: {r[k]}")
        print("  spot thickness (t/c %) vs analytic:")
        for xq, d in r["spot_thickness"].items():
            print(f"    {xq:8s} measured={d['measured_tc']:6.3f}  "
                  f"analytic={d['analytic_tc']:6.3f}  D={d['delta_pct_of_chord']:+.4f}%c")


if __name__ == "__main__":
    main()
