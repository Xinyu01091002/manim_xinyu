"""
Cover page - VWA extensions eye attractor
=========================================

A looping 16:9 black-background cover for the PhD confirmation slide deck.
It distills the visual language from scenarios 0-5 into six compact panels:
unidirectional, directional, kinematics, time series, inverse transform, and
higher-order extension.
"""

from manim import *
import numpy as np
from pathlib import Path
from presentation_nav import NAV_BG, NAV_FONT, NAV_SCENARIO_COLORS, NAV_SCENARIO_NAMES, NAV_TEXT

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = config.frame_width * config.pixel_height / config.pixel_width


C_BG = ManimColor("#030712")
C_INK = ManimColor("#F8FAFC")
C_MUTED = ManimColor("#A6B0C2")
C_BLUE = ManimColor("#61A5FF")
C_ORANGE = ManimColor("#FFB25E")
C_GREEN = ManimColor("#66D39B")
C_TEAL = ManimColor("#4BD4CB")
C_PURPLE = ManimColor("#C69CFF")
C_ROSE = ManimColor("#FF8BC7")
C_GOLD = ManimColor("#FFE45E")
C_PANEL = ManimColor("#0B1220")
C_PANEL_EDGE = ManimColor("#263244")
C_GOLD_LIGHT = ManimColor("#5E4709")
TEXT_FONT = "CMU Serif"
COVER_LOOP_SECONDS = 6.0
COVER_ROOT = Path(__file__).resolve().parent
COVER_DIRECTIONAL_FRAME_DIR = COVER_ROOT / "data" / "cover_directional_frames"


def panel_box(width, height, color):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.13,
        stroke_color=color,
        stroke_width=3.0,
        fill_color=C_PANEL,
        fill_opacity=0.92,
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


def animated_wave_group(
    width,
    carrier,
    amp,
    envelope,
    phase_tracker,
    phase_offset,
    color,
    stroke_width=4.0,
    center=ORIGIN,
    harmonic=1.0,
    extra=None,
):
    def wave():
        phase = harmonic * phase_tracker.get_value() + phase_offset
        graph = FunctionGraph(
            lambda x: amp * np.exp(-envelope * x * x) * np.sin(carrier * x + phase)
            + (0 if extra is None else extra(x, phase)),
            x_range=[-width / 2, width / 2],
            color=color,
            stroke_width=stroke_width,
        )
        graph.move_to(center)
        return graph

    return always_redraw(wave)


