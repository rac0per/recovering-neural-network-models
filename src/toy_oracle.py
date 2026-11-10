from math import isclose


def oracle(x):
    x1, x2 = x
    z = 0.25 * x1 + 0.75 * x2 + 0.5
    h = max(0.0, z)
    return 0.8 * h + 0.1


if __name__ == "__main__":
    for t in (-1.0, -0.5, 0.0, 0.5):
        print(f"t={t:5.2f}  f(t,t)={oracle([t, t]):.6f}")

    assert isclose(oracle([-1.0, -1.0]), 0.1)
    assert isclose(oracle([-0.5, -0.5]), 0.1)
    assert isclose(oracle([0.5, 0.5]), 0.9)
    assert isclose(oracle([2.0, -1.0]), 0.3)