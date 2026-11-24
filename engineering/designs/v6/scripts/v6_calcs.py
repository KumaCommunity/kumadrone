#!/usr/bin/env python3
"""
V6 engineering recalculation (geometry, mass/CG, wing loading, stability).
Reads V5 mass_budget.csv, applies V6 changes (enlarged tail + new structure),
recomputes. Python runs even though OpenSCAD is unavailable here.
Writes v6/data/*.csv and prints a V5 -> V6 comparison.
"""
import csv
import math
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DATADIR = os.path.join(HERE, "..", "data")

RHO, G = 1.225, 9.80665

# wing (unchanged from V5)
b = 1.30; S = 0.2275; MAC = 176.19; LE_MAC = 507.43; X_AC_W = 551.48; AR_W = 7.4286
# tail (V6 enlarged)
t_span = 300.0; t_rc = 200.0; t_tc = 150.0; t_dih = 47.0  # V6.1: span 270->300, 45->47
t_LEr = 750 + 20; t_LEt = 768 + 20


def tail_geom():
    g = math.radians(t_dih)
    S_panel = t_span * (t_rc + t_tc) / 2 / 1e6
    S_tot = 2 * S_panel
    lam = t_tc / t_rc
    MACt = (2 / 3) * t_rc * (1 + lam + lam ** 2) / (1 + lam)
    Sh = S_tot * math.cos(g) ** 2
    Sv = S_tot * math.sin(g) ** 2
    SMAC = t_span * (1 + 2 * lam) / (3 * (1 + lam))
    LE_MACt = t_LEr + (t_LEt - t_LEr) * SMAC / t_span
    x_ac_t = LE_MACt + 0.25 * MACt
    y_tip = 12 + t_span * math.cos(g)
    bh = 2 * y_tip
    ARh = (bh / 1000) ** 2 / Sh
    l = (x_ac_t - X_AC_W) / 1000.0
    Vh = Sh * l / (S * MAC / 1000)
    Vv = Sv * l / (S * b)
    return dict(S_panel=S_panel, S_tot=S_tot, MACt=MACt, Sh=Sh, Sv=Sv,
                x_ac_t=x_ac_t, y_tip=y_tip, bh=bh, ARh=ARh, l=l, Vh=Vh, Vv=Vv)


def a3d(a0, AR, e=0.85):
    return a0 / (1 + a0 / (math.pi * AR * e))


def stability(tg):
    aw = a3d(5.7, AR_W, 0.85)
    at = a3d(5.0, tg["ARh"], 0.80)
    x_np = (aw * S * X_AC_W + at * 0.9 * tg["Sh"] * tg["x_ac_t"] * 0.7) / \
           (aw * S + at * 0.9 * tg["Sh"] * 0.7)
    return aw, at, x_np


def load_v5():
    with open(os.path.join(ROOT, "mass_budget.csv")) as fh:
        return list(csv.DictReader(fh))


NEW_PARTS = [
    ("wing_saddle_clamp", 22.0, 590.0, "LW body + PETG pads (I-01)"),
    ("centre_spar_joiner", 12.0, 580.0, "PETG sleeves + pin (I-02)"),
    ("wing_center_spar_sleeve", 6.0, 580.0, "PETG collars (I-23)"),
    ("motor_bulkhead", 8.0, 952.0, "PETG firewall (I-09)"),
    ("camera_cradle", 6.0, 38.0, "PETG bracket (I-07)"),
    ("battery_hatch_lid", 6.0, 452.0, "LW-PLA lid (I-08)"),
    ("tail_root_spar", 3.0, 810.0, "carbon pin (I-03)"),
    ("ruddervator_hinges(2)", 6.0, 918.0, "PETG knuckles+pin (I-05)"),
    ("control_horns(2)", 2.0, 915.0, "PETG (I-05)"),
    ("pushrod_channels(2)", 4.0, 850.0, "tube (I-05)"),
    ("secured_tray_addon", 5.0, 556.0, "PETG bosses (I-10)"),
]


def mass_cg(extra_g=0.0, extra_x=556.0):
    rows = load_v5()
    old_panel = 0.240 * (0.190 + 0.140) / 2
    new_panel = (t_span * (t_rc + t_tc) / 2) / 1e6
    scale = new_panel / old_panel
    m = 0.0; mx = 0.0; detail = []
    for r in rows:
        item = r["item"]; x = float(r["x_mm"]); mass = float(r["total_mass_g"])
        if item.startswith("Example 3S"):      # V6.1: battery moved fwd to X for CG margin
            x = 285.0
        if item in ("tail_L", "tail_R", "ruddervator_L", "ruddervator_R"):
            mass *= scale
        m += mass; mx += mass * x
        detail.append((item, mass, x, r["category"]))
    for name, mass, x, note in NEW_PARTS:
        m += mass; mx += mass * x
        detail.append((name, mass, x, "V6new"))
    if extra_g:
        m += extra_g; mx += extra_x * extra_g
    return m, mx / m, detail, scale


