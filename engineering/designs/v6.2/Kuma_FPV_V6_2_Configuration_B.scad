/*
 Kuma FPV V6.2 Configuration B | recreational fixed-wing bench prototype.
 x: nose to tail, y: right, z: up. All dimensions in mm.
 See README.md for materials, hardware interfaces and verification status.
*/
$fn=36;
part = is_undef(part) ? "assembly" : part; // override via -D 'part="..."' for CLI export
show_preview_battery = true;
show_structural_rods = true;
show_dorsal_fin = false;
ruddervator_deg = is_undef(ruddervator_deg) ? 0 : ruddervator_deg;
L=970; b2=650; root_c=200; tip_c=150;
wing_dihedral_deg=7;
wing_shift=186;
tail_shift=20;
battery_center=190;
battery_size=[113,36,32];  // Manufacturer maximum case dimensions, without leads
battery_z=0;
tail_span=300; tail_root_chord=200; tail_tip_chord=150; tail_dih=47;
LEr=310+wing_shift; LEt=334+wing_shift; root_z=56; tip_z=root_z+b2*tan(wing_dihedral_deg);
wall=1.25; radial_gap=0.30;
wing_bounds=[44,246,448,650];
body_cuts=[0,102,321,540,720,900,970];
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
function tail_pt(p,f,s)= [tail_LE(f)+p[0]*tail_c(f),s*(12+f*tail_span*cos(tail_dih)) + p[1]*tail_c(f)*(-s*sin(tail_dih)),
  26+f*tail_span*sin(tail_dih)+p[1]*tail_c(f)*cos(tail_dih)];
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
// ===================== V6 ADDITIONS =====================
// Service openings. The upper openings face +z. The vent pairs face ±y.
module camera_aperture_cut(){
  translate([22,0,0]) along_x() cylinder(d=13,h=64,center=true);
}
module cooling_inlet_cut(){
  for(s=[-1,1]) translate([163,s*39,0]) rotate([90,0,0])
    hull() for(dx=[-6,6]) translate([dx,0,0]) cylinder(d=7,h=15,center=true);
}
module cooling_exit_cut(){
  for(s=[-1,1]) translate([295,s*42,0]) rotate([90,0,0])
    hull() for(dx=[-8,8]) translate([dx,0,0]) cylinder(d=8,h=15,center=true);
}
module battery_hatch_cut(clear=0){
  translate([211,0,41]) cube([180+2*clear,48+2*clear,62],center=true);
}
module servo_hatch_cut(clear=0){
  for(s=[-1,1]) translate([753,s*28,0]) cube([38+2*clear,28,22+2*clear],center=true);
}
function servo_hole_x(dx) = 753+dx;
module servo_mount_holes(){
  for(s=[-1,1],dx=[-24,24],z=[-8,8]) hole_y(servo_hole_x(dx),s*26,z,2.7,18);
}
module motor_wire_exit_cut(){ hole_y(961,-18,-2,7,15); }
module cooling_window(i){
  if(i==1) { cooling_inlet_cut(); cooling_exit_cut(); battery_hatch_cut(); }
  if(i==4) { servo_hatch_cut(); servo_mount_holes(); }
  if(i==5) motor_wire_exit_cut();
}

