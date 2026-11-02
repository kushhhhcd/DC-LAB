import csv
from pathlib import Path

CSV_FILE = "vector_events.csv"
FIELDS = ["event_id", "process_id", "event_action", "target_process"]
PROCESSES = ["P1", "P2", "P3"]

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["E1", "P1", "SEND", "P2"],
                ["E2", "P2", "RECEIVE", "P1"],
                ["E3", "P2", "LOCAL", ""],
                ["E4", "P3", "LOCAL", ""],
                ["E5", "P1", "LOCAL", ""],
            ])

def happens_before(a, b):
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))

def main():
    create_sample()
    clocks = {p: [0, 0, 0] for p in PROCESSES}
    messages = {}  # destination process -> queued message vector
    event_vectors = []

    with open(CSV_FILE, newline="") as f:
        events = list(csv.DictReader(f))

    for event in events:
        eid = event["event_id"]
        process = event["process_id"].strip()
        action = event["event_action"].strip().upper()
        target = event["target_process"].strip()

        if process not in clocks:
            print(f"Skipping {eid}: unknown process {process}")
            continue

        i = PROCESSES.index(process)
        clocks[process][i] += 1

        if action == "RECEIVE":
            # For RECEIVE rows, target_process identifies the sender.
            queue = messages.get(process, [])
            if queue:
                sent_vector = queue.pop(0)
                clocks[process] = [max(x, y) for x, y in zip(clocks[process], sent_vector)]
                clocks[process][i] += 1
            else:
                print(f"Warning: no queued message for {process} at {eid}.")
        elif action == "SEND":
            # For SEND rows, target_process identifies the receiver.
            if target in clocks:
                messages.setdefault(target, []).append(clocks[process].copy())

        vector = clocks[process].copy()
        event_vectors.append((eid, vector))
        print(f"{eid} ({process}, {action}) -> {vector}")

    print("\nCausal relationship between event pairs:")
    for i in range(len(event_vectors)):
        for j in range(i + 1, len(event_vectors)):
            id1, v1 = event_vectors[i]
            id2, v2 = event_vectors[j]
            if happens_before(v1, v2):
                relation = f"{id1} -> {id2} (causally precedes)"
            elif happens_before(v2, v1):
                relation = f"{id2} -> {id1} (causally precedes)"
            else:
                relation = f"{id1} || {id2} (concurrent)"
            print(relation)

if __name__ == "__main__":
    main()
