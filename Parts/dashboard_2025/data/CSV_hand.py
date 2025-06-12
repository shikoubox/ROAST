#!/usr/bin/env python3
# data/CSV_hand.py

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import os
import sys
import data_mani

# Path to data.csv (same folder)
CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

def _read_rows():
    """Return (rows, encoding). If file missing, return (None, 'utf-16')."""
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
        sys.exit(1)
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        print("ERROR: data.csv is empty or malformed", file=sys.stderr)
        sys.exit(1)
    return rows, encoding

def _write_rows(rows, encoding):
    """Overwrite CSV_PATH in given encoding (utf-16 emits BOM)."""
    with open(CSV_PATH, 'w', encoding=encoding, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def cmd_update(pairs):
    """Update only the first data row (row 1)."""
    rows, enc = _read_rows()
    if rows is None:
        # new file: header from pairs, then a data row
        headers = list(pairs.keys())
        current = [pairs.get(h, '') for h in headers]
        rows = [headers, current]
    else:
        headers = rows[0]
        # ensure row 1 exists
        if len(rows) < 2:
            rows.append([''] * len(headers))
        for k, v in pairs.items():
            if k in headers:
                rows[1][headers.index(k)] = v
    _write_rows(rows, enc)
    print("data.csv: current row updated", file=sys.stderr)

def cmd_update_22(byte22):
    """Update only the first data row (row 1)."""
    rows, enc = _read_rows()
    if rows is None:
        # new file: header from pairs, then a data row
        headers = list(pairs.keys())
        current = [pairs.get(h, '') for h in headers]
        rows = [headers, current]
    else:
        headers = rows[0]
        # ensure row 1 exists
        if len(rows) < 2:
            rows.append([''] * len(headers))
        v, k = data_mani.bytes_to_message(byte22)

        if k in headers:
            rows[1][headers.index(k)] = v
    _write_rows(rows, enc)
    print("data.csv: current row updated", file=sys.stderr)



def cmd_log():
    """
    Snapshot row 1 into history (prepend it right under header),
    preserving all older rows.
    """
    rows, enc = _read_rows()
    if rows is None or len(rows) < 2:
        print("ERROR: no current row to log", file=sys.stderr)
        sys.exit(1)
    header = rows[0]
    current = rows[1]
    # build new list: header, current snapshot, then all existing rows AFTER header
    new_rows = [header, current] + rows[1:]
    _write_rows(new_rows, enc)
    print("data.csv: snapshot logged", file=sys.stderr)

def usage():
    print("Usage:", file=sys.stderr)
    print("  CSV_hand.py update key1=val1 [key2=val2 ...]", file=sys.stderr)
    print("  CSV_hand.py log", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    cmd = sys.argv[1]
    if cmd == "update":
        if len(sys.argv) < 3:
            usage()
        pairs = {}
        for tok in sys.argv[2:]:
            if "=" not in tok:
                print(f"ERROR: invalid token `{tok}`", file=sys.stderr)
                sys.exit(1)
            k, v = tok.split("=", 1)
            pairs[k] = v
        cmd_update(pairs)
    elif cmd == "log":
        cmd_log()
    else:
        usage()
