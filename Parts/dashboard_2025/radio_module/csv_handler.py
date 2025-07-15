#!/usr/bin/env python3
# radio_module/csv_handler.py

import csv
import os
import sys
import re
import encoding

# Define the path to the parent folder
parent_folder = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the current script

# Define the path to the subfolder and the data file
subfolder = 'data'  # Replace with your subfolder name
data_file = 'data.csv'    # Replace with your data file name

# Construct the full path to the data file
# CSV_PATH = os.path.join(parent_folder, subfolder, data_file)
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'data.csv')


# Reads the CSV_PATH and returns a list of rows, or None if the file does not exist.
def _read_rows():
    if not os.path.exists(CSV_PATH):
        return None, 'utf-16'
    raw = open(CSV_PATH, 'rb').read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        body = raw[2:]; encoding = 'utf-16'
    elif raw.startswith(b'\xef\xbb\xbf'):
        body = raw[3:]; encoding = 'utf-8'
    else:
        body = raw; encoding = 'utf-8'
    try:
        text = body.decode(encoding)
    except Exception as e:
        print(f"ERROR: cannot decode {CSV_PATH}: {e}", file=sys.stderr)
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        print("ERROR: data.csv is empty or malformed", file=sys.stderr)
    return rows, encoding

def _write_rows(rows, encoding):
    # Overwrite CSV_PATH in given encoding (utf-16 emits BOM)
    with open(CSV_PATH, 'w', encoding=encoding, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# Update only the first data row (row 1)
def cmd_update(pairs):
    rows, enc = _read_rows()
    if rows is None:
        # New file: header from pairs, then a data row
        headers = list(pairs.keys())
        current = [pairs.get(h, '') for h in headers]
        rows = [headers, current]
    else:
        headers = rows[0]
        if len(rows) < 2:
            rows.append([''] * len(headers))
        for k, v in pairs.items():
            if k in headers:
                rows[1][headers.index(k)] = v
    _write_rows(rows, enc)
    print("data.csv: current row updated", file=sys.stderr)

# Snapshot row one into history (prepend it right under header), preserving all older rows.
def cmd_log():
    rows, enc = _read_rows()
    if rows is None or len(rows) < 2:
        print("ERROR: no current row to log", file=sys.stderr)
    header = rows[0]
    current = rows[1]
    new_rows = [header, current] + rows[1:]
    _write_rows(new_rows, enc)
    print("data.csv: snapshot logged", file=sys.stderr)

# Update first data row, with a bit string as argument
def cmd_bits(bitstr):
    if isinstance(bitstr, (bytes, bytearray)):
        try:
            int_val = int.from_bytes(bitstr, 'big')
            bitstr = f"{int_val:0{len(bitstr)*8}b}"
        except Exception as e:
            raise Exception(f"Byte-to-bitstring conversion failed: {e}")

    if not isinstance(bitstr, str):
        raise Exception(f"Input to cmd_bits must be str, bytearray or bytes, got {type(bitstr)}")

    if len(bitstr) < 16:
        raise Exception("Bitstring too short (< 16 bits)")

    try:
        # If input is bytes, convert to bitstring
        if isinstance(bitstr, bytes):
            bitstr = f"{int.from_bytes(bitstr, 'big'):0{len(bitstr)*8}b}"

        # The decoder takes 8 leading bits as the index value, and the last 16 or more bits as the value (at least 16 bits for value)
        if len(bitstr) < 16:
            print("[ERROR] bitstring too short (need >=16 bits)", file=sys.stderr)
        val_bits = bitstr[-16:]
        idx_bits = bitstr[:-16] or '0'
        # Ensure index bits no more than 8 bits (truncate higher bits)
        idx_bits = idx_bits[-8:].rjust(8, '0')
        idx = int(idx_bits, 2)
        val = encoding.decode_float16(int(val_bits, 2))
        rows, _ = _read_rows()
        if rows is None:
            print("[ERROR] cannot bit-update without existing header", file=sys.stderr)
            raise Exception("[ERROR] cannot bit-update without existing header")
        headers = rows[0]
        if idx < 0 or idx >= len(headers):
            raise Exception(f"index {idx} out of range (0–{len(headers)-1})")
        key = headers[idx]
        cmd_update({ key: str(val) })
    except Exception as e:
        raise Exception(f"{e}")

def usage():
    print("Usage:", file=sys.stderr)
    print("  csv_handler.py update key1=val1 [key2=val2 ...]", file=sys.stderr)
    print("  csv_handler.py log", file=sys.stderr)
    print("  csv_handler.py <binary-string>   # >=16 bits: [idx-bits][16-bit value]", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    else:
        cmd = sys.argv[1]
        if re.fullmatch(r'[01]+', cmd):
            cmd_bits(sys.argv[1])
        if cmd == "update":
            if len(sys.argv) < 3:
                usage()
            pairs = {}
            for tok in sys.argv[2:]:
                if "=" not in tok:
                    print(f"ERROR: invalid token `{tok}`", file=sys.stderr)
                k, v = tok.split("=", 1)
                pairs[k] = v
            cmd_update(pairs)
        elif cmd == "log":
            cmd_log()
        else:
            usage()
