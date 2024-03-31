from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import Gamme as modelGamme
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Gamme(BaseModel):
    idGamme: Optional[int] = None
    nom: str

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelGamme).all()
        return from_list_model_to_list_schema(list_model, Gamme)

    @staticmethod
    def get_gamme_by_id(id_gamme, db: Session):
        return db.query(modelGamme).filter_by(idGamme=id_gamme).first()

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelGamme)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelGamme, list_schemas)
