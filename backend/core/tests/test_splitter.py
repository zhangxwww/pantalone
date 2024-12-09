import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.text_splitter.simple_splitter import SimpleSplitter


class TestSplitter(unittest.TestCase):
    def setUp(self):
        self.splitter = SimpleSplitter(max_tokens=10, max_overlap=8, split_tokens=['。', '\n'])

    def test_split_1(self):
        text = 'abcdefghijklnmopqrstuvwxyz。\nAB\n1234567890987654321\nc。d\ne\n123。4567。890。123。456。7890。12。3'
        chunks = self.splitter.split(text)
        self.assertEqual(len(chunks), 9)
        self.assertEqual(chunks[0], 'abcdefghij')
        self.assertEqual(chunks[1], 'AB')
        self.assertEqual(chunks[2], '1234567890')
        self.assertEqual(chunks[3], 'cde1234567')
        self.assertEqual(chunks[4], '1234567890')
        self.assertEqual(chunks[5], '4567890123')
        self.assertEqual(chunks[6], '890123456')
        self.assertEqual(chunks[7], '1234567890')
        self.assertEqual(chunks[8], '4567890123')

    def test_split_2(self):
        text_list = [ 'hello', 'world', 'this', 'is', 'a', 'test', 'for', 'text', 'concatenation', 'function', 'in', 'python', 'programming', 'language', 'and', 'this', 'is', 'a', 'test', 'for', 'text', 'concatenation', 'function', 'concatenationconcatenation', 'in', 'python', 'programming', 'language', 'and', 'hello', 'world', 'this', ]
        text = '\n'.join(text_list)
        self.splitter.split(text)
