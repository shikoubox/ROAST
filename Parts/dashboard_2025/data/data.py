# data/data.py

import csv
import os

# This script expects data.csv to live in the same directory.
CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

# We keep a simple “counter.txt” file alongside data.csv to remember
# which value “i” should be on the next run. If no counter file exists, it starts at 0.
COUNTER_PATH = os.path.join(os.path.dirname(__file__), "counter.txt")

def read_counter():
    # Read the integer value of i from counter.txt. If missing, return 0.
    if not os.path.exists(COUNTER_PATH):
        return 0
    with open(COUNTER_PATH, "r", encoding="utf-8") as f:
        text = f.read().strip()
        try:
            return int(text)
        except ValueError:
            return 0

def write_counter(i_value):
    # Write the integer i_value back to counter.txt.
    with open(COUNTER_PATH, "w", encoding="utf-8") as f:
        f.write(str(i_value))

def prepend_new_row():
    # Read and increment the counter `i`
    i = read_counter()
    i += 1
    write_counter(i)

    # Build a new‐data dictionary   
    new_data = {
        "current_temp":     f"3{i}",
        "cooling_temp":     f"4{i}",
        "motor_usage":      f"5{i}",
        "speed":            f"6{i}",
        "wh_total":         f"7{i}",
        "distance":         f"8{i}",
        "solar_output":     f"9{i}",
        "brake_status":     f"10{i}",
        "tyre_lf":          f"11{i}",
        "tyre_rf":          f"12{i}",
        "tyre_lr":          f"13{i}",
        "tyre_rr":          f"14{i}",
        "module1_percent":  f"15{i}",
        "module1_voltage":  f"16{i}",
        "m1c1":             f"17{i}",
        "m1c2":             f"18{i}",
        "m1c3":             f"19{i}",
        "m1c4":             f"20{i}",
        "m1c5":             f"21{i}",
        "m1c6":             f"22{i}",
        "m1c7":             f"23{i}",
        "m1c8":             f"24{i}",
        "module2_percent":  f"25{i}",
        "module2_voltage":  f"26{i}",
        "m2c1":             f"27{i}",
        "m2c2":             f"28{i}",
        "m2c3":             f"29{i}",
        "m2c4":             f"30{i}",
        "m2c5":             f"31{i}",
        "m2c6":             f"32{i}",
        "m2c7":             f"33{i}",
        "m2c8":             f"34{i}",
        "battery_percent":  f"35{i}",
        "battery_voltage":  f"36{i}",
        "radio_dBm":        f"37{i}",
    }

    # Read the existing CSV file entirely
    if not os.path.exists(CSV_PATH):
        print(f"Could not find data.csv at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile)
        all_rows = list(reader)

    if len(all_rows) == 0:
        print("data.csv appears empty or malformed.")
        return

    # The first row is the header
    header = all_rows[0]
    old_rows = all_rows[1:]

    # Build the new row in the exact same column order as the header
    new_row = []
    for col_name in header:
        if col_name in new_data:
            new_row.append(new_data[col_name])
        else:
            new_row.append("")  # Anly missing value is left empty

    # Prepend the new row—keeping header on top, then new_row, then old_rows
    updated_rows = [header, new_row] + old_rows

    # Overwrite data.csv with the new data
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)

    print("data.csv updated successfully. New row was prepended.")

if __name__ == "__main__":
    prepend_new_row()