class VWAExtensionsCover(Scene):
    def construct(self):
        self.camera.background_color = C_BG
        loop_phase = ValueTracker(0)

        title = Text("Variable Wavenumber Approximation", font=TEXT_FONT, font_size=42, weight=BOLD, color=C_INK)
        subtitle = Text("fast nonlinear wave-group modelling across depth, bandwidth, and directionality", font=TEXT_FONT, font_size=21, color=C_MUTED)
        heading = VGroup(title, subtitle).arrange(DOWN, buff=0.02).to_edge(UP, buff=0.26)

        authors = self.author_line(font_size=17)
        affiliation = Text(
            "1 University of Oxford  |  2 University of Manchester  |  3 University of Western Australia",
            font=TEXT_FONT,
            font_size=14,
            color=C_MUTED,
        )
        byline = VGroup(authors, affiliation).arrange(DOWN, buff=0.01).next_to(heading, DOWN, buff=0.09)
        self.add(heading, byline)

        centers = [
            LEFT * 4.60 + UP * 0.76,
            ORIGIN + UP * 0.76,
            RIGHT * 4.60 + UP * 0.76,
            LEFT * 4.60 + DOWN * 2.16,
            ORIGIN + DOWN * 2.16,
            RIGHT * 4.60 + DOWN * 2.16,
        ]
        panels = [
            ("bandwidth + depth", C_BLUE, self.bandwidth_depth_panel),
            ("2nd to 5th order", C_GOLD, self.higher_order_panel),
            ("kinematics", C_TEAL, self.kinematics_panel),
            ("time series", C_ROSE, self.time_series_panel),
            ("inverse transform", C_PURPLE, self.inverse_panel),
            ("directional", C_GREEN, self.directional_panel),
        ]

        for center, (label, color, builder) in zip(centers, panels):
            box = panel_box(4.52, 2.86, color).move_to(center)
            heading = Text(label, font=TEXT_FONT, font_size=31, weight=BOLD, color=color).move_to(center + UP * 1.10)
            heading.scale_to_fit_width(min(heading.width, 4.04))
            visual = builder(center, loop_phase)
            visual.scale(1.16, about_point=center + DOWN * 0.02)
            self.add(box, heading, visual)
        self.add(self.cover_scenario_nav())
        self.play(loop_phase.animate.set_value(TAU), run_time=COVER_LOOP_SECONDS, rate_func=linear)

    def cover_scenario_nav(self):
        frame_w = config.frame_width
        frame_h = config.frame_height
        nav_h = 0.44
        nav_w = frame_w - 0.28
        y = -frame_h / 2 + nav_h / 2
        gap = 0.045
        segment_w = (nav_w - gap * 5) / 6
        left = -nav_w / 2

        bg = RoundedRectangle(
            width=frame_w,
            height=nav_h,
            corner_radius=0.09,
            stroke_width=0,
            fill_color=NAV_BG,
            fill_opacity=0.99,
        ).move_to([0, y, 0])
        top_rule = Line(
            [-frame_w / 2, y + nav_h / 2, 0],
            [frame_w / 2, y + nav_h / 2, 0],
            color=ManimColor("#334155"),
            stroke_width=1.1,
            stroke_opacity=0.9,
        )

        row = VGroup(bg, top_rule)
        for i, name in enumerate(NAV_SCENARIO_NAMES):
            color = NAV_SCENARIO_COLORS[i]
            x = left + i * (segment_w + gap) + segment_w / 2
            segment = RoundedRectangle(
                width=segment_w,
                height=0.25,
                corner_radius=0.06,
                stroke_width=0.8,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.28,
            ).move_to([x, y, 0])
            label = Text(
                f"S{i} {name}",
                font=NAV_FONT,
                font_size=13,
                color=NAV_TEXT,
                weight=BOLD,
            )
            label.scale_to_fit_width(min(label.width, segment_w - 0.16))
            label.move_to(segment)
            row.add(segment, label)

        row.set_z_index(1000)
        return row

    def author_line(self, font_size=18):
        entries = [
            ("Xinyu Liu", "1"),
            ("Tianning Tang", "1,2"),
            ("Paul Taylor", "3"),
            ("Wouter Mostert", "1"),
            ("Thomas Adcock", "1"),
        ]
        pieces = VGroup()
        for index, (name, affiliation) in enumerate(entries):
            name_text = Text(name, font=TEXT_FONT, font_size=font_size, color=C_INK)
            sup = Text(affiliation, font=TEXT_FONT, font_size=font_size * 0.50, color=C_INK)
            sup.next_to(name_text, UR, buff=0.015).shift(DOWN * 0.05)
            token = VGroup(name_text, sup)
            pieces.add(token)
            if index < len(entries) - 1:
                pieces.add(Text(",", font=TEXT_FONT, font_size=font_size, color=C_INK))
        pieces.arrange(RIGHT, buff=0.10, aligned_edge=DOWN)
        return pieces

    def bandwidth_depth_panel(self, center, loop_phase):
        group = VGroup()
        ax_origin = center + LEFT * 1.06 + DOWN * 0.78
        width = 2.55
        height = 1.45
        group.add(Line(ax_origin, ax_origin + RIGHT * width, color=C_MUTED, stroke_width=1.7).set_opacity(0.70))
        group.add(Line(ax_origin, ax_origin + UP * height, color=C_MUTED, stroke_width=1.7).set_opacity(0.70))
        group.add(MathTex(r"\alpha^{-1}", font_size=18, color=C_MUTED).move_to(ax_origin + RIGHT * (width + 0.20) + DOWN * 0.01))
        group.add(MathTex(r"k_p d", font_size=18, color=C_MUTED).rotate(PI / 2).next_to(ax_origin + UP * 0.78, LEFT, buff=0.05))

        def map_point(bandwidth, depth):
            return ax_origin + RIGHT * (bandwidth * width) + UP * (depth * height)

        def field_patch():
            phase = loop_phase.get_value()
            cells = VGroup()
            nx, ny = 13, 8
            for ix in range(nx):
                for iy in range(ny):
                    x = (ix + 0.5) / nx
                    y = (iy + 0.5) / ny
                    score = 0.48 + 0.28 * np.sin(2.5 * x + 1.8 * y + 0.35 * np.sin(phase))
                    score += 0.18 * np.exp(-4.0 * (x - 0.70) ** 2 - 5.5 * (y - 0.35) ** 2)
                    color = interpolate_color(C_BLUE, C_TEAL, np.clip(score, 0.0, 1.0))
                    cell = Rectangle(
                        width=width / nx * 0.92,
                        height=height / ny * 0.86,
                        stroke_width=0,
                        fill_color=color,
                        fill_opacity=0.18 + 0.38 * np.clip(score, 0.0, 1.0),
                    ).move_to(map_point(x, y))
                    cells.add(cell)
            return cells

        group.add(always_redraw(field_patch))
        cases = [
            (0.20, 0.82, C_BLUE, r"\mathrm{deep,\ narrow}"),
            (0.76, 0.28, C_ORANGE, r"\mathrm{shallow,\ broad}"),
        ]
        for bandwidth, depth, color, label in cases:
            dot = Dot(map_point(bandwidth, depth), radius=0.055, color=color).set_stroke(C_INK, width=1.2)
            tag = MathTex(label, font_size=15, color=color).next_to(dot, UP if depth < 0.55 else DOWN, buff=0.06)
            tag.scale_to_fit_width(min(tag.width, 1.30))
            group.add(dot, tag)
        relation = MathTex(r"\mathrm{accuracy}\ Q(\alpha,k_p d)", font_size=24, color=C_BLUE).move_to(center + DOWN * 1.02)
        relation.scale_to_fit_width(3.08)
        group.add(relation)
        return group

    def directional_panel(self, center, loop_phase):
        group = Group()
        frame_paths = sorted(COVER_DIRECTIONAL_FRAME_DIR.glob("directional_*.png"))
        if not frame_paths:
            warning = Text("directional loop missing", font=TEXT_FONT, font_size=20, color=C_GREEN)
            warning.move_to(center)
            group.add(warning)
            return group

        frames = []
        for frame_path in frame_paths:
            image = ImageMobject(str(frame_path))
            image.set_width(3.95)
            image.move_to(center + DOWN * 0.20)
            frames.append(image)

        def current_frame():
            phase = loop_phase.get_value() % TAU
            index = int((phase / TAU) * len(frames)) % len(frames)
            return frames[index].copy()

        relation = VGroup(
            MathTex(r"k", font_size=30, color=C_BLUE),
            Arrow(LEFT * 0.38, RIGHT * 0.38, buff=0, color=C_GREEN, stroke_width=4.0, max_tip_length_to_length_ratio=0.22),
            MathTex(r"\boldsymbol{\kappa}", font_size=30, color=C_GREEN),
        ).arrange(RIGHT, buff=0.12).move_to(center + DOWN * 0.88)
        note = Text("directional wavenumber", font=TEXT_FONT, font_size=15, color=C_MUTED).next_to(relation, DOWN, buff=0.02)

        group.add(always_redraw(current_frame), relation, note)
        return group

    def kinematics_panel(self, center, loop_phase):
        group = VGroup()
        ax_center = center + UP * 0.02
        group.add(local_axes(2.65, 1.08, x_label="x", y_label="z", font_size=18).move_to(ax_center))
        curve = animated_wave_group(2.58, 9.2, 0.34, 1.20, loop_phase, 0.3, C_ORANGE, stroke_width=4.2, center=ax_center)
        group.add(curve)
        for x0 in [-0.55, 0.55]:
            def probe_vector(x_sample=x0):
                phase = loop_phase.get_value() + 0.3
                y0 = 0.34 * np.exp(-1.20 * x_sample * x_sample) * np.sin(9.2 * x_sample + phase)
                pos = ax_center + RIGHT * x_sample + UP * y0
                origin = pos + UP * 0.15
                envelope = np.exp(-1.20 * x_sample * x_sample)
                u = 0.50 * envelope * np.cos(9.2 * x_sample + phase)
                w = 0.46 * envelope * np.sin(9.2 * x_sample + phase)
                return VGroup(
                    Dot(pos, radius=0.050, color=C_INK),
                    Dot(origin, radius=0.034, color=C_INK),
                    Arrow(origin, origin + RIGHT * u, buff=0, color=C_TEAL, stroke_width=4.4, max_tip_length_to_length_ratio=0.28),
                    Arrow(origin, origin + UP * w, buff=0, color=C_BLUE, stroke_width=4.4, max_tip_length_to_length_ratio=0.28),
                )

            group.add(always_redraw(probe_vector))
        formula = MathTex(r"u_s,", r"\ w_s", font_size=33).move_to(center + DOWN * 1.02)
        formula[0].set_color(C_TEAL)
        formula[1].set_color(C_BLUE)
        group.add(formula)
        return group

    def time_series_panel(self, center, loop_phase):
        group = VGroup()
        top = center + UP * 0.34
        bottom = center + DOWN * 0.42
        group.add(local_axes(2.65, 0.54, x_label="t", y_label="", font_size=16).move_to(top))
        group.add(local_axes(2.65, 0.54, x_label="t", y_label="", font_size=16).move_to(bottom))
        fixed_phase = 0.35
        linear = wave_group(2.60, 10.0, 0.16, 1.35, fixed_phase, C_BLUE, stroke_width=3.7).move_to(top)
        nonlinear = FunctionGraph(
            lambda x: 0.16 * np.exp(-1.35 * x * x) * np.sin(10.0 * x + fixed_phase)
            + 0.06 * np.exp(-1.55 * x * x) * np.sin(20.0 * x + 2.0 * fixed_phase + 0.45),
            x_range=[-1.30, 1.30],
            color=C_ORANGE,
            stroke_width=3.7,
        ).move_to(bottom)

        def moving_probe():
            cursor_x = -1.18 + (loop_phase.get_value() % TAU) / TAU * 2.36
            y_lin = 0.16 * np.exp(-1.35 * cursor_x * cursor_x) * np.sin(10.0 * cursor_x + fixed_phase)
            y_nl = y_lin + 0.06 * np.exp(-1.55 * cursor_x * cursor_x) * np.sin(
                20.0 * cursor_x + 2.0 * fixed_phase + 0.45
            )
            return VGroup(
                Line(top + RIGHT * cursor_x + DOWN * 0.34, top + RIGHT * cursor_x + UP * 0.34, color=C_INK, stroke_width=2.3),
                DashedLine(top + RIGHT * cursor_x + DOWN * 0.32, bottom + RIGHT * cursor_x + UP * 0.32, color=C_MUTED, stroke_width=1.6, dash_length=0.05),
                Dot(top + RIGHT * cursor_x + UP * y_lin, radius=0.034, color=C_INK),
                Dot(bottom + RIGHT * cursor_x + UP * y_nl, radius=0.034, color=C_INK),
            )

        group.add(linear, nonlinear, always_redraw(moving_probe))
        arrow = Arrow(top + DOWN * 0.32, bottom + UP * 0.32, buff=0.05, color=C_ROSE, stroke_width=4.2)
        relation = VGroup(
            Text("linear", font=TEXT_FONT, font_size=24, weight=BOLD, color=C_BLUE),
            Arrow(LEFT * 0.36, RIGHT * 0.36, buff=0, color=C_ROSE, stroke_width=4.0, max_tip_length_to_length_ratio=0.22),
            Text("nonlinear", font=TEXT_FONT, font_size=24, weight=BOLD, color=C_ORANGE),
        ).arrange(RIGHT, buff=0.12).move_to(center + DOWN * 0.88)
        note = Text("add bound harmonics", font=TEXT_FONT, font_size=15, color=C_MUTED).next_to(relation, DOWN, buff=0.02)
        group.add(arrow, relation, note)
        group.add(Text("linear input", font=TEXT_FONT, font_size=17, color=C_BLUE).move_to(top + RIGHT * 0.60 + UP * 0.36))
        group.add(Text("nonlinear output", font=TEXT_FONT, font_size=17, color=C_ORANGE).move_to(bottom + RIGHT * 0.42 + UP * 0.34))
        return group

    def inverse_panel(self, center, loop_phase):
        group = VGroup()
        top = center + UP * 0.38
        bottom = center + DOWN * 0.40
        group.add(local_axes(2.65, 0.54, x_label="x", y_label="", font_size=16).move_to(top))
        group.add(local_axes(2.65, 0.54, x_label="x", y_label="", font_size=16).move_to(bottom))
        fixed_phase = 0.25
        nonlinear = FunctionGraph(
            lambda x: 0.17 * np.exp(-1.35 * x * x) * np.sin(10.0 * x + fixed_phase)
            + 0.07 * np.exp(-1.50 * x * x) * np.sin(20.0 * x + 2.0 * fixed_phase + 0.3),
            x_range=[-1.30, 1.30],
            color=C_ORANGE,
            stroke_width=4.0,
        ).move_to(top)
        linear = wave_group(2.60, 10.0, 0.17, 1.35, fixed_phase, C_BLUE, stroke_width=4.0).move_to(bottom)
        arrow = Arrow(top + DOWN * 0.31, bottom + UP * 0.31, buff=0.05, color=C_PURPLE, stroke_width=4.0)
        relation = VGroup(
            Text("nonlinear", font=TEXT_FONT, font_size=24, weight=BOLD, color=C_ORANGE),
            Arrow(LEFT * 0.36, RIGHT * 0.36, buff=0, color=C_PURPLE, stroke_width=4.0, max_tip_length_to_length_ratio=0.22),
            Text("linear", font=TEXT_FONT, font_size=24, weight=BOLD, color=C_BLUE),
        ).arrange(RIGHT, buff=0.12).move_to(center + DOWN * 0.88)
        note = Text("recover linear modes", font=TEXT_FONT, font_size=15, color=C_MUTED).next_to(relation, DOWN, buff=0.02)
        labels = VGroup(
            Text("nonlinear input", font=TEXT_FONT, font_size=16, color=C_ORANGE).move_to(top + LEFT * 0.35 + UP * 0.36),
            Text("linear modes", font=TEXT_FONT, font_size=16, color=C_BLUE).move_to(bottom + LEFT * 0.52 + UP * 0.36),
        )
        group.add(nonlinear, linear, arrow, labels, relation, note)
        return group

    def higher_order_panel(self, center, loop_phase):
        group = VGroup()
        caption = MathTex(
            r"\mathrm{order}\ n:",
            r"\quad \mathrm{exact}\sim N_c^n,",
            r"\quad \mathrm{VWA}\sim N_c\log N_c",
            font_size=19,
            color=C_INK,
        ).move_to(center + UP * 0.58)
        caption[1].set_color(C_ORANGE)
        caption[2].set_color(C_TEAL)
        caption.scale_to_fit_width(3.12)
        group.add(caption)

        chart_origin = center + LEFT * 1.18 + DOWN * 0.84
        chart_w = 2.55
        chart_h = 1.30
        group.add(Line(chart_origin, chart_origin + RIGHT * chart_w, color=C_MUTED, stroke_width=1.5).set_opacity(0.65))
        group.add(Line(chart_origin, chart_origin + UP * chart_h, color=C_MUTED, stroke_width=1.5).set_opacity(0.65))
        group.add(
            MathTex(r"\log_{10}\mathrm{cost}", font_size=15, color=C_MUTED)
            .rotate(PI / 2)
            .next_to(chart_origin + UP * 0.68, LEFT, buff=0.04)
        )

        nc_log = np.log10(64)
        vwa_log = np.log10(64 * np.log2(64))
        ymin, ymax = 2.0, 9.2

        def height_from_log(value):
            return (value - ymin) / (ymax - ymin) * chart_h

        for x_pos, order in zip(np.linspace(0.38, 2.24, 4), [2, 3, 4, 5]):
            exact_h = height_from_log(order * nc_log)
            vwa_h = height_from_log(vwa_log)
            exact_bar = Rectangle(
                width=0.17,
                height=exact_h,
                stroke_width=0,
                fill_color=C_ORANGE,
                fill_opacity=0.88,
            ).move_to(chart_origin + RIGHT * (x_pos - 0.10) + UP * exact_h / 2)
            vwa_bar = Rectangle(
                width=0.17,
                height=vwa_h,
                stroke_width=0,
                fill_color=C_TEAL,
                fill_opacity=0.88,
            ).move_to(chart_origin + RIGHT * (x_pos + 0.10) + UP * vwa_h / 2)
            order_label = MathTex(rf"{order}", font_size=18, color=C_INK).move_to(chart_origin + RIGHT * x_pos + DOWN * 0.17)
            group.add(exact_bar, vwa_bar, order_label)

        group.add(MathTex(r"n", font_size=18, color=C_MUTED).move_to(chart_origin + RIGHT * 2.73 + DOWN * 0.04))
        return group
