import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

CSV_FILE = "matrix.csv"

# The CSV contains matrix A. Matrix B is a fixed 4x4 matrix for this demonstration.
# Change B if your question provides a different second matrix.
MATRIX_B = [
    [1, 2, 3, 4],
    [2, 0, 1, 3],
    [1, 1, 0, 2],
    [0, 2, 1, 1],
]

FIELDS = ["row_id", "col_0", "col_1", "col_2", "col_3"]

def create_sample():
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerows([
                ["R0", 2, 4, 1, 5],
                ["R1", 1, 3, 2, 4],
                ["R2", 5, 2, 0, 1],
                ["R3", 3, 1, 4, 2],
            ])

def multiply_row(args):
    row_id, row_a, matrix_b = args
    result = [
        sum(row_a[k] * matrix_b[k][j] for k in range(4))
        for j in range(4)
    ]
    print(f"[WORKER] {row_id} computed -> {result}")
    return row_id, result

def main():
    create_sample()
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        matrix_a = []
        for row in reader:
            values = [int(row[f"col_{i}"]) for i in range(4)]
            matrix_a.append((row["row_id"], values))

    print("[MASTER] Matrix A:")
    for row_id, values in matrix_a:
        print(row_id, values)

    print("\n[MASTER] Scattering rows to workers...")
    work = [(row_id, row, MATRIX_B) for row_id, row in matrix_a]

    with ThreadPoolExecutor(max_workers=len(work)) as executor:
        gathered = list(executor.map(multiply_row, work))

    gathered.sort(key=lambda item: item[0])
    result = [row for _, row in gathered]

    print("\n[MASTER] Gathered final matrix product A x B:")
    for row in result:
        print(row)

if __name__ == "__main__":
    main()
