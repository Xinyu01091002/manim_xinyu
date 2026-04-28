"""
Cover image - VWA extensions eye attractor
==========================================

A static 2x3 white-background cover graphic for the PhD confirmation deck.
It distills the visual language from scenarios 0-5 into six compact panels:
unidirectional, directional, kinematics, time series, inverse transform, and
higher-order extension.
"""

from manim import *
import numpy as np

config.pixel_width = 2200
config.pixel_height = 1000
config.frame_width = 16.0
config.frame_height = config.frame_width * config.pixel_height / config.pixel_width


C_INK = ManimColor("#17212B")
C_MUTED = ManimColor("#667085")
C_BLUE = ManimColor("#2675C8")
C_ORANGE = ManimColor("#E67E22")
C_GREEN = ManimColor("#2E9D64")
C_TEAL = ManimColor("#149C94")
C_PURPLE = ManimColor("#7E57C2")
C_GOLD = ManimColor("#D9A406")
C_PANEL = ManimColor("#F7F9FC")
C_GOLD_LIGHT = ManimColor("#FDE9A9")
TEXT_FONT = "CMU Serif"


def panel_box(width, height, color):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.13,
        stroke_color=color,
        stroke_width=3.0,
        fill_color=C_PANEL,
        fill_opacity=1.0,
    )
    return box


def local_axes(width, height, x_label="x", y_label=r"\eta", font_size=22):
    axes = VGroup(
        Line(LEFT * width / 2, RIGHT * width / 2, color=C_MUTED, stroke_width=2.0),
        Line(DOWN * height / 2, UP * height / 2, color=C_MUTED, stroke_width=2.0),
        MathTex(x_label, font_size=font_size, color=C_MUTED).move_to(RIGHT * (width / 2 + 0.16)),
        MathTex(y_label, font_size=font_size, color=C_MUTED).move_to(UP * (height / 2 + 0.16)),
    )
    axes.set_opacity(0.72)
    return axes


def wave_group(width, carrier, amp, envelope, phase, color, stroke_width=4.0):
    return FunctionGraph(
        lambda x: amp * np.exp(-envelope * x * x) * np.sin(carrier * x + phase),
        x_range=[-width / 2, width / 2],
        color=color,
        stroke_width=stroke_width,
    )


