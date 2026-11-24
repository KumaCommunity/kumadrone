#!/usr/bin/env python3
"""
Preliminary structural screening for Kuma V5 Config B.
Loads, wing-root bending, spar stress, root-fastener loads, ruddervator
hinge moment and required servo torque. All assumptions stated in output.
"""
import math

G = 9.80665
MASS_EMPTY = 1.3079
MASS_LOADED = 1.8079
B_HALF = 0.650
SPAN = 1.30
S = 0.2275
MAC = 0.17619
TAIL_PANEL_AREA = 0.0396
TAIL_ROOT_C = 0.190
RUD_CHORD_FRAC = 0.234          # ruddervator = aft 23.4% of tail chord
BOLT_DX = (651 - 532) / 1000.0  # fore-aft M4 pair spacing 0.119 m


def spar_section(od_mm, id_mm):
    I = math.pi / 64 * (od_mm ** 4 - id_mm ** 4) * 1e-12  # m^4
    c = od_mm / 2 * 1e-3
    A = math.pi / 4 * (od_mm ** 2 - id_mm ** 2) * 1e-6
    return I, c, A


def main():
    print("ASSUMPTIONS: limit load factor n=+3.0 (manoeuvre), ultimate=1.5x=4.5;")
    print("Schrenk-ish root-bending factor 0.40; elliptical-ish load; symmetric lift.\n")
    for tag, m in [("empty", MASS_EMPTY), ("loaded+500g", MASS_LOADED)]:
        for n in [1.0, 3.0, 4.5]:
            L = m * G * n
            L_half = L / 2
            M_root = 0.40 * L_half * B_HALF      # N.m per half wing
            print(f"  {tag:12s} n={n:3.1f}: L_total={L:6.2f} N  L_half={L_half:6.2f} N  "
                  f"M_root~{M_root:5.2f} N.m")
        print()

    print("SPAR STRESS (8 mm main spar; M_root at n=4.5 ultimate, loaded):")
    L = MASS_LOADED * G * 4.5
    M_root = 0.40 * (L / 2) * B_HALF
    cases = [("carbon tube 8x6 (1mm wall)", 8, 6, 900e6),   # pultruded UTS ~0.9-1.5 GPa
             ("carbon tube 8x7 (0.5mm wall)", 8, 7, 900e6),
             ("solid Al 6061 8mm", 8, 0, 276e6),
             ("solid steel 8mm", 8, 0, 350e6)]
    for name, od, idm, allow in cases:
        I, c, A = spar_section(od, idm)
        sigma = M_root * c / I
        fs = allow / sigma
        print(f"  {name:32s} I={I*1e12:5.1f} mm^4  sigma={sigma/1e6:6.1f} MPa  "
              f"allow={allow/1e6:5.0f} MPa  FS~{fs:4.2f}")
    print("  (Carbon pultrusion is anisotropic; compressive/tube-crush and bonded")
    print("   joints usually govern before fibre UTS. FS shown is indicative only.)\n")

    print(f"ROOT FASTENER LOAD (4x M4, fore-aft pair spacing {BOLT_DX*1000:.0f} mm):")
    F = M_root / BOLT_DX
    print(f"  M_root(ult)={M_root:.2f} N.m -> couple force {F:.1f} N shared by 2 bolts")
    print(f"  per-bolt ~{F/2:.1f} N (bending only; add torsion/gust). M4 heat-set in")
    print("  PETG pull-out ~200-400 N; in LW-PLA far lower (<50-150 N). Adequate IF")
    print("  inserts are in PETG and the saddle plate is positively attached to the")
    print("  fuselage (currently NO modelled saddle-to-fuselage fastener: bonded only).\n")

    print("RUDDERVATOR HINGE / SERVO (per panel):")
    for V in [12, 14, 16]:
        q = 0.5 * 1.225 * V * V
        S_cs = TAIL_PANEL_AREA * RUD_CHORD_FRAC
        c_cs = RUD_CHORD_FRAC * TAIL_ROOT_C
        Ch = 0.15   # representative control-surface hinge-moment coefficient
        M_h = Ch * q * S_cs * c_cs
        print(f"  V={V} m/s: q={q:5.1f} Pa  S_cs={S_cs:.4f} m2  c_cs={c_cs*1000:.1f} mm  "
              f"M_hinge={M_h*100:.2f} N.cm")
    print("  A standard ~1.5-2.0 kg.cm (15-20 N.cm) micro servo has ample torque")
    print("  margin for these hinge moments, GIVEN a sound horn/pushrod (not modelled).")


if __name__ == "__main__":
    main()
