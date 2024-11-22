import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scipy.stats import chi2, t, norm

from src.libs.math.interval import chi2_interval, t_interval, normal_interval


class TestIntervalFunctions(unittest.TestCase):
    # https://zhuanlan.zhihu.com/p/540037437

    def test_chi2_interval(self):
        p = 0.95
        df = 10
        expected = (chi2.ppf((1 - p) / 2, df), chi2.ppf((1 + p) / 2, df))
        result = chi2_interval(p, df)
        self.assertAlmostEqual(result[0], expected[0], places=5)
        self.assertAlmostEqual(result[1], expected[1], places=5)

    def test_t_interval(self):
        p = 0.95
        df = 10
        expected = (t.ppf((1 - p) / 2, df), t.ppf((1 + p) / 2, df))
        result = t_interval(p, df)
        self.assertAlmostEqual(result[0], expected[0], places=5)
        self.assertAlmostEqual(result[1], expected[1], places=5)

    def test_normal_interval(self):
        p = 0.95
        expected = (norm.ppf((1 - p) / 2), norm.ppf((1 + p) / 2))
        result = normal_interval(p)
        self.assertAlmostEqual(result[0], expected[0], places=5)
        self.assertAlmostEqual(result[1], expected[1], places=5)
