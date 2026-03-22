from manim import (
    Scene,
    Square,
    Text,
    VGroup,
    FadeIn,
    FadeOut,
    Create,
    Uncreate,
    LEFT,
    RIGHT,
    UP,
    BLUE,
)


class Queue(Scene):
    def construct(self):
        self.width = 1.0
        self.delai = 0.5
        self.queue = []
        for letter in "A", "B", "C", "D", "E":
            self.enqueue(self.create_element(letter))
            self.wait(1)
        self.dequeue()
        self.wait(1)
        self.enqueue(self.create_element("F"))
        self.wait(1)
        self.dequeue()
        self.wait(1)
        self.dequeue()
        self.wait(1)
        self.dequeue()
        self.wait(1)

    def create_element(self, letter):
        square = Square(self.width).set_fill(BLUE, opacity=1.0)
        text = Text(letter).move_to(square)
        group = VGroup(square, text)
        return group

    def enqueue(self, element):
        text = Text("Enfilage d'un élément").to_edge(UP)
        self.play(
            Create(text),
            FadeIn(element.to_edge(RIGHT)),
            run_time=self.delai,
        )
        self.wait(0.5)
        self.play(
            element.animate.move_to(self.queue[-1].get_center() + RIGHT * self.width)
            if self.queue
            else element.animate.to_edge(LEFT).shift(RIGHT * self.width),
            run_time=self.delai,
        )
        self.play(
            Uncreate(text),
            run_time=self.delai,
        )
        self.queue.append(element)

    def dequeue(self):
        if not self.queue:
            return
        text = Text("Défilage d'un élément").to_edge(UP)
        element = self.queue.pop(0)
        self.play(
            Create(text),
            run_time=self.delai,
        )
        self.play(
            element.animate.to_edge(LEFT),
            run_time=self.delai,
        )
        self.wait(0.5)
        self.play(
            Uncreate(text),
            FadeOut(element),
            run_time=self.delai,
        )
