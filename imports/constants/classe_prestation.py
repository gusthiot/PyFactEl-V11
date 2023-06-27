from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class ClassePrestation(CsvImport):
    """
    Classe pour l'importation des données de Classes Prestations
    """

    cles = ['id_classe_prest', 'id_article', 'flag_coef', 'flag_usage', 'flag_conso', 'eligible', 'id_overhead']
    nom_fichier = "classeprestation.csv"
    libelle = "Classes Prestations"

    def __init__(self, dossier_source, artsap, overheads):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param artsap: articles SAP importés
        :param overheads: overheads importés
        """
        super().__init__(dossier_source)

        del self.donnees[0]
        msg = ""
        ligne = 1
        donnees_dict = {}
        ids = []

        for donnee in self.donnees:
            donnee['id_classe_prest'], info = Format.est_un_alphanumerique(donnee['id_classe_prest'],
                                                                           "l'id classe prestation", ligne)
            msg += info
            if info == "":
                if donnee['id_classe_prest'] not in ids:
                    ids.append(donnee['id_classe_prest'])
                else:
                    msg += "l'id classe prestation '" + donnee['id_classe_prest'] + "' de la ligne " + str(ligne) + \
                           " n'est pas unique\n"

            if donnee['flag_coef'] != 'OUI' and donnee['flag_coef'] != 'NON':
                msg += "le flag coeff_prest de la ligne " + str(ligne) + " doit être OUI ou NON\n"
            if donnee['flag_usage'] != 'OUI' and donnee['flag_usage'] != 'NON':
                msg += "le flag usage de la ligne " + str(ligne) + " doit être OUI ou NON\n"
            if donnee['flag_conso'] != 'OUI' and donnee['flag_conso'] != 'NON':
                msg += "le flag conso de la ligne " + str(ligne) + " doit être OUI ou NON\n"
            if donnee['eligible'] != 'OUI' and donnee['eligible'] != 'NON':
                msg += "l'éligible de la ligne " + str(ligne) + " doit être OUI ou NON\n"

            msg += self.test_id_coherence(donnee['id_article'], "l'id article SAP", ligne, artsap)

            msg += self.test_id_coherence(donnee['id_overhead'], "l'id overhead", ligne, overheads, True)

            donnees_dict[donnee['id_classe_prest']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            Interface.fatal(ErreurConsistance(), self.libelle + "\n" + msg)
