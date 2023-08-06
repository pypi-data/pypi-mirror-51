# RNG Engine for Python3
- Python3 interface to the c++ random library
- Designed for python developers familiar with the c++ random header
- Warning: RNG is not suitable for cryptography or secure hashing.

### Quick Install for Mac
``` 
$ pip install RNG
$ python3
Python 3.7.3
>>> import RNG
>>> RNG.generate_canonical()
0.39652726016896334
```
### Installation may require the following:
- Python 3.7 or later.
- Cython, python module available: `pip install Cython`
- Python3 developer environment, setuptools etc.
- Modern C++17 Compiler and Standard Library, Clang or GCC.

### Sister Projects:
- Fortuna: Collection of abstractions to make custom random value generators. https://pypi.org/project/Fortuna/
- Pyewacket: Complete drop-in replacement for the Python3 random module. https://pypi.org/project/Pyewacket/
- MonkeyTimer: Framework for testing non-deterministic value generators. https://pypi.org/project/MonkeyTimer/

Support these and other random projects: https://www.patreon.com/brokencode

---

## RNG Specifications

#### Random Boolean
- `RNG.bernoulli_variate(ratio_of_truth: float) -> bool`
    - Produces a Bernoulli distribution of boolean values.
    - @param ratio_of_truth :: the probability of True. Expected input range: `[0.0, 1.0]`, clamped.
    - @return :: True or False
```python
# bernoulli_variate.py
from RNG import bernoulli_variate


print(bernoulli_variate(0.25))
# prints a random boolean, 25% probability of True
```

#### Random Integer
- `RNG.uniform_int_variate(left_limit: int, right_limit: int) -> int`
    - Flat uniform distribution.
    - 20x faster than random.randint()
    - @param left_limit :: input A.
    - @param right_limit :: input B. 
    - @return :: random integer in the inclusive range `[A, B]` or `[B, A]` if B < A
```python
# uniform_int_variate.py
from RNG import uniform_int_variate


print(uniform_int_variate(-6, 5))
# prints a random int in range [-6, 5]
```

- `RNG.binomial_variate(number_of_trials: int, probability: float) -> int`
    - Based on the idea of flipping a coin and counting how many heads come up after some number of flips.
    - @param number_of_trials :: how many times to flip a coin.
    - @param probability :: how likely heads will be flipped. 0.5 is a fair coin. 1.0 is a double headed coin.
    - @return :: count of how many heads came up.
- `RNG.negative_binomial_variate(trial_successes: int, probability: float) -> int`
    - Based on the idea of flipping a coin as long as it takes to succeed.
    - @param trial_successes :: the required number of heads flipped to succeed.
    - @param probability :: how likely heads will be flipped. 0.50 is a fair coin.
    - @return :: the count of how many tails came up before the required number of heads.
- `RNG.geometric_variate(probability: float) -> int`
    - Same as random_negative_binomial(1, probability). 
- `RNG.poisson_variate(mean: float) -> int`
    - @param mean :: sets the average output of the function.
    - @return :: random integer, poisson distribution centered on the mean.


#### Random Floating Point
- `RNG.generate_canonical() -> float`
    - Evenly distributes floats of maximum precision.
    - @return :: random float in range (0.0, 1.0)
```python
# generate_canonical.py
from RNG import generate_canonical


print(generate_canonical())
# prints a random float in range (0.0, 1.0)
```
- `RNG.uniform_real_variate(left_limit: float, right_limit: float) -> float`
    - Flat uniform distribution of floats.
    - @return :: random Float between left_limit and right_limit.
- `RNG.normal_variate(mean: float, std_dev: float) -> float`
    - @param mean :: sets the average output of the function.
    - @param std_dev :: standard deviation. Specifies spread of data from the mean.
- `RNG.lognormal_variate(log_mean: float, log_deviation: float) -> float`
    - @param log_mean :: sets the log of the mean of the function.
    - @param log_deviation :: log of the standard deviation. Specifies spread of data from the mean.
- `RNG.exponential_variate(lambda_rate: float) -> float`
    - Produces random non-negative floating-point values, distributed according to probability density function.
    - @param lambda_rate :: λ constant rate of a random event per unit of time/distance.
    - @return :: The time/distance until the next random event. For example, this distribution describes the time between the clicks of a Geiger counter or the distance between point mutations in a DNA strand.
