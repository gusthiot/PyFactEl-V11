from core import (Interface,
                  Format,
                  ErreurConsistance)


class Paramtexte(object):
    """
     Classe pour les labels, vérifiée par l'interface web
     """

    nom_fichier = "paramtext.csv"
    libelle = "Paramètres de Texte"

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        fichier_reader = dossier_source.reader(self.nom_fichier)
        self.donnees = {}
        try:
            for ligne in fichier_reader:
                if len(ligne) != 2:
                    Interface.fatal(ErreurConsistance(),
                                    self.libelle + " (" + self.nom_fichier + ") : nombre de colonnes incorrect : " +
                                    str(len(ligne)) +
                                    ", attendu : 2. Vérifier que les champs ne contiennent pas de point-virgule.")

                ligne[0], err = Format.est_un_alphanumerique(ligne[0], "le label", chevrons=True)
                if err != "":
                    Interface.fatal(ErreurConsistance(), self.libelle + " (" + self.nom_fichier + ") : " + err)

                ligne[1], err = Format.est_un_texte(ligne[1], "l'entête")
                if err != "":
                    Interface.fatal(ErreurConsistance(), self.libelle + " (" + self.nom_fichier +
                                    ") : pour le label '" + ligne[0] + "', " + err)

                self.donnees[ligne[0]] = ligne[1]

        except IOError as e:
            Interface.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)
