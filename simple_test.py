#!/usr/bin/env python3
"""
Simple tests for signal processing operations.
"""

import math
from simple_signal_demo import (
    create_simple_signal, time_scale, time_shift, time_reverse,
    discrete_time_scale, discrete_time_shift, discrete_time_reverse
)


def test_time_scale():
    """Test time scaling functionality."""
    print("Testing time scaling...")
    
    # Create a simple sine wave
    t = [0, 0.1, 0.2, 0.3, 0.4]
    signal = [math.sin(2 * math.pi * 5 * ti) for ti in t]  # 5 Hz sine wave
    
    # Test compression (2x faster)
    scaled_signal, scaled_time = time_scale(signal, t, 2.0)
    assert len(scaled_signal) == len(signal), "Length should be preserved"
    assert scaled_time[-1] < t[-1], "Compressed signal should be shorter in duration"
    print("  ✓ Compression test passed")
    
    # Test expansion (0.5x slower)
    scaled_signal, scaled_time = time_scale(signal, t, 0.5)
    assert len(scaled_signal) == len(signal), "Length should be preserved"
    assert scaled_time[-1] > t[-1], "Expanded signal should be longer in duration"
    print("  ✓ Expansion test passed")
    
    # Test no change
    scaled_signal, scaled_time = time_scale(signal, t, 1.0)
    # Use approximate equality due to floating point precision
    assert all(abs(s1 - s2) < 1e-10 for s1, s2 in zip(scaled_signal, signal)), "Signal should be unchanged with scale factor 1"
    print("  ✓ No change test passed")


def test_time_shift():
    """Test time shifting functionality."""
    print("Testing time shifting...")
    
    t = [0, 0.1, 0.2, 0.3, 0.4]
    signal = [1, 2, 3, 4, 5]
    
    # Test delay
    shifted_signal, shifted_time = time_shift(signal, t, 0.1)
    assert len(shifted_signal) == len(signal), "Length should be preserved"
    assert shifted_time[0] == t[0] - 0.1, "Time axis should be shifted"
    print("  ✓ Delay test passed")
    
    # Test advance
    shifted_signal, shifted_time = time_shift(signal, t, -0.1)
    assert len(shifted_signal) == len(signal), "Length should be preserved"
    assert shifted_time[0] == t[0] + 0.1, "Time axis should be shifted"
    print("  ✓ Advance test passed")
    
    # Test no change
    shifted_signal, shifted_time = time_shift(signal, t, 0.0)
    # Use approximate equality due to floating point precision
    assert all(abs(s1 - s2) < 1e-10 for s1, s2 in zip(shifted_signal, signal)), "Signal should be unchanged with shift 0"
    print("  ✓ No change test passed")


def test_time_reverse():
    """Test time reversal functionality."""
    print("Testing time reversal...")
    
    t = [0, 0.1, 0.2, 0.3, 0.4]
    signal = [1, 2, 3, 4, 5]
    
    reversed_signal, reversed_time = time_reverse(signal, t)
    
    # Check signal reversal
    assert reversed_signal == [5, 4, 3, 2, 1], "Signal should be reversed"
    print("  ✓ Signal reversal test passed")
    
    # Check time axis reversal
    expected_time = [-0.4, -0.3, -0.2, -0.1, 0.0]
    assert reversed_time == expected_time, "Time axis should be reversed and negated"
    print("  ✓ Time axis reversal test passed")


def test_discrete_operations():
    """Test discrete signal operations."""
    print("Testing discrete operations...")
    
    signal = [1, 2, 3, 4, 5]
    
    # Test discrete time scaling
    scaled = discrete_time_scale(signal, 2.0)
    assert scaled == [1, 3, 5], "Discrete scaling should decimate"
    print("  ✓ Discrete scaling test passed")
    
    # Test discrete time shifting
    shifted = discrete_time_shift(signal, 2)
    assert shifted == [0, 0, 1, 2, 3, 4, 5], "Discrete shifting should pad with zeros"
    print("  ✓ Discrete shifting test passed")
    
    # Test discrete time reversal
    reversed_signal = discrete_time_reverse(signal)
    assert reversed_signal == [5, 4, 3, 2, 1], "Discrete reversal should reverse the signal"
    print("  ✓ Discrete reversal test passed")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    signal = [1, 2, 3, 4, 5]
    t = [0, 0.1, 0.2, 0.3, 0.4]
    
    # Test invalid scale factor
    try:
        time_scale(signal, t, -1.0)
        assert False, "Should raise ValueError for negative scale factor"
    except ValueError:
        print("  ✓ Negative scale factor error handling passed")
    
    try:
        time_scale(signal, t, 0.0)
        assert False, "Should raise ValueError for zero scale factor"
    except ValueError:
        print("  ✓ Zero scale factor error handling passed")
    
    # Test discrete operations
    try:
        discrete_time_scale(signal, -1.0)
        assert False, "Should raise ValueError for negative scale factor"
    except ValueError:
        print("  ✓ Discrete negative scale factor error handling passed")


def run_all_tests():
    """Run all tests."""
    print("Running Signal Processing Tests")
    print("=" * 40)
    
    try:
        test_time_scale()
        test_time_shift()
        test_time_reverse()
        test_discrete_operations()
        test_error_handling()
        
        print("\n" + "=" * 40)
        print("ALL TESTS PASSED! ✓")
        print("=" * 40)
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()