from scipy.stats import chi2, t, norm


def chi2_interval(p: float, df: int):
    # https://blog.csdn.net/u012958850/article/details/116565996
    return chi2.interval(p, df)

def t_interval(p: float, df: int):
    return t.interval(p, df)

def normal_interval(p: float):
    return norm.interval(p)
