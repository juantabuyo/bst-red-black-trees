class Node:
    """A BST node. Child setters also maintain parent links."""

    def __init__(self, key, value=None):
        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value

    def get_left(self):
        return self._left

    def set_left(self, node):
        self._left = node
        if node is not None:
            node.set_parent(self)

    def get_right(self):
        return self._right

    def set_right(self, node):
        self._right = node
        if node is not None:
            node.set_parent(self)

    def get_parent(self):
        return self._parent

    def set_parent(self, node):
        self._parent = node

    def __str__(self):
        return f'{self.key} ({self.data})'

    def find_node(self, key):
        """Return the matching node, or None when the key is absent."""
        if self.key == key:
            return self
        elif key < self.key and self.get_left() is not None:
            return self.get_left().find_node(key)
        elif key > self.key and self.get_right() is not None:
            return self.get_right().find_node(key)
        return None

    def show(self, level=0, prefix='Root: ') -> None:
        """Print the tree structure."""
        indent = ' ' * (level * 4)
        print(f'{indent}{prefix}{self}')
        if self.get_left() is not None:
            self.get_left().show(level + 1, 'L--- ')
        if self.get_right() is not None:
            self.get_right().show(level + 1, 'R--- ')

    def min_key(self) -> 'Node':
        """Return the minimum-key node in this subtree."""
        current = self
        while current.get_left() is not None:
            current = current.get_left()
        return current

    def max_key(self) -> 'Node':
        """Return the maximum-key node in this subtree."""
        if self is None:
            return None
        current = self
        while current.get_right() is not None:
            current = current.get_right()
        return current

    def successor(self):
        """Return the next node in sorted order, or None at the maximum."""
        if self is not None:
            if self.get_right() is not None:
                return self.get_right().min_key()
            else:
                current = self
                parent = self.get_parent()
                while parent is not None and current == parent.get_right():
                    current = parent
                    parent = parent.get_parent()
            if parent is not None:
                return parent
        return None

    def predecessor(self):
        """Return the previous node in sorted order, or None at the minimum."""
        if self is not None:
            if self.get_left() is not None:
                return self.get_left().max_key()
            else:
                current = self
                parent = self.get_parent()
                while parent is not None and current == parent.get_left():
                    current = parent
                    parent = parent.get_parent()
            if parent is not None:
                return parent
        return None

    def height(self) -> int:
        """Return the longest root-to-leaf distance in edges; empty trees have height -1."""
        l = self.get_left().height() if self.get_left() is not None else -1
        r = self.get_right().height() if self.get_right() is not None else -1
        return max(l, r) + 1

