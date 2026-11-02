import csv
from pathlib import Path

CSV_FILE = "workload.csv"
FIELDS = ["job_id", "compute_units", "assigned_worker", "status"]
WORKERS = ["Worker_1", "Worker_2", "Worker_3"]
METHOD = "least"  # Change to "round_robin" for Round Robin.

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["J101", 35, "UNASSIGNED", "PENDING"],
                ["J102", 20, "UNASSIGNED", "PENDING"],
                ["J103", 50, "UNASSIGNED", "PENDING"],
                ["J104", 15, "UNASSIGNED", "PENDING"],
                ["J105", 40, "UNASSIGNED", "PENDING"],
            ])

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        jobs = list(csv.DictReader(f))

    loads = {worker: 0 for worker in WORKERS}
    counts = {worker: 0 for worker in WORKERS}
    print(f"Load balancing method: {METHOD}\n")

    for index, job in enumerate(jobs):
        if METHOD == "round_robin":
            worker = WORKERS[index % len(WORKERS)]
        else:
            # Least current compute load.
            worker = min(WORKERS, key=lambda name: loads[name])

        units = int(job["compute_units"])
        loads[worker] += units
        counts[worker] += 1
        print(f"Job {job['job_id']} ({units} units) -> {worker}")

    print("\nFinal worker load:")
    for worker in WORKERS:
        print(f"{worker}: {loads[worker]} compute units, {counts[worker]} jobs")

if __name__ == "__main__":
    main()
