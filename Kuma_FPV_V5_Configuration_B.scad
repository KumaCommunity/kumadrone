/*
 KUMA FPV V5 -- CONFIGURATION B / RECREATIONAL RC CONCEPT (not flight-certified)
 x: nose to rear, y: wing span, z: up. Dimensions in mm.
 For dimensional and assembly coupons, PETG recommended for hardpoints;
 foaming LW-PLA for non-critical skins. Do NOT use unchanged for flight.
 Select part from the part string and export F6 STL. Wing fixed in one location.
 Rear V-tail only; pitch/yaw surfaces illustrative, flight stability not validated.
 Outer surfaces NACA 2412, tail NACA 0010, no real flap hinge/servo sizing.
*/
$fn=36;
part="assembly";
show_preview_battery=true;
show_optional_payload=true; // toggle separately for render; payload mass is a CAD parameter
show_payload_cg_markers=false;
show_joiners=true;
show_structural_rods=true;
show_balance_markers=false; // optional approximate reference only, NOT a proven CG
explode_gap=34;  // visualization offset only; exports unaffected
// V5 Configuration B fixed high wing, mild enlargement from 0.2142 to 0.2275 m^2.
// 7 degrees of geometric dihedral is a trial for rudder-led bank; NOT tested.
L=970; b2=650; root_c=200; tip_c=150;
wing_dihedral_deg=7;
// Single fixed wing station for all retained equipment configurations.
// The equipment envelope is moved to the wing region to minimize CG shift.
// Assumed masses are screened separately in CSV, not calculated in this CAD.
payload_mass_g=0; // 0 = stowed equipment not displayed; 500 = display weight envelope only
payload_max_mass=500; // a NOT-VERIFIED mass target, not a load rating
payload_center=556;
wing_shift=186;
function reference_x()=LEr + (LEt-LEr)*(1+2*(tip_c/root_c))/(3*(1+tip_c/root_c))
  + .28*(2/3*root_c*(1+(tip_c/root_c)+pow(tip_c/root_c,2))/(1+(tip_c/root_c)));
function estimated_cg_x(m)=reference_x(); // DISPLAY MARKER ONLY; refer to CSV for mass-estimated CG
// NOT an actual equilibrium or stability solution.
tail_shift=20; // tail shifted aft nominally to partly restore tail moment
battery_center=410; // illustrative pack shifted near front wing edge
battery_tray_center=410; battery_tray_length=160;
payload_box=[138,46,40]; // x/y/z clear equipment ENVELOPE
tail_span=240; tail_root_chord=190; tail_tip_chord=140;
LEr=310+wing_shift; LEt=334+wing_shift; root_z=56; tip_z=root_z+b2*tan(wing_dihedral_deg);
wall=1.25; radial_gap=0.30;
wing_bounds=[44,246,448,650];
body_cuts=[0,180,360,540,720,900,970];
body_sections=[[0,12],[30,20],[80,34],[155,40],[350,42],[500,40],[700,31],[850,23],[900,21],[970,18]];
key_nominal=[14,36,10]; key_clearance=0.35;
M3_CLEAR=3.5; M3_PILOT=4.0; M3_INSERT_DEPTH=6.8;
M4_CLEAR=4.5; M4_PILOT=5.7; M4_INSERT_DEPTH=9.2;
SPAR_MAIN_OD=8; SPAR_MAIN_HOLE=8.55;
SPAR_AFT_OD=4; SPAR_AFT_HOLE=4.45;
// Configuration B: full-chord fixed wing; no aileron cutout or wiring.
// Volume estimate will need a slicer: foaming density & print walls are not fixed.

