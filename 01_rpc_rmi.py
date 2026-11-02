import csv
from pathlib import Path

CSV_FILE = "rpc_calls.csv"
FIELDS = ["call_id", "client_name", "method_name", "param_value", "timestamp"]

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                [101, "Client_A", "processData", 450, "10:00:01"],
                [102, "Client_B", "square", 12, "10:00:02"],
                [103, "Client_C", "double", 25, "10:00:03"],
            ])

# These functions represent procedures available on the remote server.
def processData(value):
    return value * 2

def square(value):
    return value ** 2

def double(value):
    return value * 2

def addTen(value):
    return value + 10

SERVER_METHODS = {
    "processData": processData,
    "square": square,
    "double": double,
    "addTen": addTen,
}

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        for call in csv.DictReader(f):
            method = call["method_name"]
            value = float(call["param_value"])
            print(f"\n[DISPATCH] {call['client_name']} invokes {method} (Call {call['call_id']})")

            if method not in SERVER_METHODS:
                print(f"[SERVER] ERROR: Method '{method}' is not registered.")
                continue

            print(f"[MARSHALLING] Sending parameter: {value}")
            result = SERVER_METHODS[method](value)
            print(f"[SERVER EXECUTION] {method}({value})")
            print(f"[RETURN] Result sent to client: {result}")

if __name__ == "__main__":
    main()
