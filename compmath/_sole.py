from abc import ABC, abstractmethod
from compmath.linalg import Matrix, get_diagonally_dominant
from compmath import _criterion
from dataclasses import dataclass


@dataclass
class SoleData:
    _n: int = 10
    _m: int = None
    _A: Matrix = None
    _b: Matrix = None

    def __post_init__(self):
        if self._m is None:
            self._m = self._n

        self._A = Matrix([[0 for _ in range(self._m)] for _ in range(self._n)])
        self._b = Matrix([[0] for _ in range(self._n)])

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        if value is not None:
            self._n = value
            self.__post_init__()

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        self._m = value
        self.__post_init__()

    @property
    def A(self):
        return self._A

    def set_A(self, i, j, value):
        if value is not None:
            self._A[i][j] = value

    @property
    def b(self):
        return self._b

    def set_b(self, i, value):
        if value is not None:
            self._b[i][0] = value


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
