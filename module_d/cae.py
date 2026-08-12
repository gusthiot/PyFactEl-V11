from core import CsvDict


class Cae(CsvDict):
    """
    Classe pour la création du Contrôle Accès Equipement
    """

    cles = ['cae-annee-fact', 'cae-mois-fact', 'cae-id-compte', 'cae-id-user', 'cae-id-machine', 'cae-login', 'cae-HP',
            'cae-HC', 'cae-DRUN', 'cae-DOP', 'cae-id-operator', 'cae-rem-operator', 'cae-rem-staff', 'cae-validation',
            'cae-id-validator']

    def __init__(self, imports):
        """
        initialisation des données
        :param imports: données importées
        """
        super().__init__(imports)
        self.nom = "cae.csv"

        num = 0
        for entree in imports.acces.donnees:
            donnee = []
            for cle in range(0, 6):
                donnee.append(entree[imports.acces.cles[cle]])
            drun = int(min(entree['dlog'], entree['t_mach']))
            dhp = min(drun, entree['dlog_hp'])
            dhc = drun - dhp
            id_groupe = imports.machines.donnees[entree['id_machine']]['id_groupe']
            if id_groupe in imports.ciseaux.donnees.keys():
                ciseau = imports.ciseaux.donnees[id_groupe]
                if ciseau['S3'] == 0:
                    hp = dhp
                    hc = dhc
                else:
                    if entree['disable'] > 0:
                        if drun < ciseau['S1']:
                            d0 = drun
                            d1 = 0
                            d2 = 0
                        else:
                            if drun < ciseau['S2']:
                                d0 = ciseau['S1']
                                d1 = drun - ciseau['S1']
                                d2 = 0
                            else:
                                d0 = ciseau['S1']
                                d1 = ciseau['S2'] - ciseau['S1']
                                d2 = drun - ciseau['S2']
                    else:
                        nn = round(drun/ciseau['S3'],0)
                        rr = drun - (nn * ciseau['S3'])
                        if rr < ciseau['S1']:
                            d0 = (nn * ciseau['S1']) + rr
                            d1 = nn * (ciseau['S2'] - ciseau['S1'])
                            d2 = nn * (ciseau['S3'] - ciseau['S2'])
                        else:
                            if rr < ciseau['S2']:
                                d0 = (nn + 1) * ciseau['S1']
                                d1 = nn * (ciseau['S2'] - ciseau['S1']) + rr - ciseau['S1']
                                d2 = nn * (ciseau['S3'] - ciseau['S2'])
                            else:
                                d0 = (nn + 1) * ciseau['S1']
                                d1 = (nn + 1) * (ciseau['S2'] - ciseau['S1'])
                                d2 = nn * (ciseau['S3'] - ciseau['S2']) + rr - ciseau['S2']
                    te = d0 + (ciseau['alpha1'] * d1 / 100) + (ciseau['alpha2'] * d2 / 100)
                    if te < dhp:
                        hp = int(te)
                        hc = 0
                    else:
                        hp = dhp
                        hc = int(te - dhp)
            else:
                hp = dhp
                hc = dhc

            donnee += [hp, hc, drun]
            for cle in range(10, 16):
                donnee.append(entree[imports.acces.cles[cle]])
            self._ajouter_valeur(donnee, num)
            num += 1
