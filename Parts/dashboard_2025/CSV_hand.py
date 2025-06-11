import csv
import os
import sys

# Path to data.csv
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "data.csv")

def prepend_new_row(new_data):

    # Read entire file as raw bytes (rb)
    if not os.path.exists(CSV_PATH):
        print(f"{CSV_PATH} file not found, creating new CSV with header only from new_data keys.")
        headers = list(new_data.keys())
        rows = [headers]
    else:
        with open(CSV_PATH, "rb") as f:
            raw = f.read()

        # Detect Byte order mark (BOM) + decoding
        if raw.startswith(b'\xff\xfe'):
            # UTF-16 LE BOM
            body = raw[2:]
            encoding = 'utf-16-le'
        elif raw.startswith(b'\xfe\xff'):
            # UTF-16 BE BOM
            body = raw[2:]
            encoding = 'utf-16-be'
        else:
            # No BOM, assume UTF-8
            body = raw
            encoding = 'utf-8'

        print(f"Detected encoding: {encoding}")

        # Decode and parse CSV
        try:
            text = body.decode(encoding)
        except UnicodeDecodeError as e:
            print(f" Decode error: {e}", file=sys.stderr)
            return

        reader = csv.reader(text.splitlines())
        all_rows = list(reader)
        if not all_rows:
            print(" data.csv appears empty or malformed.", file=sys.stderr)
            return

        headers = all_rows[0]
        rows = [headers] + all_rows[1:] # Keep header and existing rows

    # Build new row
    new_row = [ new_data.get(col, "") for col in headers ]

    # Prepend new row
    updated_rows = [rows[0], new_row] + rows[1:]

    # Write back out as UTF-16 LE with BOM
    try:
        with open(CSV_PATH, "wb") as f:
            # write UTF-16LE BOM
            f.write(b'\xff\xfe')
            for row in updated_rows:
                line = ",".join(row) + "\n"
                f.write(line.encode('utf-16-le'))
    except Exception as e:
        print(f"Error writing {CSV_PATH}: {e}", file=sys.stderr)
        return
    print("data.csv updated successfully. New row prepended.")

# Example usage:
if __name__ == "__main__":
    # Example data; in practice, build this dict from your CAN-to-CSV values
    example_data = {
        'current_temp':    '3',
        'cooling_temp':    '4',
        'motor_usage':     '5',
        'speed':           '6',
        'wh_total':        '7',
        'distance':        '8',
        'solar_output':    '9',
        'brake_status':    '10',
        'tyre_lf':         '11',
        'tyre_rf':         '12',
        'tyre_lr':         '13',
        'tyre_rr':         '14',
        'module1_percent': '15',
        'module1_voltage': '16',
        'm1c1':            '17',
        'm1c2':            '18',
        'm1c3':            '19',
        'm1c4':            '20',
        'm1c5':            '21',
        'm1c6':            '22',
        'm1c7':            '23',
        'm1c8':            '24',
        'module2_percent': '25',
        'module2_voltage': '26',
        'm2c1':            '27',
        'm2c2':            '28',
        'm2c3':            '29',
        'm2c4':            '30',
        'm2c5':            '31',
        'm2c6':            '32',
        'm2c7':            '33',
        'm2c8':            '34',
        'battery_percent': '35',
        'battery_voltage': '36',
    }
    prepend_new_row(example_data)
