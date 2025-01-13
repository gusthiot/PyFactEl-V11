from core import CsvList


class Montants(CsvList):
    """
    Classe pour la création du csv de report montants
    """

    cles = ['client-code', 'client-class', 'item-codeD', 'total-fact']

    def __init__(self, imports, par_client):
        """
        initialisation des données
        :param imports: données importées
        :param par_client: tri des transactions
        """
        super().__init__(imports)

        self.nom = ("montants.csv")

        for code, par_client in par_client.items():
            for ordre, par_article in sorted(par_client['articles'].items()):
                ligne = [code, par_article['classe'], par_article['code'], round(par_article['total'], 2)]
                self.lignes.append(ligne)