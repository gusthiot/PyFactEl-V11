from core import (Interface,
                  Format,
                  ErreurConsistance)


class Facturation(object):
    """
    Classe pour l'importation des paramètres de facturation
    """

    nom_fichier = "paramfact.csv"
    libelle = "Paramètres Généraux"
    cles = ['code_int', 'code_ext', 'canal']

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        donnees_csv = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                if len(ligne) != 2:
                    Interface.fatal(ErreurConsistance(),
                                    self.libelle + " (" + self.nom_fichier + ") : nombre de colonnes incorrect : " +
                                    str(len(ligne)) +
                                    ", attendu : 2. Vérifier que les champs ne contiennent pas de point-virgule.")
                if ligne[0] not in self.cles:
                    Interface.fatal(ErreurConsistance(), "Clé inconnue dans %s: %s" % (self.nom_fichier, ligne[0]))
                donnees_csv[ligne[0]] = ligne[1]
        except IOError as e:
            Interface.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

        msg = ""
        for cle in self.cles:
            if cle not in donnees_csv:
                msg += self._erreur_fichier("Clé manquante:" + cle)

        self.code_int, err = Format.est_un_alphanumerique(donnees_csv['code_int'], "le code INT")
        msg += self._erreur_fichier(err)
        self.code_ext, err = Format.est_un_alphanumerique(donnees_csv['code_ext'], "le code EXT")
        msg += self._erreur_fichier(err)
        self.canal, err = Format.est_un_entier(donnees_csv['canal'], "le canal", 0)
        msg += self._erreur_fichier(err)

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)

    def _erreur_fichier(self, msg):
        """
        formate une erreur de contenu du fichier
        :param msg: message d'erreur
        :return: message formaté
        """
        if msg != "":
            return self.libelle + " (" + self.nom_fichier + ") : " + msg
        else:
            return ""
