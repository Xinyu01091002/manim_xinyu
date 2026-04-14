import numpy as np

from manim import *


DEEP = BLUE_C
NONLINEAR = ORANGE
TRANSFORMED = TEAL_C
ACCENT = YELLOW
MUTED = GREY_B
PANEL = GREY_D
ORDER4 = RED_C


AMP = 0.58
DISP = 0.52
CHI_MIN = -2 * np.pi
CHI_MAX = 2 * np.pi


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


def make_wave_axes(x_length=5.4, y_length=2.1):
    return Axes(
        x_range=[-7, 7, 3.5],
        y_range=[-1.25, 1.25, 1],
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={
            "color": PANEL,
            "stroke_width": 2,
            "include_ticks": False,
            "include_numbers": False,
        },
    )


def profile_point(chi, lam):
    x = chi - lam * DISP * np.sin(chi)
    y = AMP * np.cos(chi)
    return x, y


def make_profile(axes, lam, color=WHITE, stroke_width=5):
    return ParametricFunction(
        lambda chi: axes.c2p(*profile_point(chi, lam)),
        t_range=[CHI_MIN, CHI_MAX],
        color=color,
        stroke_width=stroke_width,
    )


def make_simple_wave(axes, color=DEEP, stroke_width=5):
    return axes.plot(lambda x: AMP * np.cos(x), x_range=[CHI_MIN, CHI_MAX], color=color, stroke_width=stroke_width)


def make_hilbert_wave(axes, color=ACCENT, stroke_width=5):
    return axes.plot(lambda x: DISP * np.sin(x), x_range=[CHI_MIN, CHI_MAX], color=color, stroke_width=stroke_width)


def make_spectrum(heights, colors, labels):
    baseline = Line(LEFT * 1.35, RIGHT * 1.35, color=PANEL, stroke_width=2.5)
    xs = [-0.85, 0.0, 0.85]
    bars = VGroup()
    text_row = VGroup()
    for x, h, color, label in zip(xs, heights, colors, labels):
        bar_height = max(h, 0.03)
        bar = Rectangle(
            width=0.28,
            height=bar_height,
            stroke_width=1.2,
            color=color if h > 0.05 else PANEL,
            fill_color=color if h > 0.05 else PANEL,
            fill_opacity=0.85 if h > 0.05 else 0.15,
        )
        bar.move_to(np.array([x, baseline.get_center()[1] + bar_height / 2, 0]))
        bars.add(bar)
        text_row.add(MathTex(label, font_size=22, color=color if h > 0.05 else MUTED).next_to(bar, DOWN, buff=0.08))
    return VGroup(baseline, bars, text_row)


