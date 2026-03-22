from manim import (
    Scene,
    Square,
    Text,
    VGroup,
    FadeIn,
    FadeOut,
    ORIGIN,
    RIGHT,
    BLUE,
    WHITE,
    GREEN,
    RED,
    GOLD,
    Create,
    UP,
    DOWN,
)


class RechercheDicho(Scene):
    def __init__(self, tab, elt, **kwargs):
        super().__init__(**kwargs)
        self.tab = tab
        self.elt = elt

    def construct(self):
        width = 1.0

        # Création des rectangles avec les nombres
        rects = []
        labels = []
        for i, val in enumerate(self.tab):
            rect = (
                Square(side_length=width)
                .set_fill(BLUE, opacity=1.0)
                .shift(RIGHT * i * width)
            )
            label = Text(str(val), color=WHITE).move_to(rect)
            rects.append(rect)
            labels.append(label)

        group = VGroup(*rects, *labels).move_to(ORIGIN)
        self.play(
            FadeIn(group),
            FadeIn(Text("Recherche de " + str(self.elt)).to_edge(DOWN, buff=1.0)),
            run_time=0.5,
        )

        # Début de la recherche dichotomique
        g = 0
        d = len(self.tab) - 1

        while g <= d:
            m = (g + d) // 2

            self.play(rects[m].animate.set_fill(GOLD), run_time=0.5)
            self.wait(0.5)
            if self.tab[m] == self.elt:
                self.play(
                    Create(Text("Élément trouvé", color=GREEN).to_edge(UP)),
                    rects[m].animate.set_fill(GREEN),
                    run_time=0.5,
                )
                self.wait(0.5)
                break
            elif self.elt < self.tab[m]:
                self.play(
                    *[FadeOut(rects[i]) for i in range(m, d + 1)],
                    *[FadeOut(labels[i]) for i in range(m, d + 1)],
                    run_time=0.5,
                )
                self.wait(0.5)
                d = m - 1
            else:
                self.play(
                    *[FadeOut(rects[i]) for i in range(g, m + 1)],
                    *[FadeOut(labels[i]) for i in range(g, m + 1)],
                    run_time=0.5,
                )
                self.wait(0.5)
                g = m + 1
            self.wait(0.5)

        if g > d:
            self.play(
                Create(Text("Élément non trouvé", color=RED).move_to(ORIGIN)),
                run_time=0.5,
            )
            self.wait(0.5)
