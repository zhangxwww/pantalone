from fastapi import APIRouter

from libs.math.interval import chi2_interval, t_interval, normal_interval
from libs.decorators.timeit import timeit
from libs.decorators.log import log_request, log_response


router = APIRouter(prefix='/statistics', tags=['statistic'])


@router.get('/chi2/interval')
@log_request
@log_response
@timeit
async def get_chi2_interval(p: float, df: int):
    lower, upper = chi2_interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@router.get('/t/interval')
@log_request
@log_response
@timeit
async def get_t_interval(p: float, df: int):
    lower, upper = t_interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@router.get('/normal/interval')
@log_request
@log_response
@timeit
async def get_normal_interval(p: float):
    lower, upper = normal_interval(p)
    return {
        'lower': lower,
        'upper': upper
    }
