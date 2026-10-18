# Tree interface and metrics

The [README](../README.md) gives comparison commands and the saved 98-word example.
Keys must be mutually comparable and cannot be `None`. Reinserting a key replaces
its value. `find_node(key)` returns `(key, value)` or `None`; `delete(key)` reports
whether the key existed. Directly modifying links or colours is outside normal use.

The RBT's shared black NIL sentinel has self-linked children. Its parent temporarily
identifies the deletion position during fix-up; unrelated leaf assignments must
not overwrite it.

Height counts edges: −1 for an empty tree and 0 for a single node.
`average_depth()` averages real leaves and returns 0.0 for an empty tree.
`longest_path()` resolves ties to the right. `is_balanced_tree()` and `skew()`
measure height balance, separately from red-black invariants. A valid RBT need
not meet this stricter height-balance condition.

Recursive degenerate BSTs can exceed Python's recursion limit. Copying longest
paths and using a list as a queue can have quadratic costs. The fixture comparison
is structural, not a large-dictionary or runtime benchmark.