- `RNG.gamma_variate(shape: float, scale: float) -> float`
    - Generalization of the exponential distribution.
    - Produces random positive floating-point values, distributed according to probability density function.    
    - @param shape :: α the number of independent exponentially distributed random variables.
    - @param scale :: β the scale factor or the mean of each of the distributed random variables.
    - @return :: the sum of α independent exponentially distributed random variables, each of which has a mean of β.
- `RNG.weibull_variate(shape: float, scale: float) -> float`
    - Generalization of the exponential distribution.
    - Similar to the gamma distribution but uses a closed form distribution function.
    - Popular in reliability and survival analysis.
- `RNG.extreme_value_variate(location: float, scale: float) -> float`
    - Based on Extreme Value Theory. 
    - Used for statistical models of the magnitude of earthquakes and volcanoes.
- `RNG.chi_squared_variate(degrees_of_freedom: float) -> float`
    - Used with the Chi Squared Test and Null Hypotheses to test if sample data fits an expected distribution.
- `RNG.cauchy_variate(location: float, scale: float) -> float`
    - @param location :: It specifies the location of the peak. The default value is 0.0.
    - @param scale :: It represents the half-width at half-maximum. The default value is 1.0.
    - @return :: Continuous Distribution.
- `RNG.fisher_f_variate(degrees_of_freedom_1: float, degrees_of_freedom_2: float) -> float`
    - F distributions often arise when comparing ratios of variances.
- `RNG.student_t_variate(degrees_of_freedom: float) -> float`
    - T distribution. Same as a normal distribution except it uses the sample standard deviation rather than the population standard deviation.
    - As degrees_of_freedom goes to infinity it converges with the normal distribution.


## Development Log
##### RNG 1.5.1
- A number of testing routines have been extracted into a new module: MonkeyTimer.
    - distribution
    - timer
    - distribution_timer

##### RNG 1.5.0, internal
- Further API Refinements, new naming convention for variate generators: `<algorithm name>_variate`

##### RNG 1.4.2
- Install script update
- Test tweaks for noise reduction in timing tests.

##### RNG 1.4.1
- Test Patch for new API
- Documentation Updates

##### RNG 1.4.0
- API Refactoring

##### RNG 1.3.4
- Storm Update 3.1.1

##### RNG 1.3.3
- Installer script update

##### RNG 1.3.2
- Minor Bug Fix

##### RNG 1.3.1
- Test Update

##### RNG 1.3.1
- Fixed Typos

##### RNG 1.3.0
- Storm Update

##### RNG 1.2.5
- Low level clean up

##### RNG 1.2.4
- Minor Typos Fixed

##### RNG 1.2.3
- Documentation Update
- Test Update
- Bug Fixes

##### RNG 1.0.0 - 1.2.2, internal
- API Changes:
    - randint changed to random_int
    - randbelow changed to random_below
    - random changed to generate_canonical
    - uniform changed to random_float

##### RNG 0.2.3
- Bug Fixes

##### RNG 0.2.2
- discrete() removed.

##### RNG 0.2.1
- minor typos
- discrete() depreciated.

##### RNG 0.2.0
- Major Rebuild.

##### RNG 0.1.22
- The RNG Storm Engine is now the default standard.
- Experimental Vortex Engine added for testing.

##### RNG 0.1.21 beta
- Small update to the testing suite.

##### RNG 0.1.20 beta
- Changed default inputs for random_int and random_below to sane values.
    - random_int(left_limit=1, right_limit=20) down from `-2**63, 2**63 - 1`
    - random_below(upper_bound=10) down from `2**63 - 1`

##### RNG 0.1.19 beta
- Broke some fixed typos, for a change of pace.

##### RNG 0.1.18 beta
- Fixed some typos.

##### RNG 0.1.17 beta
- Major Refactoring.
- New primary engine: Hurricane.
- Experimental engine Typhoon added: random_below() only.

##### RNG 0.1.16 beta
- Internal Engine Performance Tuning. 

##### RNG 0.1.15 beta
- Engine Testing.

##### RNG 0.1.14 beta
- Fixed a few typos.

##### RNG 0.1.13 beta
- Fixed a few typos.

##### RNG 0.1.12 beta
- Major Test Suite Upgrade.
- Major Bug Fixes.
    - Removed several 'foot-guns' in prep for fuzz testing in future releases.

##### RNG 0.1.11 beta
- Fixed small bug in the install script.

##### RNG 0.1.10 beta
- Fixed some typos.

##### RNG 0.1.9 beta
- Fixed some typos.

