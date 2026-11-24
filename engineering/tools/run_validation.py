#!/usr/bin/env python3
"""
One-command validation suite for the Kuma FPV project.
Runs deterministic checks against the source + generated outputs and prints PASS/FAIL.
Exit code 0 = all pass, 1 = one or more fail. Does NOT need OpenSCAD/OpenVSP (uses
already-exported STLs and saved VSPAERO polars). Requires: numpy, trimesh, matplotlib.
"""
import os
import re
import sys
import subprocess
import math

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUD = os.path.join(ROOT, "engineering/audits/v5-configuration-b/scripts")
V6S = os.path.join(ROOT, "engineering/designs/v6/scripts")
sys.path.insert(0, AUD)
sys.path.insert(0, V6S)

results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except Exception as e:  # noqa
        ok, detail = False, f"EXC {type(e).__name__}: {e}"
    results.append((name, ok, detail))


def approx(v, target, tol):
    return abs(v - target) <= tol


def brace_balance(path):
    s = open(path).read()
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"//[^\n]*", "", s)
    return all(s.count(o) == s.count(c) for o, c in [("(", ")"), ("[", "]"), ("{", "}")])


def main():
    import numpy as np
    import trimesh
    import audit_calcs as ac
    import verify_airfoil as va
    import v6_calcs as v6
    import parse_vspaero as pv

    # 1-3 wing geometry
    wg = ac.wing_geometry()
    check("wing area = 0.2275 m2", lambda: (approx(wg["S_m2"], 0.2275, 1e-4), f"{wg['S_m2']:.5f}"))
    check("aspect ratio = 7.43", lambda: (approx(wg["AR"], 7.4286, 0.02), f"{wg['AR']:.3f}"))
    check("MAC = 176.19 mm", lambda: (approx(wg["MAC_mm"], 176.19, 0.2), f"{wg['MAC_mm']:.2f}"))

    # 4-5 airfoils
    w = va.analyze("2412", os.path.join(va.ROOT, "NACA_2412_Wing_Root_200mm.dxf"), 200.0, 0.12, 0.02, 0.40)
    t = va.analyze("0010", os.path.join(va.ROOT, "NACA_0010_Tail_Root_190mm.dxf"), 190.0, 0.10, 0.0, 0.40)
    check("NACA2412 t/c = 12%", lambda: (approx(w["max_thickness_pct_chord"], 12.0, 0.1),
                                        f"{w['max_thickness_pct_chord']:.3f}"))
    check("NACA0010 t/c = 10%", lambda: (approx(t["max_thickness_pct_chord"], 10.0, 0.1),
                                        f"{t['max_thickness_pct_chord']:.3f}"))

    # 6 V6 stability (analytical/VLM-class)
    tg = v6.tail_geom()
    check("V6.1 tail Vv ~ 0.051", lambda: (approx(tg["Vv"], 0.051, 0.005), f"{tg['Vv']:.4f}"))
    check("V6.1 tail Vh ~ 0.330", lambda: (approx(tg["Vh"], 0.330, 0.02), f"{tg['Vh']:.4f}"))

    # 7 VSPAERO alpha static margin from saved polar
    def vsp_sm():
        f = os.path.join(ROOT, "engineering/designs/v6/data/vspaero/V6.1_alpha.polar")
        hdr, rows = pv.read_table(f)
        a = [r[pv.col(hdr, "aoa")] for r in rows]
        cl = [r[pv.col(hdr, "cltot")] for r in rows]
        cm = [r[pv.col(hdr, "cmytot")] for r in rows]
        cla = np.polyfit(a, cl, 1)[0]; cma = np.polyfit(a, cm, 1)[0]
        sm = -cma / cla; xnp = 560 + sm * 176.19
        return approx(xnp, 557.1, 2.5), f"panel x_np {xnp:.1f}mm (SM@560 {sm*100:+.2f}%)"
    check("VSPAERO panel x_np ~ 557 mm", vsp_sm)

    # 8 V6 verified mass via verify_v6_stl
    def v6_mass():
        out = subprocess.run([sys.executable, os.path.join(V6S, "verify_v6_stl.py")],
                             capture_output=True, text=True).stdout
        m = re.search(r"V6 EMPTY.*?([0-9]+\.[0-9]+) g", out)
        over = re.search(r"over 220 bed \((\d+)\)", out)
        ok = m and approx(float(m.group(1)), 1366.15, 4) and over and over.group(1) == "0"
        return bool(ok), f"mass {m.group(1) if m else '?'} g, over={over.group(1) if over else '?'}"
    check("V6.1 empty mass ~1366.2 g, 0 over-bed", v6_mass)

    # 9 V5 STL watertightness (all 32)
    def v5_wt():
        files = [f for f in os.listdir(os.path.join(ROOT, "STL")) if f.endswith(".stl")]
        bad = 0
        for f in files:
            m = trimesh.load(os.path.join(ROOT, "STL", f), force="mesh")
            if not m.is_watertight:
                bad += 1
        return (len(files) == 32 and bad == 0), f"{len(files)} files, {bad} not watertight"
    check("V5 32 STLs watertight", v5_wt)

    # 10 SCAD syntax balance
    check("V5 SCAD delimiters balanced",
          lambda: (brace_balance(os.path.join(ROOT, "Kuma_FPV_V5_Configuration_B.scad")), ""))
    check("V6 SCAD delimiters balanced",
          lambda: (brace_balance(os.path.join(ROOT, "engineering/designs/v6/Kuma_FPV_V6_Configuration_B.scad")), ""))

    # 11 V6 STL count
    def v6_parts():
        n = len([f for f in os.listdir(os.path.join(ROOT, "engineering/designs/v6/STL")) if f.endswith(".stl")])
        return (n == 44), f"{n} STLs"
    check("V6 44 STLs exported", v6_parts)

    # ---- report ----
    npass = sum(1 for _, ok, _ in results if ok)
    print("=" * 74)
    print(f"KUMA FPV VALIDATION SUITE  —  {npass}/{len(results)} PASS")
    print("=" * 74)
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:42s} {detail}")
    print("=" * 74)
    env = f"python {sys.version.split()[0]} | numpy {np.__version__} | trimesh {trimesh.__version__}"
    print("ENV:", env)
    print("OpenSCAD:", "yes" if _which("openscad") else "no",
          "| OpenVSP app:", "yes" if os.path.exists("/Applications/OpenVSP.app") else "no")
    return 0 if npass == len(results) else 1


def _which(x):
    from shutil import which
    return which(x)


if __name__ == "__main__":
    sys.exit(main())
