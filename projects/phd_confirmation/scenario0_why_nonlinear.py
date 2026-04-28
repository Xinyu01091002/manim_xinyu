"""
Scenario 0 - Why Do Nonlinear Waves Matter?
===========================================

A compact visual motivation for the rest of the PhD confirmation sequence:
linear theory is the baseline, nonlinear bound structure changes wave shape,
and small nonlinear phase-speed differences become observable timing offsets
at a fixed wave gauge.
"""

from manim import *
import numpy as np
from presentation_nav import bottom_progress_nav

g = 9.81

K0 = 1.5
A = 0.345
SIGMA_X = 4.0
OMEGA0 = np.sqrt(g * K0)
CG = OMEGA0 / (2.0 * K0)
EPS = A * K0
PHASE_DRIFT_SCALE = 0.10
OMEGA_NL = OMEGA0 * (1.0 + PHASE_DRIFT_SCALE * EPS**2 / 2.0)

X_PROBE = 11.0
T_END = 18.0

C_LINEAR = BLUE
C_NL = YELLOW
C_BOUND = ORANGE
C_SETDOWN = GREEN
C_THIRD = PURPLE
C_PHASE = BLUE_B
C_MUTED = GREY_B
C_PANEL = GREY_D
SCENARIO0_SECONDS = 52.20
SCENARIO0_SUBSCENARIOS = [
    "opening",
    "linear baseline",
    "shape + spectrum",
    "fixed probe",
    "arrival drift",
    "bound harmonics",
]


def env(x):
    return np.exp(-x**2 / (2.0 * SIGMA_X**2))


def eta_lin(x, t):
    return A * env(x - CG * t) * np.cos(K0 * x - OMEGA0 * t)


def eta_nl(x, t):
    xg = x - CG * t
    e = env(xg)
    ph = K0 * x - OMEGA_NL * t
    linear = A * e * np.cos(ph)
    second_plus = (K0 / 2.0) * A**2 * e**2 * np.cos(2.0 * ph)
    setdown = -(K0 / 2.0) * A**2 * e**2
    third_plus = (3.0 * K0**2 / 8.0) * A**3 * e**3 * np.cos(3.0 * ph)
    return linear + second_plus + setdown + third_plus


def gaussian(k, center, width, amp):
    return amp * np.exp(-0.5 * ((k - center) / width) ** 2)


def panel_box(mob, color=C_PANEL, opacity=0.08, buff=0.16):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08).set_fill(BLACK, opacity=opacity)


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


