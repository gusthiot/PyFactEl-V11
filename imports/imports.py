from imports import Edition
from imports.constants import (ArticleSap,
                               Categorie,
                               CategPrix,
                               ClasseClient,
                               CoefPrest,
                               Facturation,
                               Groupe,
                               Machine,
                               Paramtexte,
                               Plateforme,
                               Prestation,
                               ClassePrestation,
                               Overhead)
from imports.variables import (Acces,
                               CleSubside,
                               Client,
                               Compte,
                               Livraison,
                               NoShow,
                               PlafSubside,
                               Service,
                               Subside,
                               User,
                               Partenaire)
from imports.construits import (Numero,
                                Resultat,
                                Granted,
                                UserLabo,
                                Version,
                                Transactions2,
                                ClientPrev)
from core import (Interface,
                  Chemin,
                  Format,
                  ErreurConsistance,
                  DossierDestination)


class Imports(object):
    """
    Classe pour l'importation et la structuration des données
    """

    def __init__(self, dossier_source, destination, unique):
        """
        initialisation et importation des données
        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param destination: dossier de destination de sauvegarde
        :param unique: nom unique de répértoire
        """

        self.dossier_source = dossier_source

        self.edition = Edition(dossier_source)

        # importation et vérification des données d'entrée

        self.paramtexte = Paramtexte(dossier_source)
        self.facturation = Facturation(dossier_source)
        self.classes = ClasseClient(dossier_source)
        self.clients = Client(dossier_source, self.facturation, self.classes)
        self.plateformes = Plateforme(dossier_source, self.clients, self.edition)
        self.partenaires = Partenaire(dossier_source, self.clients, self.plateformes, self.classes)
        self.artsap = ArticleSap(dossier_source)
        self.overheads = Overhead(dossier_source, self.artsap)
        self.classprests = ClassePrestation(dossier_source, self.artsap, self.overheads)
        self.resultats = Resultat(dossier_source, self.plateformes)
        self.categories = Categorie(dossier_source, self.classprests, self.plateformes)
        self.groupes = Groupe(dossier_source, self.categories)
        self.machines = Machine(dossier_source, self.groupes, self.edition)
        self.subsides = Subside(dossier_source)
        self.plafonds = PlafSubside(dossier_source, self.subsides, self.classprests, self.plateformes)
        self.cles = CleSubside(dossier_source, self.clients, self.machines, self.classes, self.subsides)
        self.comptes = Compte(dossier_source, self.clients, self.subsides)
        self.users = User(dossier_source)
        self.categprix = CategPrix(dossier_source, self.classes, self.categories)
        self.coefprests = CoefPrest(dossier_source, self.classes, self.classprests)
        self.prestations = Prestation(dossier_source, self.classprests, self.coefprests, self.plateformes,
                                      self.machines, self.edition)

        self.plateforme = self.plateformes.donnee

        self.acces = Acces(dossier_source, self.comptes, self.machines, self.users)
        self.noshows = NoShow(dossier_source, self.comptes, self.machines, self.users)
        self.livraisons = Livraison(dossier_source, self.comptes, self.prestations, self.users)
        self.services = Service(dossier_source, self.comptes, self.groupes, self.users)

        # vérification des données fondamentales

        if self.edition.plateforme != self.resultats.plateforme:
            Interface.fatal(ErreurConsistance(), "la plateforme de facturation : " + self.edition.plateforme +
                            ", doit être la même que la plateforme des résultats : " + self.resultats.plateforme)
        if self.edition.mois == self.resultats.mois:
            if self.edition.annee != self.resultats.annee:
                Interface.fatal(ErreurConsistance(), "pour un mois identique l'année de facturation : " +
                                str(self.edition.annee) + ", doit être la même que l'année des résultats : " +
                                str(self.resultats.annee))
            else:
                self.version = self.resultats.vfact + 1
        if self.edition.mois > (self.resultats.mois+1):
            Interface.fatal(ErreurConsistance(), "le mois de facturation : " + str(self.edition.mois) +
                            ", ne peut être de plus d'un mois de plus que le mois des résultats : " +
                            str(self.resultats.mois))
        if self.edition.mois == (self.resultats.mois+1):
            if self.edition.annee != self.resultats.annee:
                Interface.fatal(ErreurConsistance(), "pour un mois de plus,  l'année de facturation : " +
                                str(self.edition.annee) + ", doit être la même que l'année des résultats : " +
                                str(self.resultats.annee))
            else:
                self.version = 0
        if self.edition.mois < self.resultats.mois:
            if self.edition.mois == 1 and self.resultats.mois == 12 and self.edition.annee == (self.resultats.annee+1):
                self.version = 0
            else:
                Interface.fatal(ErreurConsistance(), "le mois de facturation : " + str(self.edition.mois) +
                                ", ne peut être plus petit que le mois des résultats : " + str(self.resultats.mois))

        self.grants = Granted(dossier_source, self.edition, self.comptes, self.classprests, self.plateformes)
        self.userlabs = UserLabo(dossier_source, self.edition, self.plateformes, self.clients, self.users)

        self.logo = ""
        extensions = [".pdf", ".eps", ".png", ".jpg"]
        for ext in extensions:
            chemin = Chemin.chemin([dossier_source.chemin, "logo" + ext])
            if Chemin.existe(chemin, False):
                self.logo = "logo" + ext
                break

        # importation des données de la version précédente
        if self.version > 0:
            self.numeros = Numero(dossier_source, self.edition, self.comptes, self.clients, self.resultats.vfact)
            self.versions = Version(dossier_source, self.edition, self.resultats.vfact)
            self.transactions_2 = Transactions2(dossier_source, self.edition, self.plateforme, self.resultats.vfact)
            self.clients_prev = ClientPrev(dossier_source, self.edition, self.facturation, self.classes,
                                           self.resultats.vfact)

        # vérification terminée, création des dossiers de sauvegarde

        self.chemin_enregistrement = Chemin.chemin([destination, self.edition.plateforme, self.edition.annee,
                                                    Format.mois_string(self.edition.mois), self.version, unique])
        self.chemin_in = Chemin.chemin([self.chemin_enregistrement, "IN"])
        self.chemin_prix = Chemin.chemin([self.chemin_enregistrement, "Prix"])
        self.chemin_cannexes = Chemin.chemin([self.chemin_enregistrement, "Annexes_CSV"])
        self.chemin_pannexes = Chemin.chemin([self.chemin_enregistrement, "Annexes_PDF"])
        self.chemin_factures = Chemin.chemin([self.chemin_enregistrement, "Factures_JSON"])
        self.chemin_out = Chemin.chemin([self.chemin_enregistrement, "OUT"])
        self.chemin_bilans = Chemin.chemin([self.chemin_enregistrement, "Bilans_Stats"])

        Chemin.existe(self.chemin_in, True)
        Chemin.existe(self.chemin_prix, True)
        Chemin.existe(self.chemin_bilans, True)
        Chemin.existe(self.chemin_out, True)
        Chemin.existe(self.chemin_cannexes, True)
        Chemin.existe(self.chemin_pannexes, True)
        Chemin.existe(self.chemin_factures, True)

        # sauvegarde des bruts

        destination_in = DossierDestination(self.chemin_in)
        destination_out = DossierDestination(self.chemin_out)
        for fichier_in in [self.paramtexte, self.facturation, self.classes, self.plateformes, self.artsap,
                           self.categories, self.groupes, self.machines, self.categprix, self.coefprests,
                           self.prestations, self.classprests, self.overheads, self.clients, self.subsides,
                           self.plafonds, self.cles, self.comptes, self.users, self.acces, self.noshows,
                           self.livraisons, self.services, self.partenaires, self.resultats, self.grants, self.userlabs,
                           self.edition]:
            destination_in.ecrire(fichier_in.nom_fichier, self.dossier_source.lire(fichier_in.nom_fichier))
        for fichier_out in [self.paramtexte, self.facturation, self.classes, self.plateformes, self.artsap,
                            self.categories, self.groupes, self.categprix, self.coefprests, self.classprests,
                            self.overheads, self.partenaires, self.resultats, self.grants, self.userlabs]:
            destination_out.ecrire(fichier_out.nom_fichier, self.dossier_source.lire(fichier_out.nom_fichier))

            destination_out.ecrire("client_" + str(self.edition.annee) + "_" + Format.mois_string(self.edition.mois) +
                                   "_" + str(self.version) + ".csv",
                                   self.dossier_source.lire(self.clients.nom_fichier))
        if self.logo != "":
            destination_in.ecrire(self.logo, dossier_source.lire(self.logo))
            destination_out.ecrire(self.logo, dossier_source.lire(self.logo))
        if self.plateforme['grille'] == "OUI":
            grille = 'grille.pdf'
            destination_in.ecrire(grille, dossier_source.lire(grille))
            destination_out.ecrire(grille, dossier_source.lire(grille))

        if self.version > 0:
            for fichier in [self.numeros, self.versions, self.transactions_2, self.clients_prev]:
                destination_in.ecrire(fichier.nom_fichier, self.dossier_source.lire(fichier.nom_fichier))
