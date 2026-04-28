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


class WhyExactInteractionsAreExpensive(Scene):
    def construct(self):
        title = Text("How expensive is exact interaction theory?", font_size=35, weight=BOLD)
        subtitle = Text("bound harmonics require interactions between spectral components", font_size=23, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav_progress.add_updater(
            lambda tracker, dt: tracker.increment_value(len(SCENARIO2_SUBSCENARIOS) * dt / SCENARIO2_SECONDS)
        )
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
        self.wait(1.6)

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
        self.wait(1.8)
        self.play(ReplacementTransform(VGroup(pair_intro_box, pair_intro), pair_eq))
        self.wait(1.6)

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

        pair_idx = 0
        slow_pair_count = 7
        for i in range(len(ks)):
            left_indicator = stems[i].copy().set_color(C_PAIR).set_z_index(5)
            left_indicator.set_stroke(width=4.2)
            right_indicator = stems[i].copy().set_color(C_PAIR).set_z_index(6)
            right_indicator.set_stroke(width=4.0)
            self.add(left_indicator, right_indicator)

            for j in range(i, len(ks)):
                animations = []
                for bin_idx, delta in enumerate(pair_vectors[(i, j)]):
                    if delta < 0.002:
                        continue
                    bin_levels[bin_idx] = min(0.98, bin_levels[bin_idx] + float(delta))
                    animations.append(bin_trackers[bin_idx].animate.set_value(bin_levels[bin_idx]))

                if animations:
                    target_indicator = stems[j].copy().set_color(C_PAIR).set_z_index(6)
                    target_indicator.set_stroke(width=4.0)
                    run_time = max(0.12, 0.28 - 0.02 * pair_idx) if pair_idx < slow_pair_count else 0.026
                    self.play(
                        Indicate(stems[i], color=C_PAIR, scale_factor=1.006, run_time=run_time),
                        Transform(right_indicator, target_indicator),
                        Indicate(stems[j], color=C_PAIR, scale_factor=1.008, run_time=run_time),
                        *animations,
                        run_time=run_time,
                    )
                pair_idx += 1
            self.remove(left_indicator, right_indicator)

        self.play(FadeOut(pair_note_box), FadeOut(pair_note))
        sum_box = SurroundingRectangle(ax_sum, color=C_PAIR, buff=0.10, corner_radius=0.07)
        full_sum = VGroup(
            Text("exact second-order theory", font_size=22, color=C_PAIR),
            Text("built from all spectral component pairs", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.08).next_to(ax_sum, DOWN, buff=0.30)
        self.play(Create(sum_box), quiet_fade(full_sum))
        self.wait(2.0)

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
        self.wait(2.6)

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
        self.wait(5.2)
        nav_progress.clear_updaters()
