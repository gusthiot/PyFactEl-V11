from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Transactions2(CsvImport):
    """
    Classe pour l'importation des données des numéros de facture
    """

    cles = ['invoice-year', 'invoice-month', 'invoice-version', 'invoice-id', 'invoice-type', 'platf-name',
            'client-code', 'client-sap', 'client-name', 'client-idclass', 'client-class', 'client-labelclass',
            'proj-id', 'proj-nbr', 'proj-name', 'user-id', 'user-name-f', 'date-start-y', 'date-start-m', 'date-end-y',
            'date-end-m', 'item-idsap', 'item-codeD', 'item-order', 'item-labelcode', 'item-id', 'item-nbr',
            'item-name', 'transac-quantity', 'item-unit', 'valuation-price', 'sum-deduct', 'total-fact']
    libelle = "Transactions 2"

    def __init__(self, dossier_source, edition, plateforme, clients, comptes, users, articles, version):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param plateforme: plateforme traitée
        :param clients: clients importés
        :param comptes: comptes importés
        :param users: users importés
        :param articles: articles SAP importés
        :param version: version de facturation ciblée
        """
        self.nom_fichier = ("Transaction2_" + plateforme['abrev_plat'] + "_" + str(edition.annee) + "_" +
                            Format.mois_string(edition.mois) + "_" + str(version) + ".csv")
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = {}

        for donnee in self.donnees:
            donnee['invoice-year'], info = Format.est_un_entier(donnee['invoice-year'], "l'annee ", 2000, 2099)
            msg += self._erreur_ligne(ligne, info)
            donnee['invoice-month'], info = Format.est_un_entier(donnee['invoice-month'], "le mois ", 1, 12)
            msg += self._erreur_ligne(ligne, info)
            donnee['invoice-version'], info = Format.est_un_entier(donnee['invoice-version'], "la version", 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['invoice-id'], info = Format.est_un_entier(donnee['invoice-id'], "l'id facture", 1001)
            msg += self._erreur_ligne(ligne, info)
            if donnee['invoice-type'] not in ["GLOB", "CPTE"]:
                msg += self._erreur_ligne(ligne, "le type ne peut être que GLOB ou CPTE")
            donnee['platf-name'], info = Format.est_un_alphanumerique(donnee['platf-name'], "l'acronyme")
            msg += self._erreur_ligne(ligne, info)
            msg += self.test_id_coherence(donnee['client-code'], "le code client", ligne, clients)
            donnee['client-sap'], info = Format.est_un_alphanumerique(donnee['client-sap'], "le code client sap")
            msg += self._erreur_ligne(ligne, info)
            donnee['client-name'], info = Format.est_un_alphanumerique(donnee['client-name'], "le nom client")
            msg += self._erreur_ligne(ligne, info)
            donnee['client-idclass'], info = Format.est_un_alphanumerique(donnee['client-idclass'], "l'id classe")
            msg += self._erreur_ligne(ligne, info)
            donnee['client-class'], info = Format.est_un_alphanumerique(donnee['client-class'], "la classe")
            msg += self._erreur_ligne(ligne, info)
            donnee['client-labelclass'], info = Format.est_un_texte(donnee['client-labelclass'], "le label classe")
            msg += self._erreur_ligne(ligne, info)
            msg += self.test_id_coherence(donnee['proj-id'], "l'id compte", ligne, comptes)
            donnee['proj-nbr'], info = Format.est_un_alphanumerique(donnee['proj-nbr'], "le compte projet")
            msg += self._erreur_ligne(ligne, info)
            donnee['proj-name'], info = Format.est_un_texte(donnee['proj-name'], "l'intitulé de compte")
            msg += self._erreur_ligne(ligne, info)
            msg += self.test_id_coherence(donnee['user-id'], "l'id user", ligne, users, True)
            donnee['user-name-f'], info = Format.est_un_texte(donnee['user-name-f'], "le nom user", True)
            msg += self._erreur_ligne(ligne, info)
            if donnee['date-start-m'] != "":
                donnee['date-start-m'], info = Format.est_un_entier(donnee['date-start-m'], "le mois de départ",
                                                                    1, 12)
                msg += self._erreur_ligne(ligne, info)
            if donnee['date-start-y'] != "":
                donnee['date-start-y'], info = Format.est_un_entier(donnee['date-start-y'], "l'annee de départ",
                                                                    2000, 2099)
                msg += self._erreur_ligne(ligne, info)
            if donnee['date-end-m'] != "":
                donnee['date-end-m'], info = Format.est_un_entier(donnee['date-end-m'], "le mois de fin", 1, 12)
                msg += self._erreur_ligne(ligne, info)
            if donnee['date-end-y'] != "":
                donnee['date-end-y'], info = Format.est_un_entier(donnee['date-end-y'], "l'annee de fin", 2000,
                                                                  2099)
                msg += self._erreur_ligne(ligne, info)
            msg += self.test_id_coherence(donnee['item-idsap'], "l'id article SAP", ligne, articles)
            donnee['item-idsap'], info = Format.est_un_alphanumerique(donnee['item-idsap'], "l'id article")
            msg += self._erreur_ligne(ligne, info)
            donnee['item-codeD'], info = Format.est_un_alphanumerique(donnee['item-codeD'], "le code D")
            msg += self._erreur_ligne(ligne, info)
            donnee['item-order'], info = Format.est_un_entier(donnee['item-order'], "l'ordre", 1)
            msg += self._erreur_ligne(ligne, info)
            donnee['item-labelcode'], info = Format.est_un_texte(donnee['item-labelcode'], "l'intitulé article")
            msg += self._erreur_ligne(ligne, info)
            donnee['item-id'], info = Format.est_un_alphanumerique(donnee['item-id'], "l'item id")
            msg += self._erreur_ligne(ligne, info)
            donnee['item-nbr'], info = Format.est_un_texte(donnee['item-nbr'], "l'item nombre")
            msg += self._erreur_ligne(ligne, info)
            donnee['item-name'], info = Format.est_un_texte(donnee['item-name'], "l'item nom")
            msg += self._erreur_ligne(ligne, info)
            donnee['transac-quantity'], info = Format.est_un_nombre(donnee['transac-quantity'], "la quantité")
            msg += self._erreur_ligne(ligne, info)
            donnee['item-unit'], info = Format.est_un_texte(donnee['item-unit'], "l'item unité")
            msg += self._erreur_ligne(ligne, info)
            donnee['valuation-price'], info = Format.est_un_nombre(donnee['valuation-price'], "le prix unitaire", 2, 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['sum-deduct'], info = Format.est_un_nombre(donnee['sum-deduct'], "la déduction", 2)
            msg += self._erreur_ligne(ligne, info)
            donnee['total-fact'], info = Format.est_un_nombre(donnee['total-fact'], "le montant total", 2, 0)
            msg += self._erreur_ligne(ligne, info)
            if donnee['invoice-id'] not in ids:
                ids[donnee['invoice-id']] = donnee['client-code']
            else:
                if donnee['client-code'] != ids[donnee['invoice-id']]:
                    msg += self._erreur_ligne(ligne, "l'id facture '" + donnee['invoice-id'] +
                                              "' ne peut concerner 2 clients : " + ids[donnee['invoice-id']] + " et " +
                                              donnee['client-code'] + "\n")

            if donnee['invoice-year'] != edition.annee:
                msg += self._erreur_ligne(ligne, " mauvaise année\n")
            if donnee['invoice-month'] != edition.mois:
                msg += self._erreur_ligne(ligne, " mauvais mois\n")
            if donnee['invoice-version'] != version:
                msg += self._erreur_ligne(ligne, " mauvaise version\n")

            donnees_dict[ligne-1] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
