# Kuma FPV V6.2 Configuration B

**Status: bench prototype.** The 1.30 m recreational fixed wing retains the 7° wing dihedral, 300 mm per-side V-tail at 47°, two ruddervators and rear pusher. The first fit article uses no optional equipment or fin.

- [CAD](Kuma_FPV_V6_2_Configuration_B.scad) and [part meshes](STL/)
- [Starting BOM](reference/starting_bom.csv) and [wiring and bench checks](WIRING_AND_BENCH.md)
- [Mesh results](data/mesh_verification.csv), [interference checks](data/fit_verification.csv), [mass and balance](data/mass_balance.csv) and [aerodynamic screen](data/vspaero_screen.csv)

## What changed

| Assembly | V6.2 design | Fit work |
|---|---|---|
| Wing attachment | Two split PETG collars wrap the fuselage. The upper halves follow the wing underside and have side-loading M4 nut pockets. The two carbon spar lines have separate angled, bored metal sockets seated in the center section. | Fit both collars with thin non-slip shims. Check shim compression, tube insertion and the fastener stack. Proof-test the carry-through, carbon bonds and shell together. |
| Tail and servos | The fixed tail incorporates reinforced root tabs with bolts through two split collars. Three recessed commercial pin hinges per side link fixed and moving surfaces. Bolted PETG horns and external links connect to removable side servo plates. | Shim the horn foot to bear flat and use backing washers. Make a hinge coupon with the actual hinge and adhesive. Confirm pin-axis alignment, combined travel, stiffness and servo-plate fastener access. |
| Battery and cooling | A forward hatch allows the maximum quoted battery case to lift vertically at x=180 and 242 mm. A rail tray, strap passages and removable lid provide access and restraint provisions. Cooling slots open through both sides of the forward shell. | Establish pack lead clearance and add padded positive stops. Install the four hatch backing tabs and verify their bond and screw engagement. Baffle or position the ESC for real airflow and measure temperatures. |
| Pusher | Two split collars, an open pylon, a replaceable 4 mm aluminum firewall, a rear skid and a wire exit. The motor envelope and firewall share z=76 mm. | Match-drill the firewall, fit the actual prop adapter and secure the motor leads away from the disk. Check skid clearance during pitch-up and under flex. |
| Yaw | A removable dorsal fin replaces the belly-fin experiment in CAD. The default assembly omits the dorsal fin. | The sampled VSPAERO response did not show a yaw improvement. Hold the fin as a fit experiment and resolve yaw/roll authority independently. |

## Parts and hardware interfaces

- Use the material column and quantities in the generated mesh report. The metric coordinate axes are x aft, y right and z up. The envelope check uses a 220 × 220 × 250 mm volume in the exported axes. Verify oriented supports, brims, warping and the internal slicer paths on your printer. Exported STL registration coordinates are shared across the assembly.
- Model wing center, collars, tray, pylon, horn and servo plates in PETG. The two socket meshes and firewall mesh are **6061-T6 reference geometry** for manufacturing and fit. The socket bores are nominal 8.18 and 4.18 mm, run from y=±7 to ±36 mm, and follow the two spar axes. Confirm actual tube OD and bonding allowance before machining. The current collar closure uses M3 through-fasteners, and the wing seats use M4 captive nuts.
- Use the purchased motor as the firewall drill template. The four Ø3.5 mm corner holes at y/z=±16 mm are firewall-to-pylon fasteners. The center hole is for shaft clearance. Specify the motor-to-firewall holes and screw engagement from the as-delivered motor.
- The servo plate uses a 24 × 13 mm opening. Transfer the actual ear pattern by fitting the delivered servos. The modeled pushrod is a centerline envelope for a neutral setup. Confirm complete ends, arms, cable exits and mixed travel on the fitted assembly.
- Turn on the dorsal fin in the OpenSCAD source for an optional fit check. Keep its fastener holes accessible. The fin mesh and insert coupon have installed quantity zero in the mass model.

## Verification and remaining flight gates

The OpenSCAD validation checks fresh mesh topology and nominal assembly geometry. The hatch, servo access, cooling and motor cable openings were checked with geometric intersections. The ruddervator test sampled ±20° relative to the fixed tail and the prop check used a nominal disk with 3 mm additional envelope clearance. Actual hinges, servo motion, manufacturing tolerances, ground pitch and structural deflection require hardware tests. The nominal disk bottom is z=−25.6 mm and the skid reaches z≈−40 mm, about 14 mm of static vertical difference before flex and pitch.

Mesh-derived material masses and vendor or estimated bought hardware put the **nominal no-FPV build at about 1.62 kg**. The nominal pack at x=190 mm gives an estimated CG near x=547.9 mm. The forward stop at x=180 gives about x=546.5 mm. The aft fit position gives about x=555.4 mm, near the modeled neutral point. Use the aft endpoint as a fit check only. The assumptions include LW-PLA 0.35 g/cm³, PETG 1.27 g/cm³, ideal CAD volumes, and estimated hardware and wiring stations. The 10.7 m/s stall calculation assumes sea-level density and CLmax=1.0. A guarded thrust-stand result and a measured launch envelope are needed before selecting a release speed.

The simplified thick-surface VSPAERO model includes a fuselage pod and cambered main wing. The no-fin neutral point is **x=555.35 mm** from a fit over −4° to +8°. That implies about **+4.2% MAC** at the nominal estimated CG and **+5.0%** at the forward-pack estimate. The fin was present in the solver mesh. Raw CMz sideslip slopes were +0.01276 and +0.03365 per radian at 2° and 6° angle of attack without the fin, and +0.00603 and +0.02649 with it. The model uses a simplified pod and lacks powered propwash, as-built deflections and dynamic derivatives. The pitch screen depends on measured CG and trim, and rudder-to-roll authority remains a flight gate. [NASA VSPAERO basics](https://www.nasa.gov/reference/openvsp-vspaero-basics/)

## Reproduce

From this directory, with Python, NumPy, trimesh, networkx and OpenSCAD on PATH:

```sh
python3 scripts/validate.py
python3 scripts/mass_balance.py
python3 openvsp/run_panel.py --out /tmp/kuma-v62-panel-new
```

The OpenSCAD test runner accepts `--openscad` with a command prefix. The Mac audit used `--openscad '/usr/bin/arch -x86_64 /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'` after the native Qt build aborted under the sandbox. The VSPAERO runner defaults to the Mac app path and accepts `--vspscript` to point to another installation. Each run needs a fresh output directory for the solver cases. Saved polars and the summary table in `data/` came from OpenVSP/VSPAERO 7.2.2. Legacy V5 and V6.1 tooling and records are retained as revision history.
