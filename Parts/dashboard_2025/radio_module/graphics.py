#radio_module/graphics.py

import os
import random
import curses

# Curses settings
messages = ["[INFO] System init..."]
height, width = 20, 120  # Console window size
## Use Unicode box-drawing characters for fancy borders
h  = '-'#'─'
v  = '|'
c  = '+'

frequency = 0
bitrate = 0
baudrate = 0
frequency_deviation = 0
tx_power = 0

def print_rfmdata():
    global rfm69
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 1, width+1  # Console window position
    
    rfmdata_win = curses.newwin(height+4-start_y, 22, start_y, start_x)

    rfmdata_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    rfmdata_win.border(v, v, h, h, c, c, c, c)

    rfmdata_win.addstr(1, 1,  "RFM69    : Detected")
    rfmdata_win.addstr(3, 1, f"Frequency:")
    rfmdata_win.addstr(4, 1, f"{frequency} MHz")
    rfmdata_win.addstr(6, 1, f"Bit rate :")
    rfmdata_win.addstr(7, 1, f"{bitrate/1000} kbit/s")
    rfmdata_win.addstr(9, 1, f"Baud rate:")
    rfmdata_win.addstr(10,1, f"{baudrate} baud/s")
    rfmdata_win.addstr(12,1, f"Freq.dev.:") 
    rfmdata_win.addstr(13,1, f"{frequency_deviation/1000} kHz") 
    rfmdata_win.addstr(15,1, f"Tx_Power :")
    rfmdata_win.addstr(16,1, f"{tx_power} dBm")



    rfmdata_win.refresh()
\
def update_rfmdata_baudrate(_baudrate):
    baudrate = _baudrate
    print_rfmdata()

def update_rfmdata(_rfm69):
    #frequency = _rfm69.frequency_mhz
    #bitrate=_rfm69.bitrate
    #frequency_deviation = _rfm69.frequency_deviation
    #tx_power = _rfm69.tx_power
    print_rfmdata()


def print_header():
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 1, 0  # Console window position
    
    header_win = curses.newwin(3, width, start_y, start_x)

    header_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    header_win.border(v, v, h, h, c, c, c, c)

    header_win.refresh()


def print_console():
    curses.curs_set(0)  # Hide cursor

    start_y, start_x = 4, 0  # Console window position
    
    console_win = curses.newwin(height, width, start_y, start_x)

    
    # console_win.clear()
    # Custom border: (ls, rs, ts, bs, tl, tr, bl, br)
    console_win.border(v, v, h, h, c, c, c, c)

    for i, msg in enumerate(messages):
        console_win.addstr(i + 1, 2, msg)  # +1 and +2 to not write over the border

    console_win.refresh()
    
def log_message(msg):
    if len(messages) >= height-2:
        messages.pop(0)  # Remove oldest
    messages.append(msg[:width-3])

'''
key_listener_thread = threading.Thread(target=curses.wrapper, args=(listen_for_keys,))
key_listener_thread.start()

# Run the main event loop
curses.wrapper(main_event_loop)

# Wait for the key listener thread to finish
key_listener_thread.join()

'''
