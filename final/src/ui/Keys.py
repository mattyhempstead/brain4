class Node:
    def __init__(self, alpha_key, punc_key, autocomplete=None):
        self.alpha_key = alpha_key
        self.punc_key = punc_key
        self.autocomplete = autocomplete

        self.left = None
        self.right = None
        self.parent = None

        self.height = None
        self.width = None

        self.leaf = False
        self.root = False

        self.rect = None

    def printKey(self):
        print(self.key)

    def is_leaf(self):
        return self.leaf

    def is_root(self):
        return self.root


class Keys:
    def __init__(self):
        self.root = None

    def init_trees(self):
        alpha_ls = ['E','T','A','I','O','N','S','H','R','B','C','D','F','G','Delete','J','K','L','M','P','Q','U','V','W','X','Y','Z','Space','123','U/L','Clear']
        punc_ls = ['.',0,',',1,2,':',';',3,4,5,'/','?','!','\'','\"',6,7,8,9,'@','&','-','_','(',')','[',']','Space','abc','Delete','Clear']

        self.root = Node(alpha_ls[0], punc_ls[0])
        self.root.root = True
        tmp = [self.root]

        for i in range(1,len(alpha_ls)):
            new = Node(alpha_ls[i], str(punc_ls[i]))
            if i < 15:
                tmp.append(new)
            else:
                # new.leaf = True
                new_autocomplete = Node(alpha_key=None, punc_key=None, autocomplete="")
                new_autocomplete.leaf = True
                new_autocomplete.parent = new
                new.left = new_autocomplete
                new.right = new_autocomplete
            cur = tmp[0]
            if cur.left is None:
                cur.left = new
                new.parent = cur
            elif cur.right is None:
                cur.right = new
                new.parent = cur
                tmp.pop(0)


def dfs(node):
    print(node.key, end=" ")
    if node.is_leaf:
        return

    dfs(node.left)
    dfs(node.right)

