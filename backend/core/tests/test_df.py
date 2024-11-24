import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.libs.df import cut_by_window, percentile, resample

class TestDF(unittest.TestCase):

    def setUp(self):
        self.data = {
            'date': pd.date_range(start='2022-01-01', periods=1000, freq='D'),
            'value': range(1000)
        }
        self.df = pd.DataFrame(self.data)
        self.df['date'] = self.df['date'].dt.date

    def test_cut_by_window_year(self):
        filtered_df = cut_by_window(self.df, 1, 'year')
        expected_start_date = pd.Timestamp.now() - pd.DateOffset(years=1)
        self.assertTrue((filtered_df['date'] >= expected_start_date.date()).all())

    def test_cut_by_window_month(self):
        filtered_df = cut_by_window(self.df, 1, 'month')
        expected_start_date = pd.Timestamp.now() - pd.DateOffset(months=1)
        self.assertTrue((filtered_df['date'] >= expected_start_date.date()).all())

    def test_cut_by_window_day(self):
        filtered_df = cut_by_window(self.df, 10, 'day')
        expected_start_date = pd.Timestamp.now() - pd.DateOffset(days=10)
        self.assertTrue((filtered_df['date'] >= expected_start_date.date()).all())

    def test_cut_by_window_no_filter(self):
        filtered_df = cut_by_window(self.df, -1)
        self.assertTrue(filtered_df.equals(self.df))

    def test_percentile(self):
        percentile_value = percentile(self.df)
        last_value = self.df['value'].iloc[-1]
        expected_percentile = (self.df['value'] < last_value).sum() / self.df.shape[0] * 100
        self.assertAlmostEqual(percentile_value, expected_percentile, places=5)

    def test_resample_daily(self):
        resampled_df = resample(self.df, 'daily')
        self.assertTrue(resampled_df.equals(self.df))

    def test_resample_weekly(self):
        resampled_df = resample(self.df, 'weekly')
        self.assertEqual(resampled_df.shape[0], 1000 // 7 + 2)
        self.assertTrue((resampled_df['date'] == resampled_df['date'].sort_values()).all())

    def test_resample_monthly(self):
        resampled_df = resample(self.df, 'monthly')
        self.assertEqual(resampled_df.shape[0], 33)
        self.assertTrue((resampled_df['date'] == resampled_df['date'].sort_values()).all())
