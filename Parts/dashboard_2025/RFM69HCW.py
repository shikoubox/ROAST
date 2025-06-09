import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69


# RFM69 Configuration
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

while True:
    # Attempt to set up the RFM69 Module
    try:
        rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
        print("RFM69: Detected")
    except RuntimeError as error:
        print("RFM69: ERROR")
        print("RFM69 Error:", error)

    time.sleep(0.1)

