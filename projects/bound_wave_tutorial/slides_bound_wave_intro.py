from manim import *

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene


BG = ManimColor("#061018")
WATER_FILL = ManimColor("#083344")
SURFACE = ManimColor("#67E8F9")
BED = ManimColor("#B45309")
FG = ManimColor("#E5EEF5")
MUTED = ManimColor("#9FB1C1")
ACCENT = ManimColor("#FBBF24")
GREEN = ManimColor("#34D399")
RED = ManimColor("#FB7185")
PURPLE = ManimColor("#C084FC")
NAV_BG = ManimColor("#030712")
NAV_TRACK = ManimColor("#1F2937")
NAV_TEXT = ManimColor("#F8FAFC")
NAV_PROGRESS_HEIGHT = 0.72
NAV_PROGRESS_RADIUS = 0.055
NAV_MAIN_COLORS = [
    ManimColor("#FFE45E"),
    ManimColor("#FFB84D"),
    ManimColor("#FF7A59"),
    ManimColor("#FF5DA2"),
    ManimColor("#C77DFF"),
]
NAV_SUB_GRADIENT_STARTS = [
    ManimColor("#8B6508"),
    ManimColor("#8A4D08"),
    ManimColor("#8A2F1C"),
    ManimColor("#851D50"),
    ManimColor("#56248A"),
]
NAV_SUB_GRADIENT_ENDS = [
    ManimColor("#FFF7B8"),
    ManimColor("#FFE7B3"),
    ManimColor("#FFD3C7"),
    ManimColor("#FFC4DF"),
    ManimColor("#E9D0FF"),
]


Text.set_default(font="CMU Serif")


