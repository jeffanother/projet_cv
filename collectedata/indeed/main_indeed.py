# -*- coding: utf-8 -*-

from collectedata.indeed.gestion_fichiers import chargement_fichier_parametres as chargement_fichier_excel_parametres
from collectedata.indeed.gestion_fichiers import ecriture_fichier_cvs as ecriture_fichier_excel_cvs
from collectedata.indeed.gestion_fichiers import test_si_fichier_output_ouvert
from collectedata.indeed.extraction_cv import scraping_cv
import pandas as pd




class ObjetIndeed:
    """
    Objet servant à manipuler les données du site Indeed
    """
    def __init__(self):
        self.nom_fichier_ecriture_resultats_recherche_cv = "CV trouvés.xlsx"
        self.nom_fichier_parametres = "Paramètres.xlsx"

        self.parametres_df = ""
        self.parametres_df_loaded = False
        self.scraping_cv_done = False
        self.tableau_de_DFs = ""
        self.df = pd.DataFrame(columns=["Site",
                                        "Type de poste recherché",
                                        "Poste actuel",
                                        "Compétences",
                                        "Lieu de résidence",
                                        "Date de mise à jour",
                                        "URL du CV",
                                        ])
        self.mode_verbeux = True
        self.blackliste = False
        self.mode_test = False
        self.ChargementFichierParametres()
        
    def ActiverModeTest(self):
        self.mode_test = True
        self.mode_verbeux = True
        self.temp = ""

#        data = [['indeed', 'Data scientist', 'expert data', 'hadoop', 'Santeny', 'http://pouet.fr'],
#                ['indeed', 'Data scientist', 'data engineer', 'hadoop, spark', 'Créteil', 'http://soup.fr'],
#                ['indeed', 'Data scientist', 'docteur en data', 'elk, spark', 'Paris', 'http://indeed.fr']]
#        colonnes = ["Site",
#                    "Type de poste",
#                    "Poste",
#                    "Compétences",
#                    "Lieu de résidence"
#                    "Date de mise à jour",
#                    "URL du CV"]
#        self.df = pd.DataFrame(data, columns=colonnes)
#        self.df_test = chargement_fichier_excel_parametres(self)
#        self.tableau_de_DFs = [{"nom" : "Poste 1", "df" : self.df_test}, 
#                               {"nom" : "Poste 2", "df" : self.df_test}]

    def ChargementFichierParametres(self):
        """
        Charge le fichier Excel contenant les paramètres
        """
        self.parametres_df = chargement_fichier_excel_parametres(self)
        
    def ScrapingCV(self):
        """
        Scrape et parse les CV trouvés sur Indeed via les paramètres de recherche
        """
        if test_si_fichier_output_ouvert(self):
            if self.scraping_cv_done is False:
                df_indeed = scraping_cv(self)
                self.df_indeed = df_indeed
                self.df = self.df.append(df_indeed, ignore_index=True)

    def EcritureFichierCV(self):
        """
        Ecriture du fichier Excel contenant les CV scrapés
        """
        ecriture_fichier_excel_cvs(self)

        


if __name__ is "__main__":
    pass
    
#    indeed = ObjetIndeed()
#    indeed.activer_mode_test()
#    print()
##    indeed.scraping_cvs()
##    indeed.ecriture_fichier_cvs()
    
    
    
    
    
