"""Estimate no-extra-equipment mass and CG using exported STL centroids and BOM stations."""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
PACK_RANGE = (180, 190, 242)
MAC_MM = 176.19
MAC_LE_MM = 507.43
WING_AREA_M2 = .2275

with (DATA / "mesh_verification.csv").open(newline="") as source:
    parts = list(csv.DictReader(source))
with (DATA / "installed_hardware.csv").open(newline="") as source:
    hardware = list(csv.DictReader(source))

part_mass = sum(float(part["estimated_total_g"]) for part in parts)
part_moment = sum(float(part["estimated_total_g"]) * float(part["x_centroid_mm"]) for part in parts)
installed_mass = sum(float(part["mass_g"]) for part in hardware)
installed_moment = sum(float(part["mass_g"]) * float(part["x_mm"]) for part in hardware)
pack = next(part for part in hardware if part["item"].startswith("Gens ace"))
total_mass = part_mass + installed_mass
results = []
for position in PACK_RANGE:
    moment = part_moment + installed_moment + float(pack["mass_g"]) * (position - float(pack["x_mm"]))
    cg = moment / total_mass
    results.append({"battery_x_mm": position, "estimated_mass_g": round(total_mass, 1),
                    "estimated_cg_mm": round(cg, 2), "estimated_cg_pct_mac": round(100*(cg-MAC_LE_MM)/MAC_MM, 2),
                    "wing_loading_g_dm2": round(total_mass/(100*WING_AREA_M2), 2),
                    "stall_screen_m_s_clmax_1": round(math.sqrt(2*(total_mass/1000)*9.80665/(1.225*WING_AREA_M2)), 2)})
print(f"Mesh-derived parts: {part_mass:.1f} g | listed hardware: {installed_mass:.1f} g")
for row in results:
    print(row)
with (DATA / "mass_balance.csv").open("w", newline="") as output:
    writer = csv.DictWriter(output, fieldnames=results[0])
    writer.writeheader()
    writer.writerows(results)
