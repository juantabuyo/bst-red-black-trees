from enum import Enum

class Color(Enum):
    RED = 0
    BLACK = 1

class RBNode:
    """A coloured node. A shared NIL node represents missing children."""

    def __init__(self, key, value=None, color=Color.RED) -> None:
        self._is_nil = False
        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value
        self.color = color

    def is_red(self) -> bool:
        return self.color == Color.RED

    def is_black(self) -> bool:
        return self.color == Color.BLACK

    def set_red(self) -> None:
        self.color = Color.RED

    def set_black(self) -> None:
        self.color = Color.BLACK

    def get_left(self) -> 'RBNode':
        return self._left

    def set_left(self, node) -> None:
        self._left = node
        if node is not None and not node._is_nil:
            node._parent = self

    def get_right(self) -> 'RBNode':
        return self._right

    def set_right(self, node) -> None:
        self._right = node
        if node is not None and not node._is_nil:
            node._parent = self

    def get_parent(self) -> 'RBNode':
        return self._parent

    def set_parent(self, node) -> None:
        self._parent = node

    def __str__(self) -> str:
        c = 'R' if self.is_red() else 'B'
        return f'{self.key}({c})'

    def show(self, level: int=0, prefix: str='Root: ') -> None:
        """Print the tree structure."""
        indent = ' ' * (4 * level)
        print(f'{indent}{prefix}{self}')
        if self.get_left() is not None and not self.get_left()._is_nil:
            self.get_left().show(level + 1, 'L--- ')
        if self.get_right() is not None and not self.get_right()._is_nil:
            self.get_right().show(level + 1, 'R--- ')

