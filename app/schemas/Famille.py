from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import Famille as modelFamille
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Famille(BaseModel):
    idFamille: Optional[int] = None
    nom: str

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelFamille).all()
        return from_list_model_to_list_schema(list_model, Famille)

    @staticmethod
    def get_famille_by_id(id_famille, db: Session):
        return db.query(modelFamille).filter_by(idFamille=id_famille).first()

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelFamille)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelFamille, list_schemas)
