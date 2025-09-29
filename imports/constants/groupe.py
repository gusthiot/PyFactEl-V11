from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Groupe(CsvImport):
    """
    Classe pour l'importation des données de Machines Cmi
    """

    cles = ['id_groupe', 'cae', 'item-id-K1', 'item-id-K2', 'item-id-K3', 'item-id-K4', 'item-id-K5', 'item-id-K6',
            'item-id-K7']
    nom_fichier = "groupe.csv"
    libelle = "Groupes de machines"

    def __init__(self, dossier_source, categories):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param categories: catégories importées
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_groupe'], info = Format.est_un_alphanumerique(donnee['id_groupe'], "l'id groupe")
            if info == "":
                if donnee['id_groupe'] not in ids:
                    ids.append(donnee['id_groupe'])
                else:
                    msg += self._erreur_ligne(ligne, "l'id groupe '" + donnee['id_groupe'] + "' n'est pas unique\n")
            else:
                msg += self._erreur_ligne(ligne, info)

            if donnee['cae'] != 'OUI' and donnee['cae'] != 'NON':
                msg += self._erreur_ligne(ligne, "le cae doit être OUI ou NON\n")

            cats = ['item-id-K1', 'item-id-K2', 'item-id-K3', 'item-id-K4', 'item-id-K5', 'item-id-K6', 'item-id-K7']
            noms = ['machine', 'opérateur', 'plateforme', 'onéreux', 'hp', 'hc', 'fixe']
            for ii in range(0, len(cats)):
                cat = cats[ii]
                nom = noms[ii]
                msg += self.test_id_coherence(donnee[cat], "l'id catégorie " + nom, ligne, categories, True)

            donnees_dict[donnee['id_groupe']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
