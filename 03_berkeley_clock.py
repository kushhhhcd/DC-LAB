import csv
from pathlib import Path

CSV_FILE = "node_clocks.csv"
FIELDS = ["node_id", "clock_time_sec", "is_faulty"]

def to_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["N1", 3600, "FALSE"],
                ["N2", 3605, "FALSE"],
                ["N3", 3598, "FALSE"],
                ["N4", 3900, "TRUE"],
            ])

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        nodes = list(csv.DictReader(f))

    valid = []
    print("Polling node clocks:")
    for n in nodes:
        clock = float(n["clock_time_sec"])
        faulty = to_bool(n["is_faulty"])
        print(f"{n['node_id']}: {clock:.2f} sec")
        if faulty:
            print(f"  -> Discarding {n['node_id']} (marked faulty)")
        else:
            valid.append((n["node_id"], clock))

    if not valid:
        print("No valid clocks available.")
        return

    average = sum(clock for _, clock in valid) / len(valid)
    print(f"\nAverage time of valid nodes: {average:.2f} sec")
    print("Clock adjustments (positive = advance, negative = slow down):")
    for node_id, clock in valid:
        adjustment = average - clock
        print(f"{node_id}: {adjustment:+.2f} sec")

if __name__ == "__main__":
    main()
