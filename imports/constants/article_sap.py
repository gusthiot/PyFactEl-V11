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

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_article'], info = Format.est_un_alphanumerique(donnee['id_article'], "l'id article SAP")
            msg += self._erreur_ligne(ligne, info)
            if info == "":
                if donnee['id_article'] not in ids:
                    ids.append(donnee['id_article'])
                else:
                    msg += self._erreur_ligne(ligne,
                                              "l'id article SAP '" + donnee['id_article'] + "' n'est pas unique\n")

            donnee['code_d'], info = Format.est_un_alphanumerique(donnee['code_d'], "le code D")
            msg += self._erreur_ligne(ligne, info)
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé")
            msg += self._erreur_ligne(ligne, info)
            donnee['code_sap'], info = Format.est_un_entier(donnee['code_sap'], "le code sap", 1)
            msg += self._erreur_ligne(ligne, info)
            donnee['quantite'], info = Format.est_un_nombre(donnee['quantite'], "la quantité", 3, 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['unite'], info = Format.est_un_texte(donnee['unite'], "l'unité")
            msg += self._erreur_ligne(ligne, info)
            donnee['ordre'], info = Format.est_un_entier(donnee['ordre'], "l'ordre annexe", 1)
            msg += self._erreur_ligne(ligne, info)
            donnee['texte_sap'], info = Format.est_un_texte(donnee['texte_sap'], "le texte sap", True)
            msg += self._erreur_ligne(ligne, info)

            donnees_dict[donnee['id_article']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
