from core import CsvList


class Sap(CsvList):
    """
    Classe pour la création du fichier SAP
    """

    cles = ['client-name', 'invoice-id', 'total-fact', 'track-status', 'track-doc-nr', 'track-err-msg']

    def __init__(self, imports, versions, sommes_1):
        """
        initialisation des données
        :param imports: données importées
        :param versions: versions nouvellement générées
        :param sommes_1: sommes des transactions 1
        """
        super().__init__(imports)

        self.nom = "sap.csv"

        for donnee in versions.valeurs.values():
            if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                client = imports.clients.donnees[donnee['client-code']]
                total = sommes_1.par_fact[donnee['invoice-id']]['transactions']['total']

                ligne = [client['abrev_labo'], donnee['invoice-id'], total, "READY", "", ""]
                self.lignes.append(ligne)
