# BST and red-black trees

A comparison of binary search trees (BSTs) and red-black trees (RBTs), using the
same words in sorted and shuffled insertion orders. Both structures implement
insertion, lookup, deletion and traversal directly. The experiment shows how
insertion order affects tree shape and how rotations limit height growth.

## Run

Python 3.12; tested with 3.12.14. Only the standard library is required.
From this folder:

```bash
python compare_trees.py --seed 42
python compare_trees.py --prefix a --prefix b --order shuffled --seed 42
python compare_trees.py --seed 42 --output results/sample_comparison.csv
python -m unittest discover -s tests -v
```

The output command replaces the named CSV. The fixture contains 98 common words.
To use your own permitted UTF-8 word list, with one word per line:

```bash
python compare_trees.py --words path/to/words.txt --prefix a --seed 42
```

Replace the placeholder path with an existing file. Prefix matching ignores case;
stored words keep their spelling. The loader removes identical duplicates and
accepts unsorted input. Both trees receive the same selected order, with at most
three prefixes and **400 words per prefix**. The original course dictionary is
not included; the small fixture is sufficient for the examples.

## Results and definitions

The saved [comparison](results/sample_comparison.csv), generated on 17 October
2026, uses all 98 fixture words and seed 42:

| Order | Tree | Height | Mean leaf depth | Height-balanced |
|---|---|---:|---:|---|
| Sorted | BST | 97 | 97.000000 | No |
| Sorted | RBT | 10 | 6.020408 | No |
| Shuffled | BST | 11 | 7.647059 | No |
| Shuffled | RBT | 7 | 5.840909 | No |

These are structural measurements, not timing benchmarks. Height counts edges
(empty tree: −1; one node: 0), and mean depth refers to real leaves.
`is_balanced_tree()` checks height balance, which is stricter than red-black
validity. A valid RBT can therefore return `False`.

Keys are unique: reinsertion replaces the associated value. `None` is reserved
for missing nodes. The RBT uses a shared black sentinel and restores colour
invariants after insertion/deletion. Sorted insertion makes an ordinary BST a
chain; the shuffled result is one example, not an average over orders.

## Limits

The recursive BST can reach Python's recursion limit on large degenerate trees.
Some traversal/printing helpers have quadratic worst-case costs. This is a small
teaching implementation, not a performance-tuned container library.

## Tests and version notes

The test command above runs seven tests. They cover all 120 insertion orders
crossed with all 120 deletion orders on five keys (14,400 combinations per tree),
plus 20,000 seeded mixed operations across both trees against a reference mapping.
Checks inspect ordering, values, parent links and counts; RBT checks also inspect
root/NIL colour, red-red violations and black height. These finite checks are
not a proof for every possible tree.

[Technical notes](docs/technical-notes.md) describe the interface and metric
conventions. This version includes post-submission fixes to sentinel handling
and successor colours during deletion, unique-key behaviour and empty-tree
metrics. The comparison still uses the coursework tree implementations.

## Academic context and credits

This is an Algorithms team project at iMAT, ICAI, Universidad Pontificia
Comillas, set as an assignment for pairs. The implementation uses course-derived
node interfaces. The teaching handout and original dictionary are not included.
