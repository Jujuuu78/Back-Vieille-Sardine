#-- MySQL #-- voir ou on met des not NULL
#-- On a pas besoin de table bon de commande car elle s'obtient en faisant des jointure entre Commande et CommandeProduit


CREATE TABLE BoutiqueEntrepot(
  idBoutique INT AUTO_INCREMENT PRIMARY KEY,
  categorie ENUM('boutique','entrepot') NOT NULL,
  adresse VARCHAR(255) UNIQUE NOT NULL,
  numTel VARCHAR(14) UNIQUE NOT NULL,
  horaires VARCHAR(100),
  dirigeant VARCHAR(100),
  image VARCHAR(100)
);

CREATE TABLE Client(
  idClient INT AUTO_INCREMENT PRIMARY KEY,
  civilite ENUM('homme','femme','autre') NOT NULL,
  nom VARCHAR(60) NOT NULL,
  prenom VARCHAR(60) NOT NULL,
  adresseMail VARCHAR(100) UNIQUE NOT NULL, #-- car on ne veut pas de doublons dans les adresses mail
  adresseFacturation VARCHAR(255),
  adresseLivraison VARCHAR(255),
  numTel VARCHAR(14) NOT NULL,
  mdp VARCHAR(60) NOT NULL,
  type ENUM('professionnel','particulier') NOT NULL,
  boutiqueFavorite INT,
  FOREIGN KEY (boutiqueFavorite) REFERENCES BoutiqueEntrepot(idBoutique)
);


