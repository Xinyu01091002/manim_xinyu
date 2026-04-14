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


def chip(tex, note, color, width=3.0):
    main = fit_to_width(MathTex(tex, font_size=28, color=color), width)
    sub = fit_to_width(Tex(note, font_size=18, color=WHITE), width + 0.1)
    block = VGroup(main, sub).arrange(DOWN, buff=0.12)
    return card(block, color=color, buff=0.2)


class HowToAbsorbH3(Scene):
    def construct(self):
        title = Text("Scenario 2: How I Absorb H3", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        self.play(Write(title), run_time=1.2)

        # Beat 1: set up the question
        beat1_title = Text(
            "Now I can ask what variable change actually removes a non-resonant H3",
            font_size=23,
            color=WHITE,
        )

        old_head = Text("physical variables", font_size=20, color=MUTED)
        old_pair = MathTex(r"(\zeta,\phi_s)", font_size=38, color=DEEP)
        old_note = Tex(r"the original canonical pair", font_size=19, color=WHITE)
        old_block = VGroup(old_head, old_pair, old_note).arrange(DOWN, buff=0.14)
        old_panel = card(old_block, color=DEEP, buff=0.22)

        map_arrow = Arrow(LEFT * 0.9, RIGHT * 0.9, buff=0, color=ACCENT, stroke_width=5)
        map_label = Tex(r"near-identity canonical map", font_size=22, color=ACCENT)
        map_block = VGroup(map_arrow, map_label).arrange(DOWN, buff=0.16)

        new_head = Text("better variables", font_size=20, color=MUTED)
        new_pair = MathTex(r"(\bar{\zeta},\bar{\phi}_s)", font_size=38, color=TRANSFORMED)
        new_note = Tex(r"same physics, simpler retained dynamics", font_size=19, color=WHITE)
        new_block = VGroup(new_head, new_pair, new_note).arrange(DOWN, buff=0.14)
        new_panel = card(new_block, color=TRANSFORMED, buff=0.22)

        bridge_global = Tex(r"the paper first writes a global generating functional $F$", font_size=19, color=MUTED)
        bridge_local = Tex(r"here I switch to the Lie-flow view because it is easier to explain order by order", font_size=19, color=ACCENT)

        beat1_row = VGroup(old_panel, map_block, new_panel).arrange(RIGHT, buff=0.34, aligned_edge=DOWN)
        beat1 = VGroup(beat1_title, beat1_row, bridge_global, bridge_local).arrange(DOWN, buff=0.24)
        beat1.move_to(DOWN * 0.2)

        self.play(FadeIn(beat1_title, shift=UP * 0.08), run_time=1.1)
        self.play(FadeIn(old_panel, shift=RIGHT * 0.08), FadeIn(new_panel, shift=LEFT * 0.08), FadeIn(map_block), run_time=1.25)
        self.play(FadeIn(bridge_global, shift=UP * 0.06), FadeIn(bridge_local, shift=UP * 0.06), run_time=1.0)
        self.wait(3.8)

        # Beat 2: Poisson bracket first
        beat2_title = Text("First I need the Poisson bracket", font_size=24, color=WHITE)
        pb_def = MathTex(
            r"\{A,B\}=\int d^2x\left["
            r"\frac{\delta A}{\delta \zeta(x)}\frac{\delta B}{\delta \phi_s(x)}"
            r"-"
            r"\frac{\delta A}{\delta \phi_s(x)}\frac{\delta B}{\delta \zeta(x)}"
            r"\right]",
            font_size=34,
            color=WHITE,
        )
        fit_to_width(pb_def, 10.6)
        pb_def.set_color_by_tex(r"\zeta", DEEP)
        pb_def.set_color_by_tex(r"\phi_s", TRANSFORMED)

        pb_note_1 = Tex(r"this is the Hamiltonian structure on the pair $(\zeta,\phi_s)$", font_size=20, color=WHITE)
        pb_note_2 = Tex(r"if I generate a variable change through this bracket, the transform stays canonical", font_size=20, color=ACCENT)
        canon_line = MathTex(r"\text{Poisson bracket} \;\Longrightarrow\; \text{canonical transform}", font_size=30, color=ACCENT)

        beat2_block = VGroup(beat2_title, pb_def, pb_note_1, pb_note_2, canon_line).arrange(DOWN, buff=0.22)
        beat2_panel = card(beat2_block, color=ACCENT, buff=0.26)
        beat2_panel.move_to(DOWN * 0.16)

        self.play(FadeOut(beat1, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat2_panel, shift=UP * 0.08), run_time=1.2)
        self.wait(4.6)

        # Beat 3: auxiliary lambda-flow with integration feel
        beat3_title = Text("Then I integrate that canonical flow from lambda = 0 to lambda = 1", font_size=24, color=WHITE)
        flow_eq = MathTex(r"\partial_{\lambda} A = \{A, W\}", font_size=40, color=ACCENT)

        step_eq = MathTex(
            r"A(\lambda+\Delta\lambda)=A(\lambda)+\Delta\lambda\,\{A,W\}+O(\Delta\lambda^2)",
            font_size=29,
            color=WHITE,
        )
        fit_to_width(step_eq, 10.8)
        z_int = MathTex(
            r"\bar{\zeta}(x)=\zeta(x)+\int_0^1 \{Z(x,\lambda),W\}\,d\lambda",
            font_size=28,
            color=WHITE,
        )
        phi_int = MathTex(
            r"\bar{\phi}_s(x)=\phi_s(x)+\int_0^1 \{\Phi(x,\lambda),W\}\,d\lambda",
            font_size=28,
            color=TRANSFORMED,
        )
        fit_to_width(z_int, 10.6)
        fit_to_width(phi_int, 10.6)

        flow_line = Line(LEFT * 2.55, RIGHT * 2.55, color=PANEL, stroke_width=4)
        proportions = [0.0, 0.25, 0.5, 0.75, 1.0]
        tick_points = [flow_line.point_from_proportion(p) for p in proportions]
        ticks = VGroup(*[Line(UP * 0.13, DOWN * 0.13, color=PANEL).move_to(pt) for pt in tick_points])
        tick_labels = VGroup(
            MathTex(r"0", font_size=22, color=WHITE).next_to(ticks[0], DOWN, buff=0.08),
            MathTex(r"\Delta\lambda", font_size=20, color=ACCENT).next_to(ticks[1], DOWN, buff=0.08),
            MathTex(r"2\Delta\lambda", font_size=20, color=ACCENT).next_to(ticks[2], DOWN, buff=0.08),
            MathTex(r"\cdots", font_size=24, color=WHITE).next_to(ticks[3], DOWN, buff=0.08),
            MathTex(r"1", font_size=22, color=WHITE).next_to(ticks[4], DOWN, buff=0.08),
        )
        start_label = MathTex(r"(\zeta,\phi_s)", font_size=28, color=DEEP).next_to(ticks[0], UP, buff=0.12)
        end_label = MathTex(r"(\bar{\zeta},\bar{\phi}_s)", font_size=28, color=TRANSFORMED).next_to(ticks[4], UP, buff=0.12)
        dot = Dot(tick_points[0], radius=0.075, color=ACCENT)
        step_note = Tex(r"integrate many small canonical steps", font_size=18, color=MUTED)
        step_note.next_to(flow_line, DOWN, buff=0.5)
        lambda_track = VGroup(flow_line, ticks, tick_labels, start_label, end_label, dot, step_note)

        h0_head = Text("at lambda = 0", font_size=18, color=MUTED)
        h0_line = MathTex(r"H = H_2 + H_3 + H_4 + \cdots", font_size=28, color=WHITE)
        h0_line.set_color_by_tex(r"H_2", DEEP)
        h0_line.set_color_by_tex(r"H_3", NONLINEAR)
        h0_line.set_color_by_tex(r"H_4", ORDER4)
        h0_block = VGroup(h0_head, h0_line).arrange(DOWN, buff=0.12)
        h0_panel = card(h0_block, color=NONLINEAR, buff=0.2)

        h1_head = Text("after integrating to lambda = 1", font_size=18, color=MUTED)
        h1_line = MathTex(r"K = H_2 + H_4 + \cdots", font_size=28, color=WHITE)
        h1_line.set_color_by_tex(r"H_2", DEEP)
        h1_line.set_color_by_tex(r"H_4", ORDER4)
        h1_note = Tex(r"$H_3$ has been absorbed into the map", font_size=18, color=TRANSFORMED)
        h1_note.set_color_by_tex(r"$H_3$", NONLINEAR)
        h1_block = VGroup(h1_head, h1_line, h1_note).arrange(DOWN, buff=0.12)
        h1_panel = card(h1_block, color=TRANSFORMED, buff=0.2)

        h_row = VGroup(h0_panel, h1_panel).arrange(RIGHT, buff=0.34, aligned_edge=UP)
        fit_to_width(h_row, 12.1)

        lambda_note = Tex(r"$\lambda$ is not physical time; it only labels the canonical deformation", font_size=20, color=ACCENT)

        beat3_block = VGroup(
            beat3_title,
            flow_eq,
            step_eq,
            z_int,
            phi_int,
            lambda_track,
            h_row,
            lambda_note,
        ).arrange(DOWN, buff=0.21)
        beat3_panel = card(beat3_block, color=ACCENT, buff=0.28)
        beat3_panel.move_to(DOWN * 0.14)

        self.play(FadeOut(beat2_panel, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat3_title, shift=UP * 0.08), FadeIn(flow_eq, shift=UP * 0.06), run_time=1.15)
        self.play(FadeIn(step_eq, shift=UP * 0.05), run_time=1.0)
        self.play(FadeIn(z_int, shift=UP * 0.05), FadeIn(phi_int, shift=UP * 0.05), run_time=1.1)
        self.play(FadeIn(lambda_track), run_time=1.05)
        self.play(FadeIn(h0_panel, shift=UP * 0.05), run_time=0.9)
        self.play(dot.animate.move_to(tick_points[1]), run_time=0.7)
        self.play(dot.animate.move_to(tick_points[2]), run_time=0.7)
        self.play(dot.animate.move_to(tick_points[3]), run_time=0.7)
        self.play(dot.animate.move_to(tick_points[4]), run_time=0.8)
        self.play(FadeIn(h1_panel, shift=UP * 0.05), FadeIn(lambda_note, shift=UP * 0.05), run_time=0.95)
        self.wait(4.6)

        # Beat 4: cubic cancellation
        beat4_title = Text("This is the algebraic step that removes H3", font_size=24, color=WHITE)
        k_expand = MathTex(r"K = H_2 + H_3 - \{H_2, W\} + O(4)", font_size=40, color=WHITE)
        k_expand.set_color_by_tex(r"H_2", DEEP)
        k_expand.set_color_by_tex(r"H_3", NONLINEAR)
        k_expand.set_color_by_tex(r"W", ACCENT)
        k_expand.set_color_by_tex(r"O(4)", ORDER4)

        choose_line = MathTex(r"\text{choose }\{H_2, W\}=H_3", font_size=36, color=ACCENT)
        choose_line.set_color_by_tex(r"H_2", DEEP)
        choose_line.set_color_by_tex(r"H_3", NONLINEAR)
        choose_line.set_color_by_tex(r"W", ACCENT)

        k_cancel = MathTex(r"K = H_2 + H_3 - H_3 + O(4)", font_size=40, color=WHITE)
        k_cancel.set_color_by_tex(r"H_2", DEEP)
        k_cancel.set_color_by_tex(r"H_3", NONLINEAR)
        k_cancel.set_color_by_tex(r"O(4)", ORDER4)

        k_final = MathTex(r"K = H_2 + O(4)", font_size=46, color=WHITE)
        k_final.set_color_by_tex(r"H_2", DEEP)
        k_final.set_color_by_tex(r"O(4)", ORDER4)

        degree_note = MathTex(r"W \text{ is cubic, so }\{H_3,W\}=O(4)", font_size=28, color=WHITE)
        o4_note = Tex(r"$O(4)$ means quartic and higher terms", font_size=20, color=ORDER4)

        fit_to_width(k_expand, 10.8)
        fit_to_width(choose_line, 8.8)
        fit_to_width(k_final, 8.0)
        fit_to_width(degree_note, 9.6)
        support_block = VGroup(degree_note, o4_note).arrange(DOWN, buff=0.16)
        beat4_intro = VGroup(beat4_title, k_expand, choose_line).arrange(DOWN, buff=0.34)
        beat4_intro.move_to(DOWN * 0.02)
        k_final.move_to(k_expand.get_center())
        support_block.next_to(k_final, DOWN, buff=0.42)

        self.play(FadeOut(VGroup(beat3_title, flow_eq, step_eq, z_int, phi_int, lambda_track, h0_panel, h1_panel, lambda_note), shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat4_title, shift=UP * 0.08), FadeIn(k_expand, shift=UP * 0.05), run_time=1.15)
        self.play(FadeIn(choose_line, shift=UP * 0.05), run_time=1.0)
        self.play(TransformMatchingTex(k_expand, k_cancel), run_time=1.1)
        h3_parts = k_cancel.get_parts_by_tex(r"H_3")
        cross_group = VGroup(*[Cross(part, stroke_color=NONLINEAR, stroke_width=5) for part in h3_parts])
        self.play(Create(cross_group), run_time=0.8)
        self.play(FadeOut(choose_line, shift=UP * 0.04), FadeOut(cross_group), TransformMatchingTex(k_cancel, k_final), run_time=1.1)
        self.play(FadeIn(support_block, shift=UP * 0.05), run_time=1.0)
        self.wait(4.4)

        # Beat 5: takeaway and bridge
        beat5_title = Text("Takeaway", font_size=26, color=WHITE, weight=BOLD)
        chip_1 = chip(r"\text{Poisson bracket}", r"this is what keeps the transform canonical", DEEP, width=3.5)
        chip_2 = chip(r"\lambda:0\rightarrow1", r"integrate the canonical flow from the old variables to the new ones", ACCENT, width=3.9)
        chip_3 = chip(r"\{H_2,W\}=H_3", r"by lambda = 1 the cubic term has been absorbed", TRANSFORMED, width=3.9)

        top_row = VGroup(chip_1, chip_2, chip_3).arrange(RIGHT, buff=0.22, aligned_edge=UP)
        fit_to_width(top_row, 12.6)
        bridge = Tex(
            r"so the end result is a canonical map whose retained Hamiltonian starts at $K=H_2+O(4)$",
            font_size=22,
            color=WHITE,
        )
        bridge.set_color_by_tex(r"$K=H_2+O(4)$", TRANSFORMED)
        last_note = Tex(
            r"the nonlinearity is not gone; it is shifted out of the retained cubic dynamics",
            font_size=21,
            color=ACCENT,
        )
        next_line = Text(
            "Next scene: why 1D deep water becomes a geometric remapping",
            font_size=21,
            color=TRANSFORMED,
            weight=BOLD,
        )

        beat5_block = VGroup(beat5_title, top_row, bridge, last_note, next_line).arrange(DOWN, buff=0.22)
        beat5_panel = card(beat5_block, color=TRANSFORMED, buff=0.28)
        beat5_panel.move_to(DOWN * 0.16)

        self.play(FadeOut(VGroup(beat4_title, k_final, support_block), shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat5_panel, shift=UP * 0.08), run_time=1.2)
        self.play(Indicate(next_line, color=ACCENT), run_time=1.0)
        self.wait(4.8)
