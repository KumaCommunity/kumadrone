# Design Issues Register — Kuma FPV V5 Configuration B

Severity: **Critical** = fundamental failure/safety/requirement conflict; **High** =
important deficiency requiring design change; **Medium** = durability/serviceability/
efficiency; **Low** = minor/documentation/cosmetic. Confidence reflects evidence strength
(observed geometry = High; analytical = Medium).

## Summary table

| ID | Component | Issue | Severity | Confidence |
|---|---|---|---|---|
| I-01 | Wing↔fuselage | No positive wing-to-fuselage load path; saddle not fastened to fuselage; through-spar absent | **Critical** | High (observed) |
| I-02 | Wing spar | No centre spar joiner; half-spars butt at y=0; slip-fit rod only | **High** | High (observed) |
| I-03 | Tail | Tail panels have no modelled registration/attachment to shoes/saddle | **High** | High (observed) |
| I-05 | Controls | Ruddervators are cosmetic shells — no hinge, horn, servo, pushrod | **Critical** | High (observed) |
| I-06 | Controls | Ruddervator-only lateral control unsubstantiated; Vv≈0.03 low; 7° dihedral unproven | **High** | Medium (analytical) |
| I-07 | Nose | Camera aperture & mount absent; nose closed; requirement R4 unmet | **High** | High (observed) |
| I-08 | Fuselage | No access hatches; battery/camera/servo service requires unbolting sections | **High** | High (observed) |
| I-09 | Propulsion | No motor thrust bulkhead/mount modelled | **High** | High (observed) |
| I-10 | Equipment | 500 g secured-equipment requirement not achievable (retention+packaging) | **Critical** | High |
| I-11 | Cooling | No ventilation for ESC/battery in closed fuselage | **Medium** | High (observed) |
| I-12 | Battery | No qualified battery restraint; 185 g pack loose | **Medium** | High (observed) |
| I-13 | Launch | Hand launch at +500 g (1.81 kg) is demanding/marginal (feasible with an athletic throw + adequate T/W); empty is fine | **High** | High |
| I-14 | Mass/CG | 500 g CG-neutral only because load placed at CG; envelope ~2.0 g/cm³ | **High** | High |
| I-15 | Manufacturing | Wing/tail meshes are nested multi-shell; print orientation/splitting unproven | **Medium** | High (observed) |
| I-16 | Hardware | Insert pull-out & LW-PLA tolerance unverified | **Medium** | Medium |
| I-17 | Electrical | EMI/antenna/wiring layout not addressed | **Medium** | Medium |
| I-18 | Stability | Static margin provisional (method-limited; Munk moment ignored) | **Medium** | Medium |
| I-19 | Fairing | Dorsal fairing floating; not connected to tail | **Low** | High (observed) |
| I-20 | Trim | CG aft of wing AC ⇒ tail download in trim (efficiency) | **Low** | Medium |
| I-21 | Appearance | Infographic depicts features absent in CAD (blends, spinner, spine) | **Low** | High |
| I-22 | Hardware | No screw-retention/vibration strategy | **Low** | High |
| I-23 | Mass budget | `wing_center` material inconsistent (SCAD "PETG" vs tables "LW-PLA"); if PETG, +114 g | **Medium** | High (observed) |

## Detail — Critical & High

### I-01 Wing-to-fuselage load path (Critical)
- **Evidence:** `wing_center` M4 holes (x=532/651, y=±20) bolt into `PETG_saddle_plate`
  insert bosses; the saddle plate has **no modelled fastener to the fuselage** (rests on
  the crown). Spar rods span y=0→620 per side but do not react against the fuselage.
- **Impact:** Wing lift/bending/torsion cannot be shown to reach the airframe; the wing
  hangs on an unspecified PETG-to-LW-PLA adhesive bond — a single-point failure.
- **Correction:** Real spar carry-through / wing box inside the fuselage that spars plug
  and bond into, plus ≥4 through-bolts with backing; define and test the bond.
- **Validation:** Wing static pull-up to 1.5× ultimate root moment (≥15 N·m) with deflection
  logging; bond shear coupons. **Depends on:** I-02.

### I-02 Centre spar joiner (High)
- **Evidence:** `wing_spar(s,0,620,...)` draws separate rods per side; no splice at y=0;
  bore 8.55 mm for 8.0 mm rod = slip fit.
