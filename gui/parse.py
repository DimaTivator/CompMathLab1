from compmath.linalg import Matrix


# read matrix and vector from the given lines
def get_matrix_vector(lines):
    nums = []
    for line in lines:
        nums.extend(list(map(float, line.split())))

    n = int(nums[0])
    if len(nums) != n * n + n + 1:
        raise ValueError("Invalid size")

    A = Matrix([[0 for _ in range(n)] for _ in range(n)])
    b = Matrix([[0] for _ in range(n)])

    for i in range(n):
        for j in range(n):
            A[i][j] = nums[i * n + j + 1]

    for i in range(n):
        b[i][0] = nums[n * n + i + 1]

    return n, A, b

