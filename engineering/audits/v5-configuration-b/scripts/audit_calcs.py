#!/usr/bin/env python3
"""
Kuma FPV V5 Configuration B - independent engineering recalculation engine.

Recomputes, from first principles, the geometry, internal volumes, mass & balance,
preliminary aerodynamics (lift, Re, stall, drag, glide) and static stability
(neutral point / static margin, tail volumes, dihedral effect).

All inputs are pulled from the SCAD source parameters and the raw STL verification;
purchased-component masses/stations are read from mass_budget.csv (flagged as
estimated). Nothing is copied from the existing metrics.json / CSVs.

Writes:
  data/geometry_derived.csv
  data/fuselage_stations.csv
  data/mass_balance_recomputed.csv
  data/aero_screening.csv
  data/stability.csv
"""
import csv
import json
import math
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DATADIR = os.path.join(HERE, "..", "data")

RHO = 1.225          # kg/m^3 sea level ISA
G = 9.80665          # m/s^2

# ---------------- SCAD source parameters (verbatim) ----------------
L = 970.0
b2 = 650.0
root_c = 200.0
tip_c = 150.0
dihedral_deg = 7.0
wing_shift = 186.0
tail_shift = 20.0
LEr = 310.0 + wing_shift        # 496
LEt = 334.0 + wing_shift        # 520
root_z = 56.0
wall = 1.25
tail_span = 240.0
tail_root_chord = 190.0
tail_tip_chord = 140.0
tail_dihedral_deg = 40.0        # each panel from horizontal
body_cuts = [0, 180, 360, 540, 720, 900, 970]
body_sections = [(0, 12), (30, 20), (80, 34), (155, 40), (350, 42),
                 (500, 40), (700, 31), (850, 23), (900, 21), (970, 18)]

# ---------------- geometry ----------------
def lerp(a, b, u):
    return a + (b - a) * u


def r_body(x):
    secs = body_sections
    if x <= secs[0][0]:
        return secs[0][1]
    if x >= secs[-1][0]:
        return secs[-1][1]
    for i in range(len(secs) - 1):
        if secs[i][0] <= x <= secs[i + 1][0]:
            u = (x - secs[i][0]) / (secs[i + 1][0] - secs[i][0])
            return lerp(secs[i][1], secs[i + 1][1], u)
    return secs[-1][1]


def wing_geometry():
    b = 2 * b2
    lam = tip_c / root_c
    S = b * (root_c + tip_c) / 2.0 / 1e6            # m^2
    AR = (b / 1000.0) ** 2 / S
    MAC = (2.0 / 3.0) * root_c * (1 + lam + lam ** 2) / (1 + lam)  # mm
    SMAC = (b2) * (1 + 2 * lam) / (3 * (1 + lam))    # spanwise MAC station mm
    LE_MAC = lerp(LEr, LEt, SMAC / b2)               # LE x at MAC station
    x_ac_wing = LE_MAC + 0.25 * MAC                  # 25% MAC (4-digit AC)
    # sweep of leading edge over half span
    le_sweep_deg = math.degrees(math.atan2(LEt - LEr, b2))
    tip_rise = b2 * math.tan(math.radians(dihedral_deg))
    d = dict(b=b, half_span=b2, root_c=root_c, tip_c=tip_c, taper=lam, S_m2=S,
             AR=AR, MAC_mm=MAC, MAC_station_y_mm=SMAC, LE_MAC_x_mm=LE_MAC,
             x_ac_wing_mm=x_ac_wing, le_sweep_deg=le_sweep_deg,
             tip_rise_mm=tip_rise, LE_root_x_mm=LEr, LE_tip_x_mm=LEt,
             root_z_mm=root_z, tip_z_mm=root_z + tip_rise)
    return d


