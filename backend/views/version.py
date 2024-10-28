from fastapi import APIRouter

from libs.utils.decorator import timeit, log_response
from __version__ import __version__


router = APIRouter(tags=['version'])


@router.get('/version')
@log_response
@timeit
async def get_version():
    return {'version': __version__}