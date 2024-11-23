import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from src.libs.math.estimation import estimate_normal_distribution


class TestEstimationFunctions(unittest.TestCase):

    def test_estimate_normal_distribution(self):
        mu, sigma = 3, 1
        data = np.random.normal(mu, sigma, 100000)
        result = estimate_normal_distribution(data)
        self.assertAlmostEqual(result[0], mu, places=2)
        self.assertAlmostEqual(result[1], sigma, places=2)
