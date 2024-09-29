from fastapi import APIRouter
from loguru import logger
from scipy.stats import chi2, t, norm

from utils import timeit


router = APIRouter(prefix='/statistics', tags=['statistic'])


@router.get('/chi2/interval')
@timeit
async def get_chi2_interval(p: float, df: int):
    logger.debug(f'chi2 p: {p}, df: {df}')
    # https://blog.csdn.net/u012958850/article/details/116565996
    lower, upper = chi2.interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@router.get('/t/interval')
@timeit
async def get_t_interval(p: float, df: int):
    logger.debug(f't: p: {p}, df: {df}')
    lower, upper = t.interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@router.get('/normal/interval')
@timeit
async def get_normal_interval(p: float):
    logger.debug(f'normal: p: {p}')
    lower, upper = norm.interval(p)
    return {
        'lower': lower,
        'upper': upper
    }