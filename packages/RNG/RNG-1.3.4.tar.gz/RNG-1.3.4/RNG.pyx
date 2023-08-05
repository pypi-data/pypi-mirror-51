#!python3
#distutils: language = c++


__all__ = (
    "bernoulli", "random_int", "random_below",
    "binomial", "negative_binomial", "geometric", "poisson",
    "generate_canonical", "random_float", "normalvariate", "lognormvariate",
    "expovariate", "gammavariate", "weibullvariate", "extreme_value",
    "chi_squared", "cauchy", "fisher_f", "student_t",
    "distribution_timer", "timer", "quick_test", "numeric_tests"
)


cdef extern from "Storm.hpp":
    long long _min_int              "Storm::min_int"()
    long long _max_int              "Storm::max_int"()
    double    _min_float            "Storm::min_float"()
    double    _max_float            "Storm::max_float"()
    double    _min_below            "Storm::min_below"()
    double    _min_above            "Storm::min_above"()
    int       _bernoulli            "Storm::bernoulli"(double)
    long long _random_int           "Storm::random_int"(long long, long long)
    long long _random_below         "Storm::random_below"(long long)
    long long _binomial             "Storm::binomial"(long long, double)
    long long _negative_binomial    "Storm::negative_binomial"(long long, double)
    long long _geometric            "Storm::geometric"(double)
    long long _poisson              "Storm::poisson"(double)
    double    _generate_canonical   "Storm::generate_canonical"()
    double    _random_float         "Storm::random_float"(double, double)
    double    _expovariate          "Storm::expovariate"(double)
    double    _gammavariate         "Storm::gammavariate"(double, double)
    double    _weibullvariate       "Storm::weibullvariate"(double, double)
    double    _normalvariate        "Storm::normalvariate"(double, double)
    double    _lognormvariate       "Storm::lognormvariate"(double, double)
    double    _extreme_value        "Storm::extreme_value"(double, double)
    double    _chi_squared          "Storm::chi_squared"(double)
    double    _cauchy               "Storm::cauchy"(double, double)
    double    _fisher_f             "Storm::fisher_f"(double, double)
    double    _student_t            "Storm::student_t"(double)


# RANDOM BOOLEAN #
def bernoulli(ratio_of_truth) -> bool:
    return _bernoulli(ratio_of_truth) == 1


# RANDOM INTEGER #
def random_int(left_limit, right_limit) -> int:
    return _random_int(left_limit, right_limit)

def random_below(upper_bound) -> int:
    return _random_below(upper_bound)

def binomial(number_of_trials, probability) -> int:
    return _binomial(number_of_trials, probability)

def negative_binomial(number_of_trials, probability) -> int:
    return _negative_binomial(number_of_trials, probability)

def geometric(probability) -> int:
    return _geometric(probability)

def poisson(mean) -> int:
    return _poisson(mean)


# RANDOM FLOATING POINT #
def generate_canonical():
    return _generate_canonical()

def random_float(left_limit, right_limit) -> float:
    return _random_float(left_limit, right_limit)
    
def expovariate(lambda_rate) -> float:
    return _expovariate(lambda_rate)
    
def gammavariate(shape, scale) -> float:
    return _gammavariate(shape, scale)
    
def weibullvariate(shape, scale) -> float:
    return _weibullvariate(shape, scale)
    
def extreme_value(location, scale) -> float:
    return _extreme_value(location, scale)
    
def normalvariate(mean, std_dev) -> float:
    return _normalvariate(mean, std_dev)
    
def lognormvariate(log_mean, log_deviation) -> float:
    return _lognormvariate(log_mean, log_deviation)
    
def chi_squared(degrees_of_freedom) -> float:
    return _chi_squared(degrees_of_freedom)
    
def cauchy(location, scale) -> float:
    return _cauchy(location, scale)
    
def fisher_f(degrees_of_freedom_1, degrees_of_freedom_2) -> float:
    return _fisher_f(degrees_of_freedom_1, degrees_of_freedom_2)
    
def student_t(degrees_of_freedom) -> float:
    return _student_t(degrees_of_freedom)


# DISTRIBUTION & PERFORMANCE TEST SUITE #
def timer(func: staticmethod, *args, cycles=32, silent=False, **kwargs):
    import time as _time
    import math as _math
    import statistics as _statistics

    def inner_timer():
        results = []
        for _ in range(cycles):
            start = _time.time_ns()
            for _ in range(cycles):
                _ = func(*args, **kwargs)
            end = _time.time_ns()
            t_time = end - start
            results.append(t_time / cycles)
        m = min(results)
        n = _statistics.stdev(results) / 2
        return m, max(1, n)

    results = [inner_timer() for _ in range(cycles)]
    m, n = min(results, key=lambda x: x[1])
    if not silent:
        print(f"Typical Timing: {_math.ceil(m)} ± {_math.ceil(n)} ns")


