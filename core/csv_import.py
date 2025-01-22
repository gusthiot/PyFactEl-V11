from core import (Interface,
                  ErreurConsistance)


class CsvImport(object):
    """
    Classe de base des classes d'importation de données

    Attributs de classe (à définir dans les sous-classes) :
         nom_fichier    Le nom relatif du fichier à charger
         libelle        Un intitulé pour les messages d'erreur
         cles           La liste des colonnes à charger
    """
    nom_fichier = ""
    cles = []
    libelle = ""

    def __init__(self, dossier_source):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        try:
            fichier_reader = dossier_source.reader(self.nom_fichier)
            donnees_csv = []
            numero = 1
            for ligne in fichier_reader:
                donnees_ligne = self._extraction_ligne(ligne, numero)
                numero += 1
                if donnees_ligne == -1:
                    continue
                donnees_csv.append(donnees_ligne)
            self.donnees = donnees_csv
            del self.donnees[0]
        except IOError as e:
            Interface.fatal(e, "impossible d'ouvrir le fichier : "+self.nom_fichier)

    def _erreur_ligne(self, ligne, msg):
        """
        formate une erreur de ligne
        :param ligne: ligne lue du fichier
        :param msg: message d'erreur
        :return: message formaté
        """
        if msg != "":
            return self.libelle + " (" + self.nom_fichier + ", ligne " + str(ligne) + ") : " + msg
        else:
            return ""

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

    def _extraction_ligne(self, ligne, num_ligne):
        """
        extracte une ligne de données du csv
        :param ligne: ligne lue du fichier
        :param num_ligne: numéro de ligne lue du fichier
        :return: tableau représentant la ligne, indexé par les clés
        """
        num = len(self.cles)
        if len(ligne) != num:
            Interface.fatal(ErreurConsistance(), self._erreur_ligne(num_ligne, "Nombre de colonnes incorrect : " +
                         str(len(ligne)) + ", attendu : " + str(num) + ". Vérifier que les champs ne contiennent pas de point-virgule. \n"))
        donnees_ligne = {}
        for xx in range(0, num):
            donnees_ligne[self.cles[xx]] = ligne[xx]
        return donnees_ligne

    def test_id_coherence(self, donnee, nom, num_ligne, corpus, zero=False):
        """
        vérifie si l'id donné est cohérent
        :param donnee: id donné
        :param nom: nom de l'id
        :param num_ligne: numéro de ligne lue du fichier
        :param corpus: données dans lesquelles l'id devrait se retrouver
        :param zero: si l'id peut être égal à zéro
        :return: un message d'erreur ou un string vide si ok
        """
        msg = ""
        if donnee == "":
            msg += nom + " ne peut être vide\n"
        elif (not zero or donnee != "0") and donnee not in corpus.donnees.keys():
            msg += nom + " '" + donnee + "' n'est pas référencé"
            if zero:
                msg += " ni égal à 0"
            msg += "\n"
        return self._erreur_ligne(num_ligne, msg)
