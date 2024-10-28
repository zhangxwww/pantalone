from fastapi import APIRouter
import subprocess

from libs.utils.decorator import timeit, log_request


router = APIRouter(tags=['git'])


@router.get('/git/updated')
@log_request
@timeit
async def get_updated():
    fetch_res = subprocess.run(['git', 'fetch', 'origin'], capture_output=True)
    if fetch_res.returncode != 0:
        return {'updated': False}
    local_commit_res = subprocess.run(['git', 'rev-parse', 'master'], capture_output=True)
    origin_commit_res = subprocess.run(['git', 'rev-parse', 'origin/master'], capture_output=True)
    if local_commit_res.returncode != 0 or origin_commit_res.returncode != 0:
        return {'updated': False}
    local_commit = local_commit_res.stdout.decode().strip()
    origin_commit = origin_commit_res.stdout.decode().strip()
    if local_commit != origin_commit:
        return {'updated': True}
    return {'updated': False}