CREATE TABLE Famille(
  idFamille INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Gamme(
  idGamme INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Marque(
  idMarque INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Produit(
  idProduit INT AUTO_INCREMENT PRIMARY KEY,
  assortiment BOOLEAN NOT NULL,
  nomProduit VARCHAR(255) UNIQUE NOT NULL,
  prix FLOAT NOT NULL,
  idFamille INT NOT NULL,
  idGamme INT NOT NULL,
  idMarque INT NOT NULL,
  detail VARCHAR(500) NOT NULL, #-- Description
  destination ENUM('repas', 'cadeau','aperitif'),
  image VARCHAR(100) NOT NULL,
  FOREIGN KEY (idFamille) REFERENCES Famille(idFamille),
  FOREIGN KEY (idGamme) REFERENCES Gamme(idGamme),
  FOREIGN KEY (idMarque) REFERENCES Marque(idMarque)
);


CREATE TABLE Assortiment(
  idAssortiment INT,
  idProduit INT,
  FOREIGN KEY (idAssortiment) REFERENCES Produit(idProduit),
  FOREIGN KEY (idProduit) REFERENCES Produit(idProduit),
  PRIMARY KEY (idAssortiment,idProduit)
);

CREATE TABLE ValeursNutritionnelles(
  idProduit INT PRIMARY KEY,
  energie INT NOT NULL,
  matieresGrasses FLOAT NOT NULL,
  dontAcidesGrasSatures FLOAT NOT NULL,
  glucide FLOAT NOT NULL,
  dontSucres FLOAT NOT NULL,
  proteines FLOAT NOT NULL,
  sel FLOAT NOT NULL,
  FOREIGN KEY (idProduit) REFERENCES Produit(idProduit)
);


CREATE TABLE Stock(
  idBoutiqueEntrepot INT,
  idProduit INT,
  quantite INT NOT NULL,
  FOREIGN KEY (idBoutiqueEntrepot) REFERENCES BoutiqueEntrepot(idBoutique),
  FOREIGN KEY (idProduit) REFERENCES Produit(idProduit),
  PRIMARY KEY (idBoutiqueEntrepot,idProduit)
);

CREATE TABLE Panier(
  idClient INT,
  idProduit INT,
  quantite INT NOT NULL,
  FOREIGN KEY (idClient) REFERENCES Client(idClient),
  FOREIGN KEY (idProduit) REFERENCES Produit(idProduit),
  PRIMARY KEY (idClient,idProduit)
);

CREATE TABLE Remise(
  typeClient ENUM('professionnel','particulier'),
  montantPourcentage FLOAT,
  minAchat INT,
  PRIMARY KEY (typeClient,montantPourcentage,minAchat)
);

CREATE TABLE Commande(
  idCommande INT AUTO_INCREMENT PRIMARY KEY,
  idClient INT,
  date DATE NOT NULL,
  remise FLOAT NOT NULL,
  statut ENUM('en_cours_de_preparation', 'preparee', 'en_cours_de_livraison', 'livree') NOT NULL,
  modeCommande ENUM('telephone', 'boutique', 'internet') NOT NULL,
  idBoutique INT,
  FOREIGN KEY (idClient) REFERENCES Client(idClient),
  FOREIGN KEY (idBoutique) REFERENCES BoutiqueEntrepot(idBoutique)
);

CREATE TABLE CommandeProduit(
  idCommande INT,
  idProduit INT,
  quantite INT NOT NULL,
  prix FLOAT NOT NULL,
  FOREIGN KEY (idProduit) REFERENCES Produit(idProduit),
  FOREIGN KEY (idCommande) REFERENCES Commande(idCommande),
  PRIMARY KEY (idCommande,idProduit)
);


CREATE TABLE Salarie(
  idSalarie INT AUTO_INCREMENT PRIMARY KEY,
  identifiant VARCHAR(60) NOT NULL,
  mdp VARCHAR(60) NOT NULL,
  UNIQUE CoupleUnique (identifiant,mdp)
);


#-- Pour supprimer la bdd :
#--DROP TABLE Salarie;
#--DROP TABLE Remise;
#--DROP TABLE Panier;
#--DROP TABLE Stock;
#--DROP TABLE ValeursNutritionnelles;
#--DROP TABLE Assortiment;
#--DROP TABLE CommandeProduit;
#--DROP TABLE Produit;
#--DROP TABLE Marque;
#--DROP TABLE Gamme;
#--DROP TABLE Famille;
#--DROP TABLE Commande;
#--DROP TABLE BoutiqueEntrepot;
#--DROP TABLE Client;




#-- FIN TABLE

INSERT INTO Famille(Nom) VALUES ("Classique")
INSERT INTO Famille(Nom) VALUES ("Assortiment")
INSERT INTO Famille(Nom) VALUES ("Specialite")
INSERT INTO Famille(Nom) VALUES ("Emiette")

INSERT INTO Gamme(Nom) VALUES ("Sardine")
INSERT INTO Gamme(Nom) VALUES ("Coquillage")
INSERT INTO Gamme(Nom) VALUES ("Lieu")

INSERT INTO Marque(Nom) VALUES ("Tradition Ocean")
INSERT INTO Marque(Nom) VALUES ("Nouveaute Ocean")


#-- De 1 à 4

INSERT INTO Produit(NumRef,Reference,Designation,Prix,Famille,Gamme,Marque,Quantite) VALUES (762,"Base","Emiette de sardine citron, olives et amandes",11.70,"Classique","Sardine","Tradition Ocean",100);
INSERT INTO Produit(NumRef,Reference,Designation,Prix,Famille,Gamme,Marque,Quantite) VALUES (4852,"Compose","Coffret sardines & sardines",29.65,"Assortiment","Sardine","Tradition Ocean",50);
INSERT INTO Produit(NumRef,Reference,Designation,Prix,Famille,Gamme,Marque,Quantite) VALUES (755,"Base","Petite marmite noisettes de st-jacques coco et gingembre",10.86,"Specialite","Coquillage","Nouveaute Ocean",150);
INSERT INTO Produit(NumRef,Reference,Designation,Prix,Famille,Gamme,Marque,Quantite) VALUES (813,"Base","Rillettes de lieu aux baies de sichuan",10.85,"Emiette","Lieu","Nouveaute Ocean",200);


#-- De 1 à 18
INSERT INTO Commande(idClient,Statut) VALUES (1,"en_cours_de_preparation");
INSERT INTO Commande(idClient,Statut) VALUES (1,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (1,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (2,"en_cours_de_livraison");
INSERT INTO Commande(idClient,Statut) VALUES (2,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (3,"en_cours_de_livraison");
INSERT INTO Commande(idClient,Statut) VALUES (3,"preparee");
INSERT INTO Commande(idClient,Statut) VALUES (3,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (4,"en_cours_de_preparation");
INSERT INTO Commande(idClient,Statut) VALUES (4,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (5,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (6,"en_cours_de_livraison");
INSERT INTO Commande(idClient,Statut) VALUES (6,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (6,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (7,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (8,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (8,"livree");
INSERT INTO Commande(idClient,Statut) VALUES (10,"en_cours_de_preparation");


#-- A creer dès qu'on cree une commande pour voir quel produit est dedans
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (1,1,4);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (1,2,1);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (1,3,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (2,1,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (2,3,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (3,1,7);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (3,4,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (4,3,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (5,3,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (5,4,1);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (6,3,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (7,2,1);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (8,1,4);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (8,2,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (8,4,6);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (9,3,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (10,1,3);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (10,2,1);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (11,4,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (12,1,8);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (12,2,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (12,3,1);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (12,4,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (13,1,5);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (13,4,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (14,1,2);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (15,3,7);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (16,2,9);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (17,1,12);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (17,1,6);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (17,2,3);
INSERT INTO CommandeProduit(NumCommande,idProduit,Quantite) VALUES (18,4,7);
