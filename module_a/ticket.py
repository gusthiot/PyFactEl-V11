from core import (Format, Chemin)
import json
import os


class Ticket(object):
    """
    Classe créant le JSON nécessaire à la génération des tickets
    """

    def __init__(self, imports, factures, par_client, versions, chemin_destination):
        """
        génère les tickets sous forme de sections html
        :param imports: données importées
        :param factures: factures générées
        :param par_client: tri des transactions 1
        :param versions: versions des factures générées
        :param chemin_destination: le dossier de sauvegarde du fichier
        """

        self.nom = "Ticket_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                   Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".html"

        self.sections = {}
        dict_ticket = {}

        textes = imports.paramtexte.donnees

        for code, par_client in par_client.items():
            if code in versions.clients:
                client = imports.clients.donnees[code]
                classe = imports.classes.donnees[client['id_classe']]

                if client['ref'] != "":
                    your_ref = textes['your-ref'] + client['ref']
                else:
                    your_ref = ""

                total = 0
                title = client['abrev_labo'] + " (" + str(code) + ")"
                dict_ticket[title] = {'code': code, 'abrev': client['abrev_labo'], 'nom2': client['nom2'],
                                      'nom3': client['nom3'], 'ref': your_ref, 'articles': {}, 'factures': {}}

                for ordre, par_article in sorted(par_client['articles'].items()):
                    article = imports.artsap.donnees[par_article['id']]
                    total += par_article['total']
                    description = article['code_d'] + " : " + str(article['code_sap'])
                    dict_ticket[title]['articles'][ordre] = {'descr': description, 'texte': article['texte_sap'],
                                                             'net': "%.2f" % par_article['total']}

                dict_ticket[title].update({'total': "%.2f" % total})

                nom_zip = "Annexes_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" + \
                          Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(code) + \
                          "_" + client['abrev_labo'] + ".zip"
                chemin_zip = imports.chemin_cannexes + "/" + nom_zip

                if os.path.isfile(chemin_zip):
                    dict_ticket[title].update({'nom_zip': nom_zip})

                if code in factures.par_client:
                    for id_fact, par_fact in factures.par_client[code].items():
                        reference = classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" + \
                            Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact)
                        dict_ticket[title]['factures'][id_fact] = {'ref': reference, 'postes': []}

                        total = 0
                        for dico_fact in par_fact['factures']:
                            dict_ticket[title]['factures'][id_fact]['postes'].append(dico_fact)
                            total += dico_fact['total']

                        dict_ticket[title]['factures'][id_fact].update({'total': "%.2f" % total})

                        if versions.valeurs[id_fact]['version-change'] == 'NEW' or \
                                versions.valeurs[id_fact]['version-change'] == 'CORRECTED':
                            prefixe_pdf = "Annexe_" + imports.plateforme['abrev_plat'] + "_" + \
                                          str(imports.edition.annee) + "_" + Format.mois_string(imports.edition.mois) \
                                          + "_" + str(par_fact['version'])
                            nom_pdf = prefixe_pdf + "_" + str(id_fact) + ".pdf"
                            chemin_pdf = imports.chemin_pannexes + "/" + nom_pdf

                            if os.path.isfile(chemin_pdf):
                                dict_ticket[title]['factures'][id_fact].update({'nom_pdf': nom_pdf})

        with open(Chemin.chemin([chemin_destination, "ticket.json"]), 'w') as outfile:
            json.dump(dict_ticket, outfile, indent=4)
