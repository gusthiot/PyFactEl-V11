from core import (Format,
                  CsvDict)


class ClientsModifs(CsvDict):
    """
    Classe pour la création de la table des modifications des clients
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'client-code', 'client-sap', 'client-name',
            'client-name2', 'client-name3', 'client-ref', 'client-email', 'client-deliv', 'client-idclass']

    def __init__(self, imports, versions):
        """
        initialisation des données
        :param imports: données importées
        :param versions: versions nouvellement générées
        """
        super().__init__(imports)
        self.nom = "Clients-modifs_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"
        unique = 0

        for code in versions.clients_changes:
            if code in self.imports.clients_prev.donnees.keys():
                self._ajout(self.imports.clients_prev.donnees[code], unique)
            else:
                self._ajout_nul(code, unique)
            unique += 1
            if code in self.imports.clients.donnees.keys():
                self._ajout(self.imports.clients.donnees[code], unique)
            else:
                self._ajout_nul(code, unique)
            unique += 1

    def _ajout(self, client, unique):
        """
        ajout d'une ligne pour un client
        :param client: données du client
        :param unique: clé unique de la ligne
        """
        self._ajouter_valeur([self.imports.edition.annee, self.imports.edition.mois, self.imports.version,
                              client['code'], client['code_sap'], client['abrev_labo'], client['nom2'], client['nom3'],
                              client['ref'], client['email'], client['mode'], client['id_classe']], unique)

    def _ajout_nul(self, code, unique):
        """
        ajout d'une ligne pour un client non-existant
        :param code: code client
        :param unique: clé unique de la ligne
        """
        self._ajouter_valeur([self.imports.edition.annee, self.imports.edition.mois, self.imports.version, code,
                              "", "", "", "", "", "", "", ""], unique)