- **Impact:** No moment continuity across the centreline; wing = two pinned cantilevers; rod
  can fret in the bore.
- **Correction:** Continuous or spliced centre spar bonded into the centre section and
  carried into the fuselage; tighten bore and bond the rod.
- **Validation:** Wing static bend test; rod pull-out/torque test. **Depends on:** I-01.

### I-03 Tail joint definition (High)
- **Evidence:** `PETG_tail_saddle` (4×M3) and `PETG_tail_shoe` exist, but `tail_fixed`
  panels have no mating holes/keys; shoe z≈38–41 vs panel root z≈26 — no obvious register.
- **Impact:** The tail (carrying pitch/yaw control and fin loads) is not connected in CAD.
- **Correction:** Tongue-and-groove/pin registration between panel root and shoes/saddle,
  through-bolts, and a spar-like root member; bond + bolt.
- **Validation:** Tail static pull/yaw test; fit check print.


### I-05 Ruddervator control mechanism (Critical — for flight)
- **Evidence:** `ruddervator(s)` is a diffusion loft shell with a ~3 mm chord gap to the
  fixed tail. No hinge line/axis/barrel, no control horn, no servo, no pushrod, no servo bay.
- **Impact:** **No functioning pitch or yaw control.** The aircraft cannot be flown as
  drawn. (Hinge moments are small, ≈0.5–1 N·cm at 12–16 m/s, so a micro servo suffices —
  the missing item is the mechanism, not the power.)
- **Correction:** Hinge geometry (printed knuckle + carbon/music-wire pin, or live hinge),
  control horn, servo bay/mount, pushrod routing with clearance and mechanical travel
  limits; define pitch-both / yaw-differential mix.
- **Validation:** Bench rig — travel, centering, slop, blow-back speed; ground taxi/low-hop
  only if a safe site exists. **Depends on:** I-03, I-06.

### I-06 Ruddervator-only lateral control (High — direction risk)
- **Evidence:** No ailerons (requirement). Roll = rudder→yaw→sideslip→dihedral roll.
  Vv≈0.030 (low end), Cl_β estimated 0.08–0.16/rad, 7° dihedral unproven.
- **Impact:** Roll response likely sluggish; poor gust/crosswind handling; 2-channel skill
  demand. Pitch is the safer axis (SM≈+8 %).
- **Correction:** Increase Vv (taller/larger V-tail or more vertical-equivalent area),
  consider more dihedral, tune differential; validate with 6-DOF sim + instrumented flight.
  An aileron variant conflicts with R6 — a requirements decision.
- **Validation:** AVL/XFLR5 derivatives + logged flight test.

### I-07 Nose camera integration (High — requirement R4)
- **Evidence:** `hull_body` closes the nose (pole at x≈0). `camera_plate` is a separate
  8×32×32 plate with a 12.5 mm bore floating at x=38 inside the closed shell; no lens
  opening, no mount to the skin.
- **Impact:** The required forward-facing FPV camera cannot see out and is not integrated.
- **Correction:** Cut a lens aperture + camera cradle into the nose; provide a replaceable
  mount and protective window/lip; route camera cable.
- **Validation:** Fit the actual camera; FOV/aim check.

### I-08 Service access (High)
- **Evidence:** No hatches/doors; access = unbolt sections via couplers. Battery, camera,
  servos internal.
- **Impact:** Battery removal for charging, camera/servo replacement, inspection are
  laborious; drives repeated insert wear and assembly error.
- **Correction:** Top/side hatch (hinged/latched) over battery/electronics; camera hatch;
  servo access panels.
- **Validation:** Build one section; time a battery swap; cycle-test latches.

### I-09 Motor thrust bulkhead (High)
- **Evidence:** Motor is a Ø36 envelope at x=969; no firewall/bulkhead; fuselage_5 ends ≈Ø36.
- **Impact:** Pusher thrust reaction and crash loads have no defined path; motor mount
  undefined.
- **Correction:** PETG/ply bulkhead ring bonded/bolted into fuselage_5 carrying the motor
  mount (X-mount or 4×M3); thrust reacted into the shell.
- **Validation:** Static thrust stand to ≥2× max thrust; vibration check.

### I-10 500 g secured equipment (Critical — requirement)
- **Evidence:** `PETG_forward_equipment_tray` is "illustrative"; no mating bosses/restraint;
  envelope 138×46×40 = 254 cm³ ⇒ ~2.0 g/cm³ for 500 g. See REQUIREMENTS §2.
