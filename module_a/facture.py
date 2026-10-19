from core import (Format, Chemin)
import json


class Facture(object):
    """
    Classe contenant les méthodes nécessaires à la génération du JSON des factures
    """

    def __init__(self, imports, versions, par_fact, chemin_destination):
        """
        génère la facture sous forme de csv
        :param imports: données importées
        :param versions: versions des factures générées
        :param par_fact: tri des transactions 1
        :param chemin_destination: le dossier de sauvegarde des factures
        """

        self.par_client = {}

        textes = imports.paramtexte.donnees

        for id_fact, donnee in versions.valeurs.items():
            if donnee['version-change'] != 'CANCELED' and donnee['version-new-amount'] > 0:
                code = donnee['client-code']
                client = imports.clients.donnees[code]
                classe = imports.classes.donnees[client['id_classe']]
                if code not in self.par_client:
                    self.par_client[code] = {}
                self.par_client[code][id_fact] = {'factures': [], 'version': donnee['version-last']}

                code_sap = client['code_sap']

                if donnee['version-change'] != 'IDEM':

                    if classe['ref_fact'] == "INT":
                        genre = imports.facturation.code_int
                    else:
                        genre = imports.facturation.code_ext

                    if client['ref'] != "":
                        your_ref = textes['your-ref'] + client['ref']
                    else:
                        your_ref = ""

                    ref = (classe['ref_fact'] + "_" + str(imports.edition.annee) + "_" +
                           Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + "_" + str(id_fact))

                    dict_fact = {'SalesOrderType': genre, 'SalesOrganization': 1028, 'DistributionChannel': 20,
                                 'OrganizationDivision': 10, 'TransactionCurrency': imports.facturation.devise,
                                 'SoldToParty': code_sap, 'PurchaseOrderByCustomer': ref, 'SDDocumentReason': "TBD",
                                 'HeaderBillingBlockReason': "TBD"}

                    dict_fact['to_Partner'] = [
                        {'PartnerFunction': "ZM", 'Personnel': imports.plateforme['admin']},
                        {'PartnerFunction': "RE", 'Customer': code_sap, 'to_Address': [
                            {'EmailAddress': client['email'],'OrganizationName3': client['nom3']}
                        ]}
                    ]

                    dict_fact['to_Text'] = [{'LongTextID': "TX06", 'LongText': your_ref}]

                    """
                    nom = ("Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_"
                           + Format.mois_string(imports.edition.mois) + "_" + str(donnee['version-last']) + "_"
                           + str(id_fact) + ".pdf")

                    dict_fact['attachment'] = [{'filename': nom, 'filetype': "application/pdf",
                                                'filedescription': "Annexe PDF", 'filecontent': ""}]

                    if classe['grille'] == "OUI" and imports.plateforme['grille'] == "OUI":
                        dict_fact['attachment'].append({'filename': "grille.pdf", 'filetype': "application/pdf",
                                                        'filedescription': "Grille tarifaire PDF", 'filecontent': ""})
                    """

                    dict_fact['to_Item'] = []

                    for order, par_article in sorted(par_fact[id_fact]['articles'].items()):
                        article = imports.artsap.donnees[par_article['id']]
                        net = par_article['total']
                        code_op = (imports.plateforme['code_p'] + classe['code_n'] + str(imports.edition.annee) +
                                   Format.mois_string(imports.edition.mois) + article['code_d'])

                        dict_fact['to_Item'].append(
                            {'Material': article['code_sap'], 'SalesOrderItemText': article['intitule'],
                             'RequestedQuantity': article['quantite'], 'WBSElement': imports.plateforme['fonds'],
                             'ZZ1_CODEOP_SDI': code_op, 'to_PricingElement': [
                                {'ConditionType': "PPR0", 'ConditionRateValue': net}
                            ], 'to_Text': [
                                {'LongTextID': "TX02", 'LongText': article['texte_sap']}]
                             })

                    if imports.edition.filigrane == "":
                        with open(Chemin.chemin([chemin_destination, "facture_"+str(id_fact)+".json"]), 'w') as outfile:
                            json.dump(dict_fact, outfile, indent=4)

                inc = 1
                for id_compte, par_compte in par_fact[id_fact]['projets'].items():
                    nom = par_compte['numero']
                    poste = inc*10
                    for ordre, par_article in sorted(par_compte['items'].items()):
                        article = imports.artsap.donnees[par_article['id']]
                        net = par_article['total']
                        description = article['code_d'] + " : " + str(article['code_sap'])
                        self.par_client[code][id_fact]['factures'].append({'poste': poste, 'nom': nom,
                                                                           'descr': description,
                                                                           'texte': article['texte_sap'],
                                                                           'net': "%.2f" % net, 'total': net})
                        poste += 1
                    inc += 1

