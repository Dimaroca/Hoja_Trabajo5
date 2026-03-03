AUTHOR: Diego Mateo Rodríguez Carrillo - 25215

Overview This project simulates the execution of processes in a
time-sharing operating system using Discrete Event Simulation (DES) with
SimPy.

Each process goes through the following states: NEW READY RUNNING
WAITING TERMINATED

Processes arrive according to an exponential distribution. Each process
requests a random amount of RAM and a random number of instructions to
execute. The CPU executes a fixed number of instructions per time unit
(quantum). After using the CPU, a process may move to I/O (WAITING) or
return to READY.

The simulation prints events as time progresses and calculates: -
Average time a process spends in the system - Standard deviation of that
time

Requirements Python 3.x SimPy

Install SimPy with: pip install simpy

How to Run 1. Save the code as CPU.py or simulation.py 2. Open a
terminal in the same folder 3. Run:

python CPU.py

If python is not recognized, try:

py CPU.py

Configuration You can modify the following variables in the code:

INTERVAL Average time between process arrivals.

N Number of processes to simulate.

RAM_TOTAL Total RAM available in the system.

CPUS Number of CPUs available.

INSTR_PER_QUANTUM Number of instructions executed per CPU time unit.

Simulation Behavior When the arrival interval decreases, processes
arrive more frequently. This increases contention for CPU and memory
resources, which typically increases the average completion time of
processes.

Output The program prints: - Process state changes during the
simulation - Average time from process start to termination - Standard
deviation of that time
