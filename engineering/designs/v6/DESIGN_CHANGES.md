# V6 Design Changes — traceability to the V5 audit

**Model:** `Kuma_FPV_V6_Configuration_B.scad` (derived from V5; V5 files untouched).
**Status of the SCAD:** **COMPILED** with OpenSCAD 2026.10.11 — all 43 exported parts are
manifold/`NoError`; STLs in `../v6/STL/`; empty mass **1403 g**, lightened to **1351.8 g** (−51 g).
Mechanical fit checks/tests still required. The Python recalculation (`scripts/v6_calcs.py`)
is run and verified. Verified mass envelope (density swept): empty 1146–1807 g, +500 g
1646–2307 g (`scripts/v6_mass_range.py`).

**Additional model fix (not audit‑driven):** building the lofted wing/tail surfaces with
`s=-1` caused a topology blow‑up on current OpenSCAD (e.g. wing_L1 1346 cm³/6423 bodies).
Fixed by generating the +y half and `mirror([0,1,0])` for left parts in `wing_loft`,
`wing_web` (via `wing_web_half`), `tail_loft` → clean symmetric watertight parts.
(The **original V5 file has the same problem on this OpenSCAD version**; the shipped V5
left‑side STLs were evidently produced with an older toolchain.)

**Post‑compile refinements (v2):**
- **I‑08:** battery lid gained a **registration flange** (+2.8 g) that seats into the opening.
- **I‑05:** added **pushrod exit holes** in `fuselage_4` so rods reach the horns.
- **I‑19/I‑21:** a **dorsal spine was trialled as a solid `hull()` (~80 g) and rejected** on
  mass grounds; it must be a thin shelled fairing (noted in the SCAD), not a solid.
- **I‑18 DONE — and it changed the verdict.** OpenVSP `vspscript` ran VSPAERO headless.
  **Wing+tail VLM:** SM +8.31 %, NP 574.6 mm (matched analytical). **Panel incl. fuselage:**
  **SM −3.9 %, NP 553 mm**, Cnβ ~0/rad — the fuselage is a big destabiliser, so the current
  V6 at CG 30.7 % MAC is **marginally unstable in pitch / neutral in yaw**. Tail study
  (base/vv1/vv3/vv2 in `data/vspaero/V6_panel_tail_study.md`): a bigger tail (~span 0.33,
  chords 0.23/0.17, ~47°) + CG ~24–27 % MAC → SM ≈ +5.6 %, Cnβ ~0.08, Clβ ~0.4.
  **Action for V6.1:** enlarge tail to vv3 and move CG forward; re‑run. See
  `openvsp/vsp_study.py`, `Kuma_V6_vspaero_run.vspscript`.
- **Mass envelope** (verified volumes): empty 1146–1807 g (nominal 1403), +500 g 1646–2307 g.

Legend for Status: **SCAD** = geometry implemented in the model; **ITER** = needs
render/fit iteration; **TEST** = needs physical/analysis validation.

