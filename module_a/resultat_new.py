from core import (CsvBase,
                  DossierDestination)


class ResultatNew(CsvBase):
    """
    Classe pour la création de la table des résultats
    """

    def __init__(self, imports, unique):
        """
        initialisation des données
        :param imports: données importées
        :param unique: nom unique de répértoire
        """
        super().__init__(imports)
        lignes = []
        self.nom = "result.csv"

        lignes.append(['FactEl', self.pt['res-factel'], 11])
        lignes.append(['Platform', self.pt['res-pltf'], imports.edition.plateforme])
        lignes.append(['Year', self.pt['res-year'], imports.edition.annee])
        lignes.append(['Month', self.pt['res-month'], imports.edition.mois])
        lignes.append(['Version', self.pt['res-version'], imports.version])
        lignes.append(['Folder', self.pt['res-folder'], unique])
        lignes.append(['Type', self.pt['res-type'], imports.edition.type])
        self.write(self.nom, DossierDestination(imports.chemin_out), lignes, False)
