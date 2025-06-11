#!/usr/bin/env python3
# data/CSV_hand.py

import csv
import os
import sys

# __file__ is .../dashboard_2025/data/CSV_hand.py
# We want .../dashboard_2025/data/data.csv — no extra "data" folder!
CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

def prepend_new_row(new_data):
    # Basic validation: must be a dict of str→str
    if not isinstance(new_data, dict):
        print("Error: new_data must be a dict", file=sys.stderr)
        return
    for k, v in new_data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            print(f"Error: invalid key/value in new_data: {k}: {v}", file=sys.stderr)
            return

    # 1) Read raw bytes to detect & strip BOM
    if not os.path.exists(CSV_PATH):
        print(f"{CSV_PATH} not found → creating new CSV with header only", file=sys.stderr)
        headers = list(new_data.keys())
        rows = [headers]
    else:
        with open(CSV_PATH, "rb") as f:
            raw = f.read()
        # detect BOM
        if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
            body = raw[2:]
            encoding = 'utf-16'
        elif raw.startswith(b'\xef\xbb\xbf'):
            body = raw[3:]
            encoding = 'utf-8'
        else:
            body = raw
            encoding = 'utf-8'

        print(f"Detected encoding: {encoding}", file=sys.stderr)

        try:
            text = body.decode(encoding)
        except Exception as e:
            print(f"Decode error: {e}", file=sys.stderr)
            return

        try:
            reader = csv.reader(text.splitlines())
            all_rows = list(reader)
            if not all_rows:
                print("Error: data.csv appears empty or malformed.", file=sys.stderr)
                return
        except Exception as e:
            print(f"CSV parse error: {e}", file=sys.stderr)
            return

        headers = all_rows[0]
        rows = [headers] + all_rows[1:]

    # 2) Build & prepend the new row in exactly the header order
    try:
        new_row = [ new_data.get(col, "") for col in headers ]
    except Exception as e:
        print(f"Error building new row: {e}", file=sys.stderr)
        return

    updated = [rows[0], new_row] + rows[1:]
    print(f"Total rows after prepend: {len(updated)}", file=sys.stderr)

    # 3) Write back out as UTF-16 (with BOM)
    try:
        with open(CSV_PATH, "w", encoding="utf-16", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(updated)
    except Exception as e:
        print(f"Error writing {CSV_PATH}: {e}", file=sys.stderr)
        return

    print(f"{CSV_PATH} updated (prepended new row)", file=sys.stderr)


if __name__ == "__main__":
    try:
        # Example usage; replace with your actual data source
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
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
