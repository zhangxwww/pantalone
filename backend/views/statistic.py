from fastapi import APIRouter
from loguru import logger
from scipy.stats import chi2, t, norm

from libs.utils import timeit, log_request, log_response


router = APIRouter(prefix='/statistics', tags=['statistic'])


@router.get('/chi2/interval')
@log_request
@log_response
@timeit
async def get_chi2_interval(p: float, df: int):
    # https://blog.csdn.net/u012958850/article/details/116565996
    lower, upper = chi2.interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@router.get('/t/interval')
@log_request
@log_response
@timeit
async def get_t_interval(p: float, df: int):
    lower, upper = t.interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@router.get('/normal/interval')
@log_request
@log_response
@timeit
async def get_normal_interval(p: float):
    lower, upper = norm.interval(p)
    return {
        'lower': lower,
        'upper': upper
    }