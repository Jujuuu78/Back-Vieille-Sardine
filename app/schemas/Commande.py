from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional
from datetime import date

from app.database.models import Commande as modelCommande
from app.database.models import EnumStatut, EnumModeCommande
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Commande(BaseModel):
    idCommande: Optional[int] = None
    idClient: int
    date: date
    remise: float
    statut: EnumStatut
    modeCommande: EnumModeCommande
    idBoutique: int


    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelCommande).all()
        return from_list_model_to_list_schema(list_model, Commande)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelCommande)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelCommande, list_schemas)