class BoundWaveIntroSlides(Slide):
    SECTIONS = [
        "potential flow",
        "why potential flow",
        "governing equation",
        "bottom BC",
        "Surface Kinematic BC",
        "Surface dynamic BC",
        "unknow surface",
        "steepness as small parameter",
        "collecting by order",
        "Taylor Expansion around z=0",
        "linear BVP",
        "vertical structure",
        "linear solution",
        "linear dispersion",
        "linear wave groups",
        "why focus groups",
        "From First Order to Second Order",
        "second-order BC",
        "quadratic forcing",
        "bound harmonic",
        "Why it is called bound wave",
        "bichromatic wave",
        "Second Order super/subharmonic for wave group",
        "bound harmonic at higher orders",
        "closing picture",
    ]
    MAIN_SECTIONS = [
        ("S0", "problem description", 0, 6),
        ("S1", "perturbation method and linearization", 6, 10),
        ("S2", "linear wave theory and wave group", 10, 16),
        ("S3", "Linear wave to second order stokes wave", 16, 19),
        ("S4", "Second Order Bound Waves", 19, 22),
        ("S5", "Second Order Theory for Wave Group", 22, 25),
    ]
    SCENARIO_METHODS = {
        "S0": [
            "_show_potential_flow_motivation",
            "_show_potential_flow_payoff",
            "_show_domain",
            "_show_bottom_condition",
            "_show_kinematic_condition",
            "_show_dynamic_condition",
        ],
        "S1": [
            "_show_free_boundary_difficulty",
            "_show_perturbation_checkpoint",
            "_show_first_order_conditions",
            "_show_surface_evaluation_step",
        ],
        "S2": [
            "_show_linear_bvp",
            "_show_linear_mode_shape",
            "_show_dynamic_amplitude",
            "_show_dispersion_relation",
            "_show_wave_group_intro",
            "_show_focused_wave_group_motivation",
            "_show_wave_group_importance",
        ],
        "S3": [
            "_show_second_order_transition",
            "_show_second_order_boundary_conditions",
            "_show_second_order_forcing",
        ],
        "S4": [
            "_show_bound_harmonic",
            "_show_free_versus_bound",
            "_show_two_component_interactions",
        ],
        "S5": [
            "_show_second_order_wave_group_map",
            "_show_bound_wave_visual_summary",
            "_show_closing_picture",
        ],
    }
    FULL_SCENARIO_ORDER = ("S0", "S1", "S2", "S3", "S4", "S5")

    def _pause(self):
        if hasattr(self, "next_slide"):
            self.next_slide(loop=False)
        else:
            self.wait(0.5)

    def _construct_methods(self, method_names):
        self.camera.background_color = BG
        for method_name in method_names:
            getattr(self, method_name)()

    def _construct_scenarios(self, scenario_codes):
        method_names = []
        for code in scenario_codes:
            method_names.extend(self.SCENARIO_METHODS[code])
        self._construct_methods(method_names)

    def _play_step(self, *animations, **kwargs):
        kwargs["run_time"] = max(kwargs.get("run_time", 0.0), 0.7)
        super().play(*animations, **kwargs)
        self._pause()

    def _text(self, text, font_size=28, color=FG, weight=NORMAL):
        # Use TeX for prose so the deck keeps a Computer Modern lecture style.
        return Tex(rf"\text{{{text}}}", font_size=font_size, color=color)

    def _title(self, text, subtitle=None):
        title = text if isinstance(text, Mobject) else self._text(text, font_size=44)
        if title.width > config.frame_width - 1.1:
            title.scale_to_fit_width(config.frame_width - 1.1)
        title.to_edge(UP, buff=0.14)
        rule = Line(LEFT * 5.9, RIGHT * 5.9, color=ACCENT, stroke_width=2.5)
        rule.next_to(title, DOWN, buff=0.08)
        group = VGroup(title, rule)
        if subtitle:
            sub = self._text(subtitle, font_size=25, color=MUTED)
            sub.next_to(rule, DOWN, buff=0.06)
            group.add(sub)
        return group

    def _caption(self, text, font_size=31):
        caption = self._text(text, font_size=font_size, color=ACCENT)
        caption.to_edge(DOWN, buff=1.28)
        return caption

    def _symbol_caption(self, parts, font_size=30):
        caption = VGroup()
        for item, kind in parts:
            if kind == "math":
                caption.add(MathTex(item, font_size=font_size + 2, color=ACCENT))
            else:
                caption.add(self._text(item, font_size=font_size, color=ACCENT))
        caption.arrange(RIGHT, buff=0.18)
        caption.to_edge(DOWN, buff=1.34)
        return caption

    def _nav(self, active_index):
        frame_w = config.frame_width
        frame_h = config.frame_height
        nav_h = NAV_PROGRESS_HEIGHT
        y_mid = -frame_h / 2 + nav_h / 2
        y_overall = y_mid + 0.19
        y_detail = y_mid - 0.19
        nav_w = frame_w - 0.28
        gap = 0.05
        bar_h = 0.20
        bg = RoundedRectangle(
            width=frame_w,
            height=nav_h,
            corner_radius=0.10,
            stroke_width=0,
            fill_color=NAV_BG,
            fill_opacity=0.99,
        ).move_to([0, y_mid, 0])
        top_rule = Line(
            [-frame_w / 2, y_mid + nav_h / 2, 0],
            [frame_w / 2, y_mid + nav_h / 2, 0],
            color=ManimColor("#334155"),
            stroke_width=1.2,
            stroke_opacity=0.9,
        )

        def label_color(color):
            r, g, b = color.to_rgb()
            return BLACK if (r + g + b) > 1.65 else NAV_TEXT

        def make_segment(
            x,
            y,
            width,
            label,
            color,
            active=False,
            show_label=True,
            font_size=13,
            text_color=None,
            active_fill_opacity=0.54,
        ):
            base = RoundedRectangle(
                width=width,
                height=bar_h,
                corner_radius=NAV_PROGRESS_RADIUS,
                stroke_width=0.7,
                stroke_color=color,
                stroke_opacity=1.0 if active else 0.42,
                fill_color=color,
                fill_opacity=0.34,
            ).move_to([x, y, 0])
            fill = RoundedRectangle(
                width=width if active else max(0.001, width * 0.50),
                height=bar_h,
                corner_radius=NAV_PROGRESS_RADIUS,
                stroke_width=0,
                fill_color=color,
                fill_opacity=active_fill_opacity if active else 0.26,
            )
            fill.align_to(base, LEFT)
            fill.set_y(y)
            group = VGroup(base, fill)
            if label:
                text = Text(
                    label,
                    font="CMU Serif",
                    font_size=font_size,
                    color=text_color if text_color is not None else label_color(color) if active else NAV_TEXT,
                    weight=BOLD if active else NORMAL,
                    disable_ligatures=True,
                )
                text.set_stroke(width=0, opacity=0)
                if text.width > width - 0.12:
                    text.scale_to_fit_width(width - 0.12)
                text.move_to(base)
                text.set_opacity(1.0 if show_label else 0.0)
                group.add(text)
            return group

        overall = VGroup()
        weights = [4.15 if start <= active_index < end else 1.0 for _, _, start, end in self.MAIN_SECTIONS]
        unit = (nav_w - gap * (len(weights) - 1)) / sum(weights)
        left_edge = -nav_w / 2
        running = 0.0
        active_main = 0
        for i, (code, name, start, end) in enumerate(self.MAIN_SECTIONS):
            if start <= active_index < end:
                active_main = i
            width = weights[i] * unit
            x = left_edge + running + width / 2
            color = NAV_MAIN_COLORS[i % len(NAV_MAIN_COLORS)]
            active = start <= active_index < end
            overall.add(
                make_segment(
                    x,
                    y_overall,
                    width,
                    f"{code}: {name}" if active else code,
                    color,
                    active=active,
                    show_label=True,
                    font_size=15 if active else 12,
                    text_color=WHITE if active else NAV_TEXT,
                    active_fill_opacity=0.54,
                )
            )
            running += width + gap

        start = self.MAIN_SECTIONS[active_main][2]
        end = self.MAIN_SECTIONS[active_main][3]
        local_names = self.SECTIONS[start:end]
        count = len(local_names)
        detail_palette = color_gradient(
            [
                NAV_SUB_GRADIENT_STARTS[active_main % len(NAV_SUB_GRADIENT_STARTS)],
                NAV_MAIN_COLORS[active_main % len(NAV_MAIN_COLORS)],
                NAV_SUB_GRADIENT_ENDS[active_main % len(NAV_SUB_GRADIENT_ENDS)],
            ],
            count,
        )
        detail = VGroup()
        active_local = active_index - start
        detail_weights = [3.35 if j == active_local else 1.0 for j in range(count)]
        detail_unit = (nav_w - gap * (count - 1)) / sum(detail_weights)
        detail_left = -nav_w / 2
        detail_running = 0.0
        for j, name in enumerate(local_names):
            idx = start + j
            active = idx == active_index
            seg_w = detail_weights[j] * detail_unit
            x = detail_left + detail_running + seg_w / 2
            detail.add(
                make_segment(
                    x,
                    y_detail,
                    seg_w,
                    name if active else "",
                    detail_palette[j],
                    active=active,
                    show_label=active,
                    font_size=15,
                    text_color=WHITE,
                    active_fill_opacity=0.70,
                )
            )
            detail_running += seg_w + gap

        nav = VGroup(bg, top_rule, overall, detail)
        nav.set_z_index(1000)
        return nav

    def _surface(self, x_min=-4.5, x_max=4.5, y0=0.78, amp=0.23, phase=-0.35):
        return FunctionGraph(
            lambda x: y0 + amp * np.cos(1.3 * x + phase),
            x_range=[x_min, x_max],
            color=SURFACE,
            stroke_width=5,
        )

    def _tank(self, width=8.5, height=2.9, labels=True, velocity=False):
        left_x = -width / 2
        right_x = width / 2
        bed_y = -height / 2
        still_y = height / 2 - 0.72
        surface = self._surface(left_x, right_x, still_y)
        points = [surface.point_from_proportion(a) for a in np.linspace(0, 1, 90)]
        water = Polygon(
            np.array([left_x, bed_y, 0]),
            *points,
            np.array([right_x, bed_y, 0]),
            stroke_width=0,
            fill_color=WATER_FILL,
            fill_opacity=0.85,
        )
        bed = Line([left_x, bed_y, 0], [right_x, bed_y, 0], color=BED, stroke_width=7)
        still = DashedLine(
            [left_x, still_y, 0],
            [right_x, still_y, 0],
            color=MUTED,
            stroke_width=2,
            dash_length=0.16,
        )
        walls = VGroup(
            Line([left_x, bed_y, 0], [left_x, still_y + 0.42, 0], color=MUTED, stroke_width=1.5),
            Line([right_x, bed_y, 0], [right_x, still_y + 0.42, 0], color=MUTED, stroke_width=1.5),
        )
        group = VGroup(water, bed, still, walls, surface)
        if labels:
            eta = MathTex(r"z=\eta(x,t)", font_size=25, color=SURFACE).next_to(surface, UP, buff=0.12)
            z0 = MathTex(r"z=0", font_size=22, color=MUTED).next_to(still, RIGHT, buff=0.12)
            zh = MathTex(r"z=-h", font_size=22, color=BED).next_to(bed, RIGHT, buff=0.12)
            group.add(VGroup(eta, z0, zh))
        if velocity:
            arrows = VGroup()
            for x in [-3.4, -2.0, -0.6, 0.8, 2.2, 3.5]:
                start = np.array([x, -0.55, 0])
                end = start + np.array([0.34, 0.32 + 0.06 * np.sin(x), 0])
                arrows.add(Arrow(start, end, buff=0, color=FG, stroke_width=2.4, max_tip_length_to_length_ratio=0.16))
            group.add(arrows)
        return group

    def _flat_tank(self, width=7.2, height=3.0, labels=True, mode=False):
        left_x = -width / 2
        right_x = width / 2
        bed_y = -height / 2
        still_y = height / 2 - 0.58
        water = Rectangle(
            width=width,
            height=still_y - bed_y,
            stroke_width=0,
            fill_color=WATER_FILL,
            fill_opacity=0.84,
        )
        water.move_to([(left_x + right_x) / 2, (bed_y + still_y) / 2, 0])
        bed = Line([left_x, bed_y, 0], [right_x, bed_y, 0], color=BED, stroke_width=7)
        still = DashedLine(
            [left_x, still_y, 0],
            [right_x, still_y, 0],
            color=MUTED,
            stroke_width=2,
            dash_length=0.16,
        )
        walls = VGroup(
            Line([left_x, bed_y, 0], [left_x, still_y + 0.34, 0], color=MUTED, stroke_width=1.5),
            Line([right_x, bed_y, 0], [right_x, still_y + 0.34, 0], color=MUTED, stroke_width=1.5),
        )
        group = VGroup(water, bed, still, walls)
        if mode:
            surface = self._surface(left_x, right_x, still_y + 0.03, amp=0.20, phase=-0.35)
            group.add(surface)
        if labels:
            z0 = MathTex(r"z=0", font_size=27, color=MUTED).next_to(still, RIGHT, buff=0.1)
            zh = MathTex(r"z=-h", font_size=27, color=BED).next_to(bed, RIGHT, buff=0.1)
            group.add(VGroup(z0, zh))
        return group

    def _wave_graph(self, func, x_min=-3.0, x_max=3.0, y0=0.0, color=SURFACE, stroke_width=4):
        xs = np.linspace(x_min, x_max, 180)
        points = [np.array([x, y0 + func(x), 0.0]) for x in xs]
        graph = VMobject()
        graph.set_points_as_corners(points)
        graph.set_style(
            stroke_color=color,
            stroke_width=stroke_width,
            stroke_opacity=1.0,
            fill_opacity=0.0,
        )
        return graph

    def _axis_line(self, x_min=-3.0, x_max=3.0, y0=0.0):
        return DashedLine(
            [x_min, y0, 0],
            [x_max, y0, 0],
            color=MUTED,
            stroke_width=1.5,
            dash_length=0.14,
        )

    def _spectrum_dot(self, x, label, color=ACCENT, y=0.0):
        dot = Dot([x, y, 0], radius=0.075, color=color)
        text = MathTex(label, font_size=25, color=color).next_to(dot, UP, buff=0.08)
        return VGroup(dot, text)

    def _clear(self, *mobjects):
        super().play(FadeOut(VGroup(*mobjects)), run_time=0.25)

    def _show_potential_flow_motivation(self):
        nav = self._nav(0)
        title = self._title(
            "Why potential flow is a useful first model",
            "for non-breaking gravity waves, the velocity field is often nearly irrotational",
        )
        tank = self._tank(width=7.2, height=3.6, labels=False, velocity=True)
        tank.to_edge(LEFT, buff=0.28).shift(DOWN * 0.04)

        assumptions = VGroup(
            self._text("Below the free surface,", font_size=29, color=MUTED),
            self._text("away from breaking/viscous layers:", font_size=29, color=MUTED),
            MathTex(r"\nabla\cdot\mathbf{u}=0", font_size=52, color=FG),
            MathTex(r"\nabla\times\mathbf{u}\approx 0", font_size=52, color=FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        assumptions.to_edge(RIGHT, buff=0.28).shift(DOWN * 0.05)
        caption = self._caption("Then the velocity can be represented by one scalar potential.", font_size=29)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(assumptions), run_time=0.55)
        self._play_step(FadeIn(caption), run_time=0.25)
        self._clear(title, nav, tank, assumptions, caption)

    def _show_potential_flow_payoff(self):
        nav = self._nav(1)
        title = self._title(
            MathTex(r"\text{The convenience: solve for } \phi \text{ and } \eta", font_size=44, color=FG),
            "instead of the full velocity and pressure fields",
        )
        left = VGroup(
            self._text("Navier-Stokes unknowns", font_size=34, color=MUTED),
            MathTex(r"u,\quad w,\quad p", font_size=66, color=FG),
            self._text("plus the free surface", font_size=32, color=MUTED),
        ).arrange(DOWN, buff=0.2)
        left.to_edge(LEFT, buff=0.5).shift(DOWN * 0.02)

        arrow = Arrow(LEFT * 1.3, RIGHT * 1.3, color=ACCENT, buff=0, stroke_width=9, max_tip_length_to_length_ratio=0.17)

        right = VGroup(
            self._text("Potential-flow unknowns", font_size=34, color=MUTED),
            MathTex(r"\phi,\qquad \eta", font_size=70, color=ACCENT),
            MathTex(r"\mathbf{u}=\nabla\phi", font_size=48, color=FG),
            MathTex(r"\phi_{xx}+\phi_{zz}=0", font_size=48, color=FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        right.to_edge(RIGHT, buff=0.52).shift(DOWN * 0.02)

        caption = self._symbol_caption(
            [
                ("velocity potential:", "text"),
                (r"\phi", "math"),
                ("free-surface elevation:", "text"),
                (r"\eta", "math"),
            ],
            font_size=30,
        )

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(left), run_time=0.55)
        self._play_step(GrowArrow(arrow), FadeIn(right), run_time=0.6)
        self._play_step(FadeIn(caption), run_time=0.25)
        self._clear(title, nav, left, arrow, right, caption)

    def _show_domain(self):
        nav = self._nav(2)
        title = self._title("The fluid occupies a finite-depth region")
        tank = self._tank(width=9.9, height=3.75, labels=True)
        tank.move_to(ORIGIN).shift(UP * 0.05)
        domain = MathTex(r"-h \le z \le \eta(x,t)", font_size=62, color=FG)
        domain.next_to(tank, DOWN, buff=0.12)
        caption = self._text("Within this fluid region, the velocity potential satisfies Laplace's equation.", font_size=25, color=ACCENT)
        caption.next_to(domain, DOWN, buff=0.10)
        if caption.width > 8.9:
            caption.scale_to_fit_width(8.9)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.65)
        self._play_step(FadeIn(domain), run_time=0.35)
        self._play_step(FadeIn(caption), run_time=0.25)
        self._clear(title, nav, tank, domain, caption)

    def _show_bottom_condition(self):
        nav = self._nav(3)
        title = self._title("At the bottom: no penetration")
        tank = self._tank(width=8.9, height=3.05, labels=True)
        tank.move_to(ORIGIN).shift(UP * 0.42)
        bed_highlight = Line(tank[1].get_start(), tank[1].get_end(), color=ACCENT, stroke_width=11)
        arrows = VGroup()
        bed_y = tank[1].get_y()
        for x in [-2.85, -0.95, 0.95, 2.85]:
            arrows.add(
                Arrow(
                    [x, bed_y + 0.54, 0],
                    [x, bed_y + 0.08, 0],
                    color=ACCENT,
                    buff=0,
                    stroke_width=5,
                    max_tip_length_to_length_ratio=0.18,
                )
            )
        equation = MathTex(r"\phi_z=0 \qquad \text{at } z=-h", font_size=57, color=BED)
        equation.next_to(tank, DOWN, buff=0.14)
        caption = self._caption("The normal velocity vanishes at the fixed bed.", font_size=29)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(bed_highlight), FadeIn(arrows), run_time=0.35)
        self._play_step(FadeIn(equation), run_time=0.35)
        self._play_step(FadeIn(caption), run_time=0.2)
        self._clear(title, nav, tank, bed_highlight, arrows, equation, caption)

    def _show_kinematic_condition(self):
        nav = self._nav(4)
        title = self._title("At the surface: particles remain on the free surface")
        tank = self._tank(width=6.85, height=3.35, labels=True)
        tank.to_edge(LEFT, buff=0.22).shift(UP * 0.18)
        surface = tank[4]
        particle = Dot(surface.point_from_proportion(0.25), radius=0.085, color=ACCENT)
        path = VMobject()
        path.set_points_smoothly([surface.point_from_proportion(a) for a in np.linspace(0.25, 0.76, 24)])
        path.set_stroke(ACCENT, width=4, opacity=0.55)

        derivation = VGroup(
            MathTex(r"F(x,z,t)=z-\eta(x,t)=0", font_size=38, color=FG),
            MathTex(r"\frac{DF}{Dt}=0", font_size=42, color=ACCENT),
            MathTex(r"w-\eta_t-u\eta_x=0", font_size=38, color=FG),
            MathTex(r"u=\phi_x,\qquad w=\phi_z", font_size=36, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        derivation.to_edge(RIGHT, buff=0.38).shift(UP * 0.05)

        surface_label = self._text("particle remains on the free surface", font_size=25, color=ACCENT)
        surface_label.next_to(tank, UP, buff=0.16).align_to(tank, LEFT).shift(RIGHT * 0.55)

        final_equation = MathTex(
            r"\eta_t=\phi_z-\phi_x\eta_x \qquad \text{at } z=\eta(x,t)",
            font_size=33,
            color=SURFACE,
        )
        final_equation.next_to(derivation, DOWN, buff=0.22).align_to(derivation, LEFT)
        caption = self._caption("The free surface moves with the water particles on it.", font_size=25)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(path), FadeIn(surface_label), FadeIn(particle), run_time=0.35)
        self._play_step(MoveAlongPath(particle, path), run_time=0.9, rate_func=smooth)
        self._play_step(FadeIn(derivation[0]), FadeIn(derivation[1]), run_time=0.45)
        self._play_step(FadeIn(derivation[2]), FadeIn(derivation[3]), run_time=0.45)
        self._play_step(FadeIn(final_equation), run_time=0.35)
        self._play_step(FadeIn(caption), run_time=0.2)
        self._clear(title, nav, tank, particle, path, surface_label, derivation, final_equation, caption)

    def _show_dynamic_condition(self):
        nav = self._nav(5)
        title = self._title("At the surface: pressure matches the atmosphere")
        tank = self._tank(width=6.85, height=3.35, labels=True)
        tank.to_edge(LEFT, buff=0.22).shift(UP * 0.18)
        surface = tank[4]
        point = Dot(surface.point_from_proportion(0.65), radius=0.085, color=GREEN)
        pressure_arrow = Arrow(point.get_center() + UP * 0.78, point.get_center() + UP * 0.14, color=GREEN, buff=0, stroke_width=4)
        p_label = MathTex(r"p=p_{\mathrm{atm}}", font_size=45, color=GREEN).next_to(pressure_arrow, UP, buff=0.08)

        bernoulli = VGroup(
            MathTex(
                r"\phi_t+\frac12|\nabla\phi|^2+\frac{p}{\rho}+gz=C(t)",
                font_size=34,
                color=FG,
            ),
            MathTex(r"p=p_{\mathrm{atm}},\qquad z=\eta", font_size=38, color=GREEN),
            MathTex(r"\text{absorb constants into }\phi", font_size=31, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bernoulli.to_edge(RIGHT, buff=0.3).shift(UP * 0.24)

        equation = VGroup(
            MathTex(r"\phi_t+\frac12(\phi_x^2+\phi_z^2)+g\eta=0", font_size=30, color=GREEN),
            MathTex(r"\text{at } z=\eta(x,t)", font_size=25, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        equation.next_to(bernoulli, DOWN, buff=0.24).align_to(bernoulli, LEFT)
        if equation.width > 4.15:
            equation.scale_to_fit_width(4.15)
        caption = self._caption("At atmospheric pressure, Bernoulli gives the dynamic free-surface condition.", font_size=24)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(point), GrowArrow(pressure_arrow), FadeIn(p_label), run_time=0.45)
        self._play_step(FadeIn(bernoulli[0]), run_time=0.35)
        self._play_step(FadeIn(bernoulli[1]), FadeIn(bernoulli[2]), run_time=0.45)
        self._play_step(FadeIn(equation), run_time=0.35)
        self._play_step(FadeIn(caption), run_time=0.2)
        self._clear(title, nav, tank, point, pressure_arrow, p_label, bernoulli, equation, caption)

    def _show_free_boundary_difficulty(self):
        nav = self._nav(6)
        title = self._title("Taylor expansion around z=0")
        tank = self._tank(width=5.85, height=3.05, labels=True)
        tank.to_edge(LEFT, buff=0.18).shift(UP * 0.08)
        focus = SurroundingRectangle(tank[4], color=RED, buff=0.06, stroke_width=3)
        still = tank[2]
        surface = tank[4]
        map_arrow = Arrow(
            surface.point_from_proportion(0.55) + RIGHT * 0.05,
            np.array([surface.point_from_proportion(0.55)[0] + 0.05, still.get_y(), 0]),
            buff=0.02,
            color=ACCENT,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.24,
        )
        known_label = MathTex(r"\text{known level: } z=0", font_size=29, color=ACCENT)
        known_label.move_to([tank.get_center()[0] - 1.25, still.get_y() - 0.42, 0])

        right = VGroup(
            MathTex(r"\text{free-boundary problem}", font_size=31, color=FG),
            MathTex(r"\text{conditions live at } z=\eta(x,t)", font_size=33, color=RED),
            MathTex(r"\eta\text{ is part of the solution}", font_size=32, color=FG),
            MathTex(r"\text{introduce a small wave-steepness parameter}", font_size=27, color=ACCENT),
            MathTex(r"\text{Taylor expand the conditions to } z=0", font_size=31, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        right.to_edge(RIGHT, buff=0.18).shift(UP * 0.05)
        if right.width > 5.55:
            right.scale_to_fit_width(5.55)
        caption = self._caption("Perturbation turns boundary conditions on an unknown surface into equations at a known mean level.", font_size=25)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(Create(focus), run_time=0.3)
        self._play_step(FadeIn(right[:3]), run_time=0.45)
        self._play_step(FadeIn(right[3]), GrowArrow(map_arrow), FadeIn(known_label), run_time=0.5)
        self._play_step(FadeIn(right[4]), run_time=0.35)
        self._play_step(FadeIn(caption), run_time=0.2)
        self._clear(title, nav, tank, focus, map_arrow, known_label, right, caption)

    def _show_perturbation_checkpoint(self):
        nav = self._nav(7)
        title = self._title("Small amplitude justifies Taylor expansion")
        tank = self._tank(width=5.85, height=3.15, labels=False)
        tank.to_edge(LEFT, buff=0.26).shift(UP * 0.72)
        still = tank[2]
        surface = tank[4]
        crest = surface.point_from_proportion(0.5)
        still_mid = np.array([crest[0], still.get_y(), 0])
        amp_arrow = DoubleArrow(still_mid, crest, color=ACCENT, buff=0.02, max_tip_length_to_length_ratio=0.22)
        amp_label = MathTex(r"a", font_size=46, color=ACCENT).next_to(amp_arrow, RIGHT, buff=0.08)
        depth_arrow = DoubleArrow(
            np.array([tank[0].get_left()[0] + 0.28, tank[1].get_y(), 0]),
            np.array([tank[0].get_left()[0] + 0.28, still.get_y(), 0]),
            color=GREEN,
            buff=0.02,
            max_tip_length_to_length_ratio=0.12,
        )
        depth_label = MathTex(r"h", font_size=46, color=GREEN).next_to(depth_arrow, LEFT, buff=0.08)
        mean_label = MathTex(r"z=0", font_size=39, color=MUTED).next_to(still, RIGHT, buff=0.1)

        scale_notes = VGroup(
            MathTex(r"\epsilon=ka\ll 1", font_size=52, color=ACCENT),
            MathTex(r"|\eta|/h\ll 1", font_size=45, color=GREEN),
            MathTex(r"z=\eta(x,t)\approx 0", font_size=41, color=FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        scale_notes.to_edge(RIGHT, buff=0.42).shift(UP * 0.98)

        definitions = VGroup(
            MathTex(r"a:\ \text{wave amplitude}", font_size=27, color=ACCENT),
            MathTex(r"k=\frac{2\pi}{\lambda}:\ \text{wavenumber}", font_size=27, color=FG),
            MathTex(r"\epsilon=ka:\ \text{wave steepness}", font_size=27, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        definitions.next_to(scale_notes, DOWN, buff=0.09).align_to(scale_notes, LEFT)

        taylor = MathTex(
            r"f(x,\eta,t)=f(x,0,t)+\eta f_z(x,0,t)+\frac12\eta^2f_{zz}(x,0,t)+\cdots",
            font_size=31,
            color=FG,
        )
        if taylor.width > 7.65:
            taylor.scale_to_fit_width(7.65)
        taylor.to_edge(DOWN, buff=1.62)
        taylor_label = self._text("Taylor expand the free-surface conditions at the mean level", font_size=25, color=MUTED)
        taylor_label.next_to(taylor, UP, buff=0.1)
        expansions = VGroup(
            MathTex(r"\eta=\epsilon\eta^{(1)}+\epsilon^2\eta^{(2)}+\cdots", font_size=28, color=ACCENT),
            MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\cdots", font_size=28, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.055)
        expansions.next_to(definitions, DOWN, buff=0.08).align_to(definitions, LEFT)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(VGroup(amp_arrow, amp_label, depth_arrow, depth_label, mean_label)), run_time=0.45)
        self._play_step(FadeIn(scale_notes), FadeIn(definitions), run_time=0.45)
        self._play_step(FadeIn(VGroup(expansions, taylor_label, taylor)), run_time=0.5)
        self._clear(
            title,
            nav,
            tank,
            amp_arrow,
            amp_label,
            depth_arrow,
            depth_label,
            mean_label,
            scale_notes,
            definitions,
            expansions,
            taylor_label,
            taylor,
        )

    def _show_first_order_conditions(self):
        nav = self._nav(8)
        title = self._title(MathTex(r"\text{Linearization means collecting the } \epsilon \text{ terms}", font_size=44, color=FG))

        expansions = VGroup(
            MathTex(r"\eta=\epsilon\eta^{(1)}+\epsilon^2\eta^{(2)}+\cdots", font_size=34, color=ACCENT),
            MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\cdots", font_size=34, color=ACCENT),
        ).arrange(DOWN, buff=0.06)
        expansions.to_edge(UP, buff=0.98)

        left = VGroup(
            self._text("start from the surface conditions", font_size=24, color=MUTED),
            MathTex(r"\eta_t=\phi_z-\phi_x\eta_x", font_size=34, color=FG),
            MathTex(r"\phi_t+\frac12(\phi_x^2+\phi_z^2)+g\eta=0", font_size=31, color=FG),
            MathTex(r"\text{at }z=\eta(x,t)", font_size=28, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        left.to_edge(LEFT, buff=0.25).shift(DOWN * 0.08)

        middle = VGroup(
            self._text("insert the expansions", font_size=24, color=MUTED),
            MathTex(r"\eta_t=\epsilon\eta^{(1)}_t+O(\epsilon^2)", font_size=31, color=SURFACE),
            MathTex(r"\phi_z=\epsilon\phi^{(1)}_z+O(\epsilon^2)", font_size=31, color=SURFACE),
            MathTex(r"\phi_x\eta_x=(\epsilon\phi^{(1)}_x)(\epsilon\eta^{(1)}_x)+O(\epsilon^3)", font_size=27, color=MUTED),
            MathTex(r"\frac12(\phi_x^2+\phi_z^2)=O(\epsilon^2)", font_size=29, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        middle.move_to(ORIGIN + DOWN * 0.08)

        right = VGroup(
            self._text("keep the coefficient of epsilon", font_size=24, color=MUTED),
            MathTex(r"\eta^{(1)}_t=\phi^{(1)}_z", font_size=43, color=SURFACE),
            MathTex(r"\phi^{(1)}_t+g\eta^{(1)}=0", font_size=43, color=GREEN),
            MathTex(r"\text{then evaluate at }z=0", font_size=27, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        right.to_edge(RIGHT, buff=0.25).shift(DOWN * 0.08)

        arrows = VGroup(
            Arrow(left.get_right() + RIGHT * 0.12, middle.get_left() + LEFT * 0.12, color=ACCENT, buff=0.05, stroke_width=4),
            Arrow(middle.get_right() + RIGHT * 0.12, right.get_left() + LEFT * 0.12, color=ACCENT, buff=0.05, stroke_width=4),
        )
        caption = self._caption("Products of first-order quantities are epsilon squared, so they first force the second-order problem.", font_size=24)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(expansions), run_time=0.5)
        self._play_step(FadeIn(left), run_time=0.45)
        self._play_step(GrowArrow(arrows[0]), FadeIn(middle), run_time=0.55)
        self._play_step(GrowArrow(arrows[1]), FadeIn(right), run_time=0.55)
        self._play_step(FadeIn(caption), run_time=0.25)
        self._clear(title, nav, expansions, left, middle, right, arrows, caption)

    def _show_surface_evaluation_step(self):
        nav = self._nav(9)
        title = self._title(MathTex(r"\text{Why the first-order surface conditions live at } z=0", font_size=44, color=FG))
        tank = self._tank(width=5.9, height=3.05, labels=False)
        tank.to_edge(LEFT, buff=0.25).shift(UP * 0.32)
        still = tank[2]
        surface = tank[4]
        surface_label = MathTex(r"z=\eta(x,t)=O(\epsilon)", font_size=31, color=SURFACE)
        surface_label.next_to(surface, UP, buff=0.10).align_to(tank, LEFT).shift(RIGHT * 0.45)
        mean_label = MathTex(r"z=0", font_size=32, color=ACCENT).next_to(still, RIGHT, buff=0.10)
        arrow = Arrow(
            surface.point_from_proportion(0.56),
            np.array([surface.point_from_proportion(0.56)[0], still.get_y(), 0]),
            color=ACCENT,
            buff=0.03,
            stroke_width=4,
        )

        taylor = VGroup(
            MathTex(r"\phi(x,\eta,t)=\phi(x,0,t)+\eta\,\phi_z(x,0,t)+\cdots", font_size=34, color=FG),
            MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\cdots,\qquad \eta=O(\epsilon)", font_size=31, color=ACCENT),
            MathTex(
                r"\phi(x,\eta,t)=\epsilon\phi^{(1)}(x,0,t)+O(\epsilon^2)",
                font_size=36,
                color=GREEN,
            ),
            MathTex(r"\text{so first-order surface terms are evaluated at }z=0", font_size=28, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        taylor.to_edge(RIGHT, buff=0.22).shift(UP * 0.10)
        caption = self._caption("The evaluation at the unknown surface is still present, but its first correction is second order.", font_size=24)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(surface_label), FadeIn(mean_label), GrowArrow(arrow), run_time=0.45)
        self._play_step(FadeIn(taylor[:2]), run_time=0.55)
        self._play_step(FadeIn(taylor[2:]), FadeIn(caption), run_time=0.45)
        self._clear(title, nav, tank, surface_label, mean_label, arrow, taylor, caption)

    def _show_linear_bvp(self):
        nav = self._nav(10)
        title = self._title("The first-order problem is now linear and fixed-boundary")
        tank = self._flat_tank(width=6.7, height=3.25, labels=True)
        tank.to_edge(LEFT, buff=0.28).shift(UP * 0.05)
        mean_highlight = Line(tank[2].get_start(), tank[2].get_end(), color=ACCENT, stroke_width=5)
        mean_label = MathTex(r"\text{free-surface conditions are applied here}", font_size=27, color=ACCENT)
        mean_label.next_to(mean_highlight, UP, buff=0.14).align_to(tank, LEFT).shift(RIGHT * 0.45)

        system = VGroup(
            MathTex(r"\phi^{(1)}_{xx}+\phi^{(1)}_{zz}=0", font_size=48, color=FG),
            MathTex(r"\phi^{(1)}_z=0\qquad z=-h", font_size=45, color=BED),
            MathTex(r"\eta^{(1)}_t=\phi^{(1)}_z\qquad z=0", font_size=45, color=SURFACE),
            MathTex(r"\phi^{(1)}_t+g\eta^{(1)}=0\qquad z=0", font_size=45, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        system.to_edge(RIGHT, buff=0.42).shift(DOWN * 0.02)

        caption = self._caption("This is the linear water-wave boundary-value problem in finite depth.", font_size=27)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(mean_highlight), FadeIn(mean_label), run_time=0.35)
        self._play_step(FadeIn(system), FadeIn(caption), run_time=0.5)
        self._clear(title, nav, tank, mean_highlight, mean_label, system, caption)

    def _show_linear_mode_shape(self):
        nav = self._nav(11)
        title = self._title("Seek one unidirectional sinusoidal mode")
        tank = self._flat_tank(width=6.35, height=3.1, labels=True, mode=True)
        tank.to_edge(LEFT, buff=0.28).shift(UP * 0.22)
        theta = MathTex(r"\theta=kx-\omega t", font_size=43, color=ACCENT)
        theta.next_to(tank, DOWN, buff=0.18)
        vertical_shape = MathTex(
            r"\cosh k(z+h)\ \text{sets the vertical structure}",
            font_size=24,
            color=MUTED,
        )
        vertical_shape.next_to(theta, DOWN, buff=0.08).align_to(theta, LEFT)

        ansatz = VGroup(
            MathTex(r"\eta^{(1)}=a\cos\theta", font_size=50, color=SURFACE),
            MathTex(
                r"\phi^{(1)}=A\,\cosh k(z+h)\,\sin\theta",
                font_size=43,
                color=FG,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ansatz.to_edge(RIGHT, buff=0.24).shift(UP * 0.46)

        check = VGroup(
            self._text("Why this vertical shape?", font_size=28, color=MUTED),
            MathTex(r"\phi^{(1)}_{xx}+\phi^{(1)}_{zz}=0", font_size=36, color=FG),
            MathTex(r"\phi^{(1)}_z=Ak\sinh k(z+h)\sin\theta", font_size=34, color=FG),
            MathTex(r"\phi^{(1)}_z=0\quad\text{at }z=-h", font_size=36, color=BED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        check.next_to(ansatz, DOWN, buff=0.22).align_to(ansatz, LEFT)

        caption = self._caption("The bottom condition selects the finite-depth vertical structure.", font_size=28)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(tank), run_time=0.55)
        self._play_step(FadeIn(theta), run_time=0.35)
        self._play_step(FadeIn(ansatz), run_time=0.45)
        self._play_step(FadeIn(check), FadeIn(vertical_shape), FadeIn(caption), run_time=0.45)
        self._clear(title, nav, tank, theta, vertical_shape, ansatz, check, caption)

    def _show_dynamic_amplitude(self):
        nav = self._nav(12)
        title = self._title("Use the dynamic condition to determine the potential amplitude")

        left = VGroup(
            self._text("mode form at the mean surface", font_size=27, color=MUTED),
            MathTex(r"\eta^{(1)}=a\cos\theta", font_size=42, color=SURFACE),
            MathTex(r"\phi^{(1)}=A\cosh k(z+h)\sin\theta", font_size=36, color=FG),
            MathTex(r"\theta=kx-\omega t", font_size=35, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        left.to_edge(LEFT, buff=0.45).shift(UP * 0.45)

        chain = VGroup(
            MathTex(r"\phi^{(1)}_t+g\eta^{(1)}=0\qquad z=0", font_size=39, color=GREEN),
            MathTex(r"\phi^{(1)}_t=-\omega A\cosh(kh)\cos\theta", font_size=34, color=FG),
            MathTex(r"-\omega A\cosh(kh)\cos\theta+ga\cos\theta=0", font_size=32, color=FG),
            MathTex(r"A=\frac{ag}{\omega\cosh(kh)}", font_size=48, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        chain.to_edge(RIGHT, buff=0.26).shift(UP * 0.05)

        defs = VGroup(
            MathTex(r"g:\ \text{gravitational acceleration}", font_size=27, color=MUTED),
            MathTex(r"\cosh(kh):\ \text{finite-depth factor at }z=0", font_size=27, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        defs.next_to(left, DOWN, buff=0.30).align_to(left, LEFT)
        caption = self._caption("The dynamic condition fixes the scale of the velocity potential.", font_size=27)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(left), run_time=0.5)
        self._play_step(FadeIn(chain[:2]), run_time=0.55)
        self._play_step(FadeIn(chain[2:]), FadeIn(defs), FadeIn(caption), run_time=0.55)
        self._clear(title, nav, left, chain, defs, caption)

    def _show_dispersion_relation(self):
        nav = self._nav(13)
        title = self._title("Linear waves travel following the linear dispersion relation")

        kin = VGroup(
            MathTex(r"\eta^{(1)}_t=\phi^{(1)}_z\qquad z=0", font_size=38, color=SURFACE),
            MathTex(r"\eta^{(1)}_t=a\omega\sin\theta", font_size=34, color=FG),
            MathTex(
                r"\phi^{(1)}_z=\frac{ag}{\omega}\frac{k\sinh kh}{\cosh kh}\sin\theta",
                font_size=30,
                color=FG,
            ),
            MathTex(r"a\omega=\frac{agk}{\omega}\tanh(kh)", font_size=32, color=FG),
            MathTex(r"\omega^2=gk\tanh(kh)", font_size=46, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        kin.to_edge(LEFT, buff=0.42).shift(UP * 0.32)

        origin = np.array([1.25, -1.05, 0])
        k_axis = Arrow(origin, origin + RIGHT * 4.35, buff=0, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.045)
        w_axis = Arrow(origin, origin + UP * 3.05, buff=0, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.06)
        k_label = MathTex(r"k", font_size=28, color=MUTED).next_to(k_axis.get_end(), DOWN, buff=0.04)
        w_label = MathTex(r"\omega", font_size=28, color=MUTED).next_to(w_axis.get_end(), LEFT, buff=0.04)
        curve = FunctionGraph(
            lambda x: origin[1] + 1.18 * np.sqrt(max(x - origin[0], 0.0)),
            x_range=[origin[0], origin[0] + 3.85],
            color=SURFACE,
            stroke_width=4,
        )
        primary = Dot(origin + RIGHT * 1.26 + UP * 1.32, radius=0.075, color=GREEN)
        primary_label = MathTex(r"(k,\omega)", font_size=27, color=GREEN).next_to(primary, LEFT, buff=0.10)
        curve_label = MathTex(r"\omega^2=gk\tanh(kh)", font_size=28, color=SURFACE)
        curve_label.next_to(curve, UP, buff=0.12).shift(RIGHT * 0.36)
        components = VGroup()
        component_labels = VGroup()
        component_points = []
        for dx, lab, col in [(0.70, r"k_1", GREEN), (1.82, r"k_2", ACCENT), (3.02, r"k_3", RED)]:
            y = origin[1] + 1.18 * np.sqrt(dx)
            point = origin + RIGHT * dx + UP * (y - origin[1])
            component_points.append(point)
            dot = Dot(point, radius=0.055, color=col)
            components.add(dot)
            component_labels.add(MathTex(lab, font_size=20, color=col).next_to(dot, DOWN, buff=0.06))
        moving_particle = Dot(component_points[0], radius=0.07, color=ACCENT)
        dispersion_walk = VMobject()
        walk_points = [
            origin + RIGHT * dx + UP * (1.18 * np.sqrt(dx))
            for dx in np.linspace(0.70, 3.02, 36)
        ]
        dispersion_walk.set_points_smoothly(walk_points)
        component_wave = MathTex(
            r"\eta^{(1)}=\sum_j a_j\cos(k_jx-\omega_jt)",
            font_size=25,
            color=ACCENT,
        )
        component_wave.next_to(k_axis, DOWN, buff=0.36).align_to(k_axis, LEFT)
        plot = VGroup(
            k_axis,
            w_axis,
            k_label,
            w_label,
            curve,
            curve_label,
            primary,
            primary_label,
            components,
            component_labels,
            moving_particle,
            component_wave,
        )

        note = VGroup(
            self._text("linear regime: each wavenumber is solved independently", font_size=18, color=MUTED),
            self._text("a sum of free components is still a solution", font_size=18, color=MUTED),
            self._text("that superposition property is why linear theory is easy to use", font_size=18, color=MUTED),
            self._text("second order will lose this independent-component property", font_size=18, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.055)
        note.move_to([0.05, -2.35, 0])
        plot.to_edge(RIGHT, buff=0.20).shift(UP * 0.18)
        right = VGroup(plot, note)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(kin[:-1]), run_time=0.55)
        self._play_step(FadeIn(kin[-1]), FadeIn(VGroup(k_axis, w_axis, k_label, w_label, curve, curve_label, primary, primary_label)), run_time=0.55)
        self._play_step(
            FadeIn(moving_particle),
            MoveAlongPath(moving_particle, dispersion_walk),
            FadeIn(components),
            FadeIn(component_labels),
            FadeIn(component_wave),
            FadeIn(note),
            run_time=1.2,
        )
        self._clear(title, nav, kin, right)

    def _show_second_order_transition(self):
        nav = self._nav(16)
        title = self._title("Linearity fails at second order")

        left = VGroup(
            Text("Airy wave", font_size=30, color=SURFACE),
            MathTex(r"\eta^{(1)}=\sum_m a_m\cos\theta_m", font_size=34, color=FG),
            Text("linear boundary conditions", font_size=22, color=MUTED),
            Text("components superpose independently", font_size=22, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        left_box = SurroundingRectangle(left, color=SURFACE, buff=0.20, corner_radius=0.07).set_fill(BG, opacity=0.50)
        left_group = VGroup(left_box, left).to_edge(LEFT, buff=0.58).shift(UP * 0.58)

        right = VGroup(
            Text("Stokes correction", font_size=30, color=ACCENT),
            MathTex(r"\eta^{(1)}\eta^{(1)},\quad \phi_x^{(1)}\eta_x^{(1)},\quad (\nabla\phi^{(1)})^2", font_size=27, color=FG),
            Text("quadratic forcing couples phases", font_size=22, color=MUTED),
            MathTex(r"(k_m,k_n)\rightarrow k_m\pm k_n", font_size=34, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        right_box = SurroundingRectangle(right, color=ACCENT, buff=0.20, corner_radius=0.07).set_fill(BG, opacity=0.50)
        right_group = VGroup(right_box, right).to_edge(RIGHT, buff=0.58).shift(UP * 0.58)

        bridge = VGroup(
            MathTex(
                r"\text{Taking the first-order wave amplitude as the ordering parameter,}",
                font_size=23,
                color=FG,
            ),
            MathTex(
                r"\text{the }O(\epsilon^2)\text{ solution contains products of first-order waves.}",
                font_size=23,
                color=FG,
            ),
            MathTex(
                r"\text{For a monochromatic Stokes wave this is self-interaction;}",
                font_size=23,
                color=MUTED,
            ),
            MathTex(
                r"\text{for bichromatic and polychromatic waves it becomes pairwise coupling.}",
                font_size=23,
                color=MUTED,
            ),
        ).arrange(DOWN, buff=0.05)
        bridge.move_to([0.0, -1.58, 0])
        bridge.scale_to_fit_width(10.8)

        caption = self._caption("Second order is solved linearly for the correction, but its source is quadratic in the Airy field.", font_size=22)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(left_group), run_time=0.55)
        self._play_step(FadeIn(right_group), run_time=0.55)
        self._play_step(FadeIn(bridge), FadeIn(caption), run_time=0.55)
        self._clear(title, nav, left_group, right_group, bridge, caption)

    def _show_second_order_boundary_conditions(self):
        nav = self._nav(17)
        title = self._title("Second Order BC by collecting epsilon-squared terms")

        expanded = VGroup(
            self._text("Dalzell Eq. (5)-(6), restricted here to one horizontal direction", font_size=24, color=MUTED),
            MathTex(
                r"g\eta+\phi_t+\eta\phi_{zt}+\frac12(\phi_x^2+\phi_z^2)=0",
                font_size=34,
                color=GREEN,
            ),
            MathTex(
                r"\eta_t-\phi_z-\eta\phi_{zz}+\phi_x\eta_x=0",
                font_size=34,
                color=SURFACE,
            ),
            MathTex(r"\text{all evaluated at }z=0", font_size=27, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        expanded.to_edge(LEFT, buff=0.34).shift(UP * 0.55)

        expansions = VGroup(
            MathTex(r"\eta=\epsilon\eta^{(1)}+\epsilon^2\eta^{(2)}+\cdots", font_size=30, color=ACCENT),
            MathTex(r"\phi=\epsilon\phi^{(1)}+\epsilon^2\phi^{(2)}+\cdots", font_size=30, color=ACCENT),
            MathTex(r"\text{collect the coefficient of }\epsilon^2", font_size=26, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        expansions.next_to(expanded, DOWN, buff=0.36).align_to(expanded, LEFT)

        collected = VGroup(
            self._text("second-order boundary conditions", font_size=24, color=MUTED),
            MathTex(
                r"\phi^{(2)}_t+g\eta^{(2)}=-\eta^{(1)}\partial_z\phi^{(1)}_t-\frac12\left((\phi^{(1)}_x)^2+(\phi^{(1)}_z)^2\right)",
                font_size=24,
                color=GREEN,
            ),
            MathTex(
                r"\eta^{(2)}_t-\phi^{(2)}_z=\eta^{(1)}\partial_z^2\phi^{(1)}-\phi^{(1)}_x\eta^{(1)}_x",
                font_size=28,
                color=SURFACE,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        collected.to_edge(RIGHT, buff=0.18).shift(UP * 0.12)

        arrow = Arrow(
            expansions.get_right() + RIGHT * 0.14,
            collected.get_left() + LEFT * 0.14,
            color=ACCENT,
            buff=0.04,
            stroke_width=5,
        )
        caption = self._caption("The second-order unknowns are linear; every forcing term is built from first-order fields.", font_size=24)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(expanded), run_time=0.55)
        self._play_step(FadeIn(expansions), run_time=0.35)
        self._play_step(GrowArrow(arrow), FadeIn(collected), run_time=0.6)
        self._play_step(FadeIn(caption), run_time=0.2)
        self._clear(title, nav, expanded, expansions, collected, arrow, caption)

    def _show_second_order_forcing(self):
        nav = self._nav(18)
        title = self._title("The first-order solution now becomes the forcing")

        x_min, x_max = -3.35, 3.35
        base_axis = self._axis_line(x_min, x_max, 0)
        eta_first = self._wave_graph(lambda x: 0.34 * np.cos(1.55 * x), x_min, x_max, 0, SURFACE, 4)
        phi_x_first = self._wave_graph(lambda x: 0.34 * np.cos(1.55 * x), x_min, x_max, -1.05, GREEN, 4)
        product = self._wave_graph(
            lambda x: 0.36 * (np.cos(1.55 * x) ** 2),
            x_min,
            x_max,
            -2.1,
            ACCENT,
            4,
        )
        axes = VGroup(base_axis, self._axis_line(x_min, x_max, -1.05), self._axis_line(x_min, x_max, -2.1))
        waves = VGroup(axes, eta_first, phi_x_first, product)
        waves.to_edge(LEFT, buff=0.62).shift(UP * 0.25)

        labels = VGroup(
            MathTex(r"\eta^{(1)}", font_size=32, color=SURFACE),
            MathTex(r"\phi^{(1)}_x", font_size=32, color=GREEN),
            MathTex(r"\eta^{(1)}\phi^{(1)}_x", font_size=29, color=ACCENT),
        )
        label_x = waves.get_left()[0] + 0.92
        labels[0].move_to([label_x, eta_first.get_y() + 0.12, 0])
        labels[1].move_to([label_x, phi_x_first.get_y() + 0.12, 0])
        labels[2].move_to([label_x + 0.28, product.get_y() + 0.12, 0])
        z0_labels = VGroup(
            MathTex(r"z=0", font_size=21, color=MUTED).next_to(axes[0], RIGHT, buff=0.08),
            MathTex(r"z=0", font_size=21, color=MUTED).next_to(axes[1], RIGHT, buff=0.08),
            MathTex(r"z=0", font_size=21, color=MUTED).next_to(axes[2], RIGHT, buff=0.08),
        )

        right = VGroup(
            self._text("same phase at the surface", font_size=25, color=MUTED),
            MathTex(r"\eta^{(1)}=a\cos\theta", font_size=34, color=SURFACE),
            MathTex(r"\phi^{(1)}_x\propto \cos\theta", font_size=34, color=GREEN),
            self._text("their product has a mean plus a double phase", font_size=24, color=MUTED),
            MathTex(r"\eta^{(1)}\phi^{(1)}_x\propto \cos^2\theta", font_size=33, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        right.to_edge(RIGHT, buff=0.24).shift(UP * 0.28)

        trig = MathTex(
            r"\cos\theta\,\cos\theta=\frac12+\frac12\cos(2\theta)",
            font_size=41,
            color=ACCENT,
        )
        trig.to_edge(DOWN, buff=1.04)
        product_mean_y = axes[2].get_y() + 0.18
        mean_marker = DashedLine(
            [product.get_left()[0], product_mean_y, 0],
            [product.get_right()[0], product_mean_y, 0],
            color=PURPLE,
            stroke_width=2,
            dash_length=0.12,
        )
        mean_label = MathTex(r"\frac12", font_size=27, color=PURPLE)
        mean_label.next_to(mean_marker, UP, buff=0.16).align_to(mean_marker, RIGHT).shift(LEFT * 0.62)
        phase_label = MathTex(r"\cos(2\theta)", font_size=25, color=ACCENT)
        phase_label.move_to([product.get_center()[0] + 1.45, product.get_y() + 0.44, 0])

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(VGroup(axes[:2], eta_first, phi_x_first, labels[:2], z0_labels[:2])), run_time=0.55)
        self._play_step(FadeIn(right[:3]), run_time=0.45)
        self._play_step(FadeIn(VGroup(axes[2], product, labels[2], z0_labels[2])), FadeIn(right[3:]), run_time=0.55)
        self._play_step(FadeIn(trig), FadeIn(mean_marker), FadeIn(mean_label), FadeIn(phase_label), run_time=0.55)
        self._clear(title, nav, waves, labels, z0_labels, right, trig, mean_marker, mean_label, phase_label)

    def _show_bound_harmonic(self):
        nav = self._nav(19)
        title = self._title("A monochromatic wave creates a bound second harmonic")

        x_min, x_max = -3.15, 3.15
        theta = lambda x: 3.0 * x
        linear = self._wave_graph(lambda x: 0.52 * np.cos(theta(x)), x_min, x_max, 1.12, SURFACE, 4)
        harmonic = self._wave_graph(lambda x: 0.10 * np.cos(2 * theta(x)), x_min, x_max, 0.02, ACCENT, 4)
        mean_shift = Line([x_min, 0.02 - 0.12, 0], [x_max, 0.02 - 0.12, 0], color=PURPLE, stroke_width=3)
        combined = self._wave_graph(
            lambda x: 0.52 * np.cos(theta(x)) + 0.10 * np.cos(2 * theta(x)),
            x_min,
            x_max,
            -1.25,
            GREEN,
            3,
        )
        linear_reference = self._wave_graph(lambda x: 0.52 * np.cos(theta(x)), x_min, x_max, -1.25, SURFACE, 2.4)
        linear_reference.set_stroke(opacity=0.58)
        linear_reference.set_fill(opacity=0)
        axes = VGroup(
            self._axis_line(x_min, x_max, 1.12),
            self._axis_line(x_min, x_max, 0.02),
            self._axis_line(x_min, x_max, -1.25),
        )
        graphs = VGroup(axes, linear, harmonic, mean_shift, linear_reference, combined)
        graphs.to_edge(LEFT, buff=0.62).shift(UP * 0.1)

        graph_labels = VGroup(
            MathTex(r"a\cos\theta", font_size=27, color=SURFACE),
            MathTex(r"\text{mean shift }+\ 2k", font_size=20, color=ACCENT),
            MathTex(r"\eta_{\mathrm{lin}}\ \text{ and }\ \eta_{\mathrm{Stokes}}", font_size=20, color=GREEN),
        )
        label_x = graphs.get_left()[0] + 0.96
        graph_labels[0].move_to([label_x, linear.get_y() + 0.58, 0])
        graph_labels[1].move_to([label_x, harmonic.get_y() + 0.33, 0])
        graph_labels[2].move_to([label_x, combined.get_y() + 0.58, 0])

        equation = VGroup(
            MathTex(r"\theta=kx-\omega t\quad(\text{larger }k\text{ shown})", font_size=31, color=MUTED),
            MathTex(
                r"\eta=a\cos\theta+a^2C_0+a^2C_2(k,h)\cos(2\theta)+O(a^3)",
                font_size=28,
                color=FG,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        equation.to_edge(RIGHT, buff=0.20).shift(UP * 0.74)

        meaning = VGroup(
            MathTex(r"\text{phase: }2\theta", font_size=31, color=ACCENT),
            MathTex(r"\text{bound wavenumber: }2k", font_size=31, color=ACCENT),
            MathTex(r"\text{frequency: }2\omega", font_size=31, color=ACCENT),
            MathTex(r"\text{monochromatic subharmonic: mean set-down}", font_size=24, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        meaning.next_to(equation, DOWN, buff=0.35).align_to(equation, LEFT)
        caption = self._caption("The second harmonic sharpens crests and flattens troughs because its phase is locked.", font_size=24)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(VGroup(graphs, graph_labels)), run_time=0.65)
        self._play_step(FadeIn(equation), run_time=0.45)
        self._play_step(FadeIn(meaning), FadeIn(caption), run_time=0.45)
        self._clear(title, nav, graphs, graph_labels, equation, meaning, caption)

    def _show_free_versus_bound(self):
        nav = self._nav(20)
        title = self._title("Linear Dispersion Relation and Second-Order Bound Wave Dispersion")

        k_axis = Line([-4.8, -1.0, 0], [4.8, -1.0, 0], color=MUTED, stroke_width=2)
        w_axis = Line([-4.4, -1.25, 0], [-4.4, 2.5, 0], color=MUTED, stroke_width=2)
        k_label = MathTex(r"K", font_size=28, color=MUTED).next_to(k_axis, RIGHT, buff=0.08)
        w_label = MathTex(r"\Omega", font_size=28, color=MUTED).next_to(w_axis, UP, buff=0.08)
        free_coeff = 0.85
        free_curve = FunctionGraph(
            lambda x: -1.0 + free_coeff * np.sqrt(max(x + 4.35, 0)),
            x_range=[-4.35, 4.2],
            color=SURFACE,
            stroke_width=4,
        )
        bound_curve = FunctionGraph(
            lambda x: -1.0 + 1.12 * np.sqrt(max(x + 4.35, 0)),
            x_range=[-4.35, 4.2],
            color=ACCENT,
            stroke_width=4,
        )
        curve_label = MathTex(r"\Omega^2=gK\tanh(Kh)", font_size=20, color=SURFACE)
        curve_label.move_to([1.55, 0.06, 0])
        bound_curve_label = MathTex(r"\Omega^2=2gK\tanh(Kh/2)", font_size=20, color=ACCENT)
        bound_curve_label.move_to([2.10, 2.42, 0])

        primary_x = -2.25
        primary_y = -1.0 + free_coeff * np.sqrt(primary_x + 4.35)
        primary = Dot([primary_x, primary_y, 0], radius=0.085, color=GREEN)
        primary_label = MathTex(r"(k,\omega)", font_size=28, color=GREEN).next_to(primary, UP, buff=0.08)
        free_second_x = 0.45
        free_second = Dot([free_second_x, -1.0 + free_coeff * np.sqrt(free_second_x + 4.35), 0], radius=0.07, color=MUTED)
        free_label = MathTex(r"\text{free at }K=2k", font_size=22, color=MUTED).next_to(free_second, DOWN, buff=0.08)
        bound_second = Dot([0.45, 1.46, 0], radius=0.09, color=ACCENT)
        bound_label = MathTex(r"(2k,2\omega)", font_size=25, color=ACCENT)
        bound_label.next_to(bound_second, DOWN, buff=0.10).shift(RIGHT * 0.24)
        lock_arrow = Arrow(primary.get_center(), bound_second.get_center(), color=ACCENT, buff=0.14, stroke_width=4)
        dispersion_gap = DashedLine(free_second.get_center(), bound_second.get_center(), color=RED, stroke_width=2, dash_length=0.1)

        plot = VGroup(
            k_axis,
            w_axis,
            k_label,
            w_label,
            free_curve,
            bound_curve,
            curve_label,
            bound_curve_label,
            primary,
            primary_label,
            free_second,
            free_label,
            bound_second,
            bound_label,
            lock_arrow,
            dispersion_gap,
        )
        plot.to_edge(LEFT, buff=0.24).shift(UP * 0.02)

        right = VGroup(
            MathTex(r"\text{free wave at }(K,\Omega):", font_size=25, color=MUTED),
            MathTex(r"\Omega^2=gK\tanh(Kh)", font_size=30, color=SURFACE),
            MathTex(r"\text{bound }n\text{th harmonic: }(K,\Omega)=(nk,n\omega)", font_size=25, color=MUTED),
            MathTex(r"\omega^2=gk\tanh(kh)", font_size=28, color=GREEN),
            MathTex(r"\Omega^2=n^2\omega^2=n\,gK\tanh(Kh/n)", font_size=27, color=ACCENT),
            MathTex(r"\text{for }n=2:\ \Omega^2=2gK\tanh(Kh/2)", font_size=25, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if right.width > 4.05:
            right.scale_to_fit_width(4.05)
        right.to_edge(RIGHT, buff=0.20).shift(UP * 0.42)
        caption = self._caption("Bound waves inherit the linear group velocity, but not the free-wave dispersion relation.", font_size=22)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(VGroup(k_axis, w_axis, k_label, w_label, free_curve, curve_label)), run_time=0.55)
        self._play_step(FadeIn(VGroup(primary, primary_label)), run_time=0.3)
        self._play_step(FadeIn(VGroup(free_second, free_label)), run_time=0.3)
        self._play_step(
            GrowArrow(lock_arrow),
            FadeIn(VGroup(bound_curve, bound_curve_label, bound_second, bound_label, dispersion_gap)),
            run_time=0.55,
        )
        self._play_step(FadeIn(right[:2]), run_time=0.35)
        self._play_step(FadeIn(right[2:]), FadeIn(caption), run_time=0.45)
        self._clear(title, nav, plot, right, caption)

    def _show_two_component_interactions(self):
        nav = self._nav(21)
        title = self._title("A bichromatic wave produces pairwise bound components")

        x_min, x_max = -3.05, 3.05
        k1 = 1.85
        k2 = 3.15
        phase = 0.55
        rows = [1.42, 0.58, -0.26, -1.10]
        colors = [SURFACE, PURPLE, GREEN, ACCENT]
        funcs = [
            lambda x: 0.22 * np.cos(k1 * x),
            lambda x: 0.22 * np.cos(k2 * x + phase),
            lambda x: 0.13 * np.cos((k1 + k2) * x + phase),
            lambda x: 0.13 * np.cos((k2 - k1) * x + phase),
        ]
        labels = [
            r"k_1",
            r"k_2",
            r"k_1+k_2",
            r"k_2-k_1",
        ]
        plot_rows = VGroup()
        row_labels = VGroup()
        for y, color, func, label in zip(rows, colors, funcs, labels):
            axis = self._axis_line(x_min, x_max, y)
            wave = self._wave_graph(func, x_min, x_max, y, color, 3.4)
            plot_rows.add(VGroup(axis, wave))
            row_labels.add(MathTex(label, font_size=24, color=color).next_to(axis, RIGHT, buff=0.10))
        plot_rows.to_edge(LEFT, buff=0.42).shift(UP * 0.15)
        for label, row in zip(row_labels, plot_rows):
            label.next_to(row[0], RIGHT, buff=0.10)
        plot_group = VGroup(plot_rows, row_labels)

        formula = VGroup(
            MathTex(r"\theta_j=k_jx-\omega_jt+\alpha_j", font_size=28, color=MUTED),
            MathTex(r"\eta^{(1)}=a_1\cos\theta_1+a_2\cos\theta_2", font_size=30, color=FG),
            MathTex(
                r"\cos\theta_1\cos\theta_2=\frac12\cos(\theta_1+\theta_2)+\frac12\cos(\theta_1-\theta_2)",
                font_size=24,
                color=ACCENT,
            ),
            MathTex(r"(K_+,\Omega_+)=(k_1+k_2,\omega_1+\omega_2)", font_size=24, color=GREEN),
            MathTex(r"(K_-,\Omega_-)=(k_2-k_1,\omega_2-\omega_1)", font_size=24, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        if formula.width > 5.45:
            formula.scale_to_fit_width(5.45)
        formula.to_edge(RIGHT, buff=0.18).shift(UP * 0.55)

        caption = self._caption("Stokes starts from one phase; a bichromatic wave creates sum and difference phases.", font_size=23)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(VGroup(plot_rows[:2], row_labels[:2])), FadeIn(formula[:2]), run_time=0.65)
        self._play_step(FadeIn(formula[2]), run_time=0.45)
        self._play_step(FadeIn(VGroup(plot_rows[2:], row_labels[2:], formula[3:])), FadeIn(caption), run_time=0.55)
        self._clear(title, nav, plot_group, formula, caption)

    def _show_bound_wave_summary(self):
        nav = self._nav(23)
        title = self._title("Bound response travels with the wave group")

        xs = np.linspace(-5.25, 5.25, 360)
        x_min, x_max = -5.25, 5.25
        group_progress = ValueTracker(0.0)
        k0 = 5.1
        g_visual = 1.0
        k_values = k0 + np.linspace(-0.78, 0.78, 11)
        omega_values = np.sqrt(g_visual * k_values)
        amplitudes = np.exp(-0.5 * ((k_values - k0) / 0.38) ** 2)
        amplitudes = 0.40 * amplitudes / np.sum(amplitudes)
        start_center = -0.82
        end_center = 0.72
        cg0 = np.sqrt(g_visual * k0) / (2.0 * k0)
        t_end = (end_center - start_center) / cg0
        focus_phases = -k_values * start_center

        def current_time():
            return t_end * group_progress.get_value()

        def current_center():
            return start_center + cg0 * current_time()

        def theta_components(x, time):
            return np.outer(k_values, x) - omega_values[:, None] * time + focus_phases[:, None]

        def component_values(order, time):
            center = current_center()
            local = xs - center
            envelope = np.exp(-0.5 * (local / 1.72) ** 2)
            theta = theta_components(xs, time)
            if order == 1:
                return np.sum(amplitudes[:, None] * np.cos(theta), axis=0)
            if order == 2:
                bound_plus = np.zeros_like(xs)
                norm = 0.0
                for i, amp_i in enumerate(amplitudes):
                    for j, amp_j in enumerate(amplitudes):
                        coeff = amp_i * amp_j
                        bound_plus += coeff * np.cos(theta[i] + theta[j])
                        norm += coeff
                return 0.20 * bound_plus / max(norm, 1e-9) - 0.045 * envelope**2
            return 0.0 * xs

        static_rows = VGroup()
        moving_rows = VGroup()
        for y, order, color, label in [
            (0.78, 1, SURFACE, r"\eta^{(1)}"),
            (-0.16, 2, ACCENT, r"\eta^{(2)}_{\rm bound}"),
            (-1.18, 0, GREEN, r"\eta^{(1)}+\eta^{(2)}_{\rm bound}"),
        ]:
            axis = self._axis_line(x_min, x_max, y)
            tag = MathTex(label, font_size=25, color=color).next_to(axis, RIGHT, buff=0.12)
            static_rows.add(VGroup(axis, tag))

            def make_curve(base_y=y, component_order=order, curve_color=color):
                time = current_time()
                if component_order == 0:
                    values = component_values(1, time) + component_values(2, time)
                else:
                    values = component_values(component_order, time)
                return self._polyline_from_samples(xs, base_y + values, color=curve_color, stroke_width=3.3)

            moving_rows.add(always_redraw(make_curve))

        def moving_envelope(sign):
            center = current_center()
            local = xs - center
            envelope = 0.40 * np.exp(-0.5 * (local / 1.72) ** 2) * (1.0 + 0.12 * np.cos(0.86 * local))
            return self._polyline_from_samples(xs, 0.78 + sign * envelope, color=MUTED, stroke_width=1.5, opacity=0.50)

        envelope_guides = VGroup(always_redraw(lambda: moving_envelope(1)), always_redraw(lambda: moving_envelope(-1)))
        crest_marker = always_redraw(
            lambda: DashedLine(
                [current_center(), -1.74, 0],
                [current_center(), 1.16, 0],
                color=FG,
                stroke_width=1.4,
                dash_length=0.10,
            ).set_opacity(0.55)
        )
        travel_arrow = Arrow([-1.00, -0.72, 0], [0.28, -0.72, 0], color=FG, buff=0.03, stroke_width=3)
        cg_label = MathTex(r"c_g", font_size=25, color=FG).next_to(travel_arrow, LEFT, buff=0.12)
        dispersion_note = VGroup(
            MathTex(r"\eta^{(1)}=\sum_j a_j\cos(k_jx-\omega_jt+\alpha_j)", font_size=24, color=SURFACE),
            MathTex(r"\omega_j^2=gk_j", font_size=25, color=ACCENT),
            MathTex(r"\eta^{(2)+}\sim\sum_{m,n}\cos(\theta_m+\theta_n)", font_size=23, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([0.0, -2.24, 0])
        if dispersion_note.width > 8.7:
            dispersion_note.scale_to_fit_width(8.7)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(VGroup(static_rows, moving_rows, envelope_guides, crest_marker)), run_time=0.60)
        self._play_step(FadeIn(VGroup(travel_arrow, cg_label)), FadeIn(dispersion_note), run_time=0.40)
        self.play(group_progress.animate.set_value(1.0), run_time=3.20, rate_func=linear)
        self._pause()
        self.remove(title, nav, static_rows, moving_rows, envelope_guides, crest_marker, travel_arrow, cg_label, dispersion_note)

    def _show_bound_wave_visual_summary(self):
        nav = self._nav(23)
        title = self._title("Bound components: waveform and spectrum")

        k0 = 1.50
        amp = 0.34
        width = 3.60

        def group_env(x):
            return np.exp(-x**2 / (2.0 * width**2))

        def theta(x):
            return k0 * x

        def eta11(x):
            return amp * group_env(x) * np.cos(theta(x))

        def eta22(x):
            return 0.5 * k0 * amp**2 * group_env(x) ** 2 * np.cos(2.0 * theta(x)) - 0.5 * k0 * amp**2 * group_env(x) ** 2

        def eta33(x):
            return (3.0 * k0**2 / 8.0) * amp**3 * group_env(x) ** 3 * np.cos(3.0 * theta(x))

        def eta44(x):
            return 0.010 * group_env(x) ** 4 * np.cos(4.0 * theta(x))

        def gaussian(k, center, sigma, height):
            return height * np.exp(-0.5 * ((k - center) / sigma) ** 2)

        ax_x = Axes(
            x_range=[-10, 10, 5],
            y_range=[-0.45, 0.45, 0.20],
            x_length=6.50,
            y_length=2.70,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"numbers_to_include": [-10, 0, 10], "font_size": 20},
            y_axis_config={"numbers_to_include": [-0.2, 0, 0.2], "font_size": 18},
        ).to_edge(LEFT, buff=0.62).shift(UP * 0.30)
        ax_k = Axes(
            x_range=[0, 6.4, 1.5],
            y_range=[0, 1.15, 0.5],
            x_length=4.55,
            y_length=2.70,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.58).shift(UP * 0.30)
        axes_labels = VGroup(
            ax_x.get_x_axis_label(MathTex("x", font_size=24, color=FG)),
            ax_x.get_y_axis_label(MathTex(r"\eta", font_size=24, color=FG)),
            ax_k.get_x_axis_label(MathTex("k", font_size=24, color=FG)),
            ax_k.get_y_axis_label(MathTex(r"|\hat\eta|", font_size=24, color=FG)),
        )
        heads = VGroup(
            Text("wave group", font_size=23, color=MUTED).next_to(ax_x, UP, buff=0.16),
            Text("wavenumber spectrum", font_size=23, color=MUTED).next_to(ax_k, UP, buff=0.16),
        )

        wave_11 = ax_x.plot(eta11, x_range=[-10, 10, 0.04], color=SURFACE, stroke_width=2.9)
        wave_22 = ax_x.plot(eta22, x_range=[-10, 10, 0.04], color=ACCENT, stroke_width=2.5)
        wave_33 = ax_x.plot(eta33, x_range=[-10, 10, 0.04], color=PURPLE, stroke_width=2.4)
        wave_44 = ax_x.plot(eta44, x_range=[-10, 10, 0.04], color=FG, stroke_width=1.8, stroke_opacity=0.58)
        env_u = ax_x.plot(lambda x: amp * group_env(x), x_range=[-10, 10, 0.08], color=BLUE_A, stroke_width=1.1, stroke_opacity=0.42)
        env_l = ax_x.plot(lambda x: -amp * group_env(x), x_range=[-10, 10, 0.08], color=BLUE_A, stroke_width=1.1, stroke_opacity=0.42)

        spec_11 = ax_k.plot(lambda k: gaussian(k, k0, 0.32, 1.0), x_range=[0.02, 6.4, 0.02], color=SURFACE, stroke_width=2.8)
        spec_20 = ax_k.plot(lambda k: gaussian(k, 0.25, 0.30, 0.26), x_range=[0.02, 1.30, 0.02], color=GREEN, stroke_width=2.2)
        spec_22 = ax_k.plot(lambda k: gaussian(k, 2 * k0, 0.38, 0.44), x_range=[0.02, 6.4, 0.02], color=ACCENT, stroke_width=2.6)
        spec_33 = ax_k.plot(lambda k: gaussian(k, 3 * k0, 0.42, 0.22), x_range=[0.02, 6.4, 0.02], color=PURPLE, stroke_width=2.5)
        spec_44 = ax_k.plot(lambda k: gaussian(k, 4 * k0, 0.45, 0.10), x_range=[0.02, 6.4, 0.02], color=FG, stroke_width=1.9, stroke_opacity=0.58)
        labels = VGroup(
            MathTex(r"\eta_{11}", font_size=26, color=SURFACE).move_to(ax_x.c2p(-8.2, 0.31)),
            MathTex(r"\eta_{22}", font_size=26, color=ACCENT).move_to(ax_x.c2p(-8.2, -0.22)),
            MathTex(r"\eta_{33}", font_size=26, color=PURPLE).move_to(ax_x.c2p(7.1, 0.16)),
            MathTex(r"\eta_{44},\eta_{55},\ldots", font_size=24, color=FG).move_to(ax_x.c2p(5.9, -0.30)),
            MathTex(r"k_0", font_size=22, color=SURFACE).next_to(ax_k.c2p(k0, 0), DOWN, buff=0.08),
            MathTex(r"k\approx0", font_size=18, color=GREEN).next_to(ax_k.c2p(0.25, 0), DOWN + RIGHT * 0.18, buff=0.08),
            MathTex(r"2k_0", font_size=22, color=ACCENT).next_to(ax_k.c2p(2 * k0, 0), DOWN, buff=0.08),
            MathTex(r"3k_0", font_size=22, color=PURPLE).next_to(ax_k.c2p(3 * k0, 0), DOWN, buff=0.08),
            MathTex(r"4k_0,\ldots", font_size=20, color=FG).next_to(ax_k.c2p(4 * k0, 0), DOWN, buff=0.08),
        )
        connector = VGroup(
            Arrow([-0.38, 0.18, 0], [0.54, 0.18, 0], color=MUTED, buff=0.04, stroke_width=2.4),
            MathTex(r"\mathcal{F}", font_size=25, color=MUTED).move_to([0.08, 0.43, 0]),
        )
        phase_lock = VGroup(
            MathTex(r"\theta=k_0x-\omega_0t", font_size=23, color=MUTED),
            MathTex(r"\eta_{22}^{+}\propto \cos(2\theta)", font_size=25, color=ACCENT),
        ).arrange(DOWN, buff=0.05).next_to(ax_x, DOWN, buff=0.28)
        dispersion_lock = VGroup(
            MathTex(r"k=2k_0", font_size=22, color=ACCENT),
            MathTex(r"\omega_{\rm bound}=2\omega_0", font_size=22, color=ACCENT),
            MathTex(r"\neq\,\Omega(2k_0)", font_size=21, color=MUTED),
        ).arrange(DOWN, buff=0.02).next_to(ax_k, DOWN, buff=0.22)
        free_relation = VGroup(
            DashedLine(
                ax_k.c2p(2 * k0, 0.0),
                ax_k.c2p(2 * k0, 0.47),
                color=MUTED,
                stroke_width=1.5,
                dash_length=0.08,
                stroke_opacity=0.55,
            ),
            Dot(ax_k.c2p(2 * k0, 0.61), radius=0.040, color=MUTED).set_opacity(0.70),
            MathTex(r"\Omega(2k_0)", font_size=18, color=MUTED).next_to(ax_k.c2p(2 * k0, 0.61), UP, buff=0.05),
            Dot(ax_k.c2p(2 * k0, 0.44), radius=0.052, color=ACCENT),
        )
        caption = self._caption("Second order adds bound components; higher orders continue the same pattern.", font_size=23)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(Create(ax_x), Create(ax_k), FadeIn(axes_labels), FadeIn(heads), FadeIn(connector), run_time=0.60)
        self._play_step(Create(wave_11), Create(env_u), Create(env_l), Create(spec_11), FadeIn(VGroup(labels[0], labels[4])), run_time=0.65)
        self._play_step(
            Create(wave_22),
            Create(spec_20),
            Create(spec_22),
            FadeIn(VGroup(labels[1], labels[5], labels[6])),
            FadeIn(phase_lock),
            FadeIn(dispersion_lock),
            FadeIn(free_relation),
            run_time=0.65,
        )
        self._play_step(Create(wave_33), Create(spec_33), FadeIn(VGroup(labels[2], labels[7])), run_time=0.55)
        self._play_step(Create(wave_44), Create(spec_44), FadeIn(VGroup(labels[3], labels[8])), FadeIn(caption), run_time=0.55)
        self._clear(
            title,
            nav,
            ax_x,
            ax_k,
            axes_labels,
            heads,
            wave_11,
            wave_22,
            wave_33,
            wave_44,
            env_u,
            env_l,
            spec_11,
            spec_20,
            spec_22,
            spec_33,
            spec_44,
            labels,
            connector,
            phase_lock,
            dispersion_lock,
            free_relation,
            caption,
        )

    def _show_closing_picture(self):
        nav = self._nav(24)
        title = self._title("The picture to keep")

        top_xs = [-4.95, -1.65, 1.65, 4.95]
        bottom_xs = [-3.30, 0.0, 3.30]
        top_y = 1.42
        bottom_y = 0.62

        def flow_box(x, y, top, bottom, color, width=2.35):
            box = RoundedRectangle(
                width=width,
                height=0.58,
                corner_radius=0.08,
                color=color,
                stroke_width=2.1,
            ).set_fill(color, opacity=0.075).move_to([x, y, 0])
            words = VGroup(
                MathTex(top, font_size=20, color=color),
                MathTex(bottom, font_size=20, color=color),
            ).arrange(DOWN, buff=0.02).move_to(box)
            return VGroup(box, words)

        top_nodes = VGroup(
            flow_box(top_xs[0], top_y, r"\text{free-surface}", r"\text{BCs}", SURFACE),
            flow_box(top_xs[1], top_y, r"\text{linearize}", r"\eta_{11},\phi_{11}", MUTED),
            flow_box(top_xs[2], top_y, r"\text{quadratic}", r"\text{forcing}", ACCENT),
            flow_box(top_xs[3], top_y, r"\text{monochromatic}", r"\text{2nd order}", ACCENT),
        )
        bottom_nodes = VGroup(
            flow_box(bottom_xs[0], bottom_y, r"\text{bichromatic}", r"k_m\pm k_n", GREEN),
            flow_box(bottom_xs[1], bottom_y, r"\text{wave group}", r"\eta_{20},\eta_{22}", FG),
            flow_box(bottom_xs[2], bottom_y, r"\text{higher order}", r"\eta_{33},\eta_{44},\ldots", PURPLE),
        )
        nodes = VGroup(top_nodes, bottom_nodes)
        arrows = VGroup(
            *[
                Arrow([top_xs[i] + 1.22, top_y, 0], [top_xs[i + 1] - 1.22, top_y, 0], color=MUTED, buff=0.02, stroke_width=2.1, tip_length=0.12)
                for i in range(len(top_xs) - 1)
            ],
            Arrow([top_xs[-1], top_y - 0.34, 0], [bottom_xs[0] + 1.10, bottom_y + 0.34, 0], color=MUTED, buff=0.02, stroke_width=2.1, tip_length=0.12),
            Arrow([bottom_xs[0] + 1.22, bottom_y, 0], [bottom_xs[1] - 1.22, bottom_y, 0], color=MUTED, buff=0.02, stroke_width=2.1, tip_length=0.12),
            Arrow([bottom_xs[1] + 1.22, bottom_y, 0], [bottom_xs[2] - 1.22, bottom_y, 0], color=MUTED, buff=0.02, stroke_width=2.1, tip_length=0.12),
        )

        travel = ValueTracker(0.0)
        xs = np.linspace(-5.15, 1.85, 380)
        wave_y = -0.50

        def env(x, center):
            return np.exp(-0.5 * ((x - center) / 1.35) ** 2)

        def parts(progress):
            center = -1.65
            phase = -1.35 * TAU * progress
            envelope = env(xs, center)
            eta11 = 0.30 * envelope * np.cos(4.9 * (xs - center) + phase)
            eta22 = 0.095 * envelope**2 * np.cos(9.8 * (xs - center) + 2.0 * phase)
            eta20 = -0.075 * envelope**2
            return eta11, eta22, eta20, eta11 + eta22 + eta20

        wave_parts = VGroup(
            always_redraw(lambda: self._polyline_from_samples(xs, wave_y + parts(travel.get_value())[0], color=SURFACE, stroke_width=2.1, opacity=0.80)),
            always_redraw(lambda: self._polyline_from_samples(xs, wave_y + parts(travel.get_value())[1], color=ACCENT, stroke_width=2.0, opacity=0.86)),
            always_redraw(lambda: self._polyline_from_samples(xs, wave_y + parts(travel.get_value())[2], color=GREEN, stroke_width=2.0, opacity=0.86)),
            always_redraw(lambda: self._polyline_from_samples(xs, wave_y - 0.52 + parts(travel.get_value())[3], color=FG, stroke_width=2.8)),
        )
        wave_labels = VGroup(
            MathTex(r"\eta_{11}", font_size=24, color=SURFACE).move_to([-5.75, wave_y + 0.20, 0]),
            MathTex(r"\eta_{22}", font_size=24, color=ACCENT).move_to([-5.75, wave_y - 0.04, 0]),
            MathTex(r"\eta_{20}", font_size=24, color=GREEN).move_to([-5.75, wave_y - 0.27, 0]),
            MathTex(r"\eta", font_size=25, color=FG).move_to([-5.75, wave_y - 0.58, 0]),
            MathTex(r"\xi=x-c_g t", font_size=21, color=MUTED).move_to([0.86, wave_y - 0.84, 0]),
        )

        kxs = np.linspace(0.0, 7.0, 360)
        spec_base_y = -1.58
        spec_left = 2.35
        spec_width = 3.55

        def spec_map(k, val):
            return spec_left + spec_width * (k / 7.0), spec_base_y + val

        def spec_curve(center, sigma, height, color, k_min=0.0, k_max=7.0, stroke_width=2.5):
            local_k = np.linspace(k_min, k_max, 260)
            ys = height * np.exp(-0.5 * ((local_k - center) / sigma) ** 2)
            pts_x = spec_left + spec_width * (local_k / 7.0)
            return self._polyline_from_samples(pts_x, spec_base_y + ys, color=color, stroke_width=stroke_width)

        spectrum_axis = VGroup(
            Line([spec_left, spec_base_y, 0], [spec_left + spec_width, spec_base_y, 0], color=MUTED, stroke_width=1.8),
            Line([spec_left, spec_base_y, 0], [spec_left, spec_base_y + 1.02, 0], color=MUTED, stroke_width=1.8),
            MathTex(r"k", font_size=21, color=MUTED).move_to([spec_left + spec_width + 0.17, spec_base_y - 0.03, 0]),
            MathTex(r"|\hat\eta|", font_size=19, color=MUTED).rotate(PI / 2).move_to([spec_left - 0.24, spec_base_y + 0.72, 0]),
        )
        spectrum = VGroup(
            spectrum_axis,
            spec_curve(3.05, 0.46, 0.88, SURFACE),
            spec_curve(0.30, 0.55, 0.38, GREEN, k_min=0.0, k_max=2.0),
            spec_curve(6.10, 0.58, 0.46, ACCENT),
            spec_curve(6.75, 0.42, 0.18, PURPLE, k_min=5.2, k_max=7.0, stroke_width=2.0),
        )
        for k, lab, color in [
            (0.28, r"0", GREEN),
            (3.05, r"k_p", SURFACE),
            (6.10, r"2k_p", ACCENT),
        ]:
            x_pos, _ = spec_map(k, 0)
            spectrum.add(MathTex(lab, font_size=20, color=color).next_to([x_pos, spec_base_y, 0], DOWN, buff=0.06))
        spectrum.add(MathTex(r"\text{wave-group spectra}", font_size=19, color=MUTED).move_to([4.28, -0.53, 0]))
        equation = MathTex(
            r"\eta=\eta_{11}+\eta_{20}+\eta_{22}+\eta_{33}+\cdots",
            font_size=36,
            color=FG,
        ).move_to([0, -2.12, 0])
        equation.set_color_by_tex(r"\eta_{11}", SURFACE)
        equation.set_color_by_tex(r"\eta_{20}", GREEN)
        equation.set_color_by_tex(r"\eta_{22}", ACCENT)
        equation.set_color_by_tex(r"\eta_{33}", PURPLE)

        closing_note = VGroup(
            Tex(r"\text{Physical space: bound harmonics reshape the travelling group.}", font_size=23, color=FG),
            Tex(r"\text{Spectral space: the same sum/difference branches form grouped spectra.}", font_size=23, color=FG),
        ).arrange(DOWN, buff=0.05).move_to([0, -2.70, 0])
        closing_note.scale_to_fit_width(10.5)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(nodes), FadeIn(arrows), run_time=0.65)
        self._play_step(FadeIn(wave_labels), Create(wave_parts), Create(spectrum), run_time=0.75)
        self.play(travel.animate.set_value(1.0), run_time=3.4, rate_func=linear)
        self._pause()
        self._play_step(FadeIn(equation), FadeIn(closing_note), run_time=0.70)
        self._clear(title, nav, nodes, arrows, wave_parts, wave_labels, spectrum, equation, closing_note)

    def _wave_group_profile(self, x, phase=0.0, center=0.0, width=1.65, carrier=5.1, amp=0.40):
        envelope = np.exp(-0.5 * ((x - center) / width) ** 2)
        sideband = 0.18 * np.cos(0.72 * (x - center) - 0.5 * phase)
        return amp * envelope * (1.0 + sideband) * np.cos(carrier * (x - center) + phase)

    def _polyline_from_samples(self, xs, ys, color=SURFACE, stroke_width=3.0, opacity=1.0):
        graph = VMobject()
        graph.set_points_as_corners([np.array([x, y, 0.0]) for x, y in zip(xs, ys)])
        graph.set_style(
            stroke_color=color,
            stroke_width=stroke_width,
            stroke_opacity=opacity,
            fill_opacity=0.0,
        )
        return graph

    def _spectrum_stems(self, positions, heights, colors, y0=-1.58, scale=0.66):
        axis = Line([-3.0, y0, 0], [3.0, y0, 0], color=MUTED, stroke_width=2)
        stems = VGroup(axis)
        for x, h, color in zip(positions, heights, colors):
            stems.add(Line([x, y0, 0], [x, y0 + scale * h, 0], color=color, stroke_width=5))
        return stems

    def _component_wave(self, x, components, count=None, phase=0.0):
        active = components if count is None else components[:count]
        return sum(a * np.cos(k * x + phi + phase * (0.45 + 0.06 * i)) for i, (a, k, phi) in enumerate(active))

    def _large_crest_average_data(self):
        rng = np.random.default_rng(37)
        xs = np.linspace(0.0, 176.0, 6400)
        ks = np.linspace(2.10, 8.40, 160)
        envelope = np.exp(-0.5 * ((ks - 4.65) / 1.05) ** 2)
        envelope += 0.34 * np.exp(-0.5 * ((ks - 6.55) / 0.58) ** 2)
        envelope += 0.18 * np.exp(-0.5 * ((ks - 3.10) / 0.38) ** 2)
        envelope *= rng.rayleigh(scale=1.0, size=len(ks))
        envelope *= 1.0 + 0.22 * rng.normal(size=len(ks))
        envelope = np.maximum(envelope, 0.0)
        envelope = envelope / np.max(envelope)
        phases = rng.uniform(0.0, 2 * np.pi, len(ks))
        sea = np.zeros_like(xs)
        for amp, k, phi in zip(envelope, ks, phases):
            sea += amp * np.cos(k * xs + phi)
        sea = sea / np.max(np.abs(sea))

        maxima = np.where((sea[1:-1] > sea[:-2]) & (sea[1:-1] > sea[2:]))[0] + 1
        maxima = maxima[sea[maxima] > 0.06]
        if len(maxima) > 120:
            order = np.linspace(0, len(maxima) - 1, 120).astype(int)
            crest_indices = maxima[order]
        else:
            crest_indices = maxima
        large_count = max(1, len(crest_indices) // 3)
        largest = crest_indices[np.argsort(sea[crest_indices])[-large_count:]]
        largest = largest[np.argsort(xs[largest])]

        tau = np.linspace(-3.0, 3.0, 220)
        aligned = []
        for idx in largest:
            profile = np.interp(xs[idx] + tau, xs, sea)
            aligned.append(profile)
        aligned = np.array(aligned)
        average = aligned.mean(axis=0)
        return xs, sea, crest_indices, largest, tau, aligned, average

    def _show_wave_group_intro(self):
        nav = self._nav(14)
        title = self._title("A focused wave group")

        k_values = np.linspace(2.55, 6.45, 31)
        k0 = 4.50
        sigma = 0.92
        amplitudes = np.exp(-0.5 * ((k_values - k0) / sigma) ** 2)
        amplitudes = amplitudes / amplitudes.max()
        phases = np.zeros_like(k_values)
        energy_order = list(np.argsort(amplitudes)[::-1])
        reveal_groups = [[idx] for idx in energy_order]

        x_min, x_max, y0 = -5.25, 5.25, 1.52
        x_span = np.linspace(x_min, x_max, 360)
        domain_axis = self._axis_line(x_min, x_max, y0)
        domain_label = Text("physical domain", font_size=29, color=MUTED).move_to([-3.95, 2.02, 0])
        focus_marker = DashedLine([np.mean([x_min, x_max]), y0 - 0.78, 0], [np.mean([x_min, x_max]), y0 + 0.78, 0], color=ACCENT, stroke_width=1.8, dash_length=0.12)

        def cumulative_wave(indices):
            if not indices:
                return np.zeros_like(x_span)
            center = np.mean([x_min, x_max])
            values = np.zeros_like(x_span)
            for idx in indices:
                amp = amplitudes[idx]
                k = k_values[idx]
                phi = phases[idx]
                values += amp * np.cos(k * (x_span - center) + phi)
            return 0.48 * values / max(np.sum(amplitudes[indices]), 1e-6)

        def component_envelope(indices):
            if not indices:
                return np.zeros_like(x_span)
            center = np.mean([x_min, x_max])
            values = np.zeros_like(x_span)
            for idx in indices:
                amp = amplitudes[idx]
                k = k_values[idx]
                values += amp * np.cos((k - k0) * (x_span - center))
            values = np.maximum(values / max(np.sum(amplitudes[indices]), 1e-6), 0.0)
            return 0.48 * values

        cumulative_indices = []
        wave_shapes = []
        for group in reveal_groups:
            cumulative_indices.extend(group)
            wave_shapes.append(self._polyline_from_samples(x_span, y0 + cumulative_wave(cumulative_indices), color=SURFACE, stroke_width=3.6))
        wave = wave_shapes[0].copy()
        final_envelope = component_envelope(energy_order)
        envelope_top = self._polyline_from_samples(x_span, y0 + final_envelope, color=ACCENT, stroke_width=1.8)
        envelope_bottom = self._polyline_from_samples(x_span, y0 - final_envelope, color=ACCENT, stroke_width=1.8)

        spec_x0, spec_x1, spec_y0 = -5.45, 5.45, -1.34
        spec_plot_x0, spec_plot_x1 = -4.35, 4.35
        spec_axis = Line([spec_x0, spec_y0, 0], [spec_x1, spec_y0, 0], color=MUTED, stroke_width=2)
        spec_y_axis = Line([spec_x0, spec_y0, 0], [spec_x0, spec_y0 + 1.06, 0], color=MUTED, stroke_width=2)
        spec_label = VGroup(
            Text("broad-banded Gaussian spectrum", font_size=28, color=MUTED),
            MathTex(r"E(k)\propto\exp[-(k-k_0)^2/(2\sigma^2)]", font_size=29, color=FG),
        ).arrange(DOWN, buff=0.06).move_to([0.0, 0.02, 0])
        spec_curve_x = np.linspace(spec_plot_x0, spec_plot_x1, 240)
        spec_center = np.mean([spec_plot_x0, spec_plot_x1])
        stem_positions = np.linspace(spec_plot_x0, spec_plot_x1, len(k_values))
        spec_scale = (stem_positions[-1] - stem_positions[0]) / (k_values[-1] - k_values[0])
        stem_height = 0.90
        def spectrum_height_at(x):
            k = k_values[0] + (x - stem_positions[0]) / spec_scale
            return stem_height * np.exp(-0.5 * ((k - k0) / sigma) ** 2)

        gaussian_curve = self._polyline_from_samples(
            spec_curve_x,
            spec_y0 + np.array([spectrum_height_at(x) for x in spec_curve_x]),
            color=BLUE_A,
            stroke_width=2.0,
            opacity=0.45,
        )
        stems = VGroup()
        for idx, (x, amp) in enumerate(zip(stem_positions, amplitudes)):
            color = ACCENT if idx == energy_order[0] else SURFACE
            stems.add(Line([x, spec_y0, 0], [x, spec_y0 + stem_height * amp, 0], color=color, stroke_width=2.3))
        k_label = MathTex(r"k", font_size=30, color=MUTED).next_to(spec_axis, RIGHT, buff=0.10)
        e_label = MathTex(r"E(k)", font_size=26, color=MUTED).rotate(PI / 2).next_to(spec_y_axis, LEFT, buff=0.12)
        tick_labels = VGroup(
            MathTex(r"k_{\min}", font_size=20, color=MUTED).next_to([spec_x0 + 0.10, spec_y0, 0], DOWN, buff=0.10),
            MathTex(r"k_0", font_size=22, color=ACCENT).next_to([spec_center, spec_y0, 0], DOWN, buff=0.10),
            MathTex(r"k_{\max}", font_size=20, color=MUTED).next_to([spec_x1 - 0.10, spec_y0, 0], DOWN, buff=0.10),
        )
        tick_marks = VGroup(*[
            Line([x, spec_y0 - 0.05, 0], [x, spec_y0 + 0.05, 0], color=MUTED, stroke_width=1.5)
            for x in [spec_x0 + 0.10, spec_center, spec_x1 - 0.10]
        ])
        add_label = Text("nearby components are phase aligned at the focus", font_size=23, color=ACCENT).move_to([0.0, -2.38, 0])

        equation = MathTex(
            r"\eta_1(x)=\sum_n a_n\cos(k_nx+\epsilon_n)",
            font_size=38,
            color=FG,
        ).move_to([3.40, 2.12, 0])
        if equation.width > 5.25:
            equation.scale_to_fit_width(5.25)

        self._play_step(FadeIn(title), FadeIn(nav), FadeIn(domain_label), Create(domain_axis), run_time=0.45)
        self._play_step(
            FadeIn(spec_label),
            Create(spec_axis),
            Create(spec_y_axis),
            FadeIn(k_label),
            FadeIn(e_label),
            FadeIn(tick_marks),
            FadeIn(tick_labels),
            Create(gaussian_curve),
            FadeIn(add_label),
            run_time=0.55,
        )
        first_batch = energy_order[:3]
        shown_stems = VGroup(*[stems[idx] for idx in first_batch])
        wave.become(wave_shapes[2])
        self.play(
            FadeIn(shown_stems),
            FadeIn(wave),
            FadeIn(equation),
            run_time=0.75,
            rate_func=smooth,
        )
        cumulative_count = len(first_batch)
        for batch_size in [5, 7, 8, len(energy_order) - 23]:
            next_count = cumulative_count + batch_size
            batch = energy_order[cumulative_count:next_count]
            if not batch:
                continue
            self.play(
                FadeIn(VGroup(*[stems[idx] for idx in batch]), lag_ratio=0.08),
                Transform(wave, wave_shapes[next_count - 1]),
                run_time=0.48,
                rate_func=smooth,
            )
            cumulative_count = next_count
        self._pause()
        self._play_step(FadeIn(envelope_top), FadeIn(envelope_bottom), FadeIn(focus_marker), run_time=0.55)
        self._clear(
            title,
            nav,
            domain_label,
            domain_axis,
            wave,
            envelope_top,
            envelope_bottom,
            focus_marker,
            spec_label,
            spec_axis,
            spec_y_axis,
            gaussian_curve,
            stems,
            k_label,
            e_label,
            tick_marks,
            tick_labels,
            add_label,
            equation,
        )

    def _show_focused_wave_group_motivation(self):
        nav = self._nav(15)
        title = self._title("Large random-wave crests average into a group-like shape")

        xs, sea, crest_indices, largest, tau, aligned, average = self._large_crest_average_data()
        avg_color = "#ff4f8b"
        record_x = np.linspace(-5.55, 5.55, len(xs))
        record_y0 = 1.52
        record_y = record_y0 + 0.34 * sea
        record_axis = Line([-5.55, record_y0, 0], [5.55, record_y0, 0], color=MUTED, stroke_width=1.5)
        record = self._polyline_from_samples(record_x, record_y, color=MUTED, stroke_width=1.8, opacity=0.80)
        crest_dots = VGroup(*[
            Dot([record_x[i], record_y[i], 0], radius=0.018, color=MUTED)
            for i in crest_indices
        ])
        large_dots = VGroup(*[
            Dot([record_x[i], record_y[i], 0], radius=0.036, color=ACCENT)
            for i in largest
        ])
        record_label = VGroup(
            Text("random sea record", font_size=21, color=MUTED),
            MathTex(r"120\ \text{crests}", font_size=23, color=MUTED),
            MathTex(r"\text{largest }1/3\ \text{waves}", font_size=23, color=ACCENT),
        ).arrange(RIGHT, buff=0.22).next_to(record_axis, UP, buff=0.66)

        average_y0 = -0.48
        average_x = np.linspace(-5.68, 5.68, len(tau))
        average_axis = Line([average_x[0], average_y0, 0], [average_x[-1], average_y0, 0], color=MUTED, stroke_width=1.5)
        average_center = 0.5 * (average_x[0] + average_x[-1])
        align_marker = DashedLine([average_center, average_y0 - 1.12, 0], [average_center, average_y0 + 1.04, 0], color=ACCENT, stroke_width=1.6, dash_length=0.12)
        aligned_traces = VGroup(*[
            self._polyline_from_samples(average_x, average_y0 + 0.54 * profile, color=SURFACE, stroke_width=1.0, opacity=0.17)
            for profile in aligned
        ])
        sample_ids = np.linspace(0, len(largest) - 1, 7).astype(int)
        sample_windows = VGroup()
        sample_traces = VGroup()
        record_window_width = 0.18
        for sample_id in sample_ids:
            idx = largest[sample_id]
            x_c = record_x[idx]
            sample_windows.add(
                Rectangle(
                    width=record_window_width,
                    height=0.52,
                    stroke_color=ACCENT,
                    stroke_width=1.2,
                    fill_color=ACCENT,
                    fill_opacity=0.08,
                ).move_to([x_c, record_y0 + 0.18, 0])
            )
            sample_traces.add(
                self._polyline_from_samples(
                    average_x,
                    average_y0 + 0.54 * aligned[sample_id],
                    color=SURFACE,
                    stroke_width=1.4,
                    opacity=0.38,
                )
            )
        avg_visual_scale = 0.58
        avg_envelope = 0.95 * max(np.max(np.abs(average)), 1e-6) * np.exp(-0.5 * (tau / 1.15) ** 2)
        avg_wave = self._polyline_from_samples(average_x, average_y0 + avg_visual_scale * average, color=avg_color, stroke_width=4.6)
        env_top = self._polyline_from_samples(average_x, average_y0 + avg_visual_scale * avg_envelope, color=ACCENT, stroke_width=1.4)
        env_bottom = self._polyline_from_samples(average_x, average_y0 - avg_visual_scale * avg_envelope, color=ACCENT, stroke_width=1.4)
        average_label = VGroup(
            Text("crest-aligned average", font_size=23, color=avg_color),
            MathTex(r"\langle\eta(x-x_c)\mid \eta_c\ \text{large}\rangle", font_size=30, color=FG),
        ).arrange(DOWN, buff=0.06).move_to([-3.64, 0.56, 0])
        average_group = VGroup(average_axis, align_marker, sample_traces, aligned_traces, env_top, env_bottom, avg_wave, average_label)

        reasons = VGroup(
            VGroup(MathTex(r"1", font_size=25, color=ACCENT), Text("select large waves", font_size=22, color=FG)).arrange(RIGHT, buff=0.10),
            VGroup(MathTex(r"2", font_size=25, color=ACCENT), Text("shift by crest position", font_size=22, color=FG)).arrange(RIGHT, buff=0.10),
            VGroup(MathTex(r"3", font_size=25, color=ACCENT), Text("average the aligned profiles", font_size=22, color=FG)).arrange(RIGHT, buff=0.10),
            Text("conditional mean -> wave-group shape", font_size=22, color=SURFACE),
        ).arrange(RIGHT, aligned_edge=DOWN, buff=0.38).move_to([0.0, -2.10, 0])
        if reasons.width > 11.2:
            reasons.scale_to_fit_width(11.2)

        arrow = Arrow([-0.42, 1.05, 0], [-0.42, 0.42, 0], color=ACCENT, buff=0.06, stroke_width=3.5)
        align_note = VGroup(
            MathTex(r"x-x_c", font_size=27, color=ACCENT),
            Text("shift every selected crest to the same origin", font_size=20, color=MUTED),
        ).arrange(RIGHT, buff=0.16).move_to([3.42, 0.68, 0])
        caption = self._caption("Averaging many large-wave neighborhoods reveals the group-like conditional shape.", font_size=23)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(Create(record_axis), Create(record), FadeIn(record_label[:2]), FadeIn(crest_dots), run_time=0.65)
        self._play_step(FadeIn(record_label[2]), FadeIn(large_dots), FadeIn(sample_windows), GrowArrow(arrow), run_time=0.55)
        self._play_step(FadeIn(average_axis), FadeIn(align_marker), FadeIn(average_label), FadeIn(align_note), run_time=0.50)
        self.play(
            LaggedStart(*[TransformFromCopy(window, trace) for window, trace in zip(sample_windows, sample_traces)], lag_ratio=0.10),
            run_time=2.35,
        )
        self._pause()
        self._play_step(FadeIn(aligned_traces), run_time=0.85)
        self._play_step(Create(avg_wave), FadeIn(env_top), FadeIn(env_bottom), run_time=1.45)
        self._play_step(FadeIn(reasons), FadeIn(caption), run_time=0.50)
        self._clear(title, nav, record_axis, record, crest_dots, large_dots, sample_windows, record_label, average_group, reasons, arrow, align_note, caption)

    def _show_wave_group_importance(self):
        nav = self._nav(15)
        title = self._title("Why not random wave or monochromatic wave?")

        xs = np.linspace(-1.78, 1.78, 180)
        card_centers = [-3.85, 0.0, 3.85]
        labels = [
            (r"1", ("ocean waves", "come in groups"), SURFACE),
            (r"2", ("wave groups", "repeat in the lab"), GREEN),
            (r"3", "extreme averages", ACCENT),
        ]
        panels = VGroup()
        for x_c, (number, text, color) in zip(card_centers, labels):
            axis_y = 0.38
            axis = Line([x_c - 1.62, axis_y, 0], [x_c + 1.62, axis_y, 0], color=MUTED, stroke_width=1.5)
            if isinstance(text, tuple):
                label_text = VGroup(*[Text(line, font_size=21, color=FG) for line in text]).arrange(DOWN, buff=0.02)
            else:
                label_text = Text(text, font_size=24, color=FG)
            tag = VGroup(
                MathTex(number, font_size=32, color=color),
                label_text,
            ).arrange(DOWN, buff=0.04).move_to([x_c, 1.64, 0])
            panels.add(VGroup(axis, tag))

        ocean_lines = VGroup()
        for offset, opacity in [(-0.28, 0.36), (0.0, 0.95), (0.28, 0.42)]:
            vals = 0.24 * np.exp(-0.5 * ((xs - offset) / 0.78) ** 2) * np.cos(8.5 * xs + 1.8 * offset)
            ocean_lines.add(self._polyline_from_samples(xs + card_centers[0], 0.38 + vals, color=SURFACE, stroke_width=2.2, opacity=opacity))

        lab_wave_group = self._polyline_from_samples(
            xs + card_centers[1],
            0.72 + 0.20 * np.exp(-0.5 * ((xs + 0.05) / 0.78) ** 2) * np.cos(8.4 * xs),
            color=GREEN,
            stroke_width=2.8,
        )
        rng_lab = np.random.default_rng(43)
        random_series = np.zeros_like(xs)
        for k, amp, phase in zip(np.linspace(4.0, 11.4, 9), rng_lab.uniform(0.04, 0.12, 9), rng_lab.uniform(0.0, 2 * np.pi, 9)):
            random_series += amp * np.cos(k * xs + phase)
        lab_random = self._polyline_from_samples(xs + card_centers[1], 0.08 + random_series, color=MUTED, stroke_width=1.8, opacity=0.82)
        lab_compare = VGroup(
            lab_wave_group,
            lab_random,
            Text("one designed group", font_size=17, color=GREEN).move_to([card_centers[1], 1.02, 0]),
            Text("random time series", font_size=17, color=MUTED).move_to([card_centers[1], -0.22, 0]),
            MathTex(r"\text{easier to reproduce}", font_size=20, color=GREEN).move_to([card_centers[1], -0.64, 0]),
        )

        trace_lines = VGroup()
        for phase, opacity in zip(np.linspace(-0.9, 0.9, 7), np.linspace(0.20, 0.42, 7)):
            vals = 0.22 * np.exp(-0.5 * (xs / 0.72) ** 2) * np.cos(8.2 * xs + phase)
            trace_lines.add(self._polyline_from_samples(xs + card_centers[2], 0.38 + vals, color=SURFACE, stroke_width=1.1, opacity=opacity))
        average = self._polyline_from_samples(
            xs + card_centers[2],
            0.38 + 0.25 * np.exp(-0.5 * (xs / 0.75) ** 2) * np.cos(8.2 * xs),
            color=ACCENT,
            stroke_width=3.8,
        )
        center_line = DashedLine([card_centers[2], -0.10, 0], [card_centers[2], 0.88, 0], color=ACCENT, stroke_width=1.4, dash_length=0.09)

        bottom_wave_x = np.linspace(-4.6, 4.6, 320)
        bottom_wave = self._polyline_from_samples(
            bottom_wave_x,
            -1.54 + 0.30 * np.exp(-0.5 * (bottom_wave_x / 1.38) ** 2) * np.cos(5.2 * bottom_wave_x),
            color=FG,
            stroke_width=3.0,
            opacity=0.88,
        )
        bottom_env = VGroup(
            self._polyline_from_samples(bottom_wave_x, -1.54 + 0.30 * np.exp(-0.5 * (bottom_wave_x / 1.38) ** 2), color=MUTED, stroke_width=1.4, opacity=0.50),
            self._polyline_from_samples(bottom_wave_x, -1.54 - 0.30 * np.exp(-0.5 * (bottom_wave_x / 1.38) ** 2), color=MUTED, stroke_width=1.4, opacity=0.50),
        )
        caption = self._caption("That is why we are interested in wave groups.", font_size=24)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(panels[0]), FadeIn(ocean_lines), run_time=0.55)
        self._play_step(FadeIn(panels[1]), Create(lab_wave_group), FadeIn(VGroup(lab_random, lab_compare[2:])), run_time=0.55)
        self._play_step(FadeIn(panels[2]), FadeIn(trace_lines), Create(average), FadeIn(center_line), run_time=0.60)
        self._play_step(Create(bottom_wave), FadeIn(bottom_env), FadeIn(caption), run_time=0.65)
        self._clear(title, nav, panels, ocean_lines, lab_compare, trace_lines, average, center_line, bottom_wave, bottom_env, caption)

    def _show_second_order_wave_group_map(self):
        nav = self._nav(22)
        title = self._title("Second superharmonic and subharmonic for a wave group")

        ax_lin = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.15, 0.5],
            x_length=4.45,
            y_length=1.55,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(LEFT, buff=0.54).shift(UP * 1.40)
        ax_super = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 1.15, 0.5],
            x_length=4.70,
            y_length=1.18,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.54).shift(UP * 1.78)
        ax_sub = Axes(
            x_range=[0, 5.0, 1],
            y_range=[0, 1.15, 0.5],
            x_length=4.70,
            y_length=1.18,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.54).shift(UP * 0.02)

        def stem(ax, x, height, color, width=3.0):
            return VGroup(
                Line(ax.c2p(x, 0), ax.c2p(x, height), color=color, stroke_width=width),
                Dot(ax.c2p(x, height), radius=0.032, color=color),
            )

        ks = np.linspace(1.25, 5.45, 15)
        amps = np.exp(-0.5 * ((ks - 3.25) / 0.88) ** 2)
        amps = amps / amps.max()
        linear_stems = VGroup(*[stem(ax_lin, k, a, SURFACE, width=2.8) for k, a in zip(ks, amps)])
        linear_band = ax_lin.plot(lambda k: np.exp(-0.5 * ((k - 3.25) / 0.88) ** 2), x_range=[0.85, 5.85, 0.03], color=SURFACE, stroke_width=1.5, stroke_opacity=0.35)

        super_bins = np.linspace(2.5, 10.9, 25)
        sub_bins = np.linspace(0.0, 4.4, 25)
        super_trackers = [ValueTracker(0.0) for _ in super_bins]
        sub_trackers = [ValueTracker(0.0) for _ in sub_bins]
        super_stems = VGroup(*[
            always_redraw(lambda k=k, tracker=tracker: stem(ax_super, k, tracker.get_value(), ACCENT, width=2.45))
            for k, tracker in zip(super_bins, super_trackers)
        ])
        sub_stems = VGroup(*[
            always_redraw(lambda k=k, tracker=tracker: stem(ax_sub, k, tracker.get_value(), GREEN, width=2.45))
            for k, tracker in zip(sub_bins, sub_trackers)
        ])

        heads = VGroup(
            Text("linear spectrum", font_size=21, color=SURFACE).next_to(ax_lin, UP, buff=0.14),
            Text("superharmonic", font_size=20, color=ACCENT).next_to(ax_super, UP, buff=0.10),
            Text("subharmonic", font_size=20, color=GREEN).next_to(ax_sub, UP, buff=0.10),
        )
        axis_labels = VGroup(
            MathTex(r"k", font_size=23, color=MUTED).next_to(ax_lin.x_axis, RIGHT, buff=0.05),
            MathTex(r"K_+", font_size=20, color=MUTED).next_to(ax_super.x_axis, RIGHT, buff=0.05),
            MathTex(r"K_-", font_size=20, color=MUTED).next_to(ax_sub.x_axis, RIGHT, buff=0.05),
            MathTex(r"|\hat\eta^{(1)}|", font_size=21, color=MUTED).rotate(PI / 2).next_to(ax_lin.y_axis, LEFT, buff=0.08),
            MathTex(r"\log|\hat\eta^{(2)}|", font_size=19, color=MUTED).rotate(PI / 2).next_to(ax_sub.y_axis, LEFT, buff=0.08),
        )

        pairs = [(i, j) for i in range(len(ks)) for j in range(i, len(ks))]
        super_vectors = {}
        sub_vectors = {}
        raw_super_vectors = []
        raw_sub_vectors = []
        wave_xs = np.linspace(-4.55, 4.55, 420)
        phases = -ks * 0.0
        super_waves = {}
        sub_waves = {}
        gravity = 1.0
        peak_k = 3.25
        water_depth = 1.0 / peak_k

        def omega(k):
            return np.sqrt(gravity * k * np.tanh(k * water_depth))

        def finite_depth_bp(k1, k2):
            w1, w2 = omega(k1), omega(k2)
            k_plus = k1 + k2
            d_plus = (w1 + w2) ** 2 - gravity * k_plus * np.tanh(k_plus * water_depth)
            if abs(d_plus) < 1e-9:
                return 0.0
            tanh_product = np.tanh(k1 * water_depth) * np.tanh(k2 * water_depth)
            direction_factor = 1.0 - 1.0 / tanh_product
            free_wave_factor = (w1 + w2) ** 2 + gravity * k_plus * np.tanh(k_plus * water_depth)
            depth_forcing = (w1**3 / np.sinh(k1 * water_depth) ** 2) + (w2**3 / np.sinh(k2 * water_depth) ** 2)
            return (
                (w1**2 + w2**2) / (2 * gravity)
                - (w1 * w2 / (2 * gravity)) * direction_factor * (free_wave_factor / d_plus)
                + ((w1 + w2) / (2 * gravity * d_plus)) * depth_forcing
            )

        def finite_depth_bm(k1, k2):
            k_minus = abs(k1 - k2)
            if k_minus < 1e-9:
                return 0.0
            w1, w2 = omega(k1), omega(k2)
            d_minus = (w1 - w2) ** 2 - gravity * k_minus * np.tanh(k_minus * water_depth)
            if abs(d_minus) < 1e-9:
                return 0.0
            tanh_product = np.tanh(k1 * water_depth) * np.tanh(k2 * water_depth)
            direction_factor = 1.0 + 1.0 / tanh_product
            free_wave_factor = (w1 - w2) ** 2 + gravity * k_minus * np.tanh(k_minus * water_depth)
            depth_forcing = (w1**3 / np.sinh(k1 * water_depth) ** 2) - (w2**3 / np.sinh(k2 * water_depth) ** 2)
            return (
                (w1**2 + w2**2) / (2 * gravity)
                + (w1 * w2 / (2 * gravity)) * direction_factor * (free_wave_factor / d_minus)
                + ((w1 - w2) / (2 * gravity * d_minus)) * depth_forcing
            )

        def stokes_second_harmonic(k):
            kh = k * water_depth
            return (k / (4 * np.tanh(kh))) * (2 + 3 / np.sinh(kh) ** 2)

        def mean_setdown(k):
            return k / (2 * np.sinh(2 * k * water_depth))

        for i, j in pairs:
            theta_i = ks[i] * wave_xs + phases[i]
            theta_j = ks[j] * wave_xs + phases[j]
            amp_pair = amps[i] * amps[j]
            k_plus = ks[i] + ks[j]
            k_minus = abs(ks[i] - ks[j])
            if i == j:
                super_weight = stokes_second_harmonic(ks[i]) * amp_pair
                setdown_weight = mean_setdown(ks[i]) * amp_pair
                difference_weight = 0.0
            else:
                super_weight = finite_depth_bp(ks[i], ks[j]) * amp_pair
                setdown_weight = 0.0
                difference_weight = finite_depth_bm(ks[i], ks[j]) * amp_pair
            sub_weight = abs(difference_weight) + setdown_weight

            weights_plus = np.exp(-0.5 * ((super_bins - k_plus) / 0.24) ** 2)
            weights_plus = weights_plus / max(np.sum(weights_plus), 1e-9)
            weights_minus = np.exp(-0.5 * ((sub_bins - k_minus) / 0.14) ** 2)
            weights_minus = weights_minus / max(np.sum(weights_minus), 1e-9)
            super_vectors[(i, j)] = abs(super_weight) * weights_plus
            sub_vectors[(i, j)] = sub_weight * weights_minus
            raw_super_vectors.append(super_vectors[(i, j)])
            raw_sub_vectors.append(sub_vectors[(i, j)])
            super_waves[(i, j)] = super_weight * np.cos(theta_i + theta_j)
            difference_wave = difference_weight * np.cos(theta_i - theta_j)
            setdown_wave = -setdown_weight * np.ones_like(wave_xs)
            sub_waves[(i, j)] = difference_wave + setdown_wave

        common_spectrum_max = max(
            float(np.max(np.sum(raw_super_vectors, axis=0))),
            float(np.max(np.sum(raw_sub_vectors, axis=0))),
            1e-9,
        )
        common_spectrum_scale = 0.94 / common_spectrum_max
        super_vectors = {key: vec * common_spectrum_scale for key, vec in super_vectors.items()}
        sub_vectors = {key: vec * common_spectrum_scale for key, vec in sub_vectors.items()}
        wave_scale = 0.30 / max(
            float(np.max(np.abs(np.sum([super_waves[p] + sub_waves[p] for p in pairs], axis=0)))),
            1e-9,
        )
        super_waves = {key: wave * wave_scale for key, wave in super_waves.items()}
        sub_waves = {key: wave * wave_scale for key, wave in sub_waves.items()}

        cumulative_super_levels = [np.zeros(len(super_bins))]
        cumulative_sub_levels = [np.zeros(len(sub_bins))]
        cumulative_super_waves = [np.zeros_like(wave_xs)]
        cumulative_sub_waves = [np.zeros_like(wave_xs)]
        levels_plus = np.zeros(len(super_bins))
        levels_minus = np.zeros(len(sub_bins))
        wave_plus = np.zeros_like(wave_xs)
        wave_minus = np.zeros_like(wave_xs)
        for pair in pairs:
            levels_plus = np.minimum(1.0, levels_plus + super_vectors[pair])
            levels_minus = np.minimum(1.0, levels_minus + sub_vectors[pair])
            wave_plus = wave_plus + super_waves[pair]
            wave_minus = wave_minus + sub_waves[pair]
            cumulative_super_levels.append(levels_plus.copy())
            cumulative_sub_levels.append(levels_minus.copy())
            cumulative_super_waves.append(wave_plus.copy())
            cumulative_sub_waves.append(wave_minus.copy())
        cumulative_super_levels = np.array(cumulative_super_levels)
        cumulative_sub_levels = np.array(cumulative_sub_levels)
        log_floor = 0.018
        log_denominator = np.log10(1 + 1 / log_floor)
        cumulative_super_levels = np.log10(1 + cumulative_super_levels / log_floor) / log_denominator
        cumulative_sub_levels = np.log10(1 + cumulative_sub_levels / log_floor) / log_denominator
        cumulative_super_waves = np.array(cumulative_super_waves)
        cumulative_sub_waves = np.array(cumulative_sub_waves)
        scan_tracker = ValueTracker(0.0)

        def current_pair():
            pair_index = min(int(scan_tracker.get_value()), len(pairs) - 1)
            return pairs[pair_index]

        def make_pair_indicator(which):
            i, j = current_pair()
            highlight = linear_stems[i if which == 0 else j].copy().set_color(GREEN).set_z_index(7)
            highlight.set_stroke(width=4.6 if which == 0 else 4.2)
            return highlight

        highlighted_pair = VGroup(
            always_redraw(lambda: make_pair_indicator(0)),
            always_redraw(lambda: make_pair_indicator(1)),
        )

        def scan_position():
            position = max(0.0, min(scan_tracker.get_value(), float(len(pairs))))
            base = min(int(np.floor(position)), len(pairs) - 1)
            alpha = position - base
            return base, alpha

        def blended(samples):
            base, alpha = scan_position()
            return (1 - alpha) * samples[base] + alpha * samples[base + 1]

        def make_super_target_indicator():
            i, j = current_pair()
            target = ks[i] + ks[j]
            height = min(1.04, 0.16 + 0.52 * amps[i] * amps[j])
            return VGroup(
                Line(ax_super.c2p(target, 0), ax_super.c2p(target, height), color=FG, stroke_width=3.4, stroke_opacity=0.90),
                Dot(ax_super.c2p(target, height), radius=0.046, color=FG),
            ).set_z_index(8)

        def make_sub_target_indicator():
            i, j = current_pair()
            target = abs(ks[i] - ks[j])
            height = min(1.04, 0.10 + 0.52 * amps[i] * amps[j])
            return VGroup(
                Line(ax_sub.c2p(target, 0), ax_sub.c2p(target, height), color=FG, stroke_width=3.4, stroke_opacity=0.90),
                Dot(ax_sub.c2p(target, height), radius=0.046, color=FG),
            ).set_z_index(8)

        target_indicators = VGroup(always_redraw(make_super_target_indicator), always_redraw(make_sub_target_indicator))
        pair_label = VGroup(
            Text("one bichromatic pair", font_size=20, color=GREEN),
            MathTex(r"k_m+k_n\quad\text{and}\quad |k_m-k_n|", font_size=24, color=FG),
        ).arrange(RIGHT, buff=0.20).move_to([-2.75, -0.58, 0])
        pair_box = SurroundingRectangle(pair_label, color=GREEN, buff=0.14, corner_radius=0.07).set_fill(BG, opacity=0.86)

        wave_rows = VGroup()
        wave_labels = VGroup()
        for y, label, color in [
            (-1.12, r"\eta_{22}", ACCENT),
            (-1.72, r"\eta_{20}", GREEN),
            (-2.32, r"\eta_{22}+\eta_{20}", FG),
        ]:
            axis = Line([wave_xs[0], y, 0], [wave_xs[-1], y, 0], color=MUTED, stroke_width=1.4, stroke_opacity=0.65)
            wave_rows.add(axis)
            wave_labels.add(MathTex(label, font_size=22, color=color).next_to(axis, LEFT, buff=0.10))

        def wave_curve(kind):
            plus = blended(cumulative_super_waves)
            minus = blended(cumulative_sub_waves)
            if kind == "plus":
                return self._polyline_from_samples(wave_xs, -1.12 + plus, color=ACCENT, stroke_width=2.6)
            if kind == "minus":
                return self._polyline_from_samples(wave_xs, -1.72 + minus, color=GREEN, stroke_width=2.6)
            return self._polyline_from_samples(wave_xs, -2.32 + plus + minus, color=FG, stroke_width=2.8)

        wave_graphs = VGroup(
            always_redraw(lambda: wave_curve("plus")),
            always_redraw(lambda: wave_curve("minus")),
            always_redraw(lambda: wave_curve("sum")),
        )

        formulas = VGroup(
            MathTex(r"\eta^{(1)}=\sum_{m=1}^{N_c} a_m\cos\theta_m", font_size=22, color=SURFACE),
            MathTex(
                r"\eta_{22}\sim\sum a_m a_n B_p(k_m,k_n;d)\cos(\theta_m+\theta_n)",
                font_size=19,
                color=ACCENT,
            ),
            MathTex(
                r"\eta_{20}=-\sum_m {a_m^2k_m\over2\sinh(2k_md)}+\sum_{m<n}a_ma_nB_m(k_m,k_n;d)\cos(\theta_m-\theta_n)",
                font_size=16,
                color=GREEN,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-1.25, -2.02, 0])
        if formulas.width > 6.45:
            formulas.scale_to_fit_width(6.45)
        formula_box = SurroundingRectangle(formulas, color=ACCENT, buff=0.18, corner_radius=0.07).set_fill(BG, opacity=0.55)
        full_sum_box = SurroundingRectangle(VGroup(ax_super, ax_sub), color=ACCENT, buff=0.08, corner_radius=0.07)

        scan_driver = VMobject()

        def update_scan(_mob):
            current_super_levels = blended(cumulative_super_levels)
            current_sub_levels = blended(cumulative_sub_levels)
            for tracker, level in zip(super_trackers, current_super_levels):
                tracker.set_value(float(level))
            for tracker, level in zip(sub_trackers, current_sub_levels):
                tracker.set_value(float(level))

        scan_driver.add_updater(update_scan)

        self._play_step(FadeIn(title), FadeIn(nav), run_time=0.45)
        self._play_step(FadeIn(ax_lin), FadeIn(ax_super), FadeIn(ax_sub), FadeIn(heads), FadeIn(axis_labels), Create(linear_band), FadeIn(linear_stems), run_time=0.65)
        self._play_step(FadeIn(pair_box), FadeIn(pair_label), FadeIn(highlighted_pair), FadeIn(target_indicators), FadeIn(wave_rows), FadeIn(wave_labels), run_time=0.65)
        self.add(super_stems, sub_stems, wave_graphs, scan_driver)
        self.play(scan_tracker.animate.set_value(float(len(pairs))), run_time=5.8, rate_func=linear)
        scan_driver.clear_updaters()
        update_scan(scan_driver)
        self.remove(scan_driver)
        self._pause()
        self.play(
            FadeOut(highlighted_pair),
            FadeOut(target_indicators),
            FadeOut(wave_rows),
            FadeOut(wave_labels),
            FadeOut(wave_graphs),
            FadeOut(pair_box),
            FadeOut(pair_label),
            run_time=0.35,
        )
        self._play_step(Create(full_sum_box), FadeIn(formula_box), FadeIn(formulas), run_time=0.70)
        move_t = ValueTracker(0.0)
        phase_xs = np.linspace(-8.0, 8.0, 520)
        omega_p = omega(peak_k)
        cg_p = (
            gravity
            * (np.tanh(peak_k * water_depth) + peak_k * water_depth / np.cosh(peak_k * water_depth) ** 2)
            / (2 * omega_p)
        )
        phase_slip_rate = omega_p - peak_k * cg_p
        envelope_width = 2.15
        envelope = lambda x: np.exp(-0.5 * (x / envelope_width) ** 2)

        group_ax = Axes(
            x_range=[-8, 8, 4],
            y_range=[-0.66, 0.66, 0.3],
            x_length=6.85,
            y_length=3.18,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(LEFT, buff=0.58).shift(UP * 0.08)
        moving_spec_ax = Axes(
            x_range=[0.0, 10.5, 2.0],
            y_range=[0.0, 1.15, 0.5],
            x_length=4.35,
            y_length=3.18,
            axis_config={"include_tip": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.58).shift(UP * 0.08)
        moving_heads = VGroup(
            Text("group frame", font_size=23, color=MUTED).next_to(group_ax, UP, buff=0.12),
            Text("bound spectra", font_size=23, color=MUTED).next_to(moving_spec_ax, UP, buff=0.12),
        )
        moving_axis_labels = VGroup(
            MathTex(r"x-c_g t", font_size=22, color=MUTED).next_to(group_ax.x_axis, RIGHT, buff=0.05),
            MathTex(r"\eta", font_size=22, color=MUTED).rotate(PI / 2).next_to(group_ax.y_axis, LEFT, buff=0.08),
            MathTex(r"k", font_size=22, color=MUTED).next_to(moving_spec_ax.x_axis, RIGHT, buff=0.05),
            MathTex(r"|\hat\eta|", font_size=21, color=MUTED).rotate(PI / 2).next_to(moving_spec_ax.y_axis, LEFT, buff=0.08),
        )

        def phase_theta(x, t):
            return peak_k * x - phase_slip_rate * t

        def eta11_group(x, t):
            return 0.34 * envelope(x) * np.cos(phase_theta(x, t))

        def eta22_group(x, t):
            return 0.11 * envelope(x) ** 2 * np.cos(2.0 * phase_theta(x, t))

        def eta20_group(x):
            return -0.085 * envelope(x) ** 2

        def eta_total_group(x, t):
            return eta11_group(x, t) + eta22_group(x, t) + eta20_group(x)

        env_u = group_ax.plot(lambda x: 0.34 * envelope(x), x_range=[-8, 8, 0.06], color=SURFACE, stroke_width=1.1, stroke_opacity=0.36)
        env_l = group_ax.plot(lambda x: -0.34 * envelope(x), x_range=[-8, 8, 0.06], color=SURFACE, stroke_width=1.1, stroke_opacity=0.36)
        setdown_env = group_ax.plot(lambda x: eta20_group(x), x_range=[-8, 8, 0.06], color=GREEN, stroke_width=1.5, stroke_opacity=0.55)
        moving_specs = VGroup(
            moving_spec_ax.plot(lambda k: np.exp(-0.5 * ((k - peak_k) / 0.42) ** 2), x_range=[0.1, 10.5, 0.03], color=SURFACE, stroke_width=2.5),
            moving_spec_ax.plot(lambda k: 0.45 * np.exp(-0.5 * ((k - 2 * peak_k) / 0.62) ** 2), x_range=[0.1, 10.5, 0.03], color=ACCENT, stroke_width=2.5),
            moving_spec_ax.plot(lambda k: 0.34 * np.exp(-0.5 * (k / 0.62) ** 2), x_range=[0.02, 3.0, 0.03], color=GREEN, stroke_width=2.5),
        )
        moving_spec_labels = VGroup(
            MathTex(r"k_p", font_size=21, color=SURFACE).next_to(moving_spec_ax.c2p(peak_k, 0), DOWN, buff=0.08),
            MathTex(r"2k_p", font_size=21, color=ACCENT).next_to(moving_spec_ax.c2p(2 * peak_k, 0), DOWN, buff=0.08),
            MathTex(r"k\approx0", font_size=20, color=GREEN).next_to(moving_spec_ax.c2p(0.35, 0), DOWN + RIGHT * 0.20, buff=0.08),
        )
        moving_legend = VGroup(
            MathTex(r"\eta_{11}", font_size=23, color=SURFACE),
            MathTex(r"\eta_{22}", font_size=23, color=ACCENT),
            MathTex(r"\eta_{20}", font_size=23, color=GREEN),
            MathTex(r"\eta_{11}+\eta_{22}+\eta_{20}", font_size=23, color=FG),
        ).arrange(RIGHT, buff=0.26).next_to(group_ax, DOWN, buff=0.24)
        moving_caption = Tex(
            r"\text{As the carrier phase slips through the envelope, the bound terms keep the same group envelope.}",
            font_size=23,
            color=FG,
        ).to_edge(DOWN, buff=1.08)
        moving_caption.scale_to_fit_width(10.4)

        moving_graphs = VGroup(
            always_redraw(lambda: group_ax.plot(lambda x: eta11_group(x, move_t.get_value()), x_range=[-8, 8, 0.045], color=SURFACE, stroke_width=2.2)),
            always_redraw(lambda: group_ax.plot(lambda x: eta22_group(x, move_t.get_value()), x_range=[-8, 8, 0.045], color=ACCENT, stroke_width=2.2)),
            always_redraw(lambda: group_ax.plot(lambda x: eta20_group(x), x_range=[-8, 8, 0.06], color=GREEN, stroke_width=2.2)),
            always_redraw(lambda: group_ax.plot(lambda x: eta_total_group(x, move_t.get_value()), x_range=[-8, 8, 0.045], color=FG, stroke_width=2.9)),
        )

        self.play(
            FadeOut(full_sum_box),
            FadeOut(formula_box),
            FadeOut(formulas),
            FadeOut(ax_lin),
            FadeOut(ax_super),
            FadeOut(ax_sub),
            FadeOut(heads),
            FadeOut(axis_labels),
            FadeOut(linear_band),
            FadeOut(linear_stems),
            FadeOut(super_stems),
            FadeOut(sub_stems),
            run_time=0.45,
        )
        self._play_step(
            Create(group_ax),
            Create(moving_spec_ax),
            FadeIn(moving_heads),
            FadeIn(moving_axis_labels),
            FadeIn(moving_legend),
            FadeIn(moving_caption),
            Create(env_u),
            Create(env_l),
            Create(setdown_env),
            Create(moving_specs),
            FadeIn(moving_spec_labels),
            FadeIn(moving_graphs),
            run_time=0.65,
        )
        self.play(move_t.animate.set_value(12.0), run_time=7.2, rate_func=linear)
        self._pause()
        self._clear(
            title,
            nav,
            ax_lin,
            ax_super,
            ax_sub,
            heads,
            axis_labels,
            linear_band,
            linear_stems,
            super_stems,
            sub_stems,
            wave_rows,
            wave_labels,
            wave_graphs,
            full_sum_box,
            formula_box,
            formulas,
            group_ax,
            moving_spec_ax,
            moving_heads,
            moving_axis_labels,
            moving_legend,
            moving_caption,
            moving_graphs,
            env_u,
            env_l,
            setdown_env,
            moving_specs,
            moving_spec_labels,
        )

    def construct(self):
        self._construct_scenarios(self.FULL_SCENARIO_ORDER)


class BoundWaveIntroS0Problem(BoundWaveIntroSlides):
    def construct(self):
        self._construct_scenarios(("S0",))


class BoundWaveIntroS1Perturbation(BoundWaveIntroSlides):
    def construct(self):
        self._construct_scenarios(("S1",))


class BoundWaveIntroS2LinearTheory(BoundWaveIntroSlides):
    def construct(self):
        self._construct_scenarios(("S2",))


class BoundWaveIntroS3SecondOrderBC(BoundWaveIntroSlides):
    def construct(self):
        self._construct_scenarios(("S3",))


class BoundWaveIntroS4BoundHarmonics(BoundWaveIntroSlides):
    def construct(self):
        self._construct_scenarios(("S4",))


class BoundWaveIntroS5WaveGroups(BoundWaveIntroSlides):
    def construct(self):
        self._construct_scenarios(("S5",))