class RedBlackTree:
    """A red-black search tree with unique keys and a shared black sentinel."""

    def __init__(self, root=None) -> None:
        self.NIL = RBNode(None)
        self.NIL.set_black()
        self.NIL._is_nil = True
        self.NIL.set_left(self.NIL)
        self.NIL.set_right(self.NIL)
        self.NIL.set_parent(self.NIL)
        self.root = self.NIL
        if root is not None:
            self.insert(root.key, root.data)

    def left_rotate(self, x: RBNode) -> None:
        """Rotate left at x, preserving search order and real-node parent links."""
        y = x.get_right()
        x.set_right(y.get_left())
        if y.get_left() != self.NIL:
            y.get_left().set_parent(x)
        y.set_parent(x.get_parent())
        if x.get_parent() is self.NIL:
            self.root = y
        elif x == x.get_parent().get_left():
            x.get_parent().set_left(y)
        else:
            x.get_parent().set_right(y)
        y.set_left(x)
        x.set_parent(y)

    def right_rotate(self, y: RBNode) -> None:
        """Rotate right at y, preserving search order and real-node parent links."""
        x = y.get_left()
        y.set_left(x.get_right())
        if x.get_right() != self.NIL:
            x.get_right().set_parent(y)
        x.set_parent(y.get_parent())
        if y.get_parent() is self.NIL:
            self.root = x
        elif y == y.get_parent().get_right():
            y.get_parent().set_right(x)
        else:
            y.get_parent().set_left(x)
        x.set_right(y)
        y.set_parent(x)

    def insert(self, key, value=None) -> None:
        """Insert a unique key, or replace the value already stored at that key."""
        if key is None:
            raise ValueError('None is reserved for missing nodes')
        y = self.NIL
        x = self.root
        z = RBNode(key, value)
        while x != self.NIL:
            y = x
            if z.key == x.key:
                x.data = value
                return
            if z.key < x.key:
                x = x.get_left()
            else:
                x = x.get_right()
        z.set_parent(y)
        if y is self.NIL:
            self.root = z
        elif z.key < y.key:
            y.set_left(z)
        else:
            y.set_right(z)
        z.set_left(self.NIL)
        z.set_right(self.NIL)
        z.set_red()
        self.insert_fixup(z)

    def insert_fixup(self, z: RBNode) -> None:
        """Restore red-black invariants using recolouring and rotations."""
        while z.get_parent().is_red():
            if z.get_parent() == z.get_parent().get_parent().get_left():
                y = z.get_parent().get_parent().get_right()
                if y.is_red():
                    z.get_parent().set_black()
                    y.set_black()
                    z.get_parent().get_parent().set_red()
                    z = z.get_parent().get_parent()
                else:
                    if z == z.get_parent().get_right():
                        z = z.get_parent()
                        self.left_rotate(z)
                    z.get_parent().set_black()
                    z.get_parent().get_parent().set_red()
                    self.right_rotate(z.get_parent().get_parent())
            else:
                y = z.get_parent().get_parent().get_left()
                if y.is_red():
                    z.get_parent().set_black()
                    y.set_black()
                    z.get_parent().get_parent().set_red()
                    z = z.get_parent().get_parent()
                else:
                    if z == z.get_parent().get_left():
                        z = z.get_parent()
                        self.right_rotate(z)
                    z.get_parent().set_black()
                    z.get_parent().get_parent().set_red()
                    self.left_rotate(z.get_parent().get_parent())
        self.root.set_black()

    def search(self, k) -> RBNode:
        """Return the matching node, or NIL when the key is absent."""
        cur = self.root
        while cur != self.NIL and k != cur.key:
            cur = cur.get_left() if k < cur.key else cur.get_right()
        return cur

    def find_node(self, k) -> tuple:
        """Return (key, value), or None when the key is absent."""
        n = self.search(k)
        return (n.key, n.data) if n != self.NIL else None

    def minimum(self, n) -> RBNode:
        """Return the minimum-key node in the given non-empty subtree."""
        current = n
        while current.get_left() != self.NIL:
            current = current.get_left()
        return current

    def transplant(self, u, v) -> None:
        """Replace subtree u with v; record the new parent even when v is NIL."""
        if u.get_parent() == self.NIL:
            self.root = v
        elif u == u.get_parent().get_left():
            u.get_parent().set_left(v)
        else:
            u.get_parent().set_right(v)
        v.set_parent(u.get_parent())

    def skew(self) -> bool:
        """Return whether any node violates height balance; not red-black validity."""

        def sk(node):
            if node is self.NIL:
                return (False, -1)
            l_sk, l_h = sk(node.get_left())
            r_sk, r_h = sk(node.get_right())
            here = abs(l_h - r_h) > 1
            return (l_sk or r_sk or here, max(l_h, r_h) + 1)
        return sk(self.root)[0]

    def delete(self, key) -> bool:
        """Remove a key. Return False when the key is absent."""
        z = self.search(key)
        if z == self.NIL:
            return False
        y = z
        y_color = y.color
        if z.get_left() == self.NIL:
            x = z.get_right()
            self.transplant(z, z.get_right())
        elif z.get_right() == self.NIL:
            x = z.get_left()
            self.transplant(z, z.get_left())
        else:
            y = self.minimum(z.get_right())
            y_color = y.color
            x = y.get_right()
            if y.get_parent() == z:
                x.set_parent(y)
            else:
                self.transplant(y, y.get_right())
                y.set_right(z.get_right())
            self.transplant(z, y)
            y.set_left(z.get_left())
            y.color = z.color
        if y_color == Color.BLACK:
            self.delete_fixup(x)
        self.NIL.set_parent(self.NIL)
        return True

    def delete_fixup(self, x: RBNode) -> None:
        """Restore black heights after deleting a black node.

        NIL is black and self-linked. Its parent temporarily records the removed
        position; rotations must not overwrite that parent through unrelated leaves.
        """
        while x != self.root and x.is_black():
            if x == x.get_parent().get_left():
                w = x.get_parent().get_right()
                if w.is_red():
                    w.set_black()
                    x.get_parent().set_red()
                    self.left_rotate(x.get_parent())
                    w = x.get_parent().get_right()
                if w.get_left().is_black() and w.get_right().is_black():
                    w.set_red()
                    x = x.get_parent()
                else:
                    if w.get_right().is_black():
                        w.get_left().set_black()
                        w.set_red()
                        self.right_rotate(w)
                        w = x.get_parent().get_right()
                    w.color = x.get_parent().color
                    x.get_parent().set_black()
                    w.get_right().set_black()
                    self.left_rotate(x.get_parent())
                    x = self.root
            else:
                w = x.get_parent().get_left()
                if w.is_red():
                    w.set_black()
                    x.get_parent().set_red()
                    self.right_rotate(x.get_parent())
                    w = x.get_parent().get_left()
                if w.get_left().is_black() and w.get_right().is_black():
                    w.set_red()
                    x = x.get_parent()
                else:
                    if w.get_left().is_black():
                        w.get_right().set_black()
                        w.set_red()
                        self.left_rotate(w)
                        w = x.get_parent().get_left()
                    w.color = x.get_parent().color
                    x.get_parent().set_black()
                    w.get_left().set_black()
                    self.right_rotate(x.get_parent())
                    x = self.root
        x.set_black()

    def height(self) -> int:
        """Return the longest root-to-leaf distance in edges; empty trees have height -1."""

        def h(n):
            if n == self.NIL:
                return -1
            return 1 + max(h(n.get_left()), h(n.get_right()))
        return h(self.root)

    def count_nodes_tree(self) -> int:
        """Count real nodes, excluding the sentinel."""

        def c(n):
            if n == self.NIL:
                return 0
            return 1 + c(n.get_left()) + c(n.get_right())
        return c(self.root)

    def is_balanced_tree(self) -> bool:
        """Test height balance: child heights differ by at most one at every node.

        This is not a test of the red-black invariants.
        """

        def check(n):
            if n == self.NIL:
                return (True, -1)
            ok_l, h_l = check(n.get_left())
            ok_r, h_r = check(n.get_right())
            return (ok_l and ok_r and (abs(h_l - h_r) <= 1), max(h_l, h_r) + 1)
        return check(self.root)[0]

    def average_depth(self) -> float:
        """Return the mean depth of real leaf nodes; root depth is zero."""
        if self.root == self.NIL:
            return 0.0

        def dfs(n, d):
            if n == self.NIL:
                return (0, 0)
            if n.get_left() == self.NIL and n.get_right() == self.NIL:
                return (d, 1)
            sum_l, cnt_l = dfs(n.get_left(), d + 1)
            sum_r, cnt_r = dfs(n.get_right(), d + 1)
            return (sum_l + sum_r, cnt_l + cnt_r)
        total, leaves = dfs(self.root, 0)
        return total / leaves if leaves else 0.0

    def longest_path(self) -> list:
        """Return one longest root-to-leaf path. Ties select the right subtree."""

        def lp(n):
            if n == self.NIL:
                return []
            left = lp(n.get_left())
            right = lp(n.get_right())
            return [n.key] + (left if len(left) > len(right) else right)
        return lp(self.root)

    def show(self) -> None:
        """Print the tree structure."""
        if self.root != self.NIL:
            self.root.show()
        else:
            print('Empty tree')

