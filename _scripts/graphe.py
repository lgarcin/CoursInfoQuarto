import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
import networkx as nx
import collections

rc("animation", html="jshtml")


class Graphe:
    def __init__(self, gr):
        self.fig = plt.figure()
        plt.axis("off")
        self.gr = gr
        pos = nx.spring_layout(self.gr)
        self.nodes = nx.draw_networkx_nodes(self.gr, pos, node_size=600)
        self.edges = nx.draw_networkx_edges(self.gr, pos)
        self.labels = nx.draw_networkx_labels(
            self.gr, pos, font_size=20, font_weight="bold"
        )

    def draw_visites(self, visites):
        self.nodes.set(color=["r" if visites[s] else "b" for s in self.gr.nodes])
        yield

    def parcours_profondeur(self, sommet_initial):
        visites = {sommet: False for sommet in self.gr.nodes}
        pile = collections.deque()
        pile.append(sommet_initial)
        while pile:
            sommet = pile.pop()
            if not visites[sommet]:
                visites[sommet] = True
                yield from self.draw_visites(visites)
            for voisin in self.gr[sommet]:
                if not visites[voisin]:
                    pile.append(voisin)

    def parcours_largeur(self, sommet_initial):
        visites = {sommet: False for sommet in self.gr.nodes}
        file = collections.deque()
        file.append(sommet_initial)
        while file:
            sommet = file.popleft()
            if not visites[sommet]:
                visites[sommet] = True
                yield from self.draw_visites(visites)
            for voisin in self.gr[sommet]:
                if not visites[voisin]:
                    file.append(voisin)

    def animate(self, i):
        pass

    def get_parcours_profondeur_animation(self, sommet_initial):
        ani = FuncAnimation(
            self.fig,
            self.animate,
            frames=lambda: self.parcours_profondeur(sommet_initial),
            save_count=len(self.gr.nodes),
            interval=1000,
        )
        plt.close()
        return ani

    def get_parcours_largeur_animation(self, sommet_initial):
        ani = FuncAnimation(
            self.fig,
            self.animate,
            frames=lambda: self.parcours_largeur(sommet_initial),
            save_count=len(self.gr.nodes),
            interval=1000,
        )
        plt.close()
        return ani
