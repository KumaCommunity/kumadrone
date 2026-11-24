#!/usr/bin/env python3
"""
Hand-launch feasibility + lateral/directional screening for Kuma V5 Config B.

Hand launch: compares required release speed (multiple of stall, across CLmax
range) with realistic human hand-launch release speeds and energies for the
empty (1.31 kg) and 500 g-loaded (1.81 kg) cases.

Lateral-directional: estimates dihedral-effect Cl_beta range for a high wing
with 7 deg dihedral, rudder yaw authority, and discusses ruddervator-only roll.
All estimates labelled; no CFD / no flight data.

Outputs data/launch_lateral.csv and prints a report.
"""
import csv
import math
import os

HERE = os.path.dirname(__file__)
DATADIR = os.path.join(HERE, "..", "data")

RHO = 1.225
G = 9.80665
S = 0.2275          # m^2 wing area (verified)
B = 1.30            # m span
MAC = 0.17619       # m
MASS_EMPTY = 1.3079
MASS_LOADED = 1.8079


def stall_speed(m, clmax):
    return math.sqrt(2 * m * G / (RHO * S * clmax))


def main():
    rows = []
    # ---- hand-launch table ----
    print("=" * 74)
    print("HAND-LAUNCH FEASIBILITY")
    print("=" * 74)
    print("Required release speed modelled as k * Vstall. Achievable release speed")
    print("depends on BOTH throw skill AND motor thrust-to-weight (T/W): with high")
    print("T/W the throw only needs to clear stall momentarily (k ~ 0.9-1.0); with")
    print("low T/W it needs k ~ 1.3. Throw speed falls with mass (bulky airframe).\n")

    def throw_speed_range(m):
        # Athletic adult, wing-equipped model (bulky): plausible release m/s.
        if m <= 0.6:
            return 13.0, 19.0
        if m <= 1.0:
            return 11.0, 16.0
        if m <= 1.5:
            return 9.5, 14.0
        if m <= 2.0:
            return 8.0, 13.0
        return 7.0, 11.0

    print(f"  {'case':12s} {'mass':>6s} {'Vs(CL1.0)':>9s} {'throw(range)':>14s} "
          f"{'k=1.0':>6s} {'k=1.15':>7s} {'verdict':>22s}")
    for tag, m in [("empty", MASS_EMPTY), ("+100g", MASS_EMPTY + 0.1),
                   ("+250g", MASS_EMPTY + 0.25), ("+500g(loaded)", MASS_LOADED)]:
        vs = stall_speed(m, 1.0)
        vlo, vhi = throw_speed_range(m)
        vk10 = 1.00 * vs
        vk115 = 1.15 * vs
        # feasible if the BEST realistic throw clears 1.15*Vs; demanding if it
        # only clears 1.0*Vs; else short.
        if vhi >= vk115:
            verdict = "Feasible (can be demanding)"
        elif vhi >= vk10:
            verdict = "Demanding (needs T/W help)"
        else:
            verdict = "Short (needs unavoidably hard throw)"
        print(f"  {tag:12s} {m:6.2f} {vs:9.2f} {vlo:5.1f}-{vhi:5.1f} m/s "
              f"{vk10:6.2f} {vk115:7.2f}   {verdict}")
        for clmax in (1.0,):
            rows.append(dict(case=tag, mass_kg=round(m, 3), clmax=clmax,
                             vstall_m_s=round(vs, 2), throw_low_m_s=vlo, throw_high_m_s=vhi,
                             v_release_k10=round(vk10, 2), v_release_k115=round(vk115, 2),
                             ke_k115_J=round(0.5 * m * vk115 ** 2, 1),
                             wing_loading_kg_m2=round(m / S, 2)))

    print("\n  Honest reading (corrected from an earlier over-stated 'conflict'):")
    print("   - EMPTY (1.31 kg, WL 5.75 kg/m2): hand-launchable; a firm throw with")
    print("     modest T/W is enough. Comfortable for an experienced thrower.")
    print("   - +500 g (1.81 kg, WL 7.95 kg/m2): DEMANDING, not impossible. It is")
    print("     feasible with an athletic throw (~12-13 m/s) OR a firm throw")
    print("     (~10-11 m/s) plus T/W >~0.7 into wind. High wing loading leaves")
    print("     little margin; a weak throw risks a stall/drop. This is a handled")
    print("     RISK to validate (throw-speed + thrust-stand), NOT a hard conflict.")
    print("   - Internal vs external stowage is irrelevant to this: it is the added")
    print("     MASS that raises stall speed. Internal actually helps (less drag).")

    # ---- lateral / directional ----
    print("\n" + "=" * 74)
    print("LATERAL / DIRECTIONAL SCREENING (ruddervator-only)")
    print("=" * 74)
    # dihedral effect Cl_beta (per rad) - empirical range for high wing + 7 deg
    cl_beta_low = 0.08
    cl_beta_high = 0.16
    print(f"  Dihedral-effect Cl_beta estimate: +{cl_beta_low:.2f} to +{cl_beta_high:.2f} /rad")
    print("   (high wing gives base positive Cl_beta; 7 deg adds roll-due-to-sideslip)")
    # vertical tail volume already computed ~0.0297
    Vv = 0.0297
    print(f"  Vertical-tail volume Vv = {Vv:.3f}  (typical stable range ~0.03-0.05+)")
    # rudder yaw authority scale (qualitative)
    print("  V-tail vertical-equivalent area Sv = 0.0327 m2 on a 0.269 m arm.")
    print("\n  Findings:")
    print("   * Cl_beta is likely adequate to convert sideslip to bank.")
    print("   * Vv ~0.030 is at the low end of acceptable -> weak directional")
    print("     stability and weak/soft rudder authority; Dutch-roll and spiral")
    print("     tendencies unquantified.")
    print("   * With NO ailerons, roll is achieved only indirectly (rudder -> yaw")
    print("     -> sideslip -> dihedral roll). Roll response will be sluggish,")
    print("     require large coordinated inputs, and be poor in gusts/crosswind.")
    print("   * Differential ruddervator (yaw) couples into pitch; elevator (both)")
    print("     couples into yaw if asymmetric -> mixing-setup sensitivity.")
    print("   * For the 1.8 kg loaded case the reduced control margin is a")
    print("     handling-quality / safety concern.")
    print("  This concept is PLAUSIBLE only for calm-air, gentle flight; it is")
    print("  NOT substantiated for the full mass range and requires 6-DOF")
    print("  simulation and instrumented flight test before commitment.")

    with open(os.path.join(DATADIR, "launch_lateral.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- geometry clearances ----
    print("\n" + "=" * 74)
    print("CLEARANCES (from CAD parameters)")
    print("=" * 74)
    prop_d = 150.0
    prop_cz = 65.0
    prop_bottom = prop_cz - prop_d / 2
    fus_bottom = -84.0 / 2
    print(f"  Prop dia {prop_d:.0f} mm centred z={prop_cz:.0f} mm -> bottom z={prop_bottom:.0f} mm")
    print(f"  Fuselage max-dia belly z={fus_bottom:.0f} mm -> prop tip {prop_bottom-fus_bottom:+.0f} mm vs belly")
    print(f"  Prop disc at x=993 mm, {993-970:.0f} mm aft of fuselage tail (pusher)")
    print(f"  Wing tip rise (7 deg over 650 mm half-span) = {650*math.tan(math.radians(7)):.1f} mm")


if __name__ == "__main__":
    main()
