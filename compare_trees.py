"""Compare the original project's BST and RBT on the same word sequences."""

import argparse
import csv
from pathlib import Path
import random
import sys

from binary_tree import BinaryTree
from red_black_tree import RedBlackTree

DEFAULT_WORDS = Path(__file__).with_name('data') / 'sample_words.txt'


def load_words_by_letter(path, letter='', max_words=400):
    """Read distinct words, without assuming the input file is sorted.

    Words are not translated or case-normalised. Only the optional prefix
    comparison ignores case. The limit bounds the recursive BST demonstration.
    """
    words = []
    seen = set()
    with Path(path).open(encoding='utf-8') as source:
        for line in source:
            word = line.strip()
            if word and word.casefold().startswith(letter.casefold()) and word not in seen:
                words.append(word)
                seen.add(word)
                if len(words) == max_words:
                    break
    return words


def build_trees(words, shuffled=False, seed=42):
    """Use identical insertion orders for both trees; leave input unchanged."""
    insertion_order = sorted(words)
    if shuffled:
        random.Random(seed).shuffle(insertion_order)
    bst = BinaryTree()
    rbt = RedBlackTree()
    for word in insertion_order:
        bst.insert(word)
        rbt.insert(word)
    return bst, rbt


def tree_metrics(name, tree, order, prefix, seed):
    return {
        'prefix': prefix or '(all)', 'order': order, 'seed': seed, 'tree': name,
        'nodes': tree.count_nodes_tree(), 'height': tree.height(),
        'height_balanced': tree.is_balanced_tree(),
        'mean_leaf_depth': round(tree.average_depth(), 6),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--words', type=Path, default=DEFAULT_WORDS,
                        help='UTF-8 file with one word per line')
    parser.add_argument('--prefix', action='append', default=[],
                        help='Case-insensitive prefix; repeat up to three times')
    parser.add_argument('--order', choices=('sorted', 'shuffled', 'both'), default='both')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--max-words', type=int, default=400,
                        help='Use at most 400 words per prefix to bound recursive BST depth')
    parser.add_argument('--output', type=Path, help='Optional CSV path; otherwise print CSV')
    args = parser.parse_args()
    if not 1 <= args.max_words <= 400:
        parser.error('--max-words must be between 1 and 400')
    if len(args.prefix) > 3:
        parser.error('At most three prefixes are supported')
    rows = []
    orders = ('sorted', 'shuffled') if args.order == 'both' else (args.order,)
    for prefix in args.prefix or ['']:
        try:
            words = load_words_by_letter(args.words, prefix, args.max_words)
        except (OSError, UnicodeError) as error:
            parser.error(f'Cannot read the word file: {error}')
        for order in orders:
            bst, rbt = build_trees(words, order == 'shuffled', args.seed)
            rows.extend(tree_metrics(name, tree, order, prefix, args.seed)
                        for name, tree in [('BST', bst), ('RBT', rbt)])
    if args.output:
        with args.output.open('w', encoding='utf-8', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    main()
