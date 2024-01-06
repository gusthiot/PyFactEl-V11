from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Granted(CsvImport):
    """
    Classe pour l'importation des données de Subsides comptabilisés
    """

    cles = ['proj-id', 'platf-code', 'item-idclass', 'subsid-alrdygrant']
    libelle = "Subsides comptabilisés"

    def __init__(self, dossier_source, edition, comptes, classprests, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param comptes: comptes importés
        :param classprests: classes prestations importées
        :param plateformes: plateformes importées
        """
        if edition.mois > 1:
            self.nom_fichier = "granted_" + str(edition.annee) + "_" + Format.mois_string(edition.mois-1) + ".csv"
        else:
            self.nom_fichier = "granted_" + str(edition.annee-1) + "_" + Format.mois_string(12) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        triplets = []

        for donnee in self.donnees:
            msg += self.test_id_coherence(donnee['proj-id'], "l'id compte", ligne, comptes)

            msg += self.test_id_coherence(donnee['item-idclass'], "l'id classe prestation", ligne, classprests)

            msg += self.test_id_coherence(donnee['platf-code'], "l'id plateforme", ligne, plateformes)

            triplet = [donnee['proj-id'], donnee['platf-code'], donnee['item-idclass']]
            if triplet not in triplets:
                triplets.append(triplet)
            else:
                msg += "Triplet type '" + donnee['proj-id'] + "' id plateforme '" + donnee['platf-code'] + \
                       "' et id classe prestation '" + donnee['item-idclass'] + "' de la ligne " + str(ligne) + \
                       " pas unique\n"

            donnee['subsid-alrdygrant'], info = Format.est_un_nombre(donnee['subsid-alrdygrant'],
                                                                     "le montant comptabilisé", ligne, 2, 0)
            msg += info

            donnees_dict[donnee['proj-id'] + donnee['platf-code'] + donnee['item-idclass']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
