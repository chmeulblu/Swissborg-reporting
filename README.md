
# Swissborg analyzer

Ce programme python analyse le fichier état csv exporté par Swissborg. 




## Features

- lit le fichier csv Swissborg (format excel)
- le reformate dans un nouveau fichier excel customizé et plus facilement exploitable :
    creer un onglet par crypto, additionne les payouts ...

- affiche à l'écran une synthese par crypto



## Pré-requis
installation de bybliothèques python via le fichier requirements.txt :
pip install -r requirements.txt -v
## démarrage
copier le fichier python et le fichier swissborg "account_statement" dans le meme repertoire

ouvrez un terminal ( fenetre )

allez dans ce répertoire

lancer le programme python



## arguments
-i : input file  ( par defaut "account_statement.xlsx")

-o : output file sans .xlxs ( par defaut "reportsb")

-h : help
## hypotheses
le format attendu du fichier swissborg ( juin 2023) : 
Local time - Time in UTC -	Type -	Currency -	Gross amount -	Gross amount (EUR)	- Fee - 	Fee (EUR)- Net amount - 	Net amount (EUR)	- Note

la monnaie fiat de l exchange est l'Euro.
## fonctionnalités ..pour plus tard
option -f pour customiser la monnaie fiat utilisée ( US ...)

formatage automatique de la largeur des colonnes du fichier export ( largeur fixe pour  l'instant)