function lerp(a,b,u)=a+(b-a)*u;
function clamp(v,a,b)=max(a,min(v,b));
function r_body(x,i=0)= i>=len(body_sections)-2 ?
  lerp(body_sections[len(body_sections)-2][1],body_sections[len(body_sections)-1][1],
    clamp((x-body_sections[len(body_sections)-2][0])/(body_sections[len(body_sections)-1][0]-body_sections[len(body_sections)-2][0]),0,1)) :
  x<=body_sections[i+1][0] ? lerp(body_sections[i][1],body_sections[i+1][1],
    clamp((x-body_sections[i][0])/(body_sections[i+1][0]-body_sections[i][0]),0,1)) : r_body(x,i+1);
function xs()=[for(i=[0:9:L]) i];
// 4-digit analytic airfoil, with 0.1015 open TE term.
function camber(x,m,p)=m==0?0:x<=p?m/(p*p)*(2*p*x-x*x):m/pow(1-p,2)*(1-2*p+2*p*x-x*x);
function slope(x,m,p)=m==0?0:x<=p?2*m/(p*p)*(p-x):2*m/pow(1-p,2)*(p-x);
function thick(x,t)=5*t*(.2969*sqrt(x)-.126*x-.3516*x*x+.2843*x*x*x-.1015*x*x*x*x);
function naca_pt(x,s,m,p,t)=let(z=camber(x,m,p),a=atan(slope(x,m,p)),h=thick(x,t))
  [x-s*h*sin(a),z+s*h*cos(a)];
function outline(m,p,t,a=0,b=1,n=25)=concat(
 [for(k=[0:n]) naca_pt(lerp(b,a,k/n),1,m,p,t)],
 [for(k=[0:n]) naca_pt(lerp(a,b,k/n),-1,m,p,t)]);
function chord(f)=lerp(root_c,tip_c,f);
function LE(f)=lerp(LEr,LEt,f);
function wing_Z(f,x=.28)=lerp(root_z,tip_z,f)+camber(x,.02,.4)*chord(f);
function wing_point(p,f,s)= [LE(f)+p[0]*chord(f),s*f*b2,lerp(root_z,tip_z,f)+p[1]*chord(f)];
function tail_c(f)=lerp(tail_root_chord,tail_tip_chord,f);
function tail_LE(f)=lerp(750+tail_shift,768+tail_shift,f);
function tail_pt(p,f,s)= [tail_LE(f)+p[0]*tail_c(f),s*(12+f*tail_span*cos(40)) + p[1]*tail_c(f)*(-s*sin(40)),
  26+f*tail_span*sin(40)+p[1]*tail_c(f)*cos(40)];