def distribution(func: staticmethod, *args, num_cycles=10000, post_processor: staticmethod = None, **kwargs):
    import statistics as _statistics

    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    try:
        stat_samples = results[:min(1000, num_cycles)]
        if type(stat_samples[0]) == type(""):
            stat_samples = list(map(float, stat_samples))
        ave = _statistics.mean(stat_samples)
        median_lo = _statistics.median_low(stat_samples)
        median_hi = _statistics.median_high(stat_samples)
        median = median_lo if median_lo == median_hi else (median_lo, median_hi)
        std_dev = _statistics.stdev(stat_samples, ave)
        output = (
            f" Minimum: {min(stat_samples)}",
            f" Median: {median}",
            f" Maximum: {max(stat_samples)}",
            f" Mean: {ave}",
            f" Std Deviation: {std_dev}",
        )
        print(f"Statistics of {len(stat_samples)} Samples:")
        print("\n".join(output))
    except:
        pass
    if post_processor is None:
        processed_results = results
        print(f"Distribution of {num_cycles} Samples:")
        unique_results = list(set(results))
    else:
        processed_results = list(map(post_processor, results))
        unique_results = list(set(processed_results))
        print(f"Post-processor Distribution of {num_cycles} Samples using {post_processor.__name__} method:")
    try:
        unique_results.sort()
    except TypeError:
        pass
    result_obj = {
        key: f"{processed_results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f" {key}: {val}")


def distribution_timer(func: staticmethod, *args, num_cycles=10000, label="", post_processor=None, **kwargs):
    def quote_str(value):
        return f'"{value}"' if type(value) is str else str(value)

    arguments = ', '.join([quote_str(v) for v in args] + [f'{k}={quote_str(v)}' for k, v in kwargs.items()])
    if label:
        print(f"Output Analysis: {label}")
    elif hasattr(func, "__qualname__"):
        print(f"Output Analysis: {func.__qualname__}({arguments})")
    elif hasattr(func, "__name__"):
        print(f"Output Analysis: {func.__name__}({arguments})")
    else:
        print(f"Output Analysis: {func}({arguments})")
    timer(func, *args, **kwargs)
    distribution(func, *args, num_cycles=num_cycles, post_processor=post_processor, **kwargs)
    print("")


def numeric_tests():
    output = (
        "Round Trip Numeric Limits:",
        f" Min Integer: {_min_int()}",
        f" Max Integer:  {_max_int()}",
        f" Min Float: {_min_float()}",
        f" Max Float:  {_max_float()}",
        f" Min Below Zero: {_min_below()}",
        f" Min Above Zero:  {_min_above()}",
    )
    return "\n".join(output)


def quick_test(n=10000):
    import time as _time
    import math as _math
    import random as _random

    def floor_mod_10(x):
        return _math.floor(x) % 10

    print("\nQuick Test: RNG Storm Engine\n")
    start = _time.time()
    print(numeric_tests())
    print("\n\nBinary Tests\n")
    distribution_timer(bernoulli, 1/3, num_cycles=n)
    print("\nInteger Tests\n")
    print("Base Case")
    distribution_timer(_random.randint, 1, 6, num_cycles=n)
    distribution_timer(random_int, 1, 6, num_cycles=n)
    print("Base Case")
    distribution_timer(_random.randrange, 6, num_cycles=n)
    distribution_timer(random_below, 6, num_cycles=n)
    distribution_timer(binomial, 4, 0.5, num_cycles=n)
    distribution_timer(negative_binomial, 5, 0.75, num_cycles=n)
    distribution_timer(geometric, 0.75, num_cycles=n)
    distribution_timer(poisson, 4.5, num_cycles=n)
    print("\nFloating Point Tests\n")
    print("Base Case")
    distribution_timer(_random.random, num_cycles=n, post_processor=round)
    distribution_timer(generate_canonical, num_cycles=n, post_processor=round)
    distribution_timer(random_float, 0.0, 10.0, num_cycles=n, post_processor=_math.floor)
    print("Base Case")
    distribution_timer(_random.expovariate, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(expovariate, 1.0, num_cycles=n, post_processor=floor_mod_10)
    print("Base Case")
    distribution_timer(_random.gammavariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(gammavariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    print("Base Case")
    distribution_timer(_random.weibullvariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(weibullvariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(extreme_value, 0.0, 1.0, num_cycles=n, post_processor=round)
    print("Base Case")
    distribution_timer(_random.gauss, 5.0, 2.0, num_cycles=n, post_processor=round)
    distribution_timer(normalvariate, 5.0, 2.0, num_cycles=n, post_processor=round)
    print("Base Case")
    distribution_timer(_random.lognormvariate, 1.6, 0.25, num_cycles=n, post_processor=round)
    distribution_timer(lognormvariate, 1.6, 0.25, num_cycles=n, post_processor=round)
    distribution_timer(chi_squared, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(cauchy, 0.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(fisher_f, 8.0, 8.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(student_t, 8.0, num_cycles=n, post_processor=round)
    end = _time.time()
    duration = round(end - start, 4)
    print()
    print('=' * 73)
    print(f"Total Test Time: {duration} seconds")
