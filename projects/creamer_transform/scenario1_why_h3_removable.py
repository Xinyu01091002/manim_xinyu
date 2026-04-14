import numpy as np

from manim import *


DEEP = BLUE_C
NONLINEAR = ORANGE
TRANSFORMED = TEAL_C
ACCENT = YELLOW
MUTED = GREY_B
PANEL = GREY_D
ORDER4 = RED_C


def card(mob, color=PANEL, buff=0.24):
    return VGroup(
        SurroundingRectangle(
            mob,
            color=color,
            buff=buff,
            corner_radius=0.12,
            stroke_width=1.5,
        ),
        mob,
    )


def fit_to_width(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def chip(tex, note, color, width=2.8):
    main = fit_to_width(MathTex(tex, font_size=28, color=color), width)
    sub = fit_to_width(Tex(note, font_size=18, color=WHITE), width + 0.1)
    block = VGroup(main, sub).arrange(DOWN, buff=0.12)
    return card(block, color=color, buff=0.2)


class WhyH3Removable(Scene):
    def construct(self):
        title = Text("Scenario 1: Why I Start With H3", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        self.play(Write(title), run_time=1.2)

        # Beat 1: why start with H3?
        beat1_title = Text("If I want the first nonlinear improvement, I should look at H3 first", font_size=23, color=WHITE)
        h_line = MathTex(r"H = H_2 + H_3 + H_4 + \cdots", font_size=42, color=WHITE)
        h_line.set_color_by_tex(r"H_2", DEEP)
        h_line.set_color_by_tex(r"H_3", NONLINEAR)
        h_line.set_color_by_tex(r"H_4", ORDER4)

        chip_h2 = chip(r"H_2", r"quadratic piece \\ already the linear dynamics", DEEP, width=3.0)
        chip_h3 = chip(r"H_3", r"first genuinely nonlinear correction", NONLINEAR, width=3.1)
        chip_h4 = chip(r"H_4", r"higher order \\ not where I start", ORDER4, width=2.8)
        chip_row = VGroup(chip_h2, chip_h3, chip_h4).arrange(RIGHT, buff=0.28, aligned_edge=UP)

        target_note = Tex(
            r"So if I am choosing a better representation at the lowest nonlinear order, $H_3$ is the natural first target.",
            font_size=22,
            color=ACCENT,
        )
        target_note.set_color_by_tex(r"$H_3$", NONLINEAR)

        beat1 = VGroup(beat1_title, h_line, chip_row, target_note).arrange(DOWN, buff=0.28)
        beat1.move_to(DOWN * 0.18)

        self.play(FadeIn(beat1_title, shift=UP * 0.08), run_time=1.15)
        self.play(Write(h_line), run_time=1.15)
        self.play(
            FadeIn(chip_h2, shift=UP * 0.08),
            FadeIn(chip_h3, shift=UP * 0.08),
            FadeIn(chip_h4, shift=UP * 0.08),
            run_time=1.2,
        )
        self.play(Indicate(chip_h3[1][0], color=NONLINEAR), FadeIn(target_note, shift=UP * 0.06), run_time=1.2)
        self.wait(3.8)

        # Beat 2: closure vs resonance
        beat2_title = Text("But here is the distinction I need", font_size=24, color=WHITE)

        closure_head = Text("Triad closure", font_size=22, color=MUTED)
        closure_eq = MathTex(r"k_1 + k_2 = k_3", font_size=34, color=NONLINEAR)
        closure_eq.set_color_by_tex(r"k_1", DEEP)
        closure_eq.set_color_by_tex(r"k_2", ACCENT)
        closure_eq.set_color_by_tex(r"k_3", TRANSFORMED)

        arrow_1 = Arrow(LEFT * 1.6 + DOWN * 0.25, LEFT * 0.25 + DOWN * 0.25, buff=0, color=DEEP, stroke_width=5)
        arrow_2 = Arrow(LEFT * 0.25 + DOWN * 0.25, RIGHT * 0.85 + UP * 0.45, buff=0, color=ACCENT, stroke_width=5)
        arrow_3 = Arrow(LEFT * 1.6 + DOWN * 0.25, RIGHT * 0.85 + UP * 0.45, buff=0, color=TRANSFORMED, stroke_width=5)
        plus = Text("+", font_size=22, color=WHITE).move_to(LEFT * 0.02 + DOWN * 0.48)
        equals = Text("=", font_size=22, color=WHITE).move_to(RIGHT * 1.05 + DOWN * 0.1)
        closure_geom = VGroup(arrow_1, arrow_2, plus, equals, arrow_3)
        closure_note = Tex(r"just says the $k$-vectors close geometrically", font_size=18, color=WHITE)
        closure_block = VGroup(closure_head, closure_eq, closure_geom, closure_note).arrange(DOWN, buff=0.16)
        closure_panel = card(closure_block, color=NONLINEAR, buff=0.22)

        resonance_head = Text("Triad resonance", font_size=22, color=MUTED)
        resonance_eq = MathTex(r"\omega_1 + \omega_2 = \omega_3\ ?", font_size=34, color=DEEP)
        resonance_note = Tex(r"this is the real dynamical test", font_size=18, color=WHITE)
        resonance_note_2 = Tex(r"closure alone does not guarantee resonance", font_size=18, color=ACCENT)
        resonance_block = VGroup(
            resonance_head,
            resonance_eq,
            resonance_note,
            resonance_note_2,
        ).arrange(DOWN, buff=0.18)
        resonance_panel = card(resonance_block, color=DEEP, buff=0.22)

        beat2_row = VGroup(closure_panel, resonance_panel).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        beat2 = VGroup(beat2_title, beat2_row).arrange(DOWN, buff=0.24)
        beat2.move_to(DOWN * 0.18)

        self.play(FadeOut(beat1, shift=UP * 0.08), run_time=1.05)
        self.play(FadeIn(beat2_title, shift=UP * 0.08), run_time=1.1)
        self.play(FadeIn(closure_panel, shift=RIGHT * 0.08), FadeIn(resonance_panel, shift=LEFT * 0.08), run_time=1.25)
        self.wait(4.0)

        # Beat 3: deep-water special case
        beat3_title = Text("Deep water is special because those two tests split apart", font_size=24, color=WHITE)
        disp_head = Text("Deep-water dispersion", font_size=22, color=MUTED)
        disp_eq = MathTex(r"\omega(k) = \sqrt{g\,|k|}", font_size=38, color=DEEP)

        closure_line = MathTex(r"k_1 + k_2 = k_3", font_size=30, color=WHITE)
        closure_line.set_color_by_tex(r"k_1", DEEP)
        closure_line.set_color_by_tex(r"k_2", ACCENT)
        closure_line.set_color_by_tex(r"k_3", TRANSFORMED)

        fail_line = MathTex(
            r"\sqrt{|k_1|} + \sqrt{|k_2|} \neq \sqrt{|k_1 + k_2|}",
            font_size=30,
            color=ACCENT,
        )
        fail_line.set_color_by_tex(r"k_1", DEEP)
        fail_line.set_color_by_tex(r"k_2", ACCENT)

        sign_line = MathTex(r"\pm \omega_1 \pm \omega_2 \pm \omega_3 \neq 0", font_size=34, color=NONLINEAR)
        sign_note = Tex(r"so the cubic frequency denominators stay finite", font_size=19, color=TRANSFORMED)
        sign_note_2 = Tex(r"the triad is allowed in $k$-space, but it is not an exact deep-water 3-wave resonance", font_size=19, color=WHITE)

        beat3_block = VGroup(
            beat3_title,
            disp_head,
            disp_eq,
            closure_line,
            fail_line,
            sign_line,
            sign_note,
            sign_note_2,
        ).arrange(DOWN, buff=0.16)
        beat3_panel = card(beat3_block, color=DEEP, buff=0.26)
        beat3_panel.move_to(DOWN * 0.16)

        self.play(FadeOut(beat2, shift=UP * 0.08), run_time=1.05)
        self.play(FadeIn(beat3_panel, shift=UP * 0.08), run_time=1.25)
        self.wait(5.0)

        # Beat 4: consequence and teaser
        beat4_title = Text("So H3 is exactly the first nonlinear piece I would try to absorb", font_size=24, color=WHITE)

        state_1 = chip(r"H_3", r"really there in the Hamiltonian", NONLINEAR, width=3.15)
        state_2 = chip(r"\text{non-resonant}", r"deep-water denominators stay finite", ACCENT, width=3.45)
        state_3 = chip(r"\text{removable}", r"good candidate for a better variable choice", TRANSFORMED, width=3.65)

        arrow_12 = Arrow(ORIGIN, RIGHT * 0.95, color=ACCENT, buff=0, stroke_width=5)
        arrow_23 = Arrow(ORIGIN, RIGHT * 0.95, color=ACCENT, buff=0, stroke_width=5)
        top_chain = VGroup(state_1, arrow_12, state_2, arrow_23, state_3).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)

        bridge_q = Tex(
            r"So the next question is: what near-identity variable change can absorb this non-resonant $H_3$?",
            font_size=20,
            color=WHITE,
        )
        bridge_q.set_color_by_tex(r"$H_3$", NONLINEAR)
        bridge_note = Tex(
            r"That is where the canonical transform enters, but I do not need that machinery yet.",
            font_size=20,
            color=ACCENT,
        )
        next_line = Text("Next scene: how to absorb H3", font_size=22, color=TRANSFORMED, weight=BOLD)

        beat4_block = VGroup(
            beat4_title,
            top_chain,
            bridge_q,
            bridge_note,
            next_line,
        ).arrange(DOWN, buff=0.24)
        beat4_panel = card(beat4_block, color=TRANSFORMED, buff=0.28)
        beat4_panel.move_to(DOWN * 0.18)

        self.play(FadeOut(beat3_panel, shift=UP * 0.08), run_time=1.05)
        self.play(FadeIn(beat4_panel, shift=UP * 0.08), run_time=1.25)
        self.play(Indicate(next_line, color=ACCENT), run_time=1.1)
        self.wait(4.8)
