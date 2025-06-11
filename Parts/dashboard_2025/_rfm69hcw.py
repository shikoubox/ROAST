import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69
import os
import random
import curses
import threading
from data import CSV_hand

# global exit flag
exit_program = False

# Button A
btnA = DigitalInOut(board.D17)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# RFM69 Configuration
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz
BAUD_RATE=1000
BIT_RATE=1000
# Optional encryption (MUST match on both)
# rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

# Curses settings
messages = ["[INFO] System init..."]
height, width = 20, 75  # Console window size
## Use Unicode box-drawing characters for fancy borders
h  = '-'#'─'
v  = '|'
c  = '+'

# Initialize RFM69 once
try:
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUD_RATE, high_power=True)
    rfm69.bitrate = BIT_RATE
    prev_packet = None
except RuntimeError as error:
    log_message("[ERROR] RFM69")
    log_message("[ERROR]: {error}")
    rfm69 = None

# Main loop
def main_event_loop(stdscr):
    global exit_program
    print_header()

    while not exit_program:
        stdscr.addstr(0, 2, "RFM69 Receiver - Press 'q' to quit. Otherwise 'b' 't' 'u' 's'")
        print_console(stdscr)
        packet = None
        if rfm69 is not None:
            print_rfmdata(rfm69)

            # Check for incoming packets

            packet = rfm69.receive()
            if packet is not None:
                rssi = rfm69.last_rssi  # This is your most accurate RSSI reading
                log_message(f"[INFO] Received signal strength: {rssi} dBm")

                prev_packet=packet
                try:
                    new_packet = packet.decode("utf-16")
                    log_message(f"[INFO] Received: {new_packet}")
                    print(CSV_hand.prepend_new_row(new_packet))
                    status = CSV_hand.prepend_new_row(new_packet)
                    print(status)
                    if status is not None:
                        log_message(f"{status}")
                    else:
                        log_message(f"[INFO] Function prepend_new_row() ran without returning a status")

                except UnicodeDecodeError:
                    log_message(f"[INFO] Received (raw): {packet}")
            else:
                stdscr.addstr(2,3,"[INFO] Waiting for packet")
                stdscr.refresh()
                time.sleep(1)
                stdscr.addstr(2,3,"[    ]                   ")
                

        else:
            log_message("[ERROR] RFM69 is none")

        stdscr.refresh()
        print_console(stdscr)


def listen_for_keys(stdscr):
    global exit_program
    curses.cbreak()  # Enable cbreak mode
    stdscr.keypad(True)  # Enable keypad input
    stdscr.refresh() 

    while not exit_program:
        stdscr.addstr(2,29, "[INFO] Listening for keypress")

        # Physical button presses?
        if not btnA.value:
            stemomg
            button_a_data = bytes("test","utf-16")
            rfm69.send(button_a_data)
            log_message('[INFO] Sent data test by button click')
        
        key = stdscr.getch()  # Wait for a key press
        log_message(f"[INFO] You pressed: {chr(key)}")
        stdscr.addstr(2,29, "[    ]                       ")

        if key == ord('t'):
            try:
                log_message("[INFO] Preparing to send BIG dataset test...")
                
                test_data = get_data_test()
                log_message(f"[DEBUG] Generated data: {str(test_data)[:width-27]}...")  # Only first 80 chars

                button_a_data = bytes(f"{test_data}", "utf-16")
                log_message("[DEBUG] Encoded data to bytes.")

                rfm69.send(button_a_data)
                log_message("[SUCCESS] Sent BIG dataset test over radio!")

            except Exception as e:
                log_message(f"[ERROR] Failed to send test data: {e}")
                stdscr.addstr(30,0,f"{e}")
                with open("thread_error.log", "a") as f:
                    f.write(f"Exception in send BIG dataset test: {e}")

        if key == ord('s'):
            log_message('[INFO] Sending "super message" by clicking keyboard')
            button_a_data = bytes("super message","utf-16")
            rfm69.send(button_a_data)
            log_message('[INFO] Sent "super message"')

        if key == ord('b'):
            log_message('[INFO] Encoding message by clicking keyboard')
            encode_to_bytes(16,1.5)
            encode_to_bytes(16,111221.541231)
            log_message('[INFO] Done encoding')

        # keyboard button presses
        if key == ord('u'):
            send_data_test(stdscr)

        if key == ord('q'):  # Exit if 'q' is pressed
            stdscr.clear()
            stdscr.addstr(3,4,"Exiting...")
            stdscr.refresh()
            exit_program = True # Set the exit flag

