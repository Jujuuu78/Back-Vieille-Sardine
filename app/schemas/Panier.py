from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import Panier as modelPanier
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Panier(BaseModel):
    idClient: int
    idProduit: int
    quantite: int

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelPanier).all()
        return from_list_model_to_list_schema(list_model, Panier)

    @staticmethod
    def create_panier(panier, db: Session):
        crud.add_list_schemas(db, modelPanier, [panier])

    @staticmethod
    def get_panier_by_client(id_client, db: Session):
        return db.query(modelPanier).filter_by(idClient=id_client).all()

    @staticmethod
    def update_panier_quantite(panier, db: Session):
        try:
            client = panier.idClient
            produit = panier.idProduit
            quantite = panier.quantite
            panier_a_mettre_a_jour = db.query(modelPanier).filter_by(idClient=client, idProduit=produit).first()
            if panier_a_mettre_a_jour:
                panier_a_mettre_a_jour.quantite = quantite
                db.commit()
                return {"message": "Quantité du produit mise à jour avec succès"}
            else:
                raise HTTPException(status_code=404, detail="Produit non trouvé dans le panier du client")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_produit_panier(id_client, id_produit, db: Session):
        try:
            panier_a_supprimer = db.query(modelPanier).filter_by(idClient=id_client, idProduit=id_produit).first()
            if panier_a_supprimer:
                db.delete(panier_a_supprimer)
                db.commit()
                return {"message": "Produit supprimé du panier avec succès"}
            else:
                raise HTTPException(status_code=404, detail="Produit non trouvé dans le panier du client")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_panier(id_client, db: Session):
        try:
            paniers = db.query(modelPanier).filter_by(idClient=id_client).all()
            if paniers:
                for panier in paniers:
                    db.delete(panier)
                db.commit()
                return {"message": "Tous les produits du panier ont été supprimés avec succès"}
            else:
                raise HTTPException(status_code=404, detail="Aucun panier trouvé pour le client spécifié")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelPanier)

    @staticmethod
    def add_all(list_schemas, db: Session):
        crud.add_list_schemas(db, modelPanier, list_schemas)
