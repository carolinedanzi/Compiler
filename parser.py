"""
Caroline Danzi
This is a Parser for the language described by the grammar below.
It takes as input a source code file written in the language, and
a token file that describes the legal tokens in the language.

17-5-2016
"""

from tree import *
from lexer import *

class Parser:

    def __init__(self, source, tokens):
        G = lexer(source, tokens)

    def parse(self):
        current, t = block(next(G), G)
        return t

    def block(self, current, G):
        pass
    
