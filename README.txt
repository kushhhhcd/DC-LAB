# Distributed Computing Lab — 10 Unique Python Programs

These programs cover the 10 distinct implementation patterns identified in the supplied
Distributed Computing lab manual. Repeated chits change the project domain and CSV
filename, but retain the same implementation pattern and columns.

## Requirements
- Python 3.9 or newer
- No third-party packages required

## Run
Open this folder in VS Code. In the terminal, run one script at a time:

```bash
python3 01_rpc_rmi.py
python3 02_bully_algorithm.py
python3 03_berkeley_clock.py
python3 04_multithreading_mutex.py
python3 05_load_balancing.py
python3 06_vector_clocks.py
python3 07_lamport_clock.py
python3 08_cristian_clock.py
python3 09_ring_election.py
python3 10_mpi_matrix_scatter_gather.py
```

Each program creates a small sample CSV automatically if its CSV file does not already
exist. You can edit that CSV to test different input values. Keep the required column
names unchanged.

## CSV files created
- `rpc_calls.csv`
- `bully_cluster.csv`
- `node_clocks.csv`
- `tasks.csv`
- `workload.csv`
- `vector_events.csv`
- `events.csv`
- `cristian_clocks.csv`
- `ring_nodes.csv`
- `matrix.csv`

## Important implementation notes
1. **RPC/RMI:** This is a local simulation of remote procedure dispatch, not a networked
   RPC server. `SERVER_METHODS` contains the remotely callable procedures.
2. **Bully:** The lowest active node starts the election; higher active nodes respond;
   the highest active node becomes coordinator.
3. **Berkeley:** Rows marked `is_faulty=TRUE` are excluded from the average. Adjustments
   are calculated relative to the average of valid clocks.
4. **Mutex:** Threads process tasks concurrently. A lock protects the shared completed
   task list.
5. **Load balancing:** Change `METHOD` to `"round_robin"` or `"least"` in the script.
   Least-load selection uses total assigned compute units.
6. **Vector clocks:** For a `SEND` row, `target_process` is the receiver. For a `RECEIVE`
   row, `target_process` identifies the sender; the simulation merges a queued message
   vector when one is available. The manual's CSV schema does not include a message ID.
7. **Lamport clock:** A `SEND` row queues its timestamp for the destination process. A
   `RECEIVE` row consumes the next queued timestamp for that process. The manual's CSV
   schema does not include a message ID.
8. **Cristian:** Uses RTT/2 as the estimated one-way delay and calculates the clock offset
   relative to the client's send/receive midpoint.
9. **Ring:** Follows `next_node_id` links and elects the highest-ID active node reached.
10. **MPI matrix multiplication:** The manual's CSV schema supplies only matrix A. A
    second 4x4 matrix B is therefore included as a clearly marked constant in the script.
    Replace `MATRIX_B` if the exam question gives another matrix. This is a thread-based
    Scatter-Gather simulation, not actual MPI (`mpi4py`).

The sample datasets are demonstrations, not data copied from the manual.
