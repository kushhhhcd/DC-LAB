import csv
from pathlib import Path

CSV_FILE = "events.csv"
FIELDS = ["event_id", "process_id", "event_type", "message_to", "initial_clock"]

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["E1", "P1", "SEND", "P2", 0],
                ["E2", "P2", "RECEIVE", "P1", 0],
                ["E3", "P1", "LOCAL", "", 0],
                ["E4", "P2", "LOCAL", "", 0],
            ])

def main():
    create_sample()
    clocks = {}
    # Queue of sent timestamps, indexed by receiver process.
    messages = {}
    results = []

    with open(CSV_FILE, newline="") as f:
        events = list(csv.DictReader(f))

    for event in events:
        eid = event["event_id"]
        process = event["process_id"].strip()
        kind = event["event_type"].strip().upper()
        message_to = event["message_to"].strip()
        clocks.setdefault(process, int(event["initial_clock"] or 0))

        if kind == "RECEIVE":
            queue = messages.get(process, [])
            received_time = queue.pop(0) if queue else 0
            clocks[process] = max(clocks[process], received_time) + 1
        else:
            clocks[process] += 1

        timestamp = clocks[process]
        results.append((timestamp, process, eid))
        print(f"{eid}: {process} {kind}, Lamport clock = {timestamp}")

        if kind == "SEND" and message_to:
            messages.setdefault(message_to, []).append(timestamp)

    print("\nTotal order (timestamp, then process ID):")
    for timestamp, process, eid in sorted(results):
        print(f"{eid} -> ({timestamp}, {process})")

if __name__ == "__main__":
    main()
