# Pyewacket
### Fast, fault-tolerant, drop-in replacement for the Python3 random module

Built on top of the RNG Storm Engine for stability and performance. While Storm is a high quality random engine, Pyewacket is not appropriate for cryptography of any kind. Pyewacket is meant for games, data science, A.I. and experimental programming, not security.

### Sister Projects:
- Fortuna: Collection of tools to make custom random value generators. https://pypi.org/project/Fortuna/
- Pyewacket: Drop-in replacement for the Python3 random module. https://pypi.org/project/Pyewacket/
- MonkeyScope: Framework for testing non-deterministic value generators. https://pypi.org/project/MonkeyScope/

Support these and other random projects: https://www.patreon.com/brokencode

### Quick Install `$ pip install Pyewacket`

### Installation may require the following:
- Python 3.7 or later with dev tools (setuptools, pip, etc.)
- Cython: `pip install Cython`
- Modern C++17 Compiler and Standard Library.

## Random Integers
- `Pyewacket.randbelow(n: int) -> int`
    - While randrange(a, b, c) can be handy, it's more complex than needed most of the time. Mathematically, randbelow(n) is equivalent to randrange(n) and they have nearly the same performance characteristics in Pyewacket, 10x - 12x faster than the random module's internal randbelow().
    - @param n :: Pyewacket expands the acceptable input domain to include non-positive values of n.
    - @return :: random integer in range (n, 0] or [0, n) depending on the sign of n.
    - Analytic Continuation about zero is used to achieve full input domain coverage for any function that normally can only take positive, non-zero values as input.
    - Symmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n) if n < 0 else 0` (this is how it works now).
    - The lambda is not the actual implementation, but it represents the idea of AC pretty well. AC will invert the meaning of a function for negative input. Thus turning _randbelow_ into _randabove_ for all negative values of n.

_It is possible that an asymmetric AC would be a better match to how negative numbers work as reverse list indexes in python._

Asymmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n)-1 if n < 0 else None` (this is how it could work).

_This would allow_ `some_list[randbelow(-n)]` _to range over the last n items in a list of size n or larger. The interesting part is that you wouldn't need to know the exact size of the list. Let me know if you think this is a good idea._

```python
from Pyewacket import randbelow


""" Standard """
randbelow(10)       # -> [0, 10)

""" Extras """
randbelow(0)        # -> [0, 0) => 0
randbelow(-10)      # -> (-10, 0]
```

- `Pyewacket.randint(a: int, b: int) -> int`
    - @param a, b :: both are required,
    - @return :: random integer in range [a, b] or [b, a]
    - Inclusive on both sides
    - Removed the asymmetric requirement of a < b
    - When a == b returns a

```python
from Pyewacket import randint


""" Standard """
randint(1, 10)      # -> [1, 10]

""" Extras """
randint(10, 1)      # -> [1, 10]
randint(10, 10)     # -> [10, 10] => 10
```

- `Pyewacket.randrange(start: int, stop: int = 0, step: int = 1) -> int`
    - Fault tolerant and about 20x faster than random.randrange()
    - @param start :: required
    - @param stop :: optional, default=0
    - @parma step :: optional, default=1
    - @return :: random integer in range (stop, start] or [start, stop) by |step|
    - Removed the requirements of start < stop, and step > 0
    - Always returns start for start == stop or step == 0

```python
from Pyewacket import randrange


""" Standard """
randrange(10)           # -> [0, 10) by whole numbers
randrange(1, 10)        # -> [1, 10) by whole numbers
randrange(1, 10, 2)     # -> [1, 10) by 2, odd numbers

""" Extras """
randrange(-10)          # -> [-10, 0) by 1
randrange(10, 1)        # -> [1, 10) by 1
randrange(10, 0, 2)     # -> [0, 10) by 2, even numbers
randrange(10, 10, 0)    # -> [10, 10) => 10
```

## Random Floating Point
- `Pyewacket.random() -> float`
    - random float in range [0.0, 1.0] or [0.0, 1.0) depending on rounding.
    - This is the only function that doesn't show a performance increase, as expected.
    - Roughly the same speed as random.random()
- `Pyewacket.uniform(a: float, b: float) -> float`
    - random float in [a, b] or [a, b) depending on rounding
    - 4x faster
