import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm69
import graphics
from graphics import log_message
import csv_handler
import encoding

# Optional encryption (MUST match on both)
# rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

rfm69 = None

# Initialize RFM69 once
def initialise():
    global rfm69
    try:
        # RFM69 Configuration
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Define radio parameters.
        RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz
        BAUD_RATE=1000
        BIT_RATE=1000

        # Pass it to rfm module
        rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUD_RATE, high_power=True)
        rfm69.bitrate = BIT_RATE

        # Update graphics
        graphics.update_rfmdata_baudrate(BAUD_RATE)
        return rfm69
    except AttributeError as error:
        log_message("[ERROR] board not loaded properly: {error}")
    except RuntimeError as error:
        log_message("[ERROR] RFM69")
        log_message(f"[ERROR]: {error}")
        rfm69 = None
        return None




def check_for_packets():
    global rfm69
    if rfm69 is None:
        raise Exception("[WARNING] Trying to check for packets, without an initalised rfm69")

    packet = rfm69.receive()
    if packet is not None:
        rssi = rfm69.last_rssi
        log_message(f"[INFO] Received signal strength: {rssi} dBm")
        csv_handler.cmdbits(encoding.encode_to_bytes(36,rssi))
        log_message(f"[INFO] Raw packet bytes: {packet}")

        try:
            if len(packet) == 3:  # 22-bit = 3 bytes
                # Treat as binary payload
                log_message(f"[INFO] Interpreting as 22-bit binary payload")
                return packet

            else:
                # Try decoding as string
                try:
                    new_packet = packet.decode("utf-16")
                    log_message(f"[INFO] Received string: {new_packet}")
                    return new_packet
                except UnicodeDecodeError:
                    log_message(f"[WARNING] Failed to decode packet as UTF-16 string")

        except Exception as e:
            log_message(f"[ERROR] Exception in packet processing: {e}")
    else:
        return None


def send_string_packet(string):
    global rfm69
    if rfm69 is None:
        raise Exception("[WARNING] Trying to check for packets, without an initalised rfm69")
    else: 
        try:
            packet_data = bytes(string,"utf-16")
            rfm69.send(packet_data)
        except Exception as e:
            log_message(f"[ERROR] Failed to send data: {e}")

def send_byte_packet(byte_packet):
    global rfm69
    if rfm69 is None:
        raise Exception("[WARNING] Trying to check for packets, without an initalised rfm69")
    else: 
        try:
            rfm69.send(byte_packet)
        except Exception as e:
            log_message(f"[ERROR] Failed to send data: {e}")

