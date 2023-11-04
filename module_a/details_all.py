from core import (Format,
                  DossierDestination)


class DetailsAll(object):
    """
    Classe pour la création du csv d'annexe détails par client
    """

    cles = ['transac-date', 'user-name-f', 'proj-nbr', 'proj-name', 'oper-name', 'oper-note', 'staff-note', 'mach-name',
            'item-grp', 'item-name', 'item-unit', 'transac-quantity', 'valuation-price', 'valuation-brut',
            'discount-type', 'discount-CHF', 'valuation-net', 'subsid-ok', 'subsid-CHF', 'total-fact', 'discount-bonus',
            'subsid-bonus']

    def __init__(self, imports, transactions_3, par_client, csv_fichiers, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_client: tri des transactions
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        :param versions: versions des factures générées
        """

        pt = imports.paramtexte.donnees
        self.csv_fichiers = csv_fichiers

        for code, pc in par_client.items():
            if code in versions.clients:
                client = imports.clients.donnees[code]
                nom_zip = ("Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + code + "_" +
                           client['abrev_labo'] + ".zip")
                nom_csv = ("Details_all" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" +
                           client['abrev_labo'] + ".csv")
                if code not in self.csv_fichiers:
                    self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                self.csv_fichiers[code]['fichiers'].append(nom_csv)
                lignes = []

                for icf in pc['projets']:
                    tbtr = pc['projets'][icf]['transactions']
                    for indice in tbtr:
                        val = transactions_3.valeurs[indice]
                        ligne = []
                        for cle in range(0, len(self.cles)):
                            if self.cles[cle] == 'user-name-f':
                                ligne.append(val['user-name'] + " " + val['user-first'][0] + ".")
                            else:
                                ligne.append(val[self.cles[cle]])
                        lignes.append(ligne)

                with DossierDestination(imports.chemin_cannexes).writer(nom_csv) as fichier_writer:
                    ligne = []
                    for cle in self.cles:
                        ligne.append(pt[cle])
                    fichier_writer.writerow(ligne)

                    for ligne in lignes:
                        fichier_writer.writerow(ligne)
