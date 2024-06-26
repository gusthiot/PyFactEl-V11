from core import (Interface,
                  Format,
                  ErreurConsistance)


class Resultat(object):
    """
    Classe pour l'importation des résultats de la facturation précédente
    """

    nom_fichier = "result.csv"
    libelle = "Résultats précédents"
    cles = ['FactEl', 'Platform', 'Year', 'Month', 'Version', 'Folder', 'Type']

    def __init__(self, dossier_source, plateformes):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param plateformes: plateformes importées
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

        self.vlog, err = Format.est_un_nombre(donnees_csv['FactEl'][1], "la version logicielle")
        msg += self._erreur_fichier(err)
        self.plateforme, err = Format.est_un_alphanumerique(donnees_csv['Platform'][1], "l'id plateforme")
        msg += self._erreur_fichier(err)
        msg += plateformes.test_id(donnees_csv['Platform'][1])
        self.annee, err = Format.est_un_entier(donnees_csv['Year'][1], "l'année", mini=2000, maxi=2099)
        msg += self._erreur_fichier(err)
        self.mois, err = Format.est_un_entier(donnees_csv['Month'][1], "le mois", mini=1, maxi=12)
        msg += self._erreur_fichier(err)
        self.vfact, err = Format.est_un_entier(donnees_csv['Version'][1], "la version de facturation", mini=0)
        msg += self._erreur_fichier(err)
        self.repertoire, err = Format.est_un_alphanumerique(donnees_csv['Folder'][1], "le répertoire")
        msg += self._erreur_fichier(err)
        if donnees_csv['Type'][1] != 'SAP' and donnees_csv['Type'][1] != 'PROFORMA' and donnees_csv['Type'][1] != 'SIMU':
            msg += self._erreur_fichier("le type doit être SAP, PROFORMA ou SIMU\n")
        else:
            self.type = donnees_csv['Type'][1]

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