// Split PETG collars seat around the fuselage and carry the wing and tail.
// Both halves have two hardware ears, with free clearance and a shim allowance.
function collar_y(x)=r_body(x)+5.7;
module collar_half(x,w,upper=true){
  zsign=upper?1:-1;
  difference(){
    union(){
      intersection(){
        difference(){ hull_body(-3.6); hull_body(-.35); }
        translate([x,0,zsign*33.15]) cube([w,125,66],center=true);
      }
      for(s=[-1,1]) translate([x,s*(collar_y(x)-2),zsign*3.3])
        cube([w,12,6.3],center=true);
    }
    hull_body(-.35);
    for(s=[-1,1]) translate([x,s*collar_y(x),0]) cylinder(d=M3_CLEAR,h=24,center=true);
  }
}
module wing_underside_clearance(){
  translate([0,0,-.35]) {
    for(s=[-1,1]) wing_loft(s,0,44,0,1,.12);
    wing_center();
  }
  for(x=[532,651],y=[-20,20]) translate([x,y,57]) cylinder(d=11.8,h=16.7,center=true);
}
module wing_collar(x,upper){
  if(!upper) collar_half(x,15,false);
  else difference(){
    union(){
      collar_half(x,15);
      // Tapered supports bridge the crown to the actual wing underside.
      hull(){
        translate([x,0,r_body(x)+1.2]) cube([15,15,4],center=true);
        translate([x,0,51]) cube([15,55,12],center=true);
      }
    }
    hull_body(-.35);
    wing_underside_clearance();
    for(y=[-20,20]) {
      translate([x,y,43]) cylinder(d=M4_CLEAR,h=40,center=true);
      // Captive M4 nut recess opens from the side under the bearing surface.
      translate([x,y,44.5]) cube([17,7.4,3.5],center=true);
    }
  }
}

// Separate left/right tubes bottom in machined two-sided dihedral sockets.
function spar_axis(q,s,y) =
  [LE(y/b2)+q*chord(y/b2),s*y,wing_Z(y/b2,q)];
function splice_od(q)=q<.5?13:9;
function spar_od(q)=q<.5?SPAR_MAIN_OD:SPAR_AFT_OD;
module wing_splice(q){
  difference(){
    union(){
      translate(spar_axis(q,1,0)) sphere(d=splice_od(q));
      for(s=[-1,1])
        cylinder_between(spar_axis(q,s,0),spar_axis(q,s,36),splice_od(q)/2);
    }
    for(s=[-1,1])
      cylinder_between(spar_axis(q,s,7),spar_axis(q,s,38),(spar_od(q)+.18)/2);
  }
}
module wing_splice_pocket(q){
  translate(spar_axis(q,1,0)) sphere(d=splice_od(q)+.5);
  for(s=[-1,1])
    cylinder_between(spar_axis(q,s,0),spar_axis(q,s,36.3),(splice_od(q)+.5)/2);
}

// Battery sits on a strapped PETG tray directly below its removable hatch.
module battery_envelope(x=battery_center){
  translate([x,0,battery_z]) cube(battery_size,center=true);
}
module battery_tray(){
  difference(){
    union(){
      for(s=[-1,1]) translate([216,s*17,-18]) cube([184,16,3],center=true);
      for(x=[133,216,298]) translate([x,0,-18]) cube([13,50,3],center=true);
      for(x=[133,298],y=[-18,18]) hull(){
        translate([x,y,-19]) cylinder(d=10,h=3,center=true);
        translate([x,y,-32]) cylinder(d=8,h=6,center=true);
      }
      for(s=[-1,1]) translate([216,s*20,-15]) cube([184,2.5,6],center=true);
    }
    for(x=[151,173,195,232,254,276],y=[-23,23])
      translate([x,y,-18]) cube([15,3,10],center=true);
    for(x=[133,298],y=[-18,18])
      translate([x,y,-27]) cylinder(d=M3_CLEAR,h=40,center=true);
    difference(){ cube([2200,400,400],center=true); hull_body(1.4); }
  }
}
module tray_shell_holes(){
  for(x=[133,298],y=[-18,18])
    translate([x,y,-34]) cylinder(d=M3_CLEAR,h=25,center=true);
}
module hatch_holes(){
  for(x=[125,297],y=[-18,18])
    translate([x,y,37]) cylinder(d=2.7,h=24,center=true);
}
module battery_hatch_lid(){
  difference(){
    intersection(){
      difference(){ hull_body(); hull_body(2.35); }
      battery_hatch_cut(-.3);
    }
    hatch_holes();
  }
}
module battery_hatch_tab(x,s){
  difference(){
    intersection(){
      translate([x,s*18,37]) cube([29,10,14],center=true);
      hull_body(1.35);
    }
    battery_hatch_lid();
    translate([x<211?125:297,s*18,37]) cylinder(d=2.1,h=16,center=true);
  }
}

