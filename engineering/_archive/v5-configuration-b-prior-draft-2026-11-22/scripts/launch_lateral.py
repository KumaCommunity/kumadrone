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
    print("Required release speed modelled as k * Vstall (k = 1.15, 1.30).")
    print("Achievable release speeds: typical adult underhand ~6-8 m/s for a")
    print("~1.3 kg model, ~8-10 m/s for a hard athletic throw; a ~1.8 kg model")
    print("realistically tops out near 6-8 m/s (energy-limited).\n")
    for tag, m in [("empty", MASS_EMPTY), ("loaded_500g", MASS_LOADED)]:
        for clmax in [0.9, 1.0, 1.1, 1.2]:
            vs = stall_speed(m, clmax)
            v115 = 1.15 * vs
            v130 = 1.30 * vs
            ke115 = 0.5 * m * v115 ** 2
            ke130 = 0.5 * m * v130 ** 2
            row = dict(case=tag, mass_kg=m, clmax=clmax, vstall_m_s=round(vs, 2),
                       v_release_115_m_s=round(v115, 2), v_release_130_m_s=round(v130, 2),
                       ke_release_115_J=round(ke115, 1), ke_release_130_J=round(ke130, 1),
                       wing_loading_kg_m2=round(m / S, 2))
            rows.append(row)
            if clmax == 1.0:
                print(f"  {tag:12s} CLmax1.0: Vs={vs:5.2f}  launch(1.15x)={v115:5.2f}  "
                      f"launch(1.3x)={v130:5.2f} m/s   KE@1.3x={ke130:5.0f} J  "
                      f"WL={m/S:4.1f} kg/m2")

    # feasibility verdict
    print("\n  Judgement (energy-limited, typical throw KE for these masses):")
    print("   - EMPTY: marginal. Needs a hard, well-aimed throw; below-margin")
    print("            launches likely to stall. Wing loading 5.7 kg/m2 is high")
    print("            for routine hand launch (foam hand-launch <~3-4.5 kg/m2).")
    print("   - LOADED (+500 g): NOT hand-launchable by a person. Wing loading")
    print("            7.95 kg/m2 and required ~13-15 m/s release exceed realistic")
    print("            throw speed/energy. No launcher permitted -> requirement")
    print("            conflict.")

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
