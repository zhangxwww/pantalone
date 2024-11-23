from scipy.stats import norm

def standard_normal_prob(z):
    """
    P(Z > z) where Z ~ N(0, 1).
    """
    return norm.sf(z)
