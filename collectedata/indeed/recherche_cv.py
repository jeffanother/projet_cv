# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from time import sleep
from random import randint


#----------------------------  Traitement de la phase de recherche des candidats  ----------------------------

def indeed_generation_url_depart(poste, codePostal, rayonRecherche, fraicheurCV):
    """
    Cette fonction génère une URL correspondant à la recherche souhaitée
    
    Sur Indeed, c'est l'URL qui permet d'accéder à une recherche en particulier.
    Les paramètres de la fonction permettent de créer une URL pointant vers la
    première page de recherche.
    """

    #Vérification de la cohérence des variables
    if not (isinstance(poste, str) and len(poste) > 0):
        raise ValueError('La valeur de la variable "poste" entrée dans la \
                         fonction "indeed_generation_url_depart" est erronée.\n\
                         - Soit ce n\'est pas un String\n\
                         - Soit le String est vide')
    if not (isinstance(codePostal, str) and len(codePostal) == 5):
        raise ValueError('La valeur de la variable "codePostal" entrée dans la \
                         fonction "indeed_generation_url_depart" est erronée.\n\
                         - Soit ce n\'est pas un String\n\
                         - Soit le String ne fait pas 5 caractères')
    if not (isinstance(rayonRecherche, str) and
            int(rayonRecherche) > 5 and
            int(rayonRecherche) < 2000):
        raise ValueError('La valeur de la variable "rayonRecherche" entrée dans \
                         la fonction "indeed_generation_url_depart" est erronée.\n\
                         - Soit ce n\'est pas un String\n\
                         - Soit la valeur n\'est pas entre 1 et 2000')
    if fraicheurCV == "mois":
        fraicheurCV = "month"
    elif fraicheurCV == "semaine":
        fraicheurCV = "week"
    elif fraicheurCV == "jour":
        fraicheurCV = "day"
    else:
        fraicheurCV = "all"

    # Génération de l'URL
    url = "https://www.indeed.com/resumes"
    poste = "?q=" + poste.replace(" ","+")
    codePostal = "l=" + codePostal
    rayonRecherche = "co=FR&radius=" + rayonRecherche
    fraicheurCV = "lmd=" + fraicheurCV
    url += "&".join([poste, codePostal, rayonRecherche, fraicheurCV])
    return url

def indeed_generation_url_page_suivante(soup):
    """
    Extrait l'URL de la page suivante de recherche et retourne False à la dernière
    """
    url = "https://www.indeed.com/resumes"
    next = soup.select("a.confirm-nav.next")
    if len(next) > 0:
        urlPartielle = next[0].attrs['href']
        return url + urlPartielle
    else:
        return False

def indeed_dataframe_Postulants(typeDePoste, codePostal, rayonPostulant, fraicheurCV):
    """
    Récupère les informations sur le candidat (dernier poste, lieu de résidence, URL du CV)
    Renvoi une dataframe pandas contenant les informations
    """
    # convertit l'abréviation du mois (ex : "févr" en "février")
    def conversion_mois(mois_a_convertir):
        mois_a_convertir_tab = mois_a_convertir.split(" ")
        if mois_a_convertir_tab[1] == "janv":
            mois_a_convertir_tab[1] = "janvier"
        if mois_a_convertir_tab[1] == "févr":
            mois_a_convertir_tab[1] = "février"
        if mois_a_convertir_tab[1] == "avr":
            mois_a_convertir_tab[1] = "avril"
        if mois_a_convertir_tab[1] == "juil":
            mois_a_convertir_tab[1] = "juillet"
        if mois_a_convertir_tab[1] == "sept":
            mois_a_convertir_tab[1] = "septembre"
        if mois_a_convertir_tab[1] == "oct":
            mois_a_convertir_tab[1] = "octobre"
        if mois_a_convertir_tab[1] == "nov":
            mois_a_convertir_tab[1] = "novembre"
        if mois_a_convertir_tab[1] == "déc":
            mois_a_convertir_tab[1] = "décembre"
        mois_convertis = " ".join(mois_a_convertir_tab)
        return mois_convertis


    poste = []
    lieuResidence = []
    urlCV = []
    maj = []
    itsOK = True
    annee = str(date.today().year)

    url = indeed_generation_url_depart(typeDePoste, codePostal, rayonPostulant, fraicheurCV)
    # Boucle traitant page HTML par page HTML (50 offres par page)
    while True:
        # Récupération page HTML
        try:
            html = requests.get(url, timeout=10).text
            #Temporisation pour éviter d'être blacklisté
            nbsecondes = randint(1, 3)
            sleep(nbsecondes)
        except:
            print("\nLe site ne répond pas !\n")
            break

        #Parsing
        soup = BeautifulSoup(html, 'html.parser')
        offres = soup.select("div.sre-entry")
        if len(offres) == 0:
            itsOK = False
            break
        # Boucle traitant offre par offre sur la page HTML
        for offre in offres:
            
            # Parsing du poste
            poste.append(offre.select("a.app_link")[0].text)
            
            # Parsing du lieu de résidence
            try:
                lieuResidenceTmp = offre.select("span.location")[0].text.replace(" - ","")
            except:
                lieuResidenceTmp = ""
            lieuResidence.append(lieuResidenceTmp)
            
            # Parsing de l'url de l'offre
            urlCV.append("https://www.indeed.com" + offre.select("a.app_link")[0].attrs['href'])
            
            # Parsing de la date de mise à jour du CV
            majTemp = offre.select("div.times span.last_updated")[0].text.split(" : ")[1].replace(".", "")
            majTemp = (majTemp + " " + annee) if len(majTemp.split(" ")) == 2 else majTemp
            maj.append(majTemp)
            maj = conversion_mois(maj)

        # Récupère l'url de la page HTML suivante
        url = indeed_generation_url_page_suivante(soup)
        if url == False:
            break

    if itsOK is True:
        taille_tableau = len(poste)
        tab_typeDePoste = [typeDePoste.capitalize() for x in range(taille_tableau)]
        tab_site = ["Indeed" for x in range(taille_tableau)]
        dataPartielle = pd.DataFrame({'Site':tab_site,
                                      'Type de poste recherché':tab_typeDePoste,
                                      'Poste actuel':poste,
                                      'Lieu de résidence':lieuResidence,
                                      'URL du CV':urlCV,
                                      'Date de mise à jour':maj
                                      })
    else:
        dataPartielle = False
        
    return dataPartielle

