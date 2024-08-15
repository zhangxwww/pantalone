import sys
import json
import base64

from fastapi import FastAPI, staticfiles, Depends
from sqlalchemy.orm import Session
from loguru import logger

from data import getChinaBondYieldData
from api_model import CN1YRDateData, UploadData
from sql_app import models
from sql_app.database import SessionLocal, engine
import sql_app.crud as crud


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/api/CN1YR')
async def get_CN1YR(data: CN1YRDateData):
    logger.debug(data.dates)
    return {'yield': getChinaBondYieldData(data.dates)}

@app.post('/api/upload')
async def upload(file: UploadData, db: Session = Depends(get_db)):
    content = base64.b64decode(file.file)
    json_data = json.loads(content.decode('utf-8'))

    # logger.debug(json_data)
    logger.debug('Creating table from json data')

    crud.create_table_from_json(db, json_data)
    return {'success': True}

app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)