def tail_geometry():
    gam = math.radians(tail_dihedral_deg)
    S_panel = tail_span * (tail_root_chord + tail_tip_chord) / 2.0 / 1e6  # m^2
    S_total = 2 * S_panel
    lam = tail_tip_chord / tail_root_chord
    MAC = (2.0 / 3.0) * tail_root_chord * (1 + lam + lam ** 2) / (1 + lam)
    # tail panel: horizontal/vertical projections (area x cos / sin of panel tilt)
    Sh_proj_area = S_total * math.cos(gam)            # pure area projection
    Sv_proj_area = S_total * math.sin(gam)
    Sh_equiv = S_total * math.cos(gam) ** 2           # cos^2 proxy used in docs
    Sv_equiv = S_total * math.sin(gam) ** 2           # sin^2 proxy used in docs
    # horizontal projected span (centre gap 2*12 mm at roots)
    y_root = 12.0
    y_tip = y_root + tail_span * math.cos(gam)
    b_h = 2 * y_tip
    AR_h = (b_h / 1000.0) ** 2 / max(Sh_equiv, 1e-9)
    # tail MAC LE x (root LE 770 -> tip LE 788)
    LE_root = 750 + tail_shift
    LE_tip = 768 + tail_shift
    SMAC = tail_span * (1 + 2 * lam) / (3 * (1 + lam))
    LE_MAC = lerp(LE_root, LE_tip, SMAC / tail_span)
    x_ac_tail = LE_MAC + 0.25 * MAC
    z_tip = 26 + tail_span * math.sin(gam)
    d = dict(S_panel_m2=S_panel, S_total_m2=S_total, taper=lam, MAC_mm=MAC,
             Sh_proj_area_m2=Sh_proj_area, Sv_proj_area_m2=Sv_proj_area,
             Sh_equiv_m2=Sh_equiv, Sv_equiv_m2=Sv_equiv, b_h_mm=b_h, AR_h=AR_h,
             LE_root_x_mm=LE_root, LE_tip_x_mm=LE_tip, x_ac_tail_mm=x_ac_tail,
             z_tip_mm=z_tip, y_tip_mm=y_tip)
    return d


def fuselage_volumes():
    """Discretise the body-of-revolution to get gross + internal volumes."""
    rows = []
    # fine Simpson-ish integration of pi*r^2 over x
    n = 9700
    dx = L / n
    V_ext = 0.0
    V_int = 0.0
    A_wet = 0.0
    for k in range(n):
        x = (k + 0.5) * dx
        r = r_body(x)
        ri = max(0.05, r - wall)
        V_ext += math.pi * r * r * dx
        V_int += math.pi * ri * ri * dx
        # lateral surface area of revolution
        x2 = x + dx
        dr = r_body(x2) - r_body(x)
        ds = math.hypot(dx, dr)
        A_wet += 2 * math.pi * r * ds
    # per-cut segment internal volumes
    for i in range(len(body_cuts) - 1):
        x0, x1 = body_cuts[i], body_cuts[i + 1]
        nn = 2000
        ddx = (x1 - x0) / nn
        vi = 0.0
        for k in range(nn):
            x = x0 + (k + 0.5) * ddx
            ri = max(0.05, r_body(x) - wall)
            vi += math.pi * ri * ri * ddx
        rows.append(dict(section=i, x0=x0, x1=x1, length_mm=x1 - x0,
                         r_avg_mm=round((r_body(x0) + r_body(x1)) / 2, 2),
                         internal_volume_cm3=round(vi / 1000.0, 2)))
    summ = dict(V_ext_cm3=V_ext / 1000.0, V_int_cm3=V_int / 1000.0,
                A_wet_cm2=A_wet / 100.0,
                max_radius_mm=max(r for _, r in body_sections),
                max_diameter_mm=2 * max(r for _, r in body_sections))
    return rows, summ



# ---------------- mass & balance ----------------
def load_mass_budget():
    path = os.path.join(ROOT, "mass_budget.csv")
    rows = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            r["total_mass_g"] = float(r["total_mass_g"])
            r["x_mm"] = float(r["x_mm"])
            rows.append(r)
    return rows