function add(a,b)=[a[0]+b[0],a[1]+b[1],a[2]+b[2]];
function sub(a,b)=[a[0]-b[0],a[1]-b[1],a[2]-b[2]];
function norm(a)=sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]);
function atan2d(y,x)=atan2(y,x);
module cylinder_between(a,b,r){
 d=sub(b,a); n=norm(d);
 translate(a) rotate(a=acos(d[2]/n),v=[-d[1],d[0],0]) cylinder(r=r,h=n);
}
// generic straight polygon loft, 3D mesh sections consistent winding.
module loft(p0,p1){
 n=len(p0);
 polyhedron(points=concat(p0,p1),faces=concat(
 [[for(j=[n-1:-1:0]) j]],[[for(j=[0:n-1]) n+j]],
 [for(j=[0:n-1]) each [[j,(j+1)%n,n+(j+1)%n],[j,n+(j+1)%n,n+j]]]
 ),convexity=10);
}
module along_x(){rotate([0,90,0]) children();}
module hull_body(inside=0){
 // Solid revolution with continuous piecewise linear taper, open-looking ends.
 rotate([0,90,0]) rotate_extrude(convexity=6,$fn=64)
  polygon(points=concat([[0,-1],[max(.05,r_body(0)-inside),-1]],
    [for(i=[0:len(body_sections)-1]) [max(.05,body_sections[i][1]-inside),body_sections[i][0]]],
    [[max(.05,r_body(L)-inside),L+1],[0,L+1]]));
}
module clip_x(xa,xb){translate([xa-.01,-100,-100]) cube([xb-xa+.02,200,200]);}
module hole_y(x,y,z,d,depth=20){
 translate([x,y,z]) rotate([90,0,0]) cylinder(d=d,h=depth,center=true);
}
module shell(i){
 x0=body_cuts[i];x1=body_cuts[i+1];
 difference(){
  intersection(){difference(){hull_body();hull_body(wall);}clip_x(x0,x1);}
  // real radial shell screw clearance. Two radial holes each adjacent seam.
  if(i>0) hole_y(body_cuts[i]+9,0,0,M3_CLEAR,110);
  if(i<len(body_cuts)-2) hole_y(body_cuts[i+1]-9,0,0,M3_CLEAR,110);
 }
}
module PETG_coupler(i){
 x=body_cuts[i+1];
 // Sleeve closely follows inner fuselage taper. Separate replaceable PETG hardpoint.
 difference(){
  union(){
   rotate([0,90,0]) rotate_extrude($fn=64)
    polygon(points=[
       [r_body(x-14)-wall-radial_gap, x-14],
       [r_body(x+14)-wall-radial_gap, x+14],
       [r_body(x+14)-wall-radial_gap-2.4, x+14],
       [r_body(x-14)-wall-radial_gap-2.4, x-14]]);
   for(dx=[-9,9],sgn=[-1,1]){
    r=r_body(x+dx)-wall-radial_gap;
    // thick PETG insert boss extends toward inside fuselage
    translate([x+dx,sgn*(r-4.3),0]) rotate([90,0,0]) cylinder(d=11.8,h=8.4,center=true);
   }
  }
  // M3 x 5.7 heat-set insert holes, nominal 4 mm pilot and 6.8 mm depth.
  for(dx=[-9,9],sgn=[-1,1]){
   r=r_body(x+dx)-wall-radial_gap;
   // Cut inward from the outward face of boss, retaining >=1.6mm backing.
   translate([x+dx,sgn*(r-3.4),0]) rotate([90,0,0]) cylinder(d=M3_PILOT,h=6.8,center=true);
  }
 }
}
// wing geometry: panels are smaller than ~200 mm long to suit ~220-mm beds.
module wing_loft(s,from_y,to_y,a=0,b=1,t=.12){
 pts=outline(.02,.4,t,a,b);
 loft([for(p=pts) wing_point(p,from_y/b2,s)],
      [for(p=pts) wing_point(p,to_y/b2,s)]);
}
module wing_web(s,from_y,to_y,q,width){
 // Solid vertical webs joining upper and lower wing skins.
 function dummy()=0;
 pts0=[for(xx=[q-width/2,q+width/2],sign=[-1,1]) naca_pt(xx,sign,.02,.4,.12)];
 // Rectangle section, clockwise mapping, top/bot stable.
 f0=from_y/b2; f1=to_y/b2;
 function xpoint(f,q)=LE(f)+q*chord(f);
 function zpoint(f,q,sgn)=lerp(root_z,tip_z,f)+naca_pt(q,sgn,.02,.4,.12)[1]*chord(f);
 polyhedron(points=[
  [xpoint(f0,q-width/2),s*from_y,zpoint(f0,q,-1)],
  [xpoint(f0,q+width/2),s*from_y,zpoint(f0,q,-1)],
  [xpoint(f0,q+width/2),s*from_y,zpoint(f0,q,1)],
  [xpoint(f0,q-width/2),s*from_y,zpoint(f0,q,1)],
  [xpoint(f1,q-width/2),s*to_y,zpoint(f1,q,-1)],
  [xpoint(f1,q+width/2),s*to_y,zpoint(f1,q,-1)],
  [xpoint(f1,q+width/2),s*to_y,zpoint(f1,q,1)],
  [xpoint(f1,q-width/2),s*to_y,zpoint(f1,q,1)]],
  faces=[[3,2,1,0],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]);
}
module wing_spar(s,y0,y1,q,dr){
 f0=y0/b2;f1=y1/b2;
 cylinder_between([LE(f0)+q*chord(f0),s*y0,wing_Z(f0,q)],
                  [LE(f1)+q*chord(f1),s*y1,wing_Z(f1,q)],dr/2);
}
module wing_key_slot(s,edge,into){
 // Edge = spanwise joint, into = +1 for panel on outside, -1 inside.
 f=edge/b2;xc=LE(f)+.52*chord(f);zc=wing_Z(f,.52);
 translate([xc,s*(edge+into*9),zc]) cube([14+2*key_clearance,18+2*key_clearance,10+2*key_clearance],center=true);
}
module wing_screw_hole(s,edge,into){
 yy=edge+into*10;f=yy/b2;
 // Vertical clearance bore from top skin through the PETG key pocket.
 // Bore crosses the outer airfoil skin; previous 16-mm blind bore did not.
 translate([LE(f)+.52*chord(f),s*yy,wing_Z(f,.52)])
   cylinder(d=M3_CLEAR,h=38,center=true);
}
module wing_panel(s=1,seg=0){
 y0=wing_bounds[seg]; y1=wing_bounds[seg+1];
 b=1;
 difference(){
  union(){
   difference(){
    wing_loft(s,y0,y1,0,b,.12);
    wing_loft(s,y0+1.5,y1-1.5,.040,b-.027,.12*.88);
   }
   wing_web(s,y0,y1,.28,.081);
   wing_web(s,y0,y1,.63,.058);
   // anti-twist PETG key pocket web at 52% chord
   wing_web(s,y0,min(y0+24,y1),.52,.15);
   wing_web(s,max(y1-24,y0),y1,.52,.15);
  }
  wing_spar(s,y0-2,y1+2,.28,SPAR_MAIN_HOLE);
  wing_spar(s,y0-2,y1+2,.63,SPAR_AFT_HOLE);
  wing_key_slot(s,y0,+1);
  wing_key_slot(s,y1,-1);
  wing_screw_hole(s,y0,+1);
  wing_screw_hole(s,y1,-1);
 }
}
module wing_center(){
 // Hollow PETG center section, stiffened around 2 spar bores and M4 holes.
 difference(){
  union(){
   difference(){
    union(){wing_loft(1,0,44,0,1,.12);wing_loft(-1,0,44,0,1,.12);}
    union(){wing_loft(1,2,43,.04,.965,.12*.85);wing_loft(-1,2,43,.04,.965,.12*.85);}
   }
   for(s=[-1,1]) {
    wing_web(s,0,44,.28,.09);wing_web(s,0,44,.63,.065);
    wing_web(s,20,44,.52,.15);
   }
   // Material immediately around mounting bolts.
   for(xx=[346+wing_shift,465+wing_shift],yy=[-20,20])
     translate([xx,yy,56]) cylinder(d=11,h=14,center=true);
  }
  for(s=[-1,1]){
   wing_spar(s,-2,46,.28,SPAR_MAIN_HOLE);
   wing_spar(s,-2,46,.63,SPAR_AFT_HOLE);
   wing_key_slot(s,44,-1);
   wing_screw_hole(s,44,-1);
  }
  for(xx=[346+wing_shift,465+wing_shift],yy=[-20,20])
   translate([xx,yy,58]) cylinder(d=M4_CLEAR,h=50,center=true);
 }
}

