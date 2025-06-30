from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)
import math


class CategPrix(CsvImport):
    """
    Classe pour l'importation des données de Catégories Prix
    """

    nom_fichier = "categprix.csv"
    cles = ['id_classe', 'id_categorie', 'prix_unit']
    libelle = "Catégories Prix"

    def __init__(self, dossier_source, classes, categories):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param classes: classes clients importées
        :param categories: catégories importées
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        clas = []
        couples = []
        ids = []

        for donnee in self.donnees:
            info = self.test_id_coherence(donnee['id_classe'], "l'id classe client", ligne, classes)
            if info == "" and donnee['id_classe'] not in clas:
                clas.append(donnee['id_classe'])
            else:
                msg += self._erreur_ligne(ligne, info)

            info = self.test_id_coherence(donnee['id_categorie'], "l'id catégorie", ligne, categories)
            if info == "" and donnee['id_categorie'] not in ids:
                ids.append(donnee['id_categorie'])
            else:
                msg += self._erreur_ligne(ligne, info)

            if (donnee['id_categorie'] != "") and (donnee['id_classe'] != ""):
                couple = [donnee['id_categorie'], donnee['id_classe']]
                if couple not in couples:
                    couples.append(couple)
                else:
                    msg += self._erreur_ligne(ligne, "Couple id catégorie '" + donnee['id_categorie'] +
                                              "' et id classe '" + donnee['id_classe'] + "' pas unique\n")

            categorie = categories.donnees[donnee['id_categorie']]
            donnee['prix_unit'], info = Format.est_un_nombre(donnee['prix_unit'], "le prix unitaire ", categorie['nb_dec'], 0)
            msg += self._erreur_ligne(ligne, info)

            pow10 = math.pow(10, 9-categorie['nb_dec'])
            if donnee['prix_unit'] >= pow10:
                msg += self._erreur_ligne(ligne, "le prix unitaire doit être strictement inférieur à " + str(pow10))

            donnees_dict[donnee['id_classe'] + donnee['id_categorie']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        for id_classe in classes.donnees.keys():
            if id_classe not in clas:
                msg += self._erreur_fichier("L'id de classe '" + id_classe +
                                            "' dans les classes clients n'est pas présent dans les catégories prix\n")

        for id_cat in categories.donnees.keys():
            if id_cat not in ids:
                msg += self._erreur_fichier("L'id catégorie '" + id_cat +
                                            "' dans les catégories n'est pas présent dans les catégories prix\n")
        for id_cat in ids:
            for classe in clas:
                couple = [id_cat, classe]
                if couple not in couples:
                    msg += self._erreur_fichier("Couple id catégorie '" + id_cat +
                                                "' et id classe client '" + classe + "' n'existe pas\n")

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)
