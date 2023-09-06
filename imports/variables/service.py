from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Service(CsvImport):
    """
    Classe pour l'importation des données de Services
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_groupe', 'date', 'duree_machine', 'duree_mo', 'id_op',
            'id_service', 'intitule', 'remarque_staff', 'validation', 'id_staff']
    nom_fichier = "srv.csv"
    libelle = "Services"

    def __init__(self, dossier_source, comptes, groupes, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param groupes: groupes importés
        :param users: users importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_list = []
        coms = []

        for donnee in self.donnees:
            donnee['mois'], info = Format.est_un_entier(donnee['mois'], "le mois ", ligne, 1, 12)
            msg += info
            donnee['annee'], info = Format.est_un_entier(donnee['annee'], "l'annee ", ligne, 2000, 2099)
            msg += info

            info = self.test_id_coherence(donnee['id_compte'], "l'id compte", ligne, comptes)
            if info == "" and donnee['id_compte'] not in coms:
                coms.append(donnee['id_compte'])
            else:
                msg += info

            msg += self.test_id_coherence(donnee['id_groupe'], "l'id groupe", ligne, groupes)

            msg += self.test_id_coherence(donnee['id_user'], "l'id user", ligne, users)

            msg += self.test_id_coherence(donnee['id_op'], "l'id opérateur", ligne, users)

            msg += self.test_id_coherence(donnee['id_staff'], "l'id staff", ligne, users, True)

            donnee['date'], info = Format.est_une_date(donnee['date'], "la date", ligne)
            msg += info

            donnee['duree_machine'], info = Format.est_un_nombre(donnee['duree_machine'], "la durée machine", ligne, 3,
                                                                 0)
            msg += info
            donnee['duree_mo'], info = Format.est_un_nombre(donnee['duree_mo'], "la durée main d'oeuvre", ligne, 3, 0)
            msg += info
            donnee['id_service'], info = Format.est_un_alphanumerique(donnee['id_service'], "l'id service", ligne)
            msg += info
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé service", ligne)
            donnee['remarque_staff'], info = Format.est_un_texte(donnee['remarque_staff'], "la remarque staff", ligne,
                                                                 True)
            msg += info

            if donnee['validation'] not in ['0', '1', '2', '3']:
                msg += "la validation " + str(ligne) + " doit être parmi [0, 1, 2, 3]"

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
