from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Overhead(CsvImport):
    """
    Classe pour l'importation des données de Overheads
    """

    cles = ['id_overhead', 'overhead_pc', 'id_article']
    nom_fichier = "overhead.csv"
    libelle = "Overheads"

    def __init__(self, dossier_source, artsap):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param artsap: articles SAP importés
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_overhead'], info = Format.est_un_alphanumerique(donnee['id_overhead'], "l'id overhead")
            msg += self._erreur_ligne(ligne, info)
            if info == "":
                if donnee['id_overhead'] not in ids:
                    ids.append(donnee['id_overhead'])
                else:
                    msg += self._erreur_ligne(ligne, "l'id overhead '" + donnee['id_overhead'] + "' n'est pas unique\n")

            msg += self.test_id_coherence(donnee['id_article'], "l'id article SAP", ligne, artsap)
            donnee['overhead_pc'], info = Format.est_un_nombre(donnee['overhead_pc'], "l'overhead", -1, 0, 100)
            msg += self._erreur_ligne(ligne, info)
            donnees_dict[donnee['id_overhead']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
