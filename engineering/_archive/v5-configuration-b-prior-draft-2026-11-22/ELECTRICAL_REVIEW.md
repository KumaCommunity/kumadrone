# Electrical & Propulsion Review — Kuma FPV V5 Configuration B

**Caveat:** the package supplies only *example* component masses at example stations; no
part numbers, ratings, or wiring are given. Compatibility cannot be verified — only the
*architecture and completeness* are reviewed. No performance figures are asserted.

## 1. Architecture completeness

| Element | Present in package? | Spec available? | Status |
|---|---|---|---|
| Motor | envelope only (Ø36, x=969) | none (kV, size, prop unknown) | ❌ unspecified |
| Propeller | Ø150 mm envelope (6 in) | none | ❌ unspecified |
| ESC | 28 g placeholder | none (current rating unknown) | ❌ unspecified |
| Battery | 3S 2200 mAh (185 g) example | capacity only; C-rating unknown | ⚠️ example |
| Power distribution | not modelled | — | ❌ absent |
| Receiver | 10 g placeholder | none | ❌ unspecified |
| Ruddervator servos | 2, 20 g total placeholder | **no torque/size**, no linkage | ❌ unspecified |
| FPV camera | 2 g nano, plate at x=38 | none; **no lens aperture** | ❌ not integrated |
| Video transmitter | 23 g, x=130 | none (power/band unknown) | ❌ unspecified |
| Antenna | listed with VTX | type/placement unknown | ❌ unspecified |
| Wiring/connectors | 25 g placeholder | — | ❌ not modelled |
| Arming switch / failsafe | not modelled | — | ❌ absent |

## 2. Compatibility (where any data exist)

- **Battery vs airframe:** a 3S 2200 is plausible for this mass class but is the single
  largest component (185 g). Endurance cannot be estimated without motor/ESC/prop and a
  measured cruise current; do **not** carry forward any endurance number.
- **Servo torque:** the ruddervator hinge moments are small (≈0.5–1 N·cm, §Structural),
  so an ordinary ~1.5–2 kg·cm micro servo has ample torque **provided** a proper horn/
  pushrod exists (it does not in CAD). Servo *speed/centering* and flutter margin are
  unassessed.
- **ESC current:** must be sized to the actual motor/prop; not determinable here. A pusher
  with a 6 in prop typically draws modest current, but this is unverified.

## 3. Cooling & ventilation

- The fuselage is a **closed body of revolution** with no vents. An ESC inside a closed
  LW-PLA tube, and the battery, will heat-soak. The rear motor is semi-exposed, but a
  pusher motor behind a firewall can also run hot. **Add cooling inlets/exits** (e.g. a
  NACA-style inlet at the nose and an exit near the ESC/battery); none is modelled.
- No thermal path/heat-sink for the ESC is provided.

## 4. Interference / EMI

- Planned layout: VTX (x=130) at the front, RX (x=290) mid, ESC (x=400) and motor wiring
  running aft to x≈970. **Long battery→ESC power leads** and the motor phase wires run
  past the receiver — a classic noise-coupling path. The VTX antenna at the nose is close
  to the RX. Recommendations: keep RX antenna away from power/motor wiring and the VTX,
  twist motor leads, add a ferrite/twisted pair, and mount the RX antenna clear of carbon
  spar and battery. **No such provision is drawn.**
- The carbon spar is conductive — keep antennas and wiring clear of it.

## 5. Battery retention, charging, inspection

- Battery tray is a **rail**, explicitly "NOT a qualified restraint system." No strap,
  latch, or crash retention is modelled. A 185 g pack loose in a fuselage is a hazard.
- **Charging:** the pack must be removed; that requires unbolting fuselage sections (no
  hatch). This is a real serviceability and safety friction — a LiPo should be easy to
  remove, inspect, and charge outside the airframe.
- No battery inspection window, no balance-lead routing shown.

## 6. Failsafe

- No receiver failsafe configuration is described. For a rudder/elevator-only aircraft a
  failsafe that commands a gentle spiral/level glide and motor-off is important; this is a
  radio-setup item but should be called out in the build documentation.

## 7. Verdict

The electrical system is a **placeholder list, not a design**. Component ratings, power
distribution, cooling, EMI layout, battery retention, and failsafe are all missing or
unverified. None of this is a geometry defect, but it means the aircraft's propulsion and
avionics cannot be assessed for compatibility or endurance, and several items (cooling,
battery retention, removable pack) are safety-relevant.
