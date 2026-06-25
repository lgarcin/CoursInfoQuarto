from manim import (
    Scene,
    Square,
    Text,
    VGroup,
    ORIGIN,
    RIGHT,
    LEFT,
    DOWN,
    UP,
    BLUE,
    GOLD,
    GREEN,
    FadeIn,
)


class TriBulles(Scene):
    def __init__(self, tab, **kwargs):
        super().__init__(**kwargs)
        self.tab = tab

    def construct(self):
        n = len(self.tab)
        width = 1.0

        # Création des rectangles avec annotations
        rects = [
            Square(side_length=width)
            .set_fill(BLUE, opacity=1)
            .move_to(RIGHT * i * width)
            for i in range(n)
        ]
        labels = [
            Text(str(self.tab[i]), font_size=24).move_to(rects[i]) for i in range(n)
        ]
        group = VGroup(*rects, *labels).move_to(ORIGIN)
        delai = 0.2
        self.play(FadeIn(group), run_time=delai)

        # Tri à bulles avec animation
        for i in reversed(range(n)):
            for j in range(i):
                # Coloration pour comparaison
                self.play(
                    rects[j].animate.set_fill(GOLD),
                    rects[j + 1].animate.set_fill(GOLD),
                    run_time=delai,
                )
                self.wait(delai)

                if self.tab[j + 1] < self.tab[j]:
                    # Échange
                    self.play(
                        rects[j].animate.shift(DOWN * width / 2),
                        rects[j + 1].animate.shift(UP * width / 2),
                        labels[j].animate.shift(DOWN * width / 2),
                        labels[j + 1].animate.shift(UP * width / 2),
                        run_time=delai,
                    )

                    self.play(
                        rects[j].animate.shift(RIGHT * width),
                        rects[j + 1].animate.shift(LEFT * width),
                        labels[j].animate.shift(RIGHT * width),
                        labels[j + 1].animate.shift(LEFT * width),
                        run_time=delai,
                    )

                    self.play(
                        rects[j].animate.shift(UP * width / 2),
                        rects[j + 1].animate.shift(DOWN * width / 2),
                        labels[j].animate.shift(UP * width / 2),
                        labels[j + 1].animate.shift(DOWN * width / 2),
                        run_time=delai,
                    )

                    # Mise à jour de l'ordre
                    rects[j], rects[j + 1] = rects[j + 1], rects[j]
                    labels[j], labels[j + 1] = labels[j + 1], labels[j]
                    self.tab[j], self.tab[j + 1] = self.tab[j + 1], self.tab[j]

                self.play(
                    rects[j].animate.set_fill(BLUE),
                    rects[j + 1].animate.set_fill(BLUE),
                    run_time=delai,
                )

            self.play(rects[i].animate.set_fill(GREEN), run_time=delai)
