from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import Remise as modelRemise
from app.database.models import EnumCategorie
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Remise(BaseModel):
    typeClient: EnumCategorie
    montantPourcentage: float
    minAchat: int


    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelRemise).all()
        return from_list_model_to_list_schema(list_model, Remise)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelRemise)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelRemise, list_schemas)
