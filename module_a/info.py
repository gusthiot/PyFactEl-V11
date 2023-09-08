from datetime import datetime


class Info(object):
    """
    Classe pour la création du fichier d'information
    """

    def __init__(self, imports, unique):
        """
        initialisation des données
        :param imports: données importées
        :param unique: nom unique de répértoire
        """
        self.lignes = []
        self.nom = "info.csv"
        self.cles = ['FactEl', 'Platform', 'Year', 'Month', 'Version', 'Folder', 'Type']
        pt = imports.paramtexte.donnees

        self.lignes.append(['FactEl', pt['res-factel'], 11])
        self.lignes.append(['Platform', pt['res-pltf'], imports.edition.plateforme])
        self.lignes.append(['Year', pt['res-year'], imports.edition.annee])
        self.lignes.append(['Month', pt['res-month'], imports.edition.mois])
        self.lignes.append(['Version', pt['res-version'], imports.version])
        self.lignes.append(['Folder', pt['res-folder'], unique])
        self.lignes.append(['Type', pt['res-type'], imports.edition.type])
        self.lignes.append(['Created', pt['info-created'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        self.lignes.append(['Sent', pt['info-sent'], ""])
        self.lignes.append(['Closed', pt['info-closed'], ""])

    def csv(self, dossier_destination):
        """
        création du fichier csv à partir de la liste des noms de colonnes et d'une liste de valeurs
        :param dossier_destination: Une instance de la classe dossier.DossierDestination
        """

        with dossier_destination.writer(self.nom) as fichier_writer:
            for ligne in self.lignes:
                fichier_writer.writerow(ligne)
