"""
Scenario 5 - Applications of the VWA Approximation
==================================================

One-page bridge after Scenario 4.  The page keeps four columns on screen while
the examples keep moving: directional wave groups, surface kinematics, time
series, and the inverse Creamer problem.
"""

from manim import *
from presentation_nav import bottom_progress_nav

C_DIRECTIONAL = GREEN_B
C_ELEVATION = ORANGE
C_BOUND = YELLOW
C_LINEAR = BLUE_B
C_KIN = TEAL
C_US = TEAL
C_WS = BLUE_D
C_MUTED = GREY_B
C_PANEL = GREY_D
C_INVERSE = PURPLE_B
SCENARIO5_SECONDS = 30.0
SCENARIO5_SUBSCENARIOS = [
    "directional",
    "kinematics",
    "time series",
    "inverse transform",
]


def frame_box(center, width, height, color):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.08, color=color, stroke_width=2.4)
    box.set_fill(BLACK, opacity=0.055)
    return box.move_to(center)


def axes_at(center, width=2.25, height=1.08, x_label="x", y_label=r"\eta", font_size=17):
    ax = VGroup(
        Line(LEFT * width / 2, RIGHT * width / 2, color=C_MUTED, stroke_width=1.8),
        Line(DOWN * height / 2, UP * height / 2, color=C_MUTED, stroke_width=1.8),
        MathTex(x_label, font_size=font_size, color=C_MUTED).move_to(RIGHT * (width / 2 + 0.14)),
        MathTex(y_label, font_size=font_size, color=C_MUTED).move_to(UP * (height / 2 + 0.15)),
    )
    ax.set_opacity(0.62)
    return ax.move_to(center)


def wave_curve(center, width, carrier, amp, phase, color, stroke_width=3.0, envelope=0.22, y_shift=0.0):
    return FunctionGraph(
        lambda x: amp * np.exp(-envelope * x * x) * np.sin(carrier * x + phase),
        x_range=[-width / 2, width / 2],
        color=color,
        stroke_width=stroke_width,
    ).move_to(center + DOWN * y_shift)


def wave_group_curve(center, width, carrier, amp, phase, color, stroke_width=3.0, envelope=1.55, y_shift=0.0):
    return FunctionGraph(
        lambda x: amp * np.exp(-envelope * x * x) * np.sin(carrier * x + phase),
        x_range=[-width / 2, width / 2],
        color=color,
        stroke_width=stroke_width,
    ).move_to(center + DOWN * y_shift)


