"""
Scenario 4 - Higher-Order VWA
=============================

First-pass scene after Scenario 3.  It shows that VWA is not only a
second-order shortcut: the same phase-preserving, kernel-reducing structure
extends to higher-order superharmonic bound waves.
"""

from manim import *
from presentation_nav import bottom_progress_nav, keep_nav

C_EXACT = ORANGE
C_VWA = YELLOW
C_WEIGHT = TEAL
C_PHASE = BLUE_B
C_LINEAR = BLUE
C_MUTED = GREY_B
C_PANEL = GREY_D
SCENARIO4_SECONDS = 53.67
SCENARIO4_SUBSCENARIOS = [
    "motivation",
    "exact n-tuples",
    "phase structure",
    "compact product",
    "cost reduction",
    "handoff",
]


def panel(mob, color=C_PANEL, buff=0.18, opacity=0.08):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08).set_fill(BLACK, opacity=opacity)


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


class HigherOrderVWA(Scene):
    def construct(self):
        title = Text("Extending VWA to higher order", font_size=38, weight=BOLD)
        subtitle = Text("same phase structure, compact FFT-ready products", font_size=25, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav_progress.add_updater(
            lambda tracker, dt: tracker.increment_value(len(SCENARIO4_SUBSCENARIOS) * dt / SCENARIO4_SECONDS)
        )
        nav = bottom_progress_nav(
            4,
            6,
            "higher-order VWA",
            SCENARIO4_SUBSCENARIOS,
            nav_progress,
            accent=C_VWA,
        )
        self.add(nav_progress, nav)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)

        transition = VGroup(
            Text("Second order showed the key mechanism.", font_size=32, color=WHITE),
            Text("But bound waves do not stop at second order.", font_size=32, color=C_MUTED),
        ).arrange(DOWN, buff=0.16).move_to(ORIGIN)
        self.play(quiet_fade(transition[0]), run_time=0.6)
        self.wait(1.8)
        self.play(quiet_fade(transition[1]), run_time=0.6)
        self.wait(3.2)
        self.play(FadeOut(transition))

        exact_title = Text("Exact theory: each higher order adds one more wavenumber", font_size=31, color=C_EXACT)
        exact_title.next_to(subtitle, DOWN, buff=0.42)
        exact_eq = MathTex(
            r"\eta_{\rm exact}^{(nn)}",
            r"=",
            r"\Re\bigl\{",
            r"\sum_{j_1}\cdots\sum_{j_n}",
            r"K^{(n)}(k_{j_1},\ldots,k_{j_n})",
            r"a_{j_1}\cdots a_{j_n}",
            r"e^{i(\theta_{j_1}+\cdots+\theta_{j_n})}",
            r"\bigr\}",
            font_size=31,
        ).next_to(exact_title, DOWN, buff=0.28)
        exact_eq.scale_to_fit_width(11.2)
        exact_eq[3].set_color(C_EXACT)
        exact_eq[4].set_color(C_EXACT)
        exact_eq[6].set_color(C_PHASE)
        self.play(quiet_fade(exact_title), quiet_fade(exact_eq), run_time=1.0)
        self.wait(2.2)

        cards = VGroup()
        for order, tuples, cost in [
            (2, r"(k_{j_1},k_{j_2})", r"\mathcal O(N_c^2)"),
            (3, r"(k_{j_1},k_{j_2},k_{j_3})", r"\mathcal O(N_c^3)"),
            (4, r"(k_{j_1},\ldots,k_{j_4})", r"\mathcal O(N_c^4)"),
            (5, r"(k_{j_1},\ldots,k_{j_5})", r"\mathcal O(N_c^5)"),
        ]:
            card = VGroup(
                Text(f"order {order}", font_size=24, color=C_MUTED),
                MathTex(tuples, font_size=30, color=WHITE),
                MathTex(cost, font_size=34, color=C_EXACT),
            ).arrange(DOWN, buff=0.08)
            box = panel(card, C_EXACT, buff=0.14, opacity=0.04)
            cards.add(VGroup(box, card))
        cards.arrange(RIGHT, buff=0.22).next_to(exact_eq, DOWN, buff=0.48)
        cards.scale_to_fit_width(11.4)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.18))
        self.wait(3.8)

        phase_keep = VGroup(
            Text("The important phase is still exact", font_size=32, color=C_PHASE),
            MathTex(
                r"\theta_{j_1}+\cdots+\theta_{j_n}",
                r"\quad\Rightarrow\quad",
                r"k_{j_1}+\cdots+k_{j_n}",
                font_size=42,
            ),
            Text("higher order means higher sum wavenumber, not a new free wave", font_size=25, color=C_MUTED),
        ).arrange(DOWN, buff=0.18).move_to(ORIGIN).shift(DOWN * 0.20)
        phase_keep[1][0].set_color(C_PHASE)
        phase_keep[1][2].set_color(C_WEIGHT)
        phase_box = panel(phase_keep, C_PHASE, buff=0.22, opacity=0.06)
        self.play(FadeOut(exact_eq), FadeOut(cards), FadeOut(exact_title))
        self.play(FadeIn(phase_box), quiet_fade(phase_keep), run_time=1.0)
        self.wait(4.4)

        self.play(FadeOut(phase_keep), FadeOut(phase_box))

        vwa_title = Text("VWA: replace the n-wavenumber kernel by one weighted signal", font_size=30, color=C_VWA)
        vwa_title.next_to(subtitle, DOWN, buff=0.44)
        vwa_title.scale_to_fit_width(11.2)
        weighted = MathTex(
            r"\eta_{a,K^{(n)}}^{(11)}",
            r"=",
            r"\mathcal F^{-1}\!\left\{K_n^{(n)}(k)\widehat\eta(k)\right\}",
            font_size=36,
            color=C_WEIGHT,
        )
        compact = MathTex(
            r"\eta_{\rm VWA}^{(nn)}(x,t)",
            r"=",
            r"\Re\left\{",
            r"\eta_{a,K^{(n)}}^{(11)}(x,t)",
            r"\left[\eta_a^{(11)}(x,t)\right]^{n-1}",
            r"\right\}",
            font_size=38,
            color=C_VWA,
        )
        compact[0].set_color(WHITE)
        compact[3].set_color(C_WEIGHT)
        compact[4].set_color(C_LINEAR)
        formula_group = VGroup(weighted, compact).arrange(DOWN, buff=0.22).next_to(vwa_title, DOWN, buff=0.66)
        formula_group.scale_to_fit_width(9.9)
        formula_box = panel(formula_group, C_VWA, buff=0.22, opacity=0.08)
        self.play(quiet_fade(vwa_title), FadeIn(formula_box), quiet_fade(formula_group), run_time=1.0)
        self.wait(5.0)

        product_cards = VGroup()
        for label, expr in [
            ("second", r"\eta_{a,K^{(2)}}^{(11)}\eta_a^{(11)}"),
            ("third", r"\eta_{a,K^{(3)}}^{(11)}[\eta_a^{(11)}]^2"),
            ("fourth", r"\eta_{a,K^{(4)}}^{(11)}[\eta_a^{(11)}]^3"),
            ("fifth", r"\eta_{a,K^{(5)}}^{(11)}[\eta_a^{(11)}]^4"),
        ]:
            body = VGroup(
                Text(label, font_size=22, color=C_MUTED),
                MathTex(expr, font_size=27, color=C_VWA),
            ).arrange(DOWN, buff=0.08)
            product_cards.add(VGroup(panel(body, C_VWA, buff=0.13, opacity=0.04), body))
        product_cards.arrange(RIGHT, buff=0.18).next_to(formula_box, DOWN, buff=0.28)
        product_cards.scale_to_fit_width(11.0)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.06) for card in product_cards], lag_ratio=0.16))
        self.wait(3.6)
        self.play(FadeOut(product_cards), run_time=0.6)

        cost = VGroup(
            VGroup(
                Text("exact order n", font_size=27, color=C_EXACT),
                MathTex(r"\mathcal O(N_c^n)", font_size=46, color=C_EXACT),
                Text("all wavenumber tuples", font_size=22, color=C_MUTED),
            ).arrange(DOWN, buff=0.08),
            Arrow(LEFT, RIGHT, color=C_MUTED, stroke_width=3),
            VGroup(
                Text("VWA order n", font_size=27, color=C_VWA),
                MathTex(r"\mathcal O(N_c\log N_c)", font_size=46, color=C_WEIGHT),
                Text("FFT fields + products", font_size=22, color=C_MUTED),
            ).arrange(DOWN, buff=0.08),
        ).arrange(RIGHT, buff=0.42).to_edge(DOWN, buff=0.92)
        cost_box = panel(cost, C_PANEL, buff=0.18, opacity=0.06)
        self.play(FadeIn(cost_box), FadeIn(cost, shift=UP * 0.08), run_time=1.2)
        self.wait(4.4)

        self.play(*[FadeOut(mob) for mob in keep_nav(list(self.mobjects), nav)])
        self.clear()
        self.add(nav_progress, nav)

        final = VGroup(
            Text("Higher-order VWA keeps the superharmonic phase structure.", font_size=48, color=WHITE),
            Text("It approximates kernel amplitudes with reusable wavenumber weights.", font_size=40, color=C_MUTED),
            Text("Next: how does the compact structure match exact theory and nonlinear simulations?", font_size=40, color=C_VWA),
        ).arrange(DOWN, buff=0.20).move_to(ORIGIN)
        for line in final:
            line.scale_to_fit_width(min(line.width, 12.15))
        self.play(quiet_fade(final[0]), run_time=0.6)
        self.wait(1.8)
        self.play(quiet_fade(final[1]), run_time=0.6)
        self.wait(1.8)
        self.play(quiet_fade(final[2]), run_time=0.6)
        self.wait(6.0)
        nav_progress.clear_updaters()
