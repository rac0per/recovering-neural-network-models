from math import isclose

from find_kink import find_toy_kink
from toy_oracle import oracle


def gradient(query, x, eps=1e-5):
    x1, x2 = x
    base = query(x)
    dx1 = (query([x1 + eps, x2]) - base) / eps
    dx2 = (query([x1, x2 + eps]) - base) / eps
    return dx1, dx2


def recover_toy(query):
    t = find_toy_kink(query)
    offset = 1e-3
    left = [t - offset, t - offset]
    right = [t + offset, t + offset]

    left_g1, left_g2 = gradient(query, left)
    right_g1, right_g2 = gradient(query, right)
    jump1 = right_g1 - left_g1
    jump2 = right_g2 - left_g2

    w_out = jump1 + jump2
    w1, w2 = jump1 / w_out, jump2 / w_out
    b_hidden = -(w1 * t + w2 * t)
    b_out = query(left)
    return (w1, w2), b_hidden, w_out, b_out


if __name__ == "__main__":
    (w1, w2), b_hidden, w_out, b_out = recover_toy(oracle)
    print(f"w = ({w1:.6f}, {w2:.6f}), b_hidden = {b_hidden:.6f}")
    print(f"w_out = {w_out:.6f}, b_out = {b_out:.6f}")

    for x1, x2 in [(0.2, -0.4), (-2.0, 0.1), (1.7, 0.3)]:
        z = w1 * x1 + w2 * x2 + b_hidden
        predicted = w_out * max(0.0, z) + b_out
        assert isclose(predicted, oracle([x1, x2]), abs_tol=1e-8)