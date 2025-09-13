#!/usr/bin/env python3
"""
Unit tests for signal processing operations.
"""

import unittest
import numpy as np
from signal_processing import SignalProcessor, create_test_signal


class TestSignalProcessing(unittest.TestCase):
    """Test cases for signal processing operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = SignalProcessor(sampling_rate=1000.0)
        self.t = np.linspace(0, 1, 100)
        self.signal = np.sin(2 * np.pi * 5 * self.t)  # 5 Hz sine wave
    
    def test_time_scale_compression(self):
        """Test time scaling with compression (scale_factor > 1)."""
        scaled_signal, scaled_time = self.processor.time_scale(self.signal, self.t, 2.0)
        
        # Check that the scaled signal is shorter in duration
        self.assertLess(scaled_time[-1], self.t[-1])
        
        # Check that the signal maintains its shape (approximately)
        self.assertAlmostEqual(np.max(scaled_signal), np.max(self.signal), places=1)
    
    def test_time_scale_expansion(self):
        """Test time scaling with expansion (scale_factor < 1)."""
        scaled_signal, scaled_time = self.processor.time_scale(self.signal, self.t, 0.5)
        
        # Check that the scaled signal is longer in duration
        self.assertGreater(scaled_time[-1], self.t[-1])
        
        # Check that the signal maintains its shape (approximately)
        self.assertAlmostEqual(np.max(scaled_signal), np.max(self.signal), places=1)
    
    def test_time_scale_no_change(self):
        """Test time scaling with no change (scale_factor = 1)."""
        scaled_signal, scaled_time = self.processor.time_scale(self.signal, self.t, 1.0)
        
        # Check that the signal is unchanged
        np.testing.assert_array_almost_equal(scaled_signal, self.signal, decimal=5)
        np.testing.assert_array_almost_equal(scaled_time, self.t, decimal=5)
    
    def test_time_scale_invalid_factor(self):
        """Test time scaling with invalid scale factor."""
        with self.assertRaises(ValueError):
            self.processor.time_scale(self.signal, self.t, -1.0)
        
        with self.assertRaises(ValueError):
            self.processor.time_scale(self.signal, self.t, 0.0)
    
    def test_time_shift_delay(self):
        """Test time shifting with delay (positive shift)."""
        shifted_signal, shifted_time = self.processor.time_shift(self.signal, self.t, 0.2)
        
        # Check that the time axis is shifted
        self.assertAlmostEqual(shifted_time[0], self.t[0] - 0.2, places=5)
        self.assertAlmostEqual(shifted_time[-1], self.t[-1] - 0.2, places=5)
    
    def test_time_shift_advance(self):
        """Test time shifting with advance (negative shift)."""
        shifted_signal, shifted_time = self.processor.time_shift(self.signal, self.t, -0.1)
        
        # Check that the time axis is shifted
        self.assertAlmostEqual(shifted_time[0], self.t[0] + 0.1, places=5)
        self.assertAlmostEqual(shifted_time[-1], self.t[-1] + 0.1, places=5)
    
    def test_time_shift_no_change(self):
        """Test time shifting with no change (shift = 0)."""
        shifted_signal, shifted_time = self.processor.time_shift(self.signal, self.t, 0.0)
        
        # Check that the signal is unchanged
        np.testing.assert_array_almost_equal(shifted_signal, self.signal, decimal=5)
        np.testing.assert_array_almost_equal(shifted_time, self.t, decimal=5)
    
    def test_time_reverse(self):
        """Test time reversal."""
        reversed_signal, reversed_time = self.processor.time_reverse(self.signal, self.t)
        
        # Check that the signal is reversed
        np.testing.assert_array_almost_equal(reversed_signal, np.flip(self.signal), decimal=5)
        
        # Check that the time axis is properly reversed
        expected_reversed_time = np.flip(-self.t)
        np.testing.assert_array_almost_equal(reversed_time, expected_reversed_time, decimal=5)
    
    def test_discrete_time_scale_compression(self):
        """Test discrete time scaling with compression."""
        discrete_signal = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1])
        scaled = self.processor.discrete_time_scale(discrete_signal, 2.0)
        
        # Check that the scaled signal is shorter
        self.assertLess(len(scaled), len(discrete_signal))
        
        # Check that it's a decimation (every other sample)
        expected = discrete_signal[::2]
        np.testing.assert_array_equal(scaled, expected)
    
    def test_discrete_time_scale_expansion(self):
        """Test discrete time scaling with expansion."""
        discrete_signal = np.array([1, 2, 3])
        scaled = self.processor.discrete_time_scale(discrete_signal, 0.5)
        
        # Check that the scaled signal is longer
        self.assertGreater(len(scaled), len(discrete_signal))
        
        # Check that it's a repetition (each sample repeated)
        expected = np.repeat(discrete_signal, 2)
        np.testing.assert_array_equal(scaled, expected)
    
    def test_discrete_time_shift_delay(self):
        """Test discrete time shifting with delay."""
        discrete_signal = np.array([1, 2, 3, 4, 5])
        shifted = self.processor.discrete_time_shift(discrete_signal, 2)
        
        # Check that the signal is padded with zeros at the beginning
        expected = np.array([0, 0, 1, 2, 3, 4, 5])
        np.testing.assert_array_equal(shifted, expected)
    
    def test_discrete_time_shift_advance(self):
        """Test discrete time shifting with advance."""
        discrete_signal = np.array([1, 2, 3, 4, 5])
        shifted = self.processor.discrete_time_shift(discrete_signal, -2)
        
        # Check that the signal has samples removed from the beginning
        expected = np.array([3, 4, 5])
        np.testing.assert_array_equal(shifted, expected)
    
    def test_discrete_time_reverse(self):
        """Test discrete time reversal."""
        discrete_signal = np.array([1, 2, 3, 4, 5])
        reversed_signal = self.processor.discrete_time_reverse(discrete_signal)
        
        # Check that the signal is reversed
        expected = np.array([5, 4, 3, 2, 1])
        np.testing.assert_array_equal(reversed_signal, expected)
    
    def test_create_test_signal(self):
        """Test the test signal creation function."""
        t, signal = create_test_signal(duration=1.0, sampling_rate=100.0)
        
        # Check that the time axis has the correct length
        expected_length = int(1.0 * 100.0)
        self.assertEqual(len(t), expected_length)
        self.assertEqual(len(signal), expected_length)
        
        # Check that the time axis is properly spaced
        self.assertAlmostEqual(t[0], 0.0, places=5)
        self.assertAlmostEqual(t[-1], 1.0, places=5)
        
        # Check that the signal has reasonable values
        self.assertGreater(np.max(signal), 0)
        self.assertLess(np.min(signal), 0)


if __name__ == '__main__':
    unittest.main()