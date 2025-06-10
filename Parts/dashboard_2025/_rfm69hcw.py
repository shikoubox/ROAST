import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69
import csv
import os
import random
import curses
import threading

# This script expects data.csv to live in a subdirectory named 'subdir'.
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "data.csv")


# Button A
btnA = DigitalInOut(board.D17)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# RFM69 Configuration
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.
#
BAUD_RATE=1000
BIT_RATE=1000
# Optional encryption (MUST match on both)
# rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

# Initialize RFM69 once
try:
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUD_RATE, high_power=True)
    rfm69.bitrate = BIT_RATE
    prev_packet = None
    print("RFM69: Detected")
    print(f"Frequency: {rfm69.frequency_mhz}MHz")
    print(f"Bit rate: {rfm69.bitrate}bit/s")
    print(f"Baud rate: {BAUD_RATE}baud/s")
    print(f"Frequency deviation: {rfm69.frequency_deviation}hz") 
    print(f"Tx_Power: {rfm69.tx_power}dBm")
    print(f"Temperature: {rfm69.temperature}C")
except RuntimeError as error:
    print("RFM69: ERROR")
    print("RFM69 Error:", error)
    rfm69 = None


# Create a thread for the key listener
key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
key_listener_thread.start()


# Run the main event loop
main_event_loop()

# Main loop
def main_event_loop():
    while True:
        packet = None
        if rfm69 is not None:
                # Check for incoming packets
            packet = rfm69.receive()
            if packet is not None:
                prev_packet=packet
                try:
                    new_packet = packet.decode("utf-16")
                    print("Received:", new_packet)
                    prepend_new_row(new_packet)
                except UnicodeDecodeError:
                    print("Received (raw):", packet)
            else:
                print('-Waiting for packet-')

        else:
            print("rfm69 is none")
        time.sleep(1)

        if not btnA.value:
            button_a_data = bytes("","utf-16")
            rfm69.send(button_a_data)
            print('Sent Button A!')

        time.sleep(1)


def listen_for_keys(stdscr):
    curses.cbreak()  # Enable cbreak mode
    stdscr.keypad(True)  # Enable keypad input
    stdscr.addstr("Listening for key presses. Press 'q' to quit.\n")
    stdscr.addstr("Press 'u' to update screen.\n")
    

    while True:
        # Physical button presses?
        if not btnA.value:
            button_a_data = bytes("test","utf-16")
            rfm69.send(button_a_data)
            print('Sent Button A!')
        
        # keyboard button presses
        key = stdscr.getch()  # Wait for a key press
        stdscr.addstr(f"You pressed: {chr(key)}\n")
        if key == ord('u'):
            send_data_test()
            print('Sent data test')

        if key == ord('q'):  # Exit if 'q' is pressed
            break


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
    prepend_new_row(new_data)


def prepend_new_row(new_data):
    # 1) Read the existing CSV file entirely
    if not os.path.exists(CSV_PATH):
        print(f"Could not find data.csv at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-16", newline="") as csvfile:
        reader = csv.reader(csvfile)
        all_rows = list(reader)

    if len(all_rows) == 0:
        print("data.csv appears empty or malformed.")
        return

    # 2) The first row is always the header
    header = all_rows[0]
    old_rows = all_rows[1:]  # everything after the header

    # 3) Build the new row in the exact same column order as the header
    new_row = []
    for col_name in header:
        if col_name in new_data:
            new_row.append(new_data[col_name])
        else:
            new_row.append("")  # leave blank if missing

    # 4) Prepend the new row—keeping header on top, then new_row, then old_rows
    updated_rows = [header, new_row] + old_rows

    # 5) Overwrite data.csv with the new content:
    with open(CSV_PATH, "w", encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)

    print("data.csv updated successfully. New row was prepended.")

# Wait for the key listener thread to finish
key_listener_thread.join()
print("Exiting...")
