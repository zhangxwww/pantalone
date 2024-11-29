import numpy as np


def estimate_normal_distribution(data: np.ndarray):
    """
    Estimate the parameters of a normal distribution.
    :param data: The data to estimate the normal distribution.
    :return: The mean and standard deviation of the normal distribution.
    """
    return np.mean(data), np.std(data, ddof=1)

def estimate_log_normal_distribution(data: np.ndarray):
    """
    Estimate the parameters of a log-normal distribution.
    :param data: The data to estimate the log-normal distribution.
    :return: The mean and standard deviation of the log-normal distribution.
    """
    log_data = np.log(data)
    r = np.mean(log_data)
    s = np.std(log_data, ddof=1)
    return r + s ** 2 / 2, s
