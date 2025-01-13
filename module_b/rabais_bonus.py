from core import (Format,
                  CsvList)


class RabaisBonus(CsvList):
    """
    Classe pour la création du csv de report rabais bonus
    """

    cles = ['client-code', 'client-class', 'item-codeD', 'deduct-CHF', 'subsid-deduct', 'discount-bonus',
            'subsid-bonus']

    def __init__(self, imports, transactions_3, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_client: tri des transactions
        """
        super().__init__(imports)

        self.nom = ("rabaisbonus.csv")

        for par_code in par_client.values():
            for par_article in par_code['articles'].values():
                base = transactions_3.valeurs[par_article['base']]
                ligne = []
                for cle in range(0, len(self.cles)-4):
                    ligne.append(base[self.cles[cle]])
                ligne += [round(par_article['deduit'], 2), round(par_article['sub_ded'], 2),
                          round(par_article['remb'], 2), round(par_article['sub_remb'], 2)]
                self.lignes.append(ligne)
