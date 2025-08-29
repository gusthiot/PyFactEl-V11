
class Sommes3(object):
    """
    Classe pour sommer les transactions 3 en fonction des clients et des plateformes
    """

    def __init__(self, imports, transactions_3):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        """
        self.par_client = {}
        self.par_item = {}
        self.par_user = {}
        self.par_machine = {}
        self.par_projet = {}
        self.par_flow = {}

        for key, transaction in transactions_3.valeurs.items():
            code_client = transaction['client-code']
            id_compte = transaction['proj-id']
            user_id = transaction['user-id']
            code_n = transaction['client-class']
            machine_id = transaction['mach-id']
            item_k = transaction['item-codeK']
            flow = transaction['flow-type']
            item_id = transaction['item-id']
            groupe_id = transaction['item-grp']
            plateforme_id = transaction['platf-code']
            exploitation = transaction['proj-expl']
            validation = transaction['transac-valid']
            date = transaction['transac-date']

            # Module B : mois de traitement = mois de facturation
            if (imports.edition.annee == transaction['invoice-year'] and
                    imports.edition.mois == transaction['invoice-month']):
                if code_client not in self.par_client.keys():
                    self.par_client[code_client] = {'articles': {}, 'projets': {}, 'comptes': {}, 'classes': {},
                                                    'users': {}, 'nb': 0, 'runs': 0, 'val_2': 0, 'val_3': 0}

                if validation == "2":
                    self.par_client[code_client]['val_2'] += transaction['valuation-net']
                if validation == "3":
                    self.par_client[code_client]['val_3'] += transaction['valuation-net']
                # => bilan annulés

                id_compte_fact = transaction['invoice-project']
                pcp = self.par_client[code_client]['projets']
                if id_compte_fact not in pcp.keys():
                    pcp[id_compte_fact] = {'comptes': {}, 'transactions': []}

                pcp[id_compte_fact]['transactions'].append(key)
                # => annexe details

                nbr = transaction['item-nbr']
                id_classe = transaction['item-idclass']
                if id_compte not in pcp[id_compte_fact]['comptes'].keys():
                    pcp[id_compte_fact]['comptes'][id_compte] = {}
                pcpc = pcp[id_compte_fact]['comptes'][id_compte]
                if id_classe not in pcpc.keys():
                    pcpc[id_classe] = {}
                pcpa = pcpc[id_classe]
                if nbr not in pcpa.keys():
                    pcpa[nbr] = {}
                if user_id not in pcpa[nbr].keys():
                    pcpa[nbr][user_id] = {'base': key, 'quantity': 0, 'deduct': 0, 'total': 0, 'start': date,
                                          'end': date}
                pcpa[nbr][user_id]['quantity'] += transaction['transac-quantity']
                pcpa[nbr][user_id]['deduct'] += transaction['deduct-CHF'] + transaction['subsid-deduct']
                pcpa[nbr][user_id]['total'] += transaction['total-fact']
                if date < pcpa[nbr][user_id]['start']:
                    pcpa[nbr][user_id]['start'] = date
                if date > pcpa[nbr][user_id]['end']:
                    pcpa[nbr][user_id]['end'] = date
                # => transactions 2

                pcc = self.par_client[code_client]['comptes']
                if id_compte not in pcc.keys():
                    pcc[id_compte] = {}
                pccd = pcc[id_compte]
                if id_classe not in pccd.keys():
                    pccd[id_classe] = {'subs': 0}
                if transaction['subsid-code'] != "" and transaction['subsid-maxproj'] > 0:
                    pccd[id_classe]['subs'] += transaction['subsid-CHF']
                # => annexe subsides

                code_d = transaction['item-codeD']
                pca = self.par_client[code_client]['articles']
                if code_d not in pca.keys():
                    pca[code_d] = {'base': key, 'avant': 0, 'compris': 0, 'deduit': 0, 'sub_ded': 0, 'fact': 0,
                                   'remb': 0, 'sub_remb': 0}
                pca[code_d]['avant'] += transaction['valuation-brut']
                pca[code_d]['compris'] += transaction['valuation-net']
                pca[code_d]['deduit'] += transaction['deduct-CHF']
                pca[code_d]['sub_ded'] += transaction['subsid-deduct']
                pca[code_d]['fact'] += transaction['total-fact']
                pca[code_d]['remb'] += transaction['discount-bonus']
                pca[code_d]['sub_remb'] += transaction['subsid-bonus']
                # => bilan subsides | rabais_bonus

            # Module C : mois de traitement = mois d'activité
            if (imports.edition.annee == date.year and
                    imports.edition.mois == date.month):

                if code_client not in self.par_client.keys():
                    self.par_client[code_client] = {'articles': {}, 'projets': {}, 'comptes': {}, 'classes': {},
                                                    'users': {}, 'nb': 0, 'runs': 0, 'val_2': 0, 'val_3': 0}
                self.par_client[code_client]['nb'] += 1
                if str(transaction['transac-runcae']) == "1":
                    self.par_client[code_client]['runs'] += 1
                # => stat client

                pccl = self.par_client[code_client]['classes']
                if code_n not in pccl.keys():
                    pccl[code_n] = {'users': {}, 'textes': {}}

                if plateforme_id != code_client and validation != "2":
                    pccu = pccl[code_n]['users']
                    if user_id not in pccu.keys():
                        pccu[user_id] = {'machines': {}, 'dates': []}

                    date_spl = date.date().isoformat()
                    pcud = pccu[user_id]['dates']
                    if date_spl not in pcud:
                        pcud.append(date_spl)
                    # par client/class/user
                    # => statdate

                if flow == 'cae':
                    pccu = pccl[code_n]['users']
                    if user_id not in pccu.keys():
                        pccu[user_id] = {'machines': {}, 'dates': []}

                    pccum = pccu[user_id]['machines']
                    if machine_id not in pccum.keys():
                        pccum[machine_id] = {'Nr': 0, "items": {}}
                    if str(transaction['transac-runcae']) == "1":
                        pccum[machine_id]['Nr'] += 1
                    if item_k not in pccum[machine_id]['items'].keys():
                        pccum[machine_id]['items'][item_k] = 0
                    pccum[machine_id]['items'][item_k] += transaction['transac-usage']
                    # par client/class/user/item K/machine
                    # => statcae

                if flow == 'srv':
                    text_k = transaction['item-text2K']
                    service = transaction['oper-note']
                    pct = pccl[code_n]['textes']
                    if text_k not in pct.keys():
                        pct[text_k] = {}
                    if service not in pct[text_k].keys():
                        pct[text_k][service] = {}
                    if groupe_id not in pct[text_k][service].keys():
                        pct[text_k][service][groupe_id] = {}
                    if item_k not in pct[text_k][service][groupe_id].keys():
                        pct[text_k][service][groupe_id][item_k] = {'quantity': 0, 'usage': 0}
                    pct[text_k][service][groupe_id][item_k]['quantity'] += transaction['transac-quantity']
                    pct[text_k][service][groupe_id][item_k]['usage'] += transaction['transac-usage']
                    # par client/class/text K/service/groupe/item K
                    # => statsrv

                pcu = self.par_client[code_client]['users']
                if user_id not in pcu.keys():
                    pcu[user_id] = {'items': {}, 'machines': {}, 'flow': {}}

                if flow == 'lvr':
                    pcui = pcu[user_id]['items']
                    if item_id not in pcui.keys():
                        pcui[item_id] = 0
                    pcui[item_id] += transaction['transac-usage']
                    # par client/user/item id
                    # => statlvr

                if flow == 'noshow' and plateforme_id != code_client:
                    pcum = pcu[user_id]['machines']
                    if machine_id not in pcum.keys():
                        pcum[machine_id] = {}
                    if item_k not in pcum[machine_id].keys():
                        pcum[machine_id][item_k] = 0
                    pcum[machine_id][item_k] += transaction['transac-quantity']
                    # par client/user/machine/item K
                    # => statnoshow

                if plateforme_id != code_client and validation != "2":
                    pcuf = pcu[user_id]['flow']
                    if flow not in pcuf.keys():
                        pcuf[flow] = 0
                    pcuf[flow] += 1
                    # par client/user/flow
                    # => stattran

                if flow in ['cae', 'srv'] and item_k == 'K2':
                    oper_id = transaction['oper-id']
                    date_spl = date.date().isoformat()
                    if flow not in self.par_flow.keys():
                        self.par_flow[flow] = {}
                    if oper_id not in self.par_flow[flow].keys():
                        self.par_flow[flow][oper_id] = {}
                    if date_spl not in self.par_flow[flow][oper_id].keys():
                        self.par_flow[flow][oper_id][date_spl] = 0
                    self.par_flow[flow][oper_id][date_spl] += transaction['transac-usage']
                    # par flow/oper-sciper/date
                    # => statoper

                if id_compte not in self.par_projet.keys():
                    self.par_projet[id_compte] = {'groupes': {}, 'items': {}}
                ppi = self.par_projet[id_compte]['items']
                if item_id not in ppi.keys():
                    ppi[item_id] = {'base': key, 'goops': 0, 'extrops': 0, 'goint': 0, 'extrint': 0, 'pltf': 0}
                net = transaction['valuation-net']

                if code_client == plateforme_id and validation != "2":
                    if transaction['item-extra'] == "TRUE":
                        if exploitation != "TRUE":
                            ppi[item_id]['extrint'] += net
                    else:
                        if exploitation == "TRUE":
                            ppi[item_id]['goops'] += net
                        else:
                            ppi[item_id]['goint'] += net
                if transaction['item-extra'] == "TRUE":
                    if ((code_client == plateforme_id and exploitation == "TRUE")
                            or validation == "2"):
                        ppi[item_id]['extrops'] += net
                # => bilan conso

                if (flow == 'lvr' and plateforme_id == code_client and transaction['item-flag-conso'] == "OUI"
                        and validation != "2"):
                        ppi[item_id]['pltf'] += net
                # par projet/item id
                # => consopltf

                if flow == 'cae' and plateforme_id == code_client and exploitation == "FALSE":
                    ppg = self.par_projet[id_compte]['groupes']
                    if groupe_id not in ppg.keys():
                        ppg[groupe_id] = {}
                    if item_k not in ppg[groupe_id].keys():
                        ppg[groupe_id][item_k] = 0
                    ppg[groupe_id][item_k] += transaction['transac-usage']
                    # par projet/groupe/ item K
                    # => statpltf

                if item_id not in self.par_item.keys():
                    self.par_item[item_id] = {'base': key, 'usage': 0, 'runtime': 0, 'nn': 0, 'rts': []}
                self.par_item[item_id]['usage'] += transaction['transac-usage']
                if transaction['transac-runtime'] != "":
                    rti = transaction['transac-runtime']
                    self.par_item[item_id]['runtime'] += rti
                    self.par_item[item_id]['nn'] += 1
                    self.par_item[item_id]['rts'].append(rti)
                # => bilan usage

                id_machine = transaction['mach-id']
                if id_machine not in self.par_machine.keys():
                    self.par_machine[id_machine] = {}
                pmi = self.par_machine[id_machine]
                if item_id not in pmi.keys():
                    pmi[item_id] = {'base': key, 'quantity': 0, 'usage': 0, 'runtime': 0, 'nn': 0, 'rts': []}
                pmi[item_id]['quantity'] += transaction['transac-quantity']
                pmi[item_id]['usage'] += transaction['transac-usage']
                run = transaction['transac-runtime']
                if run != "":
                    pmi[item_id]['runtime'] += run
                    pmi[item_id]['nn'] += 1
                    pmi[item_id]['rts'].append(run)
                # => stat machine | statmach

                if user_id not in self.par_user.keys():
                    self.par_user[user_id] = {}
                if code_client not in self.par_user[user_id].keys():
                    self.par_user[user_id][code_client] = {'days': {}, 'base': key, 'stat_trans': 0, 'stat_run': 0}
                puc = self.par_user[user_id][code_client]
                if user_id != "0":
                    puc['stat_trans'] += 1
                    if str(transaction['transac-runcae']) == "1":
                        puc['stat_run'] += 1
                    # => stat user

                day = date.day
                if day not in puc['days'].keys():
                    puc['days'][day] = key
                # => user labo
