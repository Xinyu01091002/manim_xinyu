"""
Scenario 5 - Applications of the VWA Approximation
==================================================

One-page bridge after Scenario 4.  The page keeps four columns on screen while
the examples keep moving: directional wave groups, surface kinematics, time
series, and the inverse Creamer problem.
"""

from manim import *
from pathlib import Path
from presentation_nav import bottom_progress_nav

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene

C_DIRECTIONAL = GREEN_B
C_ELEVATION = ORANGE
C_BOUND = YELLOW
C_LINEAR = BLUE_B
C_KIN = TEAL
C_US = TEAL
C_WS = BLUE_D
C_TIME = ManimColor("#FF8BC7")
C_MUTED = GREY_B
C_PANEL = GREY_D
C_INVERSE = PURPLE_B
SCENARIO5_SECONDS = 30.0
S5_DIRECTIONAL_FRAME_DIR = Path(__file__).resolve().parent / "data" / "cover_directional_frames"
DIRECTIONAL_DATA_DIR = Path(__file__).resolve().parent / "data" / "directional_extension"
CENTERLINE_DEFINITION_IMAGE = DIRECTIONAL_DATA_DIR / "centerline_offcenterline_manim_style.png"
DIRECTIONAL_ETA_RESULT_IMAGES = [
    DIRECTIONAL_DATA_DIR / "eta22_kd1p0_spread25_Akp0p02_t00900_manim.png",
    DIRECTIONAL_DATA_DIR / "eta33_kd1p0_spread25_Akp0p12_t01200_manim.png",
    DIRECTIONAL_DATA_DIR / "eta44_kd1p0_spread25_Akp0p12_t01200_manim.png",
    DIRECTIONAL_DATA_DIR / "eta55_kd5p0_spread15_Akp0p12_t01200_manim.png",
]
DIRECTIONAL_PHI_RESULT_IMAGES = [
    DIRECTIONAL_DATA_DIR / "phi22_kd1p0_spread25_Akp0p02_t00900_manim.png",
    DIRECTIONAL_DATA_DIR / "phi33_kd1p0_spread25_Akp0p12_t01200_manim.png",
    DIRECTIONAL_DATA_DIR / "phi44_kd1p0_spread25_Akp0p12_t01200_manim.png",
    DIRECTIONAL_DATA_DIR / "phi55_kd1p0_spread25_Akp0p12_t01200_manim.png",
]
TIME_SERIES_DATA_DIR = Path(__file__).resolve().parent / "data" / "time_series"
TIME_SERIES_PHI_IMAGE = TIME_SERIES_DATA_DIR / "phi_timeseries_kd5p0_alpha8p0_akp0p02_manim.png"
KINEMATICS_DATA_DIR = Path(__file__).resolve().parent / "data" / "kinematics"
KINEMATICS_RESULT_IMAGE = KINEMATICS_DATA_DIR / "superharmonic_spatial_waveform_manim_style.png"
INVERSE_VWA_DATA_DIR = Path(__file__).resolve().parent / "data" / "inverse_vwa"
INVERSE_WAVEFORMS_CSV = INVERSE_VWA_DATA_DIR / "waveforms.csv"
INVERSE_SPECTRA_CSV = INVERSE_VWA_DATA_DIR / "spectra.csv"
INVERSE_RESIDUAL_CSV = INVERSE_VWA_DATA_DIR / "residual_history.csv"
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


def semantic_badge(center, width, height, color, fill_opacity=0.08, stroke_opacity=0.8):
    badge = RoundedRectangle(width=width, height=height, corner_radius=0.12, color=color, stroke_width=1.8)
    badge.set_fill(color, opacity=fill_opacity)
    badge.set_stroke(color, opacity=stroke_opacity)
    return badge.move_to(center)


def axes_at(center, width=2.25, height=1.08, x_label="x", y_label=r"\eta", font_size=17):
    ax = VGroup(
        Line(LEFT * width / 2, RIGHT * width / 2, color=C_MUTED, stroke_width=1.8),
        Line(DOWN * height / 2, UP * height / 2, color=C_MUTED, stroke_width=1.8),
        MathTex(x_label, font_size=font_size, color=C_MUTED).move_to(RIGHT * (width / 2 + 0.14)),
        MathTex(y_label, font_size=font_size, color=C_MUTED).move_to(UP * (height / 2 + 0.15)),
    )
    ax.set_opacity(0.62)
    return ax.move_to(center)


def component_arrow(origin, vector, color, stroke_width=6.3):
    if np.linalg.norm(vector) < 0.045:
        return Dot(origin, radius=0.026, color=color)
    return Arrow(
        origin,
        origin + vector,
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.46,
    )


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