class SurfaceKinematicsVWA(Scene):
    def construct(self):
        title = Text("Extensions of VWA", font_size=46, weight=BOLD)
        subtitle = Text("completed application routes using the same compact structure", font_size=28, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav_progress.add_updater(
            lambda tracker, dt: tracker.increment_value(len(SCENARIO5_SUBSCENARIOS) * dt / SCENARIO5_SECONDS)
        )
        nav = bottom_progress_nav(
            5,
            6,
            "extensions of VWA",
            SCENARIO5_SUBSCENARIOS,
            nav_progress,
            accent=C_BOUND,
        )
        self.add(title, subtitle)
        self.add(nav_progress, nav)

        phase = ValueTracker(0.0)
        centers = [LEFT * 4.55 + DOWN * 0.02, LEFT * 1.52 + DOWN * 0.02, RIGHT * 1.52 + DOWN * 0.02, RIGHT * 4.55 + DOWN * 0.02]
        headings = [
            ("directional", C_DIRECTIONAL),
            ("kinematics", C_KIN),
            ("time series", C_ELEVATION),
            ("inverse transform", C_INVERSE),
        ]

        columns = VGroup()
        visuals = VGroup()
        for center, (heading, color) in zip(centers, headings):
            box = frame_box(center, 2.82, 3.16, color)
            label = Text(heading, font_size=28, color=color, weight=BOLD).move_to(center + UP * 1.28)
            label.scale_to_fit_width(min(label.width, 2.48))
            columns.add(VGroup(box, label))

        visuals.add(always_redraw(lambda: self.directional_wave_group(centers[0] + DOWN * 0.05, phase.get_value())))
        visuals.add(always_redraw(lambda: self.kinematics_visual(centers[1] + DOWN * 0.05, phase.get_value())))
        visuals.add(always_redraw(lambda: self.time_series_visual(centers[2] + DOWN * 0.05, phase.get_value())))
        visuals.add(always_redraw(lambda: self.inverse_creamer_visual(centers[3] + DOWN * 0.05, phase.get_value())))

        takeaway = Text(
            "VWA is a compact moving model across these extensions.",
            font_size=32,
            color=C_BOUND,
        ).to_edge(DOWN, buff=0.88)
        takeaway.scale_to_fit_width(11.4)
        self.add(columns, visuals, takeaway)
        self.play(phase.animate.set_value(8 * TAU), run_time=30.0, rate_func=linear)
        nav_progress.clear_updaters()

    def directional_wave_group(self, center, phase):
        group = VGroup()
        surf_center = center + UP * 0.03
        theta = 55 * DEGREES
        kx = np.cos(theta)
        ky = np.sin(theta)
        travel_dir = np.array([kx, ky, 0.0])
        crest_dir = np.array([-ky, kx, 0.0])

        def project(x, y, z):
            return surf_center + RIGHT * (0.88 * x + 0.44 * y) + UP * (0.34 * y + 0.92 * z)

        envelope_points = []
        for angle in np.linspace(0, TAU, 96):
            local = travel_dir * (1.12 * np.cos(angle)) + crest_dir * (0.68 * np.sin(angle))
            envelope_points.append(project(local[0], local[1], 0.0))
        envelope_outline = VMobject(color=C_DIRECTIONAL, stroke_width=1.8).set_points_smoothly(envelope_points)
        envelope_outline.set_opacity(0.38)
        group.add(envelope_outline)

        q_samples = np.linspace(-1.18, 1.18, 78)
        r_samples = np.linspace(-0.58, 0.58, 7)
        for r in r_samples:
            points = []
            base_points = []
            transverse_weight = np.exp(-2.15 * r * r)
            for q in q_samples:
                envelope = np.exp(-1.18 * q * q - 2.15 * r * r)
                carrier = np.sin(17.0 * q - phase)
                z = 0.30 * envelope * carrier
                local = travel_dir * q + crest_dir * r
                points.append(project(local[0], local[1], z))
                base_points.append(project(local[0], local[1], 0.0))
            base = VMobject(color=C_MUTED, stroke_width=0.8).set_points_smoothly(base_points).set_opacity(0.14)
            wave = VMobject(
                color=interpolate_color(C_DIRECTIONAL, WHITE, 0.18 * transverse_weight),
                stroke_width=1.5 + 1.9 * transverse_weight,
            ).set_points_smoothly(points).set_opacity(0.46 + 0.34 * transverse_weight)
            group.add(base, wave)

        wavelength = TAU / 17.0
        crest_phase = (phase % TAU) / 17.0
        for q0 in np.arange(-0.95, 1.05, wavelength):
            q = ((q0 + crest_phase + 1.05) % 2.10) - 1.05
            points = []
            for r in np.linspace(-0.56, 0.56, 24):
                envelope = np.exp(-1.18 * q * q - 2.15 * r * r)
                if envelope < 0.22:
                    continue
                local = travel_dir * q + crest_dir * r
                points.append(project(local[0], local[1], 0.03 + 0.22 * envelope))
            if len(points) >= 3:
                group.add(VMobject(color=WHITE, stroke_width=1.5).set_points_smoothly(points).set_opacity(0.34))

        arrow = Arrow(project(-0.76, -0.47, 0.22), project(0.66, 0.50, 0.31), buff=0, color=C_DIRECTIONAL, stroke_width=5.0)
        label = MathTex(r"\mathbf{k}=(k_x,k_y)", font_size=25, color=C_DIRECTIONAL).move_to(center + DOWN * 1.05)
        xy = VGroup(
            MathTex("x", font_size=18, color=C_MUTED).move_to(project(1.13, -0.70, 0)),
            MathTex("y", font_size=18, color=C_MUTED).move_to(project(-1.03, 0.80, 0)),
        )
        group.add(arrow, xy, label)
        return group

    def kinematics_visual(self, center, phase):
        group = VGroup()
        ax_center = center + UP * 0.08
        group.add(axes_at(ax_center, width=2.42, height=1.22, x_label="x", y_label="z", font_size=18))
        curve = wave_group_curve(ax_center, 2.38, 8.9, 0.31, phase, C_ELEVATION, stroke_width=3.8, envelope=1.30)
        group.add(curve)

        for x0 in [-0.58, 0.58]:
            y0 = 0.31 * np.exp(-1.30 * x0 * x0) * np.sin(8.9 * x0 + phase)
            pos = ax_center + RIGHT * x0 + UP * y0
            group.add(Dot(pos, radius=0.040, color=WHITE))
            group.add(Arrow(pos + LEFT * 0.20 + UP * 0.15, pos + RIGHT * 0.25 + UP * 0.15, buff=0, color=C_US, stroke_width=3.4))
            group.add(Arrow(pos + RIGHT * 0.18 + DOWN * 0.03, pos + RIGHT * 0.18 + UP * 0.34, buff=0, color=C_WS, stroke_width=3.4))

        formula = MathTex(r"u_s,", r"\ w_s", font_size=33).move_to(center + DOWN * 0.98)
        formula[0].set_color(C_US)
        formula[1].set_color(C_WS)
        group.add(formula)
        return group

    def time_series_visual(self, center, phase):
        group = VGroup()
        linear_center = center + UP * 0.47
        nonlinear_center = center + DOWN * 0.34
        group.add(axes_at(linear_center, width=2.40, height=0.74, x_label="t", y_label="", font_size=15))
        group.add(axes_at(nonlinear_center, width=2.40, height=0.74, x_label="t", y_label="", font_size=15))

        fixed_phase = 0.35
        linear = wave_group_curve(linear_center, 2.38, 10.0, 0.18, fixed_phase, C_LINEAR, stroke_width=3.3, envelope=1.38)
        nonlinear = FunctionGraph(
            lambda x: 0.18 * np.exp(-1.38 * x * x) * np.sin(10.0 * x + fixed_phase)
            + 0.060 * np.exp(-1.58 * x * x) * np.sin(20.0 * x + 2 * fixed_phase + 0.45),
            x_range=[-1.19, 1.19],
            color=C_ELEVATION,
            stroke_width=3.3,
        ).move_to(nonlinear_center)
        cursor_x = -1.12 + (phase % TAU) / TAU * 2.24
        y_lin = 0.18 * np.exp(-1.38 * cursor_x * cursor_x) * np.sin(10.0 * cursor_x + fixed_phase)
        y_nl = y_lin + 0.060 * np.exp(-1.58 * cursor_x * cursor_x) * np.sin(20.0 * cursor_x + 2 * fixed_phase + 0.45)
        probe = VGroup(
            Line(linear_center + RIGHT * cursor_x + DOWN * 0.39, linear_center + RIGHT * cursor_x + UP * 0.39, color=WHITE, stroke_width=2.2),
            Dot(linear_center + RIGHT * cursor_x + UP * y_lin, radius=0.040, color=WHITE),
        )
        arrow = Arrow(linear_center + DOWN * 0.28, nonlinear_center + UP * 0.28, buff=0.05, color=C_MUTED, stroke_width=2.2)
        cursor_lin = DashedLine(linear_center + RIGHT * cursor_x + DOWN * 0.33, linear_center + RIGHT * cursor_x + UP * y_lin, color=WHITE, stroke_width=1.7, dash_length=0.04)
        cursor_nl = DashedLine(nonlinear_center + RIGHT * cursor_x + DOWN * 0.33, nonlinear_center + RIGHT * cursor_x + UP * y_nl, color=WHITE, stroke_width=1.7, dash_length=0.04)
        labels = VGroup(
            Text("linear", font_size=17, color=C_LINEAR).move_to(linear_center + RIGHT * 0.48 + UP * 0.40),
            Text("nonlinear", font_size=17, color=C_ELEVATION).move_to(nonlinear_center + RIGHT * 0.36 + UP * 0.40),
            Text("probe", font_size=16, color=WHITE).move_to(center + LEFT * 0.77 + DOWN * 1.02),
        )
        group.add(linear, nonlinear, arrow, probe, cursor_lin, cursor_nl, Dot(linear_center + RIGHT * cursor_x + UP * y_lin, radius=0.030, color=WHITE), Dot(nonlinear_center + RIGHT * cursor_x + UP * y_nl, radius=0.030, color=WHITE), labels)
        return group

    def inverse_creamer_visual(self, center, phase):
        group = VGroup()
        nonlinear_center = center + UP * 0.47
        linear_center = center + DOWN * 0.35
        group.add(axes_at(nonlinear_center, width=2.40, height=0.74, x_label="x", y_label="", font_size=15))
        group.add(axes_at(linear_center, width=2.40, height=0.74, x_label="x", y_label="", font_size=15))

        fixed_phase = 0.25
        nonlinear = FunctionGraph(
            lambda x: 0.18 * np.exp(-1.38 * x * x) * np.sin(10.0 * x + fixed_phase)
            + 0.060 * np.exp(-1.58 * x * x) * np.sin(20.0 * x + 2 * fixed_phase + 0.3),
            x_range=[-1.19, 1.19],
            color=C_ELEVATION,
            stroke_width=3.8,
        ).move_to(nonlinear_center)
        linear = wave_group_curve(linear_center, 2.38, 10.0, 0.18, fixed_phase, C_LINEAR, stroke_width=3.8, envelope=1.38)
        arrow = Arrow(nonlinear_center + DOWN * 0.30, linear_center + UP * 0.30, buff=0.05, color=C_INVERSE, stroke_width=3.0, max_tip_length_to_length_ratio=0.24)
        labels = VGroup(
            Text("nonlinear space", font_size=16, color=C_ELEVATION).move_to(nonlinear_center + LEFT * 0.38 + UP * 0.40),
            Text("linear space", font_size=16, color=C_LINEAR).move_to(linear_center + LEFT * 0.50 + UP * 0.40),
        )
        relation = MathTex(r"\eta_{\rm nl}(x)\rightarrow\eta_{\rm lin}(x)", font_size=23, color=C_INVERSE).move_to(center + DOWN * 1.07)
        group.add(nonlinear, linear, arrow, labels, relation)
        return group
