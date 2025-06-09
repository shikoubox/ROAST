import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69

# RFM69 Configuration
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize RFM69 once
try:
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 433.0)
    print("RFM69: Detected")
except RuntimeError as error:
    print("RFM69: ERROR")
    print("RFM69 Error:", error)
    rfm69 = None

# Main loop
while True:
    if rfm69 is not None:
        # Check for incoming packets
        packet = rfm69.receive()
        if packet is not None:
            try:
                print("Received:", packet.decode("utf-8"))
            except UnicodeDecodeError:
                print("Received (raw):", packet)
    time.sleep(0.1)

