class BTreeNode:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

    def get_index(self, key):
        for i, k in enumerate(self.keys):
            if k > key:
                return i
        return len(self.keys)

    def insert_non_full(self, key):
        if len(self.keys) < self.order - 1:
            self.keys.append(key)
            return True
        else:
            return False

    def split_and_insert(self, key):
        if not self.insert_non_full(key):
            new_node = BTreeNode(self.order)
            mid = len(self.keys) // 2
            new_node.keys = self.keys[mid:]
            for child in self.children[mid:]:
                new_node.children.append(child)
            for i in range(mid - 1, -1, -1):
                self.keys[i + 1] = self.keys[i]
            self.keys[mid] = key
            self.children.append(new_node)

    def delete_key(self, key):
        i = self.get_index(key)
        if i > 0 and self.keys[i - 1] > key:
            i -= 1
        if i < len(self.keys) and self.keys[i + 1] == key:
            self.keys.pop(i + 1)
        else:
            return False
        if not self.is_leaf():
            if len(self.children[i + 1].keys) > self.order // 2:
                self.keys.insert(i, self.children[i + 1].keys[0])
                self.children[i + 1].keys.pop(0)
                if not self.children[i + 1].is_leaf():
                    self.children[i + 1].delete_key(self.keys[i])
            else:
                self.keys.insert(i, self.children[i + 1].keys[-1])
                self.children[i + 1].keys.pop()
                if not self.children[i + 1].is_leaf():
                    self.children[i + 1].delete_key(self.keys[i + 1])
        else:
            if len(self.keys) > self.order:
                self.keys.pop(i)
        return True

    def search(self, key):
        i = self.get_index(key)
        if i < len(self.keys) and self.keys[i] == key:
            return True
        elif i > 0 and self.keys[i - 1] > key:
            i -= 1
        return self.children[i].search(key) if not self.is_leaf() else False


class BTree:
    def __init__(self, order):
        self.root = BTreeNode(order)

    def insert(self, key):
        if not self.root.insert_non_full(key):
            new_root = BTreeNode(self.root.order)
            new_root.keys.append(self.root.keys[0])
            new_root.children.append(self.root)
            for i, child in enumerate(self.root.children[1:]):
                new_root.children.append(child)
            for i, key in enumerate(self.root.keys[1:]):
                new_root.keys.append(key)
            self.root = new_root
        self.root.insert_non_full(key)

    def delete(self, key):
        if not self.root.delete_key(key):
            return False
        if self.root.is_leaf():
            if len(self.root.keys) == 0:
                self.root = None
        else:
            for i, child in enumerate(self.root.children):
                if not child.is_leaf():
                    break
            else:
                i = 0
            if len(self.root.children[i].keys) > self.root.order // 2:
                self.root.keys.insert(i, self.root.children[i].keys[0])
                self.root.children[i].keys.pop(0)
                if not self.root.children[i].is_leaf():
                    self.root.delete(self.root.keys[i])
            else:
                self.root.keys.insert(i, self.root.children[i].keys[-1])
                self.root.children[i].keys.pop()
                if not self.root.children[i].is_leaf():
                    self.root.delete(self.root.keys[i + 1])
        return True

    def search(self, key):
        return self.root.search(key)