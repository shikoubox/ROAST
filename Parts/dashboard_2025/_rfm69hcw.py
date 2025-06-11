import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69
import os
import random
import data_mani
import curses
import curses_code
from curses_code import log_message
import threading
from data import CSV_hand
import RF69_module

# global exit flag
exit_program = False
rfm69 = None

# Button A
btnA = DigitalInOut(board.D17)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP


# Main loop
def main_event_loop(stdscr):
    global exit_program
    global rfm69
    curses_code.print_header()

    RF69_module.initialise()

    while not exit_program:
        stdscr.addstr(0, 2, "RFM69 Receiver - Press 'q' to quit. Otherwise 'b' 't' 'u' 's'")
        curses_code.print_console()
        packet = None
        
        try:
            # Check for incoming packets
            if RF69_module.check_for_packets() is None:
                stdscr.addstr(2,3,"[Waiting for packet]")
                stdscr.refresh()
                time.sleep(1)
                stdscr.addstr(2,3,"[                  ]")
        except Exception as e:
            log_message(f"[ERROR]: {e}")

        stdscr.refresh()


def listen_for_keys(stdscr):
    global exit_program
    curses.cbreak()  # Enable cbreak mode
    stdscr.keypad(True)  # Enable keypad input
    stdscr.refresh() 

    while not exit_program:
        stdscr.addstr(2,29, "[Listening for keypress]")

        # Physical button presses?
        if not btnA.value:
            try:
                RF69_module.send_string_packet("test")
            except Exception as e:
                log_message(f"{e}")
        
        key = stdscr.getch()  # Wait for a key press
        log_message(f"[INFO] You pressed: {chr(key)}")
        stdscr.addstr(2,29, "[                      ]")
        
        if key == ord('s'):
            try:
                log_message('[INFO] Sending "super message" by clicking keyboard')
                RF69_module.send_string_packet("super message")
            except Exception as e:
                log_message(f"{e}")

        if key == ord('b'):
            log_message('[INFO] Encoding message by clicking keyboard')
            try:
                b = data_mani.encode_to_bytes(16,1.5)
                log_message(f"[INFO] Message created: {b:022b}")
                message, index = data_mani.bytes_to_message(b)
                log_message(f"{index}: {message} / {data_mani.decode_float16(message)}")
            except Exception as e:
                log_message(f"{e}")

            try:
                byt = data_mani.encode_to_bytes(65,111221.541231)
                log_message(f"[INFO] Message created: {byt:022b}")
            except Exception as e:
                log_message(f"{e}")

        if key == ord('q'):  # Exit if 'q' is pressed
            stdscr.clear()
            stdscr.addstr(3,4,"Exiting...")
            stdscr.refresh()
            exit_program = True # Set the exit flag
'''
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
'''


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


key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
key_listener_thread.start()

# Run the main event loop
curses.wrapper(main_event_loop)

# Wait for the key listener thread to finish
key_listener_thread.join()

