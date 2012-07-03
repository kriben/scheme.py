#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest

from scheme import Tokenizer, Parser, Evaluator
from scheme import Operator, OperatorFactory, Symbol, Number, Environment


class TestTokenizer(unittest.TestCase):
    def test_can_tokenize_simple_string(self):
        tokens = Tokenizer.tokenize("(* a b)")
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens, ["(", "*", "a", "b", ")"])
                         
    def test_can_tokenize_strange_string(self):
        tokens = Tokenizer.tokenize("  (+(a)  (b) c)  ")
        self.assertEqual(len(tokens), 10)
        self.assertEqual(tokens, ["(", "+", "(", "a", ")", "(", "b", ")", "c", ")"])

class TestParser(unittest.TestCase):
    def test_can_parse_simple_tokens(self):
        tokens = ["(", "*", "a", "b", ")"]
        parse_tree = Parser.parse(tokens)
        self.assertEqual(type(parse_tree), list)
        self.assertEqual(len(parse_tree), 3)
        self.assertEqual(type(parse_tree[0]), Operator) 
        self.assertEqual(type(parse_tree[1]), Symbol) 
        self.assertEqual(type(parse_tree[2]), Symbol) 
        
    def test_can_parse_floating_point_numbers(self):
        tokens = ["(", "3.14", ")"]
        parse_tree = Parser.parse(tokens)
        self.assertEqual(len(parse_tree), 1)
        self.assertEqual(type(parse_tree[0]), Number) 

    def test_can_parse_nested_expression(self):
        tokens = ["(", "+", "2.3", "(", "*", "4.5", "3", ")", ")"]
        parse_tree = Parser.parse(tokens)
        self.assertEqual(len(parse_tree), 3)
        self.assertEqual(type(parse_tree[0]), Operator) 
        self.assertEqual(type(parse_tree[1]), Number) 
        self.assertEqual(type(parse_tree[2]), list)
        self.assertEqual(len(parse_tree[2]), 3)
        self.assertEqual(type(parse_tree[2][0]), Operator)

class TestEnvironment(unittest.TestCase):
    def test_throws_exception_when_getting_unbound(self):
        env = Environment()
        with self.assertRaises(Exception) as context:
            env.get("a")
        self.assertEqual(str(context.exception), 'Unbound variable: a')

        with self.assertRaises(Exception) as context:
            env.get("b")
        self.assertEqual(str(context.exception), 'Unbound variable: b')

    def test_getting_and_setting_variable(self):
        env = Environment()
        value = 2.3
        env.set("a", value)
        self.assertEqual(value, env.get("a"))


class TestEvaluator(unittest.TestCase):
    def test_can_evaluate_simple_multiplication(self):
        parse_tree = [ OperatorFactory.make_operator("*"), Number(2.0), Number(3.0) ]
        result = Evaluator.evaluate(parse_tree)
        self.assertEqual(result, 6.0)

    def test_can_evaluate_simple_addition(self):
        parse_tree = [ OperatorFactory.make_operator("+"), Number(2.0), Number(3.0) ]
        result = Evaluator.evaluate(parse_tree)
        self.assertEqual(result, 5.0)

    def test_can_evaluate_simple_division(self):
        parse_tree = [ OperatorFactory.make_operator("/"), Number(8.0), Number(2.0) ]
        result = Evaluator.evaluate(parse_tree)
        self.assertEqual(result, 4.0)

    def test_can_evaluate_simple_subtraction(self):
        parse_tree = [ OperatorFactory.make_operator("-"), Number(8.0), Number(4.0), Number(1.0) ]
        result = Evaluator.evaluate(parse_tree)
        self.assertEqual(result, 3.0)

    def test_raises_exception_on_unknown_operator(self):
        with self.assertRaises(Exception) as context:
            OperatorFactory.make_operator("#")
        self.assertEqual(str(context.exception), 'Unknown operator: #')

    def test_can_handle_nested_arithmetic(self):
        parse_tree = [ OperatorFactory.make_operator("*"), 
                       Number(2.0), 
                       [ OperatorFactory.make_operator("+"), Number(4.0), Number(5.0) ] ]
        result = Evaluator.evaluate(parse_tree)
        self.assertEqual(result, 18.0)

    def test_can_lookup_variable_from_the_environment(self):
        env = Environment()
        env.set("a", 2.0)
        env.set("b", 3.0)
        parse_tree = [ OperatorFactory.make_operator("*"), Symbol("a"), Symbol("b") ]
        result = Evaluator.evaluate(parse_tree, env)
        self.assertEqual(result, 6.0)

if __name__ == '__main__':
    unittest.main()
