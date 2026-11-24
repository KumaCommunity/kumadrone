# V6.2 electrical plan and bench release

## Wiring

| Source | Destination | Interface |
|---|---|---|
| 4S LiPo | Skywalker 50A V2 battery input | XT60 on the proposed harness. Verify polarity with a meter and insulate the joints. |
| Skywalker ESC | X2216 V3 motor | Three phase leads. Secure the extended leads through the aft grommet and pylon along a route clear of the prop. Keep the battery-side wiring short. |
| Skywalker throttle/BEC three-wire plug | ER6 PWM throttle output | PWM signal, 5 V BEC and common ground. Confirm pin ordering from the hardware labels. Use this as the primary servo/receiver supply. |
| ER6 left and right V-tail PWM outputs | Two EMAX ES08MA II servos | Assign one output per side in the radio and use standard analog-servo PWM timing. Route extension connectors where they can be secured and inspected. |
| Optional filtered 5 V branch | RunCam Nano 4 and Unify Pro32 Nano | Common signal ground and camera video to VTX video input. Budget the measured branch load. Attach the antenna before VTX power. |
| Optional ER6 battery-sense input | Battery positive through the manufacturer harness | Use only the dedicated voltage sense lead and the ER6 manual. The 4S pack voltage is above the receiver's servo rail rating. |

Place the ESC near the aft cooling slots around x=293 mm, the receiver around x=118 mm, and the two servos around x=753 mm. Separate receiver antenna elements from carbon, high-current wiring and the video transmitter. Route and secure leads before balancing. An experienced pilot can commission the first article in line-of-sight with the direct PWM radio setup and the FPV branch disconnected. [RadioMaster ER6](https://radiomasterrc.com/products/er6-2-4ghz-elrs-pwm-receiver) · [Hobbywing ESC manual](https://www.hobbywing.com/en/uploads/file/20250930/64b726be7a56c9f415385f77683cdc46.pdf)

## Bench sequence

1. **Fit and retention.** Print the insert coupon, one wing collar pair, one hinge station and one servo plate. Install real inserts and measure pull-out and bearing. Check full battery insertion with both leads, two straps and padded fore/aft stops. Check tray-hatch access and motor cable strain relief.
2. **Structure.** Weigh the final parts and assembled aircraft. Proof the wing and tail mounts, spar splice, motor pylon, collar restraint and battery tray using documented loads from the measured airframe and its proposed flight envelope. Inspect for slip, set or cracks after unloading. Include landing/skid loads before using the 8-inch prop.
3. **Controls and loss of link.** With the prop removed, calibrate throttle and verify motor inhibit, direction of both independent V-tail mixes, endpoints, repeatability and combined-stick behavior. Check for high servo current or drop in receiver voltage. Test transmitter-off loss of link with a demonstrably motor-off throttle command. Perform a radio range check in the assembled configuration.
4. **Powertrain.** On a guarded stand, start with the APC 8×4E. Fit the correct hub ring, orient the blade for aft airflow and verify rotation, RPM, static thrust, current, temperature and BEC stability. The APC 8×6EP is an alternate for later testing. SunnySky publishes about 1.37 kgf at 36.2 A on 14.8 V with its APC 8×6 test prop. That is a vendor bench reference for a similar prop, with no extrapolation to this installation or a fresh 16.8 V pack. Confirm the actual motor, prop and ESC limits before increasing load. [SunnySky test table](https://sunnyskyusa.com/products/sunnysky-x2216) · [APC RPM limits](https://www.apcprop.com/wp-content/uploads/2022/03/APC-Propeller-RPM-Limits-rev5.pdf)
5. **Release for a maiden.** Record the as-built mass/CG, prove trim and lateral control authority, and establish the allowable launch and landing envelope from the actual configuration. Use an experienced fixed-wing RC pilot and a segregated site for the initial line-of-sight flight. In the U.S., check registration, TRUST, airspace and Remote ID or FRIA applicability before flight. [FAA recreational flyer rules](https://www.faa.gov/uas/recreational_flyers)
