from random import Random


def predict(params, x):
    total = params["b_out"]
    for w, b, a in zip(params["W"], params["b"], params["a"]):
        z = sum(wi * xi for wi, xi in zip(w, x, strict=True)) + b
        total += a * max(0.0, z)
    return total


def make_target(seed):
    rng = Random(seed)
    weights = []
    for _ in range(10):
        row = [rng.random() for _ in range(10)]
        scale = sum(row)
        weights.append([value / scale for value in row])

    params = {
        "W": weights,
        "b": [rng.random() for _ in range(10)],
        "a": [rng.random() for _ in range(10)],
        "b_out": rng.random(),
    }

    def query(x):
        return predict(params, x)

    return query, params