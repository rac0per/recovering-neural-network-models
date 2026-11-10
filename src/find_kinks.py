from target_model import make_target
from random import Random

class KinkSearchError(RuntimeError):
    pass


def find_kinks(query, expected=10, *, origin=None):
    if origin is None:
        origin = [0.0] * 10

    lo, hi = -1.1, 0.1

    for segments in (128, 256, 512, 1024, 2048, 4096, 8192):
        step = (hi - lo) / segments
        grid = [lo + i * step for i in range(segments + 1)]
        values = [query([value + t for value in origin]) for t in grid]
        slopes = [(y2 - y1) / step for y1, y2 in zip(values, values[1:])]

        groups = []
        for i in range(1, len(slopes)):
            if slopes[i] - slopes[i - 1] > 1e-8:
                if groups and i == groups[-1][-1] + 1:
                    groups[-1].append(i)
                else:
                    groups.append([i])

        if len(groups) == expected:
            kinks = []
            for group in groups:
                left, right = group[0], group[-1]
                m_left, m_right = slopes[left - 1], slopes[right]
                c_left = values[left] - m_left * grid[left]
                c_right = values[right] - m_right * grid[right]
                kinks.append((c_left - c_right) / (m_right - m_left))
            return kinks

    raise KinkSearchError("Could not separate all kinks with the current grid.")

def find_scan_line(query):
    origin = [0.0] * 10
    try:
        return origin, find_kinks(query, origin=origin)
    except KinkSearchError:
        rng = Random(2026)
        origin = [rng.uniform(-0.05, 0.05) for _ in range(10)]
        return origin, find_kinks(query, origin=origin)


if __name__ == "__main__":
    query, truth = make_target(seed=42)
    estimated = find_kinks(query)
    actual = sorted(-b for b in truth["b"])
    max_error = max(abs(e - a) for e, a in zip(estimated, actual))
    print(f"Found {len(estimated)} kinks")
    print(f"Maximum error: {max_error:.3e}")