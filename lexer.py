"""
Eric Bridgeford, Caroline Danzi, Julius Ware
CSE 474 Compiler Design
Dr. Karro

This program takes in a source code file and a file describing legal tokens
in the language, and returns a generator that parses the source code and
yields each token.

We researched some Python syntax in the Python documentation.
"""

import re
import sys

class LexerError(Exception):
    """
    Exception to be thrown when the lexer encounters a bad token.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

class Token:
    """
    A class for storing token information.
    The variable instances for a token object are:
    * t_class: The token class.
    * name: The name of the token.
    * pattern: The specific pattern of the token
    * line: The line containing the token
    * line_num: The line number (numbered from 1)
    * col: The column number (numbered from 0)
    """

    def __init__(self, t_class, name, pattern, line, line_num, col):
        """
        Constructor
        """
        self.t_class = t_class
        self.name = name
        self.pattern = pattern
        self.line = line
        self.line_num = int(line_num)
        self.col = int(col)

    def __str__(self):
        """
        Defines behavior of the str function on the Token class.
        Prints as a tupple all information except self.line.
        """
        return str((self.t_class, self.name, self.pattern, self.line_num, self.col))

    def __repr__(self):
        """
        Defines the behaviour of the repr() function
        on the Token class.
        """
        return "Token: " + str(self)

    def __eq__(self, other):
        """
        Defines behaviour of the == operator on the Token class
        """
        return self.t_class == other.t_class and self.name == other.name and \
               self.pattern == other.pattern and self.line == other.line and \
               self.line_num == other.line_num and self.col == other.col


def lexer(source_file, token_file):
    """
    Input:
    * source_file: file containing the content to be tokenized
    * token_file: token file (see assignment specifications for format)
    Output:
    * A generator that will iteratively return token objects corresponding to the tokens
      of source_file, throwing a LexerError if it hits a bad token.
    """
    lines = sourceParser(source_file)
    tokenTypes = tokenParser(token_file)

    # for each original line in the source file, strip off the leading and
    # trailing whitespace, and remove any comments
    for lineNum, origLine in enumerate(lines):
        line = str.strip(origLine)
        line = re.sub("#(.|\s)*$", "", line)

        # as long as there are tokens in the line, the line will be longer than zero
        while len(line) > 0:
            # for each type of token in the list, try to match the first part of the line
            for tokenType in tokenTypes:

                # search for the pattern starting at the beginning of the line
                r = re.search("^" + tokenType[2], line)

                # if we find a match, build and yield the token object
                if r != None:
                    token = Token(tokenType[0], tokenType[1], r.group(1), origLine.strip(), lineNum+1, origLine.find(line))
                    yield token
                    # remove the part that matched (with any whitespace)
                    tokLength = len(r.group(1))
                    line = str.strip(line[tokLength:])
                    break

                elif tokenType == tokenTypes[len(tokenTypes)-1]:
                    err = LexerError("Bad token found on line "+ str(lineNum+1)+ " col "+str(origLine.find(line)))
                    raise(err)

def tokenParser(token_file):
    """
    Input: a file that lists the class, name, and regular expression
    for each token in the language
    Output: a nested list of the form [[class, name, regex], [...], ...]
    with each token in its own list
    """

    tokens = open(token_file, 'r')
    lst = []

    for line in tokens.readlines():
        # strip out all whitespace
        tempLst = re.split("\s+", str.rstrip(line))
        lst.append(tempLst)

    return lst

def sourceParser(source_file):
    """
    Input: a source code file
    Output: a list of the lines in the source code
    in the form [line1, line2, ... ]
    """

    source = open(source_file, 'r')
    lst = []

    for line in source.readlines():
        lst.append(line)

    return lst
