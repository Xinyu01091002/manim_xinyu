from manim import *
import numpy as np


WATER = ManimColor("#2E86AB")
SURFACE = ManimColor("#F6C85F")
BOTTOM = ManimColor("#6F4E37")
BOTTOM_HI = ManimColor("#D9A15F")
FREE = ManimColor("#4ECDC4")
BOUNDARY = ManimColor("#FF7A59")
SURFACE_HI = ManimColor("#FFE45E")
FREE_HI = ManimColor("#3CFFF1")
BOUNDARY_HI = ManimColor("#FF4D2E")
MUTED = GREY_B
PANEL = ManimColor("#1F2937")
BG = BLACK
PROGRESS_NAV_HEIGHT = 0.72


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


def fit_width(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def framed(mob, color=PANEL, buff=0.20, opacity=0.22):
    box = SurroundingRectangle(
        mob,
        color=color,
        buff=buff,
        corner_radius=0.08,
        stroke_width=1.5,
    ).set_fill(BLACK, opacity=opacity)
    return VGroup(box, mob)


def bottom_note(lines, color=FREE_HI, font_size=24):
    if isinstance(lines, str):
        lines = [lines]
    text = VGroup(*[Tex(line, font_size=font_size, color=WHITE) for line in lines])
    text.arrange(DOWN, buff=0.07, aligned_edge=LEFT)
    fit_width(text, config.frame_width - 1.0)
    card = framed(text, color=color, buff=0.17, opacity=0.30)
    card.to_edge(DOWN, buff=PROGRESS_NAV_HEIGHT + 0.15)
    return card


class LinearizationAndFirstWave(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("From small waves to the linear solution", font_size=34, weight=BOLD)
        subtitle = Text("derive the first-order problem, then solve it", font_size=22, color=MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.22)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)

        domain = self.build_domain()
        small_panel = self.small_parameter_panel()
        small_panel.to_edge(RIGHT, buff=0.48).shift(UP * 0.10)
        scale_marks = self.scale_marks(domain)
        note1 = bottom_note(
            [
                r"Use \(ka\ll1\) as the small parameter; keep finite depth through \(kh\).",
                r"Perturbation order: \(\phi^{(1)},\eta^{(1)},\phi^{(2)},\ldots\).",
            ],
            color=FREE_HI,
            font_size=23,
        )
        self.play(
            LaggedStart(
                Create(domain["water"]),
                Create(domain["bottom"]),
                Create(domain["still"]),
                Create(domain["surface"]),
                quiet_fade(domain["labels"]),
                quiet_fade(scale_marks),
                quiet_fade(small_panel),
                lag_ratio=0.10,
            ),
            quiet_fade(note1),
            run_time=1.6,
        )
        self.wait(4.0)

        self.play(
            FadeOut(VGroup(domain["water"], domain["bottom"], domain["still"], domain["surface"], domain["labels"])),
            FadeOut(scale_marks),
            FadeOut(small_panel),
            FadeOut(note1),
            FadeOut(title),
            FadeOut(subtitle),
            run_time=0.9,
        )

        operator_panel, operator_note = self.animate_combined_free_surface()
        self.wait(3.6)

        self.play(FadeOut(operator_panel), FadeOut(operator_note), run_time=0.45)
        first_order_panel, first_order_note = self.animate_order_collection()
        self.wait(3.8)

        self.play(FadeOut(first_order_panel), FadeOut(first_order_note), run_time=0.45)
        solve2, solve2_note = self.animate_laplace_solution()
        self.wait(3.5)

        final = self.final_solution_panel()
        final_note = bottom_note(
            r"Once \(\phi^{(1)}\) is known, Bernoulli reconstructs \(\eta^{(1)}\).",
            color=FREE_HI,
            font_size=22,
        )
        self.play(FadeOut(solve2), FadeOut(solve2_note), run_time=0.45)
        self.play(quiet_fade(final), quiet_fade(final_note), run_time=0.75)
        self.wait(5.0)

    def small_parameter_panel(self):
        heading = Text("Small parameter", font_size=31, color=WHITE, weight=BOLD)
        a_def = MathTex(r"a=\text{amplitude scale}", font_size=31, color=SURFACE_HI)
        k_def = MathTex(r"k=\frac{2\pi}{\lambda}", font_size=34, color=WHITE)
        eps = MathTex(r"\epsilon \sim ka \ll 1", font_size=42, color=FREE_HI)
        depth = MathTex(r"a/h\ll 1", font_size=36, color=FREE_HI)
        group = VGroup(heading, a_def, k_def, eps, depth).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        fit_width(group, 6.0)
        return framed(group, color=PANEL, buff=0.22, opacity=0.20)

    def free_surface_conditions_panel(self):
        heading = Text("Start from the two free-surface conditions", font_size=31, color=WHITE, weight=BOLD)
        kin = MathTex(r"\eta_t+\phi_x\eta_x-\phi_z=0", font_size=39, color=BOUNDARY_HI)
        kin_tag = MathTex(r"\Rightarrow\quad \eta_t=\phi_z-\phi_x\eta_x", font_size=37, color=BOUNDARY_HI)
        dyn = MathTex(r"\phi_t+\frac{1}{2}|\nabla\phi|^2+g\eta=0", font_size=39, color=SURFACE_HI)
        loc = MathTex(r"\text{all evaluated at } z=\eta(x,t)", font_size=31, color=MUTED)
        group = VGroup(heading, kin, kin_tag, dyn, loc).arrange(DOWN, buff=0.20)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.35)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def animate_combined_free_surface(self):
        heading = Text("Combine the free-surface conditions", font_size=36, color=WHITE, weight=BOLD)
        heading.to_edge(UP, buff=0.32)
        note = bottom_note(
            r"For higher order waves, first remove \(\eta_t\) and \(\eta_x\), leaving one equation for \(\phi\).",
            color=SURFACE_HI,
            font_size=22,
        )
        self.add(heading, note)

        def caption(text, color=WHITE):
            return Tex(text, font_size=32, color=color)

        dynamic_start = MathTex(
            r"D:\quad \phi_t+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)+g\eta=0",
            font_size=43,
            color=SURFACE_HI,
        )
        dynamic_name = Tex(
            r"\(D\): dynamic free-surface condition, from Bernoulli",
            font_size=28,
            color=SURFACE_HI,
        )
        kinematic_start = MathTex(
            r"K:\quad \eta_t=\phi_z-\phi_x\eta_x",
            font_size=43,
            color=BOUNDARY_HI,
        )
        kinematic_name = Tex(
            r"\(K\): kinematic free-surface condition, surface moves with the fluid",
            font_size=28,
            color=BOUNDARY_HI,
        )
        dynamic_block = VGroup(dynamic_name, dynamic_start).arrange(DOWN, buff=0.12)
        kinematic_block = VGroup(kinematic_name, kinematic_start).arrange(DOWN, buff=0.12)
        start_group = VGroup(dynamic_block, kinematic_block).arrange(DOWN, buff=0.32)
        fit_width(start_group, config.frame_width - 1.0)
        start_group.move_to(UP * 0.15)
        start_label = caption(r"start with the two free-surface boundary conditions", WHITE)
        start_label.next_to(start_group, UP, buff=0.36)
        loc0 = MathTex(r"z=\eta(x,t)", font_size=32, color=MUTED).next_to(start_group, DOWN, buff=0.28)
        self.play(
            FadeIn(start_label),
            FadeIn(dynamic_name),
            Write(dynamic_start),
            FadeIn(kinematic_name),
            Write(kinematic_start),
            FadeIn(loc0),
            run_time=1.3,
        )
        self.wait(1.2)

        why_title = Text("Differentiate Bernoulli on the surface", font_size=34, color=WHITE, weight=BOLD)
        why1 = MathTex(r"D(x,\eta(x,t),t)=0", font_size=43, color=SURFACE_HI)
        why2 = MathTex(r"\partial_t D(x,\eta,t)=0\quad\Rightarrow\quad \eta_t", font_size=40, color=BOUNDARY_HI)
        why3 = MathTex(r"K:\ \eta_t=\phi_z-\phi_x\eta_x", font_size=40, color=BOUNDARY_HI)
        why4 = MathTex(r"\partial_x D(x,\eta,t)=0\quad\Rightarrow\quad \eta_x", font_size=40, color=FREE_HI)
        why5 = MathTex(r"\text{then substitute to get one equation for }\phi", font_size=38, color=FREE_HI)
        why_group = VGroup(why_title, why1, why2, why3, why4, why5).arrange(DOWN, buff=0.18)
        fit_width(why_group, config.frame_width - 1.0)
        why_group.move_to(UP * 0.12)
        why_note = bottom_note(
            r"This is a surface chain-rule derivative of Bernoulli, not a new physical boundary condition.",
            color=FREE_HI,
            font_size=22,
        )
        self.play(
            FadeOut(start_label),
            FadeOut(dynamic_name),
            FadeOut(dynamic_start),
            FadeOut(kinematic_name),
            FadeOut(kinematic_start),
            FadeOut(loc0),
            FadeOut(note),
            run_time=0.35,
        )
        self.play(FadeIn(why_group), FadeIn(why_note), run_time=0.75)
        self.wait(2.2)

        note = bottom_note(
            r"Differentiate \(D(x,\eta(x,t),t)=0\): time gives \(\eta_t\), horizontal position gives \(\eta_x\).",
            color=SURFACE_HI,
            font_size=22,
        )

        dyn = MathTex(
            r"D:\quad \phi_t+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)+g\eta=0\quad (z=\eta)",
            font_size=40,
            color=SURFACE_HI,
        )
        kinetic_note = Tex(
            r"Keep the velocity-square term visible: it is where the nonlinear forcing comes from.",
            font_size=28,
            color=MUTED,
        )
        VGroup(dyn, kinetic_note).arrange(DOWN, buff=0.25).move_to(UP * 0.15)
        self.play(FadeOut(why_group), FadeOut(why_note), run_time=0.35)
        self.play(FadeIn(note), Write(dyn), FadeIn(kinetic_note), run_time=1.1)
        self.wait(1.0)

        dt_label = caption(r"Time derivative of \(D(x,\eta(x,t),t)=0\)", BOUNDARY_HI)
        dt_chain = MathTex(r"f(x,\eta,t)_t=f_t+f_z\eta_t", font_size=44, color=MUTED)
        dt_eq = MathTex(
            r"\phi_{tt}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_t"
            r"+\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\eta_t=0",
            font_size=39,
            color=WHITE,
        )
        fit_width(dt_eq, config.frame_width - 0.9)
        VGroup(dt_label, dt_chain, dt_eq).arrange(DOWN, buff=0.30).move_to(UP * 0.10)
        self.play(FadeOut(dyn), FadeOut(kinetic_note), FadeIn(dt_label), FadeIn(dt_chain), run_time=0.8)
        self.play(FadeIn(dt_eq), run_time=0.6)
        self.wait(1.3)

        kin = MathTex(r"K:\quad \eta_t=\phi_z-\phi_x\eta_x", font_size=43, color=BOUNDARY_HI)
        after_kin = MathTex(
            r"\phi_{tt}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_t"
            r"+\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]"
            r"\left(\phi_z-\phi_x\eta_x\right)=0",
            font_size=31,
            color=WHITE,
        )
        fit_width(after_kin, config.frame_width - 0.9)
        after_kin_split = MathTex(
            r"\cdots+\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\phi_z"
            r"-\phi_x\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\eta_x=0",
            font_size=34,
            color=WHITE,
        )
        fit_width(after_kin_split, config.frame_width - 0.9)
        VGroup(kin, after_kin, after_kin_split).arrange(DOWN, buff=0.24).move_to(UP * 0.08)
        note2 = bottom_note(
            r"Use \(K\) to replace \(\eta_t\). The remaining unknown surface-slope term is the part with \(\eta_x\).",
            color=BOUNDARY_HI,
            font_size=22,
        )
        self.play(FadeOut(note), FadeIn(note2), FadeOut(dt_label), FadeOut(dt_chain), FadeOut(dt_eq), FadeIn(kin), run_time=0.8)
        self.play(FadeIn(after_kin), run_time=0.55)
        self.play(FadeOut(after_kin), FadeIn(after_kin_split), run_time=0.55)
        self.wait(1.2)

        dx_label = caption(r"Horizontal derivative of \(D(x,\eta(x,t),t)=0\)", FREE_HI)
        dx_chain = MathTex(r"f(x,\eta,t)_x=f_x+f_z\eta_x", font_size=44, color=MUTED)
        dx_eq = MathTex(
            r"\phi_{tx}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_x"
            r"+\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\eta_x=0",
            font_size=36,
            color=FREE_HI,
        )
        fit_width(dx_eq, config.frame_width - 0.9)
        eta_x_eq = MathTex(
            r"\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\eta_x"
            r"=-\phi_{tx}-\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_x",
            font_size=36,
            color=FREE_HI,
        )
        fit_width(eta_x_eq, config.frame_width - 0.9)
        VGroup(dx_label, dx_eq, eta_x_eq, dx_chain).arrange(DOWN, buff=0.24).move_to(UP * 0.08)
        note_dx = bottom_note(
            r"The \(x\)-derivative of the same dynamic condition gives the missing relation for the \(\eta_x\) product.",
            color=FREE_HI,
            font_size=22,
        )
        self.play(FadeOut(kin), FadeOut(after_kin_split), FadeOut(note2), run_time=0.35)
        self.play(FadeIn(note_dx), FadeIn(dx_label), FadeIn(dx_chain), run_time=0.7)
        self.play(FadeIn(dx_eq), run_time=0.55)
        self.play(FadeIn(eta_x_eq), run_time=0.55)
        self.wait(1.2)

        source1 = MathTex(
            r"D_t+K:\quad \cdots-\phi_x\left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\eta_x=0",
            font_size=35,
            color=BOUNDARY_HI,
        )
        source2 = MathTex(
            r"D_x:\quad \left[\phi_{tz}+\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_z+g\right]\eta_x"
            r"=-\phi_{tx}-\frac{1}{2}\left(\phi_x^2+\phi_z^2\right)_x",
            font_size=34,
            color=FREE_HI,
        )
        source3 = MathTex(
            r"\Rightarrow\ -\phi_x(\cdots)\eta_x"
            r"=\phi_x\phi_{tx}+\frac{1}{2}\phi_x\left(\phi_x^2+\phi_z^2\right)_x",
            font_size=36,
            color=SURFACE_HI,
        )
        source_group = VGroup(source1, source2, source3).arrange(DOWN, buff=0.20).move_to(UP * 0.18)
        fit_width(source_group, config.frame_width - 0.9)
        self.play(FadeOut(dx_label), FadeOut(dx_eq), FadeOut(eta_x_eq), FadeOut(dx_chain), run_time=0.35)
        self.play(FadeIn(source1), FadeIn(source2), run_time=0.65)
        self.play(FadeIn(source3), run_time=0.5)
        self.wait(1.0)

        expanded = MathTex(
            r"\phi_{tt}+g\phi_z+\left(\phi_x^2+\phi_z^2\right)_t"
            r"+\frac{1}{2}\left[\phi_x\left(\phi_x^2+\phi_z^2\right)_x"
            r"+\phi_z\left(\phi_x^2+\phi_z^2\right)_z\right]=0",
            font_size=35,
            color=WHITE,
        )
        compact = MathTex(
            r"\phi_{tt}+g\phi_z+\left[\partial_t+\frac{1}{2}\left(\phi_x\partial_x+\phi_z\partial_z\right)\right]"
            r"\left(\phi_x^2+\phi_z^2\right)=0",
            font_size=37,
            color=FREE_HI,
        )
        final_loc = MathTex(r"z=\eta(x,t)", font_size=32, color=MUTED)
        final_group = VGroup(expanded, compact, final_loc).arrange(DOWN, buff=0.26)
        fit_width(final_group, config.frame_width - 0.9)
        final_group.move_to(UP * 0.08)
        final_label = caption(r"substitute the \(\eta_x\) product, then collect the velocity-square derivatives", FREE_HI)
        final_label.next_to(final_group, UP, buff=0.24)
        self.play(FadeOut(source_group), FadeOut(note_dx), FadeIn(final_label), FadeIn(expanded), run_time=0.7)
        self.play(FadeIn(compact), FadeIn(final_loc), run_time=0.7)
        final_note = bottom_note(
            r"The nonlinear velocity-square term survives as time, horizontal, and vertical derivative pieces.",
            color=FREE_HI,
            font_size=22,
        )
        self.play(FadeIn(final_note), run_time=0.35)
        self.wait(1.5)

        combined = MathTex(
            r"\phi_{tt}+g\phi_z+\left[\partial_t+\frac{1}{2}\left(\phi_x\partial_x+\phi_z\partial_z\right)\right]\left(\phi_x^2+\phi_z^2\right)=0",
            font_size=38,
            color=FREE_HI,
        )
        fit_width(combined, config.frame_width - 0.80)
        combined.move_to(UP * 0.00)
        combined_loc = MathTex(r"z=\eta(x,t)", font_size=30, color=MUTED).next_to(combined, DOWN, buff=0.16)
        self.play(FadeOut(final_label), FadeOut(expanded), FadeOut(compact), FadeOut(final_loc), run_time=0.4)
        title_combined = caption(r"combined kinematic + dynamic free-surface condition", FREE_HI)
        title_combined.next_to(combined, UP, buff=0.30)
        self.play(Write(combined), FadeIn(combined_loc), FadeIn(title_combined), run_time=1.0)
        self.wait(1.1)

        order_intro = VGroup(
            Text("Perturbation-order notation", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\cdots", font_size=42, color=FREE_HI),
            MathTex(r"\eta=\epsilon\eta^{(1)}+\epsilon^2\eta^{(2)}+\cdots", font_size=42, color=SURFACE_HI),
            MathTex(r"(n)\text{ means order }n,\quad \text{not a power}", font_size=38, color=WHITE),
        ).arrange(DOWN, buff=0.24)
        fit_width(order_intro, config.frame_width - 1.0)
        order_intro.move_to(UP * 0.12)
        order_note = bottom_note(
            r"So \(\phi^{(2)}\) is the second correction to the potential, not \(\phi\) squared.",
            color=FREE_HI,
            font_size=22,
        )
        self.play(FadeOut(combined), FadeOut(combined_loc), FadeOut(title_combined), FadeOut(final_note), run_time=0.35)
        self.play(FadeIn(order_intro), FadeIn(order_note), run_time=0.7)
        self.wait(1.5)

        note3 = bottom_note(
            r"This is still nonlinear and still lives on the unknown free surface \(z=\eta\).",
            color=FREE_HI,
            font_size=22,
        )
        advantage = VGroup(
            Text("Advantage for higher order", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\phi^{(n)}_{tt}+g\phi^{(n)}_z=\mathcal{N}^{(n)}_{\rm known}", font_size=38, color=BOUNDARY_HI),
            MathTex(r"\mathcal{N}^{(n)}_{\rm known}\leftarrow \phi^{(1:n-1)},\ \eta^{(1:n-1)}", font_size=35, color=MUTED),
            MathTex(r"\text{solve for }\phi^{(n)}", font_size=35, color=WHITE),
            MathTex(r"\eta^{(n)}=-\frac{1}{g}\phi^{(n)}_t\big|_{z=0}+\text{known terms}", font_size=34, color=SURFACE_HI),
            MathTex(r"\text{recover }\eta^{(n)}\text{ from Bernoulli}", font_size=33, color=WHITE),
        ).arrange(DOWN, buff=0.22)
        fit_width(advantage, config.frame_width - 1.0)
        advantage.move_to(UP * 0.25)
        panel = framed(advantage, color=PANEL, buff=0.24, opacity=0.20)
        self.play(FadeOut(order_intro), FadeOut(order_note), FadeOut(heading), run_time=0.45)
        self.play(FadeIn(panel), FadeIn(note3), run_time=0.75)
        return panel, note3

    def combination_derivation_panel(self):
        heading = Text("Differentiate Bernoulli", font_size=32, color=WHITE, weight=BOLD)
        moving = MathTex(
            r"\frac{d}{dt}q(x,\eta,t)=q_t+\eta_t q_z",
            font_size=37,
            color=WHITE,
        )
        substitute = MathTex(
            r"\eta_t=\phi_z-\phi_x\eta_x",
            font_size=38,
            color=BOUNDARY_HI,
        )
        remove_eta_x = MathTex(
            r"\partial_x\!\left(\phi_t+\frac{1}{2}|\nabla\phi|^2+g\eta\right)=0",
            font_size=33,
            color=SURFACE_HI,
        )
        result = MathTex(
            r"\phi_{tt}+g\phi_z+\left[\partial_t+\frac{1}{2}(\phi_x\partial_x+\phi_z\partial_z)\right](\phi_x^2+\phi_z^2)=0",
            font_size=28,
            color=FREE_HI,
        )
        loc = MathTex(r"\text{still evaluated on } z=\eta", font_size=30, color=MUTED)
        group = VGroup(heading, moving, substitute, remove_eta_x, result, loc).arrange(DOWN, buff=0.16)
        fit_width(group, config.frame_width - 0.9)
        group.move_to(UP * 0.28)
        # Rebuild arrows after group placement.
        arrows = VGroup(
            Arrow(moving.get_bottom(), result.get_top() + LEFT * 2.3, color=WHITE, buff=0.08, stroke_width=2.7),
            Arrow(substitute.get_bottom(), result.get_top(), color=BOUNDARY_HI, buff=0.08, stroke_width=2.7),
            Arrow(remove_eta_x.get_bottom(), result.get_top() + RIGHT * 2.2, color=SURFACE_HI, buff=0.08, stroke_width=2.7),
        )
        return framed(VGroup(group, arrows), color=PANEL, buff=0.22, opacity=0.20)

    def operator_panel(self):
        heading = Text("Combined condition", font_size=33, color=WHITE, weight=BOLD)
        op = MathTex(r"\phi_{tt}+g\phi_z", font_size=43, color=FREE_HI)
        hierarchy = MathTex(r"\phi^{(n)}_{tt}+g\phi^{(n)}_z=\text{known lower-order terms}", font_size=37, color=BOUNDARY_HI)
        phi_only = MathTex(r"\text{unknown in this equation: }\phi^{(n)}", font_size=33, color=WHITE)
        forcing = MathTex(r"\text{the right-hand side is known from orders }1,\ldots,n-1", font_size=30, color=MUTED)
        eta_after = MathTex(r"\eta^{(n)}\ \text{is reconstructed afterward from Bernoulli}", font_size=32, color=SURFACE_HI)
        group = VGroup(heading, op, hierarchy, phi_only, forcing, eta_after).arrange(DOWN, buff=0.18)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.25)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def taylor_panel(self):
        heading = Text("Move the equation to z = 0", font_size=33, color=WHITE, weight=BOLD)
        boundary = MathTex(r"\mathcal{B}(\phi,\eta)\big|_{z=\eta}=0", font_size=43, color=BOUNDARY_HI)
        expansion = MathTex(
            r"\mathcal{B}\big|_{0}+\eta\,\partial_z\mathcal{B}\big|_{0}+\frac{1}{2}\eta^2\partial_{zz}\mathcal{B}\big|_{0}+\cdots=0",
            font_size=35,
            color=SURFACE_HI,
        )
        takeaway = MathTex(r"\text{now every term is evaluated at the known level } z=0", font_size=32, color=WHITE)
        group = VGroup(heading, boundary, expansion, takeaway).arrange(DOWN, buff=0.25)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.25)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def animate_order_collection(self):
        heading = Text("Collect the first order", font_size=36, color=WHITE, weight=BOLD)
        heading.move_to(UP * 2.35)

        note = bottom_note(
            [
                r"Taylor expand the free-surface equation from \(z=\eta\) to \(z=0\).",
                r"Then keep the terms proportional to \(\epsilon\).",
            ],
            color=SURFACE_HI,
            font_size=21,
        )
        self.add(heading, note)

        ckfsbc = MathTex(
            r"\left[\phi_{tt}+g\phi_z+\left(\partial_t+\frac{1}{2}(\phi_x\partial_x+\phi_z\partial_z)\right)(\phi_x^2+\phi_z^2)\right]_{z=\eta}=0",
            font_size=36,
            color=BOUNDARY_HI,
        )
        fit_width(ckfsbc, config.frame_width - 0.65)
        ckfsbc.move_to(UP * 0.85)
        self.play(FadeIn(ckfsbc), run_time=0.7)
        self.wait(1.0)

        dingemans = MathTex(
            r"\sum_{m=0}^{\infty}\frac{\eta^m}{m!}\partial_z^m"
            r"\left\{\phi_{tt}+g\phi_z+\left(\partial_t+\frac{1}{2}(\phi_x\partial_x+\phi_z\partial_z)\right)(\phi_x^2+\phi_z^2)\right\}_{z=0}=0",
            font_size=34,
            color=FREE_HI,
        )
        fit_width(dingemans, config.frame_width - 0.75)
        dingemans.move_to(UP * 0.32)
        self.play(FadeOut(ckfsbc), FadeIn(dingemans), run_time=0.75)
        self.wait(1.0)

        taylor0 = MathTex(
            r"m=0:\quad \left\{\phi_{tt}+g\phi_z+\left(\partial_t+\frac{1}{2}(\phi_x\partial_x+\phi_z\partial_z)\right)(\phi_x^2+\phi_z^2)\right\}_{0}",
            font_size=33,
            color=FREE_HI,
        )
        taylor1 = MathTex(
            r"m=1:\quad \eta\,\partial_z\left\{\phi_{tt}+g\phi_z+\left(\partial_t+\frac{1}{2}(\phi_x\partial_x+\phi_z\partial_z)\right)(\phi_x^2+\phi_z^2)\right\}_{0}",
            font_size=32,
            color=SURFACE_HI,
        )
        taylor2 = MathTex(
            r"m=2:\quad \frac{1}{2}\eta^2\,\partial_{zz}\left\{\cdots\right\}_{0}",
            font_size=36,
            color=MUTED,
        )
        taylor_rows = VGroup(taylor0, taylor1, taylor2).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        fit_width(taylor_rows, config.frame_width - 0.85)
        taylor_rows.move_to(UP * 0.15)
        self.play(FadeOut(dingemans), run_time=0.35)
        self.play(FadeIn(taylor0), run_time=0.45)
        self.play(FadeIn(taylor1), run_time=0.45)
        self.play(FadeIn(taylor2), run_time=0.35)
        self.wait(1.2)

        visible_orders = VGroup(
            MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\cdots,\qquad \eta=\epsilon\eta^{(1)}+\epsilon^2\eta^{(2)}+\cdots", font_size=35, color=WHITE),
            MathTex(r"\phi_{tt}+g\phi_z:\quad O(\epsilon),\ O(\epsilon^2),\ldots", font_size=38, color=FREE_HI),
            MathTex(r"\eta\,\partial_z\{\cdots\}_{0}\quad\text{and}\quad(\phi_x^2+\phi_z^2):\quad O(\epsilon^2)\text{ or higher}", font_size=33, color=SURFACE_HI),
        ).arrange(DOWN, buff=0.18)
        fit_width(visible_orders, config.frame_width - 0.9)
        visible_orders.move_to(UP * 0.32)
        self.play(FadeOut(taylor_rows), run_time=0.4)
        self.play(FadeIn(visible_orders[0]), run_time=0.45)
        self.play(FadeIn(visible_orders[1]), FadeIn(visible_orders[2]), run_time=0.55)
        self.wait(1.6)
        self.play(FadeOut(visible_orders), run_time=0.45)

        row1 = MathTex(
            r"O(\epsilon):\quad \epsilon\left(\phi^{(1)}_{tt}+g\phi^{(1)}_z\right)_{z=0}",
            font_size=40,
            color=FREE_HI,
        )
        row2 = VGroup(
            MathTex(
                r"O(\epsilon^2):\quad \epsilon^2\left(\phi^{(2)}_{tt}+g\phi^{(2)}_z\right.",
                font_size=36,
                color=SURFACE_HI,
            ),
            MathTex(
                r"\left.+\eta^{(1)}(\phi^{(1)}_{ttz}+g\phi^{(1)}_{zz})+\text{velocity-square terms}\right)_{z=0}",
                font_size=34,
                color=SURFACE_HI,
            ),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        row2[1].shift(RIGHT * 0.48)
        fit_width(row2, config.frame_width - 1.0)
        row2.set_color(SURFACE_HI)
        row3 = MathTex(
            r"O(\epsilon^3):\quad \epsilon^3(\cdots)",
            font_size=36,
            color=MUTED,
        )
        order_rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        fit_width(order_rows, config.frame_width - 1.0)
        order_rows.move_to(UP * 0.15)
        self.play(FadeIn(row1), FadeIn(row2), FadeIn(row3), run_time=0.65)
        self.wait(2.0)

        first_order_surface = MathTex(
            r"\phi^{(1)}_{tt}+g\phi^{(1)}_z=0\qquad z=0",
            font_size=42,
            color=BOUNDARY_HI,
        )
        first_order_surface.move_to(UP * 0.15)
        self.play(
            row2.animate.set_opacity(0.15),
            row3.animate.set_opacity(0.10),
            row1.animate.set_color(BOUNDARY_HI).scale(1.05),
            run_time=0.8,
        )
        self.play(FadeOut(row2), FadeOut(row3), Transform(row1, first_order_surface), run_time=0.8)
        self.wait(1.2)

        bulk = MathTex(
            r"\epsilon(\phi^{(1)}_{xx}+\phi^{(1)}_{zz})+\epsilon^2(\phi^{(2)}_{xx}+\phi^{(2)}_{zz})+\cdots=0",
            font_size=33,
            color=WHITE,
        )
        bottom = MathTex(
            r"\epsilon\phi^{(1)}_z+\epsilon^2\phi^{(2)}_z+\cdots=0\qquad z=-h",
            font_size=33,
            color=WHITE,
        )
        bulk.next_to(first_order_surface, DOWN, buff=0.35)
        bottom.next_to(bulk, DOWN, buff=0.20)
        self.play(Write(bulk), Write(bottom), run_time=1.2)
        self.wait(1.4)

        first_bulk = MathTex(r"\phi^{(1)}_{xx}+\phi^{(1)}_{zz}=0\qquad -h<z<0", font_size=40, color=FREE_HI)
        first_bottom = MathTex(r"\phi^{(1)}_z=0\qquad z=-h", font_size=40, color=BOTTOM)
        final_surface = MathTex(r"\phi^{(1)}_{tt}+g\phi^{(1)}_z=0\qquad z=0", font_size=40, color=BOUNDARY_HI)
        eta = MathTex(r"\eta^{(1)}=-\frac{1}{g}\phi^{(1)}_t\qquad z=0", font_size=40, color=SURFACE_HI)
        first_group = VGroup(first_bulk, first_bottom, final_surface, eta).arrange(DOWN, buff=0.22)
        first_group.move_to(UP * 0.25)
        panel = framed(first_group, color=PANEL, buff=0.24, opacity=0.20)

        final_note = bottom_note(
            r"Remove \(O(\epsilon^2)\) and higher terms: the first-order problem is homogeneous.",
            color=BOUNDARY_HI,
            font_size=22,
        )
        self.play(
            FadeOut(row1),
            FadeOut(bulk),
            FadeOut(bottom),
            FadeOut(note),
            run_time=0.45,
        )
        self.play(
            FadeIn(panel[0]),
            FadeIn(first_group),
            FadeIn(final_note),
            run_time=0.75,
        )
        self.remove(heading)
        return panel, final_note

    def expansion_panel(self):
        heading = Text("Insert the perturbation series", font_size=33, color=WHITE, weight=BOLD)
        eta = MathTex(r"\eta=\epsilon\eta^{(1)}+\epsilon^2\eta^{(2)}+\epsilon^3\eta^{(3)}+\cdots", font_size=40, color=SURFACE_HI)
        phi = MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\epsilon^3\phi^{(3)}+\cdots", font_size=40, color=FREE_HI)
        collect1 = MathTex(r"O(\epsilon):\quad \phi^{(1)}_{tt}+g\phi^{(1)}_z=0", font_size=42, color=WHITE)
        collect2 = MathTex(r"O(\epsilon^2):\quad \phi^{(2)}_{tt}+g\phi^{(2)}_z=\text{known forcing}", font_size=36, color=MUTED)
        group = VGroup(heading, eta, phi, collect1, collect2).arrange(DOWN, buff=0.22)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.20)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def first_order_panel(self):
        heading = Text("First order: the homogeneous problem", font_size=33, color=WHITE, weight=BOLD)
        laplace = MathTex(r"\phi^{(1)}_{xx}+\phi^{(1)}_{zz}=0,\qquad -h<z<0", font_size=39, color=FREE_HI)
        bottom = MathTex(r"\phi^{(1)}_z=0,\qquad z=-h", font_size=39, color=BOTTOM)
        surface = MathTex(r"\phi^{(1)}_{tt}+g\phi^{(1)}_z=0,\qquad z=0", font_size=39, color=BOUNDARY_HI)
        eta = MathTex(r"\eta^{(1)}=-\frac{1}{g}\phi^{(1)}_t,\qquad z=0", font_size=39, color=SURFACE_HI)
        group = VGroup(heading, laplace, bottom, surface, eta).arrange(DOWN, buff=0.21)
        fit_width(group, config.frame_width - 1.1)
        group.move_to(UP * 0.20)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def animate_laplace_solution(self):
        heading = Text("Solve Laplace's equation", font_size=36, color=WHITE, weight=BOLD)
        heading.to_edge(UP, buff=0.32)
        note = bottom_note(
            r"Use the wave phase horizontally; Laplace's equation then decides the vertical shape.",
            color=FREE_HI,
            font_size=22,
        )
        self.add(heading, note)

        laplace = MathTex(r"\phi^{(1)}_{xx}+\phi^{(1)}_{zz}=0", font_size=54, color=FREE_HI)
        ansatz_label = Tex(r"try one travelling phase, leave the vertical shape unknown", font_size=28, color=WHITE)
        ansatz = MathTex(r"\phi^{(1)}=X(z)\sin\theta,\qquad \theta=kx-\omega t", font_size=44, color=SURFACE_HI)
        VGroup(laplace, ansatz_label, ansatz).arrange(DOWN, buff=0.34).move_to(UP * 0.25)
        self.play(Write(laplace), run_time=0.8)
        self.play(FadeIn(ansatz_label), Write(ansatz), run_time=1.0)
        self.wait(1.1)

        dx_label = Tex(r"horizontal derivative: the phase contributes \(k\)", font_size=28, color=SURFACE_HI)
        dx = MathTex(r"\phi^{(1)}_{xx}=-k^2X(z)\sin\theta", font_size=46, color=SURFACE_HI)
        dz_label = Tex(r"vertical derivative: only \(X(z)\) changes", font_size=28, color=FREE_HI)
        dz = MathTex(r"\phi^{(1)}_{zz}=X''(z)\sin\theta", font_size=46, color=FREE_HI)
        derivatives = VGroup(dx_label, dx, dz_label, dz).arrange(DOWN, buff=0.24)
        derivatives.move_to(UP * 0.20)
        self.play(FadeOut(laplace), FadeOut(ansatz_label), ansatz.animate.to_edge(UP, buff=0.95).scale(0.88), run_time=0.55)
        self.play(FadeIn(dx_label), Write(dx), run_time=0.9)
        self.play(FadeIn(dz_label), Write(dz), run_time=0.9)
        self.wait(1.1)

        combine = MathTex(
            r"\left(-k^2X+X''\right)\sin\theta=0",
            font_size=48,
            color=WHITE,
        )
        reason = Tex(r"this must hold for every \(x,t\), so the bracket must vanish", font_size=28, color=MUTED)
        ode = MathTex(r"X''-k^2X=0", font_size=58, color=WHITE)
        VGroup(combine, reason, ode).arrange(DOWN, buff=0.30).move_to(UP * 0.10)
        self.play(FadeOut(dx_label), FadeOut(dx), FadeOut(dz_label), FadeOut(dz), FadeOut(ansatz), Write(combine), run_time=0.9)
        self.play(FadeIn(reason), run_time=0.5)
        self.play(Write(ode), run_time=0.7)
        self.wait(1.2)

        note_bottom = bottom_note(
            r"Choose the vertical origin as \(z+h\), so the bottom boundary is easy to apply.",
            color=BOTTOM_HI,
            font_size=22,
        )
        general = MathTex(
            r"X=A\cosh k(z+h)+B\sinh k(z+h)",
            font_size=44,
            color=FREE_HI,
        )
        derivative = MathTex(
            r"X'=kA\sinh k(z+h)+kB\cosh k(z+h)",
            font_size=40,
            color=WHITE,
        )
        VGroup(general, derivative).arrange(DOWN, buff=0.32).move_to(UP * 0.35)
        self.play(FadeOut(note), FadeIn(note_bottom), FadeOut(combine), FadeOut(reason), TransformMatchingTex(ode, general), run_time=0.9)
        self.play(Write(derivative), run_time=0.9)
        self.wait(0.9)

        bottom = MathTex(r"z=-h:\qquad X'(-h)=kB=0", font_size=48, color=BOTTOM_HI)
        kill_b = MathTex(r"B=0", font_size=58, color=BOTTOM_HI)
        vertical_shape = MathTex(r"X=A\cosh k(z+h)", font_size=52, color=FREE_HI)
        VGroup(bottom, kill_b, vertical_shape).arrange(DOWN, buff=0.28).move_to(UP * 0.05)
        self.play(FadeOut(general), FadeOut(derivative), Write(bottom), run_time=0.8)
        self.play(Write(kill_b), run_time=0.55)
        self.play(Write(vertical_shape), run_time=0.75)
        self.wait(1.1)

        note_surface = bottom_note(
            r"Now use the linear free-surface condition to connect \(\omega\), \(k\), and \(h\).",
            color=BOUNDARY_HI,
            font_size=22,
        )
        phi_result = MathTex(
            r"\phi^{(1)}=A\cosh k(z+h)\sin\theta",
            font_size=48,
            color=FREE_HI,
        )
        phi_tt = MathTex(r"\phi^{(1)}_{tt}=-\omega^2A\cosh k(z+h)\sin\theta", font_size=38, color=SURFACE_HI)
        phi_z = MathTex(r"\phi^{(1)}_z=Ak\sinh k(z+h)\sin\theta", font_size=38, color=BOUNDARY_HI)
        VGroup(phi_result, phi_tt, phi_z).arrange(DOWN, buff=0.26).move_to(UP * 0.20)
        self.play(FadeOut(note_bottom), FadeIn(note_surface), FadeOut(bottom), FadeOut(kill_b), TransformMatchingTex(vertical_shape, phi_result), run_time=0.9)
        self.play(Write(phi_tt), run_time=0.85)
        self.play(Write(phi_z), run_time=0.85)
        self.wait(1.1)

        surface = MathTex(r"z=0:\qquad \phi^{(1)}_{tt}+g\phi^{(1)}_z=0", font_size=44, color=BOUNDARY_HI)
        substitution = MathTex(r"-\omega^2A\cosh(kh)+gAk\sinh(kh)=0", font_size=42, color=WHITE)
        divide = MathTex(r"\omega^2=gk\frac{\sinh(kh)}{\cosh(kh)}", font_size=46, color=WHITE)
        dispersion = MathTex(r"\omega^2=gk\tanh(kh)", font_size=56, color=WHITE)
        VGroup(surface, substitution, divide, dispersion).arrange(DOWN, buff=0.22).move_to(UP * 0.05)
        self.play(FadeOut(phi_result), FadeOut(phi_tt), FadeOut(phi_z), Write(surface), run_time=0.8)
        self.play(Write(substitution), run_time=0.85)
        self.play(Write(divide), run_time=0.75)
        self.play(TransformMatchingTex(divide.copy(), dispersion), run_time=0.85)
        self.wait(1.2)

        final_phi = MathTex(
            r"\phi^{(1)}=A\cosh k(z+h)\sin\theta",
            font_size=43,
            color=FREE_HI,
        )
        final_dispersion = MathTex(r"\omega^2=gk\tanh(kh)", font_size=50, color=WHITE)
        group = VGroup(final_phi, final_dispersion).arrange(DOWN, buff=0.30)
        group.move_to(UP * 0.25)
        panel = framed(group, color=PANEL, buff=0.24, opacity=0.20)
        final_note = bottom_note(
            r"The finite-depth dispersion relation appears when the surface condition is applied.",
            color=BOUNDARY_HI,
            font_size=22,
        )
        self.play(
            FadeOut(heading),
            FadeOut(note_surface),
            FadeOut(surface),
            FadeOut(substitution),
            FadeOut(divide),
            FadeOut(dispersion),
            FadeIn(panel),
            FadeIn(final_note),
            run_time=0.85,
        )
        return panel, final_note

    def solve_laplace_panel(self):
        heading = Text("Solve Laplace's equation", font_size=33, color=WHITE, weight=BOLD)
        guess = Tex(r"Guess the wave phase first:", font_size=28, color=WHITE)
        ansatz = MathTex(r"\phi^{(1)}=X(z)\sin(kx-\omega t)", font_size=40, color=FREE_HI)
        reduce = Tex(r"Substitute into Laplace's equation:", font_size=28, color=WHITE)
        into_pde = MathTex(
            r"\phi^{(1)}_{xx}+\phi^{(1)}_{zz}=(-k^2X+X'')\sin(kx-\omega t)=0",
            font_size=32,
            color=WHITE,
        )
        ode = MathTex(r"X''-k^2X=0", font_size=45, color=WHITE)
        general = MathTex(r"X=A\cosh k(z+h)+B\sinh k(z+h)", font_size=38, color=FREE_HI)
        bottom = MathTex(r"X'(-h)=0\quad\Rightarrow\quad B=0", font_size=41, color=BOTTOM)
        result = MathTex(r"\phi^{(1)}=A\cosh k(z+h)\sin(kx-\omega t)", font_size=37, color=FREE_HI)
        group = VGroup(heading, guess, ansatz, reduce, into_pde, ode, general, bottom, result).arrange(DOWN, buff=0.09)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.20)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def apply_boundary_panel(self):
        heading = Text("Use the free-surface operator", font_size=33, color=WHITE, weight=BOLD)
        surface = MathTex(r"\phi^{(1)}_{tt}+g\phi^{(1)}_z=0\quad \text{at } z=0", font_size=40, color=BOUNDARY_HI)
        substitute = MathTex(r"-\omega^2 A\cosh(kh)+gAk\sinh(kh)=0", font_size=39, color=WHITE)
        divide = MathTex(r"\omega^2=gk\,\frac{\sinh(kh)}{\cosh(kh)}", font_size=40, color=FREE_HI)
        final = MathTex(r"\boxed{\omega^2=gk\tanh(kh)}", font_size=46, color=WHITE)
        group = VGroup(heading, surface, substitute, divide, final).arrange(DOWN, buff=0.23)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.22)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def final_solution_panel(self):
        heading = Text("First-order finite-depth solution", font_size=33, color=WHITE, weight=BOLD)
        theta = MathTex(r"\theta=kx-\omega t", font_size=39, color=WHITE)
        phi = MathTex(
            r"\phi^{(1)}=\frac{a\omega}{k\sinh(kh)}\cosh k(z+h)\sin\theta",
            font_size=36,
            color=FREE_HI,
        )
        eta_from_phi = MathTex(r"\eta^{(1)}=-\frac{1}{g}\phi^{(1)}_t\big|_{z=0}", font_size=38, color=SURFACE_HI)
        eta = MathTex(r"\eta^{(1)}=a\cos\theta", font_size=44, color=SURFACE_HI)
        disp = MathTex(r"\omega^2=gk\tanh(kh)", font_size=42, color=WHITE)
        group = VGroup(heading, theta, phi, eta_from_phi, eta, disp).arrange(DOWN, buff=0.15)
        fit_width(group, config.frame_width - 1.0)
        group.move_to(UP * 0.23)
        return framed(group, color=PANEL, buff=0.24, opacity=0.20)

    def build_domain(self):
        left = -6.35
        right = -0.80
        z0 = 0.42
        bottom_y = -1.95
        amp = 0.18
        xs = np.linspace(left, right, 160)
        length = right - left
        top_points = [[x, z0 + amp * np.sin(2 * PI * (x - left) / length), 0] for x in xs]
        fill_points = top_points + [[right, bottom_y, 0], [left, bottom_y, 0]]
        water = Polygon(*fill_points, stroke_width=0, fill_color=WATER, fill_opacity=0.34)
        surface = VMobject(color=SURFACE, stroke_width=4.0).set_points_smoothly(top_points)
        still = DashedLine([left, z0, 0], [right, z0, 0], color=MUTED, stroke_width=1.6, dash_length=0.10)
        bottom = Line([left, bottom_y, 0], [right, bottom_y, 0], color=BOTTOM, stroke_width=5.0)
        eta_label = MathTex(r"z=\eta(x,t)", font_size=26, color=SURFACE).next_to(surface, UP, buff=0.15)
        still_label = MathTex(r"z=0", font_size=25, color=MUTED).next_to(still, RIGHT, buff=0.12)
        bottom_label = MathTex(r"z=-h", font_size=24, color=BOTTOM).next_to(bottom, UP, buff=0.08)
        labels = VGroup(eta_label, still_label, bottom_label)
        return {
            "water": water,
            "surface": surface,
            "still": still,
            "bottom": bottom,
            "labels": labels,
            "left": left,
            "right": right,
            "z0": z0,
            "bottom_y": bottom_y,
        }

    def scale_marks(self, domain):
        crest = domain["surface"].get_top()
        still_y = domain["z0"]
        amp_arrow = DoubleArrow(
            [domain["left"] + 1.25, still_y, 0],
            [domain["left"] + 1.25, crest[1], 0],
            color=SURFACE_HI,
            stroke_width=2.6,
            buff=0.02,
            max_tip_length_to_length_ratio=0.22,
        )
        amp_label = MathTex("a", font_size=26, color=SURFACE_HI).next_to(amp_arrow, LEFT, buff=0.08)
        depth_arrow = DoubleArrow(
            [domain["left"] + 0.40, still_y, 0],
            [domain["left"] + 0.40, domain["bottom_y"], 0],
            color=FREE_HI,
            stroke_width=2.6,
            buff=0.02,
            max_tip_length_to_length_ratio=0.08,
        )
        depth_label = MathTex("h", font_size=26, color=FREE_HI).next_to(depth_arrow, LEFT, buff=0.08)
        wavelength = DoubleArrow(
            [domain["left"] + 0.75, domain["z0"] + 0.62, 0],
            [domain["right"] - 0.75, domain["z0"] + 0.62, 0],
            color=MUTED,
            stroke_width=2.2,
            buff=0.02,
            max_tip_length_to_length_ratio=0.05,
        )
        wavelength_label = MathTex(r"\lambda=2\pi/k", font_size=25, color=MUTED).next_to(wavelength, UP, buff=0.06)
        return VGroup(amp_arrow, amp_label, depth_arrow, depth_label, wavelength, wavelength_label)
