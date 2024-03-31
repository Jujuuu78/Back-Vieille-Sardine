from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import Marque as modelMarque
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Marque(BaseModel):
    idMarque: Optional[int] = None
    nom: str

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelMarque).all()
        return from_list_model_to_list_schema(list_model, Marque)

    @staticmethod
    def get_marque_by_id(id_marque, db: Session):
        return db.query(modelMarque).filter_by(idMarque=id_marque).first()

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelMarque)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelMarque, list_schemas)
