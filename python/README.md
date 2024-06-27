
# SecureNumpy

SecureNumpy is a library designed to bridge the gap between Numpy, a fundamental package for scientific computing with Python, and the privacy-preserving paradigms of MPC. With its intuitive interface, SecureNumpy provides a seamless experience that allows users to perform Numpy's powerful array manipulations and mathematical functions on encrypted data without compromising their privacy.

SecureNumpy provides a user-friendly interface for MPC using `SecureArray`. It is a multidimensional container of items of the same type and size, supporting properties `shape` and `dtype`, explicit indexing, operator overloading, and element-wise operations.

SecureNumpy also offers a series of practical routines. The following are the main modules and supported functions in SecureNumpy:

| Module                          | Description                                                                          | Examples                 |
| ------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| Array creation                  | Methods to create SecureArray                                                        | `ones`, `zeros`, `arange`      |
| Array manipulation              | Changing array shape, transposing an array, joining arrays etc.                             | `reshape`, `transpose`, `repeat` |
| Mathematical functions          | Some arithmetic operations, e.g., exponentiation and logarithm, will be provided in the future. | `sum`, `prod`, `max`           |
| Linear algebra                  | Some matrix and vector product functions.                                            | `dot`, `inner`               |
| Sorting, searching and counting | Some sort and search functions.                                                      | `where`, `argmax`, `sort`      |
| Statistics                      | Statistic functions to calculate order, average, and variance.                        | `ptp`, `average`, `mean`       |

# SecureML

SecureML provides a series of privacy-preserving machine learning functions based on SecureNumpy.
The following are the main modules and supported functions in SecureML:

| Module                          | Description                                                                          | Examples                 |
| ------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| Activation Function             | Various types of activation functions.                                               | `sigmoid`                  |

# SecureSQL
SecureSQL provides a series of SQL-related secure functions based on SecureNumpy.

The following are the main modules and supported functions in SecureSQL:

| Module                          | Description                                                                          | Examples                 |
| ------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| Aggregate                       | Various types of Group by functions.                                                 | max, min, count, sum     |

# SetOps
Provided PSI and PJC protocols, currently supporting ECDH-PSI, KKRT-PSI, and Circuit-PSI.

The following are the main modules and supported functions in SetOps:

| Module                          | Description                                                                          | Examples                 |
| ------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| PSI                             | Various types of PSI functions.                                                      | ECDH, KKRT               |
| PJC                             | Various types of PJC functions.                                                      | Circuit-PSI              |

# Network
Provided a Python interface to Network.

# Duet
Provided a Python wrapper for the MPC virtual machine.
