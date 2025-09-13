"""
Signal Processing Module for Time Operations

This module provides functions for time-scaling, time-shifting, and time-reversal
operations on signals. It includes both continuous and discrete signal support.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from typing import Union, Tuple, Optional


class SignalProcessor:
    """
    A class for performing various time-domain operations on signals.
    """
    
    def __init__(self, sampling_rate: float = 1000.0):
        """
        Initialize the signal processor.
        
        Args:
            sampling_rate: Sampling rate in Hz for discrete signals
        """
        self.sampling_rate = sampling_rate
    
    def time_scale(self, signal: np.ndarray, time_axis: np.ndarray, 
                   scale_factor: float, method: str = 'linear') -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply time scaling to a signal.
        
        Time scaling changes the duration of the signal:
        - scale_factor > 1: Signal is compressed (faster)
        - scale_factor < 1: Signal is stretched (slower)
        - scale_factor = 1: No change
        
        Args:
            signal: Input signal array
            time_axis: Time axis corresponding to the signal
            scale_factor: Scaling factor (positive)
            method: Interpolation method ('linear', 'cubic', 'nearest')
            
        Returns:
            Tuple of (scaled_signal, scaled_time_axis)
        """
        if scale_factor <= 0:
            raise ValueError("Scale factor must be positive")
        
        # Calculate new time axis
        new_time_axis = time_axis / scale_factor
        
        # Create interpolation function
        if method == 'linear':
            interp_func = interpolate.interp1d(time_axis, signal, kind='linear', 
                                             bounds_error=False, fill_value='extrapolate')
        elif method == 'cubic':
            interp_func = interpolate.interp1d(time_axis, signal, kind='cubic', 
                                             bounds_error=False, fill_value='extrapolate')
        elif method == 'nearest':
            interp_func = interpolate.interp1d(time_axis, signal, kind='nearest', 
                                             bounds_error=False, fill_value='extrapolate')
        else:
            raise ValueError("Method must be 'linear', 'cubic', or 'nearest'")
        
        # Interpolate signal at new time points
        scaled_signal = interp_func(new_time_axis)
        
        return scaled_signal, new_time_axis
    
    def time_shift(self, signal: np.ndarray, time_axis: np.ndarray, 
                   shift_amount: float, method: str = 'linear') -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply time shifting to a signal.
        
        Time shifting moves the signal in time:
        - shift_amount > 0: Signal is delayed (shifted right)
        - shift_amount < 0: Signal is advanced (shifted left)
        - shift_amount = 0: No change
        
        Args:
            signal: Input signal array
            time_axis: Time axis corresponding to the signal
            shift_amount: Amount to shift in time units
            method: Interpolation method ('linear', 'cubic', 'nearest')
            
        Returns:
            Tuple of (shifted_signal, shifted_time_axis)
        """
        # Calculate new time axis
        new_time_axis = time_axis - shift_amount
        
        # Create interpolation function
        if method == 'linear':
            interp_func = interpolate.interp1d(time_axis, signal, kind='linear', 
                                             bounds_error=False, fill_value='extrapolate')
        elif method == 'cubic':
            interp_func = interpolate.interp1d(time_axis, signal, kind='cubic', 
                                             bounds_error=False, fill_value='extrapolate')
        elif method == 'nearest':
            interp_func = interpolate.interp1d(time_axis, signal, kind='nearest', 
                                             bounds_error=False, fill_value='extrapolate')
        else:
            raise ValueError("Method must be 'linear', 'cubic', or 'nearest'")
        
        # Interpolate signal at new time points
        shifted_signal = interp_func(new_time_axis)
        
        return shifted_signal, new_time_axis
    
    def time_reverse(self, signal: np.ndarray, time_axis: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply time reversal to a signal.
        
        Time reversal flips the signal in time, creating a mirror image.
        
        Args:
            signal: Input signal array
            time_axis: Time axis corresponding to the signal
            
        Returns:
            Tuple of (reversed_signal, reversed_time_axis)
        """
        # Reverse both signal and time axis
        reversed_signal = np.flip(signal)
        reversed_time_axis = np.flip(-time_axis)  # Flip and negate for proper time reversal
        
        return reversed_signal, reversed_time_axis
    
    def discrete_time_scale(self, signal: np.ndarray, scale_factor: float) -> np.ndarray:
        """
        Apply time scaling to a discrete signal using decimation/interpolation.
        
        Args:
            signal: Input discrete signal array
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
                # If decimation factor is too large, return a single sample
                return np.array([signal[0]])
            return signal[::decimation_factor]
        else:
            # Expansion: interpolate
            interpolation_factor = int(1 / scale_factor)
            return np.repeat(signal, interpolation_factor)
    
    def discrete_time_shift(self, signal: np.ndarray, shift_samples: int) -> np.ndarray:
        """
        Apply time shifting to a discrete signal.
        
        Args:
            signal: Input discrete signal array
            shift_samples: Number of samples to shift (positive = delay, negative = advance)
            
        Returns:
            Shifted discrete signal
        """
        if shift_samples == 0:
            return signal.copy()
        
        if shift_samples > 0:
            # Delay: pad with zeros at the beginning
            return np.concatenate([np.zeros(shift_samples), signal])
        else:
            # Advance: remove samples from the beginning
            return signal[-shift_samples:]
    
    def discrete_time_reverse(self, signal: np.ndarray) -> np.ndarray:
        """
        Apply time reversal to a discrete signal.
        
        Args:
            signal: Input discrete signal array
            
        Returns:
            Reversed discrete signal
        """
        return np.flip(signal)


def create_test_signal(duration: float = 2.0, sampling_rate: float = 1000.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create a test signal for demonstration purposes.
    
    Args:
        duration: Duration of the signal in seconds
        sampling_rate: Sampling rate in Hz
        
    Returns:
        Tuple of (time_axis, signal)
    """
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    
    # Create a composite signal with multiple frequency components
    signal = (np.sin(2 * np.pi * 2 * t) +  # 2 Hz component
              0.5 * np.sin(2 * np.pi * 5 * t) +  # 5 Hz component
              0.3 * np.sin(2 * np.pi * 10 * t))  # 10 Hz component
    
    return t, signal


