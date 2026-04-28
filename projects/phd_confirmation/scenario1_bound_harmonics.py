"""
Scenario 1 - What Are Bound Harmonics?
======================================

A compact continuation from Scenario 0:
nonlinearity adds wave components that travel with the primary group.
Those components are bound harmonics, not independent free waves.
"""

from manim import *
import numpy as np
from presentation_nav import bottom_progress_nav

g = 9.81

K0 = 1.5
A = 0.30
SIGMA_X = 4.0
OMEGA0 = np.sqrt(g * K0)
CG = OMEGA0 / (2.0 * K0)

C_LINEAR = BLUE
C_BOUND = ORANGE
C_SETDOWN = GREEN
C_THIRD = PURPLE
C_NL = YELLOW
C_MUTED = GREY_B
C_PANEL = GREY_D
SCENARIO1_SECONDS = 42.60
SCENARIO1_SUBSCENARIOS = [
    "linear component",
    "bound components",
    "shape change",
    "locked group",
    "handoff",
]


def env(x):
    return np.exp(-x**2 / (2.0 * SIGMA_X**2))


def theta(x, t):
    # Group-frame phase: envelope is fixed while the carrier oscillates.
    return K0 * x - 0.5 * OMEGA0 * t


def eta1(x, t=0.0):
    return A * env(x) * np.cos(theta(x, t))


def eta2_plus(x, t=0.0):
    return 0.5 * K0 * A**2 * env(x) ** 2 * np.cos(2.0 * theta(x, t))


def eta2_minus(x):
    return -0.5 * K0 * A**2 * env(x) ** 2


def eta3_plus(x, t=0.0):
    return (3.0 * K0**2 / 8.0) * A**3 * env(x) ** 3 * np.cos(3.0 * theta(x, t))


def eta_bound(x, t=0.0):
    return eta2_minus(x) + eta2_plus(x, t) + eta3_plus(x, t)


def eta_total(x, t=0.0):
    return eta1(x, t) + eta_bound(x, t)


def gaussian(k, center, width, amp):
    return amp * np.exp(-0.5 * ((k - center) / width) ** 2)


def panel_box(mob, color=C_PANEL, opacity=0.08, buff=0.16):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08).set_fill(BLACK, opacity=opacity)


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