class BinaryTree:
    """An unbalanced binary search tree with unique keys."""

    def __init__(self, root=None):
        self.root = root

    def show(self):
        """Print the tree structure."""
        if self.root is not None:
            self.root.show()
        else:
            print('Empty tree')

    def find_node(self, key):
        """Return (key, value), or None when the key is absent."""
        if self.root is None:
            return None
        n = self.root.find_node(key)
        if n:
            return (n.key, n.data)
        else:
            return None

    def insert(self, key, value=None) -> None:
        """Insert a unique key, or replace the value already stored at that key."""
        if key is None:
            raise ValueError('None is reserved for missing nodes')
        new_node = Node(key, value)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            cond = True
            while cond:
                if key == current.key:
                    current.data = value
                    return
                if key < current.key:
                    if current.get_left() is None:
                        current.set_left(new_node)
                        cond = False
                    else:
                        current = current.get_left()
                elif current.get_right() is None:
                    current.set_right(new_node)
                    cond = False
                else:
                    current = current.get_right()

    def height(self) -> int:
        """Return the longest root-to-leaf distance in edges; empty trees have height -1."""
        if self.root is None:
            return -1
        return self.root.height()

    def delete(self, key) -> bool:
        """Remove a key. Return False when the key is absent."""
        node_to_delete = self.root.find_node(key) if self.root else None
        if node_to_delete is None:
            return False
        parent = node_to_delete.get_parent()
        if node_to_delete.get_left() is None and node_to_delete.get_right() is None:
            if parent is None:
                self.root = None
            elif node_to_delete == parent.get_left():
                parent.set_left(None)
            else:
                parent.set_right(None)
        elif node_to_delete.get_left() is None or node_to_delete.get_right() is None:
            child = node_to_delete.get_left() if node_to_delete.get_left() is not None else node_to_delete.get_right()
            if parent is None:
                self.root = child
                self.root.set_parent(None)
            elif node_to_delete == parent.get_left():
                parent.set_left(child)
            else:
                parent.set_right(child)
        else:
            successor = node_to_delete.successor()
            if successor is not None:
                temp_node = Node(successor.key, successor.data)
                self.delete(successor.key)
                swap_contents(node_to_delete, temp_node)
        return True

    def count_nodes_tree(self) -> int:
        """Count the nodes in the tree."""

        def count(node) -> int:
            if node is None:
                return 0
            return 1 + count(node.get_left()) + count(node.get_right())
        return count(self.root)

    def is_balanced_tree(self) -> bool:
        """Check that child heights differ by at most one at every node."""

        def check(node):
            if node is None:
                return (True, -1)
            ok_l, h_l = check(node.get_left())
            ok_r, h_r = check(node.get_right())
            balanced = ok_l and ok_r and (abs(h_l - h_r) <= 1)
            return (balanced, max(h_l, h_r) + 1)
        return check(self.root)[0]

    def average_depth(self) -> float:
        """Return the mean depth of real leaf nodes; root depth is zero."""
        if self.root is None:
            return 0.0

        def dfs(node, depth):
            if node is None:
                return (0, 0)
            if node.get_left() is None and node.get_right() is None:
                return (depth, 1)
            total_l, leaves_l = dfs(node.get_left(), depth + 1)
            total_r, leaves_r = dfs(node.get_right(), depth + 1)
            return (total_l + total_r, leaves_l + leaves_r)
        total, leaves = dfs(self.root, 0)
        return total / leaves if leaves > 0 else 0.0

    def longest_path(self) -> list[object]:
        """Return one longest root-to-leaf path. Ties select the right subtree."""

        def path(node):
            if node is None:
                return []
            left = path(node.get_left())
            right = path(node.get_right())
            return [node.key] + (left if len(left) > len(right) else right)
        return path(self.root)

    def skew(self) -> bool:
        """Return whether any node violates height balance; not red-black validity."""

        def sk(node):
            if node is None:
                return (False, -1)
            l_sk, l_h = sk(node.get_left())
            r_sk, r_h = sk(node.get_right())
            here = abs(l_h - r_h) > 1
            return (l_sk or r_sk or here, max(l_h, r_h) + 1)
        return sk(self.root)[0]

def swap_contents(node1, node2) -> None:
    """Exchange the keys and data of two real nodes."""
    node1.key, node2.key = (node2.key, node1.key)
    node1.data, node2.data = (node2.data, node1.data)

def in_order(tree: BinaryTree) -> None:
    """Print keys in left-root-right order."""

    def _in(node):
        if node is None:
            return
        _in(node.get_left())
        print(node.key, end=' ')
        _in(node.get_right())
    _in(tree.root)
    print()

def pre_order(tree: BinaryTree) -> None:
    """Print keys in root-left-right order."""

    def pre(node):
        if node is None:
            return
        print(node.key, end=' ')
        pre(node.get_left())
        pre(node.get_right())
    pre(tree.root)
    print()

def post_order(tree: BinaryTree) -> None:
    """Print keys in left-right-root order."""

    def post(node):
        if node is None:
            return
        post(node.get_left())
        post(node.get_right())
        print(node.key, end=' ')
    post(tree.root)
    print()

def level_order(tree: BinaryTree) -> None:
    """Print keys in breadth-first order."""
    if tree.root is None:
        return
    queue = [tree.root]
    while queue:
        node = queue.pop(0)
        print(node.key, end=' ')
        if node.get_left() is not None:
            queue.append(node.get_left())
        if node.get_right() is not None:
            queue.append(node.get_right())
    print()


def main():
    """Print a small demonstration; assertions live in tests/."""
    tree = BinaryTree()
    for key in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(key)
    tree.show()
    print('In-order before deletion:')
    in_order(tree)
    tree.delete(3)
    tree.delete(7)
    print('In-order after deleting 3 and 7:')
    in_order(tree)
    print('Height:', tree.height())
    print('Mean leaf depth:', tree.average_depth())
    print('Height-balanced:', tree.is_balanced_tree())


if __name__ == '__main__':
    main()
