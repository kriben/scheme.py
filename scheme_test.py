#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest
from scheme import Tokenizer


class TestTokenizer(unittest.TestCase):
    def test_can_tokenize_simple_string(self):
        tokens = Tokenizer.tokenize("(* a b)")
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens, ["(", "*", "a", "b", ")"])
                         
    def test_can_tokenize_strange_string(self):
        tokens = Tokenizer.tokenize("  (+(a)  (b) c)  ")
        self.assertEqual(len(tokens), 10)
        self.assertEqual(tokens, ["(", "+", "(", "a", ")", "(", "b", ")", "c", ")"])


if __name__ == '__main__':
    unittest.main()
