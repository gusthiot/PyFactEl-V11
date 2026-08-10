from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Ciseau(CsvImport):
    """
    Classe pour l'importation des données de Ciseaux Horaires
    """

    cles = ['id_groupe', 'S1', 'alpha1', 'S2', 'alpha2', 'S3']
    nom_fichier = "ciseau.csv"
    libelle = "Ciseaux horaires"

    def __init__(self, dossier_source, groupes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param groupes: groupes importés
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}

        for donnee in self.donnees:
            msg += self.test_id_coherence(donnee['id_groupe'], "l'id groupe", ligne, groupes)
            groupe = groupes.donnees[donnee['id_groupe']]
            if groupe['cae'] != 'OUI':
                msg += self._erreur_ligne(ligne, "le groupe doit être de type CAE\n")
            donnee['S1'], info = Format.est_un_nombre(donnee['S1'], "S1 ", -1, 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['S2'], info = Format.est_un_nombre(donnee['S2'], "S2 ", -1, donnee['S1'])
            msg += self._erreur_ligne(ligne, info)
            donnee['S3'], info = Format.est_un_nombre(donnee['S3'], "S3 ", -1, donnee['S2'])
            msg += self._erreur_ligne(ligne, info)
            donnee['alpha1'], info = Format.est_un_nombre(donnee['alpha1'], "Alpha1 ", -1, 0, 100)
            msg += self._erreur_ligne(ligne, info)
            donnee['alpha2'], info = Format.est_un_nombre(donnee['alpha2'], "Alpha2 ", -1, 0, 100)
            msg += self._erreur_ligne(ligne, info)

            donnees_dict[donnee['id_groupe']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