def plot_signal_comparison(original_time: np.ndarray, original_signal: np.ndarray,
                          modified_time: np.ndarray, modified_signal: np.ndarray,
                          title: str, xlabel: str = "Time (s)", ylabel: str = "Amplitude"):
    """
    Plot comparison between original and modified signals.
    
    Args:
        original_time: Time axis of original signal
        original_signal: Original signal
        modified_time: Time axis of modified signal
        modified_signal: Modified signal
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(original_time, original_signal, 'b-', linewidth=2, label='Original')
    plt.title(f'{title} - Original Signal')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(modified_time, modified_signal, 'r-', linewidth=2, label='Modified')
    plt.title(f'{title} - Modified Signal')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.show()


def demonstrate_operations():
    """
    Demonstrate all time operations with visualizations.
    """
    # Create test signal
    t, signal = create_test_signal(duration=2.0, sampling_rate=1000.0)
    
    # Initialize processor
    processor = SignalProcessor(sampling_rate=1000.0)
    
    print("Signal Processing Operations Demo")
    print("=" * 40)
    
    # Time Scaling Examples
    print("\n1. Time Scaling:")
    print("   - Scale factor 0.5 (stretch by 2x)")
    print("   - Scale factor 2.0 (compress by 2x)")
    
    # Stretch signal (0.5x speed)
    scaled_signal_slow, scaled_time_slow = processor.time_scale(signal, t, 0.5)
    plot_signal_comparison(t, signal, scaled_time_slow, scaled_signal_slow, 
                          "Time Scaling (0.5x - Stretched)")
    
    # Compress signal (2x speed)
    scaled_signal_fast, scaled_time_fast = processor.time_scale(signal, t, 2.0)
    plot_signal_comparison(t, signal, scaled_time_fast, scaled_signal_fast, 
                          "Time Scaling (2.0x - Compressed)")
    
    # Time Shifting Examples
    print("\n2. Time Shifting:")
    print("   - Shift by +0.5s (delay)")
    print("   - Shift by -0.3s (advance)")
    
    # Delay signal
    shifted_signal_delay, shifted_time_delay = processor.time_shift(signal, t, 0.5)
    plot_signal_comparison(t, signal, shifted_time_delay, shifted_signal_delay, 
                          "Time Shifting (+0.5s - Delayed)")
    
    # Advance signal
    shifted_signal_advance, shifted_time_advance = processor.time_shift(signal, t, -0.3)
    plot_signal_comparison(t, signal, shifted_time_advance, shifted_signal_advance, 
                          "Time Shifting (-0.3s - Advanced)")
    
    # Time Reversal
    print("\n3. Time Reversal:")
    print("   - Mirror the signal in time")
    
    reversed_signal, reversed_time = processor.time_reverse(signal, t)
    plot_signal_comparison(t, signal, reversed_time, reversed_signal, 
                          "Time Reversal")
    
    # Discrete Signal Examples
    print("\n4. Discrete Signal Operations:")
    print("   - Working with discrete samples")
    
    # Create discrete signal
    discrete_signal = signal[::10]  # Downsample for discrete example
    discrete_time = t[::10]
    
    # Discrete time scaling
    discrete_scaled = processor.discrete_time_scale(discrete_signal, 2.0)
    print(f"   Original length: {len(discrete_signal)}")
    print(f"   Scaled length: {len(discrete_scaled)}")
    
    # Discrete time shifting
    discrete_shifted = processor.discrete_time_shift(discrete_signal, 5)
    print(f"   Shifted length: {len(discrete_shifted)}")
    
    # Discrete time reversal
    discrete_reversed = processor.discrete_time_reverse(discrete_signal)
    print(f"   Reversed length: {len(discrete_reversed)}")


if __name__ == "__main__":
    # Run demonstration
    demonstrate_operations()