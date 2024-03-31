from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.schemas.Panier import Panier
from app.utils.globalVariables import Produit, ValeursNutritionnelles, Famille, Gamme, Marque, Assortiment, Client, \
    BoutiqueEntrepot
from app.utils.globalVariables import dico_str_type

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/get_static_table/{str_schema:str}")
async def get_static_table(str_schema: str, db: db_dependency):
    if str_schema not in dico_str_type.keys():
        raise ValueError("type non connu")
    try:
        list_schemas = dico_str_type[str_schema].get(db)
        return list_schemas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_boutique_by_id/{id_boutique:int}")
async def get_boutique_by_id(id_boutique: int, db: db_dependency):
    try:
        list_schemas = BoutiqueEntrepot.get_boutique_by_id_boutique(id_boutique, db)
        return list_schemas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_client_boutique_favorite/{id_client:int}/{id_boutique:int}")
async def update_client_boutique_favorite(id_client: int, id_boutique: int, db: db_dependency):
    try:
        Client.update_boutique_favorite(id_client, id_boutique, db)
        return {"message": "Boutique favorite update successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_produits_famille/{id_famille:int}")
async def get_produits_famille(id_famille: int, db: db_dependency):
    try:
        list_schemas = Produit.get_produits_of_a_famille(id_famille, db)
        return list_schemas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_produits_details/{id_produit:int}")
async def get_produits_details(id_produit: int, db: db_dependency):
    try:
        produit = Produit.get_produit_by_id(id_produit, db)
        if produit is None:
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        famille = Famille.get_famille_by_id(produit.idFamille, db)
        gamme = Gamme.get_gamme_by_id(produit.idGamme, db)
        marque = Marque.get_marque_by_id(produit.idMarque, db)

        if produit.assortiment:
            produitsDetails = [
                {
                    'idProduit': produit.idProduit,
                    'assortiment': produit.assortiment,
                    'nomProduit': produit.nomProduit,
                    'prix': produit.prix,
                    'detail': produit.detail,
                    'destination': produit.destination,
                    'image': produit.image,
                    'famille': famille.nom,
                    'gamme': gamme.nom,
                    'marque': marque.nom,
                }
            ]

            produitsContenus = Assortiment.get_produits_of_a_assortiment(id_produit, db)
            for prod in produitsContenus:
                produit = Produit.get_produit_by_id(prod.idProduit, db)
                valeursNutritionnelles = ValeursNutritionnelles.get_valeurs_nutritionnelles_by_id_produit(
                    prod.idProduit, db)
                produitContenuDetails = {
                    'idProduit': produit.idProduit,
                    'nomProduit': produit.nomProduit,
                    'prix': produit.prix,
                    'detail': produit.detail,
                    'destination': produit.destination,
                    'image': produit.image,
                    'energie': valeursNutritionnelles.energie,
                    'matieresGrasses': valeursNutritionnelles.matieresGrasses,
                    'dontAcidesGrasSatures': valeursNutritionnelles.dontAcidesGrasSatures,
                    'glucide': valeursNutritionnelles.glucide,
                    'dontSucres': valeursNutritionnelles.dontSucres,
                    'proteines': valeursNutritionnelles.proteines,
                    'sel': valeursNutritionnelles.sel
                }
                produitsDetails.append(produitContenuDetails)

            return produitsDetails
        else:
            valeursNutritionnelles = ValeursNutritionnelles.get_valeurs_nutritionnelles_by_id_produit(id_produit, db)

            produitsDetails = {
                'idProduit': produit.idProduit,
                'assortiment': produit.assortiment,
                'nomProduit': produit.nomProduit,
                'prix': produit.prix,
                'detail': produit.detail,
                'destination': produit.destination,
                'image': produit.image,
                'famille': famille.nom,
                'gamme': gamme.nom,
                'marque': marque.nom,
                'energie': valeursNutritionnelles.energie,
                'matieresGrasses': valeursNutritionnelles.matieresGrasses,
                'dontAcidesGrasSatures': valeursNutritionnelles.dontAcidesGrasSatures,
                'glucide': valeursNutritionnelles.glucide,
                'dontSucres': valeursNutritionnelles.dontSucres,
                'proteines': valeursNutritionnelles.proteines,
                'sel': valeursNutritionnelles.sel
            }
            return produitsDetails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_produits_by_search/{search_term:str}")
async def get_produits_search(search_term: str, db: db_dependency):
    try:
        list_schemas = Produit.get_produits_by_search(search_term, db)
        return list_schemas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_panier_by_client/{id_client:int}")
async def get_panier_client(id_client: int, db: db_dependency):
    try:
        resultat = []
        list_schemas = Panier.get_panier_by_client(id_client, db)
        for schema in list_schemas:
            produit = Produit.get_produit_by_id(schema.idProduit, db)
            contenu = {
                'idClient': schema.idClient,
                'idProduit': produit.idProduit,
                'nomProduit': produit.nomProduit,
                'prix': produit.prix,
                'image': produit.image,
                'quantite': schema.quantite
            }
            resultat.append(contenu)
        return resultat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_panier")
async def upload_panier(db: db_dependency, panier: Panier):
    try:
        Panier.create_panier(panier, db)
        return {"message": "Panier upload successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_panier")
async def update_panier(db: db_dependency, panier: Panier):
    try:
        Panier.update_panier_quantite(panier, db)
        return {"message": "Panier update successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_produit_panier/{id_client:int}/{id_produit:int}")
async def delete_produit_panier(id_client: int, id_produit: int, db: db_dependency):
    try:
        Panier.delete_produit_panier(id_client, id_produit, db)
        return {"message": "Product delete successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_panier/{id_client:int}")
async def delete_panier(db: db_dependency, id_client: int):
    try:
        Panier.delete_panier(id_client, db)
        return {"message": "Panier delete successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
