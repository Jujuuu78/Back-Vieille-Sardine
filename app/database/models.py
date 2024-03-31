from enum import Enum as Enume

from sqlalchemy import Column, Integer, Enum, String, Boolean, Float, ForeignKey, Date

from app.database.config import Base


class EnumCivilite(str, Enume):
    homme = "homme"
    femme = "femme"
    autre = "autre"


class EnumCategorie(str, Enume):
    professionnel = "professionnel"
    particulier = "particulier"


class EnumDestination(str, Enume):
    repas = "repas"
    cadeau = "cadeau"
    aperitif = "aperitif"


class EnumCategorieBoutique(str, Enume):
    boutique = "boutique"
    entrepot = "entrepot"


class EnumStatut(str, Enume):
    enCoursDePreparation = "en_cours_de_preparation"
    preparee = "preparee"
    enCoursDeLivraison = "en_cours_de_livraison"
    livree = "livree"


class EnumModeCommande(str, Enume):
    telephone = "telephone"
    boutique = "boutique"
    internet = "internet"


class BoutiqueEntrepot(Base):
    __tablename__ = 'boutiqueEntrepot'

    idBoutique = Column(Integer, primary_key=True, autoincrement=True, index=True)
    categorie = Column(Enum(EnumCategorieBoutique), index=True)
    adresse = Column(String, index=True, unique=True)
    numTel = Column(String, index=True, unique=True)
    horaires = Column(String, index=True)
    dirigeant = Column(String, index=True)
    image = Column(String, index=True)


class Client(Base):
    __tablename__ = 'client'

    idClient = Column(Integer, primary_key=True, autoincrement=True, index=True)
    civilite = Column(Enum(EnumCivilite), index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    adresseMail = Column(String, index=True, unique=True)
    adresseFacturation = Column(String, index=True)
    adresseLivraison = Column(String, index=True)
    numTel = Column(String, index=True)
    mdp = Column(String, index=True)
    type = Column(Enum(EnumCategorie), index=True)
    boutiqueFavorite = Column(Integer, ForeignKey('boutiqueEntrepot.idBoutique'), index=True)


class Famille(Base):
    __tablename__ = 'famille'

    idFamille = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom = Column(String, index=True, unique=True)


class Gamme(Base):
    __tablename__ = 'gamme'

    idGamme = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom = Column(String, index=True, unique=True)


class Marque(Base):
    __tablename__ = 'marque'

    idMarque = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom = Column(String, index=True, unique=True)


class Produit(Base):
    __tablename__ = 'produit'

    idProduit = Column(Integer, primary_key=True, autoincrement=True, index=True)
    assortiment = Column(Boolean, index=True)
    nomProduit = Column(String, index=True, unique=True)
    prix = Column(Float, index=True)
    idFamille = Column(Integer, ForeignKey('famille.idFamille'), index=True)
    idGamme = Column(Integer, ForeignKey('gamme.idGamme'), index=True)
    idMarque = Column(Integer, ForeignKey('marque.idMarque'), index=True)
    detail = Column(String, index=True)
    destination = Column(Enum(EnumDestination), index=True)
    image = Column(String, index=True)


class Assortiment(Base):
    __tablename__ = 'assortiment'

    idAssortiment = Column(Integer, ForeignKey('produit.idProduit'), primary_key=True, index=True)
    idProduit = Column(Integer, ForeignKey('produit'), primary_key=True, index=True)


class Commande(Base):
    __tablename__ = 'commande'

    idCommande = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idClient = Column(Integer, ForeignKey('client'), index=True)
    date = Column(Date, index=True)
    remise = Column(Float, index=True)
    statut = Column(Enum(EnumStatut), index=True)
    modeCommande = Column(Enum(EnumModeCommande), index=True)
    idBoutique = Column(Integer, ForeignKey('boutiqueEntrepot'), index=True)


class CommandeProduit(Base):
    __tablename__ = 'commandeProduit'

    idCommande = Column(Integer, ForeignKey('commande'), primary_key=True, index=True)
    idProduit = Column(Integer, ForeignKey('produit'), primary_key=True, index=True)
    quantite = Column(Integer, index=True)
    prix = Column(Float, index=True)


class ValeursNutritionnelles(Base):
    __tablename__ = 'valeursNutritionnelles'

    idProduit = Column(Integer, ForeignKey('produit'), primary_key=True, index=True)
    energie = Column(Integer, index=True)
    matieresGrasses = Column(Float, index=True)
    dontAcidesGrasSatures = Column(Float, index=True)
    glucide = Column(Float, index=True)
    dontSucres = Column(Float, index=True)
    proteines = Column(Float, index=True)
    sel = Column(Float, index=True)


class Stock(Base):
    __tablename__ = 'stock'

    idBoutiqueEntrepot = Column(Integer, ForeignKey('boutiqueEntrepot.idBoutique'), primary_key=True, index=True)
    idProduit = Column(Integer, ForeignKey('produit'), primary_key=True, index=True)
    quantite = Column(Integer, index=True)


class Remise(Base):
    __tablename__ = 'remise'

    typeClient = Column(Enum(EnumCategorie), primary_key=True, index=True)
    montantPourcentage = Column(Float, primary_key=True, index=True)
    minAchat = Column(Integer, primary_key=True, index=True)


class Panier(Base):
    __tablename__ = 'panier'

    idClient = Column(Integer, ForeignKey('client'), primary_key=True, index=True)
    idProduit = Column(Integer, ForeignKey('produit'), primary_key=True, index=True)
    quantite = Column(Integer, index=True)
