# Audit Summary — Kuma FPV V5 Configuration B

**Independent engineering & design audit · 22 Nov 2026**
**Overall verdict: REQUIRES SIGNIFICANT DESIGN REVISIONS.**
Not an airworthiness certification. Configuration is a coherent *concept*, not a
flight-ready aircraft; the 500 g and hand-launch requirements are in direct conflict.

## The ten required answers

1. **Geometrically coherent?** **Yes.** Dimensions, planform, MAC, AR, tail area/volume and
   both airfoils recompute correctly from the CAD and DXFs (NACA 2412 = 12.0 % t/c, 2.0 %
   camber; NACA 0010 = 10.0 %). No unintended asymmetry; coordinate conventions consistent.
   Gap: zero wing/tail incidence and twist are modelled (a design DoF unused).

2. **Is the mass plausible?** **Plausible but assumption-dominated.** 1307.9 g empty
   reproduces to <0.1 g from the meshes, but rests on an assumed 0.35 g/cm³ foaming-LW-PLA
   density; over 0.25–0.55 g/cm³ the empty mass spans ~1.16–1.61 kg. Must be replaced by
   weighed coupons.

3. **Is the CG credible?** **Credible given the assumptions, but the 500 g case is
   CG-neutral only by construction** (load placed at x≈CG). CG ≈ 30 % MAC, and the CG is far
   more sensitive to LW-PLA density and battery station than to the equipment load.

4. **Is the wing sized for the weight?** **Reasonably empty, marginal loaded.** AR 7.43 and
   1.3 m span are fine at ~1.3 kg (WL 5.75 kg/m²) but high at 1.8 kg (WL 7.95 kg/m²).

5. **Is the rear-only control substantiated?** **No.** Pitch margin is positive (SM≈+8 %,
   provisional), but the ruddervators have no hinge/horn/servo/pushrod (cosmetic only), and
   ruddervator-only roll (Vv≈0.03, 7° dihedral) is unproven and likely sluggish. It is a
   hypothesis, not a validated control concept.

6. **Are the structural joints credible?** **Concept yes, as-drawn no.** Twin-spar/full-depth-
   web wing and coupler-ring fuselage joints are good ideas; the 8 mm carbon spar is sized
   with margin (FS≈3 at +4.5 g). But four load paths are undefined (centre spar joiner,
   wing-saddle-to-fuselage, tail-panel-to-shoe, ruddervator hinge) plus the motor bulkhead.

7. **Manufacturable on ordinary FDM?** **Yes with care.** All 32 parts fit 220×220×250 and
   are watertight. But wing/tail meshes are nested multi-shell (slicer repair needed), wing
   print orientation must be chosen (may split panels), and LW-PLA mass is a slicer outcome.

8. **Is conventional hand launch plausible?** **Empty: marginal. +500 g: no.** At 1.81 kg,
   WL 7.95 kg/m² and required ~13–15 m/s / ~150–190 J release exceed what a person can throw;
   no launcher is permitted. This is a **Critical requirement conflict.**

9. **Five most important unresolved questions:**
   (i) What is the real CLmax/Neutral Point at Re≈100–200 k?
   (ii) What is the real printed mass (LW-PLA density)?
   (iii) Can a 7°-dihedral, no-aileron, ruddervator-only aircraft be safely controlled?
   (iv) Will the wing/tail/motor joints carry flight loads and survive vibration?
   (v) Can 500 g be both secured **and** hand-launched (currently: no)?

10. **Modifications to investigate before the next prototype:**
    resolve the 500 g/launch conflict; design the control mechanism; define the four load
    paths + motor bulkhead; integrate the nose camera; add service hatches; weigh coupons and
    re-run CG; establish NP/derivatives with a proper method.

## Severity tally

| Severity | Count | Key items |
|---|---:|---|
| Critical | 4 | Wing↔fuselage load path; no control mechanism; 500 g requirement; hand launch |
| High | 7 | Centre spar; tail joint; camera aperture; service access; motor bulkhead; lateral control; 500 g packaging |
| Medium | 7 | Cooling; battery restraint; print integrity; inserts; EMI; static margin; `wing_center` material |
| Low | 4 | Dorsal fairing; trim; infographic mismatch; retention |

## What is genuinely good (to preserve)

- Correct, verified geometry and airfoils; clean parametric CAD.
- Sound structural *ideas*: twin-spar/full-depth-web wing; coupler-ring fuselage splices.
- Sane span/AR and a positive provisional pitch margin.
- Honest, well-conditioned source documentation (correctly flags unverified CLmax, incomplete
  joints, 28 %-MAC caveat).

## Deliverables in this folder

`AUDIT_SUMMARY.md` · `FULL_ENGINEERING_AUDIT.md` · `DESIGN_ISSUES.md` ·
`RECOMMENDED_CHANGES.md` · `REQUIREMENTS_TRACEABILITY.md` · `CALCULATION_VERIFICATION.md` ·
`STRUCTURAL_REVIEW.md` · `MANUFACTURING_REVIEW.md` · `HARDWARE_REVIEW.md` ·
`ELECTRICAL_REVIEW.md` · `ASSUMPTIONS_REGISTER.csv` · `GEOMETRY_VERIFICATION.csv` ·
`MASS_AND_BALANCE.csv` · `AERODYNAMIC_SCREENING.csv` · `scripts/` · `data/` ·
`graphics/` (mass/CG diagram, planform, launch/stall, static-margin sensitivity).

> CAD/parameter-derived figures and analytical screens only. No CFD, wind-tunnel, material,
> or flight testing was performed. OpenSCAD/OpenVSP/XFLR5 were unavailable in this environment
> and are not represented as run.
