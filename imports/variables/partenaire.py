from core import CsvImport
from core import (Interface,
                  ErreurConsistance)


class Partenaire(CsvImport):
    """
    Classe pour l'importation des données de Partenaires
    """

    cles = ['id_plateforme', 'code_client', 'id_classe']
    nom_fichier = "partenaire.csv"
    libelle = "Partenaires"

    def __init__(self, dossier_source, clients, plateformes, classes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param plateformes: plateformes importées
        :param classes: classes clients importées
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        couples = []

        for donnee in self.donnees:

            msg += self._test_id_coherence(donnee['id_plateforme'], "l'id plateforme", ligne, plateformes)

            msg += self._test_id_coherence(donnee['code_client'], "le code client", ligne, clients, True)

            msg += self._test_id_coherence(donnee['id_classe'], "l'id classe client", ligne, classes, True)

            couple = donnee['id_plateforme'] + donnee['code_client']

            if couple not in couples:
                couples.append(couple)
            else:
                msg += "le couple de la ligne " + str(ligne) + \
                       " n'est pas unique\n"

            donnees_dict[donnee['id_plateforme'] + donnee['code_client']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
