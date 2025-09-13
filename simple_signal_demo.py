#!/usr/bin/env python3
"""
Simple demonstration of time operations without external dependencies.
This version uses only Python standard library for basic signal operations.
"""

import math
import random


def create_simple_signal(duration=2.0, sample_rate=100):
    """
    Create a simple test signal using only standard library.
    
    Args:
        duration: Duration in seconds
        sample_rate: Samples per second
        
    Returns:
        Tuple of (time_points, signal_values)
    """
    num_samples = int(duration * sample_rate)
    time_points = [i / sample_rate for i in range(num_samples)]
    
    # Create a composite signal with multiple frequency components
    signal_values = []
    for t in time_points:
        value = (math.sin(2 * math.pi * 2 * t) +  # 2 Hz component
                 0.5 * math.sin(2 * math.pi * 5 * t) +  # 5 Hz component
                 0.3 * math.sin(2 * math.pi * 10 * t))  # 10 Hz component
        signal_values.append(value)
    
    return time_points, signal_values


def linear_interpolate(x1, y1, x2, y2, x):
    """
    Linear interpolation between two points.
    
    Args:
        x1, y1: First point
        x2, y2: Second point
        x: X value to interpolate at
        
    Returns:
        Interpolated Y value
    """
    if x2 == x1:
        return y1
    
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)


def time_scale(signal, time_axis, scale_factor):
    """
    Apply time scaling to a signal.
    
    Args:
        signal: List of signal values
        time_axis: List of time points
        scale_factor: Scaling factor (positive)
        
    Returns:
        Tuple of (scaled_signal, scaled_time_axis)
    """
    if scale_factor <= 0:
        raise ValueError("Scale factor must be positive")
    
    # Calculate new time axis
    scaled_time_axis = [t / scale_factor for t in time_axis]
    
    # Interpolate signal at new time points
    scaled_signal = []
    for new_t in scaled_time_axis:
        # Find the two points to interpolate between
        if new_t <= time_axis[0]:
            scaled_signal.append(signal[0])
        elif new_t >= time_axis[-1]:
            scaled_signal.append(signal[-1])
        else:
            # Find the surrounding points
            for i in range(len(time_axis) - 1):
                if time_axis[i] <= new_t <= time_axis[i + 1]:
                    # Linear interpolation
                    interpolated_value = linear_interpolate(
                        time_axis[i], signal[i],
                        time_axis[i + 1], signal[i + 1],
                        new_t
                    )
                    scaled_signal.append(interpolated_value)
                    break
    
    return scaled_signal, scaled_time_axis


def time_shift(signal, time_axis, shift_amount):
    """
    Apply time shifting to a signal.
    
    Args:
        signal: List of signal values
        time_axis: List of time points
        shift_amount: Amount to shift in time units
        
    Returns:
        Tuple of (shifted_signal, shifted_time_axis)
    """
    # Calculate new time axis
    shifted_time_axis = [t - shift_amount for t in time_axis]
    
    # Interpolate signal at new time points
    shifted_signal = []
    for new_t in shifted_time_axis:
        # Find the two points to interpolate between
        if new_t <= time_axis[0]:
            shifted_signal.append(signal[0])
        elif new_t >= time_axis[-1]:
            shifted_signal.append(signal[-1])
        else:
            # Find the surrounding points
            for i in range(len(time_axis) - 1):
                if time_axis[i] <= new_t <= time_axis[i + 1]:
                    # Linear interpolation
                    interpolated_value = linear_interpolate(
                        time_axis[i], signal[i],
                        time_axis[i + 1], signal[i + 1],
                        new_t
                    )
                    shifted_signal.append(interpolated_value)
                    break
    
    return shifted_signal, shifted_time_axis


def time_reverse(signal, time_axis):
    """
    Apply time reversal to a signal.
    
    Args:
        signal: List of signal values
        time_axis: List of time points
        
    Returns:
        Tuple of (reversed_signal, reversed_time_axis)
    """
    # Reverse both signal and time axis
    reversed_signal = signal[::-1]
    reversed_time_axis = [-t for t in time_axis[::-1]]
    
    return reversed_signal, reversed_time_axis


