from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import Stock as modelStock
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Stock(BaseModel):
    idBoutiqueEntrepot: int
    idProduit: int
    quantite: int


    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelStock).all()
        return from_list_model_to_list_schema(list_model, Stock)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelStock)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelStock, list_schemas)
