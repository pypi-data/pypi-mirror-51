# ComStats
Matrix broadcasting combinatorial statistics. The reasons for having a separate repository for this stems from the communication [here](https://github.com/scipy/scipy/issues/9860).

## Installation

`pip install ComStats`

## Example

This library enables numpy matrixes to be passed into statistical functions for optimised recursive comparisons across dimensions.

``` python
>>> import numpy as np
>>> from ComStats import comstats as cs
>>> input_set = np.array([
        [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
        [2, 1, 2, 3, 3, 0, 1, 0, 0, 0, 4, 1, 2, 4, 4],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [3, 0, 1, 3, 0, 0, 2, 1, 2, 3, 3, 1, 0, 0, 2]
    ])
>>> p_values, scores = cs.t_test(input_set)
>>> p_values
array([[1.        , 0.00353093, 1.        , 0.00961514],
       [0.00353093, 1.        , 0.00353093, 0.43711409],
       [1.        , 0.00353093, 1.        , 0.00961514],
       [0.00961514, 0.43711409, 0.00961514, 1.        ]])
>>> scores
array([[ 0.        , -3.38132124,  0.        , -2.88675135],
       [ 3.38132124,  0.        ,  3.38132124,  0.78881064],
       [ 0.        , -3.38132124,  0.        , -2.88675135],
       [ 2.88675135, -0.78881064,  2.88675135,  0.        ]])
```

Assuming the input_array if of the form: [A, B, C, D] then the resulting matrix is of the form: [[AA, AB, AC, AD], [BA, BB, BC, BD], [CA, CB...], ...].

To convert in and out of pandas DataFrames, see [here](https://stackoverflow.com/questions/33915638/a-groupby-with-combinations-of-the-categorical-variables).

Available functions:

* t_test() # unweighted/weighted paired/unpaired
* percentage_t_test()

See `test/test_stats.py` for usage and parameter variation.