module PETG_wing_key(){
 // Key at each wing segment boundary. Install two M3 x 5.7 inserts from top.
 difference(){
   cube(key_nominal,center=true);
   for(yy=[-10,10])
     translate([0,yy,5-M3_INSERT_DEPTH/2+.02])
       cylinder(d=M3_PILOT,h=M3_INSERT_DEPTH,center=true);
 }
}
module tail_loft(s,f0,f1,a=0,b=1,tc=.10){
 pts=outline(0,.4,tc,a,b);
 loft([for(p=pts) tail_pt(p,f0,s)], [for(p=pts) tail_pt(p,f1,s)]);
}
module tail_fixed(s){
 difference(){
  tail_loft(s,0,1,0,.75,.10);
  tail_loft(s,.02,.98,.04,.725,.10*.88);
 }
}
module ruddervator(s){
 difference(){
  tail_loft(s,0,1,.766,1,.10);
  tail_loft(s,.025,.975,.782,.968,.10*.88);
 }
}
// Separate detachable tail shoe and fuselage-mounted insert block prototypes.
module PETG_tail_saddle(){
 // Lightweight rectangular frame with four M3 receiving bosses.
 difference(){
  union(){
   for(y=[-22,22]) translate([799+tail_shift,y,27]) cube([112,9,9],center=true);
   for(x=[772+tail_shift,829+tail_shift])translate([x,0,27])cube([14,57,9],center=true);
   for(x=[772+tail_shift,829+tail_shift],y=[-15,15]) translate([x,y,22]) cylinder(d=12,h=13);
  }
  for(x=[772+tail_shift,829+tail_shift],y=[-15,15])
    translate([x,y,35-M3_INSERT_DEPTH/2+.01]) cylinder(d=M3_PILOT,h=M3_INSERT_DEPTH,center=true);
 }
}

