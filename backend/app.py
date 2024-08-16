from fastapi import FastAPI, staticfiles, Depends
from sqlalchemy.orm import Session
from loguru import logger

from data import get_china_bond_bield_data, save_base64_data, get_data_from_db
from api_model import CN1YRDateData, UploadData
from sql_app import models
from sql_app.database import SessionLocal, engine


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
    return {'yield': get_china_bond_bield_data(data.dates)}

@app.post('/api/upload')
async def upload(file: UploadData, db: Session = Depends(get_db)):
    save_base64_data(db, file.file)
    return {'success': True}

@app.get('/api/data')
async def get_data(db: Session = Depends(get_db)):
    return get_data_from_db(db)


app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)