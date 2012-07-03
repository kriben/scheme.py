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

    def apply(self, operands, environment):
        value = operands[0]
        for operand in operands[1:]:
            value = self.op(value, operand)
        return value

class AssignmentOperator(object):
    def apply(self, tokens, environment):
        assert(type(tokens[0]) == Symbol)
        environment.set(tokens[0].token, tokens[1])


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
        elif token == "set!":
            return AssignmentOperator()
        else:
            ## Unknown operator: user error?
            raise Exception("Unknown operator: %s" % token)
            

class Number(object):
    def __init__(self, token):
        self.value = token

class Parser(object):
    @staticmethod 
    def parse(tokens):
        t = tokens.pop(0)
        if t == "(": 
            tree = []
            while tokens[0] != ")":
                tree.append(Parser.parse(tokens)) 
            tokens.pop(0)
            return tree
        else:
            return Parser.make_expression(t)


    @staticmethod
    def make_expression(token):
        try:
            return OperatorFactory.make_operator(token)
        except:
            if Parser.is_number(token):
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
    def evaluate(parse_tree, environment = None):
        if type(parse_tree) is list:
            if type(parse_tree[0]) is Operator:
                results = [ Evaluator.evaluate(i, environment) for i in parse_tree[1:] ]
                return parse_tree[0].apply(results, environment)
            elif type(parse_tree[0]) is AssignmentOperator:
                # TODO: handle more than variable:value pair
                parse_tree[0].apply([parse_tree[1], Evaluator.evaluate(parse_tree[2], environment)], environment )
        elif type(parse_tree) is Number:
            return parse_tree.value
        elif type(parse_tree) is Symbol:
            return environment.get(parse_tree.token)

class Environment(object):
    def __init__(self):
        self.variables = {}

    def get(self, variable):
        if variable in self.variables:
            return self.variables[variable]
        else:
            raise Exception("Unbound variable: %s" % variable)

    def set(self, variable, value):
        self.variables[variable] = value
