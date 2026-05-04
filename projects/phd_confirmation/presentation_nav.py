from manim import *


Text.set_default(font="CMU Serif")

NAV_HEIGHT = 0.30
PROGRESS_NAV_HEIGHT = 0.72
PROGRESS_NAV_RADIUS = 0.055
NAV_BG = ManimColor("#030712")
NAV_TRACK = ManimColor("#1F2937")
NAV_MUTED = ManimColor("#CBD5E1")
NAV_TEXT = ManimColor("#F8FAFC")
NAV_SCENARIO_COLORS = [
    ManimColor("#FFE45E"),
    ManimColor("#FFB84D"),
    ManimColor("#FF7A59"),
    ManimColor("#FF5DA2"),
    ManimColor("#C77DFF"),
    ManimColor("#8EA7FF"),
]
NAV_SCENARIO_NAMES = [
    "nonlinear waves",
    "bound harmonics",
    "exact cost",
    "VWA structure",
    "higher order",
    "extensions",
]
NAV_FONT = "CMU Serif"
NAV_SUB_GRADIENT_STARTS = [
    ManimColor("#8B6508"),
    ManimColor("#8A4D08"),
    ManimColor("#8A2F1C"),
    ManimColor("#851D50"),
    ManimColor("#56248A"),
    ManimColor("#2B3B8A"),
]
NAV_SUB_GRADIENT_ENDS = [
    ManimColor("#FFF7B8"),
    ManimColor("#FFE7B3"),
    ManimColor("#FFD3C7"),
    ManimColor("#FFC4DF"),
    ManimColor("#E9D0FF"),
    ManimColor("#D5DEFF"),
]


def bottom_nav_bar(index, total, scenario_name, section_name, accent=YELLOW):
    """A thin persistent bottom bar for presentation orientation."""
    frame_w = config.frame_width
    frame_h = config.frame_height
    y = -frame_h / 2 + NAV_HEIGHT / 2
    bar = Rectangle(
        width=frame_w,
        height=NAV_HEIGHT,
        stroke_width=0,
        fill_color=NAV_BG,
        fill_opacity=0.94,
    ).move_to([0, y, 0])

    left = VGroup(
        Text(f"Scenario {index}", font_size=15, weight=BOLD, color=accent),
        Text(scenario_name, font_size=15, color=NAV_TEXT),
    ).arrange(RIGHT, buff=0.16)
    left.to_edge(LEFT, buff=0.18)
    left.set_y(y)

    right = Text(section_name, font_size=14, color=NAV_MUTED)
    right.scale_to_fit_width(min(right.width, 3.75))
    right.to_edge(RIGHT, buff=0.18)
    right.set_y(y)

    dots = VGroup()
    for i in range(total):
        dot = Circle(radius=0.035, stroke_width=0, fill_opacity=1.0)
        dot.set_fill(accent if i == index else NAV_MUTED, opacity=1.0 if i == index else 0.45)
        dots.add(dot)
    dots.arrange(RIGHT, buff=0.09).move_to([0, y, 0])

    nav = VGroup(bar, left, dots, right)
    nav.set_z_index(1000)
    return nav


