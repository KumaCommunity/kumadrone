#!/usr/bin/env python3
"""
Generate review-ready technical graphics from verified geometry/parameters.
CAD/parameter-derived schematics, NOT artistic renders.
"""
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GDIR = os.path.join(HERE, "..", "graphics")
DATADIR = os.path.join(HERE, "..", "data")

LE_MAC = 507.43
MAC = 176.19
X_AC_WING = 551.48
X_AC_TAIL = 820.11
X_NP = 573.81
X_CG_EMPTY = 560.02
X_CG_LOADED = 558.91


def load_mass():
    rows = []
    with open(os.path.join(ROOT, "mass_budget.csv")) as fh:
        for r in csv.DictReader(fh):
            rows.append((r["item"], r["category"], float(r["total_mass_g"]), float(r["x_mm"])))
    return rows


def mass_cg_diagram():
    rows = load_mass()
    fig, ax = plt.subplots(figsize=(13, 5.2))
    cats = {"LW-PLA": "#c8b98f", "PETG": "#4a6fa5", "Unselected equipment": "#8a8a8a"}
    for item, cat, m, x in rows:
        ax.scatter(x, m, s=m * 3.0, color=cats.get(cat, "#999"),
                   edgecolor="k", linewidth=0.4, alpha=0.85, zorder=3)
        if m >= 12:
            ax.annotate(item, (x, m), fontsize=6.5, xytext=(0, 5),
                        textcoords="offset points", ha="center")
    for xv, lab, c, ls in [
        (X_CG_EMPTY, "CG empty 560.0", "#d62728", "-"),
        (X_CG_LOADED, "CG +500g 558.9", "#ff7f0e", "--"),
        (X_AC_WING, "Wing AC 551.5", "#2ca02c", ":"),
        (X_NP, "Neutral pt 573.8", "#9467bd", "-."),
        (LE_MAC + 0.28 * MAC, "28% MAC 556.8", "#17becf", ":"),
    ]:
        ax.axvline(xv, color=c, ls=ls, lw=1.3, label=lab)
    ax.set_xlabel("Station x from nose (mm)")
    ax.set_ylabel("Component mass (g)  [bubble size prop. to mass]")
    ax.set_title("Kuma V5 Config B - component mass distribution and CG/stability references\n"
                 "(printed masses = CAD-volume x assumed density; purchased masses estimated)",
                 fontsize=10)
    ax.set_xlim(-20, 1030)
    ax.legend(loc="upper left", fontsize=7.5, framealpha=0.9)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(GDIR, "mass_cg_diagram.png"), dpi=150)
    plt.close(fig)


def planform():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    for sgn in (1, -1):
        xs = [496, 520, 520 + 150, 496 + 200, 496]
        ys = [0, sgn * 650, sgn * 650, 0, 0]
        ax1.plot(xs, ys, color="#b08d57", lw=2)
        ax1.fill(xs, ys, color="#e8dcc0", alpha=0.5)
        xs = [770, 788, 788 + 140, 770 + 190, 770]
        ys = [sgn * 12, sgn * 196, sgn * 196, sgn * 12, sgn * 12]
        ax1.plot(xs, ys, color="#2f4f4f", lw=1.8)
        ax1.fill(xs, ys, color="#9fc3c3", alpha=0.5)
    ax1.plot([0, 970], [0, 0], color="k", lw=6, alpha=0.4)
    ax1.axvline(496, color="orange", ls="--", lw=1, label="root LE 496")
    ax1.axvline(556.76, color="red", ls=":", lw=1.2, label="28% MAC 556.8")
    ax1.set_aspect("equal")
    ax1.set_xlabel("x (mm)")
    ax1.set_ylabel("y (mm)")
    ax1.set_title("Planform (top) - wing 1300 span, 200->150 chord; V-tail projected")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.25)
    ax2.plot([0, 970], [0, 0], color="k", lw=6, alpha=0.4)
    ax2.plot([496, 520], [56, 56], color="#b08d57", lw=2)
    ax2.plot([696, 520], [56 + 79.8, 56], color="#b08d57", lw=2, ls="--")
    ax2.annotate("dihedral 7 deg / tip rise 79.8 mm", (560, 100), fontsize=8)
    ax2.plot([770, 788], [26, 26], color="#2f4f4f", lw=2)
    ax2.plot([788, 788], [26, 180.3], color="#2f4f4f", lw=2)
    ax2.plot([993, 993], [-10, 140], color="gray", lw=4, alpha=0.5)
    ax2.annotate("prop 150 mm", (998, 50), fontsize=8)
    ax2.set_aspect("equal")
    ax2.set_ylim(-60, 220)
    ax2.set_xlim(-20, 1050)
    ax2.set_xlabel("x (mm)")
    ax2.set_ylabel("z (mm)")
    ax2.set_title("Side schematic - dihedral, V-tail height, prop clearance")
    ax2.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(GDIR, "geometry_planform.png"), dpi=150)
    plt.close(fig)



