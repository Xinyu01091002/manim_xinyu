"""
Scenario 2 - Why Exact Interactions Become Expensive
====================================================

This scene bridges the physical idea of bound harmonics to the computational
motivation for VWA: component-resolved theory keeps every nonlinear
interaction, but the number of interactions grows combinatorially.
"""

from manim import *
import numpy as np

g = 9.81
CARRIER_K = 2.9
GAMMA_JS = 3.3

C_LINEAR = BLUE
C_PAIR = ORANGE
C_TRIAD = PURPLE
C_VWA = YELLOW
C_MUTED = GREY_B
C_PANEL = GREY_D


def make_stem(ax, x, y, color=C_LINEAR, width=3):
    line = Line(ax.c2p(x, 0), ax.c2p(x, y), color=color, stroke_width=width)
    dot = Dot(ax.c2p(x, y), radius=0.055, color=color)
    return VGroup(line, dot)


def _jonswap_raw(k, k_p):
    if k <= 1e-6:
        return 0.0
    omega = np.sqrt(g * k)
    omega_p = np.sqrt(g * k_p)
    sigma = 0.07 if omega <= omega_p else 0.09
    base = omega ** (-5) * np.exp(-1.25 * (omega_p / omega) ** 4)
    peak = GAMMA_JS ** np.exp(-0.5 * ((omega - omega_p) / (sigma * omega_p)) ** 2)
    return float(base * np.sqrt(g / k) / 2.0 * peak)


