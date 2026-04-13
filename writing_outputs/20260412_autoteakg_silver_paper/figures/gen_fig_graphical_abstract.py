from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUT_DIR = Path(__file__).resolve().parent


def add_box(ax, xy, width, height, title, body, color):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        linewidth=1.0,
        edgecolor="#2C3E50",
        facecolor=color,
    )
    ax.add_patch(box)
    x, y = xy
    ax.text(x + width / 2, y + height * 0.66, title, ha="center", va="center", fontsize=10.5, weight="bold", color="#203040")
    ax.text(x + width / 2, y + height * 0.36, body, ha="center", va="center", fontsize=8.2, color="#203040", linespacing=1.25)


def add_arrow(ax, start, end):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.4,
        color="#5F6C72",
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(arrow)


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, ax = plt.subplots(figsize=(9.4, 3.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    colors = ["#E8EDF2", "#E8F2EE", "#FFF4DE", "#FDE8E1", "#EAF0FF"]
    boxes = [
        ((0.035, 0.42), 0.16, 0.34, "PubMed corpus", "2022-2026 tea\nactivity literature", colors[0]),
        ((0.235, 0.42), 0.16, 0.34, "Auto extraction", "GLM5 + rules\nschema validation", colors[1]),
        ((0.435, 0.42), 0.16, 0.34, "Context recovery", "abstract + PMC\nmethods sections", colors[2]),
        ((0.635, 0.42), 0.16, 0.34, "Silver KG v3", "635 records\n1,989 nodes\n8,195 edges", colors[3]),
        ((0.835, 0.42), 0.13, 0.34, "Queries", "evidence maps\nuncertainty\nmicrobiome paths", colors[4]),
    ]
    for xy, w, h, title, body, color in boxes:
        add_box(ax, xy, w, h, title, body, color)

    arrow_y = 0.59
    add_arrow(ax, (0.198, arrow_y), (0.232, arrow_y))
    add_arrow(ax, (0.398, arrow_y), (0.432, arrow_y))
    add_arrow(ax, (0.598, arrow_y), (0.632, arrow_y))
    add_arrow(ax, (0.798, arrow_y), (0.832, arrow_y))

    ax.text(
        0.5,
        0.18,
        "Every graph edge preserves PMID provenance, evidence level, confidence, and uncertainty flags.",
        ha="center",
        va="center",
        fontsize=9,
        color="#2C3E50",
    )
    ax.text(
        0.5,
        0.93,
        "AutoTeaKG-Silver: automated tea functional activity evidence graph",
        ha="center",
        va="center",
        fontsize=13,
        weight="bold",
        color="#203040",
    )
    fig.savefig(OUT_DIR / "fig_graphical_abstract.pdf", bbox_inches="tight")
    fig.savefig(OUT_DIR / "fig_graphical_abstract.png", bbox_inches="tight", dpi=300)
    fig.savefig(OUT_DIR / "fig_graphical_abstract.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