class WhyNonlinearWaves(Scene):
    def construct(self):
        title = Text("Why nonlinear waves matter", font_size=36, weight=BOLD)
        subtitle = Text("shape changes first; timing errors accumulate later", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav_progress.add_updater(
            lambda tracker, dt: tracker.increment_value(len(SCENARIO0_SUBSCENARIOS) * dt / SCENARIO0_SECONDS)
        )
        nav = bottom_progress_nav(
            0,
            6,
            "nonlinear waves",
            SCENARIO0_SUBSCENARIOS,
            nav_progress,
            accent=C_NL,
        )
        self.add(nav_progress, nav)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)

        ax_s = Axes(
            x_range=[-14, 14, 7],
            y_range=[-0.46, 0.46, 0.20],
            x_length=7.0,
            y_length=2.65,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [-10, 0, 10], "font_size": 24},
            y_axis_config={"numbers_to_include": [-0.2, 0.0, 0.2], "font_size": 22},
        ).to_edge(LEFT, buff=0.54).shift(UP * 0.76)
        ax_k = Axes(
            x_range=[0.0, 5.6, 1.5],
            y_range=[0.0, 1.15, 0.5],
            x_length=4.35,
            y_length=2.65,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.50).shift(UP * 0.76)

        head_s = Text("spatial wave group", font_size=24, color=C_MUTED).next_to(ax_s, UP, buff=0.18)
        head_k = Text("wavenumber spectrum", font_size=24, color=C_MUTED).next_to(ax_k, UP, buff=0.18)
        lab_xs = ax_s.get_x_axis_label(MathTex("x", font_size=25))
        lab_ys = ax_s.get_y_axis_label(MathTex(r"\eta", font_size=25))
        lab_xk = ax_k.get_x_axis_label(MathTex("k", font_size=25))
        lab_yk = ax_k.get_y_axis_label(MathTex(r"|\hat\eta|", font_size=25))

        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_s), quiet_fade(head_s), quiet_fade(lab_xs), quiet_fade(lab_ys)),
                AnimationGroup(Create(ax_k), quiet_fade(head_k), quiet_fade(lab_xk), quiet_fade(lab_yk)),
                lag_ratio=0.24,
            )
        )

        lin_wave = ax_s.plot(lambda x: eta_lin(x, 0), x_range=[-14, 14, 0.04], color=C_LINEAR, stroke_width=2.7)
        env_u = ax_s.plot(lambda x: A * env(x), x_range=[-14, 14, 0.10], color=BLUE_A, stroke_width=1.1, stroke_opacity=0.45)
        env_l = ax_s.plot(lambda x: -A * env(x), x_range=[-14, 14, 0.10], color=BLUE_A, stroke_width=1.1, stroke_opacity=0.45)
        lin_spec = ax_k.plot(lambda k: gaussian(k, K0, 0.32, 1.0), x_range=[0.05, 5.6, 0.02], color=C_LINEAR, stroke_width=2.6)
        k0_label = MathTex("k_0", font_size=25, color=C_LINEAR).next_to(ax_k.c2p(K0, 0), DOWN, buff=0.10)

        baseline = VGroup(
            Text("linear theory", font_size=25, color=C_LINEAR),
            MathTex(r"\eta_{\rm lin}=A(x)\cos(k_0x-\omega_0t)", font_size=30, color=C_LINEAR),
        ).arrange(DOWN, buff=0.10).to_edge(DOWN, buff=1.02)
        self.play(Create(lin_wave), Create(env_u), Create(env_l))
        self.play(Create(lin_spec), quiet_fade(k0_label), quiet_fade(baseline))
        self.wait(1.8)

        nl_wave = ax_s.plot(lambda x: eta_nl(x, 0), x_range=[-14, 14, 0.04], color=C_NL, stroke_width=2.9)
        nl_note = VGroup(
            Text("same wave group, different shape", font_size=25, color=C_NL),
            Text("sharper crests and flatter troughs", font_size=21, color=C_MUTED),
        ).arrange(DOWN, buff=0.08).move_to(baseline)
        self.play(FadeOut(baseline, run_time=0.3), quiet_fade(nl_note, shift=UP * 0.03), Create(nl_wave))

        xs = np.linspace(-3.0, 3.0, 900)
        x_lin = xs[np.argmax([eta_lin(x, 0) for x in xs])]
        x_non = xs[np.argmax([eta_nl(x, 0) for x in xs])]
        h_lin = eta_lin(x_lin, 0)
        h_non = eta_nl(x_non, 0)
        crest_ref = DashedLine(ax_s.c2p(-3.8, h_lin), ax_s.c2p(3.8, h_lin), color=C_LINEAR, stroke_width=1.4, dash_length=0.10)
        crest_arrow = DoubleArrow(ax_s.c2p(x_non, h_lin), ax_s.c2p(x_non, h_non), buff=0, color=C_NL, stroke_width=2.3, tip_length=0.12)
        crest_label = Text("about 10% crest lift", font_size=21, color=C_NL).next_to(crest_arrow, RIGHT, buff=0.12)
        self.play(Create(crest_ref), GrowArrow(crest_arrow), quiet_fade(crest_label, shift=RIGHT * 0.03))
        self.wait(1.8)

        spec_2 = ax_k.plot(lambda k: gaussian(k, 2 * K0, 0.42, 0.42), x_range=[0.05, 5.6, 0.02], color=C_BOUND, stroke_width=2.4)
        spec_3 = ax_k.plot(lambda k: gaussian(k, 3 * K0, 0.48, 0.20), x_range=[0.05, 5.6, 0.02], color=C_THIRD, stroke_width=2.4)
        spec_0 = ax_k.plot(lambda k: gaussian(k, 0.25, 0.36, 0.36), x_range=[0.01, 2.0, 0.02], color=C_SETDOWN, stroke_width=2.4)
        labels = VGroup(
            MathTex("2k_0", font_size=23, color=C_BOUND).next_to(ax_k.c2p(2 * K0, 0), DOWN, buff=0.10),
            MathTex("3k_0", font_size=23, color=C_THIRD).next_to(ax_k.c2p(3 * K0, 0), DOWN, buff=0.10),
            MathTex(r"k\approx0", font_size=21, color=C_SETDOWN).next_to(ax_k.c2p(0.25, 0), DOWN + RIGHT * 0.25, buff=0.10),
        )
        fingerprint = VGroup(
            Text("extra spectral energy", font_size=19, color=WHITE),
            MathTex(r"k\approx0,\quad 2k_0,\quad 3k_0", font_size=26, color=C_NL),
        ).arrange(DOWN, buff=0.08).next_to(ax_k, DOWN, buff=0.34)
        fingerprint.scale_to_fit_width(4.25)
        self.play(LaggedStart(Create(spec_0), Create(spec_2), Create(spec_3), lag_ratio=0.30), quiet_fade(labels))
        self.play(quiet_fade(fingerprint))
        self.wait(2.0)

        self.play(FadeOut(nl_note), FadeOut(crest_ref), FadeOut(crest_arrow), FadeOut(crest_label), FadeOut(fingerprint), FadeOut(env_u), FadeOut(env_l))

        probe = DashedLine(ax_s.c2p(X_PROBE, -0.44), ax_s.c2p(X_PROBE, 0.44), color=GREY_C, stroke_width=1.5, dash_length=0.08)
        probe_label = VGroup(
            Text("fixed gauge", font_size=18, color=GREY_C),
            MathTex(r"x=11\,{\rm m}", font_size=18, color=GREY_C),
        ).arrange(DOWN, buff=0.04).next_to(ax_s.c2p(X_PROBE, -0.44), DOWN, buff=0.08)
        self.play(Create(probe), quiet_fade(probe_label))

        ax_t = Axes(
            x_range=[0, T_END, 3],
            y_range=[-0.42, 0.42, 0.2],
            x_length=10.5,
            y_length=1.75,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [3, 6, 9, 12, 15, 18], "font_size": 23},
            y_axis_config={"numbers_to_include": [-0.2, 0.0, 0.2], "font_size": 21},
        ).to_edge(DOWN, buff=0.98)
        head_t = Text("what the fixed gauge records", font_size=23, color=C_MUTED).next_to(ax_t, UP, buff=0.13)
        lab_xt = ax_t.get_x_axis_label(MathTex("t", font_size=25))
        lab_yt = ax_t.get_y_axis_label(MathTex(r"\eta", font_size=25))
        self.play(Create(ax_t), quiet_fade(head_t), quiet_fade(lab_xt), quiet_fade(lab_yt))

        t = ValueTracker(0.001)
        live_lin = always_redraw(lambda: ax_s.plot(lambda x: eta_lin(x, t.get_value()), x_range=[-14, 14, 0.05], color=C_LINEAR, stroke_width=2.5))
        live_nl = always_redraw(lambda: ax_s.plot(lambda x: eta_nl(x, t.get_value()), x_range=[-14, 14, 0.05], color=C_NL, stroke_width=2.7))
        gauge_lin = always_redraw(lambda: Dot(ax_s.c2p(X_PROBE, eta_lin(X_PROBE, t.get_value())), radius=0.075, color=C_LINEAR).set_stroke(WHITE, width=1.2))
        gauge_nl = always_redraw(lambda: Dot(ax_s.c2p(X_PROBE, eta_nl(X_PROBE, t.get_value())), radius=0.075, color=C_NL).set_stroke(WHITE, width=1.2))
        trace_lin = always_redraw(lambda: ax_t.plot(lambda tau: eta_lin(X_PROBE, tau), x_range=[0, max(0.02, t.get_value()), 0.04], color=C_LINEAR, stroke_width=2.2))
        trace_nl = always_redraw(lambda: ax_t.plot(lambda tau: eta_nl(X_PROBE, tau), x_range=[0, max(0.02, t.get_value()), 0.04], color=C_NL, stroke_width=2.2))
        self.play(FadeOut(lin_wave), FadeOut(nl_wave))
        self.add(live_lin, live_nl, gauge_lin, gauge_nl, trace_lin, trace_nl)
        self.play(t.animate.set_value(T_END), run_time=14.0, rate_func=linear)
        self.wait(1.4)

        t_group = X_PROBE / CG
        window = np.linspace(t_group + 0.5, t_group + 2.5, 800)
        t_lin = window[np.argmax([eta_lin(X_PROBE, tau) for tau in window])]
        t_non = window[np.argmax([eta_nl(X_PROBE, tau) for tau in window])]
        delta_ms = abs(t_lin - t_non) * 1000.0
        v_lin = DashedLine(ax_t.c2p(t_lin, -0.38), ax_t.c2p(t_lin, 0.38), color=C_LINEAR, stroke_width=1.4, dash_length=0.09)
        v_non = DashedLine(ax_t.c2p(t_non, -0.38), ax_t.c2p(t_non, 0.38), color=C_NL, stroke_width=1.4, dash_length=0.09)
        dt_arrow = DoubleArrow(ax_t.c2p(t_non, 0.32), ax_t.c2p(t_lin, 0.32), buff=0, color=WHITE, stroke_width=2.0, tip_length=0.10)
        dt_label = MathTex(rf"\Delta t\approx {delta_ms:.0f}\,{{\rm ms}}", font_size=24, color=WHITE).next_to(dt_arrow, UP, buff=0.06)
        timing_text = VGroup(
            Text("small speed change", font_size=17, color=C_NL),
            Text("visible arrival drift", font_size=17, color=C_MUTED),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        timing_text.move_to(ax_t.c2p(2.7, 0.29))
        timing = VGroup(
            panel_box(timing_text, color=C_NL, opacity=0.16, buff=0.12),
            timing_text,
        )
        self.play(Create(v_non), Create(v_lin), GrowArrow(dt_arrow), quiet_fade(dt_label, shift=UP * 0.03))
        self.play(quiet_fade(timing))
        self.wait(2.6)

        self.play(
            *[FadeOut(mob) for mob in [
                ax_k, head_k, lab_xk, lab_yk, lin_spec, spec_0, spec_2, spec_3, k0_label, labels,
                probe, probe_label, timing,
            ]]
        )

        final_lin = ax_s.plot(lambda x: eta_lin(x, 0), x_range=[-14, 14, 0.04], color=C_LINEAR, stroke_width=2.5)
        final_nl = ax_s.plot(lambda x: eta_nl(x, 0), x_range=[-14, 14, 0.04], color=C_NL, stroke_width=2.8)
        final_trace_lin = ax_t.plot(lambda tau: eta_lin(X_PROBE, tau), x_range=[0, T_END, 0.04], color=C_LINEAR, stroke_width=2.2)
        final_trace_nl = ax_t.plot(lambda tau: eta_nl(X_PROBE, tau), x_range=[0, T_END, 0.04], color=C_NL, stroke_width=2.2)
        self.remove(live_lin, live_nl, gauge_lin, gauge_nl, trace_lin, trace_nl)
        self.add(final_lin, final_nl, final_trace_lin, final_trace_nl, v_non, v_lin, dt_arrow, dt_label)

        takeaway = VGroup(
            Text("Why it matters", font_size=25, weight=BOLD, color=WHITE),
            VGroup(
                Text("shape:", font_size=20, color=C_NL),
                Text("crests sharpen, troughs flatten", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.14),
            VGroup(
                Text("timing:", font_size=20, color=C_NL),
                Text("crests arrive earlier at a fixed gauge", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        takeaway.scale_to_fit_width(4.45)
        takeaway.move_to([3.45, 0.76, 0])
        box = panel_box(takeaway, color=C_NL, opacity=0.10, buff=0.22)
        spatial_highlight = SurroundingRectangle(ax_s, color=C_NL, buff=0.10, corner_radius=0.07)
        time_highlight = SurroundingRectangle(ax_t, color=C_NL, buff=0.10, corner_radius=0.07)
        self.play(FadeIn(box), quiet_fade(takeaway[0]))
        self.play(quiet_fade(takeaway[1]), Create(spatial_highlight))
        self.play(quiet_fade(takeaway[2]), ReplacementTransform(spatial_highlight, time_highlight))
        self.wait(2.4)

        transition_question = Text(
            "What did nonlinearity add?",
            font_size=34,
            weight=BOLD,
            color=WHITE,
        )
        transition_extra = VGroup(
            Text("Extra wave components", font_size=28, color=C_MUTED),
            Text("that travel with the group.", font_size=28, color=C_MUTED),
        ).arrange(DOWN, buff=0.10)
        transition_focus = Text(
            "These are bound harmonics.",
            font_size=30,
            weight=BOLD,
            color=C_BOUND,
        )
        transition = VGroup(transition_question, transition_extra, transition_focus).arrange(DOWN, buff=0.34)
        transition.scale_to_fit_width(9.4)
        transition.move_to(ORIGIN)

        self.play(
            FadeOut(VGroup(
                title, subtitle, ax_s, head_s, lab_xs, lab_ys, final_lin, final_nl,
                ax_t, head_t, lab_xt, lab_yt, final_trace_lin, final_trace_nl,
                v_non, v_lin, dt_arrow, dt_label, box, takeaway, time_highlight,
            )),
            run_time=0.8,
        )
        self.play(quiet_fade(transition_question), run_time=0.6)
        self.play(quiet_fade(transition_extra), run_time=0.6)
        self.play(quiet_fade(transition_focus), run_time=0.6)
        self.wait(5.0)
        nav_progress.clear_updaters()
