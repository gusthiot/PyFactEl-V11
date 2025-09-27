from core import (CsvList,
                  DossierDestination)

class Statmach(CsvList):

    cles = ['mach-id', 'transac-runtime', 'runtime-N', 'runtime-avg', 'runtime-stddev']
    nom = "statmach.csv"


class Statoper(CsvList):

    cles = ['oper-sciper', 'date', 'flow-type', 'transac-usage']
    nom = "statoper.csv"


class Statlvr(CsvList):

    cles = ['client-code', 'user-sciper', 'item-id', 'transac-usage']
    nom = "statlvr.csv"


class Statsrv(CsvList):

    cles = ['client-code', 'client-class', 'item-text2K', 'oper-note', 'item-grp', 'item-codeK', 'transac-quantity',
            'transac-usage']
    nom = "statsrv.csv"



class Statnoshow(CsvList):

    cles = ['client-code', 'user-sciper', 'item-codeK', 'mach-id', 'transac-quantity']
    nom = "statnoshow.csv"


class Statcae(CsvList):

    cles = ['client-code', 'client-class', 'user-sciper', 'item-codeK', 'mach-id', 'transac-usage', 'transac-runcae']
    nom = "statcae.csv"


class Statpltf(CsvList):

    cles = ['proj-id', 'item-grp', 'item-codeK', 'transac-usage']
    nom = "statpltf.csv"


class Stattran(CsvList):

    cles = ['client-code', 'user-sciper', 'flow-type', 'transac-nbr']
    nom = "stattran.csv"


class Statdate(CsvList):

    cles = ['client-code', 'client-class', 'user-sciper', 'date']
    nom = "statdate.csv"


class Consopltf(CsvList):

    cles = ['proj-id', 'item-id', 'valuation-net']
    nom = "consopltf.csv"
    
class ReportFiles(object):

    def __init__(self, imports, sommes_3):

        self.imports = imports
        statcae = Statcae(imports)
        statdate = Statdate(imports)
        statsrv = Statsrv(imports)
        statlvr = Statlvr(imports)
        statnoshow = Statnoshow(imports)
        stattran = Stattran(imports)
        for code_client, par_client in sommes_3.par_client.items():
            for code_n, par_classe in par_client['classes'].items():
                for user_id, par_user in par_classe['users'].items():
                    if user_id != "0":
                        sciper = imports.users.donnees[user_id]['sciper']
                    else:
                        sciper = "0"
                    for machine_id, par_machine in par_user['machines'].items():
                        for item_k, usage in par_machine['items'].items():
                            nr = 0
                            if item_k == 'K1':
                                nr = par_machine['Nr']
                            statcae.lignes.append([code_client, code_n, sciper, item_k, machine_id,
                                                round(usage, 3), nr])

                    for date in par_user['dates']:
                        statdate.lignes.append([code_client, code_n, sciper, date])

                for text, par_text in par_classe['textes'].items():
                    for service, par_service in par_text.items():
                        for groupe_id, par_groupe in par_service.items():
                            for item_k, par_item in par_groupe.items():
                                statsrv.lignes.append([code_client, code_n, text, service, groupe_id, item_k,
                                                       round(par_item['quantity'], 3), round(par_item['usage'], 3)])

            for user_id, par_user in par_client['users'].items():
                if user_id != "0":
                    sciper = imports.users.donnees[user_id]['sciper']
                else:
                    sciper = "0"
                for item_id, usage in par_user['items'].items():
                    statlvr.lignes.append([code_client, sciper, item_id, round(usage, 3)])

                for machine_id, par_machine in par_user['machines'].items():
                    for item_k, quantity in par_machine.items():
                        statnoshow.lignes.append([code_client, sciper, item_k, machine_id, round(quantity, 3)])

                for flow, nb in par_user['flow'].items():
                    stattran.lignes.append([code_client, sciper, flow, nb])

        statoper = Statoper(imports)
        for flow, par_flow in sommes_3.par_flow.items():
            for oper_id, par_oper in par_flow.items():
                oper = imports.users.donnees[oper_id]
                for date, usage in par_oper.items():
                    statoper.lignes.append([oper['sciper'], date, flow, round(usage, 3)])

        statpltf = Statpltf(imports)
        consopltf = Consopltf(imports)
        for projet_id, par_projet in sommes_3.par_projet.items():
            for groupe_id, par_groupe in par_projet['groupes'].items():
                for item_k, usage in par_groupe.items():
                    statpltf.lignes.append([projet_id, groupe_id, item_k, round(usage, 3)])

            for item_id, par_item in par_projet['items'].items():
                if par_item['pltf'] > 0:
                    consopltf.lignes.append(([projet_id, item_id, round(par_item['pltf'], 2)]))

        self.save(statcae)
        self.save(statdate)
        self.save(statsrv)
        self.save(statlvr)
        self.save(statnoshow)
        self.save(stattran)
        self.save(statoper)
        self.save(statpltf)
        self.save(consopltf)

    def save(self, csv_list):
        csv_list.csv(DossierDestination(self.imports.chemin_report))
