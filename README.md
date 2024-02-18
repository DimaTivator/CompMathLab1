### Simple-Iteration SOLE-solver $Ax = b$
- This repository provides the implementation of Simple-Iteration SOLE-solver with GUI (soon) on native Python + QT5 
---
### Restrictions 
- The matrix shouldn't be singular, so $det(A) \not 0$
- The matrix should be diagonally dominant. There should exist such permutation of its columns so that $\abs{a_{ii}} \le \sum_{j \ne i} \abs{a_{ij}}, i = 1, 2, ..., n$ 
---
### GUI Instruction
#### 1. Manual Input
- Enter matrix A and vector b in special dialogue windows
- Enter Accuracy value. Accuracy is the value that is used as epsilon in convergence criteria
- Enter a convergence criterion. Possible options:
- - abs_deviation $max \abs{x_i^k - x_i^{k-1}} \le \varepsilon$
- - relative_diff $max \abs{\frac{x_i^k - x_i^{k-1}}{x_i^k}} \le \varepsilon$
- - discrepancy_diff $max \abs{r_i^k = Ax_i^k - b} \le \varepsilon$
- Click `solve`
#### 2. File Input
- Select a .`.txt` file in file selector and click `load`
- File format:
- - Your file should contain only numerical values 
- - The first number in the file is n - the matrix size
- - Then there should be $n^2 + n$ numbers with any number of whitespaces and indents
- Enter accuracy value and convergence criterion (read `Manual Input instruction`)
- Click `solve`