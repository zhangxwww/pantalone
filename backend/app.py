import os

from fastapi import FastAPI, staticfiles
from fastapi.responses import FileResponse
from loguru import logger
from sqlalchemy import text

from sql_app import models
from sql_app.database import engine
from libs.utils import get_log_file_path

from views.statistic import router as statistic_router
from views.local_data import router as local_data_router
from views.network_data import router as network_data_router
from views.file import router as file_router
from views.git_state import router as git_state_router
from views.version import router as version_router


logger.add(
    os.path.join(get_log_file_path(), '{time}.log'),
    level='DEBUG',
    rotation='1 day',
    retention='1 week',
    compression='zip')

app = FastAPI()

@app.on_event('startup')
async def startup():
    logger.debug('startup')
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        await conn.execute(text('PRAGMA journal_mode=WAL'))

@app.on_event('shutdown')
async def shutdown():
    await engine.dispose()


app.include_router(statistic_router, prefix='/api')
app.include_router(local_data_router, prefix='/api')
app.include_router(network_data_router, prefix='/api')
app.include_router(file_router, prefix='/api')
app.include_router(git_state_router, prefix='/api')
app.include_router(version_router, prefix='/api')


@app.get('/position')
async def position():
    logger.debug('frontend')
    return FileResponse('../frontend/dist/index.html')

@app.get('/market')
async def market():
    logger.debug('frontend')
    return FileResponse('../frontend/dist/index.html')

@app.get('/percentile')
async def percentile():
    logger.debug('frontend')
    return FileResponse('../frontend/dist/index.html')

app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)