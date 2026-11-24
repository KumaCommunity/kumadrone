# Recommended Changes — Kuma FPV V5 Configuration B

Each item notes whether it is **calc-supported** (backed by numbers in this audit) or
**needs research/testing**. Issue IDs in brackets refer to `DESIGN_ISSUES.md`.

## A. Required before further design development

1. **Design a secured 500 g retention + validate the loaded launch (calc-supported).**
   This is **not a conflict** (corrected): at 1.81 kg the aircraft is hand-launchable with a
   firm/athletic throw (~12–13 m/s) or a firm throw + T/W ≳0.7 into wind; empty is comfortable.
   Actions: (a) design a captive tray with straps/latches and structural mounts [I-10];
   (b) confirm a representative 500 g load fits the bay [I-14]; (c) measure throw speed and
   thrust-to-weight and check against Vs [I-13]. If measured mass trends high (see
   `MASS_RANGE.csv`, up to ~2.27 kg at the worst print setting), trim mass or enlarge the wing.
   *Numbers:* empty WL 5.75 kg/m²; +500 g WL 7.95 kg/m², Vs 11.28 m/s. [I-10, I-13, I-14, R14, R16]
2. **Define the control mechanism (calc-supported sizing).** Hinge + horn + servo bay +
   pushrod + travel limits + mix. *Numbers:* hinge moment 0.5–1 N·cm ⇒ micro servo ample;
   the gap is the mechanism. [I-05]
3. **Define all structural joints in CAD** — wing carry-through (I-01), centre spar splice
   (I-02), tail registration (I-03), motor bulkhead (I-09). *Numbers:* spar FS≈3 at +4.5 g
   (8 mm carbon) ⇒ member is fine; joints are the missing link. [I-01..I-03, I-09]
4. **Integrate the nose camera (requirement).** Lens aperture + cradle + window. [I-07, R4]
5. **Add service access** — battery hatch, camera hatch, servo panels. [I-08, I-12]

## B. Required before structural testing

6. **Specify the spar material & bond** and print `insert_fit_coupon` for pull-tests. [I-16]
7. **Print & weigh coupons** to replace the 0.35 g/cm³ LW-PLA assumption with measured
   mass (updates CG, WL, stall, launch). (calc-supported: density is the dominant CG
   uncertainty). [A01, A03, I-14]
8. **Slice-preview/repair the nested-shell wing/tail meshes** and lock a print orientation
   (possibly split wing panels). [I-15]
9. **Design a bonded/bolted saddle-to-fuselage interface** and a test plan for bond shear
   and wing pull-up to ≥1.5× ultimate. [I-01]

## C. Required before any flight testing

10. **Establish the neutral point by a proper method** (VSPAERO/AVL/XFLR5 or DATCOM) and
    confirm static margin with the *measured* CG and mass. (calc-supported: provisional
    SM≈+8 % is method-limited). [I-18] — **Tooling provided:** `openvsp/` (model + VSPAERO
    runner) and `scripts/parse_vspaero.py` (computes SM = −Cmα/CLα and x_np from VSPAERO
    output; validated against the analytical values).
11. **Substantiate ruddervator-only control** via 6-DOF simulation + instrumented flight
    test; verify roll authority, Dutch-roll, spiral, crosswind. (needs testing). [I-06]
12. **Propulsion & electrical definition** — motor/ESC/prop/battery ratings, power
    distribution, cooling, EMI layout, failsafe, battery retention. (needs research). [I-11,
    I-17, I-12]
13. **Hand-launch velocity test** on the light prototype — measure realistic throw speed vs
    computed Vs before committing to a launch technique. (calc-supported). [I-13]
14. **Ground/low-hop testing** of controls, trim, and CG before full flight — only at a
    safe site with appropriate segregation.

## D. Optional manufacturing improvements

15. Replace many thin PETG bosses with fewer thicker ones once joints are defined (mass &
    durability). [§MANUFACTURING 6]
16. Add captive screws/tethers on frequently-opened panels; standardise on one driver size
    where possible (remove M2 if the camera bracket allows). [I-22, R12]
17. Consider a single large dorsal hatch instead of unbolting whole sections for battery
    access. [I-08]
18. Foaming-flow calibration for LW-PLA to hit a target density repeatably.

## E. Optional appearance improvements (cosmetic only)

19. Reconcile the CAD with the infographic: add a dorsal spine connecting the fairing to
    the tail, a wing-root fillet/saddle fairing, and a spinner/motor fairing — or amend the
    infographic. CAD is authoritative. [I-19, I-21]
20. Smooth the fuselage/wing/tail transitions and hide fastener heads (counterbores) for a
    cleaner look — after the engineering joints exist.

## F. Changes that need further research/experiment (cannot be finalised analytically)

- LW-PLA layer-adhesion strength by orientation (tensile/beam coupons).
- Insert pull-out in PETG vs LW-PLA (coupon test).
- Bonded PETG-to-LW-PLA joint strength.
- Real CLmax / polar at Re≈100–200k (XFLR5 / tunnel / flight).
- Real motor/prop thrust and cruise current (thrust stand).
- Actual 500 g load packaging and retention (representative mock-up).

## G. Explicit non-recommendations

- **Do not** reduce material purely to cut mass before the joints are proven (structural
  consequences unquantified).
- **Do not** substitute a launcher (prohibited) to solve the launch problem.
- **Do not** treat the watertight STLs or the infographic as evidence of structural or
  mechanical correctness.
