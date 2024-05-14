from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Categorie(CsvImport):
    """
    Classe pour l'importation des données de Catégories
    """

    cles = ['id_categorie', 'no_categorie', 'intitule', 'unite', 'id_plateforme', 'id_classe_prest']
    nom_fichier = "categorie.csv"
    libelle = "Catégories"

    def __init__(self, dossier_source, classprests, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param classprests: classes prestations importées
        :param plateformes: plateformes importées
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_categorie'], info = Format.est_un_alphanumerique(donnee['id_categorie'], "l'id catégorie", ligne)
            msg += info
            if info == "":
                if donnee['id_categorie'] not in ids:
                    ids.append(donnee['id_categorie'])
                else:
                    msg += "l'id catégorie '" + donnee['id_categorie'] + "' de la ligne " + str(ligne) +\
                           " n'est pas unique\n"

            msg += self.test_id_coherence(donnee['id_classe_prest'], "l'id classe prestation", ligne, classprests)
            if classprests.donnees[donnee['id_classe_prest']]['flag_coef'] == "OUI":
                msg += "le flag coef_prest de l'id classe prestation '" + donnee['id_classe_prest'] + \
                       "' de la ligne " + str(ligne) + "est à OUI et devrait être à NON\n"

            msg += plateformes.test_id(donnee['id_plateforme'])

            donnee['no_categorie'], info = Format.est_un_alphanumerique(donnee['no_categorie'], "le no catégorie",
                                                                        ligne)
            msg += info
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé", ligne)
            msg += info
            donnee['unite'], info = Format.est_un_texte(donnee['unite'], "l'unité", ligne)
            msg += info

            donnees_dict[donnee['id_categorie']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
