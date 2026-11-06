"""Draw the actual tree structures after inserting the same ten sorted keys."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from compare_trees import build_trees


def draw_tree(axis, tree, title, red_black=False):
    positions, nodes = {}, {}
    edges = []

    def visit(node, depth=0):
        if node is None or getattr(node, "_is_nil", False):
            return
        left, right = node.get_left(), node.get_right()
        visit(left, depth + 1)
        positions[node.key] = (len(positions), -depth)
        nodes[node.key] = node
        visit(right, depth + 1)
        for child in (left, right):
            if child is not None and not getattr(child, "_is_nil", False):
                edges.append((node.key, child.key))

    visit(tree.root)
    for source, target in edges:
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        axis.plot([x1, x2], [y1, y2], color="#aab6c2", linewidth=1.8, zorder=1)
    for key, (x, y) in positions.items():
        colour = "#b94343" if red_black and nodes[key].is_red() else "#25394b"
        axis.scatter(x, y, s=600, color=colour, zorder=2)
        axis.text(x, y, str(key), ha="center", va="center", color="white", fontsize=10)
    axis.set_title(f"{title}\n{tree.count_nodes_tree()} nodes · height {tree.height()}",
                   fontsize=13, fontweight="bold", pad=15)
    axis.set_xlim(-0.8, 9.8)
    axis.set_ylim(-9.6, 0.8)
    axis.set_axis_off()
    print(f"{title}: {tree.count_nodes_tree()} nodes, height {tree.height()}")


def main():
    bst, rbt = build_trees(list(range(1, 11)))
    figure, axes = plt.subplots(1, 2, figsize=(11, 6.5), layout="constrained")
    draw_tree(axes[0], bst, "Binary search tree")
    draw_tree(axes[1], rbt, "Red-black tree", red_black=True)
    figure.suptitle("Sorted insertion: keys 1–10", fontsize=17, fontweight="bold")
    figure.supxlabel(
        "Actual nodes and colours from the project · shared depth scale · NIL leaves omitted",
        fontsize=10,
    )
    axes[1].legend(handles=[Patch(color="#25394b", label="Black node"),
                            Patch(color="#b94343", label="Red node")],
                   loc="lower center", frameon=False)
    output = Path(__file__).parent / "docs/images/tree-comparison.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=140, facecolor="white", bbox_inches="tight")
    plt.close(figure)
    print(f"Saved {output.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()