module PETG_tail_shoe(s){
 // Alignment key and mounting shoe for removable tail panel. Simplified.
 difference(){
  union(){
   translate([800+tail_shift,s*15,38]) cube([94,19,8],center=true);
   translate([800+tail_shift,s*15,41]) cube([65,12,7],center=true);
  }
  for(x=[772+tail_shift,829+tail_shift]) translate([x,s*15,40]) cylinder(d=M3_CLEAR,h=35,center=true);
 }
}
module PETG_saddle_plate(){
 // Spar-support wing-center PETG lattice; avoid a dense 166x67 solid block.
 difference(){
  union(){
   for(y=[-20,20]) translate([405+wing_shift,y,40]) cube([166,10,7],center=true);
   for(x=[346+wing_shift,465+wing_shift])translate([x,0,40])cube([12,67,7],center=true);
   for(x=[346+wing_shift,465+wing_shift],y=[-20,20]) translate([x,y,34]) cylinder(d=14,h=13);
  }
  for(x=[346+wing_shift,465+wing_shift],y=[-20,20])
   translate([x,y,47-M4_INSERT_DEPTH/2]) cylinder(d=M4_PILOT,h=M4_INSERT_DEPTH,center=true);
 }
}

module PETG_battery_tray(){
 // Fore/aft rail for battery fit and CG trials; NOT a qualified restraint system.
 // Adjustment envelope assumes a 122 mm example battery and clear access.
 difference(){
  union(){
   for(y=[-22,22]) translate([battery_tray_center,y,-7])
      cube([battery_tray_length,7,5],center=true);
   for(x=[battery_tray_center-battery_tray_length/2+6,
           battery_tray_center,
           battery_tray_center+battery_tray_length/2-6])
      translate([x,0,-7])cube([10,49,4],center=true);
   for(y=[-22,22])translate([battery_tray_center,y,-2])
      cube([battery_tray_length,3,7],center=true);
  }
  for(x=[battery_tray_center-battery_tray_length/2+12,
         battery_tray_center+battery_tray_length/2-12],y=[-14,14])
    translate([x,y,-7]) cylinder(d=M3_CLEAR,h=30,center=true);
 }
}


