from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)
import re


class Client(CsvImport):
    """
    Classe pour l'importation des données de Clients Cmi
    """

    cles = ['code', 'code_sap', 'abrev_labo', 'nom2', 'nom3', 'ref', 'email', 'mode', 'id_classe']
    nom_fichier = "client.csv"
    libelle = "Clients"

    def __init__(self, dossier_source, facturation, classes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param facturation: paramètres de facturation
        :param classes: classes clients importées
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        codes = []

        for donnee in self.donnees:
            donnee['code_sap'], info = Format.est_un_alphanumerique(donnee['code_sap'], "le code client sap")
            msg += self._erreur_ligne(ligne, info)

            donnee['code'], info = Format.est_un_alphanumerique(donnee['code'], "le code client")
            msg += self._erreur_ligne(ligne, info)
            if info == "":
                if donnee['code'] not in codes:
                    codes.append(donnee['code'])
                else:
                    msg += self._erreur_ligne(ligne, "le code client '" + donnee['code'] + "' n'est pas unique\n")

            donnee['abrev_labo'], info = Format.est_un_alphanumerique(donnee['abrev_labo'], "l'abrev. labo")
            msg += self._erreur_ligne(ligne, info)
            donnee['nom2'], info = Format.est_un_texte(donnee['nom2'], "le nom 2", True)
            msg += self._erreur_ligne(ligne, info)
            donnee['nom3'], info = Format.est_un_texte(donnee['nom3'], "le nom 3", True)
            msg += self._erreur_ligne(ligne, info)
            donnee['ref'], info = Format.est_un_texte(donnee['ref'], "la référence", True)
            msg += self._erreur_ligne(ligne, info)

            if donnee['id_classe'] == "":
                msg += self._erreur_ligne(ligne, "le type de labo ne peut être vide\n")
            else:
                if not donnee['id_classe'] in classes.donnees.keys():
                    msg += self._erreur_ligne(ligne, "le type de labo '" + donnee['id_classe'] +
                                              "' n'existe pas dans les types N\n")
                else:
                    av_hc = classes.donnees[donnee['id_classe']]['avantage_HC']
                    donnee['rh'] = 1
                    donnee['bh'] = 0
                    if av_hc == 'BONUS':
                        donnee['bh'] = 1
                        donnee['rh'] = 0

            if (donnee['mode'] != "") and (donnee['mode'] not in facturation.modes):
                msg += self._erreur_ligne(ligne, "le mode d'envoi '" + donnee['mode'] +
                                          "' n'existe pas dans les modes d'envoi généraux\n")

            if (donnee['mode'] == "MAIL") and (not re.match("[^@]+@[^@]+\.[^@]+", donnee['email'])):
                msg += self._erreur_ligne(ligne, "le format de l'e-mail '" + donnee['email'] + "' n'est pas correct\n")

            donnees_dict[donnee['code']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
