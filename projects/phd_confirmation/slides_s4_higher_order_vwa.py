"""
Scenario 4 - Higher-Order VWA
=============================

First-pass scene after Scenario 3.  It shows that VWA is not only a
second-order shortcut: the same phase-preserving, kernel-reducing structure
extends to higher-order superharmonic bound waves.
"""

from manim import *
from pathlib import Path
from presentation_nav import bottom_progress_nav, keep_nav

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene

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
    "2nd to 5th order",
    "handoff",
]
HIGHER_ORDER_RESULT_IMAGE = (
    Path(__file__).resolve().parent
    / "data"
    / "higher_order"
    / "unidirectional_eta_orders_2to5_manim.png"
)


def panel(mob, color=C_PANEL, buff=0.18, opacity=0.08):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08).set_fill(BLACK, opacity=opacity)


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


def make_higher_order_result_slide():
    title = Text("Second to fifth order: unidirectional surface elevation", font_size=34, weight=BOLD)
    subtitle = Text(
        "same Manim-style comparison, now showing the higher-order hierarchy",
        font_size=23,
        color=C_MUTED,
    )
    header = VGroup(title, subtitle).arrange(DOWN, buff=0.07).to_edge(UP, buff=0.16)

    if HIGHER_ORDER_RESULT_IMAGE.exists():
        image = ImageMobject(str(HIGHER_ORDER_RESULT_IMAGE))
        image.set_width(12.65)
        if image.height > 6.35:
            image.set_height(6.35)
        image.next_to(header, DOWN, buff=0.10)
        return Group(header, image)

    placeholder = RoundedRectangle(
        width=11.4,
        height=5.4,
        corner_radius=0.08,
        stroke_color=C_VWA,
        fill_color=C_VWA,
        fill_opacity=0.06,
    ).next_to(header, DOWN, buff=0.28)
    label = Text("waiting for higher-order result figure", font_size=30, color=C_MUTED).move_to(placeholder)
    return VGroup(header, placeholder, label)


def make_higher_order_result_question_slide():
    title = Text("The formula is compact. What should the result show?", font_size=35, weight=BOLD)
    subtitle = Text(
        "After preserving phase and reducing the kernel cost, the check moves back to waveform space.",
        font_size=23,
        color=C_MUTED,
    )
    header = VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.22)

    left = VGroup(
        Text("compact VWA form", font_size=26, color=C_VWA, weight=BOLD),
        MathTex(
            r"\eta_{\rm VWA}^{(nn)}=\Re\!\left\{\eta_{a,K^{(n)}}^{(11)}[\eta_a^{(11)}]^{n-1}\right\}",
            font_size=31,
            color=C_VWA,
        ),
        Text("one weighted field per order", font_size=22, color=C_MUTED),
    ).arrange(DOWN, buff=0.14)
    left.scale_to_fit_width(5.45)
    left.add_to_back(panel(left, C_VWA, buff=0.20, opacity=0.08))

    right = VGroup(
        Text("result check", font_size=26, color=C_EXACT, weight=BOLD),
        MathTex(r"\eta^{(22)},\ \eta^{(33)},\ \eta^{(44)},\ \eta^{(55)}", font_size=34, color=WHITE),
        Text("do the ordered bound harmonics remain coherent?", font_size=22, color=C_MUTED),
    ).arrange(DOWN, buff=0.14)
    right.scale_to_fit_width(5.45)
    right.add_to_back(panel(right, C_EXACT, buff=0.20, opacity=0.08))

    cards = VGroup(left, right).arrange(RIGHT, buff=0.56).next_to(header, DOWN, buff=0.58)
    arrow = Arrow(cards.get_bottom() + DOWN * 0.18, cards.get_bottom() + DOWN * 0.64, color=C_WEIGHT, stroke_width=3)
    cue = Text("next: second to fifth order comparison", font_size=27, color=C_WEIGHT, weight=BOLD).next_to(arrow, DOWN, buff=0.10)
    return VGroup(header, cards, arrow, cue)


