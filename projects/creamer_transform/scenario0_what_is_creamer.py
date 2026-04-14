import numpy as np

from manim import *


PHYSICAL = BLUE_C
NONLINEAR = ORANGE
TRANSFORMED = TEAL_C
ACCENT = YELLOW
MUTED = GREY_B
PANEL = GREY_D
ORDER2 = GREEN_C
ORDER3 = RED_C


def card(mob, color=PANEL, buff=0.28):
    return VGroup(
        SurroundingRectangle(
            mob,
            color=color,
            buff=buff,
            corner_radius=0.12,
            stroke_width=1.5,
        ),
        mob,
    )


def fit_to_width(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def formula_block(lines, font_size, color, max_width, buff=0.06):
    if isinstance(lines, str):
        lines = [lines]
    block = VGroup(
        *[fit_to_width(MathTex(line, font_size=font_size, color=color), max_width) for line in lines]
    )
    return block.arrange(DOWN, buff=buff, aligned_edge=LEFT)


def hidden_copy(mob):
    ghost = mob.copy()
    ghost.set_opacity(0)
    return ghost


def profile_strip(
    surface_func,
    surface_color,
    reference_func=None,
    reference_color=GREY_D,
    component_specs=None,
    x_length=4.9,
    y_length=0.82,
    x_min=-2 * PI,
    x_max=2 * PI,
    reference_stroke_width=3.4,
    reference_stroke_opacity=1.0,
    component_stroke_width=2.6,
    component_stroke_opacity=0.9,
    graph_stroke_width=4.1,
    graph_stroke_opacity=1.0,
    reference_z_index=0,
    component_z_index=1,
    graph_z_index=2,
):
    axes = Axes(
        x_range=[x_min, x_max, PI / 2],
        y_range=[-1.1, 1.1, 1],
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"include_ticks": False, "include_numbers": False, "stroke_opacity": 0},
    )
    if reference_func is None:
        reference = Line(
            axes.c2p(x_min, 0),
            axes.c2p(x_max, 0),
            color=reference_color,
            stroke_width=reference_stroke_width,
            stroke_opacity=reference_stroke_opacity,
        )
    else:
        reference = axes.plot(
            reference_func,
            x_range=[x_min, x_max],
            color=reference_color,
            stroke_width=reference_stroke_width,
            stroke_opacity=reference_stroke_opacity,
        )
    reference.set_z_index(reference_z_index)
    components = VGroup()
    if component_specs:
        components = VGroup(
            *[
                axes.plot(
                    func,
                    x_range=[x_min, x_max],
                    color=color,
                    stroke_width=component_stroke_width,
                    stroke_opacity=component_stroke_opacity,
                ).set_z_index(component_z_index)
                for func, color in component_specs
            ]
        )
    graph = axes.plot(
        surface_func,
        x_range=[x_min, x_max],
        color=surface_color,
        stroke_width=graph_stroke_width,
        stroke_opacity=graph_stroke_opacity,
    )
    graph.set_z_index(graph_z_index)
    return VGroup(reference, components, graph)


def harmonic_tag(label, color):
    tex = MathTex(label, font_size=20, color=color)
    box = SurroundingRectangle(tex, color=color, buff=0.1, corner_radius=0.08, stroke_width=1.7)
    return VGroup(box, tex)


def profile_row(
    order_text,
    formula,
    surface_func,
    reference_func,
    formula_color,
    surface_color,
    formula_width=4.35,
    reference_color=ACCENT,
    formula_color_map=None,
    component_specs=None,
    harmonic_labels=None,
    x_min=-2 * PI,
    x_max=2 * PI,
    strip_x_length=4.9,
    strip_y_length=0.82,
    reference_stroke_width=3.4,
    reference_stroke_opacity=1.0,
    component_stroke_width=2.6,
    component_stroke_opacity=0.9,
    graph_stroke_width=4.1,
    graph_stroke_opacity=1.0,
    reference_z_index=0,
    component_z_index=1,
    graph_z_index=2,
):
    order_tag = Text(order_text, font_size=18, color=ACCENT, weight=BOLD)
    formula_tex = fit_to_width(MathTex(formula, font_size=18, color=formula_color), formula_width)
    if formula_color_map:
        for token, token_color in formula_color_map:
            formula_tex.set_color_by_tex(token, token_color)
    header = VGroup(order_tag, formula_tex).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    parts = [header]
    if harmonic_labels:
        chips = VGroup(*[harmonic_tag(label, color) for label, color in harmonic_labels]).arrange(RIGHT, buff=0.16)
        parts.append(chips)
    strip = profile_strip(
        surface_func,
        surface_color,
        reference_func=reference_func,
        reference_color=reference_color,
        component_specs=component_specs,
        x_length=strip_x_length,
        y_length=strip_y_length,
        x_min=x_min,
        x_max=x_max,
        reference_stroke_width=reference_stroke_width,
        reference_stroke_opacity=reference_stroke_opacity,
        component_stroke_width=component_stroke_width,
        component_stroke_opacity=component_stroke_opacity,
        graph_stroke_width=graph_stroke_width,
        graph_stroke_opacity=graph_stroke_opacity,
        reference_z_index=reference_z_index,
        component_z_index=component_z_index,
        graph_z_index=graph_z_index,
    )
    parts.append(strip)
    return VGroup(*parts).arrange(DOWN, buff=0.08, aligned_edge=LEFT)