| Issue | V5 problem | V6 change | Where | Status | Verify by |
|---|---|---|---|---|---|
| I‑01 | Wing bolted to a saddle plate that was **not attached** to the fuselage | `wing_saddle_clamp`: 4 top pads + 4 straps + under‑belly plate wrap the fuselage; 4×M4 through‑bolts | `module wing_saddle_clamp` | SCAD/ITER | wing pull‑up to ≥1.5× ultimate; fit print |
| I‑02 | Half‑spars butt at y=0, slip‑fit | `centre_spar_joiner`: bonded sleeve + cross‑pin at both spar lines | `module centre_spar_joiner` | SCAD/ITER | spar splice pull/bend test |
| I‑03 | Tail panels had no registration to shoes | `tail_root_spar` (carbon pin along root chord) + `tail_root_key` tongue | `module tail_root_spar/key` | SCAD/ITER | tail fit + static pull |
| I‑05 | Ruddervators were **cosmetic shells** | `ruddervator_hinge` (pin line + 3 knuckles), `control_horn`, `servo_bays_cut`, `pushrod_channel` | several modules | SCAD/ITER/TEST | bench rig: travel, slop, centering |
| I‑06 | Vv≈0.030 (weak directional); rudder‑only roll unproven | **V‑tail enlarged** span 240→270, chords 190/140→200/150, dihedral 40→45° ⇒ **Vv 0.030→0.043** | params + `tail_pt` | SCAD | VSPAERO Cnβ/Clβ + flight test |
| I‑07 | Closed nose, camera floated inside | `camera_aperture_cut` (lens tube through nose) + `camera_cradle` | modules | SCAD/ITER | fit camera; FOV/aim |
| I‑08 | No access; battery/camera/servo required unbolting sections | `battery_hatch_cut` + `battery_hatch_lid`; `servo_bays_cut` | modules | SCAD/ITER | time a battery swap |
| I‑09 | No motor firewall/mount | `motor_bulkhead` (PETG disk, Ø8 pass, 4×M3 on 19 mm BC) | `module motor_bulkhead` | SCAD/ITER | thrust‑stand to ≥2× thrust |
| I‑10 | 500 g "secured" tray was illustrative | `secured_tray_v6`: base tray + 4 bosses + 2 strap slots | `module secured_tray_v6` | SCAD/ITER | drop/vibration test |
| I‑11 | Sealed fuselage (ESC/battery heat) | `cooling_inlet_cut` (nose) + `cooling_exit_cut` (aft) | shell(0)/shell(4) | SCAD/ITER | temp check under load |
| I‑12 | No battery restraint | `battery_strap` slots via tray + hatch lid; battery fwd | battery_tray / hatch | SCAD/ITER | strap retention test |
| I‑13 | Hand launch demanding at +500 g | **Not a conflict** (see audit addendum); kept hand launch, added `hand_grip_recess`; documented WL/Vs | `grip_recess_cut` | SCAD | throw‑speed + thrust test |
| I‑14 | 500 g CG‑neutral only at x≈CG | battery fwd 410→375 holds CG; 500 g still placed ~x556 | params | CALC | weigh real load |
| I‑20 | CG aft of wing AC (tail download) | battery fwd **410→375 mm** → empty CG 560→**561.6**, SM **+7.5 %** | `battery_center` | CALC | confirm with scale |
| I‑23 | `wing_center` called "PETG" in SCAD but costed LW | keep **wing_center LW‑PLA** + localised `wing_center_spar_sleeve` collars (avoids +114 g) | module + note | SCAD | weigh part |
| I‑18 | NP/derivatives provisional | **VSPAERO:** wing+tail VLM SM +8.3 %; **panel incl. fuselage SM −3.9 %** → tail too small & CG too far aft | `openvsp/vsp_study.py`, `Kuma_V6_vspaero_run.vspscript` | **DONE** | V6.1 tail↑ + CG fwd |

## What V6 deliberately did NOT change (and why)
- **Wing planform** (span 1300, chords 200/150, AR 7.43, 7° dihedral) — verified correct in
  the audit; changing it would invalidate the verified geometry. Dihedral remains a tuning
  variable to test (7→9° would add roll coupling if flight test shows it is needed).
- **NACA 2412 / 0010** — verified; low‑Re optimality still unproven (test item).
- **Ailerons** — prohibited by the requirement; V6 improves roll authority via larger Vv.

## Numeric V5 → V6 (from `scripts/v6_calcs.py`, Python‑verified)
| Quantity | V5 | V6 | Note |
|---|---:|---:|---|
| Tail span / chords / V‑angle | 240 / 190·140 / 40° | 270 / 200·150 / 45° | enlarged |
| Tail total area | 0.0792 m² | 0.0945 m² | +19 % |
| Sh / Sv | 0.0465 / 0.0327 | 0.0473 / 0.0472 | Sv up (more vertical) |
| Vh / Vv | 0.31 / 0.030 | 0.32 / **0.043** | directional ↑ |
| Empty mass | 1307.9 g | ~1400 g | +92 g structure |
| Empty CG (%MAC) | 560.0 (29.9) | 561.6 (30.7) | battery fwd |
| Static margin | +7.8 % | **+7.5 %** | held |
| Empty WL / Vs | 57.5 g/dm² / 9.59 | 61.5 g/dm² / 9.93 | heavier |
| +500 g WL / Vs | 79.5 / 11.28 | 83.5 / 11.56 | launch more demanding |

## Still open after V6 (must do before flight)
1. **Render/export the SCAD** in OpenSCAD; fix any CSG/fit issues (not done here).
2. Build & fit‑check the clamps, hinges, bulkhead, hatches, cradle; tune clearances.
3. Weigh V6 parts; replace the +92 g estimate; re‑run `v6_calcs.py`.
4. VSPAERO on V6 tail (update tail to span 270 / 45° / chords 200·150) → Cnβ, Clβ, NP.
5. Bench the control mechanism; thrust‑stand the motor; throw‑speed test.
6. The ~92 g structural add and higher WL mean **hand launch is now closer to its limit** —
   consider trimming PETG elsewhere or accepting a firmer launch (consistent with "redesign
   the launch system if needed").