- `Pyewacket.expovariate(lambd: float) -> float`
    - 5x faster
- `Pyewacket.gammavariate(alpha, beta) -> float`
    - 10x faster
- `Pyewacket.weibullvariate(alpha, beta) -> float`
    - 4x faster
- `Pyewacket.betavariate(alpha, beta) -> float`
    - 16x faster
- `Pyewacket.paretovariate(alpha) -> float`
    - 4x faster
- `Pyewacket.gauss(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.normalvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.lognormvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.vonmisesvariate(mu: float, kappa: float) -> float`
    - 4x faster
- `Pyewacket.triangular(low: float, high: float, mode: float = None)`
    - 10x faster

## Random Sequence Values
- `Pyewacket.choice(seq: List) -> Value`
    - An order of magnitude faster than random.choice().
    - @param seq :: any zero indexed object like a list or tuple.
    - @return :: random value from the list, can be any object type that can be put into a list.
- `Pyewacket.choices(population, weights=None, *, cum_weights=None, k=1)`
    - @param population :: data values
    - @param weights :: relative weights
    - @param cum_weights :: cumulative weights
    - @param k :: number of samples to be collected
    - Only seeing a 2x performance gain.
- `Pyewacket.cumulative_weighted_choice(table, k=1)`
    - 10x faster than choices, but radically different API and a bit less flexible.
    - Supports Cumulative Weights only. Convert relative weights to cumulative if needed: `cum_weights = tuple(itertools.accumulate(rel_weights))`
    - @param table :: two dimensional list or tuple of weighted value pairs. `[(1, "a"), (10, "b"), (100, "c")...]`
        - The table can be constructed as `tuple(zip(cum_weights, population))` weights always come first.
    - @param k :: number of samples to be collected. Returns a list of size k if k > 1, otherwise returns a single value - not a list of one.
- `Pyewacket.shuffle(array: list) -> None`
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 20 times faster than random.shuffle().
    - Implements Knuth B Shuffle Algorithm. Knuth B is twice as fast as Knuth A or Fisher-Yates for every test case. This is likely due to the combination of walking backward and rotating backward into the back side of the list. With this combination it can never modify the data it still needs to walk through. Fresh snow all the way home, aka very low probability for cache misses.
- `Pyewacket.sample(population: List, k: int) -> list`
    - @param population :: list or tuple.
    - @param k :: number of unique samples to get.
    - @return :: size k list of unique random samples.
    - Performance gains range (5x to 20x) depending on len(population) and the ratio of k to len(population). Higher performance gains are seen when k ~= pop size.

## Hardware & Software Seeding
- `seed(seed: int=0) -> None`
    - Hardware seeding is enabled by default. This function is used to turn toggle software seeding and set or reset the engine seed. This affects all random functions in the module.
    - @param seed :: any non-zero positive integer less than 2**63 enables software seeding.
    - Calling `seed()` or `seed(0)` will turn off software seeding and re-enable hardware seeding.
    - While you can toggle software seeding on and off and re-seed the engine at will without error, this function is **not intended or optimized to be used inside a loop**. General rule: seed once, or better yet, not at all. Typically, software seeding is for debugging a product, hardware seeding is used for product release.


## Development Log
##### Pyewacket 1.3.0
- Major API Update, several utilities have been moved into their own module: MonkeyScope.
    - distribution_timer
    - distribution
    - timer

##### Pyewacket 1.2.4
- `Pyewacket.randrange()` bug fix
- Test Update

##### Pyewacket 1.2.3
- Minor Bug Fix

##### Pyewacket 1.2.2
- Typo Fix

##### Pyewacket 1.2.1
- Test Update

##### Pyewacket 1.2.0
- Storm Update

##### Pyewacket 1.1.2
- Low level clean up

##### Pyewacket 1.1.1
- Docs Update

##### Pyewacket 1.1.0
- Storm Engine Update

##### Pyewacket 1.0.3
- minor typos

##### Pyewacket 1.0.2
- added choices alternative `cumulative_weighted_choice`

##### Pyewacket 1.0.1
- minor typos

##### Pyewacket 1.0.0
- Storm 2 Rebuild.

##### Pyewacket 0.1.22
- Small bug fix.

##### Pyewacket 0.1.21
- Public Release

