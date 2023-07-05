
# Swissborg analyzer

Ce programme python analyse et retraite le fichier de relevé de compte exporté par Swissborg. 




## Features

- Lit le fichier de relevé de compte Excel de Swissborg "account_statement"
- Le reformate dans un nouveau fichier excel plus facilement exploitable dans un reporting global de suivi :
    crée un onglet par crypto, additionne les payouts ... par exemple pour un onglet BTC voici les premières lignes : 

| Transaction | Compte    | Date                  | Operation | Montant euro | cours       | Statut KYC | Montant KYC | Montant BTC KYC | Montant BTC Total | Note |
|-------------|-----------|-----------------------|-----------|--------------|-------------|------------|-------------|-----------------|-------------------|------|
|             | Swissborg | 27 avr 2022  08:49:50 | Achat     | 1500         | 36370,28938 | 1          | 1500        | 0,041036242     | 0,041036242       |      |
|             | Swissborg | 27 avr 2022  08:49:50 | Achat     | 500          | 36357,572   | 1          | 500         | 0,013683532     | 0,013683532       |      |
|             | Swissborg | 27 avr 2022  08:49:50 | Achat     | 1500         | 35330,01649 | 1          | 1500        | 0,042244532     | 0,042244532       |

- Affiche à l'écran une synthèse par crypto. Par exemple ci-dessous pour la crypto DOT :
 pour la currency : DOT                                  |
|---------------------------------------------------------|
nb de transaction (achat , exchange ...) 	: 2  
montant total investi en € 			: 198 €  
nombre de DOT achetés 				: 13.85  
prix moyen pondéré de ces achats	: 14.31  
nombre de DOT reçus en Payout 		: 1.09  
nb de DOT total 				    : 14.93  
cours actuel DOT				    : 4.92  
au cours actuel, cela représente une valeur de 	: 73.48  
il reste  14.93 DOT en portefeuille

et ceci pour chacune des cryptos en portefeuille ( ou que vous avez utilisés dans Swissborg, même s'il n y en plus en portefeuille)


## Pré-requis
python 3

installation des bibliothèques python nécessaires via le fichier requirements.txt :
pip install -r requirements.txt -v
## Installation et fonctionnement
copiez le fichier python et le fichier Swissborg "account_statement" dans le même repertoire

ouvrez un terminal ( fenetre )

allez dans ce répertoire

lancer le programme python



## Arguments
-i : input file  ( par defaut "account_statement.xlsx")

-o : output file sans .xlxs ( par defaut "reportsb")

-h : help
## Hypothèses
Le format attendu du fichier de relevé de compte Swissborg ( juin 2023) : 
| Local time | Time in UTC | Type | Currency | Gross amount | Gross amount (EUR) | Fee | Fee (EUR) | Net amount | Net amount (EUR) | Note |
|------------|-------------|------|----------|--------------|--------------------|-----|-----------|------------|------------------|------|

Les données Swissborg commence ligne 14. Ligne où se trouve les titres des colonnes (ci dessus).

la monnaie fiat de l'exchange est l'Euro.


## Tester votre installation

Pour tester le bon fonctionnement du programme dans votre environnement, vous trouverez dans le repertoire "test" un fichier type account_statement.xlsx  ainsi que les outputs que vous devriez obtenir apres traitement de ce fichier : report excel et copie des informations écran.




## Feedback

Si vous avez des feedbacks, questions, suggestions, merci de contacter tepejean@protonmail.com
