from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class UserLabo(CsvImport):
    """
    Classe pour l'importation des données des Utilisateurs des  laboratoires
    """

    cles = ['year', 'month', 'day', 'week-nbr', 'platf-code', 'client-code', 'user-id']
    libelle = "User labo"

    def __init__(self, dossier_source, edition, plateformes, clients, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param plateformes: plateformes importées
        :param clients: clients importés
        :param users: users importés
        """
        if edition.mois > 1:
            self.nom_fichier = "User-labo_" + str(edition.annee) + "_" + Format.mois_string(edition.mois-1) + ".csv"
        else:
            self.nom_fichier = "User-labo_" + str(edition.annee-1) + "_" + Format.mois_string(12) + ".csv"
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_list = []

        for donnee in self.donnees:
            donnee['year'], info = Format.est_un_entier(donnee['year'], "l'année", mini=2000, maxi=2099)
            msg += self._erreur_ligne(ligne, info)
            donnee['month'], info = Format.est_un_entier(donnee['month'], "le mois", mini=1, maxi=12)
            msg += self._erreur_ligne(ligne, info)

            msg += plateformes.test_id(donnee['platf-code'])

            msg += self.test_id_coherence(donnee['client-code'], "le code client", ligne, clients)

            msg += self.test_id_coherence(donnee['user-id'], "l'id user", ligne, users, True)

            donnees_list.append(donnee)
            ligne += 1

        self.donnees = donnees_list

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
