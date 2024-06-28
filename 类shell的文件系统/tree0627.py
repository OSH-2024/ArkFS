import update0626

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

class CharacterTree:
    def __init__(self):
        self.root = TreeNode([""])
    
    def build_tree(self, data):
        lines = data.strip().split('\n')
        stack = []
        cur_level = 1
        for line in lines:
            if line.startswith("Level"):
                level = int(line.split(" ")[1])
                representative_words = line.split("(Representative words: ")[1].split(")")[0].split(", ")
                new_node = TreeNode(representative_words)
                while level < len(stack) + 1:
                    stack.pop()
                

data = """Level 1 Cluster 0 (Representative words: several, dots, network):
  - a computer tower with a blue light shining on it (Index: 0)
  - a diagram of the system (Index: 2)
  - a diagram of a network with several dots (Index: 8)
  - the new interface in the new interface editor (Index: 13)

Level 2 Cluster 0 (Representative words: network, several, dots):
  - a diagram of a network with several dots (Index: 2)

Level 2 Cluster 1 (Representative words: new, interface, the):
  - the new interface in the new interface editor (Index: 3)

Level 2 Cluster 2 (Representative words: blue, tower, computer):
  - a computer tower with a blue light shining on it (Index: 0)

Level 2 Cluster 3 (Representative words: system, the, diagram):
  - a diagram of the system (Index: 1)

Level 1 Cluster 1 (Representative words: you, iq, this):
  - This is a test for liumingle's IQ. If you think you have a high IQ, try this test. (Index: 10)

Level 1 Cluster 2 (Representative words: ich, vater, schuhe):
  - a pile of paper sheets with a blue background (Index: 3)
  - "Ich muss eine neue Jacke für das Jobinterview am Diestag kaufen" (Index: 4)
  - "Ich brauche die Jeans für meinen Vater, und ich muss einen neue schuhe kaufen" (Index: 5)
  - "Ich brauche die Jeans nicht. Ich brauches die jeans nicht" - Jürgen Schubert. Schulder: "Ich habe ein gutes Leben." (Index: 6)
  - "Wir brauchen der stuhl nicht, denn wir haben drei Stühle" (Index: 7)

Level 2 Cluster 0 (Representative words: ich, vater, und):
  - "Ich brauche die Jeans für meinen Vater, und ich muss einen neue schuhe kaufen" (Index: 2)

Level 2 Cluster 1 (Representative words: am, diestag, jacke):
  - "Ich muss eine neue Jacke für das Jobinterview am Diestag kaufen" (Index: 1)

Level 2 Cluster 2 (Representative words: with, sheets, of):
  - a pile of paper sheets with a blue background (Index: 0)

Level 2 Cluster 3 (Representative words: wir, der, drei):
  - "Wir brauchen der stuhl nicht, denn wir haben drei Stühle" (Index: 4)

Level 2 Cluster 4 (Representative words: ich, nicht, jeans):
  - "Ich brauche die Jeans nicht. Ich brauches die jeans nicht" - Jürgen Schubert. Schulder: "Ich habe ein gutes Leben." (Index: 3)

Level 1 Cluster 3 (Representative words: score, this, test):
  - This is a test for changsheng's GPA. this is atest for chang sheng's GDP. this will be a test to see how well they can manage their GPA. (Index: 1)
  - This is a test for lidaifeng's EQ. this is a tests for lidetefeng's quality of life. i.e. it's a test to see if we can live up to our expectations. (Index: 9)   
  - a laptop with a red heart on the screen (Index: 11)
  - This is a test for yangbingquan's score. this is a Test for yingbingquans score. (Index: 14)
  - This is a test for zhoubohan's homework. this is atest for z houbohan’s homework. This is a Test for ZHoubohan. (Index: 15)

Level 2 Cluster 0 (Representative words: heart, with, laptop):
  - a laptop with a red heart on the screen (Index: 2)

Level 2 Cluster 1 (Representative words: score, is, this):
  - This is a test for yangbingquan's score. this is a Test for yingbingquans score. (Index: 3)

Level 2 Cluster 2 (Representative words: to, is, test):
  - This is a test for lidaifeng's EQ. this is a tests for lidetefeng's quality of life. i.e. it's a test to see if we can live up to our expectations. (Index: 1)   

Level 2 Cluster 3 (Representative words: zhoubohan, homework, this):
  - This is a test for zhoubohan's homework. this is atest for z houbohan’s homework. This is a Test for ZHoubohan. (Index: 4)

Level 2 Cluster 4 (Representative words: gpa, this, test):
  - This is a test for changsheng's GPA. this is atest for chang sheng's GDP. this will be a test to see how well they can manage their GPA. (Index: 0)

Level 1 Cluster 4 (Representative words: he, to, if):
  - This is a test for shixufei's wis adel to see if he can do it. If he fails, he will be sent to prison. (Index: 12)"""

forest = build_forest(data)
for tree in forest:
    print(tree)
