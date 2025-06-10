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

# Initialize RFM69 once
try:
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUD_RATE, high_power=True)
    rfm69.bitrate = BIT_RATE
    prev_packet = None
except RuntimeError as error:
    print("RFM69: ERROR")
    print("RFM69 Error:", error)
    rfm69 = None



# Main loop
def main_event_loop(stdscr):
    global exit_program
    stdscr.clear()

    while not exit_program:
        stdscr.addstr(0, 0, "RFM69 Receiver - Press 'q' to quit.")
        packet = None
        if rfm69 is not None:
            stdscr.addstr(0, 42, "RFM69: Detected")
            stdscr.addstr(1, 42, f"Frequency: {rfm69.frequency_mhz}MHz")
            stdscr.addstr(2, 42, f"Bit rate: {rfm69.bitrate}bit/s")
            stdscr.addstr(3, 42, f"Baud rate: {BAUD_RATE}baud/s")
            stdscr.addstr(4, 42, f"Frequency deviation: {rfm69.frequency_deviation}hz") 
            stdscr.addstr(5, 42, f"Tx_Power: {rfm69.tx_power}dBm")
#           try:
#               stdscr.addstr(6, 42, f"Temperature: {rfm69.temperature}C")
#           except RuntimeError as error:
#               stdscr.addstr(6,42, f"{error}")

            # Check for incoming packets
            

            packet = rfm69.receive()
            if packet is not None:
                prev_packet=packet
                try:
                    new_packet = packet.decode("utf-16")
                    stdscr.addstr(2, 0, f"Received: {new_packet}")
                    prepend_new_row(stdscr, new_packet)
                except UnicodeDecodeError:
                    stdscr.addstr(2, 0, f"Received (raw): {packet}")
            else:
                stdscr.addstr(2, 2, "-Waiting for packet-")
                stdscr.refresh()
                time.sleep(1)
                stdscr.addstr(2, 2, "-                  -")
                

        else:
            stdscr.addstr(2, 0, "rfm69 is none")
        stdscr.refresh()
        time.sleep(2)

def listen_for_keys(stdscr):
    global exit_program
    curses.cbreak()  # Enable cbreak mode
    stdscr.keypad(True)  # Enable keypad input
    stdscr.refresh() 

    while not exit_program:
        stdscr.addstr(7, 8, "Now listening for key presses..")
        stdscr.addstr(8, 8, "Press 'q' to quit.")
        stdscr.addstr(9, 8, "Press 'u' to update screen.")

        # Physical button presses?
        if not btnA.value:
            button_a_data = bytes("test","utf-16")
            rfm69.send(button_a_data)
            stdscr.addstr(6,0, 'Sent data test')
        
        key = stdscr.getch()  # Wait for a key press
        stdscr.addstr(7,8,f"You pressed: {chr(key)}\n")
        stdscr.addstr(8, 8, "                  ")
        stdscr.addstr(9, 8, "                           ")
        # keyboard button presses
        if key == ord('u'):
            send_data_test(stdscr)

        if key == ord('q'):  # Exit if 'q' is pressed
            stdscr.clear()
            stdscr.addstr(3,4,"Exiting...")
            stdscr.refresh()
            exit_program = True # Set the exit flag


def send_data_test(stdscr):
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
    prepend_new_row(stdscr, new_data)


def prepend_new_row(stdscr, new_data):
    # 1) Read the existing CSV file entirely
    if not os.path.exists(CSV_PATH):
        stdscr.addstr(10, 0, f"Could not find data.csv at {CSV_PATH}")
        stdscr.refresh()
        stdscr.getch()
        return

    # Read the file in binary mode to check for BOM
    with open(CSV_PATH, "rb") as csvfile:
        content = csvfile.read()
        # Check for BOM and decode accordingly
        if content.startswith(b'\xff\xfe'):
            content = content[2:]  # Remove BOM for little-endian
            encoding = 'utf-16'
        elif content.startswith(b'\xfe\xff'):
            content = content[2:]  # Remove BOM for big-endian
            encoding = 'utf-16'
        else:
            # If no BOM, assume UTF-8 or another encoding
            encoding = 'utf-8'
            with open(CSV_PATH, mode="w", encoding='utf-16', newline='') as outfile:
                writer = csv.writer(outfile)
                for row in content:
                    writer.writerow(row)
                stdscr.addstr(11,0,f"Tried updating .csv from {encoding} to utf-16")
        
        stdscr.addstr(10,0,f"Encoding of .csv file was {encoding}")

    # Decode the content and read it as CSV
    decoded_content = content.decode(encoding)
    reader = csv.reader(decoded_content.splitlines())
    all_rows = list(reader)

    if len(all_rows) == 0:
        stdscr.addstr(8, 0, "data.csv appears empty or malformed.")
        stdscr.refresh()
        stdscr.getch()
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
    with open(CSV_PATH, "w", encoding=encoding, newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)

    stdscr.addstr(10, 0, "data.csv updated successfully. New row was prepended.")
    stdscr.refresh()
    time.sleep(1)
    stdscr.addstr(10, 0,"                                                     ")
    stdscr.refresh()



key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
key_listener_thread.start()

# Run the main event loop
curses.wrapper(main_event_loop)

# Wait for the key listener thread to finish
key_listener_thread.join()