def mass_balance(extra_g=0.0, extra_x=556.0):
    rows = load_mass_budget()
    m = sum(r["total_mass_g"] for r in rows)
    mx = sum(r["total_mass_g"] * r["x_mm"] for r in rows)
    printed = sum(r["total_mass_g"] for r in rows if r["category"] in ("LW-PLA", "PETG"))
    purchased = sum(r["total_mass_g"] for r in rows if r["category"] == "Unselected equipment")
    print_lw = sum(r["total_mass_g"] for r in rows if r["category"] == "LW-PLA")
    print_petg = sum(r["total_mass_g"] for r in rows if r["category"] == "PETG")
    if extra_g:
        m += extra_g
        mx += extra_g * extra_x
    return dict(total_g=m, cg_x=mx / m, printed_g=printed, purchased_g=purchased,
                lw_g=print_lw, petg_g=print_petg, mass_moment=mx)


# ---------------- aerodynamics ----------------
def aero_screening(mass_g):
    w = mass_g / 1000.0 * G
    S = wing_geometry()["S_m2"]
    MAC = wing_geometry()["MAC_mm"] / 1000.0
    rows = []
    for V in [8, 9, 10, 11, 12, 13, 14, 16, 18]:
        q = 0.5 * RHO * V * V
        CL = w / (q * S)
        Re = RHO * V * MAC / 1.81e-5
        rows.append(dict(airspeed_m_s=V, q_Pa=round(q, 3), CL_req=round(CL, 4),
                         Re=round(Re, 0), lift_N=round(w, 3)))
    return rows, w


def stall_speed(mass_g, CLmax):
    w = mass_g / 1000.0 * G
    S = wing_geometry()["S_m2"]
    return math.sqrt(2 * w / (RHO * S * CLmax))


def glide_and_drag(mass_g, V, e=0.85):
    wg = wing_geometry()
    S, AR = wg["S_m2"], wg["AR"]
    w = mass_g / 1000.0 * G
    q = 0.5 * RHO * V * V
    CL = w / (q * S)
    CD0 = 0.038
    CDi = CL * CL / (math.pi * AR * e)
    CD = CD0 + CDi
    D = q * S * CD
    return dict(CL=CL, CD0=CD0, CDi=CDi, CD=CD, drag_N=D, L_over_D=w / D)


# ---------------- stability ----------------
def lift_slope_3d(a0_per_rad, AR, e=0.85):
    return a0_per_rad / (1.0 + a0_per_rad / (math.pi * AR * e))


def neutral_point(a_w, a_t, eta, deps, S, Sh, x_ac_w, x_ac_t):
    num = a_w * S * x_ac_w + a_t * eta * Sh * x_ac_t * (1 - deps)
    den = a_w * S + a_t * eta * Sh * (1 - deps)
    return num / den


def stability_block():
    wg = wing_geometry()
    tg = tail_geometry()
    S, Sh, Sv, b = wg["S_m2"], tg["Sh_equiv_m2"], tg["Sv_equiv_m2"], wg["b"] / 1000.0
    MAC = wg["MAC_mm"]
    a_w_sec = 5.7
    a_w = lift_slope_3d(a_w_sec, wg["AR"], e=0.85)
    a_t_sec = 5.0
    a_t = lift_slope_3d(a_t_sec, tg["AR_h"], e=0.80)
    l_t = (tg["x_ac_tail_mm"] - wg["x_ac_wing_mm"]) / 1000.0
    Vh = Sh * l_t / (S * MAC / 1000.0)
    Vv = Sv * l_t / (S * b)
    x_np = neutral_point(a_w, a_t, 0.90, 0.30, S, Sh,
                         wg["x_ac_wing_mm"], tg["x_ac_tail_mm"])
    sweep = []
    for deps in [0.10, 0.15, 0.20, 0.25, 0.30, 0.40]:
        for a_t_scale in [0.7, 0.85, 1.0]:
            at = a_t * a_t_scale
            xn = neutral_point(a_w, at, 0.90, deps, S, Sh,
                               wg["x_ac_wing_mm"], tg["x_ac_tail_mm"])
            sweep.append(dict(deps=deps, a_t_scale=a_t_scale, a_t=round(at, 3),
                              x_np_mm=round(xn, 2)))
    return dict(a_w=round(a_w, 3), a_t=round(a_t, 3), l_t_m=round(l_t, 4),
                Vh=round(Vh, 4), Vv=round(Vv, 4), Sh_m2=Sh, Sv_m2=Sv,
                x_ac_w=round(wg["x_ac_wing_mm"], 2),
                x_ac_t=round(tg["x_ac_tail_mm"], 2), x_np_nominal=round(x_np, 2),
                sweep=sweep, MAC=MAC)