class S4HigherOrderVWASlides(Slide):
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
        title = Text("Extending VWA to higher order", font_size=41, weight=BOLD)
        subtitle = Text("same phase structure, compact FFT-ready products", font_size=27, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav = bottom_progress_nav(
            4,
            6,
            "higher-order VWA",
            SCENARIO4_SUBSCENARIOS,
            nav_progress,
            accent=C_VWA,
            detail_label_color=WHITE,
            detail_font_size=16,
            detail_label_stroke=False,
        )
        self.add(nav_progress, nav)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)
        self.slide_pause(nav_progress, 0.35)

        transition = VGroup(
            Text("Second order showed the key mechanism.", font_size=32, color=WHITE),
            Text("But bound waves do not stop at second order.", font_size=32, color=C_MUTED),
        ).arrange(DOWN, buff=0.16).move_to(ORIGIN)
        self.play(quiet_fade(transition[0]), run_time=0.6)
        self.slide_pause(nav_progress, 0.8)
        self.play(quiet_fade(transition[1]), run_time=0.6)
        self.slide_pause(nav_progress, 1.0)
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
        self.slide_pause(nav_progress, 1.6)

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
        self.slide_pause(nav_progress, 2.0)

        phase_keep = VGroup(
            Text("The important phase is still exact", font_size=32, color=C_PHASE),
            MathTex(
                r"\theta_{j_1}+\cdots+\theta_{j_n}",
                r"\quad\Rightarrow\quad",
                r"k_{j_1}+\cdots+k_{j_n}",
                font_size=42,
            ),
            Text("higher order means higher sum wavenumber, not a new free wave", font_size=27, color=C_MUTED),
        ).arrange(DOWN, buff=0.18).move_to(ORIGIN).shift(DOWN * 0.20)
        phase_keep[1][0].set_color(C_PHASE)
        phase_keep[1][2].set_color(C_WEIGHT)
        phase_box = panel(phase_keep, C_PHASE, buff=0.22, opacity=0.06)
        self.play(FadeOut(exact_eq), FadeOut(cards), FadeOut(exact_title))
        self.play(FadeIn(phase_box), quiet_fade(phase_keep), run_time=1.0)
        self.slide_pause(nav_progress, 3.0)

        self.play(FadeOut(phase_keep), FadeOut(phase_box))

        vwa_title = Text("VWA: replace the n-wavenumber kernel by one weighted signal", font_size=30, color=C_VWA)
        vwa_title.next_to(subtitle, DOWN, buff=0.44)
        vwa_title.scale_to_fit_width(11.2)
        weighted = MathTex(
            r"\eta_{a,K^{(n)}}^{(11)}",
            r"=",
            r"\mathcal F^{-1}\!\left\{K_n^{(n)}(k)\widehat\eta(k)\right\}",
            font_size=39,
            color=C_WEIGHT,
        )
        compact = MathTex(
            r"\eta_{\rm VWA}^{(nn)}(x,t)",
            r"=",
            r"\Re\left\{",
            r"\eta_{a,K^{(n)}}^{(11)}(x,t)",
            r"\left[\eta_a^{(11)}(x,t)\right]^{n-1}",
            r"\right\}",
            font_size=41,
            color=C_VWA,
        )
        compact[0].set_color(WHITE)
        compact[3].set_color(C_WEIGHT)
        compact[4].set_color(C_LINEAR)
        formula_group = VGroup(weighted, compact).arrange(DOWN, buff=0.22).next_to(vwa_title, DOWN, buff=0.66)
        formula_group.scale_to_fit_width(9.9)
        formula_box = panel(formula_group, C_VWA, buff=0.22, opacity=0.08)
        self.play(quiet_fade(vwa_title), FadeIn(formula_box), quiet_fade(formula_group), run_time=1.0)
        self.slide_pause(nav_progress, 4.0)

        product_cards = VGroup()
        for label, expr in [
            ("2nd order", r"\eta_{a,K^{(2)}}^{(11)}\eta_a^{(11)}"),
            ("3rd order", r"\eta_{a,K^{(3)}}^{(11)}[\eta_a^{(11)}]^2"),
            ("4th order", r"\eta_{a,K^{(4)}}^{(11)}[\eta_a^{(11)}]^3"),
            ("5th order", r"\eta_{a,K^{(5)}}^{(11)}[\eta_a^{(11)}]^4"),
        ]:
            body = VGroup(
                Text(label, font_size=22, color=C_MUTED),
                MathTex(expr, font_size=27, color=C_VWA),
            ).arrange(DOWN, buff=0.08)
            product_cards.add(VGroup(panel(body, C_VWA, buff=0.13, opacity=0.04), body))
        product_cards.arrange(RIGHT, buff=0.18).next_to(formula_box, DOWN, buff=0.28)
        product_cards.scale_to_fit_width(11.0)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.06) for card in product_cards], lag_ratio=0.16))
        self.slide_pause(nav_progress, 4.35)
        self.play(FadeOut(product_cards), run_time=0.6)

        cost = VGroup(
            VGroup(
                Text("exact order n", font_size=27, color=C_EXACT),
                MathTex(r"\mathcal O(N_c^n)", font_size=49, color=C_EXACT),
                Text("all wavenumber tuples", font_size=22, color=C_MUTED),
            ).arrange(DOWN, buff=0.08),
            Arrow(LEFT, RIGHT, color=C_MUTED, stroke_width=3),
            VGroup(
                Text("VWA order n", font_size=27, color=C_VWA),
                MathTex(r"\mathcal O(N_c\log N_c)", font_size=49, color=C_WEIGHT),
                Text("FFT fields + products", font_size=22, color=C_MUTED),
            ).arrange(DOWN, buff=0.08),
        ).arrange(RIGHT, buff=0.42).to_edge(DOWN, buff=0.92)
        cost_box = panel(cost, C_PANEL, buff=0.18, opacity=0.06)
        self.play(FadeIn(cost_box), FadeIn(cost, shift=UP * 0.08), run_time=1.2)
        self.slide_pause(nav_progress, 5.0)

        self.play(*[FadeOut(mob) for mob in keep_nav(list(self.mobjects), nav)])
        self.clear()
        self.add(nav_progress, nav)

        result_question = make_higher_order_result_question_slide()
        self.play(FadeIn(result_question, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 5.55)
        self.play(FadeOut(result_question), run_time=0.55)
        self.clear()
        self.add(nav_progress, nav)

        result_slide = make_higher_order_result_slide()
        self.play(FadeIn(result_slide, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 6.0)
        self.play(FadeOut(result_slide), run_time=0.55)
        self.clear()
        self.add(nav_progress, nav)

        final = VGroup(
            Text("The same VWA structure extends from second to fifth order.", font_size=45, color=WHITE),
            Text("The result is a compact set of higher-order bound harmonics.", font_size=40, color=C_MUTED),
        ).arrange(DOWN, buff=0.20).move_to(ORIGIN)
        for line in final:
            line.scale_to_fit_width(min(line.width, 12.15))
        self.play(quiet_fade(final[0]), run_time=0.6)
        self.slide_pause(nav_progress, 6.35)
        self.play(quiet_fade(final[1]), run_time=0.6)
        self.slide_pause(nav_progress, 7.0)
