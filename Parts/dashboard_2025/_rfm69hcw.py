import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# RFM69 Configuration
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Optional encryption (MUST match on both)
# rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

# Initialize RFM69 once
try:
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 433.0)
    prev_packet = None
    print("RFM69: Detected")
except RuntimeError as error:
    print("RFM69: ERROR")
    print("RFM69 Error:", error)
    rfm69 = None

# Main loop
while True:
    packet = None

    if rfm69 is not None:
        # Check for incoming packets
        packet = rfm69.receive()
        if packet is not None:
            prev_packet=packet
            try:
                print("Received:", packet.decode("utf-8"))
            except UnicodeDecodeError:
                print("Received (raw):", packet)
        else:
            print('-Waiting for packet-')

    time.sleep(1)

    if not btnA.value:
        button_a_data = bytes("Button A!\r\n","utf-8")
        rfm69.send(button_a_data)
        print('Sent Button A!')

    time.sleep(1)
