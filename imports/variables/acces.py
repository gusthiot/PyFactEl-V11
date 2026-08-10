from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Acces(CsvImport):
    """
    Classe pour l'importation des données de Contrôle Accès Equipement
    """

    cles = ['annee', 'mois', 'id_compte', 'id_user', 'id_machine', 'date_login', 'dlog', 'dlog_hp', 'disable',
            't_mach', 'duree_operateur', 'id_op', 'remarque_op', 'remarque_staff', 'validation', 'id_staff']
    nom_fichier = "caelog.csv"
    libelle = "Log Contrôle Accès Equipement"

    def __init__(self, dossier_source, comptes, machines, users):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param comptes: comptes importés
        :param machines: machines importées
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
                msg += self._erreur_ligne(ligne, info)

            msg += self.test_id_coherence(donnee['id_machine'], "l'id machine", ligne, machines)

            msg += self.test_id_coherence(donnee['id_user'], "l'id user", ligne, users)

            msg += self.test_id_coherence(donnee['id_op'], "l'id opérateur", ligne, users)

            msg += self.test_id_coherence(donnee['id_staff'], "l'id staff", ligne, users, True)

            donnee['dlog'], info = Format.est_un_entier(donnee['dlog'], "le DLOG", 0)
            msg += info
            donnee['dlog_hp'], info = Format.est_un_entier(donnee['dlog_hp'], "le DLOG.HP", 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['disable'], info = Format.est_un_entier(donnee['disable'], "le disable S3 ", 0, 1)
            msg += self._erreur_ligne(ligne, info)
            donnee['t_mach'], info = Format.est_un_entier(donnee['t_mach'], "la durée du run", 0)
            msg += self._erreur_ligne(ligne, info)
            donnee['duree_operateur'], info = Format.est_un_entier(donnee['duree_operateur'], "la durée opérateur",
                                                                 0)
            msg += self._erreur_ligne(ligne, info)
            if donnee['dlog_hp'] > donnee['dlog']:
                msg += self._erreur_ligne(ligne, "le DLOG.HP ne peut pas être plus grand que DLOG")

            donnee['date_login'], info = Format.est_une_date(donnee['date_login'], "la date de login")
            msg += self._erreur_ligne(ligne, info)

            donnee['remarque_op'], info = Format.est_un_texte(donnee['remarque_op'], "la remarque opérateur", True)
            msg += self._erreur_ligne(ligne, info)

            donnee['remarque_staff'], info = Format.est_un_texte(donnee['remarque_staff'], "la remarque staff", True)
            msg += self._erreur_ligne(ligne, info)

            if donnee['validation'] not in ['0', '1', '2', '3']:
                msg += self._erreur_ligne(ligne, "la validation doit être parmi [0, 1, 2, 3]")

            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
