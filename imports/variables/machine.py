from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Machine(CsvImport):
    """
    Classe pour l'importation des données de Machines Cmi
    """

    cles = ['annee', 'mois', 'id_machine', 'nom', 'id_groupe', 'tx_rabais_hc']
    nom_fichier = "machine.csv"
    libelle = "Machines"

    def __init__(self, dossier_source, groupes, edition):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param groupes: groupes importés
        :param edition: paramètres d'édition
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['mois'], info = Format.est_un_entier(donnee['mois'], "le mois ", 1, 12)
            msg += self._erreur_ligne(ligne, info)
            donnee['annee'], info = Format.est_un_entier(donnee['annee'], "l'annee ", 2000, 2099)
            msg += self._erreur_ligne(ligne, info)
            if donnee['mois'] != edition.mois or donnee['annee'] != edition.annee:
                msg += self._erreur_ligne(ligne, "date incorrecte\n")

            donnee['id_machine'], info = Format.est_un_alphanumerique(donnee['id_machine'], "l'id machine")
            if info == "":
                if donnee['id_machine'] not in ids:
                    ids.append(donnee['id_machine'])
                else:
                    msg += self._erreur_ligne(ligne, "l'id machine '" + donnee['id_machine'] + "' n'est pas unique\n")
            else:
                msg += self._erreur_ligne(ligne, info)

            msg += self.test_id_coherence(donnee['id_groupe'], "l'id groupe", ligne, groupes)

            donnee['tx_rabais_hc'], info = Format.est_un_nombre(donnee['tx_rabais_hc'], "le rabais heures creuses",
                                                                mini=0, maxi=100)
            msg += self._erreur_ligne(ligne, info)
            donnee['nom'], info = Format.est_un_texte(donnee['nom'], "le nom machine")
            msg += self._erreur_ligne(ligne, info)

            del donnee['annee']
            del donnee['mois']
            donnees_dict[donnee['id_machine']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
