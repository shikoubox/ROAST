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

# Message hallola
messages = ["[INFO] System init..."]
height, width = 20, 80  # Console window size


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
        stdscr.addstr(0, 0, "RFM69 Receiver - Press 'q' to quit. - Press 'u t or s for different package tests")
        print_console(stdscr)
        packet = None
        if rfm69 is not None:
            stdscr.addstr(0, 50, "RFM69: Detected")
            stdscr.addstr(1, 50, f"Frequency: {rfm69.frequency_mhz}MHz")
            stdscr.addstr(2, 50, f"Bit rate: {rfm69.bitrate}bit/s")
            stdscr.addstr(3, 50, f"Baud rate: {BAUD_RATE}baud/s")
            stdscr.addstr(4, 50, f"Frequency deviation: {rfm69.frequency_deviation/1000}kHz") 
            stdscr.addstr(5, 50, f"Tx_Power: {rfm69.tx_power}dBm")
#           try:
#               stdscr.addstr(6, 42, f"Temperature: {rfm69.temperature}C")
#           except RuntimeError as error:
#               stdscr.addstr(6,42, f"{error}")

            # Check for incoming packets
            

            packet = rfm69.receive()
            if packet is not None:
                rssi = rfm69.last_rssi  # This is your most accurate RSSI reading
                log_message(f"[INFO] Received signal strength: {rssi} dBm")

                prev_packet=packet
                try:
                    new_packet = packet.decode("utf-16")
                    log_message(f"[INFO] Received: {new_packet}")
                    status = CSV_hand.prepend_new_row(new_packet)
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
        stdscr.addstr(2,25, "[INFO] Listening for keypress")

        # Physical button presses?
        if not btnA.value:
            button_a_data = bytes("test","utf-16")
            rfm69.send(button_a_data)
            log_message('[INFO] Sent data test by button click')
        
        key = stdscr.getch()  # Wait for a key press
        log_message(f"[INFO] You pressed: {chr(key)}\n")
        stdscr.addstr(2,25, "[    ]                       ")

        if key == ord('t'):
            try:
                log_message("[INFO] Preparing to send BIG dataset test...")
                
                test_data = get_data_test()
                log_message(f"[DEBUG] Generated test data: {str(test_data)[:80]}...")  # Only first 80 chars

                button_a_data = bytes(test_data, "utf-16")
                log_message("[DEBUG] Encoded data to bytes.")

                rfm69.send(button_a_data)
                log_message("[SUCCESS] Sent BIG dataset test over radio!")

            except Exception as e:
                log_message(f"[ERROR] Failed to send test data: {e}")
                with open("thread_error.log", "a") as f:
                    f.write(f"Exception in send BIG dataset test: {e}\n")

        if key == ord('s'):
            log_message('Sending "super message" by clicking keyboard')
            button_a_data = bytes("super message","utf-16")
            rfm69.send(button_a_data)
            log_message('Sent "super message"')


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

def print_header():
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 1, 1  # Console window position
    
    header_win = curses.newwin(3, width, start_y, start_x)

    # Use Unicode box-drawing characters for fancy borders
    tl = '+'#'╭'
    tr = '+'#'╮'
    bl = '+'#'╰'
    br = '+'#'╯'
    h  = '-'#'─'
    v  = '|'
    
    header_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    header_win.border(v, v, h, h, tl, tr, bl, br)




    header_win.refresh()


def print_console(stdscr):
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 5, 1  # Console window position
    
    console_win = curses.newwin(height, width, start_y, start_x)

    # Use Unicode box-drawing characters for fancy borders
    tl = '+'#'╭'
    tr = '+'#'╮'
    bl = '+'#'╰'
    br = '+'#'╯'
    h  = '-'#'─'
    v  = '|'
    
    console_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    console_win.border(v, v, h, h, tl, tr, bl, br)

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

