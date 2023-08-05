#pragma once
#include <algorithm>        // clamp, generate_n, partial_sort, min, max
#include <cmath>            // abs, cos, acos, atan, sqrt, fmod, exp, nextafter
#include <functional>       // greater
#include <limits>           // numeric_limits
#include <numeric>          // reduce
#include <random>           // generate_canonical, uniform_real_distribution, uniform_int_distribution ...
#include <vector>           // vector


namespace Storm {  // Version 3.1.1
    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 4, 3>, 128> Hurricane
    { std::random_device()() };

    using Integer = long long;
    using Float = double;

    auto min_int() -> Integer { return -std::numeric_limits<Integer>::max(); }
    auto max_int() -> Integer { return std::numeric_limits<Integer>::max(); }
    auto min_float() -> Float { return std::numeric_limits<Float>::lowest(); }
    auto max_float() -> Float { return std::numeric_limits<Float>::max(); }
    auto min_below() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    auto min_above() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }

    auto smart_clamp(Integer a, Integer b, Integer c) -> Integer {
        return std::clamp(a, std::min(b, c), std::max(c, b));
    }

    template <typename Functor>
    auto analytic_continuation(Functor && func, Integer input, Integer offset) -> Integer {
        if (input < 0) return -func(-std::max(input, Storm::min_int())) + offset;
        if (input > 0) return func(input);
        return offset;
    }

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(Storm::Hurricane);
    }

    auto random_float(Float a, Float b) -> Float {
        std::uniform_real_distribution<Float> distribution { a, b };
        return distribution(Storm::Hurricane);
    }

    auto random_below(Integer number) -> Integer {
        if (number > 0) {
            std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
            return distribution(Storm::Hurricane);
        }
        return Storm::analytic_continuation(Storm::random_below, number, 0);
    }

    auto random_index(Integer number) -> Integer {
        if (number > 0) {
            std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
            return distribution(Storm::Hurricane);
        }
        return Storm::analytic_continuation(Storm::random_index, number, -1);
    }

    auto random_int(Integer left_limit, Integer right_limit) -> Integer {
        const auto low { std::min(left_limit, right_limit) };
        const auto high { std::max(right_limit, left_limit) };
        std::uniform_int_distribution<Integer> distribution { low, high };
        return distribution(Storm::Hurricane);
    }

    auto random_range(Integer start, Integer stop, Integer step) -> Integer {
        if (start == stop or step == 0) return start;
        const auto width { std::abs(start - stop) - 1 };
        const auto pivot { step > 0 ? std::min(start, stop) : std::max(start, stop) };
        const auto step_size { std::abs(step) };
        return pivot + step_size * Storm::random_below((width + step_size) / step);
    }

    /// RNG
    auto bernoulli(const double & truth_factor) -> bool {
        std::bernoulli_distribution distribution {
            std::clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(Storm::Hurricane);
    }

    auto binomial(Integer number_of_trials, const double & probability) -> Integer {
        std::binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0),
        };
        return distribution(Storm::Hurricane);
    }

    auto negative_binomial(Integer number_of_trials, const double & probability) -> Integer {
        std::negative_binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(Storm::Hurricane);
    }

    auto geometric(const double & probability) -> Integer {
        std::geometric_distribution<Integer> distribution { std::clamp(probability, 0.0, 1.0) };
        return distribution(Storm::Hurricane);
    }

    auto poisson(const double & mean) -> Integer {
        std::poisson_distribution<Integer> distribution { mean };
        return distribution(Storm::Hurricane);
    }

    auto expovariate(Float lambda_rate) -> Float {
        std::exponential_distribution<Float> distribution { lambda_rate };
        return distribution(Storm::Hurricane);
    }

    auto gammavariate(Float shape, Float scale) -> Float {
        std::gamma_distribution<Float> distribution { shape, scale };
        return distribution(Storm::Hurricane);
    }

    auto weibullvariate(Float shape, Float scale) -> Float {
        std::weibull_distribution<Float> distribution { shape, scale };
        return distribution(Storm::Hurricane);
    }

    auto normalvariate(Float mean, Float std_dev) -> Float {
        std::normal_distribution<Float> distribution { mean, std_dev };
        return distribution(Storm::Hurricane);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) -> Float {
        std::lognormal_distribution<Float> distribution { log_mean, log_deviation };
        return distribution(Storm::Hurricane);
    }

    auto extreme_value(Float location, Float scale) -> Float {
        std::extreme_value_distribution<Float> distribution { location, scale };
        return distribution(Storm::Hurricane);
    }

    auto chi_squared(Float degrees_of_freedom) -> Float {
        std::chi_squared_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(Storm::Hurricane);
    }

    auto cauchy(Float location, Float scale) -> Float {
        std::cauchy_distribution<Float> distribution { location, scale };
        return distribution(Storm::Hurricane);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        std::fisher_f_distribution<Float> distribution {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return distribution(Storm::Hurricane);
    }

    auto student_t(Float degrees_of_freedom) -> Float {
        std::student_t_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(Storm::Hurricane);
    }

    /// Pyewacket
    auto betavariate(Float alpha, Float beta) -> Float {
        const auto y { Storm::gammavariate(alpha, 1.0) };
        if (y == 0.0) return 0.0;
        return y / (y + Storm::gammavariate(beta, 1.0));
    }

    auto paretovariate(Float alpha) -> Float {
        const auto u { 1.0 - Storm::generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    auto vonmisesvariate(Float mu, Float kappa) -> Float {
        static const Float PI { 4 * std::atan(1) };
        static const Float TAU { 8 * std::atan(1) };
        if (kappa <= 0.000001) return TAU * Storm::generate_canonical();
        const Float s { 0.5 / kappa };
        const Float r { s + std::sqrt(1 + s * s) };
        Float u1 {0};
        Float z {0};
        Float d {0};
        Float u2 {0};
        while (true) {
            u1 = Storm::generate_canonical();
            z = std::cos(PI * u1);
            d = z / (r + z);
            u2 = Storm::generate_canonical();
            if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
        }
        const Float q { 1.0 / r };
        const Float f { (q + z) / (1.0 + q * z) };
        const Float u3 { Storm::generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        return std::fmod(mu - std::acos(f), TAU);
    }

    auto triangular(Float low, Float high, Float mode) -> Float {
        if (low == high) return low;
        const Float rand { Storm::generate_canonical() };
        const Float mode_factor { (mode - low) / (high - low) };
        if (rand > mode_factor) return high + (low - high) * std::sqrt((1.0 - rand) * (1.0 - mode_factor));
        return low + (high - low) * std::sqrt(rand * mode_factor);
    }

    /// Fortuna
    auto percent_true(Float truth_factor) -> bool {
        return Storm::random_float(0.0, 100.0) < truth_factor;
    }

    auto d(Integer sides) -> Integer {
        if (sides > 0) {
            std::uniform_int_distribution<Integer> distribution {1, sides};
            return distribution(Storm::Hurricane);
        }
        return Storm::analytic_continuation(Storm::d, sides, 0);
    }

    auto dice(Integer rolls, Integer sides) -> Integer {
        if (rolls > 0) {
            auto total {0};
            for (auto i {0}; i < rolls; ++i) total += d(sides);
            return total;
        }
        return -Storm::dice(-rolls, sides);
    }

     auto ability_dice(Integer number) -> Integer {
        const Integer num { std::clamp(number, Integer(3), Integer(9)) };
        if (num == 3) return Storm::dice(3, 6);
        std::vector<Integer> the_rolls(num);
        std::generate_n(the_rolls.begin(), num, []() { return Storm::d(6); });
        std::partial_sort(the_rolls.begin(), the_rolls.begin() + 3, the_rolls.end(), std::greater<>());
        return std::reduce(the_rolls.cbegin(), the_rolls.cbegin() + 3);
    }

    auto plus_or_minus(Integer number) -> Integer {
        return Storm::random_int(-number, number);
    }

    auto plus_or_minus_linear(Integer number) -> Integer {
        const auto num { std::abs(number) };
        return Storm::dice(Integer(2), num + 1) - (num + 2);
    }

    auto plus_or_minus_gauss(Integer number) -> Integer {
        static const auto PI { 4 * std::atan(1) };
        const auto num { std::abs(number) };
        const auto result { Integer(std::round(Storm::normalvariate(0.0, num / PI))) };
        if (result >= -num and result <= num) return result;
        return Storm::plus_or_minus_linear(num);
    }

    auto fuzzy_clamp(Integer target, Integer upper_bound) -> Integer {
        if (target >= 0 and target < upper_bound) return target;
        return Storm::random_index(upper_bound);
    }

    /// ZeroCool Functors
    auto back_linear(Integer) -> Integer;
    auto front_linear(Integer number) -> Integer {
        if (number > 0) {
            return Storm::triangular(0, number, 0);
        }
        return Storm::analytic_continuation(Storm::back_linear, number, -1);
    }

    auto back_linear(Integer number) -> Integer {
        if (number > 0) {
            return Storm::triangular(0, number, number);
        }
        return Storm::analytic_continuation(Storm::front_linear, number, -1);
    }

    auto middle_linear(Integer number) -> Integer {
        if (number > 0) {
            return Storm::triangular(0, number, number / 2.0);
        }
        return Storm::analytic_continuation(Storm::middle_linear, number, -1);
    }

    auto quantum_linear(Integer number) -> Integer {
        const auto rand_num { Storm::d(3) };
        if (rand_num == 1) return Storm::front_linear(number);
        if (rand_num == 2) return Storm::middle_linear(number);
        return Storm::back_linear(number);
    }

    auto back_gauss(Integer) -> Integer;
    auto front_gauss(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Integer(std::floor(Storm::gammavariate(1.0, number / 10.0))) };
            return Storm::fuzzy_clamp(result, number);
        }
        return Storm::analytic_continuation(Storm::back_gauss, number, -1);
    }

    auto middle_gauss(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Integer(std::floor(Storm::normalvariate(number / 2.0, number / 10.0))) };
            return Storm::fuzzy_clamp(result, number);
        }
        return Storm::analytic_continuation(Storm::middle_gauss, number, -1);
    }

    auto back_gauss(Integer number) -> Integer {
        if (number > 0) {
            return number - Storm::front_gauss(number) - 1;
        }
        return Storm::analytic_continuation(Storm::front_gauss, number, -1);
    }

    auto quantum_gauss(Integer number) -> Integer {
        const auto rand_num { Storm::d(3) };
        if (rand_num == 1) return Storm::front_gauss(number);
        if (rand_num == 2) return Storm::middle_gauss(number);
        return Storm::back_gauss(number);
    }

    auto back_poisson(Integer) -> Integer;
    auto front_poisson(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Storm::poisson(number / 4.0) };
            return Storm::fuzzy_clamp(result, number);
        }
        return Storm::analytic_continuation(Storm::back_poisson, number, -1);
    }

    auto back_poisson(Integer number) -> Integer {
        if (number > 0) {
            const auto result { number - Storm::front_poisson(number) - 1 };
            return Storm::fuzzy_clamp(result, number);
        }
        return Storm::analytic_continuation(Storm::front_poisson, number, -1);
    }

    auto middle_poisson(Integer number) -> Integer {
        if (Storm::percent_true(50)) return Storm::front_poisson(number);
        return Storm::back_poisson(number);
    }

    auto quantum_poisson(Integer number) -> Integer {
        const auto rand_num { Storm::d(3) };
        if (rand_num == 1) return Storm::front_poisson(number);
        if (rand_num == 2) return Storm::middle_poisson(number);
        return Storm::back_poisson(number);
    }

    auto quantum_monty(Integer number) -> Integer {
        const auto rand_num { Storm::d(3) };
        if (rand_num == 1) return Storm::quantum_linear(number);
        if (rand_num == 2) return Storm::quantum_gauss(number);
        return Storm::quantum_poisson(number);
    }


} // end namespace
