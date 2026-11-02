import csv
from pathlib import Path

CSV_FILE = "cristian_clocks.csv"
FIELDS = ["client_id", "t0_send_ms", "t_server_ms", "t1_recv_ms"]

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["C1", 1000, 1050, 1100],
                ["C2", 2000, 2070, 2120],
            ])

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        for row in csv.DictReader(f):
            client = row["client_id"]
            t0 = float(row["t0_send_ms"])
            server = float(row["t_server_ms"])
            t1 = float(row["t1_recv_ms"])

            rtt = t1 - t0
            estimated_server_time = server + (rtt / 2)
            client_midpoint = (t0 + t1) / 2
            offset = estimated_server_time - client_midpoint
            adjusted_client_time = client_midpoint + offset

            print(f"\nClient: {client}")
            print(f"RTT = T1 - T0 = {t1} - {t0} = {rtt:.2f} ms")
            print(f"Estimated server time = {server} + RTT/2 = {estimated_server_time:.2f} ms")
            print(f"Client midpoint time = {client_midpoint:.2f} ms")
            print(f"Clock offset = {offset:+.2f} ms")
            print(f"Adjusted client time = {adjusted_client_time:.2f} ms")

if __name__ == "__main__":
    main()