class S5SurfaceKinematicsSlides(Slide):
    def slide_pause(self, nav_progress=None, progress=None):
        if nav_progress is not None and progress is not None:
            nav_progress.clear_updaters()
            nav_progress.set_value(progress)
            self.wait(0.1)
        if hasattr(self, "next_slide"):
            self.next_slide(loop=False)
        else:
            self.wait(0.8)

    def construct(self):
        nav_progress = ValueTracker(0)
        nav = bottom_progress_nav(
            5,
            6,
            "extensions of VWA",
            SCENARIO5_SUBSCENARIOS,
            nav_progress,
            accent=C_BOUND,
            detail_label_color=WHITE,
            detail_font_size=16,
            detail_label_stroke=False,
        )
        phase = ValueTracker(0.0)
        cover = self.cover_overview(phase)
        self.add(cover)
        self.add(nav_progress, nav)
        self.slide_pause(nav_progress, 0.35)
        self.play(phase.animate.set_value(2 * TAU), run_time=6.0, rate_func=linear)
        self.slide_pause(nav_progress, 0.80)

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(0.92)

        directional_intro = self.directional_extension_intro()
        self.add(directional_intro)
        self.wait(0.1)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(0.95)

        directional_definition = self.directional_centerline_definition()
        self.add(directional_definition)
        self.wait(0.1)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(0.98)

        directional_eta_results = self.directional_ow3d_results(DIRECTIONAL_ETA_RESULT_IMAGES)
        self.add(directional_eta_results)
        self.wait(0.1)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(0.99)

        directional_phi_results = self.directional_ow3d_results(DIRECTIONAL_PHI_RESULT_IMAGES)
        self.add(directional_phi_results)
        self.wait(0.1)
        self.slide_pause()

        self.play(FadeOut(directional_phi_results), run_time=0.45)
        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(1.20)

        kinematics_intro = self.kinematics_intro()
        self.play(FadeIn(kinematics_intro, shift=DOWN * 0.05), run_time=0.75)
        self.slide_pause()

        self.play(FadeOut(kinematics_intro), run_time=0.45)
        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(1.72)

        kinematics_result = self.kinematics_result()
        self.play(FadeIn(kinematics_result, shift=DOWN * 0.05), run_time=0.75)
        self.slide_pause()

        self.play(FadeOut(kinematics_result), run_time=0.45)
        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(2.20)

        time_series_intro = self.time_series_intro()
        self.play(FadeIn(time_series_intro, shift=DOWN * 0.05), run_time=0.75)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        time_series_phi = self.time_series_result(TIME_SERIES_PHI_IMAGE)
        self.add(time_series_phi)
        nav_progress.set_value(2.90)
        self.play(nav_progress.animate.set_value(2.92), run_time=0.10, rate_func=linear)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(3.18)

        inverse_intro = self.inverse_vwa_intro()
        self.add(inverse_intro)
        self.play(nav_progress.animate.set_value(3.22), run_time=0.10, rate_func=linear)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(3.48)

        inverse_demo, inverse_iteration = self.inverse_vwa_iteration_demo()
        self.add(inverse_demo)
        self.wait(0.1)
        self.slide_pause()
        self.play(inverse_iteration.animate.set_value(5), nav_progress.animate.set_value(3.60), run_time=3.0, rate_func=smooth)
        self.play(inverse_iteration.animate.set_value(15), nav_progress.animate.set_value(3.74), run_time=2.4, rate_func=smooth)
        self.play(inverse_iteration.animate.set_value(60), nav_progress.animate.set_value(3.92), run_time=3.2, rate_func=smooth)
        self.slide_pause()

        self.clear()
        self.add(nav_progress, nav)
        nav_progress.clear_updaters()
        nav_progress.set_value(3.98)
        final_phase = ValueTracker(0.0)
        final_cover = self.cover_overview(final_phase)
        self.add(final_cover)
        self.play(final_phase.animate.set_value(2 * TAU), nav_progress.animate.set_value(4.0), run_time=8.0, rate_func=linear)
        if hasattr(self, "next_slide"):
            self.next_slide(loop=True)
        else:
            self.wait(0.8)

    def cover_overview(self, phase):
        title = Text("Extensions of VWA", font_size=50, weight=BOLD)
        subtitle = Text("completed application routes using the same compact structure", font_size=31, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)

        centers = [LEFT * 4.86 + DOWN * 0.04, LEFT * 1.62 + DOWN * 0.04, RIGHT * 1.62 + DOWN * 0.04, RIGHT * 4.86 + DOWN * 0.04]
        headings = [
            ("directional", C_DIRECTIONAL),
            ("kinematics", C_KIN),
            ("time series", C_TIME),
            ("inverse transform", C_INVERSE),
        ]

        columns = VGroup()
        visuals = Group()
        for center, (heading, color) in zip(centers, headings):
            box = frame_box(center, 3.16, 3.34, color)
            label = Text(heading, font_size=32, color=color, weight=BOLD).move_to(center + UP * 1.38)
            label.scale_to_fit_width(min(label.width, 2.82))
            columns.add(VGroup(box, label))

        visuals.add(self.directional_wave_group(centers[0] + DOWN * 0.05, phase))
        visuals.add(always_redraw(lambda: self.kinematics_visual(centers[1] + DOWN * 0.03, phase.get_value())))
        visuals.add(always_redraw(lambda: self.time_series_visual(centers[2] + DOWN * 0.03, phase.get_value())))
        visuals.add(always_redraw(lambda: self.inverse_creamer_visual(centers[3] + DOWN * 0.03, phase.get_value())))

        takeaway = Text(
            "VWA is a compact moving model across these extensions.",
            font_size=30,
            color=C_BOUND,
        ).to_edge(DOWN, buff=1.04)
        takeaway.scale_to_fit_width(11.4)
        return Group(title, subtitle, columns, visuals, takeaway)

    def directional_wave_group(self, center, phase):
        group = Group()
        frame_paths = sorted(S5_DIRECTIONAL_FRAME_DIR.glob("directional_*.png"))
        if frame_paths:
            if isinstance(phase, ValueTracker):
                frames = Group()
                for index, path in enumerate(frame_paths):
                    image = ImageMobject(str(path))
                    image.set_width(2.92)
                    image.move_to(center + UP * 0.04)
                    image.set_opacity(1.0 if index == 0 else 0.0)
                    image.add_updater(
                        lambda mob, idx=index, total=len(frame_paths): mob.set_opacity(
                            1.0
                            if idx == int((phase.get_value() % TAU) / TAU * total) % total
                            else 0.0
                        )
                    )
                    frames.add(image)
                group.add(frames)
            else:
                frame_index = int((phase % TAU) / TAU * len(frame_paths)) % len(frame_paths)
                image = ImageMobject(str(frame_paths[frame_index]))
                image.set_width(2.92)
                image.move_to(center + UP * 0.04)
                group.add(image)
        else:
            group.add(Text("directional loop missing", font_size=18, color=C_DIRECTIONAL).move_to(center))

        travel_badge = semantic_badge(center + DOWN * 1.13, 1.92, 0.50, C_DIRECTIONAL, fill_opacity=0.06, stroke_opacity=0.55)
        label = VGroup(
            MathTex(r"k", font_size=25, color=C_LINEAR),
            Arrow(LEFT * 0.26, RIGHT * 0.26, buff=0, color=C_DIRECTIONAL, stroke_width=3.0, max_tip_length_to_length_ratio=0.28),
            MathTex(r"\boldsymbol{\kappa}", font_size=25, color=C_DIRECTIONAL),
        ).arrange(RIGHT, buff=0.08).move_to(travel_badge.get_center())
        group.add(travel_badge, label)
        return group

    def directional_extension_intro(self):
        title = Text("Directional extension", font_size=44, weight=BOLD)
        subtitle = Text("the scalar wavenumber becomes a directional wavenumber vector", font_size=25, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.22)

        relation = VGroup(
            MathTex(r"k", font_size=72, color=C_LINEAR),
            Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=C_DIRECTIONAL, stroke_width=6.0, max_tip_length_to_length_ratio=0.22),
            MathTex(r"\boldsymbol{\kappa}=(k_x,k_y)", font_size=64, color=C_DIRECTIONAL),
        ).arrange(RIGHT, buff=0.28).move_to(UP * 0.86)
        relation_box = semantic_badge(relation.get_center(), relation.width + 0.52, 1.18, C_DIRECTIONAL, fill_opacity=0.055, stroke_opacity=0.72)

        left = VGroup(
            Text("unidirectional VWA", font_size=27, color=C_LINEAR, weight=BOLD),
            MathTex(r"G_n(k)", font_size=38, color=C_LINEAR),
            Text("one propagation axis", font_size=22, color=C_MUTED),
        ).arrange(DOWN, buff=0.16)
        right = VGroup(
            Text("directional VWA", font_size=27, color=C_DIRECTIONAL, weight=BOLD),
            MathTex(r"G_n(\boldsymbol{\kappa})", font_size=38, color=C_DIRECTIONAL),
            Text("centerline and off-centerline sections", font_size=22, color=C_MUTED),
        ).arrange(DOWN, buff=0.16)
        columns = VGroup(left, right).arrange(RIGHT, buff=1.22).next_to(relation_box, DOWN, buff=0.48)
        for block, color in [(left, C_LINEAR), (right, C_DIRECTIONAL)]:
            box = SurroundingRectangle(block, color=color, buff=0.22, corner_radius=0.08)
            box.set_fill(BLACK, opacity=0.08)
            block.add_to_back(box)

        takeaway = Text("same compact VWA idea; geometry changes from a line to a horizontal wave-vector plane", font_size=25, color=C_DIRECTIONAL)
        takeaway.scale_to_fit_width(11.2).to_edge(DOWN, buff=1.04)
        return VGroup(title, subtitle, relation_box, relation, columns, takeaway)

    def directional_centerline_definition(self):
        title = Text("Where do we compare a directional group?", font_size=39, weight=BOLD)
        subtitle = Text("centerline and off-centerline slices turn a 3D focused group into readable sections", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.20)

        if CENTERLINE_DEFINITION_IMAGE.exists():
            image = ImageMobject(str(CENTERLINE_DEFINITION_IMAGE))
            image.set_width(13.15)
            image.move_to(UP * 0.20)
        else:
            image = Text("centerline definition image missing", font_size=28, color=C_MUTED).move_to(ORIGIN)
        return Group(image)

    def directional_ow3d_results(self, image_paths):
        panels = Group()
        for path in image_paths:
            if path.exists():
                image = ImageMobject(str(path))
                image.set_width(6.18)
                panels.add(image)
            else:
                panels.add(Text("result image missing", font_size=24, color=C_MUTED))
        panels.arrange_in_grid(rows=2, cols=2, buff=(0.0, 0.025)).move_to(UP * 0.24)
        return panels

    def kinematics_intro(self):
        title = Text("Surface-kinematics extension", font_size=41, weight=BOLD)
        subtitle = Text(
            "VWA already gives surface elevation, and the same scaffold can be evaluated for other surface variables",
            font_size=22,
            color=C_MUTED,
        )
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.18)

        variable_row = MathTex(
            r"q_s \in \{",
            r"\eta_s,",
            r"\phi_s,",
            r"u_s,",
            r"w_s",
            r"\}",
            font_size=43,
        )
        variable_row[1].set_color(C_ELEVATION)
        variable_row[2].set_color(C_BOUND)
        variable_row[3].set_color(C_US)
        variable_row[4].set_color(C_WS)
        variable_note = Text("same compact VWA logic; choose a different free-surface output", font_size=20, color=C_MUTED)
        variable_group = VGroup(variable_row, variable_note).arrange(DOWN, buff=0.07).move_to(UP * 1.48)
        variable_box = semantic_badge(
            variable_group.get_center(),
            variable_group.width + 0.64,
            variable_group.height + 0.28,
            C_KIN,
            fill_opacity=0.05,
            stroke_opacity=0.70,
        )

        scaffold = VGroup(
            Text("same VWA map", font_size=25, color=C_KIN, weight=BOLD),
            MathTex(
                r"q_s^{\rm VWA}",
                r"=",
                r"q_s^{(1)}",
                r"+",
                r"q_s^{(2)}",
                r"+",
                r"q_s^{(3)}",
                r"+ \cdots",
                font_size=32,
            ),
            Text("linear term plus bound-wave corrections", font_size=18, color=C_MUTED),
        ).arrange(DOWN, buff=0.10)
        scaffold[1][2].set_color(C_LINEAR)
        scaffold[1][4].set_color(C_BOUND)
        scaffold[1][6].set_color(C_BOUND)
        scaffold_box = semantic_badge(
            scaffold.get_center(),
            5.10,
            1.42,
            C_KIN,
            fill_opacity=0.05,
            stroke_opacity=0.64,
        )
        scaffold_panel = VGroup(scaffold_box, scaffold).move_to(LEFT * 3.18 + DOWN * 0.68)

        definitions = VGroup(
            Text("surface outputs", font_size=24, color=C_KIN, weight=BOLD),
            MathTex(r"\eta_s:\ \text{surface elevation}", font_size=24),
            MathTex(r"\phi_s:\ \text{surface velocity potential}", font_size=24),
            MathTex(r"u_s=\partial_x\phi\mid_{z=\eta_s}", font_size=25, color=C_US),
            MathTex(r"w_s=\partial_z\phi\mid_{z=\eta_s}", font_size=25, color=C_WS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        definitions[1].set_color(C_ELEVATION)
        definitions[2].set_color(C_BOUND)
        definitions_box = semantic_badge(
            definitions.get_center(),
            5.82,
            2.38,
            C_WS,
            fill_opacity=0.05,
            stroke_opacity=0.62,
        )
        definitions_panel = VGroup(definitions_box, definitions).move_to(RIGHT * 3.02 + DOWN * 0.66)

        takeaway = Text(
            "The bound-wave approximation stays the same; only the chosen surface variable changes.",
            font_size=23,
            color=C_KIN,
        )
        takeaway.scale_to_fit_width(11.35).to_edge(DOWN, buff=0.96)
        return VGroup(header, variable_box, variable_group, scaffold_panel, definitions_panel, takeaway)

    def kinematics_result(self):
        title = Text("Surface-kinematics result", font_size=39, weight=BOLD)
        subtitle = Text(
            "the same benchmark now checks elevation, potential, and both surface-velocity components",
            font_size=22,
            color=C_MUTED,
        )
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.18)

        if KINEMATICS_RESULT_IMAGE.exists():
            image = ImageMobject(str(KINEMATICS_RESULT_IMAGE))
            image.set_width(12.85)
            if image.height > 5.55:
                image.set_height(5.55)
            image.next_to(header, DOWN, buff=0.08)
        else:
            image = Text("kinematics result image missing", font_size=28, color=C_MUTED).move_to(ORIGIN)

        takeaway = Text(
            "OW3D and VWA remain closely aligned across eta_s, phi_s, u_s, and w_s.",
            font_size=23,
            color=C_KIN,
        )
        takeaway.scale_to_fit_width(11.4).to_edge(DOWN, buff=1.02)
        return Group(header, image, takeaway)

    def time_series_intro(self):
        title = Text("Time-series extension", font_size=42, weight=BOLD)
        subtitle = Text("the same bound-wave map can be evaluated on a temporal record", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.20)

        spatial = VGroup(
            Text("spatial group", font_size=25, color=C_LINEAR, weight=BOLD),
            MathTex(r"\eta^{(11)}(x)=\sum_m a_m\cos(k_mx+\theta_m)", font_size=31, color=C_LINEAR),
            MathTex(r"\eta^{(n)}:\quad G_n(k_1,\ldots,k_n)", font_size=31, color=C_BOUND),
        ).arrange(DOWN, buff=0.13)
        spatial_box = SurroundingRectangle(spatial, color=C_LINEAR, buff=0.20, corner_radius=0.08)
        spatial_box.set_fill(BLACK, opacity=0.08)
        spatial_panel = VGroup(spatial_box, spatial).move_to(LEFT * 3.15 + UP * 0.34)

        temporal = VGroup(
            Text("time record", font_size=25, color=C_TIME, weight=BOLD),
            MathTex(r"\eta^{(11)}(t)=\sum_m a_m\cos(\omega_mt+\theta_m)", font_size=31, color=C_TIME),
            MathTex(r"\eta^{(n)}:\quad G_n(\omega_1,\ldots,\omega_n)", font_size=31, color=C_BOUND),
        ).arrange(DOWN, buff=0.13)
        temporal_box = SurroundingRectangle(temporal, color=C_TIME, buff=0.20, corner_radius=0.08)
        temporal_box.set_fill(BLACK, opacity=0.08)
        temporal_panel = VGroup(temporal_box, temporal).move_to(RIGHT * 3.15 + UP * 0.34)

        arrow = Arrow(
            spatial_panel.get_right() + RIGHT * 0.15,
            temporal_panel.get_left() + LEFT * 0.15,
            buff=0.05,
            color=C_TIME,
            stroke_width=5.5,
            max_tip_length_to_length_ratio=0.16,
        )
        swap = VGroup(
            MathTex(r"k", font_size=46, color=C_LINEAR),
            Arrow(LEFT * 0.34, RIGHT * 0.34, buff=0, color=C_TIME, stroke_width=4.5, max_tip_length_to_length_ratio=0.25),
            MathTex(r"\omega", font_size=46, color=C_TIME),
        ).arrange(RIGHT, buff=0.12).move_to(DOWN * 1.20)

        note = Text("replace the wavenumber argument by the frequency argument in the same compact construction", font_size=23, color=C_MUTED)
        note.scale_to_fit_width(11.2).to_edge(DOWN, buff=1.08)
        return VGroup(title, subtitle, spatial_panel, temporal_panel, arrow, swap, note)

    def time_series_result(self, image_path):
        title = Text("Time-series reconstruction result", font_size=40, weight=BOLD)
        subtitle = Text("linear temporal traces are mapped to nonlinear bound-wave records", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.20)

        if image_path.exists():
            image = ImageMobject(str(image_path))
            image.set_height(5.35)
            image.next_to(subtitle, DOWN, buff=0.08)
        else:
            image = Text("time-series result image missing", font_size=28, color=C_MUTED).move_to(ORIGIN)

        return Group(title, subtitle, image)

    def inverse_vwa_intro(self):
        title = Text("Inverse VWA", font_size=44, weight=BOLD)
        subtitle = Text("recover the underlying linear harmonic from one nonlinear free-surface snapshot", font_size=23, color=C_MUTED)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.20)

        forward = VGroup(
            Text("forward VWA", font_size=25, color=C_LINEAR, weight=BOLD),
            MathTex(r"\eta^{(11)}", r"\longrightarrow", r"\eta", font_size=40),
            Text("linear to nonlinear", font_size=19, color=C_MUTED),
        ).arrange(DOWN, buff=0.12)
        forward[1][0].set_color(C_LINEAR)
        forward[1][2].set_color(C_ELEVATION)
        forward_box = semantic_badge(forward.get_center(), 4.95, 1.85, C_LINEAR, fill_opacity=0.045, stroke_opacity=0.66)
        forward_panel = VGroup(forward_box, forward).move_to(LEFT * 3.10 + UP * 0.36)

        inverse = VGroup(
            Text("inverse VWA", font_size=25, color=C_INVERSE, weight=BOLD),
            MathTex(r"\eta", r"\longrightarrow", r"\widehat{\eta}^{(11)}", font_size=40),
            Text("nonlinear back to linear", font_size=19, color=C_MUTED),
        ).arrange(DOWN, buff=0.12)
        inverse[1][0].set_color(C_ELEVATION)
        inverse[1][2].set_color(C_INVERSE)
        inverse_box = semantic_badge(inverse.get_center(), 5.45, 1.85, C_INVERSE, fill_opacity=0.045, stroke_opacity=0.70)
        inverse_panel = VGroup(inverse_box, inverse).move_to(RIGHT * 3.02 + UP * 0.36)

        input_block = VGroup(
            Text("input", font_size=23, color=C_ELEVATION, weight=BOLD),
            MathTex(r"\eta_{\rm measured}(x)", font_size=34, color=C_ELEVATION),
        ).arrange(DOWN, buff=0.08)
        reference_block = VGroup(
            Text("validation reference", font_size=22, color=C_LINEAR, weight=BOLD),
            MathTex(r"\eta^{(11)}_{\rm four\mbox{-}phase}(x)", font_size=34, color=C_LINEAR),
        ).arrange(DOWN, buff=0.08)
        arrow = Arrow(input_block.get_right() + RIGHT * 0.16, reference_block.get_left() + LEFT * 0.16, buff=0.10, color=C_INVERSE, stroke_width=5.0)
        validation = VGroup(input_block, arrow, reference_block).arrange(RIGHT, buff=0.52).move_to(DOWN * 1.35)

        takeaway = Text(
            "The extension reverses the usual VWA direction: from nonlinear measurement back to the linear component.",
            font_size=24,
            color=C_INVERSE,
        )
        takeaway.scale_to_fit_width(11.5).to_edge(DOWN, buff=0.96)
        return VGroup(header, forward_panel, inverse_panel, validation, takeaway)

    def inverse_vwa_data(self):
        if hasattr(self, "_inverse_vwa_cache"):
            return self._inverse_vwa_cache

        if not (INVERSE_WAVEFORMS_CSV.exists() and INVERSE_SPECTRA_CSV.exists() and INVERSE_RESIDUAL_CSV.exists()):
            self._inverse_vwa_cache = None
            return None

        wave = np.genfromtxt(str(INVERSE_WAVEFORMS_CSV), delimiter=",", names=True)
        spectra = np.genfromtxt(str(INVERSE_SPECTRA_CSV), delimiter=",", names=True)
        residual = np.genfromtxt(str(INVERSE_RESIDUAL_CSV), delimiter=",", names=True)

        focus_center = float(wave["x_over_lambda"][np.nanargmax(np.abs(wave["eta_nonlinear"]))])
        x_relative = wave["x_over_lambda"] - focus_center
        wave_mask = (x_relative >= -4.0) & (x_relative <= 4.0)
        wave_index = np.where(wave_mask)[0]
        wave_index = wave_index[np.linspace(0, len(wave_index) - 1, min(360, len(wave_index))).astype(int)]

        spec_mask = (spectra["k_over_kp"] >= 0.0) & (spectra["k_over_kp"] <= 8.0)
        spec_index = np.where(spec_mask)[0]
        spec_index = spec_index[np.linspace(0, len(spec_index) - 1, min(520, len(spec_index))).astype(int)]

        wave_iter_cols = [f"iteration_{i:03d}" for i in range(61)]
        spec_iter_cols = [f"amp_eta_est_iteration_{i:03d}" for i in range(61)]
        wave_iterations = [wave[name][wave_index] for name in wave_iter_cols]

        floor = 1e-10
        log_amp = lambda values: np.log10(np.maximum(np.asarray(values), floor))
        spec_iterations = [log_amp(spectra[name][spec_index]) for name in spec_iter_cols]

        y_candidates = [wave["eta_nonlinear"][wave_index], wave["eta11_four_phase"][wave_index], *wave_iterations[::10], wave_iterations[-1]]
        wave_abs = max(float(np.nanmax(np.abs(values))) for values in y_candidates)
        wave_ylim = max(0.25, wave_abs * 1.18)

        self._inverse_vwa_cache = {
            "x": x_relative[wave_index],
            "eta_nonlinear": wave["eta_nonlinear"][wave_index],
            "eta11_reference": wave["eta11_four_phase"][wave_index],
            "wave_iterations": wave_iterations,
            "k": spectra["k_over_kp"][spec_index],
            "spec_nonlinear": log_amp(spectra["amp_eta_nonlinear"][spec_index]),
            "spec_eta11": log_amp(spectra["amp_eta11_four_phase"][spec_index]),
            "spec_eta22": log_amp(spectra["amp_eta22_four_phase"][spec_index]),
            "spec_eta33": log_amp(spectra["amp_eta33_four_phase"][spec_index]),
            "spec_iterations": spec_iterations,
            "residual": np.asarray(residual["relative_residual"]),
            "wave_ylim": wave_ylim,
        }
        return self._inverse_vwa_cache

    def inverse_curve(self, axes, x_values, y_values, color, stroke_width=3.0, opacity=1.0):
        curve = VMobject()
        points = [axes.c2p(float(x), float(y)) for x, y in zip(x_values, y_values)]
        curve.set_points_as_corners(points)
        curve.set_stroke(color=color, width=stroke_width, opacity=opacity)
        curve.set_fill(color=color, opacity=0)
        return curve

    def inverse_vwa_iteration_demo(self):
        data = self.inverse_vwa_data()
        if data is None:
            missing = Text("inverse VWA data missing", font_size=34, color=C_INVERSE)
            return missing.move_to(ORIGIN), ValueTracker(0)

        title = Text("Inverse VWA iteration", font_size=39, weight=BOLD)
        subtitle = Text("only the red estimate moves; the nonlinear measurement and four-phase reference stay fixed", font_size=22, color=C_MUTED)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.06).to_edge(UP, buff=0.18)

        wave_axes = Axes(
            x_range=[-4, 4, 2],
            y_range=[-data["wave_ylim"], data["wave_ylim"], data["wave_ylim"]],
            x_length=9.85,
            y_length=2.05,
            tips=False,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
        ).move_to(UP * 1.18 + LEFT * 0.25)
        spec_axes = Axes(
            x_range=[0, 8, 2],
            y_range=[-9.5, -1.2, 2],
            x_length=9.85,
            y_length=2.05,
            tips=False,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
        ).move_to(DOWN * 1.32 + LEFT * 0.25)

        wave_labels = VGroup(
            MathTex(r"x/\lambda", font_size=22, color=C_MUTED).next_to(wave_axes.x_axis, RIGHT, buff=0.08),
            MathTex(r"\eta", font_size=22, color=C_MUTED).next_to(wave_axes.y_axis, UP, buff=0.06),
            Text("waveform", font_size=22, color=WHITE).next_to(wave_axes, UP, buff=0.05).align_to(wave_axes, LEFT),
        )
        spec_labels = VGroup(
            MathTex(r"k/k_p", font_size=22, color=C_MUTED).next_to(spec_axes.x_axis, RIGHT, buff=0.08),
            MathTex(r"\log_{10}|A|", font_size=22, color=C_MUTED).next_to(spec_axes.y_axis, UP, buff=0.06),
            Text("spectrum", font_size=22, color=WHITE).next_to(spec_axes, UP, buff=0.05).align_to(spec_axes, LEFT),
        )

        wave_static = VGroup(
            self.inverse_curve(wave_axes, data["x"], data["eta_nonlinear"], GREY_B, stroke_width=3.1, opacity=0.70),
            self.inverse_curve(wave_axes, data["x"], data["eta11_reference"], C_LINEAR, stroke_width=3.0, opacity=0.95),
        )
        spec_static = VGroup(
            self.inverse_curve(spec_axes, data["k"], data["spec_nonlinear"], GREY_B, stroke_width=2.6, opacity=0.50),
            self.inverse_curve(spec_axes, data["k"], data["spec_eta22"], YELLOW_E, stroke_width=1.8, opacity=0.48),
            self.inverse_curve(spec_axes, data["k"], data["spec_eta33"], TEAL_E, stroke_width=1.8, opacity=0.40),
            self.inverse_curve(spec_axes, data["k"], data["spec_eta11"], C_LINEAR, stroke_width=3.0, opacity=0.95),
        )

        iteration = ValueTracker(0)
        wave_estimates = [self.inverse_curve(wave_axes, data["x"], values, RED_C, stroke_width=3.2) for values in data["wave_iterations"]]
        spec_estimates = [self.inverse_curve(spec_axes, data["k"], values, RED_C, stroke_width=3.1) for values in data["spec_iterations"]]
        dynamic_wave = wave_estimates[0].copy()
        dynamic_spec = spec_estimates[0].copy()

        dynamic_wave.add_updater(lambda mob: mob.become(wave_estimates[int(np.clip(round(iteration.get_value()), 0, 60))]))
        dynamic_spec.add_updater(lambda mob: mob.become(spec_estimates[int(np.clip(round(iteration.get_value()), 0, 60))]))

        iteration_number = DecimalNumber(0, num_decimal_places=0, font_size=22, color=C_INVERSE)
        iteration_number.add_updater(lambda mob: mob.set_value(int(np.clip(round(iteration.get_value()), 0, 60))))
        residual_value = DecimalNumber(data["residual"][0], num_decimal_places=4, font_size=22, color=C_INVERSE)
        residual_value.add_updater(
            lambda mob: mob.set_value(data["residual"][max(0, min(59, int(np.clip(round(iteration.get_value()), 0, 60)) - 1))])
        )
        status = VGroup(
            VGroup(Text("iteration", font_size=18, color=C_MUTED), iteration_number).arrange(RIGHT, buff=0.16),
            VGroup(Text("residual", font_size=18, color=C_MUTED), residual_value).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        status_box = semantic_badge(RIGHT * 5.55 + UP * 1.40, 2.35, 1.52, C_INVERSE, fill_opacity=0.05, stroke_opacity=0.72)
        status.move_to(status_box.get_center())

        legend_items = [
            ("nonlinear input", GREY_B),
            ("four-phase reference", C_LINEAR),
            ("inverse estimate", RED_C),
            ("2nd harmonic", YELLOW_E),
            ("3rd harmonic", TEAL_E),
        ]
        legend = VGroup()
        for label, color in legend_items:
            line = Line(LEFT * 0.20, RIGHT * 0.20, color=color, stroke_width=3.2)
            text = Text(label, font_size=16, color=color)
            legend.add(VGroup(line, text).arrange(RIGHT, buff=0.08))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(RIGHT * 5.52 + DOWN * 1.02)

        final_note = Text(
            "inverse VWA recovers the linear component from a nonlinear surface measurement",
            font_size=21,
            color=C_INVERSE,
        )
        final_note.scale_to_fit_width(11.3).to_edge(DOWN, buff=0.92)

        demo = VGroup(
            header,
            wave_axes,
            spec_axes,
            wave_labels,
            spec_labels,
            wave_static,
            spec_static,
            dynamic_wave,
            dynamic_spec,
            status_box,
            status,
            legend,
            final_note,
        )
        return demo, iteration

    def kinematics_visual(self, center, phase):
        group = VGroup()
        ax_center = center + UP * 0.08
        group.add(axes_at(ax_center, width=2.42, height=1.22, x_label="x", y_label="z", font_size=18))
        curve = wave_group_curve(ax_center, 2.38, 8.9, 0.31, phase, C_ELEVATION, stroke_width=3.8, envelope=1.30)
        group.add(curve)

        for x0 in [-0.58, 0.58]:
            envelope = np.exp(-1.30 * x0 * x0)
            theta = 8.9 * x0 + phase
            y0 = 0.31 * envelope * np.sin(theta)
            pos = ax_center + RIGHT * x0 + UP * y0
            origin = pos + UP * 0.15
            u_vec = RIGHT * (0.58 * envelope * np.cos(theta))
            w_vec = UP * (0.52 * envelope * np.sin(theta))
            group.add(Dot(pos, radius=0.040, color=WHITE))
            group.add(Dot(origin, radius=0.034, color=WHITE))
            group.add(component_arrow(origin, u_vec, C_US))
            group.add(component_arrow(origin, w_vec, C_WS))

        formula = MathTex(r"u_s,", r"\ w_s", font_size=33).move_to(center + DOWN * 0.98)
        formula[0].set_color(C_US)
        formula[1].set_color(C_WS)
        group.add(formula)
        return group

    def time_series_visual(self, center, phase):
        group = VGroup()
        linear_center = center + UP * 0.54
        nonlinear_center = center + DOWN * 0.30
        group.add(axes_at(linear_center, width=2.84, height=0.66, x_label="t", y_label="", font_size=14))
        group.add(axes_at(nonlinear_center, width=2.84, height=0.66, x_label="t", y_label="", font_size=14))
        fixed_phase = 0.35
        linear = wave_group_curve(linear_center, 2.80, 10.0, 0.17, fixed_phase, C_LINEAR, stroke_width=3.3, envelope=1.30)
        nonlinear = FunctionGraph(
            lambda x: 0.18 * np.exp(-1.38 * x * x) * np.sin(10.0 * x + fixed_phase)
            + 0.060 * np.exp(-1.58 * x * x) * np.sin(20.0 * x + 2 * fixed_phase + 0.45),
            x_range=[-1.40, 1.40],
            color=C_ELEVATION,
            stroke_width=3.3,
        ).move_to(nonlinear_center)
        cursor_x = -1.34 + (phase % TAU) / TAU * 2.68
        y_lin = 0.18 * np.exp(-1.38 * cursor_x * cursor_x) * np.sin(10.0 * cursor_x + fixed_phase)
        y_nl = y_lin + 0.060 * np.exp(-1.58 * cursor_x * cursor_x) * np.sin(20.0 * cursor_x + 2 * fixed_phase + 0.45)
        probe = VGroup(
            Line(linear_center + RIGHT * cursor_x + DOWN * 0.39, linear_center + RIGHT * cursor_x + UP * 0.39, color=WHITE, stroke_width=2.2),
            Dot(linear_center + RIGHT * cursor_x + UP * y_lin, radius=0.040, color=WHITE),
        )
        transfer = DashedLine(
            linear_center + RIGHT * cursor_x + UP * y_lin,
            nonlinear_center + RIGHT * cursor_x + UP * y_nl,
            color=C_TIME,
            stroke_width=1.8,
            dash_length=0.05,
        ).set_opacity(0.72)
        arrow = Arrow(linear_center + DOWN * 0.24, nonlinear_center + UP * 0.24, buff=0.05, color=C_TIME, stroke_width=2.2)
        cursor_lin = DashedLine(linear_center + RIGHT * cursor_x + DOWN * 0.33, linear_center + RIGHT * cursor_x + UP * y_lin, color=WHITE, stroke_width=1.7, dash_length=0.04)
        cursor_nl = DashedLine(nonlinear_center + RIGHT * cursor_x + DOWN * 0.33, nonlinear_center + RIGHT * cursor_x + UP * y_nl, color=WHITE, stroke_width=1.7, dash_length=0.04)
        labels = VGroup(
            Text("linear input", font_size=15, color=C_LINEAR).move_to(linear_center + LEFT * 0.56 + UP * 0.35),
            Text("nonlinear output", font_size=14, color=C_ELEVATION).move_to(nonlinear_center + LEFT * 0.42 + UP * 0.35),
        )
        relation = VGroup(
            Text("linear", font_size=13, color=C_LINEAR, weight=BOLD),
            Arrow(LEFT * 0.20, RIGHT * 0.20, buff=0, color=C_TIME, stroke_width=2.4, max_tip_length_to_length_ratio=0.28),
            Text("nonlinear", font_size=13, color=C_ELEVATION, weight=BOLD),
        ).arrange(RIGHT, buff=0.055)
        note = Text("+ bound harmonics", font_size=10, color=C_MUTED)
        relation_group = VGroup(relation, note).arrange(DOWN, buff=0.025).move_to(center + DOWN * 1.23)
        relation_badge = semantic_badge(relation_group.get_center(), 1.90, 0.48, C_TIME)
        group.add(
            linear,
            nonlinear,
            arrow,
            probe,
            transfer,
            cursor_lin,
            cursor_nl,
            Dot(linear_center + RIGHT * cursor_x + UP * y_lin, radius=0.030, color=WHITE),
            Dot(nonlinear_center + RIGHT * cursor_x + UP * y_nl, radius=0.030, color=WHITE),
            labels,
            relation_badge,
            relation_group,
        )
        return group

    def inverse_creamer_visual(self, center, phase):
        group = VGroup()
        nonlinear_center = center + UP * 0.54
        linear_center = center + DOWN * 0.31
        group.add(axes_at(nonlinear_center, width=2.84, height=0.66, x_label="x", y_label="", font_size=14))
        group.add(axes_at(linear_center, width=2.84, height=0.66, x_label="x", y_label="", font_size=14))

        fixed_phase = 0.25
        nonlinear = FunctionGraph(
            lambda x: 0.18 * np.exp(-1.38 * x * x) * np.sin(10.0 * x + fixed_phase)
            + 0.060 * np.exp(-1.58 * x * x) * np.sin(20.0 * x + 2 * fixed_phase + 0.3),
            x_range=[-1.40, 1.40],
            color=C_ELEVATION,
            stroke_width=3.8,
        ).move_to(nonlinear_center)
        linear = wave_group_curve(linear_center, 2.80, 10.0, 0.17, fixed_phase, C_LINEAR, stroke_width=3.8, envelope=1.30)
        arrow = Arrow(nonlinear_center + DOWN * 0.24, linear_center + UP * 0.24, buff=0.05, color=C_INVERSE, stroke_width=3.0, max_tip_length_to_length_ratio=0.24)
        labels = VGroup(
            Text("nonlinear input", font_size=14, color=C_ELEVATION).move_to(nonlinear_center + LEFT * 0.46 + UP * 0.35),
            Text("linear modes", font_size=14, color=C_LINEAR).move_to(linear_center + LEFT * 0.56 + UP * 0.35),
        )
        relation = VGroup(
            Text("nonlinear", font_size=13, color=C_ELEVATION, weight=BOLD),
            Arrow(LEFT * 0.20, RIGHT * 0.20, buff=0, color=C_INVERSE, stroke_width=2.4, max_tip_length_to_length_ratio=0.28),
            Text("linear", font_size=13, color=C_LINEAR, weight=BOLD),
        ).arrange(RIGHT, buff=0.055)
        note = Text("recover modes", font_size=10, color=C_MUTED)
        relation_group = VGroup(relation, note).arrange(DOWN, buff=0.025).move_to(center + DOWN * 1.23)
        relation_badge = semantic_badge(relation_group.get_center(), 1.90, 0.48, C_INVERSE, fill_opacity=0.06, stroke_opacity=0.65)
        group.add(nonlinear, linear, arrow, labels, relation_badge, relation_group)
        return group
