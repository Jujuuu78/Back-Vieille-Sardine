from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import BoutiqueEntrepot as modelBoutiqueEntrepot
from app.database.models import EnumCategorieBoutique
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class BoutiqueEntrepot(BaseModel):
    idBoutique: Optional[int] = None
    categorie: EnumCategorieBoutique
    adresse: str
    numTel: str
    horaires: Optional[str] = None
    dirigeant: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelBoutiqueEntrepot).all()
        return from_list_model_to_list_schema(list_model, BoutiqueEntrepot)

    @staticmethod
    def get_boutique_by_id_boutique(id_boutique, db: Session):
        return db.query(modelBoutiqueEntrepot).filter_by(idBoutique=id_boutique).first()

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelBoutiqueEntrepot)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelBoutiqueEntrepot, list_schemas)