def discrete_time_scale(signal, scale_factor):
    """
    Apply time scaling to a discrete signal.
    
    Args:
        signal: List of signal values
        scale_factor: Scaling factor (positive)
        
    Returns:
        Scaled discrete signal
    """
    if scale_factor <= 0:
        raise ValueError("Scale factor must be positive")
    
    if scale_factor == 1:
        return signal.copy()
    
    if scale_factor > 1:
        # Compression: decimate
        decimation_factor = int(scale_factor)
        if decimation_factor >= len(signal):
            return [signal[0]]
        return signal[::decimation_factor]
    else:
        # Expansion: interpolate
        interpolation_factor = int(1 / scale_factor)
        result = []
        for value in signal:
            result.extend([value] * interpolation_factor)
        return result


def discrete_time_shift(signal, shift_samples):
    """
    Apply time shifting to a discrete signal.
    
    Args:
        signal: List of signal values
        shift_samples: Number of samples to shift
        
    Returns:
        Shifted discrete signal
    """
    if shift_samples == 0:
        return signal.copy()
    
    if shift_samples > 0:
        # Delay: pad with zeros at the beginning
        return [0] * shift_samples + signal
    else:
        # Advance: remove samples from the beginning
        return signal[-shift_samples:]


def discrete_time_reverse(signal):
    """
    Apply time reversal to a discrete signal.
    
    Args:
        signal: List of signal values
        
    Returns:
        Reversed discrete signal
    """
    return signal[::-1]


def print_signal_info(signal, time_axis, name):
    """
    Print information about a signal.
    
    Args:
        signal: Signal values
        time_axis: Time points
        name: Signal name
    """
    print(f"\n{name}:")
    print(f"  Duration: {time_axis[0]:.2f}s to {time_axis[-1]:.2f}s")
    print(f"  Length: {len(signal)} samples")
    print(f"  Min value: {min(signal):.3f}")
    print(f"  Max value: {max(signal):.3f}")
    print(f"  First few values: {signal[:5]}")


def demonstrate_operations():
    """
    Demonstrate all time operations.
    """
    print("Signal Processing Operations Demo")
    print("=" * 40)
    
    # Create test signal
    print("\nCreating test signal...")
    t, signal = create_simple_signal(duration=1.0, sample_rate=50)
    print_signal_info(signal, t, "Original Signal")
    
    # Time Scaling Examples
    print("\n" + "="*50)
    print("1. TIME SCALING")
    print("="*50)
    
    # Stretch signal (0.5x speed)
    print("\nStretching signal (0.5x speed):")
    scaled_signal_slow, scaled_time_slow = time_scale(signal, t, 0.5)
    print_signal_info(scaled_signal_slow, scaled_time_slow, "Stretched Signal")
    
    # Compress signal (2x speed)
    print("\nCompressing signal (2x speed):")
    scaled_signal_fast, scaled_time_fast = time_scale(signal, t, 2.0)
    print_signal_info(scaled_signal_fast, scaled_time_fast, "Compressed Signal")
    
    # Time Shifting Examples
    print("\n" + "="*50)
    print("2. TIME SHIFTING")
    print("="*50)
    
    # Delay signal
    print("\nDelaying signal by 0.2s:")
    shifted_signal_delay, shifted_time_delay = time_shift(signal, t, 0.2)
    print_signal_info(shifted_signal_delay, shifted_time_delay, "Delayed Signal")
    
    # Advance signal
    print("\nAdvancing signal by 0.1s:")
    shifted_signal_advance, shifted_time_advance = time_shift(signal, t, -0.1)
    print_signal_info(shifted_signal_advance, shifted_time_advance, "Advanced Signal")
    
    # Time Reversal
    print("\n" + "="*50)
    print("3. TIME REVERSAL")
    print("="*50)
    
    print("\nReversing signal in time:")
    reversed_signal, reversed_time = time_reverse(signal, t)
    print_signal_info(reversed_signal, reversed_time, "Reversed Signal")
    
    # Discrete Signal Examples
    print("\n" + "="*50)
    print("4. DISCRETE SIGNAL OPERATIONS")
    print("="*50)
    
    # Create discrete signal
    discrete_signal = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    print(f"\nOriginal discrete signal: {discrete_signal}")
    
    # Discrete time scaling
    discrete_scaled = discrete_time_scale(discrete_signal, 2.0)
    print(f"Time scaled (2x): {discrete_scaled}")
    
    # Discrete time shifting
    discrete_shifted = discrete_time_shift(discrete_signal, 2)
    print(f"Time shifted (+2): {discrete_shifted}")
    
    # Discrete time reversal
    discrete_reversed = discrete_time_reverse(discrete_signal)
    print(f"Time reversed: {discrete_reversed}")
    
    print("\n" + "="*50)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("="*50)


if __name__ == "__main__":
    demonstrate_operations()