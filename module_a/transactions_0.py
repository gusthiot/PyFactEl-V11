from core import (Format,
                  CsvDict)


class Transactions0(CsvDict):
    """
    Classe pour la création des transactions de niveau 0
    """

    cles = ['invoice-year', 'invoice-month', 'version-last', 'invoice-id', 'invoice-ref', 'invoice-type',
            'platf-name', 'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class',
            'client-labelclass', 'item-idsap', 'item-codeD', 'item-order', 'item-labelcode', 'total-fact']

    def __init__(self, imports, transactions_1, par_fact, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_1: transactions 1 générées
        :param par_fact: tri des transactions
        :param versions: versions des factures générées
        """
        super().__init__(imports)

        self.nom = ("Transaction0_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) +
                    "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv")

        i = 0
        for id_fact, par_fact in par_fact.items():
            version = versions.valeurs[id_fact]['version-last']
            for order, par_article in sorted(par_fact['articles'].items()):
                total = par_article['total']
                if total != 0:
                    base = transactions_1.valeurs[par_article['base']]
                    ligne = []
                    code = base['client-code']
                    client = imports.clients.donnees[code]
                    id_classe = imports.id_classe(client)
                    classe = imports.classes.donnees[id_classe]
                    ref = (classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(version) + "_" + str(id_fact))
                    for cle in self.cles:
                        if cle == 'invoice-ref':
                            ligne.append(ref)
                        elif cle == 'total-fact':
                            ligne.append(round(2*total, 1)/2)
                        elif cle == 'version-last':
                            ligne.append(version)
                        else:
                            ligne.append(base[cle])
                    self._ajouter_valeur(ligne, i)
                    i += 1
