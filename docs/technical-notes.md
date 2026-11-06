# Tree interfaces and metrics

The [README](../README.md) gives comparison commands and the 98-word example.

## Interface

Keys must be mutually comparable and cannot be `None`. Reinserting a key replaces
its value. `find_node(key)` returns `(key, value)` or `None`; `delete(key)` reports
whether the key existed. Directly changing links or colours is outside normal use.

The red-black tree's shared black NIL sentinel has self-linked children. Its
parent temporarily identifies the deletion position during fix-up; unrelated
leaf assignments must not overwrite it.

## Metrics

- Height counts edges: −1 for an empty tree and 0 for one node.
- `average_depth()` averages real leaves and returns 0.0 for an empty tree.
- `longest_path()` resolves ties to the right.
- `is_balanced_tree()` and `skew()` measure height balance, separately from
  red-black invariants. A valid red-black tree need not meet the stricter
  height-balance condition.

Recursive degenerate BSTs can exceed Python's recursion limit. Copying longest
paths and using a list as a queue can have quadratic costs. The fixture comparison
measures structure, not large-dictionary performance or runtime.

## Draw the example

The drawing uses Matplotlib; the algorithms themselves use the standard library.
From the project folder:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-visualisation.txt
python preview.py
```

`preview.py` calls `build_trees()` and replaces
`docs/images/tree-comparison.png`. It draws keys 1 to 10 from the project's tree
classes on a shared depth scale, with their actual red-black colours.
