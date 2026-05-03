"""
Small Manim Slides proof of concept for the PhD confirmation presentation.

This intentionally does not replace the video scenes. It tests the interaction
model: ordinary Manim animations continue to play, while the presenter controls
the conceptual pauses with ``next_slide``.
"""

from manim import *
import numpy as np

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene

from presentation_nav import bottom_progress_nav
from scenario0_why_nonlinear import (
    C_BOUND,
    C_LINEAR,
    C_MUTED,
    C_NL,
    C_PANEL,
    K0,
    eta_lin,
    eta_nl,
    gaussian,
    panel_box,
    quiet_fade,
)


DEMO_SUBSCENARIOS = [
    "opening",
    "linear baseline",
    "nonlinear shape",
    "presenter pause",
]


class PhDConfirmationSlidesDemo(Slide):
    def slide_pause(self):
        if hasattr(self, "next_slide"):
            self.next_slide(loop=False)
        else:
            self.wait(0.8)

    def set_nav(self, tracker, value):
        tracker.set_value(value)
        self.wait(0.1)

    def construct(self):
        title = Text("Why nonlinear waves matter", font_size=36, weight=BOLD)
        subtitle = Text("same animation language; slide-controlled pacing", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)

        nav_progress = ValueTracker(0)
        nav = bottom_progress_nav(
            0,
            6,
            "nonlinear waves",
            DEMO_SUBSCENARIOS,
            nav_progress,
            accent=C_NL,
        )
        self.add(nav, nav_progress)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)
        self.set_nav(nav_progress, 0.95)
        self.slide_pause()

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
            ),
            run_time=1.1,
        )

        lin_wave = ax_s.plot(lambda x: eta_lin(x, 0), x_range=[-13.5, 13.5], color=C_LINEAR, stroke_width=3.0)
        lin_spec = ax_k.plot(lambda k: gaussian(k, K0, 0.18, 1.0), x_range=[0.0, 5.6], color=C_LINEAR, stroke_width=3.0)
        k0_label = MathTex("k_0", font_size=26, color=C_LINEAR).next_to(ax_k.c2p(K0, 1.0), UP, buff=0.08)
        baseline = Text("Linear theory gives the reference group", font_size=25, color=C_LINEAR)
        baseline.next_to(ax_s, DOWN, buff=0.18).align_to(ax_s, LEFT)

        self.play(Create(lin_wave), Create(lin_spec), quiet_fade(k0_label), quiet_fade(baseline), run_time=1.2)
        self.set_nav(nav_progress, 1.95)
        self.slide_pause()

        nl_wave = ax_s.plot(lambda x: eta_nl(x, 0), x_range=[-13.5, 13.5], color=C_NL, stroke_width=3.2)
        spec_2 = ax_k.plot(lambda k: gaussian(k, 2 * K0, 0.24, 0.30), x_range=[0.0, 5.6], color=C_BOUND, stroke_width=3.0)
        spec_3 = ax_k.plot(lambda k: gaussian(k, 3 * K0, 0.30, 0.14), x_range=[0.0, 5.6], color=PURPLE, stroke_width=3.0)
        nl_note = Text("Bound harmonics sharpen crests and flatten troughs", font_size=25, color=C_NL)
        nl_note.next_to(ax_s, DOWN, buff=0.18).align_to(ax_s, LEFT)

        self.play(FadeOut(baseline, run_time=0.3), quiet_fade(nl_note, shift=UP * 0.03), Create(nl_wave), run_time=0.9)
        self.play(Create(spec_2), Create(spec_3), run_time=0.8)
        self.set_nav(nav_progress, 2.95)
        self.slide_pause()

        takeaway = VGroup(
            Text("In slides mode, this becomes the useful split:", font_size=25, color=WHITE),
            Text("click-controlled explanation + short animated physics segments", font_size=25, color=C_NL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        takeaway_box = panel_box(takeaway, color=C_PANEL, opacity=0.18, buff=0.22)
        VGroup(takeaway_box, takeaway).to_edge(DOWN, buff=1.08)

        self.play(FadeIn(takeaway_box), quiet_fade(takeaway), run_time=0.8)
        self.set_nav(nav_progress, len(DEMO_SUBSCENARIOS))
        self.slide_pause()
