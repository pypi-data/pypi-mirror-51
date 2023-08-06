#!python3
#distutils: language = c++
import itertools as _itertools


__all__ = (
    "seed",
    "random", "uniform",
    "randbelow", "randint", "randrange",
    "gauss", "normalvariate", "lognormvariate",
    "expovariate", "vonmisesvariate", "gammavariate", "triangular",
    "betavariate", "paretovariate", "weibullvariate",
    "shuffle", "choice", "sample", "choices",
)


cdef extern from "Pyewacket.hpp":
    void      _seed                "Pyewacket::cyclone.seed"(unsigned long long)
    double    _random              "Pyewacket::generate_canonical"()
    long long _randbelow           "Pyewacket::random_below"(long long)
    long long _randint             "Pyewacket::random_int"(long long, long long)
    long long _randrange           "Pyewacket::random_range"(long long, long long, long long)
    double    _uniform             "Pyewacket::random_float"(double, double)
    double    _expovariate         "Pyewacket::expovariate"(double)
    double    _gammavariate        "Pyewacket::gammavariate"(double, double)
    double    _weibullvariate      "Pyewacket::weibullvariate"(double, double)
    double    _normalvariate       "Pyewacket::normalvariate"(double, double)
    double    _lognormvariate      "Pyewacket::lognormvariate"(double, double)
    double    _betavariate         "Pyewacket::betavariate"(double, double)
    double    _paretovariate       "Pyewacket::paretovariate"(double)
    double    _vonmisesvariate     "Pyewacket::vonmisesvariate"(double, double)
    double    _triangular          "Pyewacket::triangular"(double, double, double)


# SEEDING #
def seed(seed=0) -> None:
    _seed(seed)


# RANDOM VALUE #
def choice(seq):
    if len(seq) == 0:
        return None
    return seq[_randbelow(len(seq))]

def shuffle(array):
    for i in reversed(range(len(array) - 1)):
        j = _randrange(i, len(array), 1)
        array[i], array[j] = array[j], array[i]

def choices(population, weights=None, *, cum_weights=None, k=1):
    def cwc(pop, weights):
        max_weight = weights[-1]
        rand = _randbelow(max_weight)
        for weight, value in zip(weights, pop):
            if weight > rand:
                return value

    if not weights and not cum_weights:
        return [choice(population) for _ in range(k)]
    if not cum_weights:
        cum_weights = list(_itertools.accumulate(weights))
    assert len(cum_weights) == len(population), "The number of weights does not match the population"
    return [cwc(population, cum_weights) for _ in range(k)]

def sample(population, k):
    n = len(population)
    assert 0 < k <= n, "Sample size k is larger than population or is negative"
    if k == 1:
        return [choice(population)]
    elif k == n or k >= n // 2:
        result = list(population)
        shuffle(result)
        return result[:k]
    else:
        result = [None] * k
        selected = set()
        selected_add = selected.add
        for i in range(k):
            j = _randbelow(n)
            while j in selected:
                j = _randbelow(n)
            selected_add(j)
            result[i] = population[j]
        return result


# RANDOM INTEGER #
def randbelow(a) -> int:
    return _randbelow(a)

def randint(a, b) -> int:
    return _randint(a, b)

def randrange(start, stop=0, step=1) -> int:
    return _randrange(start, stop, step)


# RANDOM FLOATING POINT #
def random() -> float:
    return _random()

def uniform(a, b) -> float:
    return _uniform(a, b)

def expovariate(lambd) -> float:
    return _expovariate(lambd)

def gammavariate(alpha, beta) -> float:
    return _gammavariate(alpha, beta)

def weibullvariate(alpha, beta) -> float:
    return _weibullvariate(alpha, beta)

def betavariate(alpha, beta) -> float:
    return _betavariate(alpha, beta)

def paretovariate(alpha) -> float:
    return _paretovariate(alpha)

def gauss(mu, sigma) -> float:
    return _normalvariate(mu, sigma)

def normalvariate(mu, sigma) -> float:
    return _normalvariate(mu, sigma)

def lognormvariate(mu, sigma) -> float:
    return _lognormvariate(mu, sigma)

def vonmisesvariate(mu, kappa) -> float:
    return _vonmisesvariate(mu, kappa)

def triangular(low=0.0, high=1.0, mode=0.5) -> float:
    return _triangular(low, high, mode)
