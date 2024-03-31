from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import Assortiment as modelAssortiment
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Assortiment(BaseModel):
    idAssortiment: int
    idProduit: int

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelAssortiment).all()
        return from_list_model_to_list_schema(list_model, Assortiment)

    @staticmethod
    def get_produits_of_a_assortiment(id_produit, db: Session):
        list_model = db.query(modelAssortiment).filter_by(idAssortiment=id_produit).all()
        return from_list_model_to_list_schema(list_model, Assortiment)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelAssortiment)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelAssortiment, list_schemas)
