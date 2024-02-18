### Simple-Iteration SOLE-solver
- This repository provides the implementation of Simple-Iteration SOLE-solver with GUI (soon) on native Python + QT5 
----
### GUI Instruction
#### 1. Manual Input
- Enter matrix A and vector b in special dialogue windows
- Enter Accuracy value. Accuracy is the value that is used as epsilon in convergence criteria
- Enter a convergence criterion. Possible options:
- - abs_deviation $max |x_i^k - x_i^{k-1}| \le \varepsilon$
- - relative_diff $max |\frac{x_i^k - x_i^{k-1}}{x_i^k}| \le \varepsilon$
- - discrepancy_diff $max |r_i^k = Ax_i^k - b| \le \varepsilon$