import os
from fastapi import APIRouter

from libs.decorators.timeit import timeit
from libs.decorators.log import log_response


router = APIRouter(tags=['version'])


@router.get('/version')
@log_response
@timeit
async def get_version():
    with open(os.path.join(os.path.dirname(__file__), '../../../VERSION'), 'r') as f:
        v = f.read().strip()
    return {'version': v}
