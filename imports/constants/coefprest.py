from core import CsvImport
from core import (Interface,
                  Format,
                  ErreurConsistance)


class CoefPrest(CsvImport):
    """
    Classe pour l'importation des données de Coefficients Prestations
    """

    cles = ['id_classe', 'id_classe_prest', 'coefficient']
    nom_fichier = "coeffprestation.csv"
    libelle = "Coefficients Prestations"

    def __init__(self, dossier_source, classes, classprests):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param classes: classes clients importées
        :param classprests: classes prestations importées
        """
        super().__init__(dossier_source)

        msg = ""
        ligne = 2
        donnees_dict = {}
        prests = []
        couples = []
        clas = []

        for donnee in self.donnees:
            info = self.test_id_coherence(donnee['id_classe'], "l'id classe client", ligne, classes)
            if info == "" and donnee['id_classe'] not in clas:
                clas.append(donnee['id_classe'])
            else:
                msg += self._erreur_ligne(ligne, info)
            info += self.test_id_coherence(donnee['id_classe_prest'], "l'id classe prestation", ligne, classprests)
            if info == "" and donnee['id_classe_prest'] not in prests:
                prests.append(donnee['id_classe_prest'])
            else:
                msg += self._erreur_ligne(ligne, info)

            couple = [donnee['id_classe'], donnee['id_classe_prest']]
            if couple not in couples:
                couples.append(couple)
            else:
                msg += self._erreur_ligne(ligne, "Couple id classe prestation '" + donnee['id_classe_prest'] +
                                          "' et id classe client '" + donnee['id_classe'] + "' pas unique\n")

            donnee['coefficient'], info = Format.est_un_nombre(donnee['coefficient'], "le coefficient", 2, 0)
            msg += self._erreur_ligne(ligne, info)

            donnees_dict[donnee['id_classe'] + donnee['id_classe_prest']] = donnee
            ligne += 1

        self.donnees = donnees_dict

        for id_classe in classes.donnees.keys():
            if id_classe not in clas:
                msg += self._erreur_fichier("L'id de classe '" + id_classe +
                                            "' dans les classes clients n'est pas présent dans "
                                            "les coefficients de prestations\n")

        for id_classprest, classprest in classprests.donnees.items():
            if classprest['flag_coef'] == "OUI":
                for id_classe in clas:
                    couple = [id_classe, id_classprest]
                    if couple not in couples:
                        msg += self._erreur_fichier("Couple id classe prestation '" + id_classprest +
                                                    "' et id classe client '" + id_classe + "' n'existe pas\n")

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)

    def contient_classprest(self, id_classprest):
        """
        vérifie si l'id de la classe prestation est présent
        :param id_classprest: l'id classe prestation à vérifier
        :return: True si présente, False sinon
        """
        for coefprest in self.donnees.values():
            if coefprest['id_classe_prest'] == id_classprest:
                return True
        return False
