"""Focused checks for deletion, parent links, ordering and colour invariants."""

from contextlib import redirect_stdout
from io import StringIO
from itertools import permutations
from pathlib import Path
import random
import tempfile
import unittest

import binary_tree
from binary_tree import BinaryTree
import red_black_tree
from red_black_tree import RedBlackTree
from compare_trees import build_trees, load_words_by_letter


def validate(tree, expected):
    """Check ordering, parents and membership, then red-black properties."""
    sentinel = tree.NIL if isinstance(tree, RedBlackTree) else None
    visited = set()
    ordered = []

    def walk(node, parent, lower=None, upper=None):
        if node is sentinel:
            return 1
        assert id(node) not in visited, 'Cycle or a real node shared by two parents'
        visited.add(id(node))
        assert node.get_parent() is parent, 'Incorrect parent link'
        assert lower is None or lower < node.key, 'Incorrect lower bound'
        assert upper is None or node.key < upper, 'Incorrect upper bound'
        left_height = walk(node.get_left(), node, lower, node.key)
        ordered.append(node.key)
        assert expected[node.key] == node.data, 'Incorrect stored value'
        right_height = walk(node.get_right(), node, node.key, upper)
        if sentinel is not None:
            if node.is_red():
                assert node.get_left().is_black() and node.get_right().is_black(), 'Red parent and child'
            assert left_height == right_height, 'Unequal black heights'
            return left_height + int(node.is_black())
        return 1

    if sentinel is not None:
        assert sentinel.is_black(), 'NIL must be black'
        assert sentinel.get_left() is sentinel and sentinel.get_right() is sentinel
        assert tree.root.is_black(), 'Root must be black'
    walk(tree.root, sentinel)
    assert ordered == sorted(expected), 'Membership differs from the reference mapping'
    assert tree.count_nodes_tree() == len(expected)


class TreeTests(unittest.TestCase):
    def test_reported_deletion_regression(self):
        tree = RedBlackTree()
        expected = {}
        for key in [0, 1, 3, 2]:
            tree.insert(key, key)
            expected[key] = key
            validate(tree, expected)
        self.assertTrue(tree.delete(0))
        del expected[0]
        validate(tree, expected)
        self.assertEqual(tree.find_node(0), None)

    def test_exhaustive_small_insertions_and_deletions(self):
        # Every insertion order and deletion order on five unique keys: 14,400
        # scenarios per tree. Check invariants after every mutation.
        orders = list(permutations(range(5)))
        for tree_class in (BinaryTree, RedBlackTree):
            for insertion in orders:
                for deletion in orders:
                    tree = tree_class()
                    expected = {}
                    for key in insertion:
                        tree.insert(key, str(key))
                        expected[key] = str(key)
                        validate(tree, expected)
                    for key in deletion:
                        self.assertTrue(tree.delete(key))
                        del expected[key]
                        validate(tree, expected)

    def test_seeded_mixed_operations_and_duplicate_keys(self):
        for tree_class in (BinaryTree, RedBlackTree):
            for seed in range(50):
                rng = random.Random(seed)
                tree = tree_class()
                expected = {}
                for step in range(200):
                    key = rng.randrange(40)
                    if rng.random() < 0.6:
                        tree.insert(key, step)
                        expected[key] = step
                    else:
                        self.assertEqual(tree.delete(key), key in expected)
                        expected.pop(key, None)
                    validate(tree, expected)
                    self.assertEqual(tree.find_node(key), (key, expected[key]) if key in expected else None)

    def test_empty_tree_and_reserved_key(self):
        for tree_class in (BinaryTree, RedBlackTree):
            tree = tree_class()
            self.assertEqual(tree.height(), -1)
            self.assertEqual(tree.average_depth(), 0.0)
            self.assertEqual(tree.longest_path(), [])
            self.assertFalse(tree.skew())
            self.assertTrue(tree.is_balanced_tree())
            self.assertFalse(tree.delete(5))
            with self.assertRaises(ValueError):
                tree.insert(None)
            validate(tree, {})

    def test_metrics_and_traversal_do_not_treat_nil_as_a_real_node(self):
        for module, tree_class in [(binary_tree, BinaryTree), (red_black_tree, RedBlackTree)]:
            tree = tree_class()
            for key in [5, 3, 7, 2, 4, 6, 8]:
                tree.insert(key)
            self.assertEqual(tree.height(), 2)
            self.assertEqual(tree.average_depth(), 2.0)
            self.assertEqual(tree.longest_path(), [5, 7, 8])
            self.assertFalse(tree.skew())
            output = StringIO()
            with redirect_stdout(output):
                module.in_order(tree)
            self.assertEqual(output.getvalue().split(), ['2', '3', '4', '5', '6', '7', '8'])
            output = StringIO()
            with redirect_stdout(output):
                tree.show()
            self.assertEqual(len(output.getvalue().splitlines()), 7)

    def test_height_balance_is_not_red_black_validity(self):
        tree = RedBlackTree()
        for key in range(10):
            tree.insert(key)
        validate(tree, dict.fromkeys(range(10)))
        self.assertFalse(tree.is_balanced_tree())
        self.assertTrue(tree.skew())

    def test_word_loader_and_reproducible_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            words_file = Path(temporary) / 'words.txt'
            words_file.write_text('apple\nboat\narch\napple\nArrow\n', encoding='utf-8')
            self.assertEqual(load_words_by_letter(words_file, 'A'), ['apple', 'arch', 'Arrow'])
        words = ['oak', 'apple', 'maple', 'birch']
        original = words.copy()
        first = build_trees(words, shuffled=True, seed=42)
        second = build_trees(words, shuffled=True, seed=42)
        self.assertEqual(words, original)
        for left, right in zip(first, second):
            self.assertEqual(left.longest_path(), right.longest_path())
            self.assertEqual(left.height(), right.height())
            validate(left, dict.fromkeys(words))


if __name__ == '__main__':
    unittest.main()