# ---------------- driver ----------------
def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    wg = wing_geometry()
    tg = tail_geometry()
    frows, fsum = fuselage_volumes()
    stab = stability_block()

    geom = [
        dict(quantity="Wingspan_mm", value=round(wg["b"], 2), unit="mm"),
        dict(quantity="Wing_root_chord_mm", value=wg["root_c"], unit="mm"),
        dict(quantity="Wing_tip_chord_mm", value=wg["tip_c"], unit="mm"),
        dict(quantity="Wing_taper_ratio", value=round(wg["taper"], 4), unit="-"),
        dict(quantity="Wing_area_m2", value=round(wg["S_m2"], 5), unit="m^2"),
        dict(quantity="Aspect_ratio", value=round(wg["AR"], 3), unit="-"),
        dict(quantity="MAC_mm", value=round(wg["MAC_mm"], 2), unit="mm"),
        dict(quantity="MAC_span_station_mm", value=round(wg["MAC_station_y_mm"], 2), unit="mm"),
        dict(quantity="Wing_root_LE_x_mm", value=wg["LE_root_x_mm"], unit="mm"),
        dict(quantity="Wing_tip_LE_x_mm", value=wg["LE_tip_x_mm"], unit="mm"),
        dict(quantity="Wing_LE_sweep_deg", value=round(wg["le_sweep_deg"], 3), unit="deg"),
        dict(quantity="Wing_MAC_LE_x_mm", value=round(wg["LE_MAC_x_mm"], 2), unit="mm"),
        dict(quantity="Wing_AC_25pct_MAC_x_mm", value=round(wg["x_ac_wing_mm"], 2), unit="mm"),
        dict(quantity="Wing_dihedral_deg", value=dihedral_deg, unit="deg"),
        dict(quantity="Wing_tip_rise_mm", value=round(wg["tip_rise_mm"], 2), unit="mm"),
        dict(quantity="Wing_incidence_deg", value=0.0, unit="deg"),
        dict(quantity="Wing_twist_deg", value=0.0, unit="deg"),
        dict(quantity="Tail_panel_area_m2", value=round(tg["S_panel_m2"], 5), unit="m^2"),
        dict(quantity="Tail_total_area_m2", value=round(tg["S_total_m2"], 5), unit="m^2"),
        dict(quantity="Tail_dihedral_each_deg", value=tail_dihedral_deg, unit="deg"),
        dict(quantity="Tail_Sh_area_projection_m2", value=round(tg["Sh_proj_area_m2"], 5), unit="m^2"),
        dict(quantity="Tail_Sh_cos2_proxy_m2", value=round(tg["Sh_equiv_m2"], 5), unit="m^2"),
        dict(quantity="Tail_Sv_sin2_proxy_m2", value=round(tg["Sv_equiv_m2"], 5), unit="m^2"),
        dict(quantity="Tail_horiz_span_mm", value=round(tg["b_h_mm"], 2), unit="mm"),
        dict(quantity="Tail_horiz_AR_cos2", value=round(tg["AR_h"], 3), unit="-"),
        dict(quantity="Tail_MAC_mm", value=round(tg["MAC_mm"], 2), unit="mm"),
        dict(quantity="Tail_AC_25pct_MAC_x_mm", value=round(tg["x_ac_tail_mm"], 2), unit="mm"),
        dict(quantity="Tail_arm_wing_AC_to_tail_AC_mm", value=round(tg["x_ac_tail_mm"] - wg["x_ac_wing_mm"], 2), unit="mm"),
        dict(quantity="Tail_tip_z_mm", value=round(tg["z_tip_mm"], 2), unit="mm"),
        dict(quantity="Fuselage_length_mm", value=L, unit="mm"),
        dict(quantity="Fuselage_max_diameter_mm", value=round(fsum["max_diameter_mm"], 2), unit="mm"),
        dict(quantity="Fuselage_internal_volume_cm3", value=round(fsum["V_int_cm3"], 1), unit="cm^3"),
        dict(quantity="Fuselage_wetted_area_cm2", value=round(fsum["A_wet_cm2"], 1), unit="cm^2"),
    ]
    write_csv(os.path.join(DATADIR, "geometry_derived.csv"), geom)
    write_csv(os.path.join(DATADIR, "fuselage_stations.csv"), frows)

    mb = mass_balance()
    mb_rows = []
    for tag, extra in [("empty_0g", 0), ("light_100g", 100),
                       ("medium_250g", 250), ("max_500g", 500)]:
        r = mass_balance(extra_g=extra, extra_x=556.0) if extra else mass_balance()
        wl = r["total_g"] / (wg["S_m2"] * 100.0)
        st = stall_speed(r["total_g"], 1.0)
        mb_rows.append(dict(case=tag, equipment_g=extra, total_mass_g=round(r["total_g"], 2),
                            cg_x_mm=round(r["cg_x"], 2),
                            cg_pct_MAC=round((r["cg_x"] - wg["LE_MAC_x_mm"]) / wg["MAC_mm"] * 100, 2),
                            wing_loading_g_dm2=round(wl, 2),
                            stall_m_s_CLmax1=round(st, 2)))
    write_csv(os.path.join(DATADIR, "mass_balance_recomputed.csv"), mb_rows)

    aero_rows = []
    for tag, mass in [("empty", mb["total_g"]), ("max_500g", mb["total_g"] + 500)]:
        rows, w = aero_screening(mass)
        for r in rows:
            r["case"] = tag
            r["wing_loading_g_dm2"] = round(mass / (wg["S_m2"] * 100), 2)
            aero_rows.append(r)
    write_csv(os.path.join(DATADIR, "aero_screening.csv"), aero_rows)

    write_csv(os.path.join(DATADIR, "stability.csv"), stab["sweep"])
    report(wg, tg, frows, fsum, stab, mb, mb_rows)



