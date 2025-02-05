from core import (Format,
                  CsvBase,
                  DossierDestination)


class Details(CsvBase):
    """
    Classe pour la création du csv d'annexe détails
    """

    cles = ['transac-date', 'user-name-f', 'proj-nbr', 'proj-name', 'oper-name', 'oper-note', 'staff-note', 'mach-name',
            'item-grp', 'item-name', 'item-unit', 'transac-quantity', 'valuation-price', 'valuation-brut',
            'discount-type', 'discount-CHF', 'valuation-net', 'subsid-ok', 'subsid-CHF', 'total-fact', 'discount-bonus',
            'subsid-bonus']

    def __init__(self, imports, transactions_3, par_client, numeros, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_client: tri des transactions
        :param numeros: table des numéros de version
        :param versions: versions des factures générées
        """
        super().__init__(imports)
        self.csv_fichiers = {}

        for code, pc in par_client.items():
            if code in versions.clients:
                client = imports.clients.donnees[code]
                nom_zip = ("Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + code + "_" +
                           client['abrev_labo'] + ".zip")
                prefixe_csv = ("Details_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                               Format.mois_string(imports.edition.mois) + "_" + str(imports.version))

                for icf in pc['projets']:
                    tbtr = pc['projets'][icf]['transactions']
                    id_fact = numeros.couples[code][icf]
                    if icf == "0":
                        num = icf
                    else:
                        compte = imports.comptes.donnees[icf]
                        num = compte['numero']
                    nom_csv = prefixe_csv + "_" + str(id_fact) + "_" + client['abrev_labo'] + "_" + num + ".csv"
                    if code not in self.csv_fichiers:
                        self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                    self.csv_fichiers[code]['fichiers'].append(nom_csv)
                    lignes = []
                    for indice in tbtr:
                        val = transactions_3.valeurs[indice]
                        ligne = []
                        for cle in range(0, len(self.cles)):
                            if self.cles[cle] == 'user-name-f':
                                if val['user-first'] != "":
                                    ligne.append(val['user-name'] + " " + val['user-first'][0] + ".")
                                else:
                                    ligne.append(val['user-name'])
                            else:
                                ligne.append(val[self.cles[cle]])
                        lignes.append(ligne)

                    self.write(nom_csv, DossierDestination(imports.chemin_cannexes), lignes)
