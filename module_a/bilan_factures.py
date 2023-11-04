from core import (Format,
                  CsvList)


class BilanFactures(CsvList):
    """
    Classe pour la création du bilan des factures
    """

    cles = ['invoice-year', 'invoice-month', 'version-last', 'invoice-id', 'invoice-ref', 'platf-name',
            'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass',
            'total-fact']

    def __init__(self, imports, transactions_1, par_fact):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_1: transactions 1 générées
        :param par_fact: tri des transactions
        """
        super().__init__(imports)

        self.nom = "Bilan-factures_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + \
                   "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv"

        for id_fact in par_fact.keys():
            pf = par_fact[id_fact]['transactions']['keys']
            base = transactions_1.valeurs[pf[0]]
            total = par_fact[id_fact]['transactions']['total']

            ligne = []
            for cle in self.cles:
                if cle == 'total-fact':
                    ligne.append(round(2*total, 1)/2)
                else:
                    ligne.append(base[cle])
            self.lignes.append(ligne)
