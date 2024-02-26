from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Version(CsvImport):
    """
    Classe pour l'importation des données des versions de facture
    """

    cles = ['invoice-id', 'client-code', 'invoice-type', 'version-last', 'version-change', 'version-old-amount',
            'version-new-amount']
    libelle = "Versions de facture"

    def __init__(self, dossier_source, edition, version, module_a=False):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param version: version de facturation ciblée
        :param module_a: si on ne traite que le module A
        """
        self.nom_fichier = "Table-versions-factures_" + str(edition.annee) + "_" + Format.mois_string(edition.mois) + \
                           "_" + str(version) + ".csv"
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}

        for donnee in self.donnees:
            donnee['invoice-id'], info = Format.est_un_entier(donnee['invoice-id'], "l'id facture", ligne, 1001)
            msg += info

            if module_a:
                donnee['client-code'], info = Format.est_un_entier(donnee['client-code'], "le code client", ligne, 0)
            else:
                donnee['client-code'], info = Format.est_un_alphanumerique(donnee['client-code'], "le code client",
                                                                           ligne)
            msg += info

            donnee['version-last'], info = Format.est_un_entier(donnee['version-last'], "la version", ligne, 0)
            msg += info

            options = ['NEW', 'CANCELED', 'CORRECTED', 'IDEM', 'CLIENT']
            if donnee['version-change'] not in options:
                msg += ("le version-change de la ligne " + str(ligne) +
                        " doit être NEW, CANCELED, CORRECTED, IDEM ou CLIENT\n")

            donnee['version-old-amount'], info = Format.est_un_nombre(donnee['version-old-amount'], "l'ancien montant",
                                                                      ligne, 2, 0)
            msg += info
            donnee['version-new-amount'], info = Format.est_un_nombre(donnee['version-new-amount'],
                                                                      "le nouveau montant", ligne, 2, 0)
            msg += info

            if donnee['version-change'] == 'NEW' and donnee['version-old-amount'] != 0:
                msg += "pour un NEW, l'ancien montant doit être à 0 à la ligne " + str(ligne)
            if donnee['version-change'] == 'CANCELED' and donnee['version-new-amount'] != 0:
                msg += "pour un CANCELED, le nouveau montant doit être à 0 à la ligne " + str(ligne)
            if donnee['version-change'] == 'IDEM' and donnee['version-new-amount'] != donnee['version-old-amount']:
                msg += "pour un IDEM, le nouveau montant doit être égal à l'ancien à la ligne " + str(ligne)
            if donnee['version-change'] == 'CLIENT' and donnee['version-new-amount'] != donnee['version-old-amount']:
                msg += "pour un CLIENT, le nouveau montant doit être égal à l'ancien à la ligne " + str(ligne)

            donnees_dict[donnee['invoice-id']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