def encode_to_bytes(_index, _value):
    # Encode index
    log_message(f"[INFO] Trying to encode value {_value} at index {_index}")
    if 0 <= _index < 64:  # Ensure the value is within the 6-bit range
        index = format(_index, '06b')  # Format as a 6-bit binary string
        log_message(f"[INFO] {_index} becomes {index:06b}")

    else:
        errorstring= "[ERROR] Value must be between 0 and 63 for 6-bit representation."
        log_message(errorstring)
        return errorstring
    
    value = float_to_half_precision(_value)
    log_message(f"[INFO] {_value} becomes {value:016b}")

    if not (0 <= value < 65536):
        stringg = "16-bit value must be between 0 and 65535."
        log_message(f"[ERROR] {stringg}")
        return stringg
    else:
        log_message(f"[INFO] message ID: 290")

    # Shift the 6-bit value to the left by 16 bits
    combined_value = (index << 16) | (value:16b)

    log_message(f"[INFO] Message created: {combined_value:22b}")
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


def send_data_test():
    new_data = {
        "current_temp":     random.uniform(15.0, 35.0),
        "cooling_temp":     random.uniform(25.0, 40.0),
        "motor_usage":      random.uniform(5.0, 30.0),
        "speed":            random.uniform(15.0, 70.0),
        "wh_total":         random.uniform(15.0, 30.0),
        "distance":         random.uniform(15.0, 30.0),
        "solar_output":     random.uniform(15.0, 30.0),
        "brake_status":     random.uniform(15.0, 30.0),
        "tyre_lf":          random.uniform(15.0, 30.0),
        "tyre_rf":          random.uniform(15.0, 30.0),
        "tyre_lr":          random.uniform(15.0, 30.0),
        "tyre_rr":          random.uniform(15.0, 30.0),
        "module1_percent":  random.uniform(5.0, 100.0),
        "module1_voltage":  random.uniform(3.0, 18.0),
        "m1c1":             random.uniform(1.50, 3.0),
        "m1c2":             random.uniform(1.50, 3.0),
        "m1c3":             random.uniform(1.50, 3.0),
        "m1c4":             random.uniform(1.50, 3.0),
        "m1c5":             random.uniform(1.50, 3.0),
        "m1c6":             random.uniform(1.50, 3.0),
        "m1c7":             random.uniform(1.50, 3.0),
        "m1c8":             random.uniform(1.50, 3.0),
        "module2_percent":  random.uniform(15.0, 3.0),
        "module2_voltage":  random.uniform(15.0, 3.0),
        "m2c1":             random.uniform(1.50, 3.0),
        "m2c2":             random.uniform(1.50, 3.0),
        "m2c3":             random.uniform(1.50, 3.0),
        "m2c4":             random.uniform(1.50, 3.0),
        "m2c5":             random.uniform(1.50, 3.0),
        "m2c6":             random.uniform(1.50, 3.0),
        "m2c7":             random.uniform(1.50, 3.0),
        "m2c8":             random.uniform(1.50, 3.0),
        "battery_percent":  random.uniform(10.0, 100.0),
        "battery_voltage":  random.uniform(10.0, 13.0),
    }

    stdscr.addstr(5,0, 'Sending data test')
    status = CSV_hand.prepend_new_row(new_data)
    log_message(status)

