class Node:
    def __init__(self, key):
        self.key = key
        self.color = 'red'
        self.parent = None
        self.left = None
        self.right = None

class RBTree:
    def __init__(self):
        self.nil = Node(0)
        self.nil.color = 'black'
        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_after_insert(self, x):
        while x.parent.color == 'red':
            if x.parent == x.parent.parent.right:
                y = x.parent.parent.left
                if y.color == 'red':
                    x.parent.color = 'black'
                    y.color = 'black'
                    x.parent.parent.color = 'red'
                    x = x.parent.parent
                else:
                    if x == x.parent.left:
                        x = x.parent
                        self.right_rotate(x)
                    x.parent.color = 'black'
                    x.parent.parent.color = 'red'
                    self.left_rotate(x.parent.parent)
            else:
                y = x.parent.parent.right
                if y.color == 'red':
                    x.parent.color = 'black'
                    y.color = 'black'
                    x.parent.parent.color = 'red'
                    x = x.parent.parent
                else:
                    if x == x.parent.right:
                        x = x.parent
                        self.left_rotate(x)
                    x.parent.color = 'black'
                    x.parent.parent.color = 'red'
                    self.right_rotate(x.parent.parent)
        self.root.color = 'black'

    def insert(self, key):
        z = Node(key)
        y = None
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self.fix_after_insert(z)

    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def min_value_node(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def delete_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                y = x.parent.right
                if y.color == 'red':
                    y.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    y = x.parent.right
                if y.left.color == 'black' and y.right.color == 'black':
                    y.color = 'red'
                    x = x.parent
                elif y.right.color == 'black':
                    y.left.color = 'black'
                    y.color = 'red'
                    self.right_rotate(y)
                    y = x.parent.right
                y.color = x.parent.color
                x.parent.color = 'black'
                y.right.color = 'black'
                self.left_rotate(x.parent)
                x = self.root
            else:
                y = x.parent.left
                if y.color == 'red':
                    y.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    y = x.parent.left
                if y.right.color == 'black' and y.left.color == 'black':
                    y.color = 'red'
                    x = x.parent
                elif y.left.color == 'black':
                    y.right.color = 'black'
                    y.color = 'red'
                    self.left_rotate(y)
                    y = x.parent.left
                y.color = x.parent.color
                x.parent.color = 'black'
                y.left.color = 'black'
                self.right_rotate(x.parent)
                x = self.root
        x.color = 'black'

    def delete(self, z):
        if z.left == self.nil:
            y = self.min_value_node(z.right)
        elif z.right == self.nil:
            y = self.min_value_node(z.left)
        else:
            y = self.min_value_node(z.right)
        if y != z:
            x = y.right
            while x != self.nil:
                y = x
                x = x.left
            y.right = z.right
        else:
            x = z.left
        if z.parent == None:
            self.root = x
        elif z == z.parent.left:
            z.parent.left = x
        else:
            z.parent.right = x
        if y != z:
            self.transplant(z, y)
        else:
            self.transplant(z, z.left)
        self.delete_fix(x)

    def search(self, key):
        x = self.root
        while x != self.nil:
            if x.key == key:
                return True
            elif x.key > key:
                x = x.left
            else:
                x = x.right
        return False

    def inorder_tree_walk(self, x):
        if x != self.nil:
            self.inorder_tree_walk(x.left)
            print(x.key, end=" ")
            self.inorder_tree_walk(x.right)

if __name__ == "__main__":
    rbt = RBTree()
    rbt.insert(50)
    rbt.insert(30)
    rbt.insert(20)
    rbt.insert(40)
    rbt.insert(70)
    rbt.insert(60)
    rbt.insert(80)
    print("Inorder traversal of constructed tree is")
    rbt.inorder_tree_walk(rbt.root)
    print("\nAfter deleting 20")
    rbt.delete(rbt.search(20))
    rbt.inorder_tree_walk(rbt.root)
