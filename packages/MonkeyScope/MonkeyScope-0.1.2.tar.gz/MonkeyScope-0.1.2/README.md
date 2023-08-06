# MonkeyTimer Beta
Distribution Timer for Non-deterministic Value Generators

### Sister Projects:
- Fortuna: Collection of abstractions to make custom random value generators. https://pypi.org/project/Fortuna/
- Pyewacket: Complete drop-in replacement for the Python3 random module. https://pypi.org/project/Pyewacket/
- RNG: Python3 API for the C++ Random Library. https://pypi.org/project/RNG/

Support these and other random projects: https://www.patreon.com/brokencode

### Quick Install
``` 
$ pip install MonkeyScope
$ python3

>>> import MonkeyScope ...
```
### Installation may require the following:
- Python 3.7 or later.
- Cython: `pip install Cython`
- Python3 developer environment, setuptools etc.
- Modern C++17 Compiler and Standard Library.

---

## MonkeyScope Specifications
- `MonkeyScope.distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - Logger for the statistical analysis of non-deterministic output.
    - @param func :: function, method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles=10000 :: Total number of samples to use for analysis.
    - @optional_kw post_processor=None :: Used to scale a large set of data into a smaller set of groupings for better visualization of the data, esp. useful for distributions of floats. For many functions in quick_test(), math.floor() is used, for others round() is more appropriate. For more complex post processing - lambdas work nicely. Post processing only affects the distribution, the statistics and performance results are unaffected.
- `MonkeyScope.distribution(func: staticmethod, *args, **kwargs) -> None`
    - Stats and distribution.
- `MonkeyScope.timer(func: staticmethod, *args, **kwargs) -> None`
    - Just the function timer.

## MonkeyScope Examples
```
$ python3
Python 3.7.3
>>> import MonkeyScope
>>> import random
>>> MonkeyScope.timer(random.randint, 1, 10)
Typical Timing: 1282 ± 29 ns
>>> 
>>> MonkeyScope.distribution(random.randint, 1, 10)
Statistics of 1024 samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.5419921875
 Std Deviation: 2.876777674890822
Distribution of 102400 samples:
 1: 9.91796875%
 2: 9.935546875%
 3: 9.9697265625%
 4: 10.10546875%
 5: 9.9404296875%
 6: 10.044921875%
 7: 10.0380859375%
 8: 9.9072265625%
 9: 10.15234375%
 10: 9.98828125%
>>> 
>>> MonkeyScope.distribution_timer(random.randint, 1, 10)
Output Analysis: Random.randint(1, 10)
Typical Timing: 1125 ± 32 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.48046875
 Std Deviation: 2.8314684291544103
Distribution of 102400 samples:
 1: 10.150390625%
 2: 10.1259765625%
 3: 9.990234375%
 4: 10.0419921875%
 5: 9.90234375%
 6: 10.0810546875%
 7: 9.87109375%
 8: 9.947265625%
 9: 9.9443359375%
 10: 9.9453125%

>>> 


```
### ToDo List:
0. Improve Documentation
1. Concoct Examples
2. Derive Tests
3. Refactor Inception


### Development Log:

##### MonkeyScope Beta 0.1.2
- Renamed to MonkeyScope

##### MonkeyTimer Beta 0.0.2
- Changed to c++ compiler

##### MonkeyTimer Beta 0.0.1
- Initial Project Setup
