# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from random import randint
from time import sleep
import pandas as pd
import os

from collectedata.indeed.recherche_cv import indeed_dataframe_Postulants




#----------------------------  Traitement de la partie CV  ----------------------------#

def telechargement_page_html_cv(url):
    """
    Télécharge la page HTML contenant le CV
    """
    html = requests.get(url, timeout=10).text
    if "Ce CV n'a pas pu être trouvé" in html:
#         print("\nNous sommes Blackliste\n")
        return False
    else:
        return html

#def telechargement_page_html_cv_2(url):
#    """
#    Télécharge la page HTML contenant le CV
#    """
#    # Le code en commentaire est un 1er jet pour sauvegarder et versionner les pages HTML téléchargées
#    repertoire_racine_projet = os.getcwd()
#    datastage_indeed = os.path.join(repertoire_racine_projet, "datastage", "indeed")
#    os.chdir(datastage_indeed)
#    nom_fichier = url[25:-5] + ".html"
#    # Vérifie si le CV à déjà été téléchargé
#    if not os.path.isfile(nom_fichier):
#        pass
#        
#    html = requests.get(url, timeout=10).text
#    
##    with codecs.open(nom_fichier, 'w', encoding='utf-8') as fichier:
##        pass
#        
##    os.chdir(repertoire_racine_projet)
#    if "Ce CV n'a pas pu être trouvé" in html:
#        return False
#    else:
#        return html.encode("utf-8")


def indeed_occurence_mots_cles_cv(motsCles, textCVLower):
    """
    Compte l'occurence des mots clés dans le CV
    Renvoi un String avec les mots clés classés par ordre décroissant à leur occurence
    """
    dictOccurences = {}
    for motCle in motsCles:
        motCle = motCle.strip(" ").lower()
        nbOccurence = len(re.findall(motCle, textCVLower))
        if nbOccurence > 0:  # Comme ça, les mots clés non trouvés ne resortent pas dans le classement
            dictOccurences[motCle] = nbOccurence
    dictOccurencesTriDecroissant = sorted(dictOccurences, key=dictOccurences.get, reverse=True)
    StrOccurenceTriDecroissant = ", ".join(dictOccurencesTriDecroissant)
    return StrOccurenceTriDecroissant


def indeed_occurence_mots_cles_cvs(self, indeedDF, motsCles):
    """
    Ajoute dans la dataframe "indeedDF" une colonne avec le classement des mots clés
    """
#    print("indeed_occurence_mots_cles_cvs()")
    k=0
    taille_df = len(indeedDF)
    tabOccurences = []
    for url in indeedDF['URL du CV']:
        
        # Scraping et parsing de la page html
        html = telechargement_page_html_cv(url)
        if html is False:
            print('Nous sommes blackliste !')
            break
        soup = BeautifulSoup(html, 'html.parser')
        soup_HtmlCV = soup.select("div.hresume")[0]
        textCVLower = soup_HtmlCV.text.lower()
        tabOccurences.append(indeed_occurence_mots_cles_cv(motsCles, textCVLower))
        
        #Temporisation pour éviter d'être blacklisté
        nbsecondes = randint(1, 5)
        sleep(nbsecondes)
        
    # # Supprimer la condition et la variable "k" lorsque le développement sera terminé
        k+=1
        if self.mode_verbeux:
            print(str(k) + " / " + str(taille_df) + " | " + indeedDF["Poste actuel"][k])
        if self.mode_test:
            if k>=0:
                break
    
    indeedDF['Compétences'] = pd.DataFrame(tabOccurences)
    return indeedDF
    
def scraping_cv(self):
    """
    Scrape et parse les CV trouvés sur Indeed via les paramètres de recherche
    """
#    print("scraping_cv()")
    if self.scraping_cv_done is False:
        if self.parametres_df_loaded is False:
            self.ChargementFichierParametres()
            
        # Traite la dataframe ligne par ligne
        indeed_df = pd.DataFrame()
        site = "Indeed"
        for parametresLignes in self.parametres_df.values:
            if self.blackliste is False:
                if parametresLignes[0].lower() == site.lower():
                    codePostal = str(parametresLignes[3]).strip(' ')
                    rayon = str(parametresLignes[4]).strip(' ')
                    fraicheurCV = parametresLignes[5].strip(' ').lower()
                    motsCles = parametresLignes[2].split(',')
                    
                    # Boucle tournant sur les différents type de postes mis sur la ligne
                    for typeDePoste in parametresLignes[1].split(','):
                        typeDePoste = typeDePoste.strip(' ').lower()
                        print(typeDePoste.upper())
                        indeedDF = indeed_dataframe_Postulants(typeDePoste, codePostal, rayon, fraicheurCV)
                        
                        if indeedDF is False:
                            print("Nous sommes blackliste !")
                            self.blackliste = True
                            break
                        
                        df_poste = indeed_occurence_mots_cles_cvs(self, indeedDF, motsCles)
                        indeed_df = indeed_df.append(df_poste, ignore_index=True)
        if not indeed_df.empty:
            self.scraping_cv_done = True
        else:
            indeed_df = False
        return indeed_df
