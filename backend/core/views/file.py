from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from libs.utils.decorator import timeit
import api_model
import libs.controller as controller
from db import get_db


router = APIRouter(tags=['file'])

@router.post('/upload')
@timeit
async def upload(file: api_model.UploadData, db: Session = Depends(get_db)):
    await controller.save_base64_data(db, file.file)
    return {'success': True}
