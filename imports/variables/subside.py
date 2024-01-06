from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Subside(CsvImport):
    """
    Classe pour l'importation des données de Subsides
    """

    nom_fichier = "subside.csv"
    cles = ['id_subside', 'intitule', 'type', 'debut', 'fin']
    libelle = "Subsides"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_subside'], info = Format.est_un_alphanumerique(donnee['id_subside'], "le id subside", ligne)
            msg += info
            if info == "":
                if donnee['id_subside'] not in ids:
                    ids.append(donnee['id_subside'])
                else:
                    msg += "l'id de la ligne " + str(ligne) + " n'est pas unique\n"
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé", ligne)
            msg += info

            if donnee['type'] != 'MONO' and donnee['type'] != 'MULTI':
                msg += "le type de la ligne " + str(ligne) + " doit être MONO ou MULTI\n"
            if donnee['debut'] != 'NULL':
                donnee['debut'], info = Format.est_une_date(donnee['debut'], "la date de début", ligne)
                msg += info
            if donnee['fin'] != 'NULL':
                donnee['fin'], info = Format.est_une_date(donnee['fin'], "la date de fin", ligne)
                msg += info
            if donnee['debut'] != 'NULL' and donnee['fin'] != 'NULL':
                if donnee['debut'] > donnee['fin']:
                    msg += "la date de fin de la ligne " + str(ligne) + " doit être postérieure à la date de début"

            donnees_dict[donnee['id_subside']] = donnee

            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
