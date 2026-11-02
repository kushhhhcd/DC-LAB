import csv
from pathlib import Path

CSV_FILE = "bully_cluster.csv"
FIELDS = ["node_id", "is_alive", "is_current_coordinator"]

def to_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                [1, "TRUE", "FALSE"],
                [2, "TRUE", "FALSE"],
                [3, "FALSE", "TRUE"],
                [4, "TRUE", "FALSE"],
                [5, "TRUE", "FALSE"],
            ])

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        nodes = [
            {"id": int(r["node_id"]), "alive": to_bool(r["is_alive"]),
             "coordinator": to_bool(r["is_current_coordinator"])}
            for r in csv.DictReader(f)
        ]

    alive = sorted((n for n in nodes if n["alive"]), key=lambda n: n["id"])
    if not alive:
        print("No active nodes available.")
        return

    failed = [n for n in nodes if n["coordinator"] and not n["alive"]]
    if failed:
        print(f"Coordinator Node {failed[0]['id']} has failed.")
    else:
        print("Starting election (coordinator assumed unavailable).")

    # The lowest active node initiates; higher active nodes respond.
    initiator = alive[0]["id"]
    print(f"\nNode {initiator} detects coordinator failure and starts election.")

    higher = [n for n in alive if n["id"] > initiator]
    for node in higher:
        print(f"Node {initiator} -> Node {node['id']}: ELECTION")
        print(f"Node {node['id']} -> Node {initiator}: OK")

    leader = alive[-1]["id"]
    print(f"\nNode {leader} is the highest-ID active node.")
    for node in alive:
        if node["id"] != leader:
            print(f"Node {leader} -> Node {node['id']}: COORDINATOR")
    print(f"\nNew coordinator elected: Node {leader}")

if __name__ == "__main__":
    main()
