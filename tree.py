import re

class tree:
    """
    Tree class, where a tree is a label
    with zero or more trees as children
    """

    def __init__(self, label, children = None, token = None):
        """
        Tree constructor
        """
        self.label = label
        self.children = children if children != None else []
        self.token = token

    def _str_helper(self):

        return self.label if not self.children \
            else "(" + ",".join([c._str_helper() for c in self.children]) + ")" + self.label

    def __str__(self):
        """
        Translate to newick string
        """
        return self._str_helper() + ";"


    def __repr__(self):
        return "Tree: " + str(self)

    def __len__(self):
        """
        Return number of nodes in teee
        """
        return sum(len(node) for node in self.children) + 1

    def isLeaf(self):
        """
        Return true/false indicating whether
        the tree is a leaf
        """
        return len(self.children) == 0



class ParserException(Exception):
    """
    Exception class for parse_newick
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg



# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing.
# * Expected label missing.
# * Missing command or ) where expected.
# (You may add others as you see fit.)
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.
def parse_newick(s):
    """
    Take a newick string and return the corresponding tree object.
    """
    G = lexer(s)
    current, t = T(next(G), G)
    return t

def lexer(s):
    for c in re.sub("\s+", "", s):
        yield c
    yield '$'

def T(current, G):
    current, t = S(current, G)
    if current != ";":
        raise ParserException("Missing semi-column at the end ")
    current = next(G)
    if current != "$":
        raise ParserException("Garbage after semi-column at the end.")
    return current, t

def S(current, G):
    children = []
    if current == '(':
        while current != ")":
            current, child = S(next(G), G)
            children.append(child)
            if current not in (",", ")"):
                raise ParserException("Error in S: missing closing parenthesis or wrong token")
        current = next(G)
    label = ""
    while re.match("\w", current):
        label += current
        current = next(G)
    if not label:
        raise ParserException("Missing label for leaf nodes")
    return current, tree(label, children)