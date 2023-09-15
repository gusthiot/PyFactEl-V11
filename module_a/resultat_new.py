from imports.construits import Resultat


class ResultatNew(object):
    """
    Classe pour la création de la table des résultats
    """

    def __init__(self, imports, unique):
        """
        initialisation des données
        :param imports: données importées
        :param unique: nom unique de répértoire
        """
        self.lignes = []
        self.nom = "result.csv"
        pt = imports.paramtexte.donnees

        self.lignes.append(['FactEl', pt['res-factel'], 11])
        self.lignes.append(['Platform', pt['res-pltf'], imports.edition.plateforme])
        self.lignes.append(['Year', pt['res-year'], imports.edition.annee])
        self.lignes.append(['Month', pt['res-month'], imports.edition.mois])
        self.lignes.append(['Version', pt['res-version'], imports.version])
        self.lignes.append(['Folder', pt['res-folder'], unique])
        self.lignes.append(['Type', pt['res-type'], imports.edition.type])

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'une liste de valeurs
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """

        with dossier_destination.writer(self.nom) as fichier_writer:
            for ligne in self.lignes:
                fichier_writer.writerow(ligne)