def get_data_test():
    new_data = {
        "current_temp":     random.uniform(15.0, 35.0),
        "cooling_temp":     random.uniform(25.0, 40.0),
        "motor_usage":      random.uniform(5.0, 30.0),
        "speed":            random.uniform(15.0, 70.0),
        "wh_total":         random.uniform(15.0, 30.0),
        "distance":         random.uniform(15.0, 30.0),
        "solar_output":     random.uniform(15.0, 30.0),
        "brake_status":     random.uniform(15.0, 30.0),
        "tyre_lf":          random.uniform(15.0, 30.0),
        "tyre_rf":          random.uniform(15.0, 30.0),
        "tyre_lr":          random.uniform(15.0, 30.0),
        "tyre_rr":          random.uniform(15.0, 30.0),
        "module1_percent":  random.uniform(5.0, 100.0),
        "module1_voltage":  random.uniform(3.0, 18.0),
        "m1c1":             random.uniform(1.50, 3.0),
        "m1c2":             random.uniform(1.50, 3.0),
        "m1c3":             random.uniform(1.50, 3.0),
        "m1c4":             random.uniform(1.50, 3.0),
        "m1c5":             random.uniform(1.50, 3.0),
        "m1c6":             random.uniform(1.50, 3.0),
        "m1c7":             random.uniform(1.50, 3.0),
        "m1c8":             random.uniform(1.50, 3.0),
        "module2_percent":  random.uniform(15.0, 3.0),
        "module2_voltage":  random.uniform(15.0, 3.0),
        "m2c1":             random.uniform(1.50, 3.0),
        "m2c2":             random.uniform(1.50, 3.0),
        "m2c3":             random.uniform(1.50, 3.0),
        "m2c4":             random.uniform(1.50, 3.0),
        "m2c5":             random.uniform(1.50, 3.0),
        "m2c6":             random.uniform(1.50, 3.0),
        "m2c7":             random.uniform(1.50, 3.0),
        "m2c8":             random.uniform(1.50, 3.0),
        "battery_percent":  random.uniform(10.0, 100.0),
        "battery_voltage":  random.uniform(10.0, 13.0),
    }
    return new_data

def print_rfmdata(_rfm69):
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 1, width+1  # Console window position
    
    rfmdata_win = curses.newwin(height+4-start_y, 22, start_y, start_x)

    rfmdata_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    rfmdata_win.border(v, v, h, h, c, c, c, c)

    rfmdata_win.addstr(1, 1,  "RFM69    : Detected")
    rfmdata_win.addstr(3, 1, f"Frequency:")
    rfmdata_win.addstr(4, 1, f"{_rfm69.frequency_mhz} MHz")
    rfmdata_win.addstr(6, 1, f"Bit rate :")
    rfmdata_win.addstr(7, 1, f"{_rfm69.bitrate/1000} kbit/s")
    rfmdata_win.addstr(9, 1, f"Baud rate:")
    rfmdata_win.addstr(10,1, f"{BAUD_RATE} baud/s")
    rfmdata_win.addstr(12,1, f"Freq.dev.:") 
    rfmdata_win.addstr(13,1, f"{_rfm69.frequency_deviation/1000} kHz") 
    rfmdata_win.addstr(15,1, f"Tx_Power :")
    rfmdata_win.addstr(16,1, f"{_rfm69.tx_power} dBm")


    rfmdata_win.refresh()


def print_header():
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 1, 0  # Console window position
    
    header_win = curses.newwin(3, width, start_y, start_x)

    header_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    header_win.border(v, v, h, h, c, c, c, c)

    header_win.refresh()


def print_console(stdscr):
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 4, 0  # Console window position
    
    console_win = curses.newwin(height, width, start_y, start_x)

    
    console_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    console_win.border(v, v, h, h, c, c, c, c)

    for i, msg in enumerate(messages):
        console_win.addstr(i + 1, 2, msg)  # +1 and +2 to not write over the border

    console_win.refresh()
    
def log_message(msg):
    if len(messages) >= height-2:
        messages.pop(0)  # Remove oldest
    messages.append(msg[:width-3])

key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
key_listener_thread.start()

# Run the main event loop
curses.wrapper(main_event_loop)

# Wait for the key listener thread to finish
key_listener_thread.join()

