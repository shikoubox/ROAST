# radio_module/radio_module.py
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import os
import sys
import random
import encoding
import curses
import threading
import csv_handler
import rfm69_utils
import argparse
import graphics
from graphics import log_message


# Global exit flag
exit_program = False
rfm69 = None


# Non-Verbose main loop
def main_loop(verbose = False):
    global exit_program
    global rfm69

    rfm69 = rfm69_utils.initialise()

    if rfm69 is None:
        print("[ERROR] Failed to initialize RFM69 module")
        return

    while not exit_program:
        packet = None
        # Check for incoming packets
        try:
            packet = rfm69_utils.check_for_packets()
            if packet:
                print(f"[INFO] Main loop got packet: {packet} (len={len(packet)})")
                if len(packet) == 3:
                    try:
                        time.sleep(1)
                        csv_handler.cmd_bits(packet)
                        print("[INFO] Processed 22-bit packet")
                    except Exception as e:
                        print(f"[ERROR] Failed in cmd_bits: {e}")
                else:
                    print(f"[INFO] Packet not 3 bytes, skipping processing")
            elif verbose:
                print("[Waiting for packet]")
                time.sleep(0.3)
        except Exception as e:
            print(f"[ERROR] Packet handler crash: {e}")


# TUI curses main loop
def main_event_loop(stdscr):
    global exit_program
    global rfm69
    graphics.print_header()

    rfm69 = rfm69_utils.initialise()

    if rfm69 is None:
        log_message("[ERROR] Failed to initialize RFM69 module")
        return

    graphics.update_rfmdata(rfm69)

    while not exit_program:
        stdscr.addstr(0, 2, "RFM69 Receiver - Press 'q' to quit. Otherwise 'w' 'e' 'r' 't'")
        graphics.print_console()
        packet = None
        
        # Check for incoming packets
        try:
            packet = rfm69_utils.check_for_packets()
            if packet:
                log_message(f"[INFO] Main loop got packet: {packet} (len={len(packet)})")
                if len(packet) == 3:
                    try:
                        time.sleep(1)
                        csv_handler.cmd_bits(packet)
                        log_message("[INFO] Processed 22-bit packet")
                    except Exception as e:
                        log_message(f"[ERROR] Failed in cmd_bits: {e}")
                else:
                    log_message(f"[INFO] Packet not 3 bytes, skipping processing")
            else:
                stdscr.addstr(2,3,"[Waiting for packet]")
                stdscr.refresh()
                time.sleep(1)
                stdscr.addstr(2,3,"[                  ]")
        except Exception as e:
            log_message(f"[ERROR] Packet handler crash: {e}")

        stdscr.refresh()

# Input thread for TUI mode.
def listen_for_keys(stdscr):
    global exit_program
    curses.cbreak()  # Enable cbreak mode
    stdscr.keypad(True)  # Enable keypad input
    stdscr.refresh() 

    while not exit_program:
        stdscr.addstr(2,29, "[Listening for keypress]")

        key = stdscr.getch()  # Wait for a key press
        log_message(f"[INFO] You pressed: {chr(key)}")
        stdscr.addstr(2,29, "[                      ]")
        
        if key == ord('w'):
            try:
                log_message('[INFO] Sending "super message" by clicking keyboard')
                rfm69_utils.send_string_packet("super message")
            except Exception as e:
                log_message(f"{e}")

        if key == ord('e'):
            log_message('[INFO] Encoding message by clicking keyboard')
            try:
                b = encoding.encode_to_bytes(2,69.69)
                message, index = encoding.bytes_to_message(b)
                log_message(f"{index}: {message} / {encoding.decode_float16(message)}")
                csv_handler.cmd_bits(b)
                value = random.randint(0,420)
                index = random.randint(2,6)
                csv_handler.cmd_bits(encoding.encode_to_bytes(index, value))
            except Exception as e:
                log_message(f"{e}")
            

        if key == ord('q'):  # Exit if 'q' is pressed
            stdscr.clear()
            stdscr.addstr(3,4,"Exiting...")
            stdscr.refresh()
            exit_program = True # Set the exit flag

        if key == ord('t'):
            try:
                log_message("[INFO] Trying to send packet with 69 on index 3.")
                b = encoding.encode_to_bytes(3,69)
                rfm69_utils.send_byte_packet(b)
                log_message("[SUCCESS] Sent dataset test over radio!")

            except Exception as e:
                log_message(f"[ERROR] Failed to send test data: {e}")
                stdscr.addstr(27,0,f"{e}")

        if key == ord('r'):
            try:
                value = random.randint(0,420)
                index = random.randint(0,30)
                log_message(f"[INFO] Trying to send packet with value {value} on index {index}.")
                b = encoding.encode_to_bytes(index,value)
                rfm69_utils.send_byte_packet(b)
                log_message("[SUCCESS] Sent dataset test over radio!")

            except Exception as e:
                log_message(f"[ERROR] Failed to send test data: {e}")
                stdscr.addstr(27,0,f"{e}")

# Parser for running program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Radio Module CLI")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='show the version of the program')
    # Parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-V', '--verbose', action='store_true', help='run the program verbose')
    parser.add_argument('-t', '--tui', action='store_true', help='run program with terminal interface')

    # Parse the arguments
    args, unknown = parser.parse_known_args()

    # Handle unknown commands
    if unknown:
        print(f"Unknown command: {' '.join(unknown)}", file=sys.stderr)
        sys.exit(1)

    if args.tui:
            key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
            key_listener_thread.start()
            # Wait for the key listener thread to finish
            key_listener_thread.join()
            curses.wrapper(main_event_loop) # Run the curses main event loop
    elif args.verbose:
            verbose = True
            main_loop(verbose)
    else:
            main_loop(False)
            