class BoundHarmonicsIntro(Scene):
    def construct(self):
        title = Text("What did nonlinearity add?", font_size=36, weight=BOLD)
        subtitle = Text("extra wave components that travel with the group", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav_progress.add_updater(
            lambda tracker, dt: tracker.increment_value(len(SCENARIO1_SUBSCENARIOS) * dt / SCENARIO1_SECONDS)
        )
        nav = bottom_progress_nav(
            1,
            6,
            "bound harmonics",
            SCENARIO1_SUBSCENARIOS,
            nav_progress,
            accent=C_NL,
        )
        self.add(nav_progress, nav)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)

        ax_x = Axes(
            x_range=[-12, 12, 6],
            y_range=[-0.40, 0.40, 0.20],
            x_length=6.75,
            y_length=2.65,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [-10, 0, 10], "font_size": 23},
            y_axis_config={"numbers_to_include": [-0.2, 0.0, 0.2], "font_size": 21},
        ).to_edge(LEFT, buff=0.58).shift(UP * 0.64)

        ax_k = Axes(
            x_range=[0.0, 5.6, 1.5],
            y_range=[0.0, 1.15, 0.5],
            x_length=4.35,
            y_length=2.65,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.52).shift(UP * 0.64)

        head_x = Text("wave group", font_size=24, color=C_MUTED).next_to(ax_x, UP, buff=0.18)
        head_k = Text("wavenumber spectrum", font_size=24, color=C_MUTED).next_to(ax_k, UP, buff=0.18)
        lab_x = ax_x.get_x_axis_label(MathTex("x", font_size=25))
        lab_eta = ax_x.get_y_axis_label(MathTex(r"\eta", font_size=25))
        lab_k = ax_k.get_x_axis_label(MathTex("k", font_size=25))
        lab_spec = ax_k.get_y_axis_label(MathTex(r"|\hat\eta|", font_size=25))

        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_x), quiet_fade(head_x), quiet_fade(lab_x), quiet_fade(lab_eta)),
                AnimationGroup(Create(ax_k), quiet_fade(head_k), quiet_fade(lab_k), quiet_fade(lab_spec)),
                lag_ratio=0.22,
            )
        )

        carrier = ax_x.plot(lambda x: eta1(x, 0), x_range=[-12, 12, 0.04], color=C_LINEAR, stroke_width=2.8)
        env_u = ax_x.plot(lambda x: A * env(x), x_range=[-12, 12, 0.10], color=BLUE_A, stroke_width=1.0, stroke_opacity=0.42)
        env_l = ax_x.plot(lambda x: -A * env(x), x_range=[-12, 12, 0.10], color=BLUE_A, stroke_width=1.0, stroke_opacity=0.42)
        spec_1 = ax_k.plot(lambda k: gaussian(k, K0, 0.30, 1.0), x_range=[0.05, 5.6, 0.02], color=C_LINEAR, stroke_width=2.7)
        k0_label = MathTex("k_0", font_size=24, color=C_LINEAR).next_to(ax_k.c2p(K0, 0), DOWN, buff=0.10)

        linear_card = VGroup(
            Text("linear theory", font_size=25, color=C_LINEAR),
            Text("one free-wave component", font_size=21, color=WHITE),
            MathTex(r"\eta_1", font_size=34, color=C_LINEAR),
        ).arrange(DOWN, buff=0.10)
        linear_card.to_edge(DOWN, buff=0.86)

        self.play(Create(carrier), Create(env_u), Create(env_l))
        self.play(Create(spec_1), quiet_fade(k0_label), quiet_fade(linear_card))
        self.wait(1.6)

        bound_card = VGroup(
            Text("nonlinear interactions", font_size=24, color=C_NL),
            Text("create bound components", font_size=21, color=WHITE),
            MathTex(r"\eta_{\rm bound}=\eta_2^-+\eta_2^+ + \eta_3^+", font_size=31, color=C_NL),
        ).arrange(DOWN, buff=0.10).move_to(linear_card)
        self.play(FadeOut(linear_card, run_time=0.3), quiet_fade(bound_card, shift=UP * 0.03))

        setdown = ax_x.plot(lambda x: eta2_minus(x), x_range=[-12, 12, 0.05], color=C_SETDOWN, stroke_width=2.7)
        spec_0 = ax_k.plot(lambda k: gaussian(k, 0.25, 0.34, 0.34), x_range=[0.01, 2.0, 0.02], color=C_SETDOWN, stroke_width=2.5)
        lbl_0 = MathTex(r"k\approx0", font_size=20, color=C_SETDOWN).next_to(ax_k.c2p(0.25, 0), DOWN + RIGHT * 0.25, buff=0.10)
        tag_setdown = VGroup(
            Text("set-down", font_size=21, color=C_SETDOWN),
            MathTex(r"\eta_2^-", font_size=29, color=C_SETDOWN),
        ).arrange(RIGHT, buff=0.14)
        tag_setdown.move_to(ax_x.c2p(-6.9, 0.22))
        self.play(Create(setdown), Create(spec_0), quiet_fade(lbl_0))
        self.wait(1.6)

        second = ax_x.plot(lambda x: eta2_plus(x, 0), x_range=[-12, 12, 0.04], color=C_BOUND, stroke_width=2.5)
        spec_2 = ax_k.plot(lambda k: gaussian(k, 2 * K0, 0.40, 0.44), x_range=[0.05, 5.6, 0.02], color=C_BOUND, stroke_width=2.5)
        lbl_2 = MathTex("2k_0", font_size=23, color=C_BOUND).next_to(ax_k.c2p(2 * K0, 0), DOWN, buff=0.10)
        tag_second = VGroup(
            Text("second harmonic", font_size=21, color=C_BOUND),
            MathTex(r"\eta_2^+", font_size=29, color=C_BOUND),
        ).arrange(RIGHT, buff=0.14)
        tag_second.move_to(ax_x.c2p(5.1, 0.26))
        self.play(Create(second), Create(spec_2), quiet_fade(lbl_2))
        self.wait(1.6)

        third = ax_x.plot(lambda x: eta3_plus(x, 0), x_range=[-12, 12, 0.04], color=C_THIRD, stroke_width=2.3)
        spec_3 = ax_k.plot(lambda k: gaussian(k, 3 * K0, 0.46, 0.20), x_range=[0.05, 5.6, 0.02], color=C_THIRD, stroke_width=2.5)
        lbl_3 = MathTex("3k_0", font_size=23, color=C_THIRD).next_to(ax_k.c2p(3 * K0, 0), DOWN, buff=0.10)
        tag_third = VGroup(
            Text("higher harmonics", font_size=21, color=C_THIRD),
            MathTex(r"\eta_3^+,\ldots", font_size=29, color=C_THIRD),
        ).arrange(RIGHT, buff=0.14)
        tag_third.move_to(ax_x.c2p(5.0, -0.25))
        self.play(Create(third), Create(spec_3), quiet_fade(lbl_3))
        self.wait(1.6)

        total = ax_x.plot(lambda x: eta_total(x, 0), x_range=[-12, 12, 0.04], color=WHITE, stroke_width=3.0)
        total_card = VGroup(
            MathTex(r"\eta_{\rm nl}=\eta_1+\eta_{\rm bound}", font_size=34, color=WHITE),
            Text("free component + bound components", font_size=21, color=C_MUTED),
        ).arrange(DOWN, buff=0.10).move_to(bound_card)

        self.play(
            ReplacementTransform(bound_card, total_card),
            Create(total),
        )
        self.wait(1.8)

        crest_line = DashedLine(ax_x.c2p(-2.8, A), ax_x.c2p(2.8, A), color=C_LINEAR, stroke_width=1.2, dash_length=0.09)
        crest_arrow = DoubleArrow(ax_x.c2p(0, A), ax_x.c2p(0, eta_total(0, 0)), color=C_NL, buff=0, stroke_width=2.2, tip_length=0.12)
        shape_note = Text("bound terms reshape the group", font_size=21, color=C_NL)
        shape_note.scale_to_fit_width(3.8)
        shape_note.next_to(ax_k, DOWN, buff=0.36)
        self.play(Create(crest_line), GrowArrow(crest_arrow), quiet_fade(shape_note))
        self.wait(2.0)

        self.play(
            FadeOut(crest_line),
            FadeOut(crest_arrow),
            FadeOut(shape_note),
            FadeOut(carrier),
            FadeOut(env_u),
            FadeOut(env_l),
            FadeOut(setdown),
            FadeOut(second),
            FadeOut(third),
        )

        t = ValueTracker(0.0)
        live_carrier = always_redraw(
            lambda: ax_x.plot(lambda x: eta1(x, t.get_value()), x_range=[-12, 12, 0.05], color=C_LINEAR, stroke_width=2.2)
        )
        live_bound = always_redraw(
            lambda: ax_x.plot(lambda x: eta_bound(x, t.get_value()), x_range=[-12, 12, 0.05], color=C_NL, stroke_width=2.4)
        )
        live_total = always_redraw(
            lambda: ax_x.plot(lambda x: eta_total(x, t.get_value()), x_range=[-12, 12, 0.05], color=WHITE, stroke_width=2.9)
        )
        group_window = SurroundingRectangle(ax_x, color=C_NL, buff=0.10, corner_radius=0.07)
        lock_note = VGroup(
            Text("bound components", font_size=23, color=C_NL),
            Text("stay inside the moving group", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.08)
        lock_note.scale_to_fit_width(4.2)
        lock_note.next_to(ax_k, DOWN, buff=0.36)
        lock_box = panel_box(lock_note, color=C_NL, opacity=0.12, buff=0.16)

        self.remove(total)
        self.add(live_carrier, live_bound, live_total)
        self.play(Create(group_window), FadeIn(lock_box), quiet_fade(lock_note))
        self.play(t.animate.set_value(12.0), run_time=11.0, rate_func=linear)
        self.wait(1.6)

        self.play(
            FadeOut(VGroup(
                title, subtitle, ax_x, ax_k, head_x, head_k, lab_x, lab_eta, lab_k, lab_spec,
                live_carrier, live_bound, live_total, group_window, lock_box, lock_note,
                spec_1, spec_0, spec_2, spec_3, k0_label, lbl_0, lbl_2, lbl_3, total_card,
            )),
            run_time=0.8,
        )

        end_question = Text("Bound harmonics are not independent free waves.", font_size=32, weight=BOLD, color=WHITE)
        end_answer = VGroup(
            Text("They are generated by nonlinear interactions", font_size=26, color=C_MUTED),
            Text("and remain tied to the primary group.", font_size=26, color=C_MUTED),
        ).arrange(DOWN, buff=0.10)
        next_scene = Text("Next: how expensive is exact interaction theory?", font_size=25, color=C_BOUND)
        ending = VGroup(end_question, end_answer, next_scene).arrange(DOWN, buff=0.34).move_to(ORIGIN)
        ending.scale_to_fit_width(11.0)

        self.play(quiet_fade(end_question), run_time=0.6)
        self.play(quiet_fade(end_answer), run_time=0.6)
        self.play(quiet_fade(next_scene), run_time=0.6)
        self.wait(5.2)
        nav_progress.clear_updaters()
