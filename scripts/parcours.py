from manim import Scene, Graph, Text, Create, Write, AnimationGroup, UP, RED, BLUE
import networkx as nx
import collections
import numpy as np


class DoubleParcours(Scene):
    def construct(self):
        # Graphe source (NetworkX)
        G = nx.balanced_tree(2, 3)

        # Layout identique pour les deux (2D -> 3D)
        layout = binary_tree_layout(G, root=0)
        layout_left = {k: v + [-3, 0, 0] for k, v in layout.items()}  # gauche
        layout_right = {k: v + [3, 0, 0] for k, v in layout.items()}  # droite

        # Deux graphes Manim indépendants
        graph_depth = Graph(
            G.nodes,
            G.edges,
            layout=layout_left,
            vertex_config={"radius": 0.15},
        )
        graph_breadth = Graph(
            G.nodes,
            G.edges,
            layout=layout_right,
            vertex_config={"radius": 0.15},
        )

        # Ajout à la scène
        self.play(Create(graph_depth), Create(graph_breadth))
        self.wait(1)

        titre_gauche = Text("Parcours en profondeur", font_size=28)
        titre_droite = Text("Parcours en largeur", font_size=28)

        # Positionner au-dessus des graphes
        titre_gauche.next_to(graph_depth, UP, buff=0.5)
        titre_droite.next_to(graph_breadth, UP, buff=0.5)

        # Animation d’apparition
        self.play(Write(titre_gauche), Write(titre_droite))

        # Animations synchronisées
        depth_anims = self.get_parcours_animation(graph_depth, G, 0, profondeur=True)
        breadth_anims = self.get_parcours_animation(
            graph_breadth, G, 0, profondeur=False
        )

        self.play(AnimationGroup(*depth_anims, lag_ratio=1))
        self.play(AnimationGroup(*breadth_anims, lag_ratio=1))
        self.wait()

    def get_parcours_animation(self, graph, G, start, profondeur=True):
        visites = {v: False for v in G.nodes}
        conteneur = collections.deque([start])
        anims = []

        while conteneur:
            sommet = conteneur.pop() if profondeur else conteneur.popleft()
            if not visites[sommet]:
                visites[sommet] = True
                anims.append(
                    graph[sommet].animate.set_fill(RED if profondeur else BLUE)
                )
                for voisin in G[sommet]:
                    if not visites[voisin]:
                        conteneur.append(voisin)

        return anims


def binary_tree_layout(G, root=0, x_spacing=0.5, y_spacing=0.5):
    levels = {}  # niveau → liste de nœuds
    pos = {}

    def dfs(node, depth):
        if depth not in levels:
            levels[depth] = []
        levels[depth].append(node)
        for child in G.neighbors(node):
            if child not in pos:
                pos[child] = None
                dfs(child, depth + 1)

    pos[root] = None
    dfs(root, 0)

    for depth in levels:
        n = len(levels[depth])
        for i, node in enumerate(levels[depth]):
            x = i * x_spacing - (n - 1) * x_spacing / 2
            y = -depth * y_spacing
            pos[node] = np.array([x, y, 0])
    return pos
