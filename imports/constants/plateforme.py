from core import (Interface,
                  Format,
                  Chemin,
                  ErreurConsistance)


class Plateforme(object):
    """
    Classe pour l'importation des données de Plateformes
    """

    nom_fichier = "plateforme.csv"
    cles = ['Id-Plateforme', 'Code_P', 'CF', 'Fonds', 'Admin', 'Abrev-Plateforme', 'Intitulé-Plateforme',
            'Grille-Plateforme']
    libelle = "Plateformes"

    def __init__(self, dossier_source, clients, edition):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param clients: clients importés
        :param edition: paramètres d'édition
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
        self.donnee = {}
        for cle in self.cles:
            if cle not in donnees_csv:
                msg += self._erreur_fichier("Clé manquante dans: " + cle + "\n")

            self.donnee['id_plateforme'], err = Format.est_un_alphanumerique(donnees_csv['Id-Plateforme'][1],
                                                                             "l'id plateforme")
            msg += self._erreur_fichier(err)

            if donnees_csv['Id-Plateforme'][1] == "":
                msg += self._erreur_fichier("l'id plateforme ne peut être vide\n")
            elif donnees_csv['Id-Plateforme'][1] not in clients.donnees.keys():
                msg += self._erreur_fichier("l'id plateforme n'existe pas dans les clients \n")
            elif donnees_csv['Id-Plateforme'][1] != edition.plateforme:
                msg += self._erreur_fichier("l'id plateforme n'est pas celui de paramedit \n")

            self.donnee['code_p'], err = Format.est_un_alphanumerique(donnees_csv['Code_P'][1], "le code P")
            msg += self._erreur_fichier(err)
            self.donnee['centre'], err = Format.est_un_alphanumerique(donnees_csv['CF'][1], "le centre financier")
            msg += self._erreur_fichier(err)
            self.donnee['fonds'], err = Format.est_un_alphanumerique(donnees_csv['Fonds'][1], "les fonds à créditer")
            msg += self._erreur_fichier(err)
            self.donnee['admin'], err = Format.est_un_entier(donnees_csv['Admin'][1], "le sciper admin à créditer", 0)
            msg += self._erreur_fichier(err)
            self.donnee['abrev_plat'], err = Format.est_un_alphanumerique(donnees_csv['Abrev-Plateforme'][1],
                                                                          "l'abréviation")
            msg += self._erreur_fichier(err)
            self.donnee['intitule'], err = Format.est_un_texte(donnees_csv['Intitulé-Plateforme'][1],
                                                               "l'intitulé")
            msg += self._erreur_fichier(err)

            if donnees_csv['Grille-Plateforme'][1] != 'OUI' and donnees_csv['Grille-Plateforme'][1] != 'NON':
                msg += self._erreur_fichier("grille-plateforme doit être OUI ou NON\n")
            else:
                self.donnee['grille'] = donnees_csv['Grille-Plateforme'][1]

            if (donnees_csv['Grille-Plateforme'][1] == 'OUI' and
                    not Chemin.existe(Chemin.chemin([dossier_source.chemin, 'grille.pdf']))):
                msg += self._erreur_fichier("la grille n'existe pas dans le dossier d'entrée \n")

        if msg != "":
            Interface.fatal(ErreurConsistance(), msg)

    def test_id(self, id_plateforme):
        msg = ""
        if id_plateforme == "":
            msg += "l'id plateforme ne peut être vide\n"
        elif id_plateforme != self.donnee['id_plateforme']:
            msg += ("l'id plateforme " + id_plateforme + " n'est pas celui attendu : " +
                    self.donnee['id_plateforme'] + "\n")
        return msg

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
