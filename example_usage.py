#!/usr/bin/env python3
"""
Simple example demonstrating time operations on signals.
"""

import numpy as np
import matplotlib.pyplot as plt
from signal_processing import SignalProcessor, create_test_signal


def simple_example():
    """
    A simple example showing basic usage of time operations.
    """
    print("Simple Signal Processing Example")
    print("=" * 35)
    
    # Create a simple test signal
    t = np.linspace(0, 2, 200)
    signal = np.sin(2 * np.pi * 3 * t) + 0.5 * np.sin(2 * np.pi * 7 * t)
    
    # Initialize processor
    processor = SignalProcessor()
    
    # Time scaling: make signal 2x faster
    print("\n1. Time Scaling (2x faster):")
    scaled_signal, scaled_time = processor.time_scale(signal, t, 2.0)
    print(f"   Original duration: {t[-1]:.2f}s")
    print(f"   Scaled duration: {scaled_time[-1]:.2f}s")
    
    # Time shifting: delay by 0.5 seconds
    print("\n2. Time Shifting (delay by 0.5s):")
    shifted_signal, shifted_time = processor.time_shift(signal, t, 0.5)
    print(f"   Original start time: {t[0]:.2f}s")
    print(f"   Shifted start time: {shifted_time[0]:.2f}s")
    
    # Time reversal
    print("\n3. Time Reversal:")
    reversed_signal, reversed_time = processor.time_reverse(signal, t)
    print(f"   Original time range: [{t[0]:.2f}, {t[-1]:.2f}]s")
    print(f"   Reversed time range: [{reversed_time[0]:.2f}, {reversed_time[-1]:.2f}]s")
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Original signal
    plt.subplot(2, 2, 1)
    plt.plot(t, signal, 'b-', linewidth=2)
    plt.title('Original Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # Time scaled signal
    plt.subplot(2, 2, 2)
    plt.plot(scaled_time, scaled_signal, 'r-', linewidth=2)
    plt.title('Time Scaled (2x faster)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # Time shifted signal
    plt.subplot(2, 2, 3)
    plt.plot(shifted_time, shifted_signal, 'g-', linewidth=2)
    plt.title('Time Shifted (delay 0.5s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # Time reversed signal
    plt.subplot(2, 2, 4)
    plt.plot(reversed_time, reversed_signal, 'm-', linewidth=2)
    plt.title('Time Reversed')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def discrete_signal_example():
    """
    Example with discrete signals.
    """
    print("\n\nDiscrete Signal Processing Example")
    print("=" * 40)
    
    # Create discrete signal
    discrete_signal = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1])
    print(f"Original discrete signal: {discrete_signal}")
    
    processor = SignalProcessor()
    
    # Discrete time scaling
    scaled_discrete = processor.discrete_time_scale(discrete_signal, 2.0)
    print(f"Time scaled (2x): {scaled_discrete}")
    
    # Discrete time shifting
    shifted_discrete = processor.discrete_time_shift(discrete_signal, 2)
    print(f"Time shifted (+2): {shifted_discrete}")
    
    # Discrete time reversal
    reversed_discrete = processor.discrete_time_reverse(discrete_signal)
    print(f"Time reversed: {reversed_discrete}")


if __name__ == "__main__":
    simple_example()
    discrete_signal_example()