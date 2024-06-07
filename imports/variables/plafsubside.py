from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class PlafSubside(CsvImport):
    """
    Classe pour l'importation des données ded Plafonds de Subsides
    """

    nom_fichier = "plafsubside.csv"
    cles = ['id_subside', 'id_plateforme', 'id_classe_prest', 'pourcentage', 'max_mois', 'max_compte']
    libelle = "Plafonds Subsides"

    def __init__(self, dossier_source, subsides, classprests, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param subsides: subsides importés
        :param classprests: classes prestations importées
        :param plateformes: plateformes importées
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        triplets = []

        for donnee in self.donnees:
            msg += self.test_id_coherence(donnee['id_subside'], "l'id subside", ligne, subsides)

            msg += self.test_id_coherence(donnee['id_classe_prest'], "l'id classe prestation", ligne, classprests)

            msg += self._erreur_ligne(ligne, plateformes.test_id(donnee['id_plateforme']))

            triplet = [donnee['id_subside'], donnee['id_plateforme'], donnee['id_classe_prest']]
            if triplet not in triplets:
                triplets.append(triplet)
            else:
                msg += self._erreur_ligne(ligne, "Triplet id subside '" + donnee['id_subside'] + "' id plateforme '" +
                                          donnee['id_plateforme'] + "' et id classe prestation '" +
                                          donnee['id_classe_prest'] + "' pas unique\n")

            donnee['pourcentage'], info = Format.est_un_nombre(donnee['pourcentage'], "le pourcentage", 2, 0, 100)
            msg += self._erreur_ligne(ligne, info)
            donnee['max_mois'], info = Format.est_un_nombre(donnee['max_mois'], "le max mensuel", 2, 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['max_compte'], info = Format.est_un_nombre(donnee['max_compte'], "le max compte", 2, 0)
            msg += self._erreur_ligne(ligne, info)

            donnees_dict[donnee['id_subside'] + donnee['id_plateforme'] + donnee['id_classe_prest']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
