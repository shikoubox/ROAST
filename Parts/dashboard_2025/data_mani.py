import os
import random

def encode_to_bytes(_index, _value):
    # Encode index
    if 0 <= _index < 64:  # Ensure the value is within the 6-bit range
        index = _index & 0x3F
    else:
        raise Exception("[ERROR] 6-bit value must be between 0 and 63")
    
    value = float_to_half_precision(_value)

    if not (0 <= value < 65536):
        raise Exception("[ERROR] 16-bit value must be between 0 and 65535.")

    # Shift the 6-bit value to the left by 16 bits
    combined_value = (index << 16) | (value)

    return combined_value

def float_to_half_precision(value):
    if value == 0.0:
        return 0  # Special case for zero

    # Determine the sign bit
    sign = 0
    if value < 0:
        sign = 1
        value = -value

    # Find the exponent and normalize the value
    exponent = 0
    while value >= 2.0:
        value /= 2.0
        exponent += 1
    while value < 1.0:
        value *= 2.0
        exponent -= 1

    # Adjust exponent with bias (15 for half-precision)
    exponent += 15

    # Check for overflow/underflow
    if exponent >= 31:  # Overflow
        return (sign << 15) | (31 << 10)  # Return infinity
    if exponent <= 0:  # Underflow
        return (sign << 15)  # Return zero

    # Get the mantissa (10 bits)
    mantissa = int((value - 1) * (1 << 10))  # Scale to 10 bits

    # Combine sign, exponent, and mantissa
    half_precision = (sign << 15) | (exponent << 10) | (mantissa & 0x3FF)
    return half_precision



def encode_to_message():
    
    return False
