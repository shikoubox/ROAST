import os
import random

def encode_to_bytes(_index, _value):
    # Encode index
    if 0 <= _index < 64:  # Ensure the value is within the 6-bit range
        index = _index & ((1<<6)-1)
    else:
        raise Exception("[ERROR] 6-bit value must be between 0 and 63")

    value = encode_float16(_value)

    if not (0 <= value < 65536):
        raise Exception("[ERROR] 16-bit value must be between 0 and 65535.")

    # Shift the 6-bit value to the left by 16 bits
    combined_value = (index << 16) | (value)
    return combined_value.to_bytes(3, 'big')

def encode_float16(value):
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

def decode_float16(half_float):
    # Extract the sign, exponent, and mantissa
    sign = (half_float >> 15) & 0x1  # Get the sign bit
    exponent = (half_float >> 10) & 0x1F  # Get the exponent bits
    mantissa = half_float & 0x3FF  # Get the mantissa bits

    # Calculate the value
    if exponent == 0 and mantissa == 0:
        # Zero case
        return 0.0
    elif exponent == 0:
        # Subnormal numbers
        return ((-1) ** sign) * (mantissa / (1 << 10)) * (2 ** -14)
    elif exponent == 31:
        # Inf or NaN
        return float('inf') if mantissa == 0 else float('nan')

    # Normalized numbers
    exponent -= 15  # Adjust the exponent (bias of 15)
    value = (1 + mantissa / (1 << 10)) * (2 ** exponent)
    return (-1) ** sign * value

def bytes_to_message(msg):
    _msg = int.from_bytes(msg, "big")
    message = _msg & ((1<<16)-1)
    index = (_msg >> 16) & ((1<<6)-1)

    return message, index

def encode_to_message():

    return False