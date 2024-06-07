from core import (Interface,
                  Format,
                  ErreurConsistance)


class Facturation(object):
    """
    Classe pour l'importation des paramètres de facturation
    """

    nom_fichier = "paramfact.csv"
    libelle = "Paramètres Généraux"
    cles = ['code_int', 'code_ext', 'devise', 'modes']

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        donnees_csv = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                cle = ligne.pop(0)
                if cle not in self.cles:
                    Interface.fatal(ErreurConsistance(), "Clé inconnue dans %s: %s" % (self.nom_fichier, cle))
                while ligne[-1] == "":
                    del ligne[-1]
                donnees_csv[cle] = ligne
        except IOError as e:
            Interface.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

        msg = ""
        for cle in self.cles:
            if cle not in donnees_csv:
                msg += self._erreur_fichier("Clé manquante:" + cle + "\n")

        self.code_int, err = Format.est_un_alphanumerique(donnees_csv['code_int'][1], "le code INT")
        msg += self._erreur_fichier(err)
        self.code_ext, err = Format.est_un_alphanumerique(donnees_csv['code_ext'][1], "le code EXT")
        msg += self._erreur_fichier(err)
        self.devise, err = Format.est_un_alphanumerique(donnees_csv['devise'][1], "la devise")
        msg += self._erreur_fichier(err)

        self.modes = []
        for mode in donnees_csv['modes'][1:]:
            mode, err = Format.est_un_alphanumerique(mode, "le mode d'envoi", vide=True)
            self.modes.append(mode)
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
