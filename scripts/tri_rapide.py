from manim import (
    Scene,
    Text,
    Square,
    BLUE,
    GREEN,
    RED,
    GOLD,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    VGroup,
    FadeIn,
    FadeOut,
)


class TriRapide(Scene):
    def __init__(self, tab, **kwargs):
        super().__init__(**kwargs)
        self.tab = tab

    def construct(self):
        width = 1.0
        delai = 0.4
        rects = []
        labels = []

        # Création des carrés et labels
        n = len(self.tab)  # Define 'n' as the length of the tab
        rects = [Square(1).set_fill(BLUE, 1) for _ in range(n)]
        labels = [Text(str(self.tab[i]), font_size=24) for i in range(n)]

        for i in range(n):
            rects[i].move_to(RIGHT * i * width)
            labels[i].move_to(rects[i])

        # Groupe global pour centrage
        group = VGroup(*rects, *labels).move_to(ORIGIN)
        self.play(FadeIn(group), run_time=delai)

        self.wait(delai)

        def tri(indices):
            if len(indices) <= 1:
                return

            self.wait(delai)

            piv = indices[0]
            left = [i for i in indices if self.tab[i] < self.tab[piv]]
            mid = [i for i in indices if self.tab[i] == self.tab[piv]]
            right = [i for i in indices if self.tab[i] > self.tab[piv]]
            other = [i for i in range(n) if i not in indices]
            other_group = VGroup(
                *[rects[i] for i in other], *[labels[i] for i in other]
            )

            if other:
                self.play(FadeOut(other_group), run_time=delai)
                self.wait(delai)

            # Coloration
            self.play(
                *[rects[i].animate.set_fill(GREEN) for i in left],
                *[rects[i].animate.set_fill(RED) for i in right],
                *[rects[i].animate.set_fill(GOLD) for i in mid],
                run_time=delai,
            )

            self.wait(delai)

            # Déplacement vertical (optionnel, pour effet visuel)
            if left or right:
                self.play(
                    *[rects[i].animate.shift(UP * width) for i in left],
                    *[labels[i].animate.shift(UP * width) for i in left],
                    *[rects[i].animate.shift(DOWN * width) for i in right],
                    *[labels[i].animate.shift(DOWN * width) for i in right],
                    run_time=delai,
                )

            self.wait(delai)

            # Déplacement horizontal relatif
            new_order = left + mid + right
            self.play(
                *[
                    rects[i].animate.shift(
                        RIGHT * (new_order.index(i) - indices.index(i))
                    )
                    for i in indices
                ],
                *[
                    labels[i].animate.shift(
                        RIGHT * (new_order.index(i) - indices.index(i))
                    )
                    for i in indices
                ],
                run_time=delai,
            )

            self.wait(delai)

            # Retour vertical
            if left or right:
                self.play(
                    *[rects[i].animate.shift(DOWN * width) for i in left],
                    *[labels[i].animate.shift(DOWN * width) for i in left],
                    *[rects[i].animate.shift(UP * width) for i in right],
                    *[labels[i].animate.shift(UP * width) for i in right],
                    run_time=delai,
                )

            # Remise en couleur
            self.play(*[rects[i].animate.set_fill(BLUE) for i in indices], run_time=0.1)
            self.wait(delai)

            if other:
                self.play(FadeIn(other_group), run_time=delai)
                self.wait(delai)

            # Appel récursif
            tri(left)
            tri(right)

        tri(list(range(n)))
