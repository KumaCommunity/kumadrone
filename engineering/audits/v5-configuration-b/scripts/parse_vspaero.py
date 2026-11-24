#!/usr/bin/env python3
"""
Parse VSPAERO output (.polar from an AoA sweep, or .stab from a Stability run)
and compute the neutral point / static margin and lateral derivatives.

Usage:
    python3 parse_vspaero.py <file> [x_ref_m]
    e.g. python3 parse_vspaero.py Kuma_V5B_vspaero.polar 0.560
         python3 parse_vspaero.py Kuma_V5B_vspaero.stab 0.560

x_ref_m = VSPAERO moment-reference station (Xcg) in meters from the nose; default
0.560 (empty CG). x_np = x_ref + SM*cref. Relations: SM = -Cm_alpha/CL_alpha.
Columns are detected fuzzily and printed so you can confirm against your version.
"""
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(__file__)
DATADIR = os.path.join(HERE, "..", "data")
CREF = 0.17619
AUDIT_XNP_MM = 573.8
AUDIT_SM_PCT = 7.8


def norm(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def split_line(line):
    if "," in line:
        return [tok.strip() for tok in line.split(",") if tok.strip() != ""]
    return line.split()


def read_table(path):
    with open(path, "r", errors="ignore") as fh:
        raw = [ln.rstrip("\n") for ln in fh]
    hdr = None
    hi = -1
    for i, ln in enumerate(raw):
        toks = split_line(ln)
        nz = [norm(t) for t in toks]
        if any(n.startswith("cl") for n in nz) and \
           any("aoa" in n or "alpha" in n or "beta" in n for n in nz):
            hdr = toks
            hi = i
            break
    if hdr is None:
        raise SystemExit(f"Could not find a VSPAERO header in {path}. First lines:\n"
                         + "\n".join(raw[:6]))
    rows = []
    for ln in raw[hi + 1:]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        toks = split_line(ln)
        if len(toks) != len(hdr):
            continue
        try:
            rows.append([float(t) for t in toks])
        except ValueError:
            continue
    return hdr, rows


def col(hdr, *predicates):
    for k, name in enumerate(hdr):
        n = norm(name)
        if all(p in n for p in predicates):
            return k
    return None


def slope(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(np.unique(x)) < 2:
        return None
    m, _ = np.polyfit(x, y, 1)
    return float(m)



def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    path = sys.argv[1]
    x_ref = float(sys.argv[2]) if len(sys.argv) > 2 else 0.560
    hdr, rows = read_table(path)
    print("Detected columns:", hdr)
    if not rows:
        raise SystemExit("No numeric data rows parsed.")

    CL_a = Cm_a = Cn_b = Cl_b = None

    def find_deriv(*preds):
        return col(hdr, *preds)

    idx_cla = find_deriv("cl", "alpha")
    idx_cma = find_deriv("cm", "alpha")
    idx_cnb = find_deriv("cn", "beta")
    idx_clb = find_deriv("cl", "beta")
    if idx_cla is not None:
        CL_a = float(np.mean([r[idx_cla] for r in rows]))
    if idx_cma is not None:
        Cm_a = float(np.mean([r[idx_cma] for r in rows]))
    if idx_cnb is not None:
        Cn_b = float(np.mean([r[idx_cnb] for r in rows]))
    if idx_clb is not None:
        Cl_b = float(np.mean([r[idx_clb] for r in rows]))

    i_aoa = col(hdr, "aoa")
    if i_aoa is None:
        i_aoa = col(hdr, "alpha")
    i_beta = col(hdr, "beta")
    i_cl = col(hdr, "cltot")
    if i_cl is None:
        i_cl = col(hdr, "cl")
    # pitch moment is about Y in VSPAERO (CMytot); avoid matching CMox/CMoz
    i_cm = col(hdr, "cmytot")
    if i_cm is None:
        i_cm = col(hdr, "cmy")
    if i_cm is None:
        i_cm = col(hdr, "cmtot")
    if i_cm is None:
        i_cm = col(hdr, "cm")
    i_cn = col(hdr, "cntot")
    if i_cn is None:
        i_cn = col(hdr, "cn")

    if i_aoa is not None and i_cl is not None:
        a = [r[i_aoa] for r in rows]
        s = slope(a, [r[i_cl] for r in rows])
        if s is not None and CL_a is None:
            CL_a = s
        if i_cm is not None:
            s2 = slope(a, [r[i_cm] for r in rows])
            if s2 is not None and Cm_a is None:
                Cm_a = s2
    if i_beta is not None and i_cn is not None and Cn_b is None:
        b = [r[i_beta] for r in rows]
        s = slope(b, [r[i_cn] for r in rows])
        if s is not None:
            Cn_b = s

    print("\n=== STABILITY DERIVATIVES ===")
    print(f"  CL_alpha = {CL_a}")
    print(f"  Cm_alpha = {Cm_a}")
    print(f"  Cn_beta  = {Cn_b}")
    print(f"  Cl_beta  = {Cl_b}")
    print("  (angle units as output; ratios below are unit-consistent)")

    out = dict(x_ref_m=x_ref, CL_alpha=CL_a, Cm_alpha=Cm_a, Cn_beta=Cn_b,
               Cl_beta=Cl_b, static_margin_pct=None, x_np_mm=None)

    if CL_a not in (None, 0.0) and Cm_a is not None:
        sm = -Cm_a / CL_a
        x_np = x_ref + sm * CREF
        out["static_margin_pct"] = round(sm * 100, 2)
        out["x_np_mm"] = round(x_np * 1000, 1)
        print("\n=== LONGITUDINAL STABILITY ===")
        print(f"  Static margin = -Cm_a/CL_a = {sm*100:+.2f} % MAC")
        print(f"  Neutral point x_np = {x_np*1000:.1f} mm  (x_ref={x_ref*1000:.0f} mm)")
        print(f"  Audit analytical:  SM {AUDIT_SM_PCT:+.1f} % MAC, x_np {AUDIT_XNP_MM:.1f} mm")
        if sm > 0:
            print("  -> POSITIVE static margin (CG forward of NP): longitudinally stable.")
        else:
            print("  -> NEGATIVE static margin: UNSTABLE; move CG forward (battery fwd).")

    if Cn_b is not None:
        print("\n=== DIRECTIONAL ===")
        print(f"  Cn_beta = {Cn_b:+.4g} ->",
              "directionally stable" if Cn_b > 0
              else "directionally UNSTABLE (Vv~0.03 is low)")
    if Cl_b is not None:
        print(f"  Cl_beta = {Cl_b:+.4g} -> dihedral effect (sign per convention)")

    os.makedirs(DATADIR, exist_ok=True)
    with open(os.path.join(DATADIR, "vspaero_derivatives.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out.keys()))
        w.writeheader()
        w.writerow(out)
    print(f"\nWrote {os.path.join(DATADIR, 'vspaero_derivatives.csv')}")


if __name__ == "__main__":
    main()
