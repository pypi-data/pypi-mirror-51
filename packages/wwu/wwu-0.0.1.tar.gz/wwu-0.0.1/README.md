# WWU

Do you have limited storage space and a bunch of boxes to store? wwu tells you which way up will be best.

Boxes have 6 permutations in terms of storing them and currently wwu provides an indexed value of a permutation so you will only receive values in the range of 0 - 5.

## Example

```py
from wwu import Box

b = Box(10, 10, 20)  # Create a box with 10 x 10 x 20 dimensions.
b.wwu(10, 10, 20)  # Find the optimal permutation in storage space of 10 x 10 x 20

>>> 0
```

## Installation

```
pip install wwu
```

## Tests

```
pytest
```

```
========================================= test session starts ==========================================
platform linux -- Python 3.7.4, pytest-5.1.2, py-1.8.0, pluggy-0.12.0
rootdir: /var/home/Um9i/Documents/wwu
collected 2 items                                                                                      

tests/test_wwu.py ..                                                                             [100%]

========================================== 2 passed in 0.01s ===========================================
```
