

class Sommes2(object):
    """
    Classe pour sommer les transactions 2
    """

    def __init__(self, transactions_2):
        """
        initialisation des données
        :param transactions_2: transactions 2 générées
        """
        self.par_fact = {}
        self.par_client = {}
        for key, trans in transactions_2.valeurs.items():
            if trans['invoice-id'] not in self.par_fact:
                self.par_fact[trans['invoice-id']] = {'base': key, 'total': 0, 'projets': {}, 'comptes': {}}
            self.par_fact[trans['invoice-id']]['total'] += trans['total-fact']
            projets = self.par_fact[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {'transactions': [], 'articles': {}, 'numero': trans['proj-nbr'],
                                             'intitule': trans['proj-name']}
            tpa = projets[trans['proj-id']]['articles']
            if trans['item-idsap'] not in tpa:
                tpa[trans['item-idsap']] = {'items': {}, 'total': 0, 'base': key}
            tpa[trans['item-idsap']]['total'] += trans['total-fact']
            # => transactions 1

            tps = tpa[trans['item-idsap']]['items']
            if trans['item-nbr'] not in tps:
                tps[trans['item-nbr']] = {}
            tpsi = tps[trans['item-nbr']]
            if trans['user-id'] not in tpsi:
                tpsi[trans['user-id']] = []
            tpsi[trans['user-id']].append(key)
            # => versions / pdfs

            projets[trans['proj-id']]['transactions'].append(key)
            # => annexes

            if trans['client-code'] not in self.par_client.keys():
                self.par_client[trans['client-code']] = {'transactions': []}
            self.par_client[trans['client-code']]['transactions'].append(key)
            # => annexes all

    @staticmethod
    def sommes_old(transactions):
        """
        crée l'arborescence des anciennes transactions, fonction projet->articleSAP->article->utilisateur
        :param transactions: données transactions
        :return: arborescence sous forme de dictionnaire
        """
        arbre = {}
        for key, trans in transactions.items():
            if trans['invoice-id'] not in arbre:
                arbre[trans['invoice-id']] = {'projets': {}}
            projets = arbre[trans['invoice-id']]['projets']
            if trans['proj-id'] not in projets:
                projets[trans['proj-id']] = {'articles': {}}
            tpa = projets[trans['proj-id']]['articles']
            if trans['item-idsap'] not in tpa:
                tpa[trans['item-idsap']] = {'items': {}}
            tps = tpa[trans['item-idsap']]['items']
            if trans['item-nbr'] not in tps:
                tps[trans['item-nbr']] = {}
            tpsi = tps[trans['item-nbr']]
            if trans['user-id'] not in tpsi:
                tpsi[trans['user-id']] = []
            tpsi[trans['user-id']].append(key)
        return arbre