def bottom_progress_nav(
    scenario_index,
    total_scenarios,
    scenario_name,
    subscenario_names,
    progress_tracker,
    accent=YELLOW,
):
    """Two-tier persistent progress bar: whole talk and current scenario."""
    frame_w = config.frame_width
    frame_h = config.frame_height
    nav_w = frame_w - 0.28
    bar_center_x = 0
    y_mid = -frame_h / 2 + PROGRESS_NAV_HEIGHT / 2
    y_overall = y_mid + 0.19
    y_detail = y_mid - 0.19
    bar_h = 0.20
    gap = 0.05

    bg = RoundedRectangle(
        width=frame_w,
        height=PROGRESS_NAV_HEIGHT,
        corner_radius=0.10,
        stroke_width=0,
        fill_color=NAV_BG,
        fill_opacity=0.99,
    ).move_to([0, y_mid, 0])
    top_rule = Line(
        [-frame_w / 2, y_mid + PROGRESS_NAV_HEIGHT / 2, 0],
        [frame_w / 2, y_mid + PROGRESS_NAV_HEIGHT / 2, 0],
        color=ManimColor("#334155"),
        stroke_width=1.2,
        stroke_opacity=0.9,
    )

    def label_color(color):
        r, g, b = color.to_rgb()
        return BLACK if (r + g + b) > 1.65 else NAV_TEXT

    def fill_width_for_segment(progress, segment_index, total_segments, width):
        progress = max(0.0, min(progress, total_segments))
        if progress >= segment_index + 1:
            return width
        if progress <= segment_index:
            return 0.0
        return width * (progress - segment_index)

    def update_fill(fill, base, color, width, progress, segment_index, total_segments):
        fill_w = fill_width_for_segment(progress, segment_index, total_segments, width)
        fill.set_opacity(1.0 if progress < segment_index + 1 else 0.54)
        if fill_w <= 1e-3:
            fill.stretch_to_fit_width(1e-3)
            fill.set_opacity(0.0)
        else:
            fill.stretch_to_fit_width(fill_w)
        fill.set_height(base.height)
        fill.align_to(base, LEFT)
        fill.set_y(base.get_y())
        fill.set_fill(color)

    def active_segment(progress, total_segments):
        progress = max(0.0, min(progress, total_segments))
        if progress >= total_segments:
            return total_segments - 1
        return int(progress)

    def update_label(label, progress, segment_index, total_segments, show_inactive_labels):
        is_active = segment_index == active_segment(progress, total_segments)
        if show_inactive_labels:
            label.set_opacity(1.0 if is_active else 0.68)
        else:
            label.set_opacity(1.0 if is_active else 0.0)

    def update_base(base, progress, segment_index, total_segments):
        base.set_stroke(opacity=1.0 if segment_index == active_segment(progress, total_segments) else 0.42)

    def segmented_row(
        names,
        active_index,
        y,
        progress_func,
        palette=None,
        active_label=None,
        width_weights=None,
        show_inactive_labels=True,
    ):
        count = len(names)
        weights = width_weights if width_weights else [1.0] * count
        unit_w = (nav_w - gap * (count - 1)) / sum(weights)
        seg_widths = [unit_w * weight for weight in weights]
        row = VGroup()
        left_edge = bar_center_x - nav_w / 2
        for i, name in enumerate(names):
            color = palette[i % len(palette)] if palette else accent
            seg_w = seg_widths[i]
            x = left_edge + sum(seg_widths[:i]) + gap * i + seg_w / 2
            base = RoundedRectangle(
                width=seg_w,
                height=bar_h,
                corner_radius=PROGRESS_NAV_RADIUS,
                stroke_width=0.7,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.34,
            ).move_to([x, y, 0])
            base.set_stroke(opacity=0.42 if i != active_index else 1.0)
            base.add_updater(
                lambda mob, idx=i, count=count: update_base(mob, progress_func(), idx, count)
            )
            row.add(base)

            fill = RoundedRectangle(
                width=1e-3,
                height=bar_h,
                corner_radius=PROGRESS_NAV_RADIUS,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0,
            )
            fill.align_to(base, LEFT)
            fill.set_y(y)
            fill.add_updater(
                lambda mob, base=base, color=color, seg_w=seg_w, idx=i, count=count: update_fill(
                    mob,
                    base,
                    color,
                    seg_w,
                    progress_func(),
                    idx,
                    count,
                )
            )
            row.add(fill)

            label_text = active_label if i == active_index and active_label else name
            current_only = not show_inactive_labels
            font_size = 13 if current_only else 14 if i == active_index else 11
            label = Text(
                label_text,
                font=NAV_FONT,
                font_size=font_size,
                color=label_color(color) if current_only or i == active_index else NAV_TEXT,
                weight=BOLD if current_only or i == active_index else NORMAL,
            )
            label.scale_to_fit_width(min(label.width, seg_w - 0.12))
            label.move_to(base)
            if current_only or i == active_index:
                label.set_stroke(NAV_BG if label_color(color) == NAV_TEXT else WHITE, width=0.6, opacity=0.75)
            label.set_opacity(1.0 if i == active_index or show_inactive_labels else 0.0)
            label.add_updater(
                lambda mob, idx=i, count=count, show=show_inactive_labels: update_label(
                    mob, progress_func(), idx, count, show
                )
            )
            row.add(label)
        return row

    def scenario_progress():
        progress = max(0.0, min(progress_tracker.get_value(), len(subscenario_names)))
        return scenario_index + progress / max(len(subscenario_names), 1)

    def detail_progress():
        return max(0.0, min(progress_tracker.get_value(), len(subscenario_names)))

    start = NAV_SUB_GRADIENT_STARTS[scenario_index % len(NAV_SUB_GRADIENT_STARTS)]
    end = NAV_SUB_GRADIENT_ENDS[scenario_index % len(NAV_SUB_GRADIENT_ENDS)]
    sub_palette = color_gradient([start, NAV_SCENARIO_COLORS[scenario_index], end], len(subscenario_names))

    overall_names = [f"S{i}" for i in range(total_scenarios)]
    active_scenario_name = (
        NAV_SCENARIO_NAMES[scenario_index]
        if scenario_index < len(NAV_SCENARIO_NAMES)
        else scenario_name
    )
    overall_weights = [1.0] * total_scenarios
    overall_weights[scenario_index] = 3.2
    overall = segmented_row(
        overall_names,
        scenario_index,
        y_overall,
        scenario_progress,
        palette=NAV_SCENARIO_COLORS,
        active_label=f"S{scenario_index}: {active_scenario_name}",
        width_weights=overall_weights,
    )
    detail = segmented_row(
        subscenario_names,
        min(int(detail_progress()), len(subscenario_names) - 1),
        y_detail,
        detail_progress,
        palette=sub_palette,
        active_label=subscenario_names[min(int(detail_progress()), len(subscenario_names) - 1)],
        show_inactive_labels=False,
    )

    nav = VGroup(bg, top_rule, overall, detail)
    nav.set_z_index(1000)
    return nav


def keep_nav(mobjects, nav):
    return [mob for mob in mobjects if mob is not nav and not isinstance(mob, ValueTracker)]