// Side plates trap the servo cases from outside and leave access to horn/linkage.
module servo_plate(s){
  difference(){
    intersection(){
      translate([753,s*40,0]) cube([56,35,30],center=true);
      difference(){ hull_body(-2.8); hull_body(-.28); }
    }
    // 24 x 13-mm universal opening. Drill ears to the delivered servo drawing.
    translate([753,s*29,0]) cube([24,30,13],center=true);
    servo_mount_holes();
  }
}
module servo_envelope(s){
  translate([753,s*26,0]) cube([23.5,24,12.6],center=true);
}
function horn_ball(s) = let(p=hinge_pt(horn_f(),s))
  add(p,[3,s*15*sin(tail_dih),-15*cos(tail_dih)]);
module linkage_preview(s){
  cylinder_between([759,s*39,-4],horn_ball(s),1);
}
module camera_cradle(){
  difference(){
    translate([43,0,0]) cube([13,29,29],center=true);
    translate([43,0,0]) cube([16,15.3,15.3],center=true);
    for(y=[-10.5,10.5]) translate([43,y,0]) cylinder(d=2.1,h=31,center=true);
  }
}

// Motor pylon has its own two clamping stations and a replaceable firewall.
motor_x=969;
motor_z=76;
prop_x=1022;
prop_d=203.2;
module motor_pylon(){
  difference(){
    union(){
      difference(){
        translate([965,0,motor_z]) cube([8,43,43],center=true);
        translate([965,0,motor_z]) cube([10,23,23],center=true);
      }
      for(x=[925,949]){
        translate([x,0,r_body(x)+6.3]) cube([13,25,3],center=true);
        for(s=[-1,1]) hull(){
          translate([x,s*9.7,r_body(x)+7.4]) cube([10,4.6,4],center=true);
          translate([964,s*16,motor_z+(x==925?15:-15)]) cube([8,5,8],center=true);
        }
      }
    }
    for(x=[925,949],y=[-8,8]) translate([x,y,r_body(x)+8])
      cylinder(d=M3_CLEAR,h=11,center=true);
    for(y=[-16,16],z=[-16,16]) translate([962,y,motor_z+z]) along_x()
      cylinder(d=M3_CLEAR,h=28,center=true);
  }
}
module motor_collar(x,upper){
  if(!upper) difference(){
    union(){
      collar_half(x,13,false);
      translate([x,0,-r_body(x)-1.8]) cube([13,19,5.6],center=true);
    }
    hull_body(-.35);
    translate([x,0,-25]) cylinder(d=M3_CLEAR,h=32,center=true);
  }
  else difference(){
    union(){
      collar_half(x,13);
      translate([x,0,r_body(x)+1.8]) cube([13,26,5.6],center=true);
    }
    hull_body(-.35);
    for(x=[925,949]) motor_collar(x,false);
    for(y=[-8,8]) translate([x,y,23]) cylinder(d=M3_CLEAR,h=27,center=true);
  }
}
module motor_firewall(){
  difference(){
    translate([motor_x+2,0,motor_z]) cube([4,43,43],center=true);
    translate([motor_x+2,0,motor_z]) along_x() cylinder(d=9,h=8,center=true);
    for(y=[-16,16],z=[-16,16])
      translate([motor_x+2,y,motor_z+z]) along_x() cylinder(d=M3_CLEAR,h=8,center=true);
  }
}
module prop_disk(clear=0){
  translate([prop_x-5,0,motor_z]) along_x()
    cylinder(d=prop_d+2*clear,h=12+2*clear,center=true,$fn=96);
}
module motor_envelope(){
  translate([990,0,motor_z]) along_x() cylinder(d=27.7,h=34,center=true);
}
module lower_rear_skid(){
  difference(){
    hull(){
      for(x=[925,949]) translate([x,0,-r_body(x)-1]) cube([13,19,4],center=true);
      translate([938,0,-37]) cube([35,12,6],center=true);
    }
    hull_body(-.35);
    for(x=[925,949]) translate([x,0,-26]) cylinder(d=M3_CLEAR,h=36,center=true);
  }
}

