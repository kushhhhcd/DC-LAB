import csv
from pathlib import Path

CSV_FILE = "ring_nodes.csv"
FIELDS = ["node_id", "next_node_id", "is_active", "priority_rank"]

def to_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                [1, 2, "TRUE", 70],
                [2, 3, "TRUE", 85],
                [3, 4, "FALSE", 95],
                [4, 1, "TRUE", 90],
            ])

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        rows = list(csv.DictReader(f))

    nodes = {
        int(r["node_id"]): {
            "next": int(r["next_node_id"]),
            "active": to_bool(r["is_active"]),
            "priority": int(r["priority_rank"])
        } for r in rows
    }
    active_ids = [node_id for node_id, data in nodes.items() if data["active"]]
    if not active_ids:
        print("No active nodes in the ring.")
        return

    # Start at the smallest active node and follow next_node_id links.
    current = min(active_ids)
    token = []
    visited = set()
    print("Coordinator failure detected. Starting ring election...")
    while current not in visited and current in nodes:
        visited.add(current)
        if nodes[current]["active"]:
            token.append(current)
            print(f"Election token passed through Node {current}")
        current = nodes[current]["next"]

    if not token:
        print("No active node received the election token.")
        return

    # The manual specifies election of the highest-ID active node.
    leader = max(token)
    print(f"\nElection message returned after circulating through: {token}")
    print(f"New coordinator elected: Node {leader}")

if __name__ == "__main__":
    main()
