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
| R14 | Optional **secured** onboard equipment up to 500 g | **Partial (retention not met)** | no modelled retention/mount; 254 cm³ envelope needs ~2 g/cm³ for 500 g. A captive tray can be added; carrying 500 g is feasible (see R16) — the gap is the *secured* mount, not the mass | I-10, I-14 |
| R15 | No payload-release mechanism | Met | none modelled | — |
| R16 | Conventional hand launch | **Met (demanding when loaded)** | empty 1.31 kg comfortable; **+500 g (1.81 kg) demanding/marginal but feasible** with an athletic throw (~12–13 m/s) or firm throw + T/W ≳0.7 into wind. Not a hard conflict; validate by throw-speed test | I-13 |
| R17 | No launcher / auto-deploy / military function | Met | none present | — |
| R18 | Evaluate empty and fully-equipped | Met | this audit evaluates 0/100/250/500 g | — |

## 2. The 500 g requirement — re-assessment (corrected; no hard conflict)

The 500 g equipment load is a **requirement to evaluate, not an established capability.**
On re-examination the earlier "conflict" verdict was **over-stated** and is corrected here:

1. **Hand-launch (R16) — feasible but demanding, not impossible.** Internal stowage vs
   external is irrelevant; the governing factor is **added mass → stall speed**. Empty
   1.31 kg (WL 5.75 kg/m², Vs 9.6 m/s) is comfortable. +500 g → 1.81 kg (WL 7.95 kg/m²,
   Vs 11.3 m/s); realistic throw for a bulky ~1.8 kg model ≈ 8–13 m/s, required ≈ 11.3 m/s
   (high T/W) to 13 m/s (low T/W). So it flies from a **firm/athletic throw plus adequate
   thrust-to-weight (~0.7+) into wind** — demanding and low-margin, but achievable. Internal
   actually *helps* (less drag). → not a conflict.
2. **Structural retention (R13/R14) — the real gap.** No secured mount for 500 g is modelled;
   the tray is "illustrative" with no mating bosses. **This is what must be designed.**
3. **Packaging (R11)** — the 138×46×40 mm (254 cm³) envelope needs ~2.0 g/cm³ for 500 g;
   verify a real representative load fits (may need a larger bay).
4. **CG** — the 500 g case is CG-neutral **only** because the load is assumed at x=556 mm ≈
   CG; that is a reasonable design choice but must be held in the actual build.
5. **Mass range** — because printed mass is uncertain (LW-PLA density), the +500 g all-up
   mass ranges **~1.57–2.27 kg** (see MASS_RANGE.csv); at the top of that range launch
   becomes harder. Measure real mass before committing a loaded launch.

**Therefore:** the 500 g case is **carryable and hand-launchable within limits**, provided
(a) a real secured retention structure is designed (I-10), (b) the load fits the bay, and
(c) launch uses a firm throw + adequate T/W and is validated by throw-speed testing (I-13).
The audit does **not** force an infeasible claim: if measured all-up mass trends high,
trim mass or enlarge the wing.

## 3. Design priorities (weighted by the brief)

| Priority | Status | Comment |
|---|---|---|
| 1. Flight stability & controllability | **Partial** | longitudinal SM ≈ +8 % (provisional); directional Vv≈0.03 low; ruddervator-only roll unproven |
| 2. Structural integrity | **Partial** | concept sound; 4 load paths undefined |
| 3. Safe hand-launch & landing | **Met (demanding loaded)** | empty comfortable; +500 g demanding/low-margin but feasible |
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