module shell(i){
 x0=body_cuts[i];x1=body_cuts[i+1];
 difference(){
  intersection(){difference(){hull_body();hull_body(wall);}clip_x(x0,x1);}
  // real radial shell screw clearance. Two radial holes each adjacent seam.
  if(i>0) hole_y(body_cuts[i]+9,0,0,M3_CLEAR,110);
  if(i<len(body_cuts)-2) hole_y(body_cuts[i+1]-9,0,0,M3_CLEAR,110);
  cooling_window(i);
  if(i==1) tray_shell_holes();

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
 if(s<0){ mirror([0,1,0]) wing_loft(1,from_y,to_y,a,b,t); }   // V6: build +side, mirror (robust)
 else {
  pts=outline(.02,.4,t,a,b);
  loft([for(p=pts) wing_point(p,from_y/b2,s)],
       [for(p=pts) wing_point(p,to_y/b2,s)]);
 }
}
module wing_web_half(from_y,to_y,q,width){
 // Solid vertical webs joining upper/lower wing skins, positive-y half only.
 function dummy()=0;
 pts0=[for(xx=[q-width/2,q+width/2],sign=[-1,1]) naca_pt(xx,sign,.02,.4,.12)];
 f0=from_y/b2; f1=to_y/b2;
 function xpoint(f,q)=LE(f)+q*chord(f);
 function zpoint(f,q,sgn)=lerp(root_z,tip_z,f)+naca_pt(q,sgn,.02,.4,.12)[1]*chord(f);
 polyhedron(points=[
  [xpoint(f0,q-width/2),from_y,zpoint(f0,q,-1)],
  [xpoint(f0,q+width/2),from_y,zpoint(f0,q,-1)],
  [xpoint(f0,q+width/2),from_y,zpoint(f0,q,1)],
  [xpoint(f0,q-width/2),from_y,zpoint(f0,q,1)],
  [xpoint(f1,q-width/2),to_y,zpoint(f1,q,-1)],
  [xpoint(f1,q+width/2),to_y,zpoint(f1,q,-1)],
  [xpoint(f1,q+width/2),to_y,zpoint(f1,q,1)],
  [xpoint(f1,q-width/2),to_y,zpoint(f1,q,1)]],
  faces=[[3,2,1,0],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]);
}
module wing_web(s,from_y,to_y,q,width){
 if(s<0){ mirror([0,1,0]) wing_web_half(from_y,to_y,q,width); }
 else { wing_web_half(from_y,to_y,q,width); }
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
 // PETG center section with spar splice seats and wingsaddle attachment.
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
  for(q=[.28,.63]) wing_splice_pocket(q);
  for(xx=[346+wing_shift,465+wing_shift],yy=[-20,20])
   translate([xx,yy,58]) cylinder(d=M4_CLEAR,h=50,center=true);
 }
}

