from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class ArticleSap(CsvImport):
    """
    Classe pour l'importation des données des Articles SAP
    """

    cles = ['id_article', 'code_d', 'ordre', 'intitule', 'code_sap', 'quantite', 'unite', 'texte_sap']
    nom_fichier = "articlesap.csv"
    libelle = "Articles SAP"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_article'], info = Format.est_un_alphanumerique(donnee['id_article'], "l'id article SAP", ligne)
            msg += info
            if info == "":
                if donnee['id_article'] not in ids:
                    ids.append(donnee['id_article'])
                else:
                    msg += "l'id article SAP '" + donnee['id_article'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            donnee['code_d'], info = Format.est_un_alphanumerique(donnee['code_d'], "le code D", ligne)
            msg += info
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé", ligne)
            msg += info
            donnee['code_sap'], info = Format.est_un_entier(donnee['code_sap'], "le code sap", ligne, 1)
            msg += info
            donnee['quantite'], info = Format.est_un_nombre(donnee['quantite'], "la quantité", ligne, 3, 0)
            msg += info
            donnee['unite'], info = Format.est_un_texte(donnee['unite'], "l'unité", ligne)
            msg += info
            donnee['ordre'], info = Format.est_un_entier(donnee['ordre'], "l'ordre annexe", ligne, 1)
            msg += info
            donnee['texte_sap'], info = Format.est_un_texte(donnee['texte_sap'], "le texte sap", ligne, True)
            msg += info

            donnees_dict[donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
