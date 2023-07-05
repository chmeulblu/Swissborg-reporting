import pandas as pd
#import xlsxwriter
import requests
import argparse


#------------------------------------------------
# quelques fonctions
#
#------------------------------------------------

# récupere le cours actuel d'une crypto en monnaie fiat ou stable sur Binance
# à tester pour connaitre avant les couples possibles. marche bien par exemple pour BTC , ETH, DOT ... vers soit EUR soit USDT
# renvoie une erreur si le cours n'est pas trouvé

def get_cur_price ( crypto , fiat ) :
    # recupere la valeur via une API sur Binance
    base_url = 'https://api.binance.com'
    path ='/api/v3/ticker/price?symbol='
    currencies = crypto+fiat

    data = requests.get(base_url+path+currencies)
    data=data.json()

    return float (data['price'])






#---------------------------------------------------
# gestion des arguments si il y en a ( sinon des  valeurs par defauts sont definis )
# on récupere les arguments depuis la ligne de commande
#
#---------------------------------------------------

# noms de fichier par default
default_inputfile  = 'account_statement.xlsx'
default_reportfile = 'reportsb'

parser = argparse
parser = argparse.ArgumentParser(
                    description = 'Extrait, compile et formatte le fichier de reporting de Swissborg.')

parser.add_argument('-i', '--SBinputfile' , metavar='', default = default_inputfile, help='le nom du fichier d entree de swissborg (doit etre dans le meme repertoire que le programme). par default :'+ default_inputfile)
parser.add_argument('-o', '--outputfile', metavar='', default = default_reportfile, help='le nom du fichier Excel du reporting qui sera créé (sans le xlsx). Par default :'+default_reportfile )
args = parser.parse_args()


inputfile=args.SBinputfile
reportfile=args.outputfile +'.xlsx'

print( 'inputfile :' , inputfile, '\noutputfile :' , reportfile)



#---------------------------------------------------------
# initialise quelques variables spécifiques pour swissborg
#
#---------------------------------------------------------


kyc = 1   		# swissborg est KYC par defaut ( a tuner peut etre si cas particuliers... )
Header = 13		# nombre de lignes d entete ( = inutile, à sauter ) du fichier fourni par SB.

#  dans cette version on prend comme hypothese que la currency fiat de depot est l'euro ('EUR')


# -------------------------------------------------------
#
# lit le fichier fourni par Swissborg en sautant le header :
#        recupere les labels (= nouvelle ligne 1) puis les data qui suivent ( nouvelle ligne 2 et suivantes )
# juin 2023. le format du fichier Excel de Swissborg est formatté de la facon suivante :
# Local time	Time in UTC	Type	Currency	Gross amount	Gross amount (EUR)	Fee	Fee (EUR)	Net amount	Net amount (EUR)	Note
# le fichier est dans le repertoire d execution du programme ( si lancé en ligne de commande , à verifier autrement si executable)
#
# ---------------------------------------------------------

compte_sb = pd.read_excel(inputfile,header=Header)


# -----------------------------------------------------
#
#  traitements globaux sur l'ensemble du datamap 
#  en préliminaire aux traitements individuels par currency
#  
#
# -----------------------------------------------------

#  1 - transforme le type generic 'object' de la colonne 'Date' en type 'date'
compte_sb['Local time'] = pd.to_datetime(compte_sb['Local time'])

#  2 - si une operation de vente : le montant vendu passe en négatif
compte_sb.loc[compte_sb.Type =='Sell' , 'Net amount'] = compte_sb['Net amount'] * -1

# 3 - s il est mentionné un exchange ET une autre monnaie que EUR ( c est a dire une cryptomonnaie) dans la colonne 'Note', il s'agit vraiment d'un exchange entre crypto:
# on met à jour le type d'operation à Exchange, et le montant en euro passe à zero ( il n y a pas d'achat en euro sur cette opération)
compte_sb.loc[
        (compte_sb.Note.str.contains('Exchanged') &
        ((compte_sb.Note.str.contains('EUR') == False )))  ,
             ['Type','Gross amount (EUR)'] ]=['Exchange',0] 
# sinon, il s agit d un Achat : on remplace le type d'operation 'buy' par Achat et on supprime le texte de la note qui allourdit le tableau
compte_sb.loc[ compte_sb.Note.str.contains('EUR') == True, ['Type','Note']]= ['Achat','']


# on memorise la liste de toutes les currencies traitées :
# a noter, la currency fiat = l'euro (EUR) en fait partie
list_currency = compte_sb['Currency'].unique()
print()
print('Currency identifiée : ' + list_currency)

# on définit les colonnes de l'Excel qui sont utiles pour notre reporting. On ne gardera que ces colonnes
mes_colonnes =['Local time', 'Type','Gross amount (EUR)', 'Net amount', 'Net amount (EUR)','Note']

# on initialise la structure Excel de reporting : nom du fichier + XlsxWriter comme structure. ( permet plus de souplesse )
# on en profite pour reformater les données correspondantes à une date+heure en J/M/A h:m. facilite la lecture des dates du tableau final, pas obligatoire.
writer = pd.ExcelWriter(reportfile, engine='xlsxwriter',datetime_format='d mmm yyyy  hh:mm:ss')