def launch_stall():
    RHO, G, S = 1.225, 9.80665, 0.2275
    masses = [1.3079, 1.4079, 1.5579, 1.8079]
    labels = ["empty", "100 g", "250 g", "500 g"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    for cl in [0.9, 1.0, 1.1, 1.2]:
        vs = [math.sqrt(2 * m * G / (RHO * S * cl)) for m in masses]
        ax1.plot(labels, vs, "o-", label=f"CLmax={cl}")
    ax1.set_ylabel("Stall speed (m/s)")
    ax1.set_title("Stall speed vs equipment load")
    ax1.axhspan(6, 9, color="green", alpha=0.12, label="comfortable hand launch")
    ax1.axhspan(9, 12, color="orange", alpha=0.12, label="marginal")
    ax1.axhspan(12, 16, color="red", alpha=0.12, label="not hand-launchable")
    ax1.legend(fontsize=7.5)
    ax1.grid(True, alpha=0.25)
    wl = [m / S for m in masses]
    ax2.bar(labels, wl, color=["#2ca02c", "#bcbd22", "#ff7f0e", "#d62728"])
    ax2.axhline(4.5, color="green", ls="--", label="typical hand-launch ceiling ~4.5 kg/m2")
    ax2.set_ylabel("Wing loading (kg/m2)")
    ax2.set_title("Wing loading vs equipment load")
    for i, v in enumerate(wl):
        ax2.text(i, v + 0.1, f"{v:.1f}", ha="center", fontsize=9)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.25, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(GDIR, "launch_and_stall.png"), dpi=150)
    plt.close(fig)


def static_margin():
    rows = []
    with open(os.path.join(DATADIR, "stability.csv")) as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    fig, ax = plt.subplots(figsize=(8, 5))
    deps_vals = sorted(set(float(r["deps"]) for r in rows))
    for scale in ["0.7", "0.85", "1.0"]:
        xnp = [float(r["x_np_mm"]) for r in rows if r["a_t_scale"] == scale]
        ax.plot(deps_vals, xnp, "o-", label=f"a_t x {scale}")
    ax.axhline(X_CG_EMPTY, color="#d62728", ls="--", lw=1.5, label="CG empty 560.0")
    ax.axhline(X_CG_LOADED, color="#ff7f0e", ls=":", lw=1.5, label="CG +500g 558.9")
    ax.set_xlabel("Downwash gradient d(eps)/d(alpha)")
    ax.set_ylabel("Neutral point x (mm)")
    ax.set_title("Neutral-point sensitivity - all cases aft of CG (SM > 0),\n"
                 "margin thin at low tail effectiveness")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(GDIR, "static_margin_sensitivity.png"), dpi=150)
    plt.close(fig)


def main():
    os.makedirs(GDIR, exist_ok=True)
    mass_cg_diagram()
    planform()
    launch_stall()
    static_margin()
    print("Wrote graphics to", os.path.abspath(GDIR))


if __name__ == "__main__":
    main()
