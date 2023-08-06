#pragma once
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace Pyewacket {
    using Integer = long long;
    using Float = double;
    
    struct Cyclone {
        using MT64_SCRAM = std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256>;
        std::random_device hardware_seed;
        MT64_SCRAM hurricane { hardware_seed() };
        template <typename D>
        auto operator()(D distribution) {
            return distribution(hurricane);
        }
        auto seed(unsigned long long seed) -> void {
            MT64_SCRAM seeded_storm { seed == 0 ? hardware_seed() : seed };
            hurricane = seeded_storm;
        }
    } cyclone;

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(cyclone.hurricane);
    }
    
    auto random_float(Float left_limit, Float right_limit) -> Float {
        auto distribution = std::uniform_real_distribution<Float> { left_limit, right_limit };
        return cyclone(distribution);
    }

    auto random_int(Integer left_limit, Integer right_limit) -> Integer {
        auto distribution = std::uniform_int_distribution<Integer> {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return cyclone(distribution);
    }

    auto random_below(Integer number) -> Integer {
        return random_int(0, std::nextafter(number, 0));
    }

    auto random_range(Integer start, Integer stop, Integer step) -> Integer {
        if (start == stop or step == 0) return start;
        const auto width { std::abs(start - stop) - 1 };
        const auto pivot { step > 0 ? std::min(start, stop) : std::max(start, stop) };
        const auto step_size { std::abs(step) };
        return pivot + step_size * random_below((width + step_size) / step);
    }

    auto bernoulli(Float truth_factor) -> bool {
        auto distribution = std::bernoulli_distribution {
            std::clamp(truth_factor, 0.0, 1.0)
        };
        return cyclone(distribution);
    }

    auto binomial(Integer number_of_trials, Float probability) -> Integer {
        auto distribution = std::binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return cyclone(distribution);
    }

    auto negative_binomial(Integer number_of_trials, Float probability) -> Integer {
        auto distribution = std::negative_binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return cyclone(distribution);
    }

    auto geometric(Float probability) -> Integer {
        auto distribution = std::geometric_distribution<Integer> { std::clamp(probability, 0.0, 1.0) };
        return cyclone(distribution);
    }

    auto poisson(Float mean) -> Integer {
        auto distribution = std::poisson_distribution<Integer> { mean };
        return cyclone(distribution);
    }

    auto expovariate(Float lambda_rate) -> Float {
        auto distribution = std::exponential_distribution<Float> { lambda_rate };
        return cyclone(distribution);
    }

    auto gammavariate(Float shape, Float scale) -> Float {
        auto distribution = std::gamma_distribution<Float> { shape, scale };
        return cyclone(distribution);
    }

    auto weibullvariate(Float shape, Float scale) -> Float {
        auto distribution = std::weibull_distribution<Float> { shape, scale };
        return cyclone(distribution);
    }

    auto normalvariate(Float mean, Float std_dev) -> Float {
        auto distribution = std::normal_distribution<Float> { mean, std_dev };
        return cyclone(distribution);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) -> Float {
        auto distribution = std::lognormal_distribution<Float> { log_mean, log_deviation };
        return cyclone(distribution);
    }

    auto extreme_value(Float location, Float scale) -> Float {
        auto distribution = std::extreme_value_distribution<Float> { location, scale };
        return cyclone(distribution);
    }

    auto chi_squared(Float degrees_of_freedom) -> Float {
        auto distribution = std::chi_squared_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return cyclone(distribution);
    }

    auto cauchy(Float location, Float scale) -> Float {
        auto distribution = std::cauchy_distribution<Float> { location, scale };
        return cyclone(distribution);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        auto distribution = std::fisher_f_distribution<Float> {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return cyclone(distribution);
    }

    auto student_t(Float degrees_of_freedom) -> Float {
        auto distribution = std::student_t_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return cyclone(distribution);
    }

    auto betavariate(Float alpha, Float beta) -> Float {
        const auto y = Float { gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + gammavariate(beta, 1.0));
    }
    
    auto paretovariate(Float alpha) -> Float {
        const auto u = Float { 1.0 - generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }
    
    auto vonmisesvariate(Float mu, Float kappa) -> Float {
        static const auto PI = Float { 4 * std::atan(1) };
        static const auto TAU = Float { 2 * PI };
        if (kappa <= 0.000001) return TAU * generate_canonical();
            const auto s = Float { 0.5 / kappa };
            const auto r = Float { s + std::sqrt(1 + s * s) };
            auto u1 = Float {0};
            auto z = Float {0};
            auto d = Float {0};
            auto u2 = Float {0};
            while (true) {
                u1 = generate_canonical();
                z = std::cos(PI * u1);
                d = z / (r + z);
                u2 = generate_canonical();
                if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
            }
        const auto q = Float { 1.0 / r };
        const auto f = Float { (q + z) / (1.0 + q * z) };
        const auto u3 = Float { generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        return std::fmod(mu - std::acos(f), TAU);
    }
    
    auto triangular(Float low, Float high, Float mode) -> Float {
        if (high - low == 0) return low;
        auto u = Float { generate_canonical() };
        auto c = Float { (mode - low) / (high - low) };
        if (u > c) {
            u = 1.0 - u;
            c = 1.0 - c;
            const auto temp = low;
            low = high;
            high = temp;
        }
        return low + (high - low) * std::sqrt(u * c);
    }
    
} // end Pyewacket namespace