class WhatIsCreamer(Scene):
    def construct(self):
        title = Text("Scenario 0: How I Would Introduce Creamer", font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        self.play(Write(title))

        # Phase 1: what the exact H is
        vars_line = MathTex(r"(\zeta,\phi_s)", font_size=36, color=PHYSICAL)
        vars_note = Text("let me start from the canonical surface variables", font_size=18, color=MUTED)
        h_title = Text("First, here is the exact Hamiltonian", font_size=22, color=WHITE)
        h_line = fit_to_width(
            MathTex(
                r"H(\zeta,\phi_s)=\frac12\int d^2x\left[\phi_s\left(D_z-(\partial_x\zeta)\cdot D_x\right)\phi_s+g\zeta^2\right]",
                font_size=29,
                color=WHITE,
            ),
            10.1,
        )
        h_note = Tex(
            r"Because $D_x,D_z$ depend on $\zeta$, this exact $H$ is already nonlinear.",
            font_size=24,
            color=ACCENT,
        )
        intro = VGroup(
            vars_line,
            vars_note,
            h_title,
            h_line,
            h_note,
        ).arrange(DOWN, buff=0.16)
        intro_card = card(intro, color=PHYSICAL, buff=0.32)
        intro_card.move_to(ORIGIN + DOWN * 0.18)

        self.play(FadeIn(intro_card, shift=UP * 0.15), run_time=1.3)
        self.wait(3.0)

        # Phase 2: the operator expansion from the local MMA derivation
        operator_title = Text("Now, this is the DNO I want to expand", font_size=22, color=MUTED)
        operator_eq = fit_to_width(
            MathTex(
                r"G(\zeta)\phi_s:=\left(D_z-\nabla\zeta\cdot D_x\right)\phi_s",
                font_size=31,
                color=WHITE,
            ),
            10.3,
        )
        operator_note = Text("The Some Creamer MMA code expands this operator order by order.", font_size=18, color=MUTED)
        n0_line = MathTex(
            r"G_0\phi_s=\theta\phi_s",
            font_size=29,
            color=PHYSICAL,
        )
        n1_line = fit_to_width(
            MathTex(
                r"G_1(\zeta)\phi_s=-\theta(\zeta\theta\phi_s)-\nabla\cdot(\zeta\nabla\phi_s)",
                font_size=24,
                color=NONLINEAR,
            ),
            10.3,
        )
        n2_line = fit_to_width(
            MathTex(
                r"G_2(\zeta,\zeta)\phi_s=\theta\zeta\theta\zeta\theta\phi_s+\frac12\theta(\zeta^2\Delta\phi_s)+\frac12\Delta(\zeta^2\theta\phi_s)",
                font_size=21,
                color=WHITE,
            ),
            10.3,
        )
        operator_block = VGroup(
            operator_title,
            operator_eq,
            operator_note,
            n0_line,
            n1_line,
            n2_line,
        ).arrange(DOWN, buff=0.18)
        operator_card = card(operator_block, color=PHYSICAL, buff=0.28)
        operator_card.move_to(DOWN * 0.18)

        # Phase 3: order-by-order comparison
        compare_title = Text("Now compare where the expansion is taken", font_size=20, color=MUTED)

        left_context = VGroup(
            Text("If I expand in the shape function", font_size=21, color=PHYSICAL, weight=BOLD),
            fit_to_width(
                MathTex(
                    r"F(x,\zeta)=F(x,0)+\zeta F_z(x,0)+\frac12\zeta^2F_{zz}(x,0)+\cdots",
                    font_size=20,
                    color=WHITE,
                ),
                5.9,
            ),
            fit_to_width(
                MathTex(
                    r"\zeta=\zeta^{(1)}+\zeta^{(2)}+\zeta^{(3)}+\cdots",
                    font_size=23,
                    color=PHYSICAL,
                ),
                5.85,
            ),
            Tex(r"$F$ here is just a generic field on the shifted surface, not the gravity $g$.", font_size=16, color=MUTED),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        left_context_panel = card(left_context, color=PHYSICAL, buff=0.2)

        right_context = VGroup(
            Text("If I do the Stokes expansion", font_size=21, color=NONLINEAR, weight=BOLD),
            fit_to_width(
                MathTex(
                    r"\eta=\epsilon\eta_1+\epsilon^2\eta_2+\epsilon^3\eta_3+\cdots",
                    font_size=22,
                    color=WHITE,
                ),
                6.05,
            ),
            fit_to_width(
                MathTex(
                    r"\phi=\epsilon\phi_1+\epsilon^2\phi_2+\epsilon^3\phi_3+\cdots",
                    font_size=22,
                    color=WHITE,
                ),
                6.05,
            ),
            Tex(r"I Taylor-expand the BCs from $z=\eta$ back to $z=0$", font_size=18, color=ACCENT),
        ).arrange(DOWN, buff=0.07, aligned_edge=LEFT)
        right_context_panel = card(right_context, color=NONLINEAR, buff=0.2)

        framing_row = VGroup(left_context_panel, right_context_panel).arrange(RIGHT, buff=0.24, aligned_edge=UP)

        order_slot = hidden_copy(Text("3rd order", font_size=26, color=ACCENT, weight=BOLD))
        order_label_1 = Text("1st order", font_size=26, color=ACCENT, weight=BOLD)
        order_label_2 = Text("2nd order", font_size=26, color=ACCENT, weight=BOLD)
        order_label_3 = Text("3rd order", font_size=26, color=ACCENT, weight=BOLD)

        left_formula_1 = formula_block(
            r"\zeta^{(1)} F_z(x,0)",
            font_size=31,
            color=PHYSICAL,
            max_width=6.0,
        )
        left_formula_2 = formula_block(
            r"\zeta^{(2)} F_z(x,0)+\frac12\left(\zeta^{(1)}\right)^2 F_{zz}(x,0)",
            font_size=25,
            color=PHYSICAL,
            max_width=6.0,
        )
        left_formula_3 = formula_block(
            r"\zeta^{(3)} F_z(x,0)+\zeta^{(1)}\zeta^{(2)} F_{zz}(x,0)+\frac16\left(\zeta^{(1)}\right)^3 F_{zzz}(x,0)",
            font_size=22,
            color=PHYSICAL,
            max_width=6.0,
        )
        left_slot = hidden_copy(left_formula_3)

        left_panel_shell = VGroup(
            Text("the next Taylor term from the shape", font_size=18, color=PHYSICAL, weight=BOLD),
            left_slot,
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        left_panel = card(left_panel_shell, color=PHYSICAL, buff=0.22)

        kin_formula_1 = formula_block(
            r"\eta_{1,t}=\phi_{1,z}",
            font_size=29,
            color=WHITE,
            max_width=6.1,
        )
        kin_formula_2 = formula_block(
            [
                r"\eta_{2,t}-\phi_{2,z}=\eta_1\phi_{1,zz}",
                r"-\eta_{1,x}\phi_{1,x}",
            ],
            font_size=24,
            color=WHITE,
            max_width=6.1,
        )
        kin_formula_3 = formula_block(
            [
                r"\eta_{3,t}-\phi_{3,z}=\eta_1\phi_{2,zz}+\eta_2\phi_{1,zz}",
                r"+\frac12\eta_1^2\phi_{1,zzz}",
                r"-\eta_{1,x}\phi_{2,x}-\eta_{2,x}\phi_{1,x}-\eta_1\eta_{1,x}\phi_{1,xz}",
            ],
            font_size=20,
            color=WHITE,
            max_width=6.1,
        )
        kin_slot = hidden_copy(kin_formula_3)

        dyn_formula_1 = formula_block(
            r"\phi_{1,t}+g\eta_1=0",
            font_size=29,
            color=WHITE,
            max_width=6.1,
        )
        dyn_formula_2 = formula_block(
            [
                r"\phi_{2,t}+g\eta_2=-\eta_1\phi_{1,tz}",
                r"-\frac12\left(\phi_{1,x}^2+\phi_{1,z}^2\right)",
            ],
            font_size=22,
            color=WHITE,
            max_width=6.1,
        )
        dyn_formula_3 = formula_block(
            [
                r"\phi_{3,t}+g\eta_3=-\eta_1\phi_{2,tz}-\eta_2\phi_{1,tz}",
                r"-\frac12\eta_1^2\phi_{1,tzz}-\phi_{1,x}\phi_{2,x}-\phi_{1,z}\phi_{2,z}",
                r"-\eta_1\left(\phi_{1,x}\phi_{1,xz}+\phi_{1,z}\phi_{1,zz}\right)",
            ],
            font_size=20,
            color=WHITE,
            max_width=6.1,
        )
        dyn_slot = hidden_copy(dyn_formula_3)

        right_panel_shell = VGroup(
            Text("what the Stokes BCs become at z=0", font_size=18, color=NONLINEAR, weight=BOLD),
            Text("kinematic BC", font_size=15, color=MUTED),
            kin_slot,
            Text("dynamic BC", font_size=15, color=MUTED),
            dyn_slot,
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        right_panel = card(right_panel_shell, color=NONLINEAR, buff=0.22)

        panels_row = VGroup(left_panel, right_panel).arrange(RIGHT, buff=0.24, aligned_edge=UP)

        cross_note = fit_to_width(
            MathTex(
                r"\zeta=\zeta_L+\zeta_S \;\Rightarrow\; \zeta^2=\zeta_L^2+2\zeta_L\zeta_S+\zeta_S^2",
                font_size=18,
                color=ACCENT,
            ),
            11.15,
        )
        cross_note.set_color_by_tex(r"\zeta_L", ACCENT)
        cross_note.set_color_by_tex(r"\zeta_S", PHYSICAL)
        harmonic_note = fit_to_width(
            Tex(
                r"These source terms are what later generate the bound harmonics $\cos2\theta,\cos3\theta,\ldots$.",
                font_size=16,
                color=MUTED,
            ),
            10.9,
        )
        third_notes = VGroup(cross_note, harmonic_note).arrange(DOWN, buff=0.06)

        compare_shell = VGroup(compare_title, framing_row, order_slot, panels_row).arrange(DOWN, buff=0.16)
        compare_shell.move_to(DOWN * 0.18)
        third_notes.next_to(panels_row, DOWN, buff=0.08)

        order_label_1.move_to(order_slot)
        order_label_2.move_to(order_slot)
        order_label_3.move_to(order_slot)

        left_formula_1.move_to(left_slot)
        left_formula_2.move_to(left_slot)
        left_formula_3.move_to(left_slot)
        kin_formula_1.move_to(kin_slot)
        kin_formula_2.move_to(kin_slot)
        kin_formula_3.move_to(kin_slot)
        dyn_formula_1.move_to(dyn_slot)
        dyn_formula_2.move_to(dyn_slot)
        dyn_formula_3.move_to(dyn_slot)

        # Phase 4: more graphical comparison
        visual_title = Text("First, think about the usual Stokes wave", font_size=25, color=MUTED)
        intro_formula_1 = fit_to_width(
            MathTex(
                r"\eta(\theta)=a\cos\theta",
                font_size=35,
                color=NONLINEAR,
            ),
            12.8,
        )
        intro_formula_2 = fit_to_width(
            MathTex(
                r"\eta(\theta)=a\cos\theta+(ak)C_{22}\cos2\theta",
                font_size=35,
                color=NONLINEAR,
            ),
            12.8,
        )
        intro_formula_3 = fit_to_width(
            MathTex(
                r"\eta(\theta)=a\cos\theta+(ak)C_{22}\cos2\theta+(ak)^2C_{33}\cos3\theta+\cdots",
                font_size=35,
                color=NONLINEAR,
            ),
            12.8,
        )
        for formula in [intro_formula_1, intro_formula_2, intro_formula_3]:
            formula.set_color_by_tex(r"\cos\theta", NONLINEAR)
            formula.set_color_by_tex(r"\cos2\theta", ORDER2)
            formula.set_color_by_tex(r"\cos3\theta", ORDER3)
        intro_harmonics_1 = VGroup(
            harmonic_tag(r"\cos\theta\,(k)", NONLINEAR),
        ).arrange(RIGHT, buff=0.16)
        intro_harmonics_2 = VGroup(
            harmonic_tag(r"\cos\theta\,(k)", NONLINEAR),
            harmonic_tag(r"\cos2\theta\,(2k)", ORDER2),
        ).arrange(RIGHT, buff=0.16)
        intro_harmonics_3 = VGroup(
            harmonic_tag(r"\cos\theta\,(k)", NONLINEAR),
            harmonic_tag(r"\cos2\theta\,(2k)", ORDER2),
            harmonic_tag(r"\cos3\theta\,(3k)", ORDER3),
        ).arrange(RIGHT, buff=0.16)
        intro_strip_1 = profile_strip(
            lambda x: 0.28 * np.cos(2 * x),
            WHITE,
            reference_func=lambda x: 0 * x,
            reference_color=ACCENT,
            component_specs=[
                (lambda x: 0.28 * np.cos(2 * x), NONLINEAR),
            ],
            x_length=12.8,
            y_length=2.0,
            x_min=-3 * PI,
            x_max=3 * PI,
        )
        intro_strip_2 = profile_strip(
            lambda x: 0.28 * np.cos(2 * x) + 0.12 * np.cos(4 * x),
            WHITE,
            reference_func=lambda x: 0 * x,
            reference_color=ACCENT,
            component_specs=[
                (lambda x: 0.28 * np.cos(2 * x), NONLINEAR),
                (lambda x: 0.12 * np.cos(4 * x), ORDER2),
            ],
            x_length=12.8,
            y_length=2.0,
            x_min=-3 * PI,
            x_max=3 * PI,
        )
        intro_strip_3 = profile_strip(
            lambda x: 0.28 * np.cos(2 * x) + 0.12 * np.cos(4 * x) + 0.055 * np.cos(6 * x),
            WHITE,
            reference_func=lambda x: 0 * x,
            reference_color=ACCENT,
            component_specs=[
                (lambda x: 0.28 * np.cos(2 * x), NONLINEAR),
                (lambda x: 0.12 * np.cos(4 * x), ORDER2),
                (lambda x: 0.055 * np.cos(6 * x), ORDER3),
            ],
            x_length=12.8,
            y_length=2.0,
            x_min=-3 * PI,
            x_max=3 * PI,
        )
        intro_formula_slot = hidden_copy(intro_formula_3)
        intro_harmonics_slot = hidden_copy(intro_harmonics_3)
        intro_strip_slot = hidden_copy(intro_strip_3)
        intro_formula_1.move_to(intro_formula_slot)
        intro_formula_2.move_to(intro_formula_slot)
        intro_formula_3.move_to(intro_formula_slot)
        intro_harmonics_1.move_to(intro_harmonics_slot)
        intro_harmonics_2.move_to(intro_harmonics_slot)
        intro_harmonics_3.move_to(intro_harmonics_slot)
        intro_strip_1.move_to(intro_strip_slot)
        intro_strip_2.move_to(intro_strip_slot)
        intro_strip_3.move_to(intro_strip_slot)
        z0_tag = MathTex(r"z=0", font_size=40, color=ACCENT)
        z0_tag.move_to(intro_strip_slot[0].get_center() + DOWN * 0.24)
        z0_emphasis = Tex(r"every order is expanded back to this level", font_size=24, color=ACCENT)
        z0_emphasis.next_to(z0_tag, DOWN, buff=0.04)
        intro_note = Tex(
            r"In the usual Stokes picture, every order is referred back to the same flat level $z=0$.",
            font_size=26,
            color=WHITE,
        )
        intro_note.set_color_by_tex(r"z=0", ACCENT)
        stokes_intro_block = VGroup(
            visual_title,
            intro_formula_slot,
            intro_harmonics_slot,
            VGroup(intro_strip_slot, z0_tag, z0_emphasis),
            intro_note,
        ).arrange(
            DOWN,
            buff=0.08,
        )
        stokes_intro_block.move_to(UP * 0.1)
        intro_formula_1.move_to(intro_formula_slot)
        intro_formula_2.move_to(intro_formula_slot)
        intro_formula_3.move_to(intro_formula_slot)
        intro_harmonics_1.move_to(intro_harmonics_slot)
        intro_harmonics_2.move_to(intro_harmonics_slot)
        intro_harmonics_3.move_to(intro_harmonics_slot)
        intro_strip_1.move_to(intro_strip_slot)
        intro_strip_2.move_to(intro_strip_slot)
        intro_strip_3.move_to(intro_strip_slot)

        split_title = Text("Now let me split that picture in two", font_size=20, color=MUTED)

        flat_rows = VGroup(
            profile_row(
                "1st",
                r"a\cos\theta",
                lambda x: 0.28 * np.cos(2 * x),
                lambda x: 0 * x,
                WHITE,
                WHITE,
                formula_width=2.15,
                formula_color_map=[(r"\cos\theta", NONLINEAR)],
                component_specs=[(lambda x: 0.28 * np.cos(2 * x), NONLINEAR)],
                harmonic_labels=[(r"\cos\theta\,(k)", NONLINEAR)],
                x_min=-3 * PI,
                x_max=3 * PI,
            ),
            profile_row(
                "2nd",
                r"+\ (ak)C_{22}\cos2\theta",
                lambda x: 0.28 * np.cos(2 * x) + 0.12 * np.cos(4 * x),
                lambda x: 0 * x,
                WHITE,
                WHITE,
                formula_width=3.15,
                formula_color_map=[(r"\cos\theta", NONLINEAR), (r"\cos2\theta", ORDER2)],
                component_specs=[
                    (lambda x: 0.28 * np.cos(2 * x), NONLINEAR),
                    (lambda x: 0.12 * np.cos(4 * x), ORDER2),
                ],
                harmonic_labels=[(r"\cos\theta\,(k)", NONLINEAR), (r"\cos2\theta\,(2k)", ORDER2)],
                x_min=-3 * PI,
                x_max=3 * PI,
            ),
            profile_row(
                "3rd",
                r"+\ (ak)^2 C_{33}\cos3\theta",
                lambda x: 0.28 * np.cos(2 * x) + 0.12 * np.cos(4 * x) + 0.055 * np.cos(6 * x),
                lambda x: 0 * x,
                WHITE,
                WHITE,
                formula_width=3.45,
                formula_color_map=[
                    (r"\cos\theta", NONLINEAR),
                    (r"\cos2\theta", ORDER2),
                    (r"\cos3\theta", ORDER3),
                ],
                component_specs=[
                    (lambda x: 0.28 * np.cos(2 * x), NONLINEAR),
                    (lambda x: 0.12 * np.cos(4 * x), ORDER2),
                    (lambda x: 0.055 * np.cos(6 * x), ORDER3),
                ],
                harmonic_labels=[
                    (r"\cos\theta\,(k)", NONLINEAR),
                    (r"\cos2\theta\,(2k)", ORDER2),
                    (r"\cos3\theta\,(3k)", ORDER3),
                ],
                x_min=-3 * PI,
                x_max=3 * PI,
            ),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        flat_note = Tex(r"Every order still points back to the same highlighted $z=0$.", font_size=17, color=ACCENT)
        flat_visual = VGroup(
            Text("Left: keep the flat reference z=0", font_size=19, color=NONLINEAR, weight=BOLD),
            Tex(r"reference level: the highlighted flat $z=0$", font_size=17, color=ACCENT),
            flat_rows,
            flat_note,
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        flat_level = lambda x: 0 * x
        setdown = lambda x: -0.42 * np.exp(-(x / 2.2) ** 2)
        long_wave = lambda x: setdown(x)
        packet_envelope = lambda x: np.exp(-(x / 1.55) ** 2)
        packet_phase = lambda x: np.cos(7.6 * x + 0.35)
        short_packet = lambda x: 0.10 * packet_envelope(x) * packet_phase(x)
        cross_packet = lambda x: -0.036 * (long_wave(x) / 0.42) * packet_envelope(x) * packet_phase(x)
        third_packet = lambda x: 0.016 * (long_wave(x) / 0.42) ** 2 * packet_envelope(x) * packet_phase(x)
        long_short_rows = VGroup(
            profile_row(
                "1st",
                r"\zeta_L+\zeta_S",
                lambda x: long_wave(x) + short_packet(x),
                long_wave,
                PHYSICAL,
                PHYSICAL,
                formula_width=2.55,
                formula_color_map=[(r"\zeta_L", ACCENT), (r"\zeta_S", PHYSICAL)],
                component_specs=[(flat_level, MUTED), (lambda x: long_wave(x) + short_packet(x), PHYSICAL)],
                harmonic_labels=[(r"\zeta_S", PHYSICAL)],
                x_min=-3 * PI,
                x_max=3 * PI,
                strip_y_length=1.25,
                reference_stroke_width=1.9,
                reference_stroke_opacity=1.0,
                component_stroke_width=1.3,
                component_stroke_opacity=0.7,
                graph_stroke_width=0.0,
                graph_stroke_opacity=0.0,
                reference_z_index=3,
                component_z_index=2,
            ),
            profile_row(
                "2nd",
                r"+\ \zeta_L\zeta_S",
                lambda x: long_wave(x) + short_packet(x) + cross_packet(x),
                long_wave,
                WHITE,
                WHITE,
                formula_width=2.55,
                formula_color_map=[(r"\zeta_L\zeta_S", ORDER2)],
                component_specs=[
                    (flat_level, MUTED),
                    (lambda x: long_wave(x) + short_packet(x), PHYSICAL),
                    (lambda x: long_wave(x) + short_packet(x) + cross_packet(x), ORDER2),
                ],
                harmonic_labels=[(r"\zeta_S", PHYSICAL), (r"\zeta_L\zeta_S", ORDER2)],
                x_min=-3 * PI,
                x_max=3 * PI,
                strip_y_length=1.25,
                reference_stroke_width=1.9,
                reference_stroke_opacity=1.0,
                component_stroke_width=1.3,
                component_stroke_opacity=0.7,
                graph_stroke_width=0.0,
                graph_stroke_opacity=0.0,
                reference_z_index=3,
                component_z_index=2,
            ),
            profile_row(
                "3rd",
                r"+\ \zeta_L^2\zeta_S+\zeta_S^2",
                lambda x: long_wave(x) + short_packet(x) + cross_packet(x) + third_packet(x),
                long_wave,
                WHITE,
                WHITE,
                formula_width=3.95,
                formula_color_map=[(r"\zeta_L^2\zeta_S", ORDER3), (r"\zeta_S^2", ORDER3)],
                component_specs=[
                    (flat_level, MUTED),
                    (lambda x: long_wave(x) + short_packet(x), PHYSICAL),
                    (lambda x: long_wave(x) + short_packet(x) + cross_packet(x), ORDER2),
                    (lambda x: long_wave(x) + short_packet(x) + cross_packet(x) + third_packet(x), ORDER3),
                ],
                harmonic_labels=[(r"\zeta_S", PHYSICAL), (r"\zeta_L\zeta_S", ORDER2), (r"\zeta_L^2\zeta_S", ORDER3)],
                x_min=-3 * PI,
                x_max=3 * PI,
                strip_y_length=1.25,
                reference_stroke_width=1.9,
                reference_stroke_opacity=1.0,
                component_stroke_width=1.3,
                component_stroke_opacity=0.7,
                graph_stroke_width=0.0,
                graph_stroke_opacity=0.0,
                reference_z_index=3,
                component_z_index=2,
            ),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        long_shift_note = MathTex(r"z=0 \;\longrightarrow\; z=\eta_L(x)", font_size=22, color=WHITE)
        long_shift_note.set_color_by_tex(r"z=0", MUTED)
        long_shift_note.set_color_by_tex(r"\eta_L", ACCENT)
        long_short_note = Tex(
            r"Now I let the long wave itself become the reference shape.",
            font_size=17,
            color=ACCENT,
        )
        long_short_visual = VGroup(
            Text("Right: expand around the long-wave shape", font_size=19, color=PHYSICAL, weight=BOLD),
            Tex(r"grey = old $z=0$, yellow = the set-down / long-wave shape $\zeta_L(x)$", font_size=17, color=ACCENT),
            long_shift_note,
            long_short_rows,
            long_short_note,
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        long_row1_strip = long_short_rows[0][-1]
        long_row1_ref = long_row1_strip[0]

        flat_visual_card = card(flat_visual, color=NONLINEAR, buff=0.18)
        long_short_card = card(long_short_visual, color=PHYSICAL, buff=0.18)
        split_row = VGroup(flat_visual_card, long_short_card).arrange(RIGHT, buff=0.2, aligned_edge=UP)
        split_block = VGroup(split_title, split_row).arrange(DOWN, buff=0.16)
        split_block.move_to(DOWN * 0.13)

        self.play(FadeOut(intro_card, shift=UP * 0.1), run_time=1.1)
        self.play(FadeIn(operator_card, shift=UP * 0.15), run_time=1.3)
        self.wait(4.0)
        self.play(FadeOut(operator_card, shift=UP * 0.1), run_time=1.1)
        self.play(
            FadeIn(compare_title, shift=UP * 0.1),
            FadeIn(framing_row, shift=UP * 0.1),
            FadeIn(order_label_1, shift=UP * 0.08),
            FadeIn(left_panel, shift=RIGHT * 0.08),
            FadeIn(right_panel, shift=LEFT * 0.08),
            run_time=1.35,
        )
        self.play(FadeIn(left_formula_1, shift=UP * 0.06), run_time=1.0)
        self.play(FadeIn(kin_formula_1, shift=UP * 0.06), run_time=1.0)
        self.play(FadeIn(dyn_formula_1, shift=UP * 0.06), run_time=1.0)
        self.wait(4.0)
        self.play(FadeTransform(order_label_1, order_label_2), run_time=1.1)
        self.play(FadeTransform(left_formula_1, left_formula_2), run_time=1.1)
        self.play(FadeTransform(kin_formula_1, kin_formula_2), run_time=1.1)
        self.play(FadeTransform(dyn_formula_1, dyn_formula_2), run_time=1.1)
        self.wait(5.0)
        self.play(FadeTransform(order_label_2, order_label_3), run_time=1.1)
        self.play(FadeTransform(left_formula_2, left_formula_3), run_time=1.1)
        self.play(FadeTransform(kin_formula_2, kin_formula_3), run_time=1.1)
        self.play(FadeTransform(dyn_formula_2, dyn_formula_3), run_time=1.1)
        self.play(FadeIn(third_notes, shift=UP * 0.05), run_time=1.0)
        self.wait(6.0)
        self.play(
            FadeOut(compare_title, shift=UP * 0.08),
            FadeOut(framing_row, shift=UP * 0.08),
            FadeOut(order_label_3, shift=UP * 0.08),
            FadeOut(left_panel, shift=UP * 0.08),
            FadeOut(right_panel, shift=UP * 0.08),
            FadeOut(left_formula_3, shift=UP * 0.08),
            FadeOut(kin_formula_3, shift=UP * 0.08),
            FadeOut(dyn_formula_3, shift=UP * 0.08),
            FadeOut(third_notes, shift=UP * 0.05),
            run_time=1.25,
        )
        self.play(
            FadeIn(visual_title, shift=UP * 0.08),
            FadeIn(intro_formula_1, shift=UP * 0.06),
            FadeIn(intro_strip_1, shift=UP * 0.06),
            FadeIn(z0_tag, shift=UP * 0.04),
            FadeIn(z0_emphasis, shift=UP * 0.04),
            FadeIn(intro_note, shift=UP * 0.04),
            run_time=1.35,
        )
        self.play(FadeIn(intro_harmonics_1, shift=UP * 0.04), run_time=1.0)
        self.wait(1.4)
        self.play(
            FadeTransform(intro_formula_1, intro_formula_2),
            FadeTransform(intro_strip_1, intro_strip_2),
            FadeTransform(intro_harmonics_1, intro_harmonics_2),
            run_time=1.25,
        )
        self.wait(1.4)
        self.play(
            FadeTransform(intro_formula_2, intro_formula_3),
            FadeTransform(intro_strip_2, intro_strip_3),
            FadeTransform(intro_harmonics_2, intro_harmonics_3),
            run_time=1.25,
        )
        self.wait(2.6)
        self.play(
            FadeOut(visual_title, shift=UP * 0.08),
            FadeOut(intro_formula_3, shift=UP * 0.08),
            FadeOut(intro_harmonics_3, shift=UP * 0.08),
            FadeOut(intro_strip_3, shift=UP * 0.08),
            FadeOut(z0_tag, shift=UP * 0.04),
            FadeOut(z0_emphasis, shift=UP * 0.04),
            FadeOut(intro_note, shift=UP * 0.04),
            run_time=1.2,
        )
        self.play(FadeIn(split_title, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(flat_visual_card, shift=RIGHT * 0.08), FadeIn(long_short_card, shift=LEFT * 0.08), run_time=1.35)
        self.play(Indicate(long_shift_note, color=ACCENT), run_time=1.15)
        self.play(
            AnimationGroup(
                *[
                    ShowPassingFlash(row[-1][0].copy().set_stroke(color=ACCENT, width=3.5))
                    for row in long_short_rows[1:]
                ],
                lag_ratio=0.16,
            ),
            run_time=1.6,
        )
        self.wait(5.4)

        # Phase 5: bridge to the next scene
        bridge_top = Text("So here is the deep-water choice I want to explain next", font_size=22, color=MUTED)
        bridge_mid = Tex(
            r"In deep water, Creamer first chooses to absorb only the cubic part $H_3$.",
            font_size=24,
            color=WHITE,
        )
        bridge_mid.set_color_by_tex(r"H_3", NONLINEAR)

        h_before = MathTex(r"H = H_2 + H_3 + H_4 + \cdots", font_size=34, color=WHITE)
        h_before.set_color_by_tex(r"H_3", NONLINEAR)
        h_arrow = Arrow(ORIGIN, RIGHT * 1.4, color=ACCENT, buff=0)
        h_arrow_label = Text("deep water", font_size=18, color=ACCENT)
        h_arrow_label.next_to(h_arrow, UP, buff=0.08)
        h_after = MathTex(r"K = H_2 + O(4)", font_size=34, color=TRANSFORMED)
        h_flow = VGroup(h_before, VGroup(h_arrow, h_arrow_label), h_after).arrange(RIGHT, buff=0.28, aligned_edge=DOWN)

        teaser = Tex(
            r"The cubic term is present, but in deep water it is not resonant.",
            font_size=21,
            color=ACCENT,
        )

        roadmap_1 = Tex(r"1. why is $H_3$ the first target?", font_size=22, color=WHITE)
        roadmap_2 = Tex(r"2. why does deep water make it non-resonant?", font_size=22, color=WHITE)
        roadmap_3 = Tex(r"3. only after that: what change of variables removes it?", font_size=22, color=WHITE)
        roadmap_1.set_color_by_tex(r"H_3", NONLINEAR)
        roadmap = VGroup(roadmap_1, roadmap_2, roadmap_3).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

        bridge_outro = Tex(
            r"So next I want to answer the first two questions before I bring in the canonical machinery.",
            font_size=19,
            color=MUTED,
        )

        o4_note = Text("O(4) = quartic and higher terms", font_size=18, color=MUTED)

        creamer_block = VGroup(
            bridge_top,
            bridge_mid,
            h_flow,
            teaser,
            roadmap,
            bridge_outro,
            o4_note,
        ).arrange(DOWN, buff=0.24)
        creamer_card = card(creamer_block, color=ACCENT, buff=0.32)
        creamer_card.move_to(DOWN * 0.25)

        self.play(
            FadeOut(split_title),
            FadeOut(flat_visual_card),
            FadeOut(long_short_card),
            run_time=1.2,
        )
        self.play(FadeIn(creamer_card, shift=UP * 0.15), run_time=1.35)
        self.wait(5.0)
