from manim import (
    Scene,
    Square,
    Text,
    VGroup,
    FadeIn,
    FadeOut,
    Create,
    Uncreate,
    RIGHT,
    LEFT,
    ORIGIN,
    UP,
    BLUE,
)


class Stack(Scene):
    def construct(self):
        self.width = 1.0
        self.delai = 0.5
        self.stack = []
        for letter in "A", "B", "C", "D", "E":
            self.push(self.create_element(letter))
            self.wait(1)
        self.pop()
        self.wait(1)
        self.push(self.create_element("F"))
        self.wait(1)
        self.pop()
        self.wait(1)
        self.pop()
        self.wait(1)
        self.pop()
        self.wait(1)

    def create_element(self, letter):
        square = Square(self.width).set_fill(BLUE, opacity=1.0)
        text = Text(letter).move_to(square)
        group = VGroup(square, text)
        return group

    def push(self, element):
        text = Text("Empilement d'un élément").to_edge(UP)
        self.play(
            Create(text),
            FadeIn(element.to_edge(RIGHT)),
            run_time=self.delai,
        )
        self.wait(0.5)
        self.play(
            element.animate.move_to(self.stack[-1].get_center() + RIGHT * self.width)
            if self.stack
            else element.animate.to_edge(LEFT),
            run_time=self.delai,
        )
        self.play(
            Uncreate(text),
            run_time=self.delai,
        )
        self.stack.append(element)

    def pop(self):
        if not self.stack:
            return
        text = Text("Dépilement d'un élément").to_edge(UP)
        element = self.stack.pop()
        self.play(
            Create(text),
            run_time=self.delai,
        )
        self.play(
            element.animate.to_edge(RIGHT),
            run_time=self.delai,
        )
        self.wait(0.5)
        self.play(
            Uncreate(text),
            FadeOut(element),
            run_time=self.delai,
        )
