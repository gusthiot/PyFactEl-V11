from datetime import datetime
import re


class Format(object):
    """
    Classe contenant des méthodes pour vérifier ou adapter le format des données
    """
    @staticmethod
    def mois_string(mois):
        """
        prend un mois comme nombre, et le retourne comme string, avec un '0' devant si plus petit que 10
        :param mois: mois formaté en nombre
        :return: mois formaté en string
        """
        try:
            mint = int(mois)
            if mint < 10:
                return "0" + str(mint)
            else:
                return str(mint)
        except ValueError:
            return "mois pas un entier"

    @staticmethod
    def nombre(nombre, signifiant=2):
        """
        affiche un nombre en float arrondi avec 2 chiffres après la virgule et avec un séparateur des milliers
        :param nombre: nombre à afficher
        :param signifiant: nombre de chiffres après la virgule
        :return: nombre arrondi, avec 2 chiffres par défaut après la virgule, en string
        """
        try:
            float(nombre)
            return ('{:,.'+str(signifiant)+'f}').format(nombre).replace(",", "'")
        except ValueError:
            return "pas un nombre"

    @staticmethod
    def est_un_texte(donnee, colonne, vide=False):
        """
        vérifie que la donnée est bien un texte
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        try:
            s_d = str(donnee)
            if s_d.startswith('"') and s_d.endswith('"'):
                s_d = s_d[1:-1]
            if s_d == "" and not vide:
                return "", colonne + " ne peut être vide\n"
            return s_d, ""
        except ValueError:
            return "", colonne + " doit être un texte\n"

    @staticmethod
    def est_une_date(donnee, colonne, vide=False):
        """
        vérifie que la donnée est bien une date
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        try:
            s_d = str(donnee)
            if s_d.startswith('"') and s_d.endswith('"'):
                s_d = s_d[1:-1]
            if s_d == "":
                if not vide:
                    return "", colonne + " ne peut être vide\n"
                else:
                    return "", ""
            date = datetime.strptime(s_d, '%Y-%m-%d %H:%M:%S')
            return date, ""
        except ValueError:
            return "", colonne + " doit être une date du bon format : YYYY-MM-DD HH:MM:SS\n"

    @staticmethod
    def est_un_document(donnee, colonne, vide=False):
        """
        vérifie que la donnée est bien un nom de document
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        try:
            chars = set('\/:*?“<>|')
            s_d = str(donnee)
            if s_d == "" and not vide:
                return "", colonne + " ne peut être vide\n"
            if any((c in chars) for c in s_d):
                return "", colonne + " n'est pas un nom de document valide\n"
            return s_d, ""
        except:
            return "", colonne + " doit être un texte\n"

    @staticmethod
    def est_un_chemin(donnee, colonne, vide=False):
        """
        vérifie que la donnée est bien un chemin
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        try:
            chars = set('*?"<>|')
            s_d = str(donnee)
            if s_d == "" and not vide:
                return "", colonne + " ne peut être vide\n"
            if any((c in chars) for c in s_d):
                return "", colonne + " n'est pas un chemin valide\n"
            return s_d.replace("\\", "/"), ""
        except:
            return "", colonne + " doit être un texte\n"

    @staticmethod
    def est_un_alphanumerique(donnee, colonne, barres=False, chevrons=False, vide=False):
        """
        vérifie que la donnée est bien un texte
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param barres: True si la variable peut contenir des barres obliques, False sinon
        :param chevrons: True si la variable peut contenir des < >, False sinon
        :param vide: True si la variable peut être vide, False sinon
        :return: la donnée formatée et un string vide si ok, "" et un message d'erreur sinon
        """
        try:
            if barres:
                if chevrons:
                    pattern = '^[a-zA-Z0-9_<>\-./\\\\]+$'
                else:
                    pattern = '^[a-zA-Z0-9_\-./\\\\]+$'
            else:
                if chevrons:
                    pattern = '^[a-zA-Z0-9_<>\-]+$'
                else:
                    pattern = '^[a-zA-Z0-9_\-]+$'
            s_d = str(donnee)
            if s_d == "":
                if not vide:
                    return "", colonne + " ne peut être vide\n"
                else:
                    return "", ""
            if not re.match(pattern, s_d):
                return "", colonne + " n'est pas un alphanumérique valide\n"
            return s_d, ""
        except:
            return "", colonne + " doit être un texte\n"

    @staticmethod
    def est_un_nombre(donnee, colonne, arrondi=-1, mini=None, maxi=None):
        """
        vérifie que la donnée est bien un nombre
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param arrondi: arrondi après la virgule (-1 si pas d'arrondi)
        :param mini: borne minimale facultative
        :param maxi: borne maximale facultative
        :return: la donnée formatée en nombre et un string vide si ok, 0 et un message d'erreur sinon
        """
        try:
            fl_d = float(donnee)
            if mini is not None and fl_d < mini:
                return -1, colonne + " doit être un nombre >= " + str(min) + "\n"
            if maxi is not None and fl_d > maxi:
                return -1, colonne + " doit être un nombre <= " + str(max) + "\n"
            if arrondi > -1:
                return round(fl_d, arrondi), ""
            else:
                return fl_d, ""
        except ValueError:
            return -1, colonne + " doit être un nombre\n"

    @staticmethod
    def est_un_entier(donnee, colonne, mini=None, maxi=None):
        """
        vérifie que la donnée est bien un nombre entier dans les bornes éventuelles
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée (nom de la variable)
        :param mini: borne minimale facultative
        :param maxi: borne maximale facultative
        :return: la donnée formatée en nombre et un string vide si ok, 0 et un message d'erreur sinon
        """
        try:
            entier = int(donnee)
            if mini is not None and entier < mini:
                return -1, colonne + " doit être un nombre entier >= " + str(mini) + "\n"
            if maxi is not None and entier > maxi:
                return -1, colonne + " doit être un nombre entier <= " + str(maxi) + "\n"
            return entier, ""
        except ValueError:
            return -1, colonne + " doit être un nombre entier\n"
