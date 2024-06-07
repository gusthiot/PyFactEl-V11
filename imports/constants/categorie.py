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

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_categorie'], info = Format.est_un_alphanumerique(donnee['id_categorie'], "l'id catégorie")
            msg += self._erreur_ligne(ligne, info)
            if info == "":
                if donnee['id_categorie'] not in ids:
                    ids.append(donnee['id_categorie'])
                else:
                    msg += self._erreur_ligne(ligne,
                                              "l'id catégorie '" + donnee['id_categorie'] + "' n'est pas unique\n")

            msg += self.test_id_coherence(donnee['id_classe_prest'], "l'id classe prestation", ligne, classprests)
            if classprests.donnees[donnee['id_classe_prest']]['flag_coef'] == "OUI":
                msg += self._erreur_ligne(ligne,
                                          "le flag coef_prest de l'id classe prestation '" +
                                          donnee['id_classe_prest'] + "' est à OUI et devrait être à NON\n")

            msg += self._erreur_ligne(ligne, plateformes.test_id(donnee['id_plateforme']))

            donnee['no_categorie'], info = Format.est_un_alphanumerique(donnee['no_categorie'], "le no catégorie")
            msg += self._erreur_ligne(ligne, info)
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé")
            msg += self._erreur_ligne(ligne, info)
            donnee['unite'], info = Format.est_un_texte(donnee['unite'], "l'unité")
            msg += self._erreur_ligne(ligne, info)

            donnees_dict[donnee['id_categorie']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
