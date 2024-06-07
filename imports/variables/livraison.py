from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Livraison(CsvImport):
    """
    Classe pour l'importation des données de Livraisons
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_prestation', 'date_livraison', 'quantite',
            'id_operateur', 'id_livraison', 'date_commande', 'remarque', 'validation', 'id_staff']
    nom_fichier = "lvr.csv"
    libelle = "Livraison Prestations"

    def __init__(self, dossier_source, comptes, prestations, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param prestations: prestations importées
        :param users: users importés
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_list = []
        coms = []

        for donnee in self.donnees:
            donnee['mois'], info = Format.est_un_entier(donnee['mois'], "le mois ", 1, 12)
            msg += self._erreur_ligne(ligne, info)
            donnee['annee'], info = Format.est_un_entier(donnee['annee'], "l'annee ", 2000, 2099)
            msg += self._erreur_ligne(ligne, info)
            info = self.test_id_coherence(donnee['id_compte'], "l'id compte", ligne, comptes)
            if info == "" and donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])
            else:
                msg += info

            msg += self.test_id_coherence(donnee['id_prestation'], "l'id prestation", ligne, prestations)

            msg += self.test_id_coherence(donnee['id_user'], "l'id user", ligne, users)

            msg += self.test_id_coherence(donnee['id_operateur'], "l'id opérateur", ligne, users)

            msg += self.test_id_coherence(donnee['id_staff'], "l'id staff", ligne, users, True)

            donnee['quantite'], info = Format.est_un_nombre(donnee['quantite'], "la quantité", 1, 0)
            msg += self._erreur_ligne(ligne, info)

            donnee['date_livraison'], info = Format.est_une_date(donnee['date_livraison'], "la date de livraison")
            msg += self._erreur_ligne(ligne, info)
            donnee['date_commande'], info = Format.est_une_date(donnee['date_commande'], "la date de commande")
            msg += self._erreur_ligne(ligne, info)
            donnee['id_livraison'], info = Format.est_un_texte(donnee['id_livraison'], "l'id livraison")
            msg += self._erreur_ligne(ligne, info)
            donnee['remarque'], info = Format.est_un_texte(donnee['remarque'], "la remarque", True)
            msg += self._erreur_ligne(ligne, info)

            if donnee['validation'] not in ['0', '1', '2', '3']:
                msg += self._erreur_ligne(ligne, "la validation doit être parmi [0, 1, 2, 3]\n")

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
