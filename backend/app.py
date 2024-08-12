import uvicorn
from fastapi import FastAPI, staticfiles

from data import getChinaBondYieldData
from models.CN1YR import CN1YRDateData

app = FastAPI()

@app.post('/api/CN1YR')
async def get_CN1YR(data: CN1YRDateData):
    return {'yield': getChinaBondYieldData(data.dates)}

app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)