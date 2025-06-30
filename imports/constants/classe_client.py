from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class ClasseClient(CsvImport):
    """
    Classe pour l'importation des données de Classes Clients
    """

    cles = ['id_classe', 'code_n', 'intitule', 'ref_fact', 'avantage_HC', 'subsides', 'grille', 'id_overhead']
    nom_fichier = "classeclient.csv"
    libelle = "Classes Clients"

    def __init__(self, dossier_source, overheads):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param overheads: overheads importés
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_classe'], info = Format.est_un_alphanumerique(donnee['id_classe'], "l'id classe client")
            msg += self._erreur_ligne(ligne, info)
            if info == "":
                if donnee['id_classe'] not in ids:
                    ids.append(donnee['id_classe'])
                else:
                    msg += self._erreur_ligne(ligne,
                                              "l'id classe client '" + donnee['id_classe'] + "' n'est pas unique\n")

            donnee['code_n'], info = Format.est_un_alphanumerique(donnee['code_n'], "le code N")
            msg += self._erreur_ligne(ligne, info)
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé")
            msg += self._erreur_ligne(ligne, info)
            msg += self.test_id_coherence(donnee['id_overhead'], "l'id overhead", ligne, overheads, True)
            if donnee['ref_fact'] != 'INT' and donnee['ref_fact'] != 'EXT':
                msg += self._erreur_ligne(ligne, "le code référence client doit être INT ou EXT\n")
                if donnee['avantage_HC'] != 'BONUS' and donnee['avantage_HC'] != 'RABAIS':
                    msg += self._erreur_ligne(ligne, "l'avantage HC doit être BONUS ou RABAIS\n")
                if donnee['subsides'] != 'BONUS' and donnee['subsides'] != 'RABAIS':
                    msg += self._erreur_ligne(ligne, "le mode subsides doit être BONUS ou RABAIS\n")
            if donnee['grille'] != 'OUI' and donnee['grille'] != 'NON':
                msg += self._erreur_ligne(ligne, "la grille tarifaire doit être OUI ou NON\n")

            donnees_dict[donnee['id_classe']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
