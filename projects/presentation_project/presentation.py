from manim import *
import numpy as np

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene

BG = ManimColor("#0F172A")
FG = "#E2E8F0"
ACCENT = "#38BDF8"
ACCENT2 = "#22C55E"
MUTED = "#94A3B8"


class TitleSlide(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("Project Presentation", font_size=72, color=FG, weight=BOLD)
        subtitle = Text("Built with Manim", font_size=36, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.35)
        underline = Line(LEFT * 3.2, RIGHT * 3.2, color=ACCENT, stroke_width=6)
        underline.next_to(subtitle, DOWN, buff=0.6)
        self.play(FadeIn(title, shift=UP * 0.25), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), Create(underline), run_time=0.8)
        self.wait(1.2)


class AgendaSlide(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = Text("Agenda", font_size=58, color=FG, weight=BOLD).to_edge(UP, buff=0.7)
        items = VGroup(
            Text("1. Problem", font_size=42, color=FG),
            Text("2. Method", font_size=42, color=FG),
            Text("3. Results", font_size=42, color=FG),
            Text("4. Next Steps", font_size=42, color=FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        items.move_to(LEFT * 1.4 + DOWN * 0.3)
        marker = Dot(radius=0.08, color=ACCENT2)

        self.play(Write(header), run_time=0.6)
        for item in items:
            marker.next_to(item, LEFT, buff=0.35)
            self.play(FadeIn(item, shift=RIGHT * 0.2), FadeIn(marker, scale=0.7), run_time=0.35)
        self.wait(1)


class ResultsSlide(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = Text("Results Snapshot", font_size=56, color=FG, weight=BOLD).to_edge(UP, buff=0.6)

        ax = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=8,
            y_length=4.2,
            axis_config={"color": MUTED, "include_numbers": True, "font_size": 24},
            tips=False,
        )
        ax.shift(DOWN * 0.6)

        curve = ax.plot(lambda x: 1 - np.exp(-x / 2.8), color=ACCENT, stroke_width=6)
        label = Text("Convergence", font_size=28, color=ACCENT).next_to(ax, RIGHT, buff=0.6)

        self.play(Write(header), run_time=0.6)
        self.play(Create(ax), run_time=0.9)
        self.play(Create(curve), FadeIn(label, shift=LEFT * 0.2), run_time=1.1)
        self.wait(1.2)


class Deck(Slide):
    def _slide_break(self):
        if hasattr(self, "next_slide"):
            self.next_slide(loop=False)

    def _show_title(self):
        title = Text("Project Presentation", font_size=72, color=FG, weight=BOLD)
        subtitle = Text("Built with Manim", font_size=36, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.35)
        underline = Line(LEFT * 3.2, RIGHT * 3.2, color=ACCENT, stroke_width=6)
        underline.next_to(subtitle, DOWN, buff=0.6)

        self.play(FadeIn(title, shift=UP * 0.25), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), Create(underline), run_time=0.8)
        self._slide_break()
        self.play(FadeOut(VGroup(title, subtitle, underline)), run_time=0.4)

    def _show_agenda(self):
        header = Text("Agenda", font_size=58, color=FG, weight=BOLD).to_edge(UP, buff=0.7)
        items = VGroup(
            Text("1. Problem", font_size=42, color=FG),
            Text("2. Method", font_size=42, color=FG),
            Text("3. Results", font_size=42, color=FG),
            Text("4. Next Steps", font_size=42, color=FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        items.move_to(LEFT * 1.4 + DOWN * 0.3)

        self.play(Write(header), run_time=0.6)
        for item in items:
            marker = Dot(radius=0.08, color=ACCENT2).next_to(item, LEFT, buff=0.35)
            self.play(FadeIn(item, shift=RIGHT * 0.2), FadeIn(marker, scale=0.7), run_time=0.3)
        self._slide_break()
        self.play(FadeOut(VGroup(header, items)), run_time=0.35)

    def _show_results(self):
        header = Text("Results Snapshot", font_size=56, color=FG, weight=BOLD).to_edge(UP, buff=0.6)
        ax = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=8,
            y_length=4.2,
            axis_config={"color": MUTED, "include_numbers": True, "font_size": 24},
            tips=False,
        )
        ax.shift(DOWN * 0.6)
        curve = ax.plot(lambda x: 1 - np.exp(-x / 2.8), color=ACCENT, stroke_width=6)
        label = Text("Convergence", font_size=28, color=ACCENT).next_to(ax, RIGHT, buff=0.6)

        self.play(Write(header), run_time=0.6)
        self.play(Create(ax), run_time=0.8)
        self.play(Create(curve), FadeIn(label, shift=LEFT * 0.2), run_time=1.0)
        self._slide_break()

    def construct(self):
        self.camera.background_color = BG
        self._show_title()
        self._show_agenda()
        self._show_results()
