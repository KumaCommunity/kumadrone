#!/usr/bin/env python3
"""
Orthographic views (front/side/top/rear) rendered from the exported V6 STLs.
Deterministic (no GUI camera). Usage: python3 plot_ortho.py <view>
  view in {front,side,top,rear}; builds a triangle cache on first run.
"""
import os
import sys
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import trimesh

HERE = os.path.dirname(__file__)
STLDIR = os.path.join(HERE, "..", "STL")
GDIR = os.path.join(HERE, "..", "graphics")
CACHE = "/tmp/v6_tris.npz"
EXCLUDE = {"forward_equipment_tray", "insert_fit_coupon", "camera_plate", "dorsal_fairing"}
LW = np.array([0.85, 0.80, 0.60])
PETG = np.array([0.34, 0.46, 0.60])
OTHER = np.array([0.6, 0.6, 0.6])
PETG_PARTS = {"coupler_0", "coupler_1", "coupler_2", "coupler_3", "coupler_4", "wing_key",
              "tail_saddle", "tail_shoe_R", "tail_shoe_L", "saddle_plate", "camera_cradle",
              "secured_tray", "motor_bulkhead", "centre_spar_joiner",
              "wing_center_spar_sleeve", "control_horn_R", "control_horn_L",
              "ruddervator_hinge_R", "ruddervator_hinge_L"}


def build_cache():
    tris = []
    mats = []
    for f in sorted(glob.glob(os.path.join(STLDIR, "*.stl"))):
        name = os.path.splitext(os.path.basename(f))[0]
        if name in EXCLUDE:
            continue
        m = trimesh.load(f, force="mesh")
        t = np.asarray(m.triangles, float)
        if len(t) == 0:
            continue
        tris.append(t)
        mat = 1 if name in PETG_PARTS else 0
        mats.append(np.full(len(t), mat))
    T = np.concatenate(tris)
    M = np.concatenate(mats)
    np.savez_compressed(CACHE, tris=T.astype(np.float32), mats=M.astype(np.int8))


VIEWS = {
    "top":   (np.array([0, 0, 1.0]), np.array([1.0, 0, 0]), np.array([0, 1.0, 0])),
    "side":  (np.array([0, 1.0, 0]), np.array([1.0, 0, 0]), np.array([0, 0, 1.0])),
    "front": (np.array([-1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])),
    "rear":  (np.array([1.0, 0, 0]), np.array([0, -1.0, 0]), np.array([0, 0, 1.0])),
}


def render(view):
    d = np.load(CACHE)
    T = d["tris"].astype(float)      # (N,3,3)
    M = d["mats"]
    e, u, v = VIEWS[view]
    e = e / np.linalg.norm(e)
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    nl = np.linalg.norm(n, axis=1)
    nl[nl == 0] = 1
    n = n / nl[:, None]
    facing = n @ e
    keep = facing > 0.02
    T = T[keep]; M = M[keep]; n = n[keep]; facing = facing[keep]
    # project
    P = np.einsum("nij,j->ni", T, u)     # u-coord of 3 verts
    Q = np.einsum("nij,j->ni", T, v)
    verts2 = np.stack([P, Q], axis=2)    # (N,3,2)
    cent = T.mean(axis=1)
    depth = cent @ e
    order = np.argsort(depth)            # far first
    verts2 = verts2[order]; M = M[order]; facing = facing[order]
    shade = 0.40 + 0.60 * np.clip(facing, 0, 1)
    base = np.where(M[:, None] == 1, PETG[None, :], LW[None, :])
    colors = np.clip(base * shade[:, None], 0, 1)
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.add_collection(PolyCollection(verts2, facecolors=colors, edgecolors="none"))
    ax.autoscale(); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"Kuma V6 Config B - {view.upper()} view (lightened, orthographic)")
    fig.tight_layout()
    os.makedirs(GDIR, exist_ok=True)
    fig.savefig(os.path.join(GDIR, f"v6_{view}.png"), dpi=150)
    plt.close(fig)
    print("wrote", os.path.join(GDIR, f"v6_{view}.png"))


if __name__ == "__main__":
    if not os.path.exists(CACHE):
        build_cache()
    render(sys.argv[1] if len(sys.argv) > 1 else "top")
