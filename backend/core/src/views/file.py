from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api_model
import controller.local as local_controller
from db import get_db
from libs.decorators.timeit import timeit


router = APIRouter(tags=['file'])

@router.post('/upload')
@timeit
async def upload(file: api_model.UploadData, db: Session = Depends(get_db)):
    await local_controller.save_base64_data(db, file.file)
    return {'success': True}
