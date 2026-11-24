# Requirements Traceability — Kuma FPV V5 Configuration B

Status key: **Met** = demonstrated in CAD/evidence; **Partial** = concept present but
incomplete/undefined; **Not met** = absent; **Conflict** = requirement cannot be
satisfied simultaneously with another. Issue IDs refer to `DESIGN_ISSUES.md`.

## 1. Configuration requirements

| # | Requirement | Status | Evidence / reason | Issue |
|---|---|---|---|---|
| R1 | Version Kuma FPV V5, Configuration B | Met | files/geometry named accordingly | — |
| R2 | Primary construction LW-PLA | Met | 520.5 g printed LW-PLA shells | — |
| R3 | PETG reinforcement where appropriate | Met | couplers, keys, saddle, shoes, trays (~310 g) | — |
| R4 | Forward-facing nano FPV camera in nose cone | **Not met** | nose is a closed surface of revolution; camera plate floats at x=38 inside, **no lens aperture or mount** | I-07 |
| R5 | High-mounted fixed wing | Met | wing chord line at z=56 mm above fuselage centreline | — |
| R6 | No wing-mounted ailerons | Met | full-chord fixed panels; no aileron cut | — |
| R7 | Upright V-tail, two ruddervators | **Partial** | 40° V panels + ruddervator shells exist; **no hinge, horn, servo, linkage** | I-05 |
| R8 | Rear-mounted electric pusher | Met (envelope) | motor Ø36 @x969, prop @x993; no bulkhead/mount | I-09 |
| R9 | Conventional manual RC flight | **Partial** | ruddervator-only concept; control mechanism & authority unproven | I-05, I-06 |
| R10 | Removable wings and tail for transport | **Partial** | modular by design; wing/tail joints undefined/missing | I-01..I-03 |
| R11 | Modular fuselage, accessible electronics | **Partial** | 6 bolt-together sections; **no hatches**; battery/camera/servo access poor | I-08, I-11 |
| R12 | Primarily M3/M4 metric fasteners | Met | M3 majority, M4 wing centre, few M2 (camera) | — |
| R13 | Interlocking connections that distribute loads (not screw-shear/printed-thread only) | **Partial** | coupler rings + keys are interlocking; **spar not carried through; saddle not attached**; several joints rely on printed threads/adhesive | I-01..I-03 |
| R14 | Optional **secured** onboard equipment up to 500 g | **Conflict / Not met** | no retention; 254 cm³ envelope is small for 500 g; and 500 g breaks hand-launch (R16). See §2 | I-10, I-14 |
| R15 | No payload-release mechanism | Met | none modelled | — |
| R16 | Conventional hand launch | **Conflict (Critical)** | empty 1.31 kg ≈ marginal; **+500 g (1.81 kg) not hand-launchable**; no launcher permitted | I-13 |
| R17 | No launcher / auto-deploy / military function | Met | none present | — |
| R18 | Evaluate empty and fully-equipped | Met | this audit evaluates 0/100/250/500 g | — |

## 2. The 500 g requirement — explicit conflict analysis

The 500 g equipment load is a **requirement to evaluate, not an established capability.**
The audit finds it is **not achievable** as currently framed:

1. **Hand-launch (R16).** At 1.81 kg the loaded wing loading is 7.95 kg/m² and the stall
   speed (CLmax 1.0) is 11.28 m/s; a safe launch needs ~13–15 m/s release. A person cannot
   throw 1.8 kg at that speed/energy, and no launcher is permitted. → **direct conflict.**
2. **Structural retention (R13/R14).** No secured mount for 500 g is modelled; the tray is
   "illustrative" with no mating bosses.
3. **Packaging (R11).** The 138×46×40 mm (254 cm³) envelope needs ~2.0 g/cm³ average
   packing for 500 g — denser than most hobby electronics. A representative 500 g load may
   not fit.
4. **CG.** CG-neutrality of the 500 g case exists **only** because the load is assumed at
   x=556 mm ≈ CG. Move it forward and the CG shifts (and the aircraft is already near the
   aft CG the hand-launch case dislikes).

**Therefore:** the 500 g capability is a **Critical requirement conflict**. The audit does
**not** force the design to meet it. Recommended resolution is to (a) redefine the
requirement (e.g. ≤150–250 g of secured equipment, or a launcher-compatible variant), or
(b) accept that the aircraft is a 1.3 kg hand-launched airframe and treat 500 g as out of
scope. See RECOMMENDED_CHANGES.

## 3. Design priorities (weighted by the brief)

| Priority | Status | Comment |
|---|---|---|
| 1. Flight stability & controllability | **Partial** | longitudinal SM ≈ +8 % (provisional); directional Vv≈0.03 low; ruddervator-only roll unproven |
| 2. Structural integrity | **Partial** | concept sound; 4 load paths undefined |
| 3. Safe hand-launch & landing | **Fails (loaded)** | empty marginal; loaded infeasible |
| 4. Manufacturing (ordinary FDM) | **Met w/ caveats** | all parts fit; nested-shell slicing & wing orientation to be proven |
| 5. Repeatable assembly/disassembly | **Partial** | modular; service access poor |
| 6. Low mass / electrical efficiency | **Unknown** | no propulsion data; 1.31 kg plausible but density-assumption-driven |
| 7. Repairability / standardisation | **Partial** | modular & M3/M4 good; some joints non-standard/M2 |
| 8. Appearance / visual consistency | **Partial** | CAD is crude vs infographic; large discrepancy |

## 4. Requirements verdict

Most *configuration-layout* requirements are met. The two that are **not** met and drive
the overall assessment are the **integrated nose camera** (R4) and the **secured 500 g
load / hand-launch** pair (R14/R16). The **control mechanism** (R7/R9) is the third
blocking gap. Everything else is "met or partial," consistent with a concept-stage CAD.
