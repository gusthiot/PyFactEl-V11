from core import (Format,
                  ErreurConsistance,
                  Interface,
                  CsvDict)
from imports.construits import Transactions2


class Transactions2New(CsvDict):
    """
    Classe pour la création des transactions de niveau 2
    """

    def __init__(self, imports, transactions_3=None, par_client=None, numeros=None):
        """
        initialisation des données
        :param imports: données importées
        :param transactions_3: transactions 3 générées
        :param par_client: tri des transactions
        :param numeros: table des numéros de version
        """
        super().__init__(imports)

        self.nom = ("Transaction2_" + imports.plateforme['abrev_plat'] + "_" + str(imports.edition.annee) +
                    "_" + Format.mois_string(imports.edition.mois) + "_" + str(imports.version) + ".csv")
        self.cles = Transactions2.cles

        i = 0
        if par_client is not None and transactions_3 is not None and numeros is not None:
            for code, par_code in par_client.items():
                for icf in par_code['projets']:
                    par_fact = par_code['projets'][icf]
                    id_fact = numeros.couples[code][icf]
                    for id_compte, par_compte in sorted(par_fact['comptes'].items()):
                        for id_classprest, par_classprest in sorted(par_compte.items()):
                            somme_classe = 0
                            classprest = imports.classprests.donnees[id_classprest]
                            base = None
                            for nbr, par_item in par_classprest.items():
                                for par_user in par_item.values():
                                    if par_user['quantity'] != 0:
                                        ligne = [imports.edition.annee, imports.edition.mois, imports.version, id_fact]
                                        base = transactions_3.valeurs[par_user['base']]
                                        if base['invoice-project'] == "0":
                                            ligne.append("GLOB")
                                        else:
                                            ligne.append("CPTE")
                                        for cle in range(5, 16):
                                            ligne.append(base[self.cles[cle]])
                                        if base['user-first'] != "":
                                            ligne.append(base['user-name'] + " " + base['user-first'][0] + ".")
                                        else:
                                            ligne.append(base['user-name'])
                                        ligne += [par_user['start'].year, par_user['start'].month, par_user['end'].year,
                                                  par_user['end'].month, classprest['id_article']]
                                        for cle in range(22, 28):
                                            ligne.append(base[self.cles[cle]])
                                        total_fact = round(2*par_user['total'], 1)/2
                                        ligne += [round(par_user['quantity'], 3), base['item-unit'],
                                                  base['valuation-price'], round(par_user['deduct'], 2), total_fact]
                                        self._ajouter_valeur(ligne, i)
                                        somme_classe += total_fact
                                        i += 1
                            if somme_classe > 0 and classprest['id_overhead'] != "0" and base is not None:
                                classe = imports.classes.donnees[base['client-idclass']]
                                if classe['overhead'] > 0:
                                    ligne = [imports.edition.annee, imports.edition.mois, imports.version, id_fact]
                                    overhead = imports.overheads.donnees[classprest['id_overhead']]
                                    artsap = imports.artsap.donnees[overhead['id_article']]
                                    if base['invoice-project'] == "0":
                                        ligne.append("GLOB")
                                    else:
                                        ligne.append("CPTE")
                                    for cle in range(5, 15):
                                        ligne.append(base[self.cles[cle]])
                                    ligne += ["0", "", "", "", "", "", overhead['id_article'], artsap['code_d'],
                                              artsap['ordre'], artsap['intitule'], classprest['id_overhead'],
                                              overhead['no_overhead'], overhead['intitule'], round(somme_classe, 2), "%",
                                              classe['overhead'], 0, round(2*somme_classe * classe['overhead'] / 100, 1)/2]
                                    self._ajouter_valeur(ligne, i)
                                    i += 1

        elif imports.data is not None:
            for donnee in imports.data.donnees:
                if (imports.edition.annee == donnee['invoice-year'] and
                        imports.edition.mois == donnee['invoice-month']):
                    code = donnee['client-code']
                    client = imports.clients.donnees[code]
                    id_classe = client['id_classe']
                    classe = imports.classes.donnees[id_classe]
                    id_article = donnee['item-idsap']
                    article = imports.artsap.donnees[id_article]
                    if imports.edition.plateforme == code:
                        montant = 0
                    else:
                        montant = donnee['transac-quantity'] * donnee['valuation-price'] - donnee['deduct-CHF']
                    ligne = [imports.edition.annee, imports.edition.mois, imports.version, code, "GLOB",
                             imports.plateforme['abrev_plat'], code, client['code_sap'], client['abrev_labo'],
                             id_classe, classe['code_n'], classe['intitule'], donnee['proj-id'], donnee['proj-nbr'],
                             donnee['proj-name'], donnee['user-id'], donnee['user-name'], donnee['date-start-y'],
                             donnee['date-start-m'], donnee['date-end-y'], donnee['date-end-m'], id_article,
                             article['code_d'], article['ordre'], article['intitule'], donnee['item-id'],
                             donnee['item-nbr'], donnee['item-name'], round(donnee['transac-quantity'], 3),
                             donnee['item-unit'], donnee['valuation-price'], donnee['deduct-CHF'],
                             round(2*montant, 1)/2]
                    self._ajouter_valeur(ligne, i)
                    i += 1
        else:
            Interface.fatal(ErreurConsistance(), "Il y a comme un problème dans Transactions 2 !")
