from manim import *
import numpy as np


class SimpleFloatingTurbine(Scene):
    def construct(self):
        self.camera.background_color = "#EAF6FF"

        sky_top = Rectangle(
            width=14.4,
            height=8.2,
            stroke_width=0,
            fill_color="#DFF3FF",
            fill_opacity=1,
        ).move_to(UP * 0.7)
        sky_haze = Rectangle(
            width=14.4,
            height=2.6,
            stroke_width=0,
            fill_color="#C6E8FF",
            fill_opacity=0.45,
        ).move_to(UP * 2.3)
        sun = Circle(
            radius=0.6,
            stroke_width=0,
            fill_color="#FFF2B3",
            fill_opacity=0.75,
        ).move_to(LEFT * 4.9 + UP * 2.8)
        self.add(sky_top, sky_haze, sun)

        title = Text("Floating Wind Turbine", font_size=34, color="#0E3A5D", weight=BOLD)
        title.to_edge(UP, buff=0.35)
        title_bg = SurroundingRectangle(
            title,
            color="#CFEAFF",
            fill_color="#F3FAFF",
            fill_opacity=0.85,
            stroke_width=1,
            buff=0.15,
        )
        self.play(FadeIn(title_bg, shift=DOWN * 0.15), Write(title))
        self.wait(0.6)

        seabed = Rectangle(width=14, height=0.8, color="#8B5A2B", fill_opacity=1)
        seabed.to_edge(DOWN, buff=0)
        seabed_top_y = seabed.get_top()[1]

        freqs = np.linspace(0.1, 2.0, 50)
        peak_freq = 0.4
        sigma = 0.3
        spectrum = np.exp(-((freqs - peak_freq) / sigma) ** 2)
        rng = np.random.default_rng(98)
        phases = rng.uniform(0, 2 * PI, len(freqs))

        def generate_random_wave(x_vals, time=0):
            y_vals = np.zeros_like(x_vals)
            for freq, amp, phase in zip(freqs, spectrum, phases):
                y_vals += amp * 0.05 * np.sin(2 * PI * freq * x_vals + phase + time * freq)
            return y_vals

        def create_water_body(x_vals, time=0):
            y_vals = generate_random_wave(x_vals, time)
            water_points = [[x, y, 0] for x, y in zip(x_vals, y_vals)]
            water_points.append([x_vals[-1], seabed_top_y, 0])
            water_points.append([x_vals[0], seabed_top_y, 0])
            return Polygon(
                *water_points,
                color="#2E7FBF",
                fill_opacity=0.72,
                stroke_color="#86D7FF",
                stroke_width=3,
            )

        x_vals = np.linspace(-7, 7, 200)
        water = create_water_body(x_vals, 0.1)

        self.play(DrawBorderThenFill(seabed), DrawBorderThenFill(water))
        self.wait(0.6)

        platform = RoundedRectangle(
            width=2.2,
            height=0.32,
            corner_radius=0.06,
            color="#C9915D",
            fill_opacity=1,
        ).move_to(UP * 0.18)
        pontoon = RoundedRectangle(
            width=1.45,
            height=0.18,
            corner_radius=0.05,
            color="#B5763F",
            fill_opacity=1,
        ).move_to(platform.get_bottom() + DOWN * 0.08)

        tower = Rectangle(width=0.15, height=2.55, color="#DFE5EE", fill_opacity=1)
        tower.set_stroke(color="#6A7788", width=1.6)
        tower.move_to(platform.get_top() + UP * (tower.height / 2))

        nacelle = RoundedRectangle(
            width=0.86,
            height=0.3,
            corner_radius=0.08,
            color="#F6F9FC",
            fill_opacity=1,
        )
        nacelle.set_stroke(color="#5F6E80", width=1.6)
        nacelle.move_to(tower.get_top() + UP * 0.16 + RIGHT * 0.09)

        # Rotor is placed at nacelle front for a correct geometry.
        hub = Circle(radius=0.1, color="#2F3B4A", fill_opacity=1)
        hub.move_to(nacelle.get_right() + RIGHT * 0.03)

        blade_length = 1.0
        blade1 = Line(
            hub.get_center(), hub.get_center() + UP * blade_length, stroke_width=6, color="#52647A"
        )
        angle2 = np.radians(210)
        blade2 = Line(
            hub.get_center(),
            hub.get_center() + np.array([blade_length * np.cos(angle2), blade_length * np.sin(angle2), 0]),
            stroke_width=6,
            color="#52647A",
        )
        angle3 = np.radians(330)
        blade3 = Line(
            hub.get_center(),
            hub.get_center() + np.array([blade_length * np.cos(angle3), blade_length * np.sin(angle3), 0]),
            stroke_width=6,
            color="#52647A",
        )
        blades = VGroup(blade1, blade2, blade3)

        hub_glow = Circle(radius=0.22, color="#CDE9FF", fill_opacity=0.35, stroke_opacity=0)
        hub_glow.move_to(hub.get_center())

        self.play(
            DrawBorderThenFill(platform),
            DrawBorderThenFill(pontoon),
            DrawBorderThenFill(tower),
            DrawBorderThenFill(nacelle),
            DrawBorderThenFill(hub),
        )
        self.play(FadeIn(hub_glow), Create(blades), run_time=1.2)
        self.wait(0.6)

        rotor_circle = DashedVMobject(
            Circle(radius=blade_length, color="#3A8FCA", stroke_width=2, stroke_opacity=0.7),
            num_dashes=40,
            dashed_ratio=0.45,
        )
        rotor_circle.move_to(hub.get_center())
        self.play(Create(rotor_circle, run_time=1.2))

        anchor_chains = VGroup()
        anchor_weights = VGroup()

        left_chain_points = []
        start_left = platform.get_center() + LEFT * 0.8 + DOWN * 0.15
        end_left = LEFT * 3.5 + seabed.get_top()
        for i in range(15):
            t = i / 14
            x = start_left[0] + t * (end_left[0] - start_left[0])
            y = start_left[1] + t * (end_left[1] - start_left[1]) - 0.4 * np.sin(PI * t)
            left_chain_points.append([x, y, 0])
        left_chain = VMobject()
        left_chain.set_points_as_corners(left_chain_points)
        left_chain.set_stroke(color=DARK_GRAY, width=4)
        left_chain_end = end_left.copy()

        left_anchor = Rectangle(width=0.3, height=0.2, color="#FFD84D", fill_opacity=1)
        left_anchor.move_to(end_left)

        right_chain_points = []
        start_right = platform.get_center() + RIGHT * 0.8 + DOWN * 0.15
        end_right = RIGHT * 3.5 + seabed.get_top()
        for i in range(15):
            t = i / 14
            x = start_right[0] + t * (end_right[0] - start_right[0])
            y = start_right[1] + t * (end_right[1] - start_right[1]) - 0.4 * np.sin(PI * t)
            right_chain_points.append([x, y, 0])
        right_chain = VMobject()
        right_chain.set_points_as_corners(right_chain_points)
        right_chain.set_stroke(color=DARK_GRAY, width=4)
        right_chain_end = end_right.copy()

        right_anchor = Rectangle(width=0.3, height=0.2, color="#FFD84D", fill_opacity=1)
        right_anchor.move_to(end_right)

        anchor_chains.add(left_chain, right_chain)
        anchor_weights.add(left_anchor, right_anchor)

        self.play(Create(anchor_chains), DrawBorderThenFill(anchor_weights))
        self.wait(0.6)

        depth_label = Text("h", font_size=20, color=BLACK)
        depth_label.move_to(RIGHT * 5.5 + UP * 0.75)
        depth_arrow = Arrow(
            RIGHT * 5.5 + UP * 0,
            RIGHT * 5.5 + seabed.get_top(),
            color=BLACK,
            stroke_width=2,
        )
        labels = VGroup(depth_label, depth_arrow)

        self.play(Write(labels))
        self.wait(0.6)

        floating_objects = VGroup(platform, pontoon, tower, nacelle, hub, blades, rotor_circle, hub_glow)
        base_platform_x = platform.get_center()[0]
        base_platform_y = platform.get_center()[1]
        sim_t = ValueTracker(0.0)

        def wave_updater(mob, dt):
            current_time = sim_t.get_value()
            new_water = create_water_body(x_vals, current_time)
            mob.set_points(new_water.get_points())

        def create_chain_points(start, end, n=15, sag_scale=0.4):
            points = []
            for i in range(n):
                t = i / (n - 1)
                x = start[0] + t * (end[0] - start[0])
                y = start[1] + t * (end[1] - start[1]) - sag_scale * np.sin(PI * t)
                points.append([x, y, 0])
            return points

        def platform_float_updater(mob, dt):
            current_time = sim_t.get_value()
            platform_x = mob.get_center()[0]

            platform_wave_height = 0
            for freq, amp, phase in zip(freqs, spectrum, phases):
                platform_wave_height += amp * 0.05 * np.sin(
                    2 * PI * freq * platform_x + phase + current_time * freq
                )

            additional_float = 0.045 * np.sin(2 * PI * 0.16 * current_time) + 0.015 * np.sin(
                2 * PI * 0.37 * current_time
            )
            additional_surge = 0.065 * np.sin(2 * PI * 0.09 * current_time + 0.4)
            target_x = base_platform_x + additional_surge
            target_y = platform_wave_height + base_platform_y + additional_float
            surge_shift = target_x - mob.get_center()[0]
            heave_shift = target_y - mob.get_center()[1]
            floating_objects.shift(RIGHT * surge_shift + UP * heave_shift)

            # Gentle roll tied to low-frequency wave component.
            roll_target = 0.038 * np.sin(2 * PI * 0.10 * current_time + 0.8)
            prev_roll = getattr(mob, "_prev_roll", 0.0)
            floating_objects.rotate(roll_target - prev_roll, about_point=mob.get_center())
            mob._prev_roll = roll_target

        def left_chain_updater(mob, dt):
            start = platform.get_center() + LEFT * 0.8 + DOWN * 0.15
            mob.set_points_as_corners(create_chain_points(start, left_chain_end))

        def right_chain_updater(mob, dt):
            start = platform.get_center() + RIGHT * 0.8 + DOWN * 0.15
            mob.set_points_as_corners(create_chain_points(start, right_chain_end))

        def blade_spin_updater(mob, dt):
            current_time = sim_t.get_value()
            prev_time = getattr(mob, "_prev_sim_t", current_time)
            mob.rotate(-4.0 * (current_time - prev_time), about_point=hub.get_center())
            mob._prev_sim_t = current_time

        water.add_updater(wave_updater)
        platform.add_updater(platform_float_updater)
        left_chain.add_updater(left_chain_updater)
        right_chain.add_updater(right_chain_updater)
        blades.add_updater(blade_spin_updater)

        self.play(sim_t.animate.set_value(36), run_time=36, rate_func=linear)

        water.remove_updater(wave_updater)
        platform.remove_updater(platform_float_updater)
        left_chain.remove_updater(left_chain_updater)
        right_chain.remove_updater(right_chain_updater)
        blades.remove_updater(blade_spin_updater)

        self.play(FadeOut(labels), FadeOut(title_bg), run_time=0.8)
        self.wait(0.5)