class WhyExactInteractionsAreExpensive(Scene):
    def construct(self):
        title = Text("Why wave-interaction theory becomes expensive", font_size=34, weight=BOLD)
        title.to_edge(UP, buff=0.18)
        self.play(Write(title))

        # Left panel: linear spectrum
        ax_lin = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.2, 0.4],
            x_length=6.3,
            y_length=2.45,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(LEFT, buff=0.78).shift(UP * 0.95)
        head_lin = Text("linear spectrum", font_size=26, color=C_MUTED).next_to(ax_lin, UP, buff=0.18)
        lab_lin = ax_lin.get_x_axis_label(MathTex("k", font_size=30))
        lab_lin_y = MathTex(r"|\hat{\eta}^{(11)}|", font_size=26, color=C_MUTED).rotate(90 * DEGREES).next_to(
            ax_lin, LEFT, buff=0.35
        )

        ks = np.linspace(1.35, 5.05, 28)
        base_norm = max(_jonswap_raw(k, CARRIER_K) for k in np.linspace(0.8, 5.4, 1400))
        amps = np.array([_jonswap_raw(k, CARRIER_K) / base_norm for k in ks])
        amps = amps / amps.max()
        stems = VGroup(*[make_stem(ax_lin, k, a) for k, a in zip(ks, amps)])
        lin_band = ax_lin.plot(
            lambda k: _jonswap_raw(k, CARRIER_K) / base_norm,
            x_range=[1.0, 5.2, 0.03],
            color=BLUE_A,
            stroke_width=2.0,
            stroke_opacity=0.45,
        )
        k_labels = VGroup(*[
            MathTex(rf"k_{{{i + 1}}}", font_size=16, color=C_LINEAR).next_to(ax_lin.c2p(k, 0), DOWN, buff=0.08)
            for i, k in enumerate(ks)
            if i in {0, 4, 8, 12, 16, 20, 24, 27}
        ])

        lin_note = Text(
            "A realistic wave group may have many components.",
            font_size=22,
            color=C_MUTED,
        ).next_to(ax_lin, DOWN, buff=0.24).align_to(ax_lin, LEFT)

        # Reserve the second-order spectrum space early.
        ax_sum = Axes(
            x_range=[0, 11, 2],
            y_range=[0, 1.2, 0.4],
            x_length=5.6,
            y_length=2.45,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.44).shift(UP * 0.95)
        head_sum = Text("second-order spectrum", font_size=26, color=C_MUTED).next_to(ax_sum, UP, buff=0.18)
        lab_sum = ax_sum.get_x_axis_label(MathTex("k", font_size=30))
        lab_sum_y = MathTex(r"|\hat{\eta}^{(22)}|", font_size=26, color=C_MUTED).rotate(90 * DEGREES).next_to(
            ax_sum, LEFT, buff=0.35
        )
        sum_panel = RoundedRectangle(
            width=6.15,
            height=3.35,
            corner_radius=0.10,
            stroke_color=C_PANEL,
            stroke_width=1.0,
            fill_color=BLACK,
            fill_opacity=0.08,
        ).move_to(ax_sum.get_center())

        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_lin), Write(head_lin), Write(lab_lin), Write(lab_lin_y)),
                AnimationGroup(FadeIn(sum_panel), Create(ax_sum), Write(head_sum), Write(lab_sum), Write(lab_sum_y)),
                lag_ratio=0.2,
            )
        )
        self.play(Create(lin_band))
        self.play(LaggedStart(*[Create(s) for s in stems], lag_ratio=0.05), Write(k_labels))
        self.play(FadeIn(lin_note, shift=DOWN * 0.10))
        self.wait(0.8)

        lin_eq = MathTex(
            r"\eta^{(11)}(x,t)=\sum_{m=1}^{N_c} a_m\cos\theta_m",
            font_size=32,
            color=C_LINEAR,
        ).next_to(ax_lin, DOWN, buff=1.10)
        pair_eq = VGroup(
            MathTex(
                r"\eta^{(22)}_{\rm exact}"
                r"=\sum_{m=1}^{N_c}\sum_{n=1}^{N_c} a_m a_n\,G_{m+n}(k_m,k_n)",
                font_size=25,
                color=WHITE,
            ),
            MathTex(
                r"\qquad\qquad\qquad\qquad\cdot \cos(\theta_m+\theta_n)",
                font_size=25,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(ax_sum, DOWN, buff=1.04)
        pair_note = Text(
            "Each component pair contributes one sum-frequency term.",
            font_size=22,
            color=C_MUTED,
        ).move_to([0.0, -1.05, 0.0])
        pair_story_box = SurroundingRectangle(
            pair_note,
            color=C_PAIR,
            buff=0.14,
            corner_radius=0.07,
        ).set_fill(BLACK, opacity=0.10)

        self.play(FadeOut(lin_note))
        self.play(FadeIn(lin_eq, shift=UP * 0.08))
        self.play(Write(pair_eq))
        self.play(FadeIn(pair_note, shift=DOWN * 0.08))
        self.play(Create(pair_story_box))
        self.wait(1.2)

        self.play(
            FadeOut(pair_note),
            FadeOut(pair_story_box),
        )

        num_components = len(ks)
        pairs = [(i, j) for i in range(num_components) for j in range(i, num_components)]
        pair_products = [amps[i] * amps[j] for i, j in pairs]
        max_product = max(pair_products)
        bin_centers = np.linspace(2.8, 10.0, 29)
        bin_levels = [0.0 for _ in bin_centers]
        bin_trackers = [ValueTracker(0.0) for _ in bin_centers]
        binned_stems = VGroup(*[
            always_redraw(
                lambda x=x, tracker=tracker: make_stem(
                    ax_sum,
                    x,
                    tracker.get_value(),
                    color=C_PAIR,
                    width=2.8,
                )
            )
            for x, tracker in zip(bin_centers, bin_trackers)
        ])

        pair_weight_note = MathTex(
            r"\text{all pairs build the second-order superharmonic band}",
            font_size=22,
            color=C_PAIR,
        ).next_to(ax_sum, DOWN, buff=0.14)
        self.add(binned_stems)
        self.play(FadeIn(pair_weight_note, shift=UP * 0.06))

        gaussian_sigma = 0.24
        slow_pair_count = 8
        pair_vectors = {}
        pair_vector_list = []
        for i, j in pairs:
            sx = ks[i] + ks[j]
            amp_prod = amps[i] * amps[j]
            weights = np.exp(-0.5 * ((bin_centers - sx) / gaussian_sigma) ** 2)
            weights = weights / max(np.sum(weights), 1e-9)
            vec = amp_prod * weights
            pair_vectors[(i, j)] = vec
            pair_vector_list.append(vec)

        total_second_raw = np.sum(pair_vector_list, axis=0)
        second_scale = 0.96 / max(float(np.max(total_second_raw)), 1e-9)
        pair_vectors = {key: vec * second_scale for key, vec in pair_vectors.items()}

        pair_idx = 0
        for i in range(num_components):
            left_indicator = stems[i].copy().set_color(C_PAIR)
            left_indicator.set_stroke(width=4.5)
            left_indicator.set_z_index(5)
            self.add(left_indicator)
            right_indicator = stems[i].copy().set_color(C_PAIR)
            right_indicator.set_stroke(width=4.0)
            right_indicator.set_z_index(6)
            self.add(right_indicator)

            for j in range(i, num_components):
                pair_vec = pair_vectors[(i, j)]
                animations = []
                for bin_idx, delta in enumerate(pair_vec):
                    if delta < 0.002:
                        continue
                    bin_levels[bin_idx] = min(0.98, bin_levels[bin_idx] + delta)
                    animations.append(bin_trackers[bin_idx].animate.set_value(bin_levels[bin_idx]))

                if pair_idx < slow_pair_count:
                    run_time = max(0.12, 0.26 - 0.018 * pair_idx)
                else:
                    run_time = max(0.022, 0.065 - 0.00005 * (pair_idx - slow_pair_count))

                if animations:
                    target_indicator = stems[j].copy().set_color(C_PAIR)
                    target_indicator.set_stroke(width=4.0)
                    target_indicator.set_z_index(6)
                    self.play(
                        AnimationGroup(
                            Indicate(
                                stems[i],
                                color=C_PAIR,
                                scale_factor=1.004,
                                run_time=run_time * 0.92,
                            ),
                            Transform(right_indicator, target_indicator),
                            lag_ratio=0.0,
                        ),
                        AnimationGroup(
                            Indicate(
                                stems[j],
                                color=C_PAIR,
                                scale_factor=1.010 if pair_idx < slow_pair_count else 1.006,
                                run_time=max(0.02, run_time * 0.42),
                            ),
                            lag_ratio=0.0,
                        ),
                        *animations,
                        run_time=run_time,
                    )
                pair_idx += 1

            self.remove(left_indicator, right_indicator)

        sum_box = SurroundingRectangle(
            VGroup(ax_sum, head_sum, pair_weight_note),
            color=C_PAIR,
            buff=0.12,
            corner_radius=0.08,
        ).set_fill(BLACK, opacity=0.06)
        self.play(Create(sum_box))
        self.wait(1.0)

        # Complexity summary: keep it simple, no component-resolved grid.
        self.play(
            FadeOut(lin_eq),
            FadeOut(pair_eq),
            FadeOut(pair_weight_note),
            FadeOut(sum_box),
            FadeOut(sum_panel),
        )
        self.wait(0.4)

        scaling_group = VGroup(
            VGroup(
                Text("2nd order", font_size=22, color=C_PAIR),
                MathTex(r"N_c^2", font_size=38, color=C_PAIR),
                Text("pairs", font_size=20, color=C_MUTED),
            ).arrange(DOWN, buff=0.10),
            VGroup(
                Text("3rd order", font_size=22, color=C_TRIAD),
                MathTex(r"N_c^3", font_size=38, color=C_TRIAD),
                Text("triads", font_size=20, color=C_MUTED),
            ).arrange(DOWN, buff=0.10),
            VGroup(
                Text("nth order", font_size=22, color=C_VWA),
                MathTex(r"N_c^n", font_size=38, color=C_VWA),
                Text("n-tuples", font_size=20, color=C_MUTED),
            ).arrange(DOWN, buff=0.10),
        ).arrange(RIGHT, buff=0.85).move_to([0.2, -2.15, 0])

        arrows = VGroup(
            Arrow(scaling_group[0].get_right(), scaling_group[1].get_left(), buff=0.12, color=GREY_B, stroke_width=2),
            Arrow(scaling_group[1].get_right(), scaling_group[2].get_left(), buff=0.12, color=GREY_B, stroke_width=2),
        )

        complexity_hint = Text(
            "More components and higher order both increase the cost.",
            font_size=23,
            color=C_MUTED,
        ).next_to(scaling_group, UP, buff=0.44)
        complexity_panel = RoundedRectangle(
            width=7.0,
            height=2.6,
            corner_radius=0.10,
            stroke_color=GREY_D,
            stroke_width=1.0,
            fill_color=BLACK,
            fill_opacity=0.08,
        ).move_to(VGroup(complexity_hint, scaling_group).get_center() + DOWN * 0.26)
        cost_line = MathTex(
            r"\mathrm{accurate,\ but\ repeated\ evaluation\ becomes\ the\ bottleneck}",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=0.22)

        self.play(FadeIn(complexity_panel), FadeIn(complexity_hint, shift=UP * 0.06))
        self.play(Write(scaling_group[0]))
        self.play(GrowArrow(arrows[0]), Write(scaling_group[1]))
        self.play(GrowArrow(arrows[1]), Write(scaling_group[2]))
        self.play(Write(cost_line))
        self.wait(1.2)

        # Final centered message.
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)])
        self.clear()
        self.wait(0.2)

        bridge_box = RoundedRectangle(
            width=8.8,
            height=1.8,
            corner_radius=0.12,
            stroke_color=C_VWA,
            stroke_width=1.8,
            fill_color=BLACK,
            fill_opacity=0.18,
        ).move_to(DOWN * 0.15)
        bridge = VGroup(
            Text("Next Step", font_size=30, color=C_VWA, weight=BOLD),
            Tex(
                r"We therefore seek a reduced, spectrally consistent",
                font_size=27,
                color=WHITE,
            ),
            Tex(
                r"formulation for superharmonic bound waves.",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.16).move_to(bridge_box)

        self.play(FadeIn(bridge_box), Write(bridge))
        self.wait(3.0)
