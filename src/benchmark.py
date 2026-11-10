from random import Random
from statistics import median
from time import perf_counter

from recover_network import max_parameter_error, recover_network
from target_model import make_target, predict


TRIALS = 100
TOLERANCE = 1e-7


def run_trial(seed, holdout):
    query, truth = make_target(seed)
    query_count = 0

    def counted_query(x):
        nonlocal query_count
        query_count += 1
        return query(x)

    start = perf_counter()
    try:
        recovered = recover_network(counted_query)
    except RuntimeError as error:
        elapsed_ms = (perf_counter() - start) * 1000
        return query_count, elapsed_ms, None, str(error)
    elapsed_ms = (perf_counter() - start) * 1000

    parameter_error = max_parameter_error(recovered, truth)
    output_error = max(abs(predict(recovered, x) - query(x)) for x in holdout)
    errors = (parameter_error, output_error)

    failure = None
    if not all(error < TOLERANCE for error in errors):
        failure = f"parameter error={parameter_error:.3e}, output error={output_error:.3e}"

    return query_count, elapsed_ms, errors, failure


def main():
    rng = Random(2026)
    holdout = [[rng.uniform(-2.0, 2.0) for _ in range(10)] for _ in range(100)]
    counts, timings, completed_errors = [], [], []
    failures = 0

    for seed in range(TRIALS):
        queries, elapsed_ms, errors, failure = run_trial(seed, holdout)
        counts.append(queries)
        timings.append(elapsed_ms)

        if errors is not None:
            completed_errors.append(errors)
        if failure is not None:
            failures += 1
            print(f"Seed {seed} failed ({queries} queries): {failure}")

    passed = TRIALS - failures
    print(f"Success rate: {passed}/{TRIALS} ({passed / TRIALS:.1%})")
    print(f"Queries (median / max): {median(counts):g} / {max(counts)}")
    print(f"Attack time (median / max): {median(timings):.2f} / {max(timings):.2f} ms")

    if completed_errors:
        print(f"Worst parameter error: {max(p for p, _ in completed_errors):.3e}")
        print(f"Worst output error:    {max(o for _, o in completed_errors):.3e}")


if __name__ == "__main__":
    main()