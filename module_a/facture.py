from core import (Format, Chemin)
import json
import base64


class Facture(object):
    """
    Classe contenant les méthodes nécessaires à la génération du JSON des factures
    """

    def __init__(self, imports, versions, sommes_1, sciper, chemin_destination):
        """
        génère la facture sous forme de csv
        :param imports: données importées
        :param versions: versions des factures générées
        :param sommes_1: sommes des transactions 1
        :param sciper: sciper de la personne lançant la facturation
        :param chemin_destination: le dossier de sauvegarde du fichier
        """

        self.par_client = {}

        textes = imports.paramtexte.donnees

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
                    dict_fact = {'execmode': "SIMU"}

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

                    dict_fact['header'] = {'ordertype': genre, 'ordernr': ref, 'currency': imports.facturation.devise,
                                           'clientnr': code_sap, 'distribution': client['mode'],
                                           'description': your_ref}
                    dict_fact['shipper'] = {'sciper': sciper, 'fund': imports.plateforme['fonds']}

                    lien = ("Annexe_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) + "_" +
                            Format.mois_string(imports.edition.mois) + "_" + str(donnee['version-last']) + "_" +
                            str(id_fact) + ".pdf")

                    with open(Chemin.chemin([imports.chemin_pannexes, lien]), "rb") as pdf:
                        annexe_base64 = base64.b64encode(pdf.read())

                    dict_fact['attachment'] = [{'filename': lien, 'filecontent': annexe_base64.decode('utf-8')}]

                    if classe['grille'] == "OUI":
                        grille = imports.plateforme['grille'] + '.pdf'
                        with open(Chemin.chemin([imports.dossier_source.chemin, grille]), "rb") as pdf:
                            grille_base64 = base64.b64encode(pdf.read())
                        dict_fact['attachment'].append({'filename': grille,
                                                        'filecontent': grille_base64.decode('utf-8')})

                    dict_fact['partner'] = {'clientnr': code_sap, 'name2': client['nom2'], 'name3': client['nom3'],
                                            'email': client['email']}

                    dict_fact['items'] = []

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
                            dict_fact['items'].append({'number': article['code_sap'], 'qty': article['quantite'],
                                                       'price': net, 'unit': article['unite'],
                                                       'text': article['texte_sap'],
                                                       'shipper_imputation': {'opcode': code_op},
                                                       'internalconsoname': nom})

                        description = article['code_d'] + " : " + str(article['code_sap'])
                        self.par_client[code][id_fact]['factures'].append({'poste': poste, 'nom': nom,
                                                                           'descr': description,
                                                                           'texte': article['texte_sap'],
                                                                           'net': "%.2f" % net, 'total': net,
                                                                           'compte': par_compte['numero']})
                        poste += 1
                    inc += 1

                if donnee['version-change'] == 'NEW' or donnee['version-change'] == 'CORRECTED':
                    if imports.edition.filigrane == "":
                        with open(Chemin.chemin([chemin_destination, "facture_"+str(id_fact)+".json"]), 'w') as outfile:
                            json.dump(dict_fact, outfile, indent=4)
