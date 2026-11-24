# Structural Review — Kuma FPV V5 Configuration B

**Scope:** load paths, joints, fasteners, printed-structure credibility. The CAD is a
concept; several load paths are visibly incomplete. This review separates what is
*plausible if built as intended* from what is *actually drawn and connected*.

## 1. Load cases (auditor-chosen basis)

| Case | Factor | Note |
|---|---|---|
| Level flight | n = 1.0 | trim incl. tail download |
| Limit manoeuvre | n = +3.0 | recreational-limited assumption |
| Ultimate | n = +4.5 | 1.5 × limit (ASTM F2245-style) |
| Negative | n = −1.5 | gust/pushover |

Root bending screens (`scripts/structural_screen.py`):

| Case | L_total | L_half | M_root (per half, k=0.40) |
|---|---:|---:|---:|
| empty, 3 g | 38.5 N | 19.2 N | 5.00 N·m |
| empty, 4.5 g | 57.7 N | 28.9 N | 7.50 N·m |
| +500 g, 3 g | 53.2 N | 26.6 N | 6.91 N·m |
| +500 g, 4.5 g | 79.8 N | 39.9 N | 10.37 N·m |

## 2. Wing structure

**Drawn (verified from meshes):** each panel is a hollow airfoil shell with
*full-depth chordwise webs at ≈28% and ≈63% chord*, plus anti-twist webs near joints.
The 28%/63% webs coincide with the 8 mm / 4 mm spar bores — the carbon rods run *inside*
the webs. This is a credible twin-spar / D-cell-like concept, and the internal webs are
real material spanning the section (confirmed: panel material volume 181.9 cm³ = outer
569.6 − three 44 mm-deep void chambers; webs are the chamber walls).

**Spar sizing (8 mm main spar, M_root = 10.4 N·m at +4.5 g loaded):**

| Spar | I (mm⁴) | σ (MPa) | FS (indicative) |
|---|---:|---:|---:|
| carbon tube 8×6 (1 mm wall) | 137.4 | 302 | 2.98 |
| carbon tube 8×7 (0.5 mm wall) | 83.2 | 499 | 1.80 |
| solid Al 6061 8 mm | 201.1 | 206 | 1.34 |
| solid steel 8 mm | 201.1 | 206 | 1.70 |

An 8 mm carbon tube is adequately sized *as a beam*. Carbon is anisotropic and
tube-crush/bonded joints usually govern, so FS is indicative only.

**Load-path gaps (the real problem):**
- **Spar continuity at the centre.** The two half-spars run y=0→620 each side but
  merely **butt at y=0** — no joiner, splice, or carry-through box. No continuous
  centre spar exists in the CAD.
- **Rod-to-panel transfer is slip-fit only.** Bore 8.55 mm for an 8.0 mm rod (0.55 mm
  clearance). Unbonded, the rod transmits bending only by loose bearing — a pin, not a
  bonded spar. Repeated flexing wears the printed bore.
- **Wing-to-fuselage.** The wing-centre bolts (4 × M4) go into the **PETG saddle
  plate**, but the *saddle plate has no modelled fastener to the fuselage* — it rests
  on the fuselage crown. The wing cannot be shown to transfer lift/moment into the
  fuselage; it relies on an unspecified PETG-to-LW-PLA adhesive bond.
- **Root moment path.** Absent a carried-through spar, root bending is reacted by the
  M4 couple (119 mm spacing): ≈44 N/bolt at ultimate (bending only). Small *if* inserts
  are in PETG and the saddle is bonded — but the saddle attachment is unproven. Torsion
  (roll/gust) adds load into the same 4 bolts and keys.

**Verdict (wing):** *Plausible in concept, not connected in CAD.* The spar/webs are a
sound idea; the centre joiner and wing-to-fuselage carry-through must be designed,
bonded/bolted, and load-tested.

## 3. Fuselage

- Shell: 1.25 mm LW-PLA wall (≈3 perimeters at 0.4 mm nozzle) — thin but printable.
- **Joints are the best-developed feature:** each seam has a PETG coupler ring spanning
  ±14 mm with four M3 heat-set bosses at x±9; both adjacent shells screw radially into
  it. A genuine, credible splice.
