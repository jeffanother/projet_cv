# -*- coding: utf-8 -*-


from collectedata.indeed.main_indeed import ObjetIndeed



indeed = ObjetIndeed()
indeed.ChargementFichierParametres()
print(indeed.parametres_df)