class VWAExtensionsCover(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Variable Wavenumber Approximation", font=TEXT_FONT, font_size=40, weight=BOLD, color=C_INK)
        subtitle = Text("one compact structure for nonlinear wave estimation", font=TEXT_FONT, font_size=22, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.04).to_edge(UP, buff=0.07)
        self.add(title, subtitle)

        centers = [
            LEFT * 4.65 + UP * 0.82,
            ORIGIN + UP * 0.82,
            RIGHT * 4.65 + UP * 0.82,
            LEFT * 4.65 + DOWN * 2.04,
            ORIGIN + DOWN * 2.04,
            RIGHT * 4.65 + DOWN * 2.04,
        ]
        panels = [
            ("unidirectional", C_BLUE, self.unidirectional_panel),
            ("2nd to 5th order", C_GOLD, self.higher_order_panel),
            ("kinematics", C_TEAL, self.kinematics_panel),
            ("time series", C_ORANGE, self.time_series_panel),
            ("inverse transform", C_PURPLE, self.inverse_panel),
            ("directional", C_GREEN, self.directional_panel),
        ]

        for center, (label, color, builder) in zip(centers, panels):
            box = panel_box(3.58, 2.58, color).move_to(center)
            heading = Text(label, font=TEXT_FONT, font_size=27, weight=BOLD, color=color).move_to(center + UP * 0.98)
            heading.scale_to_fit_width(min(heading.width, 3.12))
            visual = builder(center)
            self.add(box, heading, visual)

    def unidirectional_panel(self, center):
        ax_center = center + DOWN * 0.05
        group = VGroup()
        group.add(local_axes(2.70, 1.08, font_size=18).move_to(ax_center))
        wave = wave_group(2.65, 12.0, 0.38, 1.25, 0.6, C_BLUE, stroke_width=4.6).move_to(ax_center)
        env_u = FunctionGraph(lambda x: 0.38 * np.exp(-1.25 * x * x), x_range=[-1.32, 1.32], color=C_BLUE, stroke_width=1.6).move_to(ax_center)
        env_l = FunctionGraph(lambda x: -0.38 * np.exp(-1.25 * x * x), x_range=[-1.32, 1.32], color=C_BLUE, stroke_width=1.6).move_to(ax_center)
        env_u.set_opacity(0.30)
        env_l.set_opacity(0.30)
        kernel = MathTex(r"k_0", font_size=30, color=C_BLUE).move_to(center + DOWN * 1.00)
        group.add(env_u, env_l, wave, kernel)
        return group

    def directional_panel(self, center):
        group = VGroup()
        surf_center = center + DOWN * 0.06
        theta = 55 * DEGREES
        travel_dir = np.array([np.cos(theta), np.sin(theta), 0.0])
        crest_dir = np.array([-np.sin(theta), np.cos(theta), 0.0])

        def project(x, y, z):
            return surf_center + RIGHT * (0.95 * x + 0.42 * y) + UP * (0.30 * y + 0.78 * z)

        outline_points = []
        for angle in np.linspace(0, TAU, 96):
            local = travel_dir * (1.18 * np.cos(angle)) + crest_dir * (0.62 * np.sin(angle))
            outline_points.append(project(local[0], local[1], 0.0))
        outline = VMobject(color=C_GREEN, stroke_width=2.0).set_points_smoothly(outline_points).set_opacity(0.34)
        group.add(outline)

        q_samples = np.linspace(-1.18, 1.18, 88)
        for r in np.linspace(-0.52, 0.52, 7):
            points = []
            transverse = np.exp(-2.5 * r * r)
            for q in q_samples:
                envelope = np.exp(-1.08 * q * q - 2.5 * r * r)
                z = 0.32 * envelope * np.sin(17.5 * q + 0.45)
                local = travel_dir * q + crest_dir * r
                points.append(project(local[0], local[1], z))
            wave = VMobject(
                color=interpolate_color(C_GREEN, WHITE, 0.22 * transverse),
                stroke_width=1.4 + 2.2 * transverse,
            ).set_points_smoothly(points).set_opacity(0.50 + 0.34 * transverse)
            group.add(wave)

        for q in np.arange(-0.95, 1.05, TAU / 17.5):
            points = []
            for r in np.linspace(-0.50, 0.50, 26):
                envelope = np.exp(-1.08 * q * q - 2.5 * r * r)
                if envelope < 0.24:
                    continue
                local = travel_dir * q + crest_dir * r
                points.append(project(local[0], local[1], 0.05 + 0.20 * envelope))
            if len(points) > 2:
                group.add(VMobject(color=WHITE, stroke_width=1.4).set_points_smoothly(points).set_opacity(0.42))

        arrow = Arrow(project(-0.80, -0.42, 0.18), project(0.68, 0.46, 0.26), buff=0, color=C_GREEN, stroke_width=5.0)
        label = MathTex(r"\mathbf{k}=(k_x,k_y)", font_size=27, color=C_GREEN).move_to(center + DOWN * 1.02)
        group.add(arrow, label)
        return group

    def kinematics_panel(self, center):
        group = VGroup()
        ax_center = center + UP * 0.02
        group.add(local_axes(2.65, 1.08, x_label="x", y_label="z", font_size=18).move_to(ax_center))
        curve = wave_group(2.58, 9.2, 0.34, 1.20, 0.3, C_ORANGE, stroke_width=4.2).move_to(ax_center)
        group.add(curve)
        for x0 in [-0.55, 0.55]:
            y0 = 0.34 * np.exp(-1.20 * x0 * x0) * np.sin(9.2 * x0 + 0.3)
            pos = ax_center + RIGHT * x0 + UP * y0
            group.add(Dot(pos, radius=0.050, color=C_INK))
            group.add(Arrow(pos + LEFT * 0.22 + UP * 0.17, pos + RIGHT * 0.28 + UP * 0.17, buff=0, color=C_TEAL, stroke_width=4.0))
            group.add(Arrow(pos + RIGHT * 0.18 + DOWN * 0.04, pos + RIGHT * 0.18 + UP * 0.36, buff=0, color=C_BLUE, stroke_width=4.0))
        formula = MathTex(r"u_s,\ w_s", font_size=33, color=C_TEAL).move_to(center + DOWN * 1.02)
        group.add(formula)
        return group

    def time_series_panel(self, center):
        group = VGroup()
        top = center + UP * 0.34
        bottom = center + DOWN * 0.42
        group.add(local_axes(2.65, 0.54, x_label="t", y_label="", font_size=16).move_to(top))
        group.add(local_axes(2.65, 0.54, x_label="t", y_label="", font_size=16).move_to(bottom))
        linear = wave_group(2.60, 10.0, 0.16, 1.35, 0.4, C_BLUE, stroke_width=3.7).move_to(top)
        nonlinear = FunctionGraph(
            lambda x: 0.16 * np.exp(-1.35 * x * x) * np.sin(10.0 * x + 0.4)
            + 0.06 * np.exp(-1.55 * x * x) * np.sin(20.0 * x + 1.0),
            x_range=[-1.30, 1.30],
            color=C_ORANGE,
            stroke_width=3.7,
        ).move_to(bottom)
        cursor_x = -0.58
        group.add(linear, nonlinear)
        group.add(Line(top + RIGHT * cursor_x + DOWN * 0.34, top + RIGHT * cursor_x + UP * 0.34, color=C_INK, stroke_width=2.3))
        group.add(DashedLine(top + RIGHT * cursor_x + DOWN * 0.32, bottom + RIGHT * cursor_x + UP * 0.32, color=C_MUTED, stroke_width=1.6, dash_length=0.05))
        group.add(Text("probe", font=TEXT_FONT, font_size=19, color=C_INK).move_to(center + LEFT * 0.95 + DOWN * 1.03))
        group.add(Text("linear", font=TEXT_FONT, font_size=17, color=C_BLUE).move_to(top + RIGHT * 0.72 + UP * 0.36))
        group.add(Text("nonlinear", font=TEXT_FONT, font_size=17, color=C_ORANGE).move_to(bottom + RIGHT * 0.58 + UP * 0.34))
        return group

    def inverse_panel(self, center):
        group = VGroup()
        top = center + UP * 0.38
        bottom = center + DOWN * 0.40
        group.add(local_axes(2.65, 0.54, x_label="x", y_label="", font_size=16).move_to(top))
        group.add(local_axes(2.65, 0.54, x_label="x", y_label="", font_size=16).move_to(bottom))
        nonlinear = FunctionGraph(
            lambda x: 0.17 * np.exp(-1.35 * x * x) * np.sin(10.0 * x + 0.2)
            + 0.07 * np.exp(-1.50 * x * x) * np.sin(20.0 * x + 0.7),
            x_range=[-1.30, 1.30],
            color=C_ORANGE,
            stroke_width=4.0,
        ).move_to(top)
        linear = wave_group(2.60, 10.0, 0.17, 1.35, 0.2, C_BLUE, stroke_width=4.0).move_to(bottom)
        arrow = Arrow(top + DOWN * 0.31, bottom + UP * 0.31, buff=0.05, color=C_PURPLE, stroke_width=4.0)
        relation = MathTex(r"\eta_{\rm nl}\rightarrow\eta_{\rm lin}", font_size=29, color=C_PURPLE).move_to(center + DOWN * 1.02)
        group.add(nonlinear, linear, arrow, relation)
        return group

    def higher_order_panel(self, center):
        group = VGroup()
        formula = MathTex(
            r"\eta_{\rm VWA}^{(nn)}",
            r"=",
            r"\Re\{",
            r"\eta_{a,K^{(n)}}^{(11)}",
            r"[\eta_a^{(11)}]^{n-1}",
            r"\}",
            font_size=24,
            color=C_INK,
        ).move_to(center + UP * 0.42)
        formula.scale_to_fit_width(3.12)
        formula[0].set_color(C_GOLD)
        formula[3].set_color(C_TEAL)
        formula[4].set_color(C_BLUE)
        group.add(formula)

        xs = [-1.05, -0.35, 0.35, 1.05]
        orders = ["2", "3", "4", "5"]
        heights = [0.38, 0.58, 0.78, 0.98]
        for x, order, height in zip(xs, orders, heights):
            base = center + RIGHT * x + DOWN * 0.62
            bar = RoundedRectangle(
                width=0.34,
                height=height,
                corner_radius=0.06,
                stroke_color=C_GOLD,
                fill_color=interpolate_color(C_GOLD_LIGHT, C_GOLD, 0.35),
                fill_opacity=0.90,
                stroke_width=1.8,
            ).move_to(base + UP * height / 2)
            label = MathTex(rf"n={order}", font_size=22, color=C_INK).next_to(bar, DOWN, buff=0.08)
            group.add(bar, label)
        cost = MathTex(r"\mathcal O(N_c\log N_c)", font_size=30, color=C_GOLD).move_to(center + DOWN * 1.05)
        group.add(cost)
        return group
