import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._nodes = None
        # Mappe per accesso rapido (id -> oggetto)
        self._id_map = {}
        # TODO

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # 1. Pulizia: Se il grafo esiste già, lo svuoto
        self.G.clear()
        self._nodes = set()
        self._id_map = {}

        # 2. Recupero tutti i rifugi (nodi) dal DB
        all_rifugi = DAO.get_rifugio()

        # 3. Aggiungo i nodi al grafo
        for rifugio in all_rifugi:
            # Salvo nella mappa per recuperare l'oggetto dato l'ID
            self._id_map[rifugio.id] = rifugio
            self._nodes.add(rifugio)
            # Aggiungo il nodo al grafo (passo l'intero oggetto)
            self.G.add_node(rifugio)

        # 4. Recupero tutte le tratte (archi potenziali)
        all_connessioni = DAO.get_connessione(year)

        # 5. Aggiungo gli archi
        peso = None
        for c in all_connessioni:
            # Controllo che entrambi i rifugi esistano (sicurezza)
            if c.r1 in self._id_map and c.r2 in self._id_map:
                u = self._id_map[c.r1]
                v = self._id_map[c.r2]
                if c.difficolta == 'facile':
                    fattore_difficolta = 1
                    peso = float(c.distanza) * fattore_difficolta
                elif c.difficolta == 'media':
                    fattore_difficolta = 1.5
                    peso = float(c.distanza) * fattore_difficolta
                elif c.difficolta == 'difficile':
                    fattore_difficolta = 2
                    peso = float(c.distanza) * fattore_difficolta
                # Aggiungo l'arco.
                self.G.add_edge(u, v, weight = peso)

        # 6. PULIZIA DEL GRAFO
        nodi_isolati = [node for node in self.G.nodes() if self.G.degree(node) == 0]
        self.G.remove_nodes_from(nodi_isolati)

        # Aggiorno la lista interna dei nodi attivi
        self._nodes = set(self.G.nodes())

        # TODO

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        all_weights = [ arco[2]['weight'] for arco in self.G.edges(data = True) ]
        min_weight = min(all_weights)
        max_weight = max(all_weights)
        return min_weight, max_weight
        # TODO

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0
        all_edges = self.G.edges(data = True)
        for arco in all_edges:
            if arco[2]['weight'] < soglia:
                minori += 1
            elif arco[2]['weight'] > soglia:
                maggiori += 1
        return minori, maggiori

        # TODO

    """Implementare la parte di ricerca del cammino minimo"""
    def get_minimo_cammino(self):
        # Tecnica 1: NetworkX BFS
        reachable_nx = self.get_minimo_cammino_bfs_tree()

        # Tecnica 2: Ricorsiva
        reachable_iter = self.get_minimo_cammino_recursive()

        return reachable_nx

    def get_minimo_cammino_bfs_tree(self, start):
        pass

    def get_minimo_cammino_recursive(self, start):
        pass
    # TODO
