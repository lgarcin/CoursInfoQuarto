from math import inf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
import networkx as nx

rc('animation', html='jshtml')
rc('text', usetex=True)


class Dijkstra:
    def __init__(self, gr):
        self.fig = plt.figure()
        plt.axis('off')
        self.gr = gr
        pos = nx.planar_layout(self.gr)
        self.nodes = nx.draw_networkx_nodes(self.gr, pos, node_size=400)
        self.edges = nx.draw_networkx_edges(self.gr, pos)
        self.node_labels = nx.draw_networkx_labels(self.gr, pos)
        self.edge_labels = nx.get_edge_attributes(self.gr, 'weight')
        nx.draw_networkx_edge_labels(
            self.gr, pos, edge_labels=self.edge_labels)
        self.title = plt.title('')
        self.title.set_fontname('Comic Sans MS')

    def get_color(self, s):
        if s == self.min_dist_sommet:
            return 'g'
        if s in self.voisins:
            return 'c'
        if s in self.sommets_non_traites:
            return 'r'
        return 'y'

    def get_label(self, s):
        label = r"$"+s+"_{"
        label += "\infty" if self.dist[s] == inf else str(self.dist[s])
        label += "}$"
        return label

    def draw(self):
        self.title.set_text(self.text)
        self.nodes.set(color=[self.get_color(s) for s in self.gr.nodes])
        for s in self.node_labels:
            self.node_labels[s].set_text(self.get_label(s))
        yield

    def dijkstra(self, sommet_initial):
        self.sommet_initial = sommet_initial
        self.dist = {s: inf for s in self.gr.nodes}
        self.dist[sommet_initial] = 0
        self.sommets_non_traites = {s for s in self.gr.nodes}
        self.min_dist_sommet = None
        self.voisins = []
        self.text = 'Calcul des distances minimales à partir de '+self.sommet_initial
        yield from self.draw()
        while len(self.sommets_non_traites) != 0:
            min_dist = inf
            for s in self.sommets_non_traites:
                if self.dist[s] < min_dist:
                    self.min_dist_sommet = s
                    min_dist = self.dist[s]
            self.text = 'Le plus proche voisin non traité de ' + \
                self.sommet_initial+' est '+self.min_dist_sommet
            yield from self.draw()
            self.sommets_non_traites.remove(self.min_dist_sommet)
            self.voisins = {s: self.gr[self.min_dist_sommet][s] for s in self.gr[self.min_dist_sommet]
                            if s in self.sommets_non_traites}
            for s in self.voisins:
                d = min_dist+self.voisins[s]['weight']
                self.dist[s] = min(self.dist[s], d)
            self.text = 'Mise à jour des distances des voisins non traités de ' + self.min_dist_sommet if len(
                self.voisins) > 0 else self.min_dist_sommet+' ne possède pas de voisin non traité'
            yield from self.draw()
            self.text = 'Le sommet '+self.min_dist_sommet+' est marqué comme traité'
            self.min_dist_sommet = None
            self.voisins = []
            yield from self.draw()
        self.text = ''
        yield from self.draw()

    def animate(self, i):
        pass

    def get_dijkstra_animation(self, sommet_initial):
        ani = FuncAnimation(
            self.fig, self.animate, frames=lambda: self.dijkstra(sommet_initial), save_count=3*len(self.gr.nodes)+2, interval=2000)
        plt.close()
        return ani