// Non-dropping, removable near-wing equipment tray. Mounting/retention is illustrative.
// Volume is 138 x 46 x 40 = 254 cm^3, NOT a blanket 500 g battery fit claim.
// Retained cargo only; no payload-release hardware.
module PETG_forward_equipment_tray(){
 x=payload_center; len=payload_box[0]; wide=payload_box[1]; high=payload_box[2];
 difference(){
  union(){
   // lightweight longitudinal bed frame beneath equipment envelope
   for(y=[-(wide/2+2),(wide/2+2)]) translate([x,y,-high/2-2])
      cube([len+7,3.2,3.2],center=true);
   for(xx=[x-len/2-2,x,x+len/2+2])translate([xx,0,-high/2-2])
      cube([5,wide+7,3.2],center=true);
   // end walls have lightened centers for wiring/service access
   for(xx=[x-len/2-3,x+len/2+3])
     translate([xx,0,0]) difference(){
       cube([3.5,wide+7,high+4],center=true);
       cube([5,wide-4,high-7],center=true);
     }
   // small side-retainer tabs; final restraints are not specified
   for(xx=[x-25,x+25],sgn=[-1,1]) translate([xx,sgn*(wide/2+1),-high/2+4])
      cube([9,5,13],center=true);
  }
  // Nominal clearance holes only, mating bosses and restraint still require design
  for(xx=[x-len/2+12,x+len/2-12],sgn=[-1,1])
    translate([xx,sgn*(wide/2+1),-high/2-2])
      cylinder(d=M3_CLEAR,h=12,center=true);
 }
}
module optional_payload_envelope(){
 color([.18,.77,.57,.48]) translate([payload_center,0,0])
  cube(payload_box,center=true);
}

// Non-structural removable printed upper fairing. Mounting tabs and screw heads
// are visual prototypes only; bench checks required for clearance and retention.
module dorsal_fairing(){
 difference(){
  hull(){
   translate([445,0,54]) scale([45,34,20]) sphere(r=1,$fn=20);
   translate([605,0,54]) scale([36,34,16]) sphere(r=1,$fn=20);
  }
  translate([395,-55,-70]) cube([285,110,137]); // shell above z=67
  // M3 fairing bores; these are NOT mating hardpoints
  for(x=[454,598],y=[-19,19])
   translate([x,y,73]) cylinder(d=M3_CLEAR,h=25,center=true);
 }
}
module camera_plate(){
 // Camera envelope: universal 14x14 body / up to 19x19 bracket; verify camera.
 difference(){
  translate([38,0,0]) cube([8,32,32],center=true);
  translate([38,0,0]) along_x() cylinder(d=12.5,h=12,center=true);
  for(y=[-11,11],z=[-11,11]) translate([38,y,z]) along_x() cylinder(d=2.1,h=12,center=true);
 }
}
module insert_fit_coupon(){
 // Small, quick PETG test. Verify on actual filament/printer before other parts.
 difference(){
   translate([0,0,7])cube([66,26,14],center=true);
   translate([-19,0,14-M3_INSERT_DEPTH/2+.01])cylinder(d=M3_PILOT,h=M3_INSERT_DEPTH,center=true);
   translate([19,0,14-M4_INSERT_DEPTH/2+.01])cylinder(d=M4_PILOT,h=M4_INSERT_DEPTH,center=true);
 }
}
module prop_and_motor_envelope(){
 color([.2,.3,.35,.65]) translate([969,0,65]) along_x() cylinder(d=36,h=32,center=true);
 color([.15,.18,.20,.45]) translate([993,0,65]) rotate([0,90,0]) cylinder(d=150,h=3,center=true);
}
module reference_model(is_exploded=false){
 e=is_exploded ? explode_gap : 0;
 for(i=[0:len(body_cuts)-2]) translate([i*e,0,0]) color([.76,.8,.81,.65]) shell(i);
 if(show_joiners) for(i=[0:len(body_cuts)-3]) translate([(i+.5)*e,0,0]) color([.22,.24,.29]) PETG_coupler(i);
 translate([2*e,0,0]) color([.72,.75,.77]) wing_center();
 for(s=[-1,1],j=[0:2]) translate([2*e,s*(j+1)*e,0]) color([.87,.83,.72]) wing_panel(s,j);
 if(!is_exploded) for(s=[-1,1],edge=[44,239.333,434.667]) {
   f=edge/b2; color([.3,.4,.46]) translate([LE(f)+.52*chord(f),s*edge,wing_Z(f,.52)]) PETG_wing_key();
 }
 for(s=[-1,1]) translate([5*e,s*e,0]) color([.80,.78,.70]) tail_fixed(s);
 for(s=[-1,1]) translate([5*e,s*e,e*.20]) color([.60,.75,.72]) ruddervator(s);
 translate([5*e,0,0]) color([.33,.35,.39]) PETG_tail_saddle();
 for(s=[-1,1]) translate([5*e,s*.5*e,0]) color([.29,.31,.35]) PETG_tail_shoe(s);
 translate([2*e,0,0]) color([.33,.35,.39]) PETG_saddle_plate();
 translate([e,0,0]) color([.28,.37,.42]) PETG_battery_tray();
 color([.23,.26,.29]) camera_plate();
 translate([e,0,0]) color([.25,.55,.43]) PETG_forward_equipment_tray();
 if(show_optional_payload && payload_mass_g>0 && !is_exploded) optional_payload_envelope();
 if(show_structural_rods && !is_exploded){
  for(s=[-1,1]){
   color([.12,.13,.14]) wing_spar(s,0,620,.28,8);
   color([.18,.19,.20]) wing_spar(s,0,620,.63,4);
  }
 }
 if(show_preview_battery)color([.1,.52,.68,.7])translate([battery_center+e,0,6])cube([122,38,30],center=true);
 if(show_balance_markers && !is_exploded){
   // Marker A: illustrative 28% MAC reference, not a validated neutral point.
   // Marker B: identical display reference; real CG is calculated in separate CSV.
   color([.93,.68,.20])translate([reference_x(),0,-72]) cylinder(d=3,h=170);
   // Real empty/loaded CG values appear only in CSV; not a CAD-rendered guarantee.
   
 }
 translate([5*e,0,0]) prop_and_motor_envelope();
}

