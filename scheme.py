import operator

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
    def __init__(self, op):
        self.op = op

    def apply(self, operands):
        value = operands[0]
        for operand in operands[1:]:
            value = self.op(value, operand)
        return value

class OperatorFactory(object):
    @staticmethod
    def make_operator(token):
        if token == "*":
            return Operator(operator.mul)
        elif token == "/":
            try: 
                return Operator(operator.div)
            except AttributeError:
                ## Handle python3
                return Operator(operator.truediv) 
        elif token == "+":
            return Operator(operator.add)
        elif token == "-":
            return Operator(operator.sub)
        else:
            ## Unknown operator: user error?
            raise Exception("Unknown operator: %s" % token)
            

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
            return OperatorFactory.make_operator(token)
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
            
class Evaluator(object):
    @staticmethod
    def evaluate(parse_tree):
        if type(parse_tree) is list:
            if type(parse_tree[0]) is Operator:
                results = [ Evaluator.evaluate(i) for i in parse_tree[1:] ]
                return parse_tree[0].apply(results)
        elif type(parse_tree) is Number:
            return parse_tree.value
