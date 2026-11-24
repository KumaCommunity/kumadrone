"""Fresh OpenSCAD export and geometric checks for the Kuma V6.2 prototype."""
import argparse
import csv
import shlex
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import trimesh

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Kuma_FPV_V6_2_Configuration_B.scad"
BODY = [f"fuselage_{i}" for i in range(6)]
WING = [f"wing_{side}{i}" for side in "RL" for i in range(1, 4)]
TAIL = [f"{name}_{side}" for name in ("tail", "ruddervator") for side in "RL"]
PAIRED = [f"{name}_{side}" for name in ("control_horn", "servo_plate") for side in "RL"]
COLLARS = [f"{name}_collar_{station}_{half}"
           for name, stations in (("wing", (532, 651)), ("tail", (807, 853)), ("motor", (925, 949)))
           for station in stations for half in ("upper", "lower")]
EXTRAS = ["wing_center", "wing_key", "splice_main", "splice_aft", "battery_tray",
          "battery_hatch_lid", "hatch_tab_front", "hatch_tab_aft", "camera_cradle",
          "motor_pylon", "motor_firewall", "rear_skid", "dorsal_fin", "insert_fit_coupon"]
PARTS = BODY + [f"coupler_{i}" for i in range(5)] + WING + TAIL + PAIRED + COLLARS + EXTRAS
QUANTITY = {"wing_key": 6, "hatch_tab_front": 2, "hatch_tab_aft": 2,
            "dorsal_fin": 0, "insert_fit_coupon": 0}
LIGHT = set(BODY + WING + TAIL + ["battery_hatch_lid", "dorsal_fin"])
ALUMINUM = {"motor_firewall", "splice_main", "splice_aft"}
PROBES = [
    ("battery_access_forward", 0, False), ("battery_access_aft", 0, False),
    ("battery_tray_pack", 0, False), ("hatch_lid_shell", 0, False),
    ("cooling_inlet", 0, True), ("cooling_exit", 0, True), ("servo_access", 0, True),
    ("motor_wire_exit", 0, True),
    ("servo_case_fit", 0, False), ("linkage_wall", 0, False), ("spar_socket", 0, False),
    ("spar_tube", 0, False), ("wing_collar_clearance", 0, False),
    ("tail_mount", 0, False), ("horn_motion", -20, False), ("horn_motion", 20, False),
    ("prop_clearance", 0, False), ("motor_mount", 0, False),
]


def run_scad(command, source, destination, definitions):
    args = command + ["--backend=Manifold", "--export-format=binstl", "-o", str(destination)]
    for definition in definitions:
        args.extend(["-D", definition])
    return subprocess.run(args + [str(source)], capture_output=True, text=True, check=False)


def export_part(command, part, output_root):
    destination = output_root / "STL" / f"{part}.stl"
    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "part.stl"
        run = run_scad(command, SOURCE, output, [f'part="{part}"'])
        if run.returncode or "NoError" not in run.stderr or "WARNING:" in run.stderr:
            raise RuntimeError(f"{part} did not export cleanly\n{run.stdout}{run.stderr}")
        mesh = trimesh.load(output, force="mesh")
        solids = sum(piece.volume > 0.01 for piece in mesh.split(only_watertight=False))
        fits = all(mesh.extents <= [220, 220, 250])
        material, density = ("6061 reference", 2.7) if part in ALUMINUM else (
            ("LW-PLA", .35) if part in LIGHT else ("PETG", 1.27))
        quantity = QUANTITY.get(part, 1)
        volume = mesh.volume / 1000
        row = {"part": part, "watertight": mesh.is_watertight, "solid_components": solids,
               "fits_220x220x250": fits, "material": material, "qty": quantity,
               "volume_cm3": round(volume, 4), "x_centroid_mm": round(mesh.center_mass[0], 3),
               "estimated_total_g": round(volume * density * quantity, 2)}
        destination.write_bytes(output.read_bytes())
        return row


def check_probe(command, probe):
    name, angle, expect_cut = probe
    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "probe.stl"
        run = run_scad(command, ROOT / "scripts/fit_checks.scad", output,
                       ['part="audit"', f'probe="{name}"', f"ruddervator_deg={angle}"])
        if output.exists() and run.returncode == 0:
            volume = abs(trimesh.load(output, force="mesh").volume)
        elif "top level object is empty" in run.stderr.lower():
            volume = 0
        else:
            raise RuntimeError(f"{name} failed to evaluate\n{run.stdout}{run.stderr}")
    return {"check": name, "angle_deg": angle, "intersection_mm3": round(volume, 4),
            "pass": volume > 1 if expect_cut else volume < 0.1}


def write_csv(output_root, name, rows):
    with (output_root / "data" / name).open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openscad", default="openscad", help="OpenSCAD command and optional prefix")
    parser.add_argument("--output", type=Path, default=ROOT, help="Directory for STL and data outputs")
    args = parser.parse_args()
    command = shlex.split(args.openscad)
    (args.output / "STL").mkdir(parents=True, exist_ok=True)
    (args.output / "data").mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda part: export_part(command, part, args.output), PARTS))
        probes = list(executor.map(lambda probe: check_probe(command, probe), PROBES))
    write_csv(args.output, "mesh_verification.csv", results)
    write_csv(args.output, "fit_verification.csv", probes)
    bad = [row["part"] for row in results if not (
        row["watertight"] and row["solid_components"] == 1 and row["fits_220x220x250"])]
    print(f"{len(results)-len(bad)}/{len(results)} parts watertight, single-solid and within bed bounds")
    print("Mesh exceptions:", ", ".join(bad) or "none")
    for row in probes:
        print(f'{row["check"]:24} {row["angle_deg"]:3} deg {row["intersection_mm3"]:10.4f} mm³ '
              f'{"PASS" if row["pass"] else "FAIL"}')
    return int(bool(bad) or any(not row["pass"] for row in probes))


if __name__ == "__main__":
    raise SystemExit(main())
