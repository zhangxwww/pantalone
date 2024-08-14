import json
import base64

from fastapi import FastAPI, staticfiles

from data import getChinaBondYieldData
from api_model import CN1YRDateData, UploadData
import sql_app.crud as crud

app = FastAPI()

@app.post('/api/CN1YR')
async def get_CN1YR(data: CN1YRDateData):
    return {'yield': getChinaBondYieldData(data.dates)}

@app.post('/api/upload')
async def upload(file: UploadData):
    content = base64.b64decode(file.file)
    json_data = json.loads(content.decode('utf-8'))
    crud.create_table_from_json(json_data)
    return {'success': True}

app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)