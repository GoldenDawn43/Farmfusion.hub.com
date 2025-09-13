# Signal Processing - Time Operations

This Python module provides comprehensive implementations of time-domain operations on signals, including time-scaling, time-shifting, and time-reversal.

## Features

- **Time Scaling**: Compress or stretch signals in time
- **Time Shifting**: Delay or advance signals in time
- **Time Reversal**: Mirror signals in time
- **Both Continuous and Discrete Signal Support**
- **Multiple Interpolation Methods**
- **Comprehensive Visualization and Examples**

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
import numpy as np
from signal_processing import SignalProcessor, create_test_signal

# Create a test signal
t, signal = create_test_signal(duration=2.0, sampling_rate=1000.0)

# Initialize processor
processor = SignalProcessor(sampling_rate=1000.0)

# Time scaling: make signal 2x faster
scaled_signal, scaled_time = processor.time_scale(signal, t, 2.0)

# Time shifting: delay by 0.5 seconds
shifted_signal, shifted_time = processor.time_shift(signal, t, 0.5)

# Time reversal: mirror the signal
reversed_signal, reversed_time = processor.time_reverse(signal, t)
```

## Usage Examples

### 1. Time Scaling

Time scaling changes the duration of a signal:
- `scale_factor > 1`: Signal is compressed (faster playback)
- `scale_factor < 1`: Signal is stretched (slower playback)
- `scale_factor = 1`: No change

```python
# Make signal 2x faster (compress)
scaled_signal, scaled_time = processor.time_scale(signal, t, 2.0)

# Make signal 0.5x slower (stretch)
stretched_signal, stretched_time = processor.time_scale(signal, t, 0.5)
```

### 2. Time Shifting

Time shifting moves a signal in time:
- `shift_amount > 0`: Signal is delayed (shifted right)
- `shift_amount < 0`: Signal is advanced (shifted left)
- `shift_amount = 0`: No change

```python
# Delay signal by 0.5 seconds
delayed_signal, delayed_time = processor.time_shift(signal, t, 0.5)

# Advance signal by 0.3 seconds
advanced_signal, advanced_time = processor.time_shift(signal, t, -0.3)
```

### 3. Time Reversal

Time reversal creates a mirror image of the signal in time:

```python
# Reverse the signal in time
reversed_signal, reversed_time = processor.time_reverse(signal, t)
```

### 4. Discrete Signal Operations

For discrete signals, use the discrete methods:

```python
# Discrete time scaling
discrete_signal = np.array([1, 2, 3, 4, 5])
scaled_discrete = processor.discrete_time_scale(discrete_signal, 2.0)

# Discrete time shifting
shifted_discrete = processor.discrete_time_shift(discrete_signal, 2)

# Discrete time reversal
reversed_discrete = processor.discrete_time_reverse(discrete_signal)
```

## Running Examples

### Basic Example
```bash
python example_usage.py
```

### Full Demonstration
```bash
python signal_processing.py
```

### Run Tests
```bash
python test_signal_processing.py
```

## API Reference

### SignalProcessor Class

#### `__init__(sampling_rate=1000.0)`
Initialize the signal processor with a sampling rate.

#### `time_scale(signal, time_axis, scale_factor, method='linear')`
Apply time scaling to a continuous signal.

**Parameters:**
- `signal`: Input signal array
- `time_axis`: Time axis corresponding to the signal
- `scale_factor`: Scaling factor (positive)
- `method`: Interpolation method ('linear', 'cubic', 'nearest')

**Returns:** Tuple of (scaled_signal, scaled_time_axis)

#### `time_shift(signal, time_axis, shift_amount, method='linear')`
Apply time shifting to a continuous signal.

**Parameters:**
- `signal`: Input signal array
- `time_axis`: Time axis corresponding to the signal
- `shift_amount`: Amount to shift in time units
- `method`: Interpolation method ('linear', 'cubic', 'nearest')

**Returns:** Tuple of (shifted_signal, shifted_time_axis)

#### `time_reverse(signal, time_axis)`
Apply time reversal to a continuous signal.

**Parameters:**
- `signal`: Input signal array
- `time_axis`: Time axis corresponding to the signal

**Returns:** Tuple of (reversed_signal, reversed_time_axis)

#### `discrete_time_scale(signal, scale_factor)`
Apply time scaling to a discrete signal.

#### `discrete_time_shift(signal, shift_samples)`
Apply time shifting to a discrete signal.

#### `discrete_time_reverse(signal)`
Apply time reversal to a discrete signal.

## Mathematical Background

### Time Scaling
For a signal x(t), time scaling by factor a produces:
- x(t/a) for a > 1 (compression)
- x(t/a) for 0 < a < 1 (expansion)

### Time Shifting
For a signal x(t), time shifting by amount τ produces:
- x(t - τ) for τ > 0 (delay)
- x(t - τ) for τ < 0 (advance)

### Time Reversal
For a signal x(t), time reversal produces:
- x(-t)

## Requirements

- Python 3.7+
- NumPy >= 1.21.0
- Matplotlib >= 3.5.0
- SciPy >= 1.7.0

## License

This project is open source and available under the MIT License.