if(part=="assembly") reference_model(false);
else if(part=="exploded") reference_model(true);
else if(part=="payload_preview") {
  // The exposed forward-bay preview is for dimensional discussion, not a structural cutaway.
  color([.65,.70,.73,.22]) shell(0);
  color([.65,.70,.73,.22]) shell(1);
  color([.24,.46,.36]) PETG_forward_equipment_tray();
  optional_payload_envelope();
  color([.18,.29,.34]) camera_plate();
  color([.15,.48,.69,.50]) translate([battery_center,0,6])cube([122,38,30],center=true);
}
else if(part=="wing_center") wing_center();
else if(part=="wing_R1") wing_panel(1,0);
else if(part=="wing_R2") wing_panel(1,1);
else if(part=="wing_R3") wing_panel(1,2);
else if(part=="wing_L1") wing_panel(-1,0);
else if(part=="wing_L2") wing_panel(-1,1);
else if(part=="wing_L3") wing_panel(-1,2);
else if(part=="tail_R") tail_fixed(1);
else if(part=="tail_L") tail_fixed(-1);
else if(part=="ruddervator_R") ruddervator(1);
else if(part=="ruddervator_L") ruddervator(-1);
else if(part=="tail_saddle") PETG_tail_saddle();
else if(part=="tail_shoe_R") PETG_tail_shoe(1);
else if(part=="tail_shoe_L") PETG_tail_shoe(-1);
else if(part=="saddle_plate") PETG_saddle_plate();
else if(part=="wing_key") PETG_wing_key();
else if(part=="insert_fit_coupon") insert_fit_coupon();
else if(part=="battery_tray") PETG_battery_tray();
else if(part=="forward_equipment_tray") PETG_forward_equipment_tray();
else if(part=="camera_plate") camera_plate();
else if(part=="dorsal_fairing") dorsal_fairing();
else if(part=="m3_coupler_coupon") PETG_coupler(1);
else if(part=="wing_profile_2d") polygon([for(p=outline(.02,.4,.12,0,1,80)) [p[0]*root_c,p[1]*root_c]]);
else for(i=[0:len(body_cuts)-2]){
 if(part==str("fuselage_",i)) shell(i);
 if(i<len(body_cuts)-2 && part==str("coupler_",i)) PETG_coupler(i);
}
