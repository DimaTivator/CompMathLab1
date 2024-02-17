from abc import ABC, abstractmethod
from compmath.linalg import Matrix, get_diagonally_dominant
from compmath import _criterion


class BasicSolver(ABC):
    """
    Basic class for all solvers

    Attributes
    -------------

    criterion: str, optional (default='abs_deviation') -- The stop criterion for the solver
    Possible values: 'abs_deviation', 'relative_diff', 'discrepancy_diff'

    eps: float, optional (default=1e-6) -- The error rate of the solver

    max_iter: int, optional (default=100) -- The maximum number of iterations until the method converges

    Methods
    -------------

    solve()

    """

    def __init__(
            self,
            criterion='abs_deviation',
            eps=1e-6,
            max_iter=100
    ):
        self.criterion = criterion
        self.eps = eps
        self.max_iter = max_iter

    @abstractmethod
    def solve(self, **kwargs):
        pass


class SimpleIterationSolver(BasicSolver):

    def __init__(
            self,
            criterion='abs_deviation',
            eps=1e-6,
            max_iter=100
    ):
        super().__init__(criterion, eps, max_iter)

        # get criterion function by name
        try:
            self.crit_func = getattr(_criterion, self.criterion)
        except AttributeError:
            raise ValueError(f'Criterion function {self.criterion} not found')

    def solve(self, **kwargs):
        """
        This method implements the Simple Iteration algorithm to solve the system of linear equations
        Ax = b

        Required keyword Arguments:
        - A: Matrix of shape (n, n)
        - b: Matrix of shape (n, 1)
        """

        A, b = kwargs['A'], kwargs['b']

        if A.det() == 0:
            raise ValueError('The matrix A is singular')

        A = get_diagonally_dominant(A)
        if A is None:
            raise ValueError("The matrix A is not diagonally dominant. Method can't be used")

        n = A.num_rows

        x = Matrix([[0] for _ in range(n)])

        C = Matrix([[-A[i][j] / A[i][i] if i != j else 0 for j in range(n)] for i in range(n)])
        b = Matrix([[b[i][0] / A[i][i]] for i in range(n)])

        # add at start [0, 0, ..., 0]

        for _ in range(self.max_iter):
            prev = x[:][0]
            x = C * x + b
            d = self.crit_func(x[:][0], prev)
            # print([val for val in x], d)
            if d < self.eps:
                break