- **Impact:** R14 cannot be met as drawn (retention + packaging + launch).
- **Correction:** Redefine requirement (≤150–250 g secured) **or** design a real captive
  tray with straps/latches, structural mounts, larger bay — accepting it cannot be
  hand-launched at 500 g.
- **Validation:** Drop/vibration test of retained mass; fit a representative load.
  **Depends on:** I-13, I-14.

### I-13 Hand launch at 1.81 kg (High — demanding, not a conflict)
- **Corrected finding (supersedes an earlier over-stated "conflict"):** the issue is
  **mass → stall speed**, NOT internal vs external stowage (internal is actually better:
  less drag). Empty 1.31 kg (WL 5.75 kg/m², Vs 9.6 m/s) is comfortably hand-launchable.
  +500 g → 1.81 kg (WL 7.95 kg/m², Vs 11.3 m/s): the realistic throw range for a bulky
  ~1.8 kg model is ~8–13 m/s, and required release is ~11.3 m/s (k=1.0, high T/W) to
  ~13 m/s (k=1.15, low T/W). So it is **feasible with an athletic throw (~12–13 m/s) OR a
  firm throw (~10–11 m/s) plus T/W ≳0.7 into wind** — demanding and low-margin, not
  impossible.
- **Impact:** A handled RISK: a weak throw can stall/drop; high wing loading leaves little
  margin; requires a strong throw and/or good thrust-to-weight.
- **Correction (optional, to add margin):** trim mass toward ~1.5–1.6 kg, or slightly
  enlarge the wing, or ensure T/W ≳0.7; validate throw speed vs Vs on the real airframe.
- **Validation:** Measure actual throw speed (radar/app) at the real 1.81 kg mass, and a
  static-thrust stand for T/W, before committing a loaded launch.
- **Dependencies:** R14 (secured retention), T/W from the propulsion spec (I-09).

## Detail — Medium & Low (condensed)

- **I-11 Cooling (Med):** closed fuselage, no vents. Add nose inlet + aft exit for ESC/
  battery; validate temps under load.
- **I-12 Battery restraint (Med):** rail only, no strap/latch. Add strap + crash retention;
  ensure pack removable for charging (ties to I-08).
- **I-14 CG/packaging (High):** 500 g CG-neutral only because at x≈CG; envelope dense.
  Measure actual load; re-run CG with real station/mass.
- **I-15 Print integrity (Med):** nested multi-shell wing/tail meshes; wing orientation.
  Slice-preview, repair/unite, choose orientation (may split panels), weigh coupons.
- **I-16 Inserts (Med):** print `insert_fit_coupon`, pull-test chosen inserts in PETG and
  LW-PLA; confirm hole shrink with LW-PLA.
- **I-17 EMI (Med):** long power/motor leads near RX; carbon spar conductive. Separate,
  twist, ferrite, antenna clear of carbon & VTX.
- **I-18 Static margin (Med):** SM≈+8 % provisional; method-limited; Munk moment ignored.
  Confirm NP with VSPAERO/AVL/XFLR5 and flight test before flight.
- **I-19 Fairing (Low):** `dorsal_fairing` floats (x≈445–605), not joined to tail; infographic
  implies a spine. Either extend to a real spine or remove; purely cosmetic/aero.
- **I-20 Trim (Low):** CG (≈30 % MAC) aft of wing AC (25 %) ⇒ tail download in trim; moving
  CG to ~26–27 % MAC reduces trim drag and raises SM. Not a defect, an optimisation.
- **I-21 Appearance (Low):** infographic shows smooth blends, spinner, dorsal spine, wing
  fillets **absent in CAD**. CAD is authoritative; treat infographic as aspirational.
- **I-22 Retention (Low):** add thread-locker/safety on vibration-sensitive screws.
- **I-23 `wing_center` material (Med):** SCAD comment says "Hollow PETG center section" but
  `geometry_mass_screen.csv`/`mass_budget.csv` call it LW-PLA (43.5 g). PETG would be
  157.8 g (+114 g ⇒ empty ≈1422 g, CG ≈561.7 mm). Engineering intent (spar bores + M4 mount)
  favours PETG — so the mass budget likely **under-counts** it. Resolve and re-run CG.
