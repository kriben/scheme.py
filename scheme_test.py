#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest
from scheme import Tokenizer, Parser, Evaluator

from scheme import Operator, Symbol, Number


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

class TestEvaluator(unittest.TestCase):
    def test_can_evaluate_simple_multiplication(self):
        parse_tree = [ Operator(), Number(2.0), Number(3.0) ]
        result = Evaluator.evaluate(parse_tree)
        self.assertEqual(result, 6.0)


if __name__ == '__main__':
    unittest.main()
