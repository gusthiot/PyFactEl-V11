from core import CsvImport


class Sap(CsvImport):
    """
    Classe pour l'importation des données du précédent fichier SAP
    """

    cles = ['client-name', 'invoice-id', 'total-fact', 'track-status', 'track-doc-nr', 'track-err-msg']
    nom_fichier = "sap.csv"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        super().__init__(dossier_source)

        donnees_list = []

        for donnee in self.donnees:
            if donnee['track-status'] == 'ERROR':
                donnees_list.append(donnee['invoice-id'])

        self.donnees = donnees_list


