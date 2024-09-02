

class CsvBase(object):
    """
    Classe de base pour les fichiers csv récapitulatifs
    """
    cles = []
    nom = ""

    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        self.imports = imports
        self.pt = self.imports.paramtexte.donnees

    def get_keys(self):
        """
        génération de la ligne d'entête
        """
        ligne = []
        for cle in self.cles:
            ligne.append(self.pt[cle])
        return ligne

    def check_ligne(self, ligne):
        """
        arrondissement des float pour éviter les mauvaises surprises
        """
        result = []
        for valeur in ligne:
            if isinstance(valeur, float):
                result.append(round(valeur, 3))
            else:
                result.append(valeur)
        return result

    def write(self, nom, dossier_destination, lignes, keys=True):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'une liste de valeurs
        :param nom: nom di fichier csv
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        :params lignes: tableau contenant les valeurs
        :params keys: True si on veut la ligne d'entête, False sinon
        """
        with dossier_destination.writer(nom) as fichier_writer:
            if keys:
                fichier_writer.writerow(self.get_keys())
            for ligne in lignes:
                fichier_writer.writerow(self.check_ligne(ligne))


class CsvDict(CsvBase):
    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.valeurs = {}

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'un dictionnaire de valeurs
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """

        with dossier_destination.writer(self.nom) as fichier_writer:
            fichier_writer.writerow(self.get_keys())
            for valeur in self.valeurs.values():
                ligne = []
                for i in range(0, len(self.cles)):
                    ligne.append(valeur[self.cles[i]])
                fichier_writer.writerow(self.check_ligne(ligne))

    def _ajouter_valeur(self, donnee, unique):
        """
        ajout d'une ligne au prototype de csv
        :param donnee: contenu de la ligne
        :param unique: clé d'identification unique de la ligne
        """
        valeur = {}
        for i in range(0, len(self.cles)):
            valeur[self.cles[i]] = donnee[i]
        self.valeurs[unique] = valeur


class CsvList(CsvBase):
    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.lignes = []

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'une liste de valeurs
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """

        with dossier_destination.writer(self.nom) as fichier_writer:
            fichier_writer.writerow(self.get_keys())
            for ligne in self.lignes:
                fichier_writer.writerow(self.check_ligne(ligne))
