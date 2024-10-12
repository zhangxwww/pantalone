import os

from fastapi import FastAPI, staticfiles
from fastapi.responses import FileResponse
from loguru import logger

from sql_app import models
from sql_app.database import engine
from utils import get_log_file_path

from views.statistic import router as statistic_router
from views.local_data import router as local_data_router
from views.network_data import router as network_data_router
from views.file import router as file_router


logger.add(
    os.path.join(get_log_file_path(), '{time}.log'),
    level='DEBUG',
    rotation='1 day',
    retention='1 week',
    compression='zip')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(statistic_router, prefix='/api')
app.include_router(local_data_router, prefix='/api')
app.include_router(network_data_router, prefix='/api')
app.include_router(file_router, prefix='/api')


@app.get('/position')
async def position():
    logger.debug('frontend')
    return FileResponse('../frontend/dist/index.html')

@app.get('/market')
async def market():
    logger.debug('frontend')
    return FileResponse('../frontend/dist/index.html')

app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)