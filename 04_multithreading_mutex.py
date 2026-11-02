import csv
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

CSV_FILE = "tasks.csv"
FIELDS = ["task_id", "thread_name", "burst_ms", "priority", "status"]
lock = threading.Lock()
completed_tasks = []

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["T1", "Worker_1", 300, "HIGH", "PENDING"],
                ["T2", "Worker_2", 200, "MEDIUM", "PENDING"],
                ["T3", "Worker_3", 400, "LOW", "PENDING"],
                ["T4", "Worker_1", 250, "HIGH", "PENDING"],
            ])

def process_task(task):
    task_id = task["task_id"]
    worker = task["thread_name"]
    print(f"{worker}: waiting to process {task_id}")
    time.sleep(max(0, int(task["burst_ms"])) / 1000)

    # Mutex protects the shared completed_tasks list.
    with lock:
        print(f"{worker}: LOCK ACQUIRED for {task_id}")
        completed_tasks.append(task_id)
        print(f"{worker}: {task_id} marked COMPLETED")
        print(f"{worker}: LOCK RELEASED")

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        tasks = list(csv.DictReader(f))

    print("Starting concurrent workers...\n")
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_task, tasks)

    print("\nFinal completed task list:")
    print(completed_tasks)

if __name__ == "__main__":
    main()
