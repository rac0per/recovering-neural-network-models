from toy_oracle import oracle


def find_toy_kink(query):
    left, right = -1.0, 0.5
    baseline = query([left, left])

    while right - left > 1e-8:
        mid = (left + right) / 2
        if query([mid, mid]) == baseline:
            left = mid
        else:
            right = mid

    return (left + right) / 2


if __name__ == "__main__":
    kink = find_toy_kink(oracle)
    print(f"Estimated kink: {kink:.8f}")
    assert abs(kink + 0.5) < 1e-8