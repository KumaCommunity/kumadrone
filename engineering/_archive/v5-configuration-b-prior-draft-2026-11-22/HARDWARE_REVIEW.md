# Hardware Review — Kuma FPV V5 Configuration B

Audited against `hardware_schedule.csv` and the SCAD fastener parameters.

## 1. Fastener schedule

| Interface | Hardware | Nominal geometry | Count | Assessment |
|---|---|---|---|---|
| Fuselage joints | M3 + PETG coupler | 3.5 clear / 4.0 pilot / 6.8 depth | 20 nominal | Credible; inserts in PETG ✅ |
| Wing segment keys | M3 in PETG key | 3.5 / 4.0 / 6.8 | 6 keys (12 bores) | Spar continuity unproven ⚠️ |
| Wing centre saddle | M4 | 4.5 / 5.7 / 9.2 | 4 | Saddle→fuselage attachment missing ❌ |
| V-tail saddle | M3 + PETG shoes | 3.5 / 4.0 / 6.8 | 4 | Panel→shoe registration missing ⚠️ |
| Battery rail | M3 | 3.5 clear | 4 | Restraint system missing ❌ |
| Equipment tray | M3 | 3.5 clear | 4 | Structural restraint missing ❌ |
| Nose camera plate | M2 | 2.1 clear | 4 | Verify actual camera bracket; no nose aperture ❌ |
| Dorsal fairing | M3 | 3.5 clear | 4 | No mating bosses ❌ |

## 2. Insert compatibility & edge distances

- **M3:** pilot 4.0 mm / depth 6.8 mm suits an insert of OD ≈4.0 mm, length ≈5.7 mm
  (common "M3 short"). **Verify against the exact insert** — ODs range 4.0–4.6 mm.
- **M4:** pilot 5.7 mm / depth 9.2 mm suits OD ≈5.7 mm, length ≈8–9 mm. Verify.
- **M3 clearance 3.5 mm** for a 3.0 mm screw = 0.25 mm radial — acceptable, slightly snug.
- **M4 clearance 4.5 mm** for a 4.0 mm screw = 0.25 mm radial — acceptable.
- **Boss walls:** PETG coupler boss Ø11.8 mm around a 4.0 mm hole → (11.8−4.0)/2 = 3.9 mm
  wall — good. Wing key (14 wide) around a 4.0 hole with holes at ±10 on the 36 mm axis:
  ~5 mm to the 14 mm sides, ~8 mm to the ends — acceptable.
- **Depth/backing:** 6.8 mm insert in a 10 mm key leaves 3.2 mm backing — acceptable but
  thin; do not over-torque.

## 3. Material of inserts

- Inserts must be in **PETG** (couplers, keys, saddle, shoes). Heat-set inserts in
  **LW-PLA** (foamed) have very low pull-out/crush — avoid; if unavoidable, use a printed
  PETG boss bonded into the LW-PLA.

## 4. Retention & vibration

- No thread-locker, nyloc, or clip strategy is described. A rear pusher vibrates;
  add medium thread-locker on non-service screws and a positive lock (nyloc or safety)
  on the motor mount. Provide captive screws or tethered hardware where panels are opened
  often.

## 5. Count / variety

- Predominantly M3, some M4, a few M2 (camera) — **reasonable standardisation**. The M2
  camera fasteners are a separate driver size; acceptable for a bracket but adds a tool.
- Total screw count (~50+) is high because access is by unbolting whole sections. This is
  the price of the fully-modular concept; trade against a single large hatch (§DFM).

## 6. Repeat-assembly wear

- Heat-set inserts in printed bosses wear with repeated use; LW-PLA shells around the
  screw holes will ovalise. For often-opened joints (battery access) use a metal insert
  in a PETG boss and consider a captive screw + shoulder so the thread is not the datum.

## 7. Verdict

Fastener *geometry* is self-consistent and plausible; the failure mode is **joint
definition, not screw size**. Every interface listed as "missing/partial" in §1 must have
a defined mating part before hardware counts are meaningful. The supplied insert coupon
should be printed and pull-tested first.
