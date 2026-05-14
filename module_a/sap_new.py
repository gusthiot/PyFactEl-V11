from core import CsvList
from imports.construits import Sap


class SapNew(CsvList):
    """
    Classe pour la création du fichier SAP
    """

    def __init__(self, imports, versions, par_fact):
        """
        initialisation des données
        :param imports: données importées
        :param versions: versions nouvellement générées
        :param par_fact: tri des transactions 1
        """
        super().__init__(imports)
        self.cles = Sap.cles
        self.nom = Sap.nom_fichier

        for donnee in versions.valeurs.values():
            if donnee['version-change'] != 'CANCELED' and donnee['version-new-amount'] > 0:
                if donnee['version-change'] != 'IDEM':
                    client = imports.clients.donnees[donnee['client-code']]
                    total = par_fact[donnee['invoice-id']]['transactions']['total']
                    ligne = [client['abrev_labo'], donnee['invoice-id'], round(2*total, 1)/2, "READY", "", ""]
                    self.lignes.append(ligne)
