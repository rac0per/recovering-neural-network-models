from random import Random

from find_kinks import find_scan_line
from target_model import make_target, predict


def gradient(query, x, eps):
    base = query(x)
    result = []
    for i in range(len(x)):
        shifted = x.copy()
        shifted[i] += eps
        result.append((query(shifted) - base) / eps)
    return result


def recover_network(query):
    origin, kinks = find_scan_line(query)
    bounds = [-1.1, *kinks, 0.1]
    recovered = {"W": [], "b": [], "a": [], "b_out": query([-1.1] * 10)}

    for i, t in enumerate(kinks):
        gap = min(t - bounds[i], bounds[i + 2] - t)
        offset = min(1e-3, gap / 4)
        eps = offset / 4

        left_point = [value + (t - offset) for value in origin]
        right_point = [value + (t + offset) for value in origin]
        left = gradient(query, left_point, eps)
        right = gradient(query, right_point, eps)

        jump = [r - l for l, r in zip(left, right)]

        a = sum(jump)
        if a <= 0.0:
            raise RuntimeError(f"Invalid gradient jump at t={t}")

        w = [value / a for value in jump]
        b = -t - sum(wi * xi for wi, xi in zip(w, origin))
        recovered["W"].append(w)
        recovered["b"].append(b)

        recovered["a"].append(a)

    return recovered


def max_parameter_error(recovered, truth):
    recovered_order = sorted(range(10), key=lambda i: -recovered["b"][i])
    truth_order = sorted(range(10), key=lambda j: -truth["b"][j])
    errors = [abs(recovered["b_out"] - truth["b_out"])]

    for i, j in zip(recovered_order, truth_order):
        errors.append(abs(recovered["b"][i] - truth["b"][j]))
        errors.append(abs(recovered["a"][i] - truth["a"][j]))
        errors.extend(
            abs(estimated - actual)
            for estimated, actual in zip(recovered["W"][i], truth["W"][j])
        )

    return max(errors)


if __name__ == "__main__":
    query, truth = make_target(seed=42)
    recovered = recover_network(query)

    rng = Random(2026)
    holdout = [[rng.uniform(-2.0, 2.0) for _ in range(10)] for _ in range(100)]
    parameter_error = max_parameter_error(recovered, truth)
    output_error = max(abs(predict(recovered, x) - query(x)) for x in holdout)

    print(f"Recovered neurons: {len(recovered['W'])}")
    print(f"Maximum parameter error: {parameter_error:.3e}")
    print(f"Maximum output error:    {output_error:.3e}")

    assert parameter_error < 1e-7
    assert output_error < 1e-7