from datetime import datetime
from core import (CsvBase,
                  DossierDestination)


class Info(CsvBase):
    """
    Classe pour la création du fichier d'information
    """

    def __init__(self, imports, unique, login):
        """
        initialisation des données
        :param imports: données importées
        :param unique: nom unique de répértoire
        :param login: login de la personne lançant la facturation
        """
        super().__init__(imports)
        lignes = []
        self.nom = "info.csv"

        lignes.append(['FactEl', self.pt['res-factel'], 11.01, ""])
        lignes.append(['Platform', self.pt['res-pltf'], imports.edition.plateforme, ""])
        lignes.append(['Year', self.pt['res-year'], imports.edition.annee, ""])
        lignes.append(['Month', self.pt['res-month'], imports.edition.mois, ""])
        lignes.append(['Version', self.pt['res-version'], imports.version, ""])
        lignes.append(['Folder', self.pt['res-folder'], unique, ""])
        lignes.append(['Type', self.pt['res-type'], imports.edition.type, ""])
        lignes.append(['Created', self.pt['info-created'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), login])
        lignes.append(['Sent', self.pt['info-sent'], "", ""])
        lignes.append(['Closed', self.pt['info-closed'], "", ""])
        self.write(self.nom, DossierDestination(imports.chemin_enregistrement), lignes, False)