- Section transitions are gentle (max Ø84 mm at x≈350 → Ø18 mm at tail); no abrupt steps.
- **Access openings:** no modelled hatches/doors — access is by unbolting whole
  sections via couplers. Repeated assembly wears the M3 inserts.
- **Motor bulkhead:** motor envelope is a Ø36 mm cylinder at x=969; no firewall/thrust
  bulkhead is modelled. A pusher's thrust reaction pushes the motor forward — must be
  reacted by a real bulkhead (missing).

## 4. Tail

- **Tail-to-fuselage:** PETG `tail_saddle` (4 × M3 bosses) + two PETG `tail_shoes`. But
  the *tail panels have no modelled mating holes/keys* to the shoes or saddle — the
  connection is not drawn. Shoe geometry (z≈38–41) does not obviously register to the
  panel root (z≈26); the interface must be defined.
- **Ruddervator support:** separate lofted shell with a ~3 mm chord gap to the fixed
  tail. **No hinge line, hinge axis, barrel, control horn, servo, or pushrod anywhere
  in the CAD.** As drawn, the ruddervators are cosmetic surfaces, not a mechanism.
- **Hinge/servo loads:** ruddervator hinge moment is tiny — ≈0.55 / 0.74 / 0.97 N·cm at
  12/14/16 m/s (Ch≈0.15 vs a standard 15–20 N·cm micro servo). Torque is not the
  constraint; the missing mechanism is.


## 5. Fasteners and inserts

| Interface | Hardware | Concern |
|---|---|---|
| Fuselage seams | M3 + PETG coupler | credible; repeated-use wear on inserts |
| Wing keys | M3 in PETG key | key may print as nested shells; spar continuity unproven |
| Wing centre | M4 in PETG saddle | saddle-to-fuselage attachment missing |
| V-tail | M3 in PETG saddle/shoes | panel-to-shoe registration missing |
| Camera/dorsal | M2 / M3 | matching bosses not developed |

- Clearances: M3 clear 3.5 / pilot 4.0 / depth 6.8 mm; M4 clear 4.5 / pilot 5.7 /
  depth 9.2 mm — plausible for common heat-set inserts but **test-coupon targets, not
  verified** for the user's inserts (`insert_fit_coupon.stl` supplied — correct approach).
- **LW-PLA insert risk:** heat-set inserts into *foamed* LW-PLA have very low pull-out
  and crush resistance. Inserts must live in PETG bosses with ≥3–4 mm wall; the couplers
  do this, but the wing saddle and fairing interfaces are less clear.
- **Screw retention / vibration:** no thread-locker, nyloc, or clip provision described.
  A pusher vibrates; screws into heat-set inserts can back out. Add a retention strategy
  (medium thread-locker; safety on the motor mount).

## 6. Fatigue, layer separation, print-direction strength

- LW-PLA parts are weakest in **inter-layer (Z) tension** and in **creep** under steady
  load. Wing skin, fuselage shell, and tail are all LW-PLA; the belly and wing skins see
  repeated landing/vibration loads. With no material data for the print orientation, **no
  defensible factor of safety can be assigned** to the printed structure (ASSUMPTIONS A18).
- Control load direction vs print direction: webs and skins should be printed so dominant
  bending stress is *in-plane*, not peeling layers.

## 7. Analytic vs. requires-test

- **Analytically sufficient (done here):** spar beam stress, root-bolt couple, hinge
  moment, internal volume, basic load cases.
- **Requires simulation/test:** bonded saddle-to-fuselage, insert pull-out, layer
  adhesion, panel-to-shoe joint, vibration/fatigue, crash/landing loads.

## 8. Structural conclusion

The airframe is a **credible structural concept wrapped around an incomplete joint
scheme**. The two-spar wing with full-depth webs and the coupler-ring fuselage joints are
good ideas. But four load paths are *unresolved in the CAD* — (1) centre spar joiner,
(2) wing-saddle-to-fuselage attachment, (3) tail-panel-to-shoe registration, (4)
ruddervator hinge/linkage — plus the motor thrust bulkhead. None can be claimed
flight-safe until designed and tested. The source correctly calls the spar/saddle/V-tail
joint load paths "incomplete."
