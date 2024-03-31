from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import CommandeProduit as modelCommandeProduit
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class CommandeProduit(BaseModel):
    idCommande: int
    idProduit: int
    quantite: int
    prix: float


    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelCommandeProduit).all()
        return from_list_model_to_list_schema(list_model, CommandeProduit)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelCommandeProduit)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelCommandeProduit, list_schemas)
