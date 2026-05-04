"""
Scenario 2 - Why Exact Interactions Become Expensive
====================================================

Polished version of the original interaction-accumulation scene:
many linear components feed a second-order spectrum through pairwise
sum-frequency interactions, then the cost scaling motivates VWA.
"""

from manim import *
import numpy as np
from presentation_nav import bottom_progress_nav, keep_nav

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene

g = 9.81
K_PEAK = 2.9
GAMMA_JS = 3.3

C_LINEAR = BLUE
C_PAIR = ORANGE
C_TRIAD = PURPLE
C_VWA = YELLOW
C_MUTED = GREY_B
C_PANEL = GREY_D
SCENARIO2_SECONDS = 39.58
SCENARIO2_SUBSCENARIOS = [
    "input spectrum",
    "pair formula",
    "pair accumulation",
    "cost scaling",
    "measured bottleneck",
    "directional explosion",
    "VWA question",
]


def jonswap_raw(k, k_p):
    if k <= 1e-6:
        return 0.0
    omega = np.sqrt(g * k)
    omega_p = np.sqrt(g * k_p)
    sigma = 0.07 if omega <= omega_p else 0.09
    base = omega ** (-5) * np.exp(-1.25 * (omega_p / omega) ** 4)
    peak = GAMMA_JS ** np.exp(-0.5 * ((omega - omega_p) / (sigma * omega_p)) ** 2)
    return float(base * np.sqrt(g / k) / 2.0 * peak)


def make_stem(ax, x, y, color=C_LINEAR, width=2.7):
    return VGroup(
        Line(ax.c2p(x, 0), ax.c2p(x, y), color=color, stroke_width=width),
        Dot(ax.c2p(x, y), radius=0.045, color=color),
    )


def panel_box(mob, color=C_PANEL, opacity=0.08, buff=0.16):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08).set_fill(BLACK, opacity=opacity)


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