##### RNG 0.1.8 beta
- Fixed some typos.
- More documentation added.

##### RNG 0.1.7 beta
- The `random_floating_point` function renamed to `random_float`.
- The function `c_rand()` has been removed as well as all the cruft it required.
- Major Documentation Upgrade.
- Fixed an issue where keyword arguments would fail to propagate. Both, positional args and kwargs now work as intended.
- Added this Dev Log.

##### RNG 0.0.6 alpha
- Minor ABI changes.

##### RNG 0.0.5 alpha
- Tests redesigned slightly for Float functions.

##### RNG 0.0.4 alpha
- Random Float Functions Implemented.

##### RNG 0.0.3 alpha
- Random Integer Functions Implemented.

##### RNG 0.0.2 alpha
- Random Bool Function Implemented.

##### RNG 0.0.1 pre-alpha
- Planning & Design.


## MonkeyTimer: Distribution and Performance Test Suite
```
Quick Test: RNG Storm Engine
=========================================================================

Boolean Variate Distributions

Output Analysis: bernoulli_variate(0.0)
Typical Timing: 32 ± 12 ns
Statistics of 1024 samples:
 Minimum: False
 Median: False
 Maximum: False
 Mean: 0
 Std Deviation: 0.0
Distribution of 10240 samples:
 False: 100.0%

Output Analysis: bernoulli_variate(0.3333333333333333)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.34375
 Std Deviation: 0.47519096331149147
Distribution of 10240 samples:
 False: 66.201171875%
 True: 33.798828125%

Output Analysis: bernoulli_variate(0.5)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: False
 Median: True
 Maximum: True
 Mean: 0.521484375
 Std Deviation: 0.4997823023144626
Distribution of 10240 samples:
 False: 49.0625%
 True: 50.9375%

Output Analysis: bernoulli_variate(0.6666666666666666)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: False
 Median: True
 Maximum: True
 Mean: 0.6513671875
 Std Deviation: 0.4767703398158829
Distribution of 10240 samples:
 False: 32.412109375%
 True: 67.587890625%

Output Analysis: bernoulli_variate(1.0)
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: True
 Median: True
 Maximum: True
 Mean: 1
 Std Deviation: 0.0
Distribution of 10240 samples:
 True: 100.0%


Integer Variate Distributions

Base Case
Output Analysis: Random.randint(1, 6)
Typical Timing: 1188 ± 18 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 3
 Maximum: 6
 Mean: 3.51171875
 Std Deviation: 1.7164204309541053
Distribution of 10240 samples:
 1: 16.748046875%
 2: 16.748046875%
 3: 16.7578125%
 4: 16.171875%
 5: 17.119140625%
 6: 16.455078125%

Output Analysis: uniform_int_variate(1, 6)
Typical Timing: 63 ± 13 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 3
 Maximum: 6
 Mean: 3.49609375
 Std Deviation: 1.706747111851172
Distribution of 10240 samples:
 1: 17.216796875%
 2: 16.58203125%
 3: 16.640625%
 4: 16.201171875%
 5: 16.89453125%
 6: 16.46484375%

Output Analysis: binomial_variate(4, 0.5)
Typical Timing: 125 ± 6 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 2
 Maximum: 4
 Mean: 1.990234375
 Std Deviation: 0.9876571326534981
Distribution of 10240 samples:
 0: 5.83984375%
 1: 25.771484375%
 2: 37.021484375%
 3: 24.990234375%
 4: 6.376953125%

Output Analysis: negative_binomial_variate(5, 0.75)
Typical Timing: 125 ± 6 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 1
 Maximum: 9
 Mean: 1.642578125
 Std Deviation: 1.4317935739712264
Distribution of 10240 samples:
 0: 23.505859375%
 1: 30.048828125%
 2: 21.9140625%
 3: 13.046875%
 4: 6.806640625%
 5: 2.744140625%
 6: 1.220703125%
 7: 0.458984375%
 8: 0.17578125%
 9: 0.05859375%
 10: 0.01953125%

Output Analysis: geometric_variate(0.75)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 0
 Maximum: 6
 Mean: 0.3349609375
 Std Deviation: 0.6949815910960272
Distribution of 10240 samples:
 0: 74.892578125%
 1: 18.57421875%
 2: 4.94140625%
 3: 1.142578125%
 4: 0.29296875%
 5: 0.078125%
 6: 0.05859375%
 7: 0.01953125%

Output Analysis: poisson_variate(4.5)
Typical Timing: 125 ± 1 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 14
 Mean: 4.5224609375
 Std Deviation: 2.161487169159546
Distribution of 10240 samples:
 0: 1.25%
 1: 4.6875%
 2: 10.986328125%
 3: 17.197265625%
 4: 18.28125%
 5: 16.826171875%
 6: 13.02734375%
 7: 8.662109375%
 8: 4.853515625%
 9: 2.40234375%
 10: 1.005859375%
 11: 0.546875%
 12: 0.166015625%
 13: 0.078125%
 14: 0.029296875%


Floating Point Variate Distributions

Base Case
Output Analysis: Random.random()
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0006388470747341612
 Median: (0.4583390582236725, 0.4589449537736383)
 Maximum: 0.9998833078220133
 Mean: 0.47560204568672454
 Std Deviation: 0.28999057863750183
Post-processor distribution of 10240 samples using round method:
 0: 50.693359375%
 1: 49.306640625%

Output Analysis: generate_canonical()
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0004296508719445195
 Median: (0.4917702846481638, 0.49188511675337104)
 Maximum: 0.9978423639409355
 Mean: 0.49181897826571025
 Std Deviation: 0.2876430386292914
Post-processor distribution of 10240 samples using round method:
 0: 49.658203125%
 1: 50.341796875%

Output Analysis: uniform_real_variate(0.0, 10.0)
Typical Timing: 94 ± 12 ns
Statistics of 1024 samples:
 Minimum: 0.0019713906008227973
 Median: (5.0088507641964055, 5.009507796219312)
 Maximum: 9.987524245931592
 Mean: 5.064104214610925
 Std Deviation: 2.9217505674564164
Post-processor distribution of 10240 samples using floor method:
 0: 9.94140625%
 1: 10.234375%
 2: 10.15625%
 3: 10.380859375%
 4: 9.951171875%
 5: 10.01953125%
 6: 9.873046875%
 7: 9.62890625%
 8: 9.931640625%
 9: 9.8828125%

Base Case
Output Analysis: Random.expovariate(1.0)
Typical Timing: 344 ± 10 ns
Statistics of 1024 samples:
 Minimum: 8.208047312447906e-05
 Median: (0.6686009795871479, 0.6721875885943366)
 Maximum: 7.8351444976253335
 Mean: 0.9571749101061867
 Std Deviation: 0.9753799224623942
Post-processor distribution of 10240 samples using floor method:
 0: 63.310546875%
 1: 23.076171875%
 2: 8.681640625%
 3: 3.02734375%
 4: 1.083984375%
 5: 0.576171875%
 6: 0.146484375%
 7: 0.048828125%
 8: 0.01953125%
 9: 0.009765625%
 11: 0.01953125%

Output Analysis: exponential_variate(1.0)
Typical Timing: 63 ± 10 ns
Statistics of 1024 samples:
 Minimum: 0.0013282608302530423
 Median: (0.6690274531506568, 0.669316218295648)
 Maximum: 8.748834094909625
 Mean: 1.0318402860279123
 Std Deviation: 1.0548016848406403
Post-processor distribution of 10240 samples using floor method:
 0: 63.61328125%
 1: 22.587890625%
 2: 8.603515625%
 3: 3.310546875%
 4: 1.162109375%
 5: 0.46875%
 6: 0.17578125%
 7: 0.0390625%
 8: 0.01953125%
 9: 0.01953125%

Base Case
Output Analysis: Random.gammavariate(1.0, 1.0)
Typical Timing: 469 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.0006029624140358793
 Median: (0.7315241311192433, 0.7353963314603675)
 Maximum: 7.196638281972511
 Mean: 1.0011919746296876
 Std Deviation: 0.9634904644142317
Post-processor distribution of 10240 samples using floor method:
 0: 64.130859375%
 1: 22.03125%
 2: 8.80859375%
 3: 3.154296875%
 4: 1.240234375%
 5: 0.41015625%
 6: 0.126953125%
 7: 0.05859375%
 8: 0.029296875%
 10: 0.009765625%

Output Analysis: gamma_variate(1.0, 1.0)
Typical Timing: 63 ± 11 ns
Statistics of 1024 samples:
 Minimum: 0.0005988820827224266
 Median: (0.6857081774501348, 0.686356057608084)
 Maximum: 7.263998659948883
 Mean: 0.9806944084458747
 Std Deviation: 0.9622234373186321
Post-processor distribution of 10240 samples using floor method:
 0: 63.0859375%
 1: 23.4765625%
 2: 8.955078125%
 3: 2.8515625%
 4: 0.9375%
 5: 0.44921875%
 6: 0.13671875%
 7: 0.09765625%
 8: 0.009765625%

Base Case
Output Analysis: Random.weibullvariate(1.0, 1.0)
Typical Timing: 407 ± 16 ns
Statistics of 1024 samples:
 Minimum: 3.0687715901322686e-05
 Median: (0.668937878075442, 0.6701855697870736)
 Maximum: 5.840822106883279
 Mean: 0.9672608159897019
 Std Deviation: 0.9480419472328683
Post-processor distribution of 10240 samples using floor method:
 0: 63.408203125%
 1: 23.0078125%
 2: 8.65234375%
 3: 3.251953125%
 4: 1.11328125%
 5: 0.3515625%
 6: 0.126953125%
 7: 0.068359375%
 8: 0.01953125%

Output Analysis: weibull_variate(1.0, 1.0)
Typical Timing: 94 ± 15 ns
Statistics of 1024 samples:
 Minimum: 0.00014086748786664374
 Median: (0.6945683032536986, 0.6982508879406859)
 Maximum: 5.80290970777546
 Mean: 0.9892732402317378
 Std Deviation: 0.9445212781958421
Post-processor distribution of 10240 samples using floor method:
 0: 62.8125%
 1: 23.828125%
 2: 8.80859375%
 3: 2.8515625%
 4: 1.005859375%
 5: 0.44921875%
 6: 0.185546875%
 7: 0.01953125%
 8: 0.01953125%
 9: 0.01953125%

Output Analysis: extreme_value_variate(0.0, 1.0)
Typical Timing: 63 ± 11 ns
Statistics of 1024 samples:
 Minimum: -2.2549353788055053
 Median: (0.3760487699667133, 0.3766491002847829)
 Maximum: 7.953843598096162
 Mean: 0.572674798704818
 Std Deviation: 1.2480372336144154
Post-processor distribution of 10240 samples using round method:
 -2: 1.0546875%
 -1: 17.919921875%
 0: 35.400390625%
 1: 25.205078125%
 2: 12.51953125%
 3: 5.15625%
 4: 1.669921875%
 5: 0.615234375%
 6: 0.263671875%
 7: 0.126953125%
 8: 0.048828125%
 9: 0.009765625%
 10: 0.009765625%

Base Case
Output Analysis: Random.gauss(5.0, 2.0)
Typical Timing: 594 ± 12 ns
Statistics of 1024 samples:
 Minimum: -1.5155551600414325
 Median: (4.900045625318894, 4.910640304340043)
 Maximum: 10.074285309328179
 Mean: 4.903701264243073
 Std Deviation: 1.9284195623352982
Post-processor distribution of 10240 samples using round method:
 -3: 0.009765625%
 -2: 0.09765625%
 -1: 0.15625%
 0: 1.044921875%
 1: 2.802734375%
 2: 6.513671875%
 3: 11.865234375%
 4: 17.36328125%
 5: 20.126953125%
 6: 17.861328125%
 7: 11.669921875%
 8: 6.650390625%
 9: 2.71484375%
 10: 0.830078125%
 11: 0.244140625%
 12: 0.0390625%
 13: 0.009765625%

Output Analysis: normal_variate(5.0, 2.0)
Typical Timing: 94 ± 11 ns
Statistics of 1024 samples:
 Minimum: -1.6386997496778761
 Median: (4.893535541707389, 4.8952247982158745)
 Maximum: 11.47237356973277
 Mean: 4.989727450891901
 Std Deviation: 2.0086474955642575
Post-processor distribution of 10240 samples using round method:
 -2: 0.05859375%
 -1: 0.224609375%
 0: 0.869140625%
 1: 2.392578125%
 2: 6.865234375%
 3: 11.943359375%
 4: 17.6953125%
 5: 19.443359375%
 6: 17.216796875%
 7: 12.041015625%
 8: 7.138671875%
 9: 2.783203125%
 10: 1.015625%
 11: 0.25390625%
 12: 0.048828125%
 13: 0.009765625%

Base Case
Output Analysis: Random.lognormvariate(1.6, 0.25)
Typical Timing: 844 ± 37 ns
Statistics of 1024 samples:
 Minimum: 2.477424724086346
 Median: (4.900857180539914, 4.901204763837707)
 Maximum: 12.011155123497085
 Mean: 5.052798380724913
 Std Deviation: 1.2653879254348632
Post-processor distribution of 10240 samples using round method:
 2: 0.244140625%
 3: 8.330078125%
 4: 26.240234375%
 5: 31.220703125%
 6: 20.17578125%
 7: 9.111328125%
 8: 3.251953125%
 9: 1.015625%
 10: 0.322265625%
 11: 0.068359375%
 12: 0.009765625%
 13: 0.009765625%

Output Analysis: lognormal_variate(1.6, 0.25)
Typical Timing: 94 ± 6 ns
Statistics of 1024 samples:
 Minimum: 2.3183785808960096
 Median: (4.874986177263607, 4.876857798124825)
 Maximum: 11.730007308909611
 Mean: 5.0532590833629625
 Std Deviation: 1.2985639553150765
Post-processor distribution of 10240 samples using round method:
 2: 0.302734375%
 3: 8.30078125%
 4: 26.9140625%
 5: 30.8203125%
 6: 19.609375%
 7: 9.08203125%
 8: 3.49609375%
 9: 1.025390625%
 10: 0.37109375%
 11: 0.048828125%
 12: 0.029296875%

Output Analysis: chi_squared_variate(1.0)
Typical Timing: 125 ± 13 ns
Statistics of 1024 samples:
 Minimum: 4.936117433434296e-07
 Median: (0.4459156690762514, 0.4465653999002458)
 Maximum: 10.791875060714037
 Mean: 1.044424368814932
 Std Deviation: 1.5011087023219227
Post-processor distribution of 10240 samples using floor method:
 0: 68.37890625%
 1: 15.91796875%
 2: 7.6171875%
 3: 3.59375%
 4: 1.787109375%
 5: 1.19140625%
 6: 0.625%
 7: 0.419921875%
 8: 0.244140625%
 9: 0.068359375%
 10: 0.068359375%
 11: 0.048828125%
 12: 0.029296875%
 13: 0.009765625%

Output Analysis: cauchy_variate(0.0, 1.0)
Typical Timing: 63 ± 8 ns
Statistics of 1024 samples:
 Minimum: -470.67404141176274
 Median: (0.07716803089648394, 0.0842124948591796)
 Maximum: 1719.0816436410664
 Mean: 0.665703585009031
 Std Deviation: 59.31979062261256
Post-processor distribution of 10240 samples using floor_mod_10 method:
 0: 26.03515625%
 1: 11.083984375%
 2: 5.91796875%
 3: 3.994140625%
 4: 3.232421875%
 5: 2.98828125%
 6: 3.73046875%
 7: 5.48828125%
 8: 11.69921875%
 9: 25.830078125%

Output Analysis: fisher_f_variate(8.0, 8.0)
Typical Timing: 188 ± 14 ns
Statistics of 1024 samples:
 Minimum: 0.05459418873515563
 Median: (0.9919763938480465, 0.9943128957909915)
 Maximum: 12.175780106763689
 Mean: 1.329020084097388
 Std Deviation: 1.209412184995222
Post-processor distribution of 10240 samples using floor method:
 0: 50.361328125%
 1: 32.5390625%
 2: 10.25390625%
 3: 3.642578125%
 4: 1.484375%
 5: 0.771484375%
 6: 0.380859375%
 7: 0.244140625%
 8: 0.068359375%
 9: 0.078125%
 10: 0.0390625%
 11: 0.029296875%
 12: 0.0390625%
 13: 0.01953125%
 14: 0.01953125%
 16: 0.009765625%
 17: 0.009765625%
 25: 0.009765625%

Output Analysis: student_t_variate(8.0)
Typical Timing: 157 ± 14 ns
Statistics of 1024 samples:
 Minimum: -3.6063905568291186
 Median: (-0.023436101947007702, -0.02125804725939844)
 Maximum: 5.463724716098776
 Mean: 0.03336687922475384
 Std Deviation: 1.158115050869326
Post-processor distribution of 10240 samples using round method:
 -6: 0.0390625%
 -5: 0.087890625%
 -4: 0.302734375%
 -3: 1.533203125%
 -2: 6.73828125%
 -1: 23.125%
 0: 36.953125%
 1: 22.626953125%
 2: 6.728515625%
 3: 1.4453125%
 4: 0.322265625%
 5: 0.078125%
 6: 0.01953125%


=========================================================================
Total Test Time: 0.5838 seconds

```
