from manim import (
    Scene,
    Square,
    Text,
    BLUE,
    YELLOW,
    GREEN,
    RED,
    RIGHT,
    DOWN,
    UP,
    VGroup,
    ORIGIN,
)


class RechercheMotif(Scene):
    def __init__(self, chaine, motif, **kwargs):
        super().__init__(**kwargs)
        self.chaine = chaine
        self.motif = motif

    def construct(self):
        # === Paramètres ===
        case_size = 1.0
        motif_offset = 1.5  # Distance verticale entre chaîne et motif

        # === Fonctions utilitaires ===
        def create_boxes(texte, y_offset, color=BLUE, opacity=0.3):
            objets = []
            for i, char in enumerate(texte):
                box = (
                    Square(case_size)
                    .set_fill(color, opacity)
                    .move_to(RIGHT * i * case_size)
                )
                box.shift(DOWN * y_offset)
                label = Text(char).scale(0.8).move_to(box.get_center())
                self.add(box, label)
                objets.append((box, label))
            return objets

        def move_group(group, dx=0, dy=0, duration=0.3):
            anims = []
            for box, txt in group:
                anims.append(box.animate.shift(RIGHT * dx + UP * dy))
                anims.append(txt.animate.shift(RIGHT * dx + UP * dy))
            if anims:
                self.play(*anims, run_time=duration)

        def highlight_boxes(group, indices, color, duration=0.3):
            anims = [group[i][0].animate.set_fill(color, opacity=0.5) for i in indices]
            if anims:
                self.play(*anims, run_time=duration)

        # === Création des éléments ===
        cases_chaine = create_boxes(self.chaine, y_offset=0)
        cases_motif = create_boxes(
            self.motif, y_offset=-motif_offset, color=YELLOW, opacity=0.5
        )
        groupe_total = VGroup(
            *[item for pair in cases_chaine for item in pair],
            *[item for pair in cases_motif for item in pair],
        )
        groupe_total.move_to(ORIGIN)

        self.wait(0.5)

        # === Recherche animée ===
        n, m = len(self.chaine), len(self.motif)
        for ind in range(n - m + 1):
            nb = 0
            while nb < m and self.chaine[ind + nb] == self.motif[nb]:
                move_group([cases_chaine[ind + nb]], dy=+motif_offset)
                nb += 1

            if nb == m:
                highlight_boxes(cases_chaine, range(ind, ind + m), GREEN)
                break
            else:
                move_group([cases_chaine[ind + k] for k in range(nb)], dy=-motif_offset)
                move_group(cases_motif, dx=1)

        else:
            highlight_boxes(cases_chaine, range(n), RED)

        self.wait(1)
