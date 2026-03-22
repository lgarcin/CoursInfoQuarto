from manim import (
    Scene,
    Square,
    BLUE,
    RED,
    GREEN,
    RIGHT,
    ORIGIN,
    VGroup,
    Text,
    FadeIn,
    UP,
    DOWN,
)


class TriFusion(Scene):
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

        indices = list(range(n))

        def tri(a, b):
            if b - a <= 1:
                return
            tri(a, (a + b) // 2)
            tri((a + b) // 2, b)

            local_indices = indices[a:b]
            left = local_indices[: len(local_indices) // 2]
            right = local_indices[len(local_indices) // 2 :]

            self.play(
                *[rects[i].animate.set_fill(RED) for i in left],
                *[rects[i].animate.set_fill(GREEN) for i in right],
                run_time=delai,
            )

            self.play(
                *[rects[i].animate.shift(UP * width / 2) for i in left],
                *[labels[i].animate.shift(UP * width / 2) for i in left],
                *[rects[i].animate.shift(DOWN * width / 2) for i in right],
                *[labels[i].animate.shift(DOWN * width / 2) for i in right],
                run_time=delai,
            )

            sorted_local_indices = sorted(local_indices, key=lambda i: self.tab[i])
            indices[a:b] = sorted_local_indices

            self.play(
                *[
                    rects[i].animate.shift(
                        RIGHT * (sorted_local_indices.index(i) - local_indices.index(i))
                    )
                    for i in local_indices
                ],
                *[
                    labels[i].animate.shift(
                        RIGHT * (sorted_local_indices.index(i) - local_indices.index(i))
                    )
                    for i in local_indices
                ],
                run_time=delai,
            )

            self.play(
                *[rects[i].animate.shift(DOWN * width / 2) for i in left],
                *[labels[i].animate.shift(DOWN * width / 2) for i in left],
                *[rects[i].animate.shift(UP * width / 2) for i in right],
                *[labels[i].animate.shift(UP * width / 2) for i in right],
                run_time=delai,
            )

            self.play(
                *[rects[i].animate.set_fill(BLUE) for i in local_indices],
                run_time=delai,
            )

        tri(0, n)
