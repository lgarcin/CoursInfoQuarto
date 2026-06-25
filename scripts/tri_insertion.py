from manim import (
    Scene,
    Square,
    Text,
    VGroup,
    FadeIn,
    LEFT,
    RIGHT,
    ORIGIN,
    BLUE,
    RED,
    GREEN,
    UP,
    DOWN,
)


class TriInsertion(Scene):
    def __init__(self, tab, **kwargs):
        super().__init__(**kwargs)
        self.tab = tab

    def construct(self):
        n = len(self.tab)
        width = 1.0
        delai = 0.2

        # Création des carrés et labels
        rects = [Square(1).set_fill(BLUE, 1) for _ in range(n)]
        labels = [Text(str(self.tab[i]), font_size=24) for i in range(n)]

        for i in range(n):
            rects[i].move_to(RIGHT * i * width)
            labels[i].move_to(rects[i])

        # Groupe global pour centrage
        group = VGroup(*rects, *labels).move_to(ORIGIN)
        self.play(FadeIn(group), run_time=delai)

        self.play(
            rects[0].animate.set_fill(GREEN),
            run_time=delai,
        )

        # Indices logique → visuel
        indices = list(range(n))

        for i in range(1, n):
            self.play(
                rects[indices[i]].animate.set_fill(RED),
                run_time=delai,
            )
            self.play(
                rects[indices[i]].animate.shift(UP),
                labels[indices[i]].animate.shift(UP),
                run_time=delai,
            )
            index = indices[i]
            val = self.tab[index]
            pos = i
            while pos > 0 and self.tab[indices[pos - 1]] > val:
                pos -= 1
                self.play(
                    rects[indices[pos]].animate.shift(RIGHT * width),
                    labels[indices[pos]].animate.shift(RIGHT * width),
                    rects[index].animate.shift(LEFT * width),
                    labels[index].animate.shift(LEFT * width),
                    run_time=delai,
                )
                indices[pos + 1] = indices[pos]
            indices[pos] = index
            self.play(
                rects[index].animate.shift(DOWN),
                labels[index].animate.shift(DOWN),
                run_time=delai,
            )
            self.play(
                rects[indices[pos]].animate.set_fill(GREEN),
                run_time=delai,
            )
