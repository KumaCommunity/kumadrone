include <../Kuma_FPV_V6_2_Configuration_B.scad>
probe = is_undef(probe) ? "" : probe;
module bare_shell(){ difference(){ hull_body(); hull_body(wall); } }
module battery_access(x){ hull(){ battery_envelope(x); translate([0,0,75]) battery_envelope(x); } }
module model_tail(){
  for(s=[-1,1]) { tail_fixed(s); ruddervator(s); control_horn(s); }
}
if(probe=="battery_access_forward")
  intersection(){ battery_access(180); shell(1); }
if(probe=="battery_access_aft")
  intersection(){ battery_access(242); shell(1); }
if(probe=="battery_tray_pack")
  intersection(){ battery_tray(); for(x=[180,242]) battery_envelope(x); }
if(probe=="hatch_lid_shell")
  intersection(){ battery_hatch_lid(); shell(1); }
if(probe=="cooling_inlet")
  intersection(){ cooling_inlet_cut(); bare_shell(); }
if(probe=="cooling_exit")
  intersection(){ cooling_exit_cut(); bare_shell(); }
if(probe=="servo_access")
  intersection(){ servo_hatch_cut(); bare_shell(); }
if(probe=="motor_wire_exit")
  intersection(){ motor_wire_exit_cut(); bare_shell(); }
if(probe=="servo_case_fit")
  intersection(){ servo_envelope(1); servo_plate(1); }
if(probe=="linkage_wall")
  intersection(){ linkage_preview(1); shell(4); }
if(probe=="spar_socket")
  intersection(){ for(q=[.28,.63]) wing_splice(q); wing_center(); }
if(probe=="spar_tube"){
  intersection(){
    for(q=[.28,.63]) wing_splice(q);
    union() for(q=[.28,.63],s=[-1,1]) wing_spar(s,7,36,q,spar_od(q));
  }
}
if(probe=="wing_collar_clearance")
  intersection(){
    for(x=[532,651]) wing_collar(x,true);
    union(){ wing_center(); shell(2); shell(3); }
  }
if(probe=="tail_mount")
  intersection(){ for(x=[807,853]) tail_collar(x,true); tail_fixed(1); }
if(probe=="horn_motion")
  intersection(){ tail_fixed(1); move_ruddervator(1,ruddervator_deg){ ruddervator(1); control_horn(1); } }
if(probe=="prop_clearance")
  intersection(){ prop_disk(3); union(){ shell(5); model_tail(); motor_firewall(); motor_pylon(); lower_rear_skid(); } }
if(probe=="motor_mount")
  intersection(){ motor_pylon(); for(x=[925,949]) motor_collar(x,true); }
