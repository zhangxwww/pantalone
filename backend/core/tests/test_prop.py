import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.libs.math.prob import standard_normal_prob


class TestStandardNormalProb(unittest.TestCase):

    def test_standard_normal_prob(self):
        self.assertAlmostEqual(standard_normal_prob(0), 0.5, places=5)
        self.assertAlmostEqual(standard_normal_prob(1.96), 0.025, places=5)
        self.assertAlmostEqual(standard_normal_prob(-1.96), 0.975, places=5)
        self.assertAlmostEqual(standard_normal_prob(3), 0.00135, places=5)
        self.assertAlmostEqual(standard_normal_prob(-3), 0.99865, places=5)
