from manim import *
import numpy as np


WATER = ManimColor("#2E86AB")
SURFACE = ManimColor("#F6C85F")
BOTTOM = ManimColor("#6F4E37")
FREE = ManimColor("#4ECDC4")
BOUNDARY = ManimColor("#FF7A59")
SURFACE_HI = ManimColor("#FFE45E")
FREE_HI = ManimColor("#3CFFF1")
BOUNDARY_HI = ManimColor("#FF4D2E")
BOTTOM_HI = ManimColor("#D9A066")
MUTED = GREY_B
PANEL = ManimColor("#1F2937")
BG = BLACK
PROGRESS_NAV_HEIGHT = 0.72
NAV_SAFE_BUFF = 0.16


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


def fit_width(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def equation_row(tex, note, color=WHITE, note_color=MUTED):
    eq = MathTex(tex, font_size=30, color=color)
    note_mob = Text(note, font_size=18, color=note_color)
    row = VGroup(eq, note_mob).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    return row


def label(text, font_size=20, color=WHITE):
    return Text(text, font_size=font_size, color=color)


def note_card(lines, color, max_width=5.8):
    if isinstance(lines, str):
        lines = [lines]
    text = VGroup(*[Text(line, font_size=19, color=WHITE) for line in lines])
    text.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    fit_width(text, max_width)
    box = SurroundingRectangle(
        text,
        color=color,
        buff=0.14,
        corner_radius=0.08,
        stroke_width=1.8,
    ).set_fill(BLACK, opacity=0.30)
    return VGroup(box, text)


def move_above_nav(mob, buff=NAV_SAFE_BUFF):
    min_y = -config.frame_height / 2 + PROGRESS_NAV_HEIGHT + buff
    mob.shift(UP * max(0, min_y - mob.get_bottom()[1]))
    return mob


class FiniteDepthProblemSetup(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("The finite-depth free-surface problem", font_size=35, weight=BOLD)
        subtitle = Text(
            "governing equation and boundary conditions",
            font_size=22,
            color=MUTED,
        )
        VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.22)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)

        domain = self.build_domain()
        equations = self.build_equation_panel()

        self.play(
            LaggedStart(
                Create(domain["water_fill"]),
                Create(domain["bottom"]),
                Create(domain["still"]),
                Create(domain["surface"]),
                lag_ratio=0.18,
            ),
            run_time=1.8,
        )
        self.play(
            LaggedStart(
                quiet_fade(domain["labels"]),
                quiet_fade(domain["potential"]),
                quiet_fade(domain["assumptions"]),
                lag_ratio=0.18,
            ),
            run_time=1.0,
        )
        self.wait(1.2)

        panel_bg = equations["background"]
        self.play(quiet_fade(panel_bg), quiet_fade(equations["heading"]), run_time=1.0)

        interior_shade = domain["water_body"].copy()
        interior_shade.set_fill(FREE_HI, opacity=0.22)
        interior_shade.set_stroke(FREE_HI, width=3.5, opacity=1.0)
        interior_note = note_card(
            [
                "Mass conservation for incompressible potential flow:",
                "div(u,w)=0 and (u,w)=grad phi, so phi is harmonic inside.",
            ],
            FREE_HI,
        )
        interior_note.next_to(domain["bottom"], DOWN, buff=0.25).align_to(domain["water_fill"], LEFT)
        move_above_nav(interior_note)
        interior_box = self.row_box(equations["interior"], FREE_HI)
        self.play(
            FadeOut(domain["assumptions"]),
            quiet_fade(equations["interior"]),
            Create(interior_shade),
            Create(interior_box),
            run_time=1.6,
        )
        self.play(quiet_fade(interior_note), run_time=1.0)
        self.wait(3.2)

        bottom_glow = domain["bottom"].copy().set_color(BOTTOM_HI).set_stroke(width=12.0, opacity=1.0)
        bottom_arrows = VGroup(
            Arrow([-5.25, -1.45, 0], [-5.25, -1.98, 0], buff=0, color=BOTTOM_HI, stroke_width=4.0),
            Arrow([-3.50, -1.45, 0], [-3.50, -1.98, 0], buff=0, color=BOTTOM_HI, stroke_width=4.0),
            Arrow([-1.75, -1.45, 0], [-1.75, -1.98, 0], buff=0, color=BOTTOM_HI, stroke_width=4.0),
        )
        bottom_note = note_card(
            [
                "Impermeable bed:",
                "the normal velocity through the flat bottom is zero.",
            ],
            BOTTOM_HI,
        )
        bottom_note.move_to(interior_note)
        bottom_box = self.row_box(equations["bottom_bc"], BOTTOM_HI)
        self.play(
            FadeOut(interior_note),
            FadeOut(interior_box),
            FadeOut(interior_shade),
            quiet_fade(equations["bottom_bc"]),
            Create(bottom_glow),
            LaggedStart(*[GrowArrow(arrow) for arrow in bottom_arrows], lag_ratio=0.18),
            Create(bottom_box),
            run_time=1.7,
        )
        self.play(quiet_fade(bottom_note), run_time=1.0)
        self.wait(3.0)

        surface_glow = domain["surface"].copy().set_color(SURFACE_HI).set_stroke(width=11.0, opacity=1.0)
        particle_path = domain["motion_path"].copy().set_color(SURFACE_HI).set_stroke(width=3.2, opacity=0.75)
        particle = Dot(domain["motion_path"].get_start(), radius=0.075, color=WHITE)
        particle_ring = Circle(radius=0.13, color=SURFACE_HI, stroke_width=2.4).move_to(particle)
        particle_trail = TracedPath(
            particle.get_center,
            stroke_color=SURFACE_HI,
            stroke_width=3.0,
            dissipating_time=1.5,
        )
        track_label = Text("same particle stays on the interface", font_size=18, color=SURFACE_HI)
        track_label.next_to(domain["surface"], UP, buff=0.36).shift(LEFT * 0.85)
        velocity_arrow = always_redraw(
            lambda: Arrow(
                particle.get_center() + LEFT * 0.28 + DOWN * 0.03,
                particle.get_center() + RIGHT * 0.62 + UP * 0.03,
                buff=0.04,
                color=BOUNDARY_HI,
                stroke_width=3.4,
                max_tip_length_to_length_ratio=0.18,
            )
        )
        no_cross_marker = VGroup(
            Line(ORIGIN + DOWN * 0.24, ORIGIN + UP * 0.24, color=FREE_HI, stroke_width=3.0),
            Cross(
                Line(ORIGIN + LEFT * 0.13, ORIGIN + RIGHT * 0.13),
                stroke_color=BOUNDARY_HI,
                stroke_width=3.0,
                scale_factor=0.35,
            ),
        )
        no_cross_marker.move_to(domain["surface_center"] + RIGHT * 1.15 + DOWN * 0.04)
        no_cross_label = Text("no crossing", font_size=15, color=FREE_HI)
        no_cross_label.next_to(no_cross_marker, UP, buff=0.08)
        no_cross_group = VGroup(no_cross_marker, no_cross_label)
        kin_note = note_card(
            [
                "Kinematic free surface:",
                "surface particles move with the surface, not through it.",
            ],
            BOUNDARY_HI,
        )
        kin_note.move_to(interior_note)
        kin_box = self.row_box(equations["kinematic"], BOUNDARY_HI)
        self.play(
            FadeOut(bottom_note),
            FadeOut(bottom_box),
            FadeOut(bottom_glow),
            FadeOut(bottom_arrows),
            quiet_fade(equations["kinematic"]),
            Create(surface_glow),
            Create(particle_path),
            quiet_fade(track_label),
            quiet_fade(particle),
            quiet_fade(particle_ring),
            GrowArrow(velocity_arrow),
            quiet_fade(no_cross_group, shift=UP * 0.04),
            Create(kin_box),
            run_time=1.7,
        )
        self.add(particle_trail)
        self.play(
            MoveAlongPath(particle, domain["motion_path"]),
            UpdateFromFunc(particle_ring, lambda mob: mob.move_to(particle)),
            run_time=4.5,
            rate_func=linear,
        )
        self.play(quiet_fade(kin_note), run_time=1.0)
        self.wait(3.2)

        pressure_badge = VGroup(
            MathTex(r"p=p_{\rm atm}", font_size=29, color=SURFACE_HI),
            Text("pressure continuity at the surface", font_size=17, color=WHITE),
        ).arrange(DOWN, buff=0.04)
        pressure_badge.next_to(domain["surface"], UP, buff=0.36).shift(RIGHT * 0.92)
        pressure_arrows = VGroup(
            Arrow(pressure_badge.get_bottom() + LEFT * 0.48, domain["surface_center"] + RIGHT * 0.30, buff=0.04, color=SURFACE_HI, stroke_width=3.2),
            Arrow(pressure_badge.get_bottom(), domain["surface_center"] + RIGHT * 0.95 + DOWN * 0.02, buff=0.04, color=SURFACE_HI, stroke_width=3.2),
            Arrow(pressure_badge.get_bottom() + RIGHT * 0.48, domain["surface_center"] + RIGHT * 1.60 + DOWN * 0.08, buff=0.04, color=SURFACE_HI, stroke_width=3.2),
        )
        bernoulli_terms = VGroup(
            self.term_chip(r"\phi_t", "unsteady potential", FREE_HI),
            self.term_chip(r"\frac12|\nabla\phi|^2", "kinetic energy", BOUNDARY_HI),
            self.term_chip(r"g\eta", "elevation head", SURFACE_HI),
        )
        bernoulli_terms.arrange(RIGHT, buff=0.12)
        fit_width(bernoulli_terms, 5.7)
        bernoulli_terms.move_to(domain["water_body"].get_center() + DOWN * 0.48)
        dyn_note = note_card(
            [
                "Dynamic free surface:",
                "the Bernoulli balance is evaluated on the pressure surface.",
            ],
            BOUNDARY_HI,
        )
        dyn_note.move_to(interior_note)
        dyn_box = self.row_box(equations["dynamic"], BOUNDARY_HI)
        self.play(
            FadeOut(kin_note),
            FadeOut(kin_box),
            FadeOut(velocity_arrow),
            FadeOut(no_cross_group),
            FadeOut(particle),
            FadeOut(particle_ring),
            FadeOut(particle_trail),
            FadeOut(particle_path),
            FadeOut(track_label),
            quiet_fade(equations["dynamic"]),
            quiet_fade(pressure_badge),
            LaggedStart(*[GrowArrow(arrow) for arrow in pressure_arrows], lag_ratio=0.18),
            LaggedStart(*[quiet_fade(term, shift=UP * 0.05) for term in bernoulli_terms], lag_ratio=0.15),
            Create(dyn_box),
            run_time=2.0,
        )
        self.play(quiet_fade(dyn_note), run_time=1.0)
        self.wait(3.5)

        takeaway = VGroup(
            Text(
                "Laplace's equation is easy once the boundaries are known.",
                font_size=23,
                color=WHITE,
            ),
            MarkupText(
                'Hard part: the <span foreground="#FFE45E">solution</span> is part of the boundary condition,',
                font_size=22,
            ),
            MarkupText(
                'because the condition must be imposed on the unknown <span foreground="#FFE45E">free surface</span>.',
                font_size=22,
            ),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        fit_width(takeaway, config.frame_width - 0.90)
        takeaway.to_edge(LEFT, buff=0.45)
        takeaway.set_y(-3.30)
        move_above_nav(takeaway, buff=0.18)
        box = Rectangle(
            width=config.frame_width - 0.70,
            height=takeaway.height + 0.36,
            color=SURFACE,
            stroke_width=1.6,
        ).set_fill(BLACK, opacity=0.28)
        box.move_to([0, takeaway.get_center()[1], 0])
        final_surface_glow = domain["surface"].copy().set_color(SURFACE_HI).set_stroke(width=11.0, opacity=1.0)
        final_surface_label = Text("unknown boundary", font_size=17, color=SURFACE_HI)
        final_surface_label.next_to(domain["surface_center"] + LEFT * 0.70 + UP * 0.23, UP, buff=0.10)
        final_surface_label.set_x(domain["surface_center"][0] - 0.42)
        final_label_box = SurroundingRectangle(
            final_surface_label,
            color=SURFACE_HI,
            buff=0.08,
            corner_radius=0.06,
            stroke_width=1.5,
        ).set_fill(BLACK, opacity=0.28)
        final_surface_callout = VGroup(final_label_box, final_surface_label)
        final_surface_callout_arrow = Arrow(
            final_surface_callout.get_bottom(),
            domain["surface_center"] + LEFT * 0.42 + UP * 0.04,
            buff=0.05,
            color=SURFACE_HI,
            stroke_width=2.8,
            max_tip_length_to_length_ratio=0.10,
        )
        self.play(
            FadeOut(dyn_note),
            FadeOut(dyn_box),
            FadeOut(surface_glow),
            FadeOut(pressure_badge),
            FadeOut(pressure_arrows),
            FadeOut(bernoulli_terms),
            FadeOut(domain["labels"][0]),
            Create(final_surface_glow),
            quiet_fade(final_surface_callout, shift=UP * 0.04),
            GrowArrow(final_surface_callout_arrow),
            quiet_fade(box),
            quiet_fade(takeaway),
            run_time=1.2,
        )
        self.wait(3.0)

    def row_box(self, row, color):
        return SurroundingRectangle(
            row,
            color=color,
            buff=0.09,
            corner_radius=0.06,
            stroke_width=2.0,
        )

    def term_chip(self, tex, text, color):
        formula = MathTex(tex, font_size=25, color=color)
        note = Text(text, font_size=14, color=WHITE)
        group = VGroup(formula, note).arrange(DOWN, buff=0.04)
        box = SurroundingRectangle(
            group,
            color=color,
            buff=0.10,
            corner_radius=0.06,
            stroke_width=1.5,
        ).set_fill(BLACK, opacity=0.35)
        return VGroup(box, group)

    def build_domain(self):
        left = -6.45
        right = -0.55
        z0 = 0.72
        bottom_y = -2.05
        amp = 0.22
        length = right - left

        def surf_y(x):
            phase = 2 * PI * (x - left) / length
            return z0 + amp * np.sin(phase) + 0.08 * np.sin(2 * phase + 0.4)

        xs = np.linspace(left, right, 160)
        top_points = [[x, surf_y(x), 0] for x in xs]
        fill_points = top_points + [[right, bottom_y, 0], [left, bottom_y, 0]]
        water_fill = Polygon(
            *fill_points,
            stroke_width=0,
            fill_color=WATER,
            fill_opacity=0.34,
        )

        surface = VMobject(color=SURFACE, stroke_width=4.0)
        surface.set_points_smoothly(top_points)
        motion_points = [[x, surf_y(x), 0] for x in np.linspace(left + 0.80, right - 1.55, 110)]
        motion_path = VMobject(color=SURFACE_HI, stroke_width=3.0)
        motion_path.set_points_smoothly(motion_points)
        still = DashedLine(
            [left, z0, 0],
            [right, z0, 0],
            color=MUTED,
            stroke_width=1.6,
            dash_length=0.10,
            dashed_ratio=0.55,
        )
        bottom = Line([left, bottom_y, 0], [right, bottom_y, 0], color=BOTTOM, stroke_width=5.0)
        side_l = Line([left, bottom_y, 0], [left, z0 + 0.42, 0], color=PANEL, stroke_width=1.2)
        side_r = Line([right, bottom_y, 0], [right, z0 + 0.42, 0], color=PANEL, stroke_width=1.2)

        eta_label = MathTex(r"z=\eta(x,t)", font_size=28, color=SURFACE)
        eta_label.next_to(surface, UP, buff=0.15).shift(LEFT * 0.35)
        swl_label = MathTex(r"z=0\ \text{still water}", font_size=23, color=MUTED)
        swl_label.next_to(still, RIGHT, buff=0.12)
        bottom_label = MathTex(r"z=-h", font_size=25, color=BOTTOM)
        bottom_label.next_to(bottom, UP, buff=0.08)
        labels = VGroup(eta_label, swl_label, bottom_label)

        potential = VGroup(
            MathTex(r"\phi(x,z,t)", font_size=34, color=WHITE),
            MathTex(r"(u,w)=\nabla\phi=(\phi_x,\phi_z)", font_size=24, color=MUTED),
        ).arrange(DOWN, buff=0.06)
        potential.move_to([(left + right) / 2, -0.52, 0])

        assumptions = VGroup(
            label("inviscid", 17, MUTED),
            label("incompressible", 17, MUTED),
            label("irrotational", 17, MUTED),
            label("finite depth", 17, SURFACE),
        ).arrange(RIGHT, buff=0.14)
        assumptions.next_to(bottom, DOWN, buff=0.52)
        fit_width(assumptions, 5.8)

        return {
            "water_fill": VGroup(water_fill, side_l, side_r),
            "water_body": water_fill,
            "surface": surface,
            "motion_path": motion_path,
            "still": still,
            "bottom": bottom,
            "labels": labels,
            "potential": potential,
            "assumptions": assumptions,
            "surface_center": surface.get_center(),
            "interior_point": potential.get_center(),
        }

    def build_equation_panel(self):
        heading = Text("Governing equation", font_size=25, color=WHITE, weight=BOLD)
        interior = equation_row(
            r"\nabla^2\phi=\phi_{xx}+\phi_{zz}=0,\quad -h<z<\eta",
            "mass conservation in the fluid",
            color=FREE,
        )
        bottom_bc = equation_row(
            r"\phi_z=0,\quad z=-h",
            "no normal flow through the bed",
            color=BOTTOM,
        )
        kinematic = equation_row(
            r"\eta_t+\phi_x\eta_x-\phi_z=0,\quad z=\eta(x,t)",
            "surface moves with the fluid particles",
            color=BOUNDARY,
        )
        dynamic = equation_row(
            r"\phi_t+\frac{1}{2}|\nabla\phi|^2+g\eta=0,\quad z=\eta(x,t)",
            "Bernoulli with atmospheric pressure gauge",
            color=BOUNDARY,
        )

        rows = VGroup(heading, interior, bottom_bc, kinematic, dynamic).arrange(
            DOWN,
            buff=0.24,
            aligned_edge=LEFT,
        )
        fit_width(rows, 5.25)
        rows.to_edge(RIGHT, buff=0.46).shift(UP * 0.42)
        background = SurroundingRectangle(
            rows,
            color=PANEL,
            buff=0.22,
            corner_radius=0.10,
            stroke_width=1.4,
        ).set_fill(BLACK, opacity=0.18)

        return {
            "background": background,
            "heading": heading,
            "interior": interior,
            "bottom_bc": bottom_bc,
            "kinematic": kinematic,
            "dynamic": dynamic,
        }

    def build_mechanism_tags(self):
        items = [
            (r"\phi_x\eta_x", "products", BOUNDARY),
            (r"\phi_x^2+\phi_z^2", "quadratic velocity", BOUNDARY),
            (r"z=\eta", "moving boundary", SURFACE),
        ]
        tags = VGroup()
        for tex, text, color in items:
            formula = MathTex(tex, font_size=24, color=color)
            note = Text(text, font_size=17, color=MUTED)
            group = VGroup(formula, note).arrange(DOWN, buff=0.05)
            box = SurroundingRectangle(
                group,
                color=color,
                buff=0.13,
                corner_radius=0.08,
                stroke_width=1.3,
            ).set_fill(BLACK, opacity=0.20)
            tags.add(VGroup(box, group))
        tags.arrange(RIGHT, buff=0.22)
        fit_width(tags, 5.9)
        return tags

    def build_mechanism_arrows(self, domain, mechanisms):
        surface_target = domain["surface_center"] + UP * 0.10
        interior_target = domain["interior_point"] + UP * 0.16
        targets = [
            surface_target + LEFT * 1.2,
            interior_target + RIGHT * 0.85,
            surface_target + RIGHT * 1.25,
        ]
        arrows = VGroup()
        for tag, target in zip(mechanisms, targets):
            arrows.add(
                Arrow(
                    tag.get_top(),
                    target,
                    buff=0.08,
                    color=tag[0].get_color(),
                    stroke_width=2.1,
                    max_tip_length_to_length_ratio=0.08,
                )
            )
        return arrows