##### Pyewacket 0.0.2b1
- Added software seeding.

##### Pyewacket v0.0.1b8
- Fixed a small bug in the tests.

##### Pyewacket v0.0.1b7
- Engine Fine Tuning
- Fixed some typos.

##### Pyewacket v0.0.1b6
- Rearranged tests to be more consistent and match the documentation.

##### Pyewacket v0.0.1b5
- Documentation Upgrade
- Minor Performance Tweaks

##### Pyewacket v0.0.1b4
- Public Beta

##### Pyewacket v0.0.1b3
- quick_test()
- Extended Functionality
    - sample()
    - expovariate()
    - gammavariate()
    - weibullvariate()
    - betavariate()
    - paretovariate()
    - gauss()
    - normalvariate()
    - lognormvariate()
    - vonmisesvariate()
    - triangular()

##### Pyewacket v0.0.1b2
- Basic Functionality
    - random()
    - uniform()
    - randbelow()
    - randint()
    - randrange()
    - choice()
    - choices()
    - shuffle()

##### Pyewacket v0.0.1b1
- Initial Design & Planning


## Distribution and Performance Tests
```
MonkeyScope: Pyewacket

Base Case
Output Analysis: Random._randbelow(10)
Typical Timing: 594 ± 25 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.40234375
 Std Deviation: 2.8903443217275546
Distribution of 10000 samples:
 0: 10.7%
 1: 10.44%
 2: 9.94%
 3: 10.12%
 4: 9.97%
 5: 9.05%
 6: 9.96%
 7: 9.54%
 8: 10.0%
 9: 10.28%

Output Analysis: randbelow(10)
Typical Timing: 63 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.38671875
 Std Deviation: 2.837546641608558
Distribution of 10000 samples:
 0: 10.12%
 1: 9.98%
 2: 10.24%
 3: 9.9%
 4: 9.73%
 5: 10.37%
 6: 10.2%
 7: 9.8%
 8: 9.7%
 9: 9.96%

Base Case
Output Analysis: Random.randint(1, 10)
Typical Timing: 1219 ± 21 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.3837890625
 Std Deviation: 2.9219516533899546
Distribution of 10000 samples:
 1: 9.68%
 2: 10.26%
 3: 10.13%
 4: 10.06%
 5: 10.15%
 6: 10.38%
 7: 10.16%
 8: 9.66%
 9: 9.34%
 10: 10.18%

Output Analysis: randint(1, 10)
Typical Timing: 63 ± 15 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.3388671875
 Std Deviation: 2.8827550574661265
Distribution of 10000 samples:
 1: 10.08%
 2: 10.53%
 3: 9.61%
 4: 10.12%
 5: 10.06%
 6: 9.8%
 7: 9.99%
 8: 9.76%
 9: 10.05%
 10: 10.0%

Base Case
Output Analysis: Random.randrange(0, 10, 2)
Typical Timing: 1282 ± 21 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.1328125
 Std Deviation: 2.9232504939938666
Distribution of 10000 samples:
 0: 19.72%
 2: 19.7%
 4: 20.57%
 6: 19.26%
 8: 20.75%

Output Analysis: randrange(0, 10, 2)
Typical Timing: 94 ± 1 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.298828125
 Std Deviation: 2.8326677259261137
Distribution of 10000 samples:
 0: 19.5%
 2: 19.41%
 4: 20.34%
 6: 19.74%
 8: 21.01%

Base Case
Output Analysis: Random.random()
Typical Timing: 32 ± 15 ns
Statistics of 1024 samples:
 Minimum: 0.0007674339680512343
 Median: (0.5132795429578163, 0.5143627137630267)
 Maximum: 0.9991465401858827
 Mean: 0.5122766732108667
 Std Deviation: 0.2923353652863211
Post-processor distribution of 10000 samples using round method:
 0: 50.29%
 1: 49.71%

Output Analysis: random()
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0022239896577658648
 Median: (0.4908223815475243, 0.4915039200779949)
 Maximum: 0.9954015973351845
 Mean: 0.4906668608106786
 Std Deviation: 0.2824156891197003
Post-processor distribution of 10000 samples using round method:
 0: 51.07%
 1: 48.93%

Base Case
Output Analysis: Random.uniform(0.0, 10.0)
Typical Timing: 219 ± 11 ns
Statistics of 1024 samples:
 Minimum: 0.009048765432749795
 Median: (5.187833077652803, 5.197592652053529)
 Maximum: 9.993079620211931
 Mean: 5.0646000865660685
 Std Deviation: 2.8902110618633783
Post-processor distribution of 10000 samples using floor method:
 0: 9.62%
 1: 10.48%
 2: 10.32%
 3: 9.78%
 4: 10.1%
 5: 9.98%
 6: 10.03%
 7: 9.88%
 8: 9.85%
 9: 9.96%

Output Analysis: uniform(0.0, 10.0)
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0007837959588220177
 Median: (4.80489115662667, 4.82484920225708)
 Maximum: 9.98965026064113
 Mean: 4.858770190971524
 Std Deviation: 2.9053289351301954
Post-processor distribution of 10000 samples using floor method:
 0: 10.11%
 1: 10.37%
 2: 10.15%
 3: 10.51%
 4: 9.49%
 5: 9.45%
 6: 10.05%
 7: 9.92%
 8: 9.97%
 9: 9.98%

Base Case
Output Analysis: Random.expovariate(1.0)
Typical Timing: 313 ± 14 ns
Statistics of 1024 samples:
 Minimum: 0.0001316700360825842
 Median: (0.6913039062259381, 0.6936870166033268)
 Maximum: 6.818872642116488
 Mean: 1.0101165029510673
 Std Deviation: 1.0140139592361765
Post-processor distribution of 10000 samples using floor method:
 0: 62.73%
 1: 23.54%
 2: 9.0%
 3: 2.86%
 4: 1.23%
 5: 0.44%
 6: 0.14%
 7: 0.05%
 9: 0.01%

Output Analysis: expovariate(1.0)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: 0.00034972692927543223
 Median: (0.7265796147385545, 0.7280041874790373)
 Maximum: 6.991757360862405
 Mean: 1.0106053633992123
 Std Deviation: 0.9573000133146745
Post-processor distribution of 10000 samples using floor method:
 0: 62.24%
 1: 24.01%
 2: 8.86%
 3: 3.0%
 4: 1.12%
 5: 0.52%
 6: 0.13%
 7: 0.08%
 8: 0.03%
 10: 0.01%

Base Case
Output Analysis: Random.gammavariate(2.0, 1.0)
Typical Timing: 1157 ± 66 ns
Statistics of 1024 samples:
 Minimum: 0.07394991134324855
 Median: (1.6823695448152443, 1.6857126685359396)
 Maximum: 12.170349185886773
 Mean: 2.005749622575991
 Std Deviation: 1.4681667195125285
Post-processor distribution of 10000 samples using round method:
 0: 8.61%
 1: 35.55%
 2: 26.4%
 3: 15.07%
 4: 7.98%
 5: 3.46%
 6: 1.58%
 7: 0.77%
 8: 0.33%
 9: 0.14%
 10: 0.06%
 11: 0.03%
 12: 0.02%

Output Analysis: gammavariate(2.0, 1.0)
Typical Timing: 125 ± 11 ns
Statistics of 1024 samples:
 Minimum: 0.014690527978743928
 Median: (1.6312439013262294, 1.6348206605498885)
 Maximum: 9.64630015059904
 Mean: 1.9880477061046065
 Std Deviation: 1.4545362161238342
Post-processor distribution of 10000 samples using round method:
 0: 9.26%
 1: 34.35%
 2: 27.1%
 3: 15.24%
 4: 7.5%
 5: 3.59%
 6: 1.72%
 7: 0.74%
 8: 0.32%
 9: 0.14%
 10: 0.02%
 11: 0.01%
 14: 0.01%

Base Case
Output Analysis: Random.weibullvariate(1.0, 1.0)
Typical Timing: 407 ± 14 ns
Statistics of 1024 samples:
 Minimum: 6.74118228740073e-05
 Median: (0.7213886114369163, 0.7255211038893652)
 Maximum: 7.208505779124245
 Mean: 1.0318908962486315
 Std Deviation: 1.0217264748652426
Post-processor distribution of 10000 samples using floor method:
 0: 62.92%
 1: 23.49%
 2: 8.48%
 3: 3.29%
 4: 1.11%
 5: 0.43%
 6: 0.2%
 7: 0.05%
 8: 0.01%
 9: 0.01%
 10: 0.01%

Output Analysis: weibullvariate(1.0, 1.0)
Typical Timing: 94 ± 13 ns
Statistics of 1024 samples:
 Minimum: 0.0014154846413768883
 Median: (0.7283563961008704, 0.7324662920265946)
 Maximum: 6.263939102711681
 Mean: 0.9965007731596198
 Std Deviation: 0.9496618609389123
Post-processor distribution of 10000 samples using floor method:
 0: 64.02%
 1: 22.68%
 2: 8.69%
 3: 2.9%
 4: 1.0%
 5: 0.36%
 6: 0.27%
 7: 0.06%
 9: 0.01%
 11: 0.01%

Base Case
Output Analysis: Random.betavariate(3.0, 3.0)
Typical Timing: 2469 ± 86 ns
Statistics of 1024 samples:
 Minimum: 0.02970308652342968
 Median: (0.4981588232354882, 0.49961439601764807)
 Maximum: 0.977286379732123
 Mean: 0.5041774932741807
 Std Deviation: 0.18788330798475938
Post-processor distribution of 10000 samples using round method:
 0: 50.26%
 1: 49.74%

Output Analysis: betavariate(3.0, 3.0)
Typical Timing: 188 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.04765998484284484
 Median: (0.5089427417284045, 0.5090798012070167)
 Maximum: 0.9357050870999734
 Mean: 0.5030869392003663
 Std Deviation: 0.1930858989883189
Post-processor distribution of 10000 samples using round method:
 0: 49.52%
 1: 50.48%

Base Case
Output Analysis: Random.paretovariate(4.0)
Typical Timing: 282 ± 13 ns
Statistics of 1024 samples:
 Minimum: 1.0013010722563964
 Median: (1.190056958663205, 1.1902654376971329)
 Maximum: 6.801658712029509
 Mean: 1.3583624862772823
 Std Deviation: 0.5211934520008308
Post-processor distribution of 10000 samples using floor method:
 1: 93.32%
 2: 5.34%
 3: 0.93%
 4: 0.2%
 5: 0.08%
 6: 0.1%
 7: 0.03%

Output Analysis: paretovariate(4.0)
Typical Timing: 63 ± 13 ns
Statistics of 1024 samples:
 Minimum: 1.000480307984482
 Median: (1.1909161234508896, 1.191008641743139)
 Maximum: 5.539856493861284
 Mean: 1.3325996015379562
 Std Deviation: 0.431563715896487
Post-processor distribution of 10000 samples using floor method:
 1: 94.0%
 2: 4.86%
 3: 0.75%
 4: 0.2%
 5: 0.15%
 6: 0.02%
 9: 0.02%

Base Case
Output Analysis: Random.gauss(1.0, 1.0)
Typical Timing: 594 ± 10 ns
Statistics of 1024 samples:
 Minimum: -2.190564649070913
 Median: (1.096290819313381, 1.0965163533878306)
 Maximum: 3.654806062739117
 Mean: 1.0722864368040677
 Std Deviation: 0.9558802321544907
Post-processor distribution of 10000 samples using round method:
 -3: 0.02%
 -2: 0.65%
 -1: 5.86%
 0: 23.6%
 1: 38.55%
 2: 24.25%
 3: 6.4%
 4: 0.63%
 5: 0.04%

Output Analysis: gauss(1.0, 1.0)
Typical Timing: 94 ± 6 ns
Statistics of 1024 samples:
 Minimum: -1.962896617740205
 Median: (1.0107386334754718, 1.0107843737922038)
 Maximum: 4.130931933620957
 Mean: 0.9951344090908586
 Std Deviation: 0.9724548726499896
Post-processor distribution of 10000 samples using round method:
 -3: 0.01%
 -2: 0.59%
 -1: 6.08%
 0: 23.91%
 1: 38.78%
 2: 24.08%
 3: 5.8%
 4: 0.71%
 5: 0.04%

Base Case
Output Analysis: Random.normalvariate(0.0, 2.8)
Typical Timing: 625 ± 41 ns
Statistics of 1024 samples:
 Minimum: -9.011028092963254
 Median: (0.11470795958402581, 0.11622612747884022)
 Maximum: 8.080223077262685
 Mean: 0.0237498977305559
 Std Deviation: 2.810373821872536
Post-processor distribution of 10000 samples using round method:
 -11: 0.01%
 -10: 0.07%
 -9: 0.13%
 -8: 0.24%
 -7: 0.57%
 -6: 1.42%
 -5: 2.9%
 -4: 5.11%
 -3: 8.45%
 -2: 10.89%
 -1: 13.31%
 0: 14.17%
 1: 13.84%
 2: 10.75%
 3: 7.81%
 4: 5.43%
 5: 2.39%
 6: 1.39%
 7: 0.71%
 8: 0.27%
 9: 0.12%
 10: 0.02%

Output Analysis: normalvariate(0.0, 2.8)
Typical Timing: 94 ± 10 ns
Statistics of 1024 samples:
 Minimum: -9.81162415855735
 Median: (-0.040029081075939804, -0.03834111419972398)
 Maximum: 8.405610497028198
 Mean: 0.02956010649229245
 Std Deviation: 2.8782216303350654
Post-processor distribution of 10000 samples using round method:
 -10: 0.03%
 -9: 0.11%
 -8: 0.25%
 -7: 0.59%
 -6: 1.49%
 -5: 2.95%
 -4: 5.43%
 -3: 8.02%
 -2: 11.27%
 -1: 13.14%
 0: 13.59%
 1: 12.51%
 2: 11.27%
 3: 8.51%
 4: 5.19%
 5: 3.01%
 6: 1.64%
 7: 0.66%
 8: 0.24%
 9: 0.08%
 10: 0.02%

Base Case
Output Analysis: Random.lognormvariate(0.0, 0.5)
Typical Timing: 813 ± 41 ns
Statistics of 1024 samples:
 Minimum: 0.2195924808293882
 Median: (1.0178330027092113, 1.0178866630435872)
 Maximum: 4.958327185159613
 Mean: 1.156758692696711
 Std Deviation: 0.602876910210775
Post-processor distribution of 10000 samples using round method:
 0: 7.87%
 1: 71.4%
 2: 17.5%
 3: 2.5%
 4: 0.57%
 5: 0.09%
 6: 0.07%

Output Analysis: lognormvariate(0.0, 0.5)
Typical Timing: 94 ± 8 ns
Statistics of 1024 samples:
 Minimum: 0.22958627153198902
 Median: (0.994480922194363, 0.9954442665549613)
 Maximum: 6.455911790568637
 Mean: 1.1502706437558647
 Std Deviation: 0.6316415808521929
Post-processor distribution of 10000 samples using round method:
 0: 8.61%
 1: 70.51%
 2: 17.4%
 3: 2.77%
 4: 0.53%
 5: 0.11%
 6: 0.06%
 7: 0.01%

Base Case
Output Analysis: Random.vonmisesvariate(0, 0)
Typical Timing: 250 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0016881678868460057
 Median: (3.0942253235570183, 3.0950877799255525)
 Maximum: 6.258552410265742
 Mean: 3.1157433031956114
 Std Deviation: 1.8160662647179846
Post-processor distribution of 10000 samples using floor method:
 0: 16.01%
 1: 16.34%
 2: 15.84%
 3: 16.18%
 4: 15.61%
 5: 15.97%
 6: 4.05%

Output Analysis: vonmisesvariate(0, 0)
Typical Timing: 63 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0030437037313934988
 Median: (3.324061633432509, 3.3316583665343935)
 Maximum: 6.282526743105312
 Mean: 3.237507582060361
 Std Deviation: 1.8161866642691042
Post-processor distribution of 10000 samples using floor method:
 0: 15.93%
 1: 16.08%
 2: 15.94%
 3: 15.89%
 4: 16.21%
 5: 15.68%
 6: 4.27%

Base Case
Output Analysis: Random.triangular(0.0, 10.0, 0.0)
Typical Timing: 469 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0014087509407367804
 Median: (2.934481051078799, 2.9507604381846466)
 Maximum: 9.61339531798091
 Mean: 3.4362101544681645
 Std Deviation: 2.4086234965404434
Post-processor distribution of 10000 samples using floor method:
 0: 18.6%
 1: 17.58%
 2: 14.81%
 3: 12.69%
 4: 11.18%
 5: 8.73%
 6: 7.1%
 7: 5.09%
 8: 3.19%
 9: 1.03%

Output Analysis: triangular(0.0, 10.0, 0.0)
Typical Timing: 32 ± 11 ns
Statistics of 1024 samples:
 Minimum: 0.0014073969442662815
 Median: (2.9462323843968186, 2.946335217727974)
 Maximum: 9.850342458169068
 Mean: 3.3433465167955765
 Std Deviation: 2.34849218154558
Post-processor distribution of 10000 samples using floor method:
 0: 19.26%
 1: 17.76%
 2: 14.55%
 3: 13.21%
 4: 10.68%
 5: 9.19%
 6: 6.48%
 7: 5.0%
 8: 3.07%
 9: 0.8%

Base Case
Output Analysis: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 750 ± 25 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5654296875
 Std Deviation: 2.8814328280659955
Distribution of 10000 samples:
 0: 10.04%
 1: 9.93%
 2: 9.52%
 3: 10.03%
 4: 10.06%
 5: 10.14%
 6: 10.35%
 7: 9.94%
 8: 9.87%
 9: 10.12%

Output Analysis: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 63 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.6083984375
 Std Deviation: 2.8253093972282013
Distribution of 10000 samples:
 0: 9.88%
 1: 10.25%
 2: 10.39%
 3: 10.26%
 4: 10.3%
 5: 9.92%
 6: 9.55%
 7: 10.43%
 8: 9.92%
 9: 9.1%

Base Case
Output Analysis: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Typical Timing: 2282 ± 22 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0693359375
 Std Deviation: 2.4992818418033287
Distribution of 10000 samples:
 0: 18.16%
 1: 16.11%
 2: 14.72%
 3: 12.98%
 4: 10.66%
 5: 8.97%
 6: 7.13%
 7: 5.48%
 8: 3.79%
 9: 2.0%

Output Analysis: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Typical Timing: 1157 ± 15 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 2
 Maximum: 9
 Mean: 2.99609375
 Std Deviation: 2.390921321456625
Distribution of 10000 samples:
 0: 18.16%
 1: 16.41%
 2: 14.45%
 3: 12.22%
 4: 11.01%
 5: 9.19%
 6: 7.27%
 7: 5.66%
 8: 3.83%
 9: 1.8%

Base Case
Output Analysis: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Typical Timing: 1719 ± 12 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0185546875
 Std Deviation: 2.4016627225285982
Distribution of 10000 samples:
 0: 18.1%
 1: 17.08%
 2: 13.93%
 3: 12.2%
 4: 10.95%
 5: 9.56%
 6: 7.43%
 7: 5.51%
 8: 3.52%
 9: 1.72%

Output Analysis: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Typical Timing: 688 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.033203125
 Std Deviation: 2.490425673050935
Distribution of 10000 samples:
 0: 18.17%
 1: 17.03%
 2: 14.1%
 3: 12.46%
 4: 10.8%
 5: 9.27%
 6: 6.79%
 7: 5.65%
 8: 3.7%
 9: 2.03%

Base Case
Timer only: random.shuffle(some_list) of size 10:
Typical Timing: 6875 ± 170 ns

Timer only: shuffle(some_list) of size 10:
Typical Timing: 500 ± 1 ns

Base Case
Output Analysis: Random.sample([4, 6, 2, 5, 3, 7, 1, 9, 8, 0], k=3)
Typical Timing: 3969 ± 55 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.470703125
 Std Deviation: 2.9254539201723566
Distribution of 10000 samples:
 0: 10.13%
 1: 9.8%
 2: 10.42%
 3: 10.06%
 4: 9.81%
 5: 9.98%
 6: 9.66%
 7: 9.74%
 8: 9.86%
 9: 10.54%

Output Analysis: sample([4, 6, 2, 5, 3, 7, 1, 9, 8, 0], k=3)
Typical Timing: 844 ± 11 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5751953125
 Std Deviation: 2.8614486759097377
Distribution of 10000 samples:
 0: 9.59%
 1: 9.77%
 2: 10.1%
 3: 10.24%
 4: 10.22%
 5: 10.2%
 6: 10.08%
 7: 10.6%
 8: 9.75%
 9: 9.45%


Total Test Time: 1.474 sec

```
