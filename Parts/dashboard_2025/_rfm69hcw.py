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

# Message hallola
messages = ["System init...", "Waiting for data...", "Packet received!", "RSSI: -42 dBm"]


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
    print_console(stdscr)

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
                rssi = rfm69.last_rssi  # This is your most accurate RSSI reading
                log_message("Received signal strength:", rssi, "dBm")

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
        print_console(std_scr)
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
    #prepend_new_row(new_data)

def print_console(stdscr):
    curses.curs_set(0)  # Hide cursor

    height, width = 10, 50  # Console window size
    start_y, start_x = 5, 20  # Console window position
    
    console_win = curses.newwin(height, width, start_y, start_x)
    console_win.box()

    # Use Unicode box-drawing characters for fancy borders
    #tl = '╭'
    #tr = '╮'
    #bl = '╰'
    #br = '╯'
    #h  = '─'
    #v  = '│'
    
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    #console_win.border(v, v, h, h, tl, tr, bl, br)
    console_win.border('#')


    for i, msg in enumerate(messages):
        console_win.addstr(i + 1, 2, msg)  # +1 and +2 to not write over the border
        console_win.refresh()
        curses.napms(1000)  # wait 1 second

    console_win.getch()  # Wait for user input
    
def log_message(msg):
    if len(messages) >= max_lines:
        messages.pop(0)  # Remove oldest
    messages.append(msg)

    console_win.clear()
    console_win.box()

    for i, m in enumerate(messages):
        console_win.addstr(i + 1, 2, m[:width - 4])  # Truncate if too long

    console_win.refresh()

key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
key_listener_thread.start()

# Run the main event loop
curses.wrapper(main_event_loop)

# Wait for the key listener thread to finish
key_listener_thread.join()