class S2ExactInteractionsSlides(Slide):
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
        title = Text("How expensive is exact interaction theory?", font_size=35, weight=BOLD)
        subtitle = Text("bound harmonics require interactions between spectral components", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav = bottom_progress_nav(
            2,
            6,
            "exact interactions",
            SCENARIO2_SUBSCENARIOS,
            nav_progress,
            accent=C_PAIR,
        )
        self.add(nav_progress, nav)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)
        self.slide_pause(nav_progress, 0.45)

        ax_lin = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.15, 0.4],
            x_length=6.15,
            y_length=2.40,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(LEFT, buff=0.66).shift(UP * 0.82)
        ax_sum = Axes(
            x_range=[0, 11, 2],
            y_range=[0, 1.15, 0.4],
            x_length=5.25,
            y_length=2.40,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.54).shift(UP * 0.82)

        head_lin = Text("linear spectrum", font_size=24, color=C_MUTED).next_to(ax_lin, UP, buff=0.17)
        head_sum = Text("second-order spectrum", font_size=24, color=C_MUTED).next_to(ax_sum, UP, buff=0.17)
        lab_lin = ax_lin.get_x_axis_label(MathTex("k", font_size=25))
        lab_sum = ax_sum.get_x_axis_label(MathTex("k", font_size=25))
        lab_lin_y = ax_lin.get_y_axis_label(MathTex(r"|\hat\eta^{(11)}|", font_size=23))
        lab_sum_y = ax_sum.get_y_axis_label(MathTex(r"|\hat\eta^{(22)}|", font_size=23))

        ks = np.linspace(1.35, 5.05, 22)
        norm = max(jonswap_raw(k, K_PEAK) for k in np.linspace(0.8, 5.5, 1200))
        amps = np.array([jonswap_raw(k, K_PEAK) / norm for k in ks])
        amps = amps / amps.max()
        stems = VGroup(*[make_stem(ax_lin, k, a) for k, a in zip(ks, amps)])
        band = ax_lin.plot(
            lambda k: jonswap_raw(k, K_PEAK) / norm,
            x_range=[1.0, 5.25, 0.03],
            color=BLUE_A,
            stroke_width=1.8,
            stroke_opacity=0.42,
        )
        k_labels = VGroup(
            MathTex("k_1", font_size=19, color=C_LINEAR).next_to(ax_lin.c2p(ks[0], 0), DOWN, buff=0.08),
            MathTex("k_m", font_size=19, color=C_LINEAR).next_to(ax_lin.c2p(ks[10], 0), DOWN, buff=0.08),
            MathTex("k_{N_c}", font_size=19, color=C_LINEAR).next_to(ax_lin.c2p(ks[-1], 0), DOWN, buff=0.08),
        )

        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_lin), quiet_fade(head_lin), quiet_fade(lab_lin), quiet_fade(lab_lin_y)),
                AnimationGroup(Create(ax_sum), quiet_fade(head_sum), quiet_fade(lab_sum), quiet_fade(lab_sum_y)),
                lag_ratio=0.22,
            )
        )
        self.play(Create(band), LaggedStart(*[Create(s) for s in stems], lag_ratio=0.035), quiet_fade(k_labels))

        linear_eq = MathTex(
            r"\eta^{(11)}=\sum_{m=1}^{N_c}a_m\cos\theta_m",
            font_size=30,
            color=C_LINEAR,
        ).next_to(ax_lin, DOWN, buff=0.92)
        self.play(quiet_fade(linear_eq))
        self.slide_pause(nav_progress, 1.0)

        pair_intro = VGroup(
            Text("second order:", font_size=23, color=C_PAIR),
            Text("all component pairs contribute", font_size=23, color=WHITE),
            MathTex(r"(k_m,k_n)\rightarrow k_m+k_n", font_size=30, color=C_PAIR),
        ).arrange(DOWN, buff=0.10).next_to(ax_sum, DOWN, buff=0.28)
        pair_intro.scale_to_fit_width(4.75)
        pair_intro_box = panel_box(pair_intro, color=C_PAIR, opacity=0.10, buff=0.16)
        pair_eq = VGroup(
            MathTex(
                r"\eta^{(22)}_{\rm exact}"
                r"=\sum_{m=1}^{N_c}\sum_{n=1}^{N_c}a_ma_nG(k_m,k_n)",
                font_size=27,
                color=WHITE,
            ),
            MathTex(
                r"\qquad\qquad\qquad\cdot\cos(\theta_m+\theta_n)",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT).next_to(ax_sum, DOWN, buff=1.28)
        pair_eq.scale_to_fit_width(4.80)

        self.play(FadeIn(pair_intro_box), quiet_fade(pair_intro))
        self.slide_pause(nav_progress, 1.75)
        self.play(ReplacementTransform(VGroup(pair_intro_box, pair_intro), pair_eq))
        self.slide_pause(nav_progress, 2.0)

        bin_centers = np.linspace(2.8, 10.0, 29)
        bin_levels = [0.0 for _ in bin_centers]
        bin_trackers = [ValueTracker(0.0) for _ in bin_centers]
        sum_stems = VGroup(*[
            always_redraw(
                lambda x=x, tracker=tracker: make_stem(
                    ax_sum,
                    x,
                    tracker.get_value(),
                    color=C_PAIR,
                    width=2.6,
                )
            )
            for x, tracker in zip(bin_centers, bin_trackers)
        ])
        self.add(sum_stems)

        pair_note = VGroup(
            Text("accumulating pair contributions", font_size=21, color=C_PAIR),
            MathTex(r"\theta_m+\theta_n", font_size=26, color=C_PAIR),
        ).arrange(DOWN, buff=0.08).next_to(ax_sum, DOWN, buff=0.28)
        pair_note_box = panel_box(pair_note, color=C_PAIR, opacity=0.10, buff=0.14)
        self.play(FadeIn(pair_note_box), quiet_fade(pair_note))

        pairs = [(i, j) for i in range(len(ks)) for j in range(i, len(ks))]
        pair_vectors = {}
        raw_vectors = []
        sigma = 0.24
        for i, j in pairs:
            sx = ks[i] + ks[j]
            weights = np.exp(-0.5 * ((bin_centers - sx) / sigma) ** 2)
            weights = weights / max(np.sum(weights), 1e-9)
            vec = amps[i] * amps[j] * weights
            pair_vectors[(i, j)] = vec
            raw_vectors.append(vec)
        scale = 0.96 / max(float(np.max(np.sum(raw_vectors, axis=0))), 1e-9)
        pair_vectors = {key: vec * scale for key, vec in pair_vectors.items()}

        cumulative_levels = [np.zeros(len(bin_centers))]
        levels = np.zeros(len(bin_centers))
        for pair in pairs:
            for bin_idx, delta in enumerate(pair_vectors[pair]):
                if delta >= 0.002:
                    levels[bin_idx] = min(0.98, levels[bin_idx] + float(delta))
            cumulative_levels.append(levels.copy())
        cumulative_levels = np.array(cumulative_levels)

        scan_tracker = ValueTracker(0.0)

        def current_pair():
            pair_index = min(int(scan_tracker.get_value()), len(pairs) - 1)
            return pairs[pair_index]

        def make_pair_indicator(which):
            i, j = current_pair()
            stem = stems[i if which == 0 else j].copy().set_color(C_PAIR).set_z_index(6)
            stem.set_stroke(width=4.2 if which == 0 else 4.0)
            return stem

        left_indicator = always_redraw(lambda: make_pair_indicator(0))
        right_indicator = always_redraw(lambda: make_pair_indicator(1))

        scan_driver = VMobject()

        def update_scan(_mob):
            position = max(0.0, min(scan_tracker.get_value(), float(len(pairs))))
            base = min(int(np.floor(position)), len(pairs) - 1)
            alpha = position - base
            current_levels = (1 - alpha) * cumulative_levels[base] + alpha * cumulative_levels[base + 1]
            for tracker, level in zip(bin_trackers, current_levels):
                tracker.set_value(float(level))

        scan_driver.add_updater(update_scan)
        self.add(scan_driver, left_indicator, right_indicator)
        self.play(scan_tracker.animate.set_value(float(len(pairs))), run_time=13.0, rate_func=linear)
        scan_driver.clear_updaters()
        update_scan(scan_driver)
        self.remove(scan_driver, left_indicator, right_indicator)
        bin_levels = list(cumulative_levels[-1])

        self.play(FadeOut(pair_note_box), FadeOut(pair_note))
        sum_box = SurroundingRectangle(ax_sum, color=C_PAIR, buff=0.10, corner_radius=0.07)
        full_sum = VGroup(
            Text("exact second-order theory", font_size=22, color=C_PAIR),
            Text("built from all spectral component pairs", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.08).next_to(ax_sum, DOWN, buff=0.30)
        self.play(Create(sum_box), quiet_fade(full_sum))
        self.slide_pause(nav_progress, 3.0)

        self.play(FadeOut(linear_eq), FadeOut(pair_eq), FadeOut(sum_box), FadeOut(full_sum))
        scaling = VGroup(
            VGroup(Text("2nd order", font_size=22, color=C_PAIR), MathTex(r"N_c^2", font_size=38, color=C_PAIR), Text("pairs", font_size=19, color=C_MUTED)).arrange(DOWN, buff=0.08),
            VGroup(Text("3rd order", font_size=22, color=C_TRIAD), MathTex(r"N_c^3", font_size=38, color=C_TRIAD), Text("triads", font_size=19, color=C_MUTED)).arrange(DOWN, buff=0.08),
            VGroup(Text("nth order", font_size=22, color=C_VWA), MathTex(r"N_c^n", font_size=38, color=C_VWA), Text("n-tuples", font_size=19, color=C_MUTED)).arrange(DOWN, buff=0.08),
        ).arrange(RIGHT, buff=0.72).move_to([0.0, -1.84, 0])
        scaling_box = panel_box(scaling, GREY_D, opacity=0.10, buff=0.20)
        cost_note = VGroup(
            Text("accurate,", font_size=21, color=C_MUTED),
            Text("but repeated evaluation becomes the bottleneck", font_size=21, color=C_MUTED),
        ).arrange(RIGHT, buff=0.18)
        cost_note.next_to(scaling_box, UP, buff=0.14)
        self.play(FadeIn(scaling_box), quiet_fade(cost_note))
        self.play(quiet_fade(scaling[0]))
        self.play(quiet_fade(scaling[1]))
        self.play(quiet_fade(scaling[2]))
        self.slide_pause(nav_progress, 4.0)

        self.play(*[FadeOut(mob) for mob in keep_nav(self.mobjects, nav)], run_time=0.8)
        self.clear()
        self.add(nav_progress, nav)

        measured_title = Text("The exact summation is already the bottleneck", font_size=34, weight=BOLD)
        measured_sub = Text(
            "MF12 explicit interactions become slow before we add repeated design loops",
            font_size=22,
            color=C_MUTED,
        )
        VGroup(measured_title, measured_sub).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.20)

        table_rows = [
            (r"\alpha", r"N_c", r"\eta^{(22)}", r"\eta^{(33)}"),
            ("1", "126", r"4.1{\times}10^3\!-\!1.1{\times}10^4", r"1.7{\times}10^5\!-\!3.1{\times}10^5"),
            ("8", "66", r"1.4{\times}10^3\!-\!2.8{\times}10^3", r"2.5{\times}10^4\!-\!4.9{\times}10^4"),
        ]
        table = VGroup()
        for r_i, row in enumerate(table_rows):
            row_group = VGroup()
            for c_i, cell in enumerate(row):
                color = WHITE if r_i == 0 else C_PAIR if c_i in (2, 3) else C_MUTED
                tex = MathTex(cell, font_size=24 if r_i == 0 else 22, color=color)
                box = Rectangle(width=[0.85, 0.95, 2.25, 2.25][c_i], height=0.46, stroke_width=0.8, stroke_color=GREY_D)
                box.set_fill(BLACK, opacity=0.18 if r_i == 0 else 0.06)
                cell_group = VGroup(box, tex)
                row_group.add(cell_group)
            row_group.arrange(RIGHT, buff=0.02)
            table.add(row_group)
        table.arrange(DOWN, buff=0.02).move_to([-2.25, 0.40, 0])
        table_caption = Text("speedup relative to the compact evaluation", font_size=20, color=C_MUTED).next_to(table, DOWN, buff=0.18)
        table_panel = panel_box(VGroup(table, table_caption), C_PAIR, opacity=0.08, buff=0.20)

        exact_card = VGroup(
            Text("exact MF12 summation", font_size=24, color=C_PAIR, weight=BOLD),
            MathTex(r"\sum_m\sum_n\quad\hbox{and}\quad\sum_l\sum_m\sum_n", font_size=31, color=C_PAIR),
            Text("the number of retained components sets the cost", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.12)
        exact_card_box = panel_box(exact_card, C_PAIR, opacity=0.09, buff=0.20)
        exact_block = VGroup(exact_card_box, exact_card).move_to([3.35, 0.72, 0])

        vwa_card = VGroup(
            Text("compact evaluation time", font_size=24, color=C_VWA, weight=BOLD),
            MathTex(r"10^{-4}\hbox{--}10^{-3}\ {\rm s}", font_size=32, color=C_VWA),
            Text("shown only as the reference used for speedup", font_size=19, color=C_MUTED),
        ).arrange(DOWN, buff=0.10)
        vwa_card_box = panel_box(vwa_card, C_VWA, opacity=0.08, buff=0.20)
        vwa_block = VGroup(vwa_card_box, vwa_card).move_to([3.35, -0.88, 0])

        caution = Text(
            "High-frequency truncation reduces work, but can also change bound-wave statistics.",
            font_size=20,
            color=C_MUTED,
        ).to_edge(DOWN, buff=0.96)

        self.play(quiet_fade(measured_title), quiet_fade(measured_sub), run_time=0.5)
        self.play(FadeIn(table_panel), quiet_fade(table), quiet_fade(table_caption), quiet_fade(exact_block), quiet_fade(vwa_block), run_time=0.9)
        self.play(quiet_fade(caution), run_time=0.4)
        self.slide_pause(nav_progress, 5.0)

        self.play(*[FadeOut(mob) for mob in keep_nav(self.mobjects, nav)], run_time=0.8)
        self.clear()
        self.add(nav_progress, nav)

        dir_title = Text("Directional groups make the exact cost explode", font_size=34, weight=BOLD)
        dir_sub = Text(r"$512\times512$ grid; exact cost rises with retained directional components", font_size=21, color=C_MUTED)
        VGroup(dir_title, dir_sub).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.20)

        chart_ax = Axes(
            x_range=[-0.5, 2.5, 1],
            y_range=[-2.0, 4.5, 1],
            x_length=7.2,
            y_length=3.2,
            axis_config={"include_tip": False, "stroke_color": GREY_B, "stroke_width": 1.5},
        ).move_to([-1.60, -0.18, 0])
        y_lab = MathTex(r"\log_{10}({\rm time/s})", font_size=24, color=C_MUTED).next_to(chart_ax, LEFT, buff=0.18).rotate(PI / 2)
        sigma_labels = VGroup(
            *[MathTex(fr"{s}^\circ", font_size=22, color=C_MUTED).next_to(chart_ax.c2p(i, -2.0), DOWN, buff=0.10) for i, s in enumerate([0, 15, 30])]
        )
        x_lab = Text("directional spreading", font_size=21, color=C_MUTED).next_to(chart_ax, DOWN, buff=0.46)

        mf12_a1 = [2.36, 4849.47, 17191.63]
        mf12_a8 = [0.65, 594.44, 2130.45]
        vwa = [0.0147, 0.0148, 0.0163]
        bars = VGroup()
        for i in range(3):
            for offset, value, color in [(-0.18, mf12_a1[i], C_PAIR), (0.0, mf12_a8[i], C_TRIAD), (0.18, vwa[i], C_VWA)]:
                y0 = chart_ax.c2p(i + offset, -2.0)
                y1 = chart_ax.c2p(i + offset, np.log10(value))
                bar = Rectangle(width=0.12, height=max(0.03, y1[1] - y0[1]), stroke_width=0, fill_color=color, fill_opacity=0.92)
                bar.move_to([(y0[0] + y1[0]) / 2, (y0[1] + y1[1]) / 2, 0])
                bars.add(bar)

        legend = VGroup(
            VGroup(Square(0.14, fill_color=C_PAIR, fill_opacity=1, stroke_width=0), Text(r"MF12, $\alpha=1$", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.10),
            VGroup(Square(0.14, fill_color=C_TRIAD, fill_opacity=1, stroke_width=0), Text(r"MF12, $\alpha=8$", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.10),
            VGroup(Square(0.14, fill_color=C_VWA, fill_opacity=1, stroke_width=0), Text("compact eval.", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        legend_box = panel_box(legend, GREY_D, opacity=0.20, buff=0.12)
        legend_group = VGroup(legend_box, legend).move_to([3.65, 1.20, 0])

        nc_table = VGroup(
            Text("retained components", font_size=22, color=WHITE, weight=BOLD),
            MathTex(r"\sigma=0^\circ:\quad N_c=39,\ 20", font_size=23, color=C_MUTED),
            MathTex(r"\sigma=15^\circ:\quad N_c=1776,\ 624", font_size=23, color=C_MUTED),
            MathTex(r"\sigma=30^\circ:\quad N_c=3337,\ 1176", font_size=23, color=C_MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        nc_panel = panel_box(nc_table, C_PANEL, opacity=0.10, buff=0.18)
        nc_group = VGroup(nc_panel, nc_table).move_to([3.55, -0.75, 0])

        dir_takeaway = Text("MF12 grows from seconds to hours as directional components are retained.", font_size=22, color=C_PAIR)
        dir_takeaway.to_edge(DOWN, buff=0.95)

        self.play(quiet_fade(dir_title), quiet_fade(dir_sub), run_time=0.5)
        self.play(Create(chart_ax), FadeIn(y_lab), FadeIn(sigma_labels), FadeIn(x_lab), FadeIn(bars), quiet_fade(legend_group), quiet_fade(nc_group), run_time=1.0)
        self.play(quiet_fade(dir_takeaway), run_time=0.4)
        self.slide_pause(nav_progress, 6.0)

        self.play(*[FadeOut(mob) for mob in keep_nav(self.mobjects, nav)], run_time=0.8)
        self.clear()
        self.add(nav_progress, nav)

        bridge = VGroup(
            Text("Can we keep the physics", font_size=34, weight=BOLD, color=WHITE),
            Text("without evaluating every pair?", font_size=34, weight=BOLD, color=WHITE),
            Text("Reduce the interaction kernel.", font_size=26, color=C_VWA),
            Text("Next: Variable Wavenumber Approximation (VWA).", font_size=27, color=C_VWA),
        ).arrange(DOWN, buff=0.20)
        bridge.scale_to_fit_width(10.0)
        bridge.move_to(ORIGIN)

        self.play(quiet_fade(bridge[0]), quiet_fade(bridge[1]), run_time=0.6)
        self.play(quiet_fade(bridge[2]), run_time=0.6)
        self.play(quiet_fade(bridge[3]), run_time=0.6)
        self.slide_pause(nav_progress, 7.0)
