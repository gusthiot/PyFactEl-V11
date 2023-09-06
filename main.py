# This Python file uses the following encoding: utf-8

"""
Fichier principal à lancer pour faire tourner le logiciel

"""
import datetime
import time
import traceback
import argparse
from core import (Interface,
                  Chemin,
                  DossierSource,
                  DossierDestination,
                  Latex)
from module_d import (Articles,
                      Tarifs,
                      Transactions3)
from module_c import (UserLaboNew,
                      BilanUsages,
                      BilanConsos,
                      StatMachine,
                      StatNbUser,
                      StatUser,
                      StatClient,
                      SommesUL,
                      Sommes3)
from module_b import (GrantedNew,
                      NumeroNew,
                      BilanSubsides,
                      BilanAnnules,
                      Transactions2New)
from module_a import (VersionNew,
                      Details,
                      AnnexeSubsides,
                      Sommes2,
                      Sommes1,
                      Modifications,
                      Annexe,
                      Transactions1,
                      BilanFactures,
                      Pdfs,
                      Journal,
                      Facture,
                      Total,
                      Ticket,
                      Sap,
                      Info,
                      ResultatNew)
from imports import (Edition,
                     Imports)

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--sansgraphiques", help="Pas d'interface graphique", action="store_true")
parser.add_argument("-e", "--entrees", help="Chemin des fichiers d'entrée")
parser.add_argument("-d", "--destination", help="Racine des sauvegardes")
parser.add_argument("-u", "--unique", help="Nom unique du dossier de sauvegarde")
parser.add_argument("-s", "--sciper", help="Sciper de la personne lançant la facturation")
parser.add_argument("-n", "--nopdf", help="Sans produire les pdfs", action="store_true")
args = parser.parse_args()

if args.sansgraphiques > 0:
    Interface.interface_graphique(False)

if args.nopdf > 0:
    with_pdf = False
else:
    with_pdf = True

if args.entrees:
    dossier_data = args.entrees
else:
    dossier_data = Interface.choisir_dossier()
dossier_source = DossierSource(dossier_data)

if args.destination:
    destination = args.destination
else:
    destination = "./"

if args.unique:
    unique = args.unique
else:
    unique = int(time.time())

if args.sciper:
    sciper = args.sciper
else:
    sciper = "000000"

try:
    if Chemin.existe(Chemin.chemin([dossier_data, Edition.nom_fichier])):
        start_time = time.time()

        imports = Imports(dossier_source, destination, unique)

        # Module D
        articles = Articles(imports)
        tarifs = Tarifs(imports)
        articles.csv(DossierDestination(imports.chemin_prix))
        tarifs.csv(DossierDestination(imports.chemin_prix))
        transactions_3 = Transactions3(imports, articles, tarifs)
        transactions_3.csv(DossierDestination(imports.chemin_bilans))

        # Module C
        sommes_3 = Sommes3(imports, transactions_3)
        usr_lab = UserLaboNew(imports, transactions_3, sommes_3.par_user)
        usr_lab.csv(DossierDestination(imports.chemin_out))
        sommes_ul = SommesUL(usr_lab, imports)
        bil_use = BilanUsages(imports, transactions_3, sommes_3.par_item)
        bil_use.csv(DossierDestination(imports.chemin_bilans))
        bil_conso = BilanConsos(imports, transactions_3, sommes_3.par_projet)
        bil_conso.csv(DossierDestination(imports.chemin_bilans))
        stat_nb_user = StatNbUser(imports, sommes_ul.par_ul)
        stat_nb_user.csv(DossierDestination(imports.chemin_bilans))
        stat_user = StatUser(imports, transactions_3, sommes_3.par_user)
        stat_user.csv(DossierDestination(imports.chemin_bilans))
        stat_cli = StatClient(imports, sommes_ul.par_ul, sommes_3.par_client)
        stat_cli.csv(DossierDestination(imports.chemin_bilans))
        stat_mach = StatMachine(imports, transactions_3, sommes_3.par_machine)
        stat_mach.csv(DossierDestination(imports.chemin_bilans))

        # Module B
        new_grants = GrantedNew(imports, transactions_3)
        new_grants.csv(DossierDestination(imports.chemin_out))
        new_numeros = NumeroNew(imports, transactions_3)
        new_numeros.csv(DossierDestination(imports.chemin_out))
        bil_subs = BilanSubsides(imports, transactions_3, sommes_3.par_client)
        bil_subs.csv(DossierDestination(imports.chemin_bilans))
        bil_annule = BilanAnnules(imports, sommes_3.par_client)
        bil_annule.csv(DossierDestination(imports.chemin_bilans))
        new_transactions_2 = Transactions2New(imports, transactions_3, sommes_3.par_client, new_numeros)
        new_transactions_2.csv(DossierDestination(imports.chemin_bilans))
        new_transactions_2.csv(DossierDestination(imports.chemin_out))

        # Module A
        sommes_2 = Sommes2(new_transactions_2)
        new_versions = VersionNew(imports, new_transactions_2, sommes_2)
        new_versions.csv(DossierDestination(imports.chemin_out))
        modifications = Modifications(imports, new_versions)
        modifications.csv(DossierDestination(imports.chemin_enregistrement))
        if imports.version > 0:
            journal = Journal(imports, new_versions, new_transactions_2)
            journal.csv(DossierDestination(imports.chemin_bilans))
        details = Details(imports, transactions_3, sommes_3.par_client, new_numeros, new_versions)
        ann_subs = AnnexeSubsides(imports, sommes_3.par_client, details.csv_fichiers, new_versions)
        annexes = Annexe(imports, new_transactions_2, sommes_2, ann_subs.csv_fichiers, new_versions)
        transactions_1 = Transactions1(imports, new_transactions_2, sommes_2, new_versions)
        transactions_1.csv(DossierDestination(imports.chemin_bilans))
        sommes_1 = Sommes1(transactions_1)
        bil_facts = BilanFactures(imports, transactions_1, sommes_1)
        bil_facts.csv(DossierDestination(imports.chemin_bilans))
        total = Total(imports, transactions_1, sommes_1, annexes.csv_fichiers, new_versions)
        Chemin.csv_files_in_zip(total.csv_fichiers, imports.chemin_cannexes)
        if with_pdf and Latex.possibles():
            pdfs = Pdfs(imports, new_transactions_2, sommes_2, new_versions)
        factures = Facture(imports, new_versions, sommes_1, sciper, imports.chemin_factures)
        tickets = Ticket(imports, factures, sommes_1, new_versions)
        tickets.creer_html(DossierDestination(imports.chemin_enregistrement))
        resultats = ResultatNew(imports)
        resultats.csv(DossierDestination(imports.chemin_out))
        sap = Sap(imports, new_versions, sommes_1)
        sap.csv(DossierDestination(imports.chemin_enregistrement))
        info = Info(imports)
        info.csv(DossierDestination(imports.chemin_enregistrement))

        Interface.affiche_message("OK " + str(imports.version) + " !!! (" +
                                  str(datetime.timedelta(seconds=(time.time() - start_time))).split(".")[0] + ")")
    else:
        Interface.affiche_message("Carnet d'ordre introuvable")
except Exception as e:
    Interface.fatal(traceback.format_exc(), "Erreur imprévue :\n")
