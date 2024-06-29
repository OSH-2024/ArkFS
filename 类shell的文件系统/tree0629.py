

class TreeNode:
    def __init__(self, representative_words, index=None, time=None, state=None):
        self.representative_words = representative_words
        self.index = index
        self.time = time
        self.type = state
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
        print(self.index, end=" ")
        print(self.time, end=" ")
        print(self.type)
        for child in self.children:
            child.show(storey+1)
    
    def destroy(self):
        for child in self.children:
            child.destroy()
        self.children.clear()
        self.representative_words = None
        self.index = None
        self.time = None
        self.type = None

class CharacterTree:
    def __init__(self):
        self.root = TreeNode(None)
    
    def build_tree(self, data):
        stack = [self.root]
        for nodeinfo in data:
            level = nodeinfo[0]
            representative_words = nodeinfo[1]
            if len(nodeinfo[2]) > 1:
                indexes = None
                time = None
                state = None
            else:
                indexes = nodeinfo[2][0][0]
                time = nodeinfo[2][0][1]
                state = nodeinfo[2][0][2]
            
            new_node = TreeNode(representative_words, indexes, time, state)
            
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
    
    
            

data = [[1, ['diagram', 'the', 'of'], 
         [(0, 1713275347.023852, 'img', 'a computer tower with a blue light shining on it'), 
          (2, 1714214477.0871334, 'img', 'a diagram of the system'), 
          (8, 1714214477.097888, 'img', 'a diagram of a network with several dots'), 
          (13, 1713275562.494238, 'img', 'the new interface in the new interface editor')]], 
          [2, ['system', 'diagram', 'the'], 
           [(8, 1714214477.097888, 'img', 'a diagram of a network with several dots')]], 
           [2, ['sheets', 'background', 'paper'], 
            [(13, 1713275562.494238, 'img', 'the new interface in the new interface editor')]], 
            [2, ['shining', 'light', 'computer'], 
             [(0, 1713275347.023852, 'img', 'a computer tower with a blue light shining on it')]], 
             [2, ['gpa', 'this', 'test'], 
              [(2, 1714214477.0871334, 'img', 'a diagram of the system')]], 
              [1, ['you', 'iq', 'this'], 
               [(10, 1717255847.0698338, 'txt', "This is a test for liumingle's IQ. If you think you have a high IQ, try this test.")]], [1, ['ich', 'nicht', 'die'], [(3, 1713275347.039931, 'img', 'a pile of paper sheets with a blue background'), (4, 1718022455.3486648, 'txt', '"Ich muss eine neue Jacke für das Jobinterview am Diestag kaufen"'), (5, 1718022455.3495991, 'txt', '"Ich brauche die Jeans für meinen Vater, und ich muss einen neue schuhe kaufen"'), (6, 1718022455.3495991, 'txt', '"Ich brauche die Jeans nicht. Ich brauches die jeans nicht" - Jürgen Schubert. Schulder: "Ich habe ein gutes Leben."'), (7, 1718022455.3495991, 'txt', '"Wir brauchen der stuhl nicht, denn wir haben drei Stühle"')]], [2, ['system', 'diagram', 'the'], [(5, 1718022455.3495991, 'txt', '"Ich brauche die Jeans für meinen Vater, und ich muss einen neue schuhe kaufen"')]], [2, ['gpa', 'this', 'test'], [(4, 1718022455.3486648, 'txt', '"Ich muss eine neue Jacke für das Jobinterview am Diestag kaufen"')]], [2, ['shining', 'light', 'computer'], [(3, 1713275347.039931, 'img', 'a pile of paper sheets with a blue background')]], [2, ['diestag', 'jacke', 'am'], [(7, 1718022455.3495991, 'txt', '"Wir brauchen der stuhl nicht, denn wir haben drei Stühle"')]], [2, ['sheets', 'background', 'paper'], [(6, 1718022455.3495991, 'txt', '"Ich brauche die Jeans nicht. Ich brauches die jeans nicht" - Jürgen Schubert. Schulder: "Ich habe ein gutes Leben."')]], [1, ['this', 'is', 'for'], [(1, 1717255895.5607598, 'txt', "This is a test for changsheng's GPA. this is atest for chang sheng's GDP. this will be a test to see how well they can manage their GPA."), (9, 1717255869.4116726, 'txt', "This is a test for lidaifeng's EQ. this is a tests for lidetefeng's quality of life. i.e. it's a test to see if we can live up to our expectations."), (11, 1713275347.0590267, 'img', 'a laptop with a red heart on the screen'), (14, 1717255955.6176527, 'txt', "This is a test for yangbingquan's score. this is a Test for yingbingquans score."), (15, 1717256551.3271585, 'txt', "This is a test for zhoubohan's homework. this is atest for z houbohan’s homework. This is a Test for ZHoubohan.")]], [2, ['system', 'diagram', 'the'], [(11, 1713275347.0590267, 'img', 'a laptop with a red heart on the screen')]], [2, ['sheets', 'background', 'paper'], [(14, 1717255955.6176527, 'txt', "This is a test for yangbingquan's score. this is a Test for yingbingquans score.")]], [2, ['gpa', 'this', 'test'], [(9, 1717255869.4116726, 'txt', "This is a test for lidaifeng's EQ. this is a tests for lidetefeng's quality of life. i.e. it's a test to see if we can live up to our expectations.")]], [2, ['diestag', 'jacke', 'am'], [(15, 1717256551.3271585, 'txt', "This is a test for zhoubohan's homework. this is atest for z houbohan’s homework. This is a Test for ZHoubohan.")]], [2, ['shining', 'light', 'computer'], [(1, 1717255895.5607598, 'txt', "This is a test for changsheng's GPA. this is atest for chang sheng's GDP. this will be a test to see how well they can manage their GPA.")]], [1, ['he', 'to', 'if'], [(12, 1718022455.3495991, 'txt', "This is a test for shixufei's wis adel to see if he can do it. If he fails, he will be sent to prison.")]]]
  
CTree = CharacterTree()
CTree.build_tree(data)
CTree.traverse()
