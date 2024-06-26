from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class Compte(CsvImport):
    """
    Classe pour l'importation des données de Comptes Cmi
    """

    cles = ['id_compte', 'numero', 'intitule', 'exploitation', 'code_client', 'type_subside']
    nom_fichier = "compte.csv"
    libelle = "Comptes"

    def __init__(self, dossier_source, clients, subsides):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param subsides: subsides importés
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            msg += self.test_id_coherence(donnee['code_client'], "le code client", ligne, clients)

            donnee['numero'], info = Format.est_un_alphanumerique(donnee['numero'], "le numéro de compte")
            msg += self._erreur_ligne(ligne, info)
            donnee['intitule'], info = Format.est_un_texte(donnee['intitule'], "l'intitulé")
            msg += self._erreur_ligne(ligne, info)
            donnee['id_compte'], info = Format.est_un_alphanumerique(donnee['id_compte'], "l'id compte")
            msg += self._erreur_ligne(ligne, info)
            if info == "":
                if donnee['id_compte'] not in ids:
                    ids.append(donnee['id_compte'])
                else:
                    msg += self._erreur_ligne(ligne, "l'id compte '" + donnee['id_compte'] + "' n'est pas unique\n")
            if donnee['exploitation'] != 'TRUE' and donnee['exploitation'] != 'FALSE':
                msg += self._erreur_ligne(ligne, "l'exploitation doit être 'TRUE' ou 'FALSE'\n")

            msg += self.test_id_coherence(donnee['type_subside'], "le type subside", ligne, subsides, True)

            donnee['numero'] = donnee['numero'][0:16]
            donnee['intitule'] = donnee['intitule'][0:120]

            donnees_dict[donnee['id_compte']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
