from core import (Format, Chemin)
import json


class Facture(object):
    """
    Classe contenant les méthodes nécessaires à la génération du JSON des factures
    """

    def __init__(self, imports, versions, sommes_1, sciper):
        """
        génère la facture sous forme de csv
        :param imports: données importées
        :param versions: versions des factures générées
        :param sommes_1: sommes des transactions 1
        :param sciper: sciper de la personne lançant la facturation
        """

        self.nom = "facture.json"

        self.par_client = {}

        textes = imports.paramtexte.donnees

        self.dict_fact = {}

        for id_fact, donnee in versions.valeurs.items():
            if donnee['version-change'] != 'CANCELED' and donnee['version-new-amount'] > 0:
                code = donnee['client-code']
                intype = donnee['invoice-type']
                client = imports.clients.donnees[code]
                classe = imports.classes.donnees[client['id_classe']]
                if code not in self.par_client:
                    self.par_client[code] = {}
                self.par_client[code][id_fact] = {'factures': [], 'intype': intype, 'version': donnee['version-last']}

                code_sap = client['code_sap']

                if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                    self.dict_fact[id_fact] = {}
                    sdf = self.dict_fact[id_fact]
                    sdf['execmode'] = "SIMU"

                    if classe['ref_fact'] == "INT":
                        genre = imports.facturation.code_int
                    else:
                        genre = imports.facturation.code_ext

                    if client['ref'] != "":
                        your_ref = textes['your-ref'] + client['ref']
                    else:
                        your_ref = ""

                    ref = classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" + \
                        Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact)

                    sdf['header'] = {'ordertype': genre, 'ordernr': ref, 'currency': imports.facturation.devise,
                                     'clientnr': code_sap, 'distribution': client['mode'], 'description': your_ref}
                    sdf['shipper'] = {'sciper': sciper, 'fund': imports.plateforme['fonds']}

                    if classe['grille'] == "OUI":
                        grille = imports.plateforme['grille'] + '.pdf'
                    else:
                        grille = ""

                    lien = ("Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                            Format.mois_string(imports.edition.mois) + "_" + str(donnee['version-last']) + "_" +
                            str(id_fact) + ".pdf")

                    sdf['attachment'] = [{'filename': lien}, {'filename': grille}]

                    sdf['partner'] = {'clientnr': code_sap, 'name2': client['nom2'], 'name3': client['nom3'],
                                      'email': client['email']}

                    sdf['items'] = []

                inc = 1
                # date_dernier = str(imports.edition.annee) + Format.mois_string(imports.edition.mois) + \
                #     str(imports.edition.dernier_jour)
                for id_compte, par_compte in sommes_1.par_fact[id_fact]['projets'].items():
                    nom = par_compte['numero']
                    poste = inc*10
                    for ordre, par_article in sorted(par_compte['items'].items()):
                        article = imports.artsap.donnees[par_article['id']]
                        net = par_article['total']
                        code_op = imports.plateforme['code_p'] + classe['code_n'] + str(imports.edition.annee) + \
                            Format.mois_string(imports.edition.mois) + article['code_d']

                        if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                            sdf['items'].append({'number': article['code_sap'], 'qty': article['quantite'],
                                                 'price': net, 'unit': article['unite'], 'text': article['texte_sap'],
                                                 'shipper_imputation': {'opcode': code_op}, 'internalconsoname': nom})

                        description = article['code_d'] + " : " + str(article['code_sap'])
                        self.par_client[code][id_fact]['factures'].append({'poste': poste, 'nom': nom,
                                                                           'descr': description,
                                                                           'texte': article['texte_sap'],
                                                                           'net': "%.2f" % net, 'total': net,
                                                                           'compte': par_compte['numero']})
                        poste += 1
                    inc += 1

    def json(self, chemin_destination):
        """
        création du fichier json à partir d'un dictionnaire de valeurs
        :param chemin_destination: le dossier de sauvegarde du fichier
        """

        with open(Chemin.chemin([chemin_destination, self.nom]), 'w') as outfile:
            json.dump(self.dict_fact, outfile, indent=4)
