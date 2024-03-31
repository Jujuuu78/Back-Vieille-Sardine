from app.schemas.Assortiment import Assortiment
from app.schemas.BoutiqueEntrepot import BoutiqueEntrepot
from app.schemas.Client import Client
from app.schemas.Famille import Famille
from app.schemas.Gamme import Gamme
from app.schemas.Marque import Marque
from app.schemas.Produit import Produit
from app.schemas.Commande import Commande
from app.schemas.CommandeProduit import CommandeProduit
from app.schemas.ValeursNutritionnelles import ValeursNutritionnelles
from app.schemas.Stock import Stock
from app.schemas.Remise import Remise
from app.schemas.Panier import Panier


dico_str_type = {
    "client": Client,
    "famille": Famille,
    "gamme": Gamme,
    "marque": Marque,
    "produit": Produit,
    "assortiment": Assortiment,
    "boutiqueEntrepot": BoutiqueEntrepot,
    "commande": Commande,
    "commandeProduit": CommandeProduit,
    "valeursNutritionnelles": ValeursNutritionnelles,
    "stock": Stock,
    "remise": Remise,
    "panier": Panier
}
