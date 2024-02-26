from core import Format
from imports.variables import Client


class ClientPrev(Client):
    """
    Classe pour l'importation des données des précédents Clients Cmi
    """
    def __init__(self, dossier_source, edition, facturation, classes, version):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param facturation: paramètres de facturation
        :param classes: classes clients importées
        :param version: version de facturation ciblée
        """
        self.nom_fichier = ("client_" + str(edition.annee) + "_" + Format.mois_string(edition.mois) +
                            "_" + str(version) + ".csv")
        super().__init__(dossier_source, facturation, classes)