def report(wg, tg, frows, fsum, stab, mb, mb_rows):
    line = "=" * 78
    print(line)
    print("GEOMETRY (recomputed from SCAD parameters)")
    print(line)
    for g in []:
        pass
    print(f"  Wingspan                : {wg['b']:.1f} mm")
    print(f"  Root / tip chord        : {wg['root_c']:.1f} / {wg['tip_c']:.1f} mm  taper {wg['taper']:.3f}")
    print(f"  Wing area               : {wg['S_m2']:.5f} m^2")
    print(f"  Aspect ratio            : {wg['AR']:.3f}")
    print(f"  MAC                     : {wg['MAC_mm']:.2f} mm at y={wg['MAC_station_y_mm']:.1f} mm")
    print(f"  Root LE / tip LE x      : {wg['LE_root_x_mm']:.1f} / {wg['LE_tip_x_mm']:.1f} mm  (sweep {wg['le_sweep_deg']:.2f} deg)")
    print(f"  Wing AC (25% MAC) x     : {wg['x_ac_wing_mm']:.2f} mm")
    print(f"  Dihedral / tip rise     : {dihedral_deg:.1f} deg / {wg['tip_rise_mm']:.1f} mm")
    print(f"  Incidence / twist       : 0.0 deg / 0.0 deg (none modeled)")
    print(f"  Tail panel / total area : {tg['S_panel_m2']:.5f} / {tg['S_total_m2']:.5f} m^2")
    print(f"  Tail V-angle each side  : {tail_dihedral_deg:.1f} deg")
    print(f"  Sh (cos^2 proxy)        : {tg['Sh_equiv_m2']:.5f} m^2   (area projection {tg['Sh_proj_area_m2']:.5f})")
    print(f"  Sv (sin^2 proxy)        : {tg['Sv_equiv_m2']:.5f} m^2")
    print(f"  Tail horiz span / AR    : {tg['b_h_mm']:.1f} mm / {tg['AR_h']:.3f}")
    print(f"  Tail AC x               : {tg['x_ac_tail_mm']:.2f} mm   arm {tg['x_ac_tail_mm']-wg['x_ac_wing_mm']:.1f} mm")
    print(f"  Fuselage max diameter   : {fsum['max_diameter_mm']:.1f} mm   internal volume {fsum['V_int_cm3']:.1f} cm3")

    print("\n" + line)
    print("FUSELAGE SEGMENT INTERNAL VOLUMES")
    print(line)
    for r in frows:
        print(f"  sec {r['section']}  x={r['x0']:.0f}-{r['x1']:.0f}  L={r['length_mm']:.0f}  "
              f"r~{r['r_avg_mm']:.1f}  Vint={r['internal_volume_cm3']:.1f} cm3")

    print("\n" + line)
    print("MASS & BALANCE (recomputed)")
    print(line)
    print(f"  LW-PLA {mb['lw_g']:.1f} g | PETG {mb['petg_g']:.1f} g | purchased {mb['purchased_g']:.1f} g")
    for r in mb_rows:
        print(f"  {r['case']:12s} m={r['total_mass_g']:8.1f} g  CG={r['cg_x_mm']:7.2f} mm "
              f"({r['cg_pct_MAC']:5.1f}%MAC)  WL={r['wing_loading_g_dm2']:6.1f} g/dm2 "
              f"Vs(CL1)={r['stall_m_s_CLmax1']:.2f} m/s")

    print("\n" + line)
    print("STABILITY")
    print(line)
    print(f"  a_w={stab['a_w']}/rad  a_t={stab['a_t']}/rad  l_t={stab['l_t_m']} m")
    print(f"  Vh={stab['Vh']}  Vv={stab['Vv']}")
    print(f"  x_np nominal = {stab['x_np_nominal']} mm")
    cg_e = mb_rows[0]["cg_x_mm"]
    cg_l = mb_rows[-1]["cg_x_mm"]
    print(f"  SM empty  = {(stab['x_np_nominal']-cg_e)/stab['MAC']*100:+.2f}% MAC")
    print(f"  SM loaded = {(stab['x_np_nominal']-cg_l)/stab['MAC']*100:+.2f}% MAC")
    print("  x_np sensitivity:")
    for s in stab["sweep"]:
        flag = "  <== UNSTABLE (x_np < empty CG)" if s["x_np_mm"] < cg_e else ""
        print(f"    deps={s['deps']:.2f} a_t_scale={s['a_t_scale']:.2f} x_np={s['x_np_mm']:.1f} mm{flag}")

    print("\n" + line)
    print("STALL SPEED vs CLmax")
    print(line)
    for cl in [0.9, 1.0, 1.1, 1.2]:
        print(f"  CLmax={cl:.1f}: empty={stall_speed(mb['total_g'],cl):.2f} m/s  "
              f"+500g={stall_speed(mb['total_g']+500,cl):.2f} m/s")

    print("\n" + line)
    print("DRAG / GLIDE (CD0=0.038, e=0.85)")
    print(line)
    for tag, mass in [("empty", mb["total_g"]), ("+500g", mb["total_g"] + 500)]:
        best = None
        for i in range(60, 220, 5):
            V = i / 10.0
            g = glide_and_drag(mass, V)
            if best is None or g["L_over_D"] > best[1]["L_over_D"]:
                best = (V, g)
        print(f"  {tag:6s} best L/D={best[1]['L_over_D']:.1f} at {best[0]:.1f} m/s (CL={best[1]['CL']:.2f})")


if __name__ == "__main__":
    main()
