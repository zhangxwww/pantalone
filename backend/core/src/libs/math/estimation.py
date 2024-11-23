import numpy as np


def estimate_normal_distribution(data: np.ndarray):
    """
    Estimate the parameters of a normal distribution.
    :param data: The data to estimate the normal distribution.
    :return: The mean and standard deviation of the normal distribution.
    """
    return np.mean(data), np.std(data, ddof=1)
