from core import (Format,
                  CsvBase,
                  DossierDestination)


class Annexe(CsvBase):
    """
    Classe pour la création du csv d'annexe
    """

    cles = ['proj-nbr', 'proj-name', 'item-labelcode', 'user-name-f', 'date-start-y', 'date-start-m', 'date-end-y',
            'date-end-m', 'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'sum-deduct', 'total-fact']

    def __init__(self, imports, transactions_2, par_fact, csv_fichiers, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2: transactions 2 générées
        :param par_fact: tri des transactions
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        :param versions: versions des factures générées
        """
        super().__init__(imports)
        self.csv_fichiers = csv_fichiers

        for id_fact in par_fact.keys():
            base = transactions_2.valeurs[par_fact[id_fact]['base']]
            code = base['client-code']
            if code in versions.clients:
                intype = base['invoice-type']
                client = imports.clients.donnees[code]
                nom_zip = ("Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(code) +
                           "_" + client['abrev_labo'] + ".zip")
                prefixe = ("Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version))

                lignes = []

                if intype == "GLOB":
                    nom_csv = prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_0.csv"
                else:
                    compte = imports.comptes.donnees[base['proj-id']]
                    nom_csv = (prefixe + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + compte['numero'] +
                               ".csv")

                if code not in self.csv_fichiers:
                    self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                self.csv_fichiers[code]['fichiers'].append(nom_csv)

                for pc in par_fact[id_fact]['projets'].values():
                    for key in pc['transactions']:
                        trans = transactions_2.valeurs[key]
                        ligne = []
                        for cle in range(0, len(self.cles)):
                            ligne.append(trans[self.cles[cle]])
                        lignes.append(ligne)

                self.write(nom_csv, DossierDestination(imports.chemin_cannexes), lignes)
