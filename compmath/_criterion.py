from compmath import Matrix


def abs_deviation(prev: list, cur: list, eps=1e-5) -> bool:
    return max([abs(prev[i] - cur[i]) for i in range(len(prev))]) < eps


def relative_diff(prev: list, cur: list, eps=1e-5) -> bool:
    return max([abs((prev[i] - cur[i]) / cur[i]) for i in range(len(prev))]) < eps


def discrepancy_diff(A: Matrix, b: Matrix, x: Matrix, eps=1e-5) -> bool:
    r = A * x - b
    return max([r[i] for i in range(len(r))]) < eps