module PETG_wing_key(){
 // Key at each wing segment boundary. Install two M3 x 5.7 inserts from top.
 difference(){
   cube(key_nominal,center=true);
   translate([0,0,0]) cube([7,11,key_nominal[2]+2],center=true); // V6 lightening slot
   for(yy=[-10,10])
     translate([0,yy,5-M3_INSERT_DEPTH/2+.02])
       cylinder(d=M3_PILOT,h=M3_INSERT_DEPTH,center=true);
 }
}
module tail_loft(s,f0,f1,a=0,b=1,tc=.10){
 if(s<0){ mirror([0,1,0]) tail_loft(1,f0,f1,a,b,tc); }
 else {
  pts=outline(0,.4,tc,a,b);
  loft([for(p=pts) tail_pt(p,f0,s)], [for(p=pts) tail_pt(p,f1,s)]);
 }
}
function hinge_fractions()=[.14,.50,.86];
function hinge_pt(f,s)=tail_pt([.758,0],f,s);
module tail_local(f,s){
  p=hinge_pt(f,1);
  sweep=atan((hinge_pt(0,1)[0]-hinge_pt(1,1)[0])/tail_span);
  if(s>0) translate(p) rotate([tail_dih,0,0]) rotate([0,0,sweep]) children();
  else mirror([0,1,0]) translate(p) rotate([tail_dih,0,0]) rotate([0,0,sweep]) children();
}
module tail_hinge_features(s,moving,pockets=false){
  for(f=hinge_fractions()) tail_local(f,s) {
    if(pockets)
      translate([moving?8:-8,0,0]) cube([16,12.4,1.5],center=true);
    else
      translate([moving?7:-7,0,0]) cube([15,26,5],center=true);
  }
}
module tail_root_tab(s){
  for(x=[807,853]) hull(){
    translate([x,s*24,25.9]) cube([15,13,5],center=true);
    translate([x,s*25,41]) cube([15,9,6],center=true);
  }
}
module tail_root_holes(){
  for(x=[807,853],y=[-24,24])
    translate([x,y,32]) cylinder(d=M3_CLEAR,h=40,center=true);
}
module tail_fixed(s){
  difference(){
    union(){
      difference(){
        tail_loft(s,0,1,0,.75,.10);
        tail_loft(s,.02,.98,.04,.725,.10*.88);
      }
      intersection(){ tail_loft(s,0,1,0,.75,.10); tail_hinge_features(s,false); }
      tail_root_tab(s);
    }
    tail_hinge_features(s,false,true);
    tail_root_holes();
  }
}
function horn_f()=.25;
module horn_holes(s){
  tail_local(horn_f(),s) for(x=[12,20])
    translate([x,0,0]) cylinder(d=2.2,h=24,center=true);
}
module ruddervator(s){
  difference(){
    union(){
      difference(){
        tail_loft(s,0,1,.766,1,.10);
        tail_loft(s,.025,.975,.782,.968,.10*.88);
      }
      intersection(){
        tail_loft(s,0,1,.766,1,.10);
        union(){
          tail_hinge_features(s,true);
          tail_local(horn_f(),s) translate([17,0,0]) cube([16,12,14],center=true);
        }
      }
    }
    tail_hinge_features(s,true,true);
    horn_holes(s);
  }
}
module control_horn(s){
  difference(){
    tail_local(horn_f(),s) union(){
      translate([16,0,-6.6]) cube([16,11,3],center=true);
      hull(){
        translate([13,0,-7]) cube([6,5,2],center=true);
        translate([3,0,-15]) rotate([90,0,0]) cylinder(d=8,h=5,center=true);
      }
    }
    horn_holes(s);
    tail_local(horn_f(),s) translate([3,0,-15]) rotate([90,0,0])
      cylinder(d=2,h=8,center=true);
  }
}
module move_ruddervator(s,deg){
  a=hinge_pt(0,s); axis=sub(hinge_pt(1,s),a);
  translate(a) rotate(a=s*deg,v=axis) translate(-a) children();
}
module tail_collar(x,upper){
  if(!upper) collar_half(x,13,false);
  else difference(){
    union(){
      collar_half(x,13);
      for(y=[-24,24]) hull(){
        translate([x,y*.71,r_body(x)-6]) cube([13,12,4],center=true);
        translate([x,y,20.2]) cube([13,13,6],center=true);
      }
      translate([x,0,r_body(x)+2.2]) cube([13,17,5],center=true);
    }
    hull_body(-.35);
    for(s=[-1,1]) translate([0,0,-.15]) tail_fixed(s);
    tail_root_holes();
    translate([x,0,39]) cylinder(d=M3_CLEAR,h=37,center=true);
  }
}
module dorsal_fin(){
  difference(){
    union(){
      hull(){
        translate([788,-1.5,33]) cube([125,3,3],center=false);
        translate([822,-1.25,107]) cube([65,2.5,3],center=false);
      }
      for(x=[807,853]) hull(){
        translate([x,0,r_body(x)+6.3]) cube([12,15,3],center=true);
        translate([x,0,47]) cube([12,3,3],center=true);
      }
    }
    for(x=[807,853]) translate([x,0,31])
      cylinder(d=M3_CLEAR,h=13,center=true);
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
module reference_model(){
  for(i=[0:len(body_cuts)-2]) color("ivory") shell(i);
  for(i=[0:len(body_cuts)-3]) color("slategray") PETG_coupler(i);
  color("ivory") wing_center();
  for(s=[-1,1],i=[0:2]) color("ivory") wing_panel(s,i);
  for(s=[-1,1],y=[44,246,448])
    translate([LE(y/b2)+.52*chord(y/b2),s*y,wing_Z(y/b2,.52)]) color("slategray") PETG_wing_key();
  if(show_structural_rods) for(q=[.28,.63]){
    color("slategray") wing_splice(q);
    for(s=[-1,1]) color("black") wing_spar(s,7,620,q,spar_od(q));
  }
  for(x=[532,651],top=[false,true]) color("slategray") wing_collar(x,top);
  for(x=[807,853],top=[false,true]) color("slategray") tail_collar(x,top);
  for(s=[-1,1]){
    color("ivory") tail_fixed(s);
    move_ruddervator(s,ruddervator_deg){
      color("lightblue") ruddervator(s);
      color("slategray") control_horn(s);
    }
    color("slategray") servo_plate(s);
    if($preview) color("black") {
      servo_envelope(s);
      linkage_preview(s);
    }
  }
  color("slategray") battery_tray();
  for(x=[120,303],s=[-1,1]) color("slategray") battery_hatch_tab(x,s);
  if(show_preview_battery) color([.22,.48,.78,.55]) battery_envelope();
  color("ivory") battery_hatch_lid();
  color("slategray") camera_cradle();
  if(show_dorsal_fin) color("lightblue") dorsal_fin();
  for(x=[925,949],top=[false,true]) color("slategray") motor_collar(x,top);
  color("slategray") motor_pylon();
  color("slategray") lower_rear_skid();
  color("silver") motor_firewall();
  color("black") motor_envelope();
  if($preview) color([.2,.3,.4,.25]) prop_disk();
}

if(part=="assembly") reference_model();
else if(part=="wing_center") wing_center();
else if(part=="wing_key") PETG_wing_key();
else if(part=="splice_main") wing_splice(.28);
else if(part=="splice_aft") wing_splice(.63);
else if(part=="battery_tray") battery_tray();
else if(part=="battery_hatch_lid") battery_hatch_lid();
else if(part=="hatch_tab_front") battery_hatch_tab(120,1);
else if(part=="hatch_tab_aft") battery_hatch_tab(303,1);
else if(part=="camera_cradle") camera_cradle();
else if(part=="motor_pylon") motor_pylon();
else if(part=="motor_firewall") motor_firewall();
else if(part=="rear_skid") lower_rear_skid();
else if(part=="dorsal_fin") dorsal_fin();
else if(part=="insert_fit_coupon") insert_fit_coupon();
else {
  for(i=[0:len(body_cuts)-2]){
    if(part==str("fuselage_",i)) shell(i);
    if(i<len(body_cuts)-2 && part==str("coupler_",i)) PETG_coupler(i);
  }
  for(s=[-1,1]){
    name=s>0?"R":"L";
    for(i=[0:2]) if(part==str("wing_",name,i+1)) wing_panel(s,i);
    if(part==str("tail_",name)) tail_fixed(s);
    if(part==str("ruddervator_",name)) ruddervator(s);
    if(part==str("control_horn_",name)) control_horn(s);
    if(part==str("servo_plate_",name)) servo_plate(s);
  }
  for(top=[false,true]){
    label=top?"upper":"lower";
    for(x=[532,651]) if(part==str("wing_collar_",x,"_",label)) wing_collar(x,top);
    for(x=[807,853]) if(part==str("tail_collar_",x,"_",label)) tail_collar(x,top);
    for(x=[925,949]) if(part==str("motor_collar_",x,"_",label)) motor_collar(x,top);
  }
}
