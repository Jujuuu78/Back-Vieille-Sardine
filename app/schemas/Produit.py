from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import EnumDestination
from app.database.models import Famille as modelFamille
from app.database.models import Gamme as modelGamme
from app.database.models import Marque as modelMarque
from app.database.models import Produit as modelProduit
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Produit(BaseModel):
    idProduit: Optional[int] = None
    assortiment: bool
    nomProduit: str
    prix: float
    idFamille: int
    idGamme: int
    idMarque: int
    detail: str
    destination: EnumDestination
    image: str

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelProduit).all()
        return from_list_model_to_list_schema(list_model, Produit)

    @staticmethod
    def get_produits_of_a_famille(id_famille, db: Session):
        list_model = db.query(modelProduit).filter_by(idFamille=id_famille).all()
        return from_list_model_to_list_schema(list_model, Produit)

    @staticmethod
    def get_produit_by_id(id_produit, db: Session):
        return db.query(modelProduit).filter_by(idProduit=id_produit).first()

    @staticmethod
    def get_produits_by_search(search_term, db: Session):
        list_model = db.query(modelProduit). \
            join(modelGamme, modelProduit.idGamme == modelGamme.idGamme). \
            join(modelMarque, modelProduit.idMarque == modelMarque.idMarque). \
            join(modelFamille, modelProduit.idFamille == modelFamille.idFamille). \
            filter(
            or_(
                modelProduit.nomProduit.ilike(f"%{search_term}%"),
                modelProduit.destination.ilike(f"%{search_term}%"),
                modelProduit.detail.ilike(f"%{search_term}%"),
                modelFamille.nom.ilike(f"%{search_term}%"),
                modelGamme.nom.ilike(f"%{search_term}%"),
                modelMarque.nom.ilike(f"%{search_term}%")
            )
        ).all()
        return from_list_model_to_list_schema(list_model, Produit)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelProduit)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelProduit, list_schemas)