def in_order(tree: RedBlackTree) -> None:
    """Print keys in left-root-right order."""

    def _in(node):
        if node is None or getattr(node, 'key', None) is None:
            return
        _in(node.get_left())
        print(node.key, end=' ')
        _in(node.get_right())
    if getattr(tree.root, 'key', None) is not None:
        _in(tree.root)
    print()

def pre_order(tree: RedBlackTree) -> None:
    """Print keys in root-left-right order."""

    def pre(node):
        if node is None or getattr(node, 'key', None) is None:
            return
        print(node.key, end=' ')
        pre(node.get_left())
        pre(node.get_right())
    if getattr(tree.root, 'key', None) is not None:
        pre(tree.root)
    print()

def post_order(tree: RedBlackTree) -> None:
    """Print keys in left-right-root order."""

    def post(node):
        if node is None or getattr(node, 'key', None) is None:
            return
        post(node.get_left())
        post(node.get_right())
        print(node.key, end=' ')
    if getattr(tree.root, 'key', None) is not None:
        post(tree.root)
    print()

def level_order(tree: RedBlackTree) -> None:
    """Print keys in breadth-first order."""
    if tree.root == tree.NIL:
        return
    queue = [tree.root]
    while queue:
        node = queue.pop(0)
        print(node.key, end=' ')
        if node.get_left() != tree.NIL:
            queue.append(node.get_left())
        if node.get_right() != tree.NIL:
            queue.append(node.get_right())
    print()


def main():
    """Print a small demonstration; assertions live in tests/."""
    tree = RedBlackTree()
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
