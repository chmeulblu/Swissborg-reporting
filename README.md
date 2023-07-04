
# Swissborg analyzer

Ce programme python analyse et retraite le fichier de relevé de compte exporté par Swissborg. 




## Features

- Lit le fichier de relevé de compte Excel de Swissborg "account_statement"
- Le reformate dans un nouveau fichier excel plus facilement exploitable dans un reporting global de suivi :
    crée un onglet par crypto, additionne les payouts ...

|   | Transaction | Compte | Operation | Montant euro | Date | cours | Statut KYC | Montant KYC | Montant BTC KYC | Montant BTC Total |
|---|-------------|--------|-----------|--------------|------|-------|------------|-------------|-----------------|-------------------|
- Affiche à l'écran une synthèse par crypto.



## Pré-requis
python 3

installation des bibliothèques python nécessaires via le fichier requirements.txt :
pip install -r requirements.txt -v
## Installation et fonctionnement
copiez le fichier python et le fichier Swissborg "account_statement" dans le même repertoire

ouvrez un terminal ( fenetre )

allez dans ce répertoire

lancer le programme python



## arguments
-i : input file  ( par defaut "account_statement.xlsx")

-o : output file sans .xlxs ( par defaut "reportsb")

-h : help
## hypotheses
Le format attendu du fichier de relevé de compte Swissborg ( juin 2023) : 
| Local time | Time in UTC | Type | Currency | Gross amount | Gross amount (EUR) | Fee | Fee (EUR) | Net amount | Net amount (EUR) | Note |
|------------|-------------|------|----------|--------------|--------------------|-----|-----------|------------|------------------|------|

Les données Swissborg commence ligne 14. Ligne où se trouve les titres des colonnes (ci dessus).

la monnaie fiat de l'exchange est l'Euro.


## fonctionnalités ... pour plus tard


Dimensionnement automatique de la largeur des colonnes du fichier de reporting généré ( largeur identique fixe pour  l'instant pour toutes les colonnes ). Contactez moi si vous savez comment faire !
## Tester votre installation

Pour tester le bon fonctionnement du programme dans votre environnement, vous trouverez dans le repertoire "test" un fichier type account_statement.xlsx  ainsi que les outputs que vous devriez obtenir apres traitement de ce fichier : report excel et copie des informations écran.




## Feedback

Si vous avez des feedbacks, questions, suggestions, merci de contacter tepejean@protonmail.com