def main():
    os.makedirs(DATADIR, exist_ok=True)
    tg = tail_geom()
    aw, at, x_np = stability(tg)
    m0, cg0, detail, scale = mass_cg()
    v5rows = load_v5()
    v5m = sum(float(r["total_mass_g"]) for r in v5rows)
    v5cg = sum(float(r["total_mass_g"]) * float(r["x_mm"]) for r in v5rows) / v5m

    def wl(m): return m / (S * 100.0)
    def vs(m, cl=1.0): return math.sqrt(2 * (m / 1000) * G / (RHO * S * cl))

    print("=" * 70); print("V6 GEOMETRY / STABILITY"); print("=" * 70)
    print(f"  Wing: span {b} m, S {S} m2, AR {AR_W}, MAC {MAC} mm (unchanged)")
    print(f"  Tail V6: span {t_span} mm, chords {t_rc}/{t_tc}, dihedral {t_dih} deg")
    print(f"    panel {tg['S_panel']:.4f} total {tg['S_tot']:.4f} m2 (V5 0.0792)")
    print(f"    Sh {tg['Sh']:.4f} Sv {tg['Sv']:.4f} m2  horiz AR {tg['ARh']:.2f}")
    print(f"    tail AC x {tg['x_ac_t']:.1f} mm  arm {tg['x_ac_t']-X_AC_W:.1f} mm")
    print(f"    Vh {tg['Vh']:.3f}  Vv {tg['Vv']:.3f}  (V5 Vh 0.31 / Vv 0.030)")
    print(f"    a_w {aw:.2f} a_t {at:.2f} /rad  x_np {x_np:.1f} mm")
    sm = (x_np - cg0) / MAC * 100
    print(f"    -> static margin (empty) {sm:+.2f} % MAC")

    print("\n" + "=" * 70); print("V6 MASS / CG / LOADING (estimated)"); print("=" * 70)
    print(f"  tail area scale {scale:.3f}")
    print(f"  V5 empty {v5m:7.1f} g @ CG {v5cg:6.2f} mm")
    print(f"  V6 empty {m0:7.1f} g @ CG {cg0:6.2f} mm  (delta +{m0-v5m:.1f} g)")
    for name, mass, x, n in detail:
        if n == "V6new":
            print(f"     {name:26s} {mass:5.1f} g @ x={x:.0f}")
    for extra in (0, 100, 250, 500):
        mm, cc, _, _ = mass_cg(extra)
        print(f"  +{extra:3d} g: {mm:7.1f} g  CG {cc:6.1f} mm ({((cc-LE_MAC)/MAC*100):4.1f}%MAC)"
              f"  WL {wl(mm):5.1f} g/dm2  Vs {vs(mm):5.2f} m/s")

    with open(os.path.join(DATADIR, "v6_geometry.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["quantity", "value", "note"])
        for k, v, note in [("tail_span_mm", t_span, ""), ("tail_root_chord_mm", t_rc, ""),
                     ("tail_tip_chord_mm", t_tc, ""), ("tail_dihedral_deg", t_dih, ""),
                     ("tail_S_total_m2", round(tg["S_tot"], 5), "V5 0.0792"),
                     ("Sh_m2", round(tg["Sh"], 5), ""), ("Sv_m2", round(tg["Sv"], 5), ""),
                     ("horiz_AR", round(tg["ARh"], 3), ""),
                     ("tail_AC_x_mm", round(tg["x_ac_t"], 2), ""),
                     ("tail_arm_mm", round(tg["x_ac_t"] - X_AC_W, 2), ""),
                     ("Vh", round(tg["Vh"], 4), "V5 0.31"), ("Vv", round(tg["Vv"], 4), "V5 0.030"),
                     ("a_w_per_rad", round(aw, 3), ""), ("a_t_per_rad", round(at, 3), ""),
                     ("x_np_mm", round(x_np, 2), "provisional"), ("SM_empty_pct", round(sm, 2), "")]:
            w.writerow([k, v, note])
    with open(os.path.join(DATADIR, "v6_loading.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["equipment_g", "mass_g", "cg_mm", "cg_pct_MAC",
                                        "wl_g_dm2", "Vs_m_s_CL1.0"])
        for extra in (0, 100, 250, 500):
            mm, cc, _, _ = mass_cg(extra)
            w.writerow([extra, round(mm, 1), round(cc, 2), round((cc - LE_MAC) / MAC * 100, 2),
                        round(wl(mm), 1), round(vs(mm), 2)])
    with open(os.path.join(DATADIR, "v6_mass_detail.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["item", "mass_g", "x_mm", "category"])
        for name, mass, x, cat in detail:
            w.writerow([name, round(mass, 2), x, cat])
    print("\nWrote v6_geometry.csv, v6_loading.csv, v6_mass_detail.csv")


if __name__ == "__main__":
    main()
