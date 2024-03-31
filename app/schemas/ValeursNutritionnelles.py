from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import ValeursNutritionnelles as modelValeursNutritionnelles
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class ValeursNutritionnelles(BaseModel):
    idProduit: int
    energie: int
    matieresGrasses: float
    dontAcidesGrasSatures: float
    glucide: float
    dontSucres: float
    proteines: float
    sel: float


    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelValeursNutritionnelles).all()
        return from_list_model_to_list_schema(list_model, ValeursNutritionnelles)

    @staticmethod
    def get_valeurs_nutritionnelles_by_id_produit(id_produit, db: Session):
        return db.query(modelValeursNutritionnelles).filter_by(idProduit=id_produit).first()

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelValeursNutritionnelles)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelValeursNutritionnelles, list_schemas)
