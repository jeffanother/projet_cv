# -*- coding: utf-8 -*-

import pandas as pd
import os
import sys



def chargement_fichier_parametres(self):
    """
    Chargement du fichier excel contenant les paramètres des recherches
    Renvoi une dataframe Pandas
    """
    nom_fichier = self.nom_fichier_parametres
    courant = os.getcwd()
    courant_m1 = ""
    while True:
        courant_m1 = courant
        if not os.path.isfile(nom_fichier):
            courant = os.path.dirname(courant) # Remonte au répertoire parent
            os.chdir(courant)
            if courant == courant_m1:
                break
        else:
            break

    if os.path.isfile(nom_fichier):
        xls_file = pd.ExcelFile(nom_fichier)
        excelOnglet1 = xls_file.sheet_names[0]
        df = xls_file.parse(excelOnglet1)
        self.parametres_df_loaded = True
        return df
    else:
        sys.exit("Le fichier de paramètre et soit absent, soit il ne porte pas le nom %s" % nom_fichier)
        return False
    
    
def ecriture_fichier_cvs(self):
    """
    Ecriture du fichier Excel contenant les CV scrapés
    """
    nomFeuilleExcel = "Scraping"
    try:
        writer = pd.ExcelWriter(self.nom_fichier_ecriture_resultats_recherche_cv)
        self.df.to_excel(writer, nomFeuilleExcel, index=False)
        writer.close()
    except:
        ## Essai pour écrire avec un autre nom si le fichier est déjà ouvert
#        try:
#            del writer
#            writer = pd.ExcelWriter(self.nom_fichier_ecriture_resultats_recherche_cv + "(2)")
#            self.df.to_excel(writer, nomFeuilleExcel, index=False)
#        except:
        raise IOError("Problème à l'écriture du fichier Excel contenant les CV.\n\
                      Le fichier est probablement ouvert.")


def test_si_fichier_output_ouvert(self):
    ecriture_possible = True
    nom_fichier = self.nom_fichier_ecriture_resultats_recherche_cv
    if os.path.isfile(nom_fichier):
        try:
            writer = pd.ExcelWriter(self.nom_fichier_ecriture_resultats_recherche_cv)
            writer.close()
        except:
            ecriture_possible = False
            print("Le fichier est ouvert, fermer le logiciel utilisant le fichier %s"
                  % self.nom_fichier_ecriture_resultats_recherche_cv)
    return ecriture_possible