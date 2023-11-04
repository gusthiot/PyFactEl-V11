from core import (Format,
                  DossierDestination)


class AnnexeAll(object):
    """
    Classe pour la création du csv d'annexe
    """

    cles = ['proj-nbr', 'proj-name', 'item-labelcode', 'user-name-f', 'date-start-y', 'date-start-m', 'date-end-y',
            'date-end-m', 'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'sum-deduct', 'total-fact']

    def __init__(self, imports, transactions_2, par_client, csv_fichiers, versions):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_2: transactions 2 générées
        :param par_client: sommes des transactions
        :param csv_fichiers: fichiers csv et nom du fichier zip par client
        :param versions: versions des factures générées
        """

        pt = imports.paramtexte.donnees
        self.csv_fichiers = csv_fichiers

        for code, pc in par_client.items():
            if code in versions.clients:
                client = imports.clients.donnees[code]
                nom_zip = ("Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(code) +
                           "_" + client['abrev_labo'] + ".zip")

                nom_csv = ("Annexe_all_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" +
                           client['abrev_labo'] + ".csv")

                lignes = []

                if code not in self.csv_fichiers:
                    self.csv_fichiers[code] = {'nom': nom_zip, 'fichiers': []}
                self.csv_fichiers[code]['fichiers'].append(nom_csv)

                for key in pc['transactions']:
                    trans = transactions_2.valeurs[key]
                    ligne = []
                    for cle in range(0, len(self.cles)):
                        ligne.append(trans[self.cles[cle]])
                    lignes.append(ligne)

                with DossierDestination(imports.chemin_cannexes).writer(nom_csv) as fichier_writer:
                    ligne = []
                    for cle in self.cles:
                        ligne.append(pt[cle])
                    fichier_writer.writerow(ligne)

                    for ligne in lignes:
                        fichier_writer.writerow(ligne)
