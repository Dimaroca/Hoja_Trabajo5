import simpy
import random
import statistics

RANDOM_SEED = 42

INTERVAL = 10
PROCESSES = 200

RAM_TOTAL = 100
CPUS = 2
INSTR_PER_QUANTUM = 3


def log(env, msg):
    """Prints an event with the current simulation time."""
    print("%.3f:" % env.now, msg)


def process(env, pid, RAM, CPU, IO, quantum, times):
    """Simulates a process lifecycle and records its total execution time."""

    start = env.now
    mem = random.randint(1, 10)
    instr = random.randint(1, 10)

    log(env, "P%s NEW arrives" % pid)

    log(env, "P%s requests RAM" % pid)
    yield RAM.get(mem)
    log(env, "P%s READY" % pid)

    while instr > 0:

        log(env, "P%s requests CPU : READY" % pid)
        with CPU.request() as turn:
            yield turn

            log(env, "P%s RUNNING" % pid)

            if instr >= quantum:
                yield env.timeout(1)
                instr -= quantum
            else:
                t = instr / float(quantum)
                yield env.timeout(t)
                instr = 0

            log(env, "P%s leaves CPU" % pid)

        if instr <= 0:
            break

        r = random.randint(1, 21)

        if r == 1:
            log(env, "P%s WAITING" % pid)
            with IO.request() as io:
                yield io
                yield env.timeout(1)
            log(env, "P%s READY" % pid)
        else:
            log(env, "P%s READY" % pid)

    log(env, "P%s TERMINATED" % pid)
    yield RAM.put(mem)

    end = env.now
    times.append(end - start)


def generate(env, n, interval, RAM, CPU, IO, quantum, times):
    """Creates processes with exponential inter-arrival time."""

    for i in range(n):
        env.process(process(env, i, RAM, CPU, IO, quantum, times))
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def run(n, interval, ram, count, quantum):
    """Runs the simulation and prints average and standard deviation."""

    random.seed(RANDOM_SEED)

    env = simpy.Environment()

    RAM = simpy.Container(env, init=ram, capacity=ram)
    CPU = simpy.Resource(env, capacity=count)
    IO = simpy.Resource(env, capacity=1)

    times = []

    env.process(generate(env, n, interval, RAM, CPU, IO, quantum, times))

    env.run()

    mean = statistics.mean(times)
    std = statistics.stdev(times) if len(times) > 1 else 0.0

    print("\nRESULTS")
    print("Interval:", interval)
    print("Processes:", n)
    print("Average time:", round(mean, 2))
    print("Standard deviation:", round(std, 2))


run(PROCESSES, INTERVAL, RAM_TOTAL, CPUS, INSTR_PER_QUANTUM)