class OneDDeepWaterRemapping(Scene):
    def construct(self):
        title = Text("Scenario 3: Why 1D Deep Water Becomes a Remapping", font_size=31, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        self.play(Write(title), run_time=1.2)

        # Beat 1: 1D collapse into Hilbert geometry
        beat1_title = Text("In 1D deep water, the kernels collapse into a Hilbert-transform picture", font_size=23, color=WHITE)

        d_formula = MathTex(r"D(1,2,3)=0", font_size=33, color=NONLINEAR)
        b_formula = MathTex(r"B(1,2,3)=-\frac12 |k_3|\,\hat{k}_1\hat{k}_2", font_size=31, color=WHITE)
        hilbert_z = MathTex(r"\tilde Z = \mathcal H[Z]", font_size=31, color=ACCENT)
        hilbert_phi = MathTex(r"\tilde \Phi = \mathcal H[\Phi]", font_size=31, color=TRANSFORMED)

        top_row = VGroup(d_formula, b_formula).arrange(RIGHT, buff=0.48, aligned_edge=DOWN)
        bottom_row = VGroup(hilbert_z, hilbert_phi).arrange(RIGHT, buff=0.48, aligned_edge=DOWN)
        formula_grid = VGroup(top_row, bottom_row).arrange(DOWN, buff=0.24)
        fit_to_width(formula_grid, 10.8)

        axes1 = make_wave_axes(x_length=5.4, y_length=2.05)
        z_curve = make_simple_wave(axes1, color=DEEP, stroke_width=5)
        hz_curve = make_hilbert_wave(axes1, color=ACCENT, stroke_width=5)
        z_label = MathTex(r"Z_0(\chi)\sim \cos(k\chi)", font_size=24, color=DEEP).next_to(axes1, UP, buff=0.15).shift(LEFT * 1.0)
        hz_label = MathTex(r"\tilde Z_0(\chi)\sim \sin(k\chi)", font_size=24, color=ACCENT).next_to(axes1, UP, buff=0.15).shift(RIGHT * 1.25)
        phase_note = Tex(r"same wavelength, $90^\circ$ phase shift", font_size=19, color=MUTED)
        phase_note.next_to(axes1, DOWN, buff=0.16)
        graph_block = VGroup(axes1, z_curve, hz_curve, z_label, hz_label, phase_note)
        graph_panel = card(graph_block, color=ACCENT, buff=0.22)

        beat1 = VGroup(beat1_title, formula_grid, graph_panel).arrange(DOWN, buff=0.26)
        beat1.move_to(DOWN * 0.16)

        self.play(FadeIn(beat1_title, shift=UP * 0.08), run_time=1.05)
        self.play(FadeIn(top_row, shift=UP * 0.05), FadeIn(bottom_row, shift=UP * 0.05), run_time=1.15)
        self.play(Create(z_curve), Create(hz_curve), FadeIn(axes1), FadeIn(z_label), FadeIn(hz_label), FadeIn(phase_note), run_time=1.35)
        self.wait(4.0)

        # Beat 2: characteristic labels and horizontal motion
        beat2_title = Text("Now each surface point keeps its label chi and only moves horizontally", font_size=23, color=WHITE)
        char_eq = MathTex(r"x=\chi-\lambda \tilde Z_0(\chi)", font_size=40, color=ACCENT)
        hold_eq = MathTex(r"\tilde Z(x,\lambda)=\tilde Z_0(\chi)", font_size=30, color=TRANSFORMED)

        axes2 = make_wave_axes(x_length=8.2, y_length=2.5)
        ghost_curve = make_profile(axes2, 0.0, color=MUTED, stroke_width=3)
        tracker = ValueTracker(0.0)
        live_curve = always_redraw(lambda: make_profile(axes2, tracker.get_value(), color=TRANSFORMED, stroke_width=5))

        chi_values = [-4.3, -0.4, 3.2]
        dots = VGroup()
        labels = VGroup()
        label_buffers = [UP, DOWN, UP]
        for idx, chi in enumerate(chi_values, start=1):
            dot = always_redraw(
                lambda c=chi: Dot(axes2.c2p(*profile_point(c, tracker.get_value())), radius=0.07, color=ACCENT)
            )
            label = always_redraw(
                lambda d=dot, n=idx, vec=label_buffers[idx - 1]: MathTex(
                    rf"\chi_{n}",
                    font_size=22,
                    color=ACCENT,
                ).next_to(d, vec, buff=0.09)
            )
            dots.add(dot)
            labels.add(label)

        lambda_text = Tex(r"$\lambda: 0 \rightarrow 1$", font_size=20, color=MUTED)
        lambda_text.next_to(axes2, DOWN, buff=0.18)
        motion_note = Tex(r"grey = original parameter profile, teal = the same points after horizontal transport", font_size=18, color=MUTED)
        motion_note.next_to(lambda_text, DOWN, buff=0.1)

        graph2_block = VGroup(axes2, ghost_curve, live_curve, dots, labels, lambda_text, motion_note)
        graph2_panel = card(graph2_block, color=TRANSFORMED, buff=0.22)

        beat2 = VGroup(beat2_title, char_eq, hold_eq, graph2_panel).arrange(DOWN, buff=0.22)
        beat2.move_to(DOWN * 0.14)

        self.play(FadeOut(beat1, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat2_title, shift=UP * 0.08), FadeIn(char_eq, shift=UP * 0.05), run_time=1.15)
        self.play(FadeIn(hold_eq, shift=UP * 0.05), FadeIn(axes2), FadeIn(ghost_curve), FadeIn(live_curve), FadeIn(lambda_text), FadeIn(motion_note), run_time=1.2)
        self.play(FadeIn(dots), FadeIn(labels), run_time=0.85)
        self.play(tracker.animate.set_value(1.0), run_time=3.2)
        self.wait(3.6)

        # Beat 3: chi-space vs x-space
        beat3_title = Text("So a simple chi-profile becomes a nonlinear x-profile after remapping", font_size=23, color=WHITE)

        left_axes = make_wave_axes(x_length=4.7, y_length=2.0)
        left_curve = make_profile(left_axes, 0.0, color=DEEP, stroke_width=5)
        left_title = Text("chi-space", font_size=20, color=MUTED)
        left_note = Tex(r"one clean parent mode", font_size=18, color=WHITE)
        left_spec = make_spectrum([0.9, 0.0, 0.0], [DEEP, NONLINEAR, ORDER4], [r"k", r"2k", r"3k"])
        left_panel_body = VGroup(left_title, left_axes, left_curve, left_note, left_spec).arrange(DOWN, buff=0.16)
        left_panel = card(left_panel_body, color=DEEP, buff=0.22)

        right_axes = make_wave_axes(x_length=4.7, y_length=2.0)
        right_curve = make_profile(right_axes, 1.0, color=TRANSFORMED, stroke_width=5)
        right_title = Text("x-space after remapping", font_size=20, color=MUTED)
        right_note = Tex(r"crest sharpened, trough widened", font_size=18, color=WHITE)
        right_spec = make_spectrum([0.9, 0.34, 0.16], [DEEP, NONLINEAR, ORDER4], [r"k", r"2k", r"3k"])
        right_panel_body = VGroup(right_title, right_axes, right_curve, right_note, right_spec).arrange(DOWN, buff=0.16)
        right_panel = card(right_panel_body, color=TRANSFORMED, buff=0.22)

        compare_arrow = Arrow(LEFT * 0.9, RIGHT * 0.9, buff=0, color=ACCENT, stroke_width=5)
        compare_label = Tex(r"same points, new horizontal positions", font_size=18, color=ACCENT)
        arrow_block = VGroup(compare_arrow, compare_label).arrange(DOWN, buff=0.14)

        compare_row = VGroup(left_panel, arrow_block, right_panel).arrange(RIGHT, buff=0.26, aligned_edge=DOWN)
        fit_to_width(compare_row, 12.7)
        beat3 = VGroup(beat3_title, compare_row).arrange(DOWN, buff=0.24)
        beat3.move_to(DOWN * 0.14)

        self.play(FadeOut(beat2, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat3_title, shift=UP * 0.08), run_time=1.05)
        self.play(FadeIn(left_panel, shift=RIGHT * 0.08), FadeIn(arrow_block), FadeIn(right_panel, shift=LEFT * 0.08), run_time=1.25)
        self.wait(4.2)

        # Beat 4: takeaway and bridge
        beat4_title = Text("This is the deep-water 1D miracle", font_size=26, color=WHITE, weight=BOLD)
        chip_1 = card(MathTex(r"D=0", font_size=30, color=NONLINEAR), color=NONLINEAR, buff=0.2)
        chip_2 = card(MathTex(r"x=\chi-\tilde Z_0(\chi)", font_size=30, color=ACCENT), color=ACCENT, buff=0.2)
        chip_3 = card(MathTex(r"\text{simple in }\chi \;\Longrightarrow\; \text{nonlinear in }x", font_size=28, color=TRANSFORMED), color=TRANSFORMED, buff=0.2)

        chip_row = VGroup(chip_1, chip_2, chip_3).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
        fit_to_width(chip_row, 12.7)
        bridge = Tex(r"The abstract canonical transform becomes a readable geometry of horizontal remapping.", font_size=22, color=WHITE)
        next_line = Text("Next scene: reconstruction creates bound harmonics", font_size=22, color=TRANSFORMED, weight=BOLD)

        beat4_block = VGroup(beat4_title, chip_row, bridge, next_line).arrange(DOWN, buff=0.24)
        beat4_panel = card(beat4_block, color=TRANSFORMED, buff=0.28)
        beat4_panel.move_to(DOWN * 0.16)

        self.play(FadeOut(beat3, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(beat4_panel, shift=UP * 0.08), run_time=1.2)
        self.play(Indicate(next_line, color=ACCENT), run_time=1.0)
        self.wait(4.8)
