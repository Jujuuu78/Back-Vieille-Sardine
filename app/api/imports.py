from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.config import get_db
from app.utils.globalVariables import dico_str_type
from app.utils.imports.importFile import upload_data_from_excel_to_static_table

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("upload_data_static_table/{str_schema:str}")
async def upload_data_static_table(str_schema: str, file: UploadFile, db: db_dependency):
    if str_schema not in dico_str_type.keys():
        raise ValueError("type non connu")
    try:
        await upload_data_from_excel_to_static_table(file, dico_str_type[str_schema], db)
        return JSONResponse("Upload data sucessfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
