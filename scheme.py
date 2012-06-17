
class Tokenizer(object):
    @staticmethod
    def tokenize(string):
        # Isolate the parentheses make the separate tokens with split()
        string = string.replace("(", " ( ")
        string = string.replace(")", " ) ")
        tokens = string.split()
        return tokens

class Symbol(object):
    def __init__(self, token):
        self.token = token

class Operator(object):
    pass

class Number(object):
    def __init__(self, token):
        self.value = token

class Parser(object):
    @staticmethod 
    def parse(tokens):
        tree = []
        for t in tokens:
            if t != "(" and t != ")":
                tree.append(Parser.make_expression(t))
        return tree

    @staticmethod
    def make_expression(token):
        if token == "*":
            return Operator()
        elif Parser.is_number(token):
            return Number(token)
        else:
            return Symbol(token)
        
        
    @staticmethod
    def is_number(token):
        try:
            float(token)
            return True
        except:
            return False
            
