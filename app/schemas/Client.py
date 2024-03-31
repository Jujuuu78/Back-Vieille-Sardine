from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.database.models import Client as modelClient
from app.database.models import EnumCivilite, EnumCategorie
from app.schemas import crud
from app.utils.convertType import from_list_model_to_list_schema


class Client(BaseModel):
    idClient: Optional[int] = None
    civilite: EnumCivilite
    nom: str
    prenom: str
    adresseMail: str
    adresseFacturation: Optional[str] = None
    adresseLivraison: Optional[str] = None
    numTel: str
    mdp: str
    type: EnumCategorie
    boutiqueFavorite: Optional[int] = None

    class Config:
        orm_mode = True

    @staticmethod
    def get(db: Session):
        list_model = db.query(modelClient).all()
        return from_list_model_to_list_schema(list_model, Client)

    @staticmethod
    def delete_all(db: Session):
        crud.delete_all(db, modelClient)

    @staticmethod
    def create_user(client, db: Session):
        crud.add_list_schemas(db, modelClient, [client])

    @staticmethod
    def update_boutique_favorite(id_client, id_boutique, db: Session):
        try:
            client_a_mettre_a_jour = db.query(modelClient).filter_by(idClient=id_client).first()
            if client_a_mettre_a_jour:
                client_a_mettre_a_jour.boutiqueFavorite = id_boutique
                db.commit()
                return {"message": "Boutique favorite mise à jour avec succès"}
            else:
                raise HTTPException(status_code=404, detail="Boutique non trouvée dans la BDD")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_client(db: Session, adresseMail):
        user = db.query(modelClient).filter_by(adresseMail=adresseMail).first()
        if user:
            user_sch = Client(**{k: getattr(user, k) for k in Client.__annotations__})
            return user_sch

        return None
