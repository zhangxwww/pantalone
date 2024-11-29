import math

from .prob import standard_normal_prob


def geometric_random_walk_prob(dt, mu, sigma, y):
    """
    X ~ N((mu - 1/2 sigma^2) * dt, sigma^2 dt)
    return: P(X >= y)
    """
    return standard_normal_prob((y - (mu - 0.5 * sigma ** 2) * dt) / (sigma * (dt ** 0.5)))

def exp_geometric_random_walk(mu, dt):
    return math.exp(mu * dt)

def std_geometric_random_walk(sigma, dt):
    return sigma * (dt ** 0.5)

def mean_geometric_random_walk(mu, sigma, dt):
    return mu * dt - sigma ** 2 * dt / 2
