from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh


def generate_thumbnail(model_path: Path, thumb_path: Path, color: str = '#888888') -> None:
    mesh = trimesh.load(model_path, force='mesh')
    fig = plt.figure(figsize=(2.56, 2.56), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    collection = Poly3DCollection(mesh.triangles, facecolor=color, edgecolor='k', linewidths=0.1)
    ax.add_collection3d(collection)
    ax.view_init(elev=0, azim=90)
    ax.axis('off')
    max_range = max(mesh.extents)
    mid = mesh.bounds.mean(axis=0)
    ax.set_xlim(mid[0] - max_range/2, mid[0] + max_range/2)
    ax.set_ylim(mid[1] - max_range/2, mid[1] + max_range/2)
    ax.set_zlim(mid[2] - max_range/2, mid[2] + max_range/2)
    fig.savefig(thumb_path, dpi=100, transparent=True)
    plt.close(fig)
