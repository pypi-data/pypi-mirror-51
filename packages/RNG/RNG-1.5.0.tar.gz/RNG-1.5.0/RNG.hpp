#pragma once
#include <algorithm>
#include <limits>
#include <random>


namespace RNG {

    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 4, 3>, 128> Hurricane {
        std::random_device()()
    };

    using Integer = long long;
    using Float = double;

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(RNG::Hurricane);
    }

    auto uniform_real_variate(Float a, Float b) -> Float {
        std::uniform_real_distribution<Float> distribution { a, b };
        return distribution(RNG::Hurricane);
    }

    auto uniform_int_variate(Integer left_limit, Integer right_limit) -> Integer {
        std::uniform_int_distribution<Integer> distribution {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return distribution(RNG::Hurricane);
    }

    auto bernoulli_variate(Float truth_factor) -> bool {
        std::bernoulli_distribution distribution {
            std::clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(RNG::Hurricane);
    }

    auto binomial_variate(Integer number_of_trials, Float probability) -> Integer {
        std::binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(RNG::Hurricane);
    }

    auto negative_binomial_variate(Integer number_of_trials, Float probability) -> Integer {
        std::negative_binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(RNG::Hurricane);
    }

    auto geometric_variate(Float probability) -> Integer {
        std::geometric_distribution<Integer> distribution { std::clamp(probability, 0.0, 1.0) };
        return distribution(RNG::Hurricane);
    }

    auto poisson_variate(Float mean) -> Integer {
        std::poisson_distribution<Integer> distribution { mean };
        return distribution(RNG::Hurricane);
    }

    auto exponential_variate(Float lambda_rate) -> Float {
        std::exponential_distribution<Float> distribution { lambda_rate };
        return distribution(RNG::Hurricane);
    }

    auto gamma_variate(Float shape, Float scale) -> Float {
        std::gamma_distribution<Float> distribution { shape, scale };
        return distribution(RNG::Hurricane);
    }

    auto weibull_variate(Float shape, Float scale) -> Float {
        std::weibull_distribution<Float> distribution { shape, scale };
        return distribution(RNG::Hurricane);
    }

    auto normal_variate(Float mean, Float std_dev) -> Float {
        std::normal_distribution<Float> distribution { mean, std_dev };
        return distribution(RNG::Hurricane);
    }

    auto lognormal_variate(Float log_mean, Float log_deviation) -> Float {
        std::lognormal_distribution<Float> distribution { log_mean, log_deviation };
        return distribution(RNG::Hurricane);
    }

    auto extreme_value_variate(Float location, Float scale) -> Float {
        std::extreme_value_distribution<Float> distribution { location, scale };
        return distribution(RNG::Hurricane);
    }

    auto chi_squared_variate(Float degrees_of_freedom) -> Float {
        std::chi_squared_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(RNG::Hurricane);
    }

    auto cauchy_variate(Float location, Float scale) -> Float {
        std::cauchy_distribution<Float> distribution { location, scale };
        return distribution(RNG::Hurricane);
    }

    auto fisher_f_variate(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        std::fisher_f_distribution<Float> distribution {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return distribution(RNG::Hurricane);
    }

    auto student_t_variate(Float degrees_of_freedom) -> Float {
        std::student_t_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(RNG::Hurricane);
    }

} // end namespace
