

class TreeNode:
    def __init__(self, representative_words, index=None):
        self.representative_words = representative_words
        self.index = index
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.representative_words) + " (Index: " + str(self.index) + ")\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
    def show(self, storey=0):
        print(storey, end=" ")
        print(self.representative_words, end=' ')
        print(self.index)
        for child in self.children:
            child.show(storey+1)
    
    def destroy(self):
        for child in self.children:
            child.destroy()
        self.children.clear()
        self.representative_words = None
        self.index = None

class CharacterTree:
    def __init__(self):
        self.root = TreeNode(None)
    
    def build_tree(self, data):
        stack = [self.root]
        for nodeinfo in data:
            level = nodeinfo[0]
            representative_words = nodeinfo[1]
            indexes = nodeinfo[2]
            new_node = TreeNode(representative_words, indexes)
            
            while len(stack) > level:
                stack.pop()

            stack[-1].add_child(new_node)
            stack.append(new_node)
    
    def traverse(self):
        self.root.show()
    
    def destroy(self):
        self.root.destroy()

    def update(self, data):
        self.destroy()
        self.build_tree(data)
    
    
            

data = [[1, ['diagram', 'the', 'of'], [0, 2, 8, 13]], 
        [2, ['network', 'several', 'dots'], [8]], 
        [2, ['new', 'interface', 'the'], [13]], 
        [2, ['blue', 'tower', 'computer'], [0]], 
        [2, ['system', 'the', 'diagram'], [2]], 
        [1, ['you', 'iq', 'this'], [10]], 
        [1, ['ich', 'nicht', 'die'], [3, 4, 5, 6, 7]], 
        [2, ['ich', 'vater', 'und'], [5]], 
        [2, ['am', 'diestag', 'jacke'], [4]], 
        [2, ['with', 'sheets', 'of'], [3]], 
        [2, ['wir', 'der', 'drei'], [7]], 
        [2, ['ich', 'nicht', 'jeans'], [6]], 
        [1, ['this', 'is', 'for'], [1, 9, 11, 14, 15]], 
        [2, ['heart', 'with', 'laptop'], [11]], 
        [2, ['score', 'is', 'this'], [14]], 
        [2, ['to', 'is', 'test'], [9]], 
        [2, ['zhoubohan', 'homework', 'this'], [15]], 
        [2, ['gpa', 'this', 'test'], [1]], 
        [1, ['he', 'to', 'if'], [12]]]

new_data = [[1, ['diagram', 'the', 'of'], [1, 2, 8, 13]], 
        [2, ['network', 'several', 'dots'], [8]], 
        [2, ['new', 'interface', 'the'], [13]], 
        [2, ['blue', 'tower', 'computer'], [0]], 
        [2, ['system', 'the', 'diagram'], [2]], 
        [1, ['you', 'iq', 'this'], [10]], 
        [1, ['ich', 'nicht', 'die'], [3, 4, 5, 6, 7]], 
        [2, ['ich', 'vater', 'und'], [5]], 
        [2, ['am', 'diestag', 'jacke'], [4]], 
        [2, ['with', 'sheets', 'of'], [3]], 
        [2, ['wir', 'der', 'drei'], [7]], 
        [2, ['ich', 'nicht', 'jeans'], [6]], 
        [1, ['this', 'is', 'for'], [1, 9, 11, 14, 15]], 
        [2, ['heart', 'with', 'laptop'], [11]], 
        [2, ['score', 'is', 'this'], [14]], 
        [2, ['to', 'is', 'test'], [9]], 
        [2, ['zhoubohan', 'homework', 'this'], [15]], 
        [2, ['gpa', 'this', 'test'], [1]], 
        [1, ['he', 'to', 'if'], [56]]]
  
CTree = CharacterTree()
CTree.build_tree(data)
CTree.traverse()
CTree.update(new_data)
CTree.traverse()