# ------------------------------------------------------------------------------------
#
# on demarre ! 
# on itere et traite chacune des Currencies
# un onglet est ensuite créé pour chaque currency 
#
# ------------------------------------------------------------------------------------

for cur in list_currency :

    # on filtre dans le datamap principal les lignes pour ne garder que les transactions Achat, Vente, Exchange et Deposit de la currency.
    # pour Swissborg = cela supprime : 
    #       	Withdrawal 	: correspond à un envoi vers un wallet exterieur. Ignoré pour  l instant dans le fichier reporting créé utilisé toutefois utilisé dans la synthese d information
    #       	Payouts 	: les yields, ils sont traités dans un datamap à part, pour en garder juste la somme dans le reporting 
    tab_buy_sell = compte_sb.loc[
            ( compte_sb['Currency']==cur) &
             compte_sb['Type'].isin(['Achat','Sell','Exchange','Deposit']) ,  
       mes_colonnes]

    # calcul et mémorise le total de Payouts de la cur s'il y en a pour cette currency
    tab_payouts = compte_sb.loc[
            ( compte_sb['Currency']==cur) &
             compte_sb['Type'].isin(['Payouts']) ,  
       mes_colonnes]
    Total_Payouts = tab_payouts['Net amount'].sum()
 
  
    # on calcule le cours de la currency de chaque transaction ... c'est à dire le montant réeellement transformé en currency / montant net de currency obtenu
    cours = ( (tab_buy_sell['Net amount (EUR)'] / abs(tab_buy_sell['Net amount'])))

    # on renomme les colonnes selon tableau reporting désiré
    tab_buy_sell.columns = ['Date', 'Operation', 'Montant euro', 'Montant '+ cur +' Total', 'montant euro net','Note']

    # s'il y en a, on rajoute en derniere ligne le total des Payouts.
    if (Total_Payouts > 0) :
        payout_row = { 'Operation' : 'Payouts', 'Montant '+ cur +' Total' : Total_Payouts }
        tab_buy_sell.loc [ len(compte_sb.index) ] = payout_row  # tous les Payouts du reporting auront le meme numero d index . cela peut etre changé ( increment d une variable) . pas fait) 
 
 
    # on rajoute quelques nouvelles colonnes que l'on souhaite voir dans le reporting,  en initialisant avec des valeurs si possible : 

    #  nouvelle colonne du cours de la currency au moment de la transaction
    tab_buy_sell["cours"] = cours

    # nouvelle colonne pour Status KYC
    tab_buy_sell["Statut KYC"] = kyc

    # nouvelle colonne pour transaction
    tab_buy_sell["Transaction"] =' '

    # nouvelle colonne pour compte
    tab_buy_sell["Compte"] = "Swissborg"

    # nouvelle colonne pour montant KYC
    tab_buy_sell["Montant KYC"]= tab_buy_sell["Statut KYC"]*tab_buy_sell['Montant euro']

    #nouvelle colonne pour montant KYC de la currency
    tab_buy_sell['Montant '+ cur+ ' KYC']= tab_buy_sell["Statut KYC"]*tab_buy_sell['Montant ' + cur +' Total']

    # nouvelle colonne p/p , perte ou profit d une ligne d achat par rapport au cours actuel. Abandonné pour l'instant.
    #tab_buy_sell["p/p"]=0     # init à zero , pourrait etre initialisé a la valeur p/p au moment du traitement ( puisque  l'on a le cours )


    # on mets les colonnes dans l'ordre choisi pour le fichier du reporting  (à adapter selon votre souhait)
    tab_buy_sell = tab_buy_sell[['Transaction', 'Compte', 'Date','Operation', 'Montant euro', 'cours', 'Statut KYC', 'Montant KYC', 'Montant ' + cur+ ' KYC', 'Montant ' + cur + ' Total','Note']]

    # 
    # --------------------------------------------------------------------
    # ça y est, le reporting pour cette currency est finalisé
    # on le stocke dans un onglet excel au nom de cette currency 
    
    tab_buy_sell.to_excel(writer, sheet_name=cur,index=False,freeze_panes=(1,1))
    
    #  dernier ajustement : on dimensionne la largeur de chacune des colonnes à son element le plus grand en nombre de caracteres
    for column in tab_buy_sell:
        column_length = max(tab_buy_sell[column].astype(str).map(len).max(), len(column))
        col_idx = tab_buy_sell.columns.get_loc(column)
        writer.sheets[cur].set_column(col_idx, col_idx, column_length+1)
        
    # --------------------------------------------------------------------
 
 
    # -------------------------------------------------------------------------------------------------------------
    #
    # en bonus : 
    # affiche sur l'ecran ((stdout), mais pas dans le fichier de reporting, quelques valeurs de synthese pour chaque currency :
    # ce n'est pas necessaire pour le fichier reporting
    # juste pour information et utilisation/recopie si utile par ailleurs
    #
    # -------------------------------------------------------------------------------------------------------------
    
    print()
    print('pour la currency : '+ cur )
    
    nb_transaction = tab_buy_sell.Transaction.count()
    print('nb de transaction (achat , exchange ...) \t: ' + str (nb_transaction))
 
 
    # memorise le total des retraits du portefeuille de cette currency s'il y en a
    tab_withdrawal = compte_sb.loc[
            ( compte_sb['Currency']==cur) &
             compte_sb['Type'].isin(['Withdrawal'])]
    Total_withdrawal = tab_withdrawal['Gross amount'].sum()
    Total_transfered = tab_withdrawal['Net amount'].sum()
    
    # memorise les euros investis sur la currency et le nombre de currency acheté pour ce montant
    tab_investi_euro = compte_sb.loc[
            ( compte_sb['Currency']==cur) &
             compte_sb['Type'].isin([ ( 'Deposit' if cur =='EUR' else 'Achat')])]
    Total_investi_euro = tab_investi_euro['Gross amount (EUR)'].sum()
    Total_cur_achete= tab_investi_euro['Net amount'].sum()
    
    # memorise le nombre de cur recues d'un autre exchange
    tab_recu_exterieur = compte_sb.loc[
            ( compte_sb['Currency']==cur) &
             compte_sb['Type'].isin([ ( 'Deposit')])]
    Total_recu_exterieur = tab_recu_exterieur['Net amount'].sum()
  
    # memorise  le nombre de cur obtenues via exchange/swap interne
    tab_nb_cur_recu_interne = tab_buy_sell.loc[
            tab_buy_sell['Operation'].isin([('Exchange')])
            ]
    Total_cur_recu_interne = tab_nb_cur_recu_interne['Montant '+cur+' Total'].sum()
    
    # memorise le nombre de currency restant en portefeuille
    nb_cur_restant = tab_buy_sell['Montant '+cur+' Total'].sum()

    # memorise le nombre total de cette currency
    nb_cur_total = tab_buy_sell['Montant ' + cur +' Total'].sum()

  
    print('montant total investi en € \t\t\t: '+ str(int(Total_investi_euro)) + ' €')
    

    # si c'est une crypto on peut afficher un peu plus de données
    if ( cur != 'EUR') :
        if (Total_cur_achete > 0 )  		:
            print('nombre de '+ cur + ' achetés \t\t\t\t: ' + str(format(Total_cur_achete, '.2f')))
            print('prix moyen pondéré de ces achats\t\t: '+ str(format(Total_investi_euro/Total_cur_achete,'.2f')))
     
        if (Total_recu_exterieur > 0 )  	: print('nombre de '+ cur + ' reçus de wallets externes \t: ' + str (format(Total_recu_exterieur,'.2f')))
 
        if (Total_cur_recu_interne > 0 )  	: print('nombre de '+ cur + ' issues d exchanges internes \t: '+str(format(Total_cur_recu_interne,'.2f')))
        if (Total_Payouts > 0) 				: print('nombre de '+ cur + ' reçus en Payout \t\t\t: ' + str(format(Total_Payouts,'.2f')))
        if (Total_cur_achete > 0 )  		: print('nb de ' + cur + ' total \t\t\t\t: ' + str(format(nb_cur_total,'.2f')))
        try :  # va essayer de recuperer le cour de la currency , si ça marche on l affiche ainsi que valeur du portefeuille
            cours_cur_actuel = get_cur_price (cur, "EUR")
            print('cours actuel ' +cur + '\t\t\t\t: ' + str(format(cours_cur_actuel,'.2f')))
            print('au cours actuel, cela représente une valeur de \t: ' + str( format(cours_cur_actuel * nb_cur_total ,'.2f')))
        except :
            pass # on a pas eu le cours de la currency ( souvent un binome inconnu de l API)  --> ne fait rien

    # on termine en affichant ce qui a ete retiré du portefeuille s'il y en a et ce qui reste en portefeuille pour cette currency
    if ( Total_withdrawal > 0) 			:
        print ( str(format(Total_withdrawal,'.2f')) +' ' + cur + ' retirés du portefeuille SW ')
        print ( str(format(Total_transfered,'.2f')) +' ' + cur + ' réellement transférés vers adresses externes (= moins cout exchange)') 
    print ( '\nil reste  ' +  str( format(nb_cur_total - Total_withdrawal,'.2f')) + ' ' +cur + ' en portefeuille')   
   
    print()
    print()
    
    # --------------------------------------------------------------------------------
    # affichage des infos suplémentaires terminé pour cette currency
    # --------------------------------------------------------------------------------
    

# on boucle sur la currency suivante




# -------------------------------------------------------------------------------------------------
#
# on a traité toutes les currencies ( euro + cryptos)  du fichier Swissborg
# on sauvegarde/écrit le fichier final Excel de reporting
#
# -------------------------------------------------------------------------------------------------

writer.close()

print()
print('traitement terminé, le reporting formaté est sauvegardé dans le fichier : ' + reportfile )


# that's all folk
