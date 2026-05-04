"""
Scenario 3 - The VWA Structure
==============================

This scene explains the second-order superharmonic step after Scenario 2.
It starts with one interacting component pair, then expands to the exact
pairwise grid, and finally shows how VWA replaces the full pair-dependent
kernel by two reusable one-dimensional weighted signals.
"""

from manim import *
import numpy as np
from pathlib import Path
from presentation_nav import bottom_progress_nav, keep_nav

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene

C_LINEAR = BLUE
C_EXACT = ORANGE
C_VWA = YELLOW
C_WEIGHT = TEAL
C_PHASE = BLUE_B
C_MUTED = GREY_B
C_PANEL = GREY_D
C_MF12 = ManimColor("#22D3EE")
SCENARIO3_SECONDS = 87.93
SCENARIO3_SUBSCENARIOS = [
    "pair anatomy",
    "kernel grid",
    "variable phase",
    "self kernel",
    "product and FFT",
    "scaling",
    "kernel check",
    "waveforms and Q",
]

KERNEL_DATA_DIR = Path(__file__).resolve().parent / "data" / "kernel_data"
Q_DATA_PATH = Path(__file__).resolve().parent / "data" / "q_metric" / "Q_vs_Alpha_2nd_eta_phi_for_manim.csv"
Q_SWEEP_IMAGE_PATH = Path(__file__).resolve().parent / "data" / "q_metric" / "Q_vs_Alpha_2nd_eta_phi_2x3_manim_cropped.png"
WAVEFORM_DATA_PATH = Path(__file__).resolve().parent / "data" / "waveform_eta22" / "2nd_waveform_kph1_alpha1_data.csv"
WAVEFORM_IMAGE_PATHS = [
    Path(__file__).resolve().parent / "data" / "waveform_eta22" / "2nd_waveform_kph5_alpha8_manim_cropped.png",
    Path(__file__).resolve().parent / "data" / "waveform_eta22" / "2nd_waveform_kph1_alpha1_manim_cropped.png",
]
KERNEL_SUMMARY = {
    "kph_0p5": {
        "label": r"k_p h=0.5",
        "median_rel": "8.8%",
        "max_rel": "329%",
        "average_rel": "33.8%",
        "note": "finite depth: the off-diagonal kernel changes more strongly",
    },
    "kph_5p0": {
        "label": r"k_p h=5.0",
        "median_rel": "0.008%",
        "max_rel": "19.7%",
        "average_rel": "1.3%",
        "note": "intermediate-deep: the self-kernel average tracks the exact kernel",
    },
}


def colored_rect(width, height, color, opacity=0.12):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.3,
        fill_color=color,
        fill_opacity=opacity,
    )


def make_kernel_cell(row, col, rows, cols, width, height, value, color=C_EXACT):
    dx = width / cols
    dy = height / rows
    left = -width / 2
    bottom = -height / 2
    rect = Rectangle(
        width=dx,
        height=dy,
        stroke_width=0.55,
        stroke_color=GREY_E,
        fill_color=interpolate_color(BLUE_E, color, value),
        fill_opacity=0.86,
    )
    rect.move_to([left + (col + 0.5) * dx, bottom + (row + 0.5) * dy, 0])
    return rect


def kernel_value(row, col, rows, cols):
    kh_m = 0.5 + row / (rows - 1) * 3.5
    kh_n = 0.5 + col / (cols - 1) * 3.5
    return eta_kernel_shade(kh_m, kh_n)


def coth(x):
    return np.cosh(x) / np.sinh(x)


def eta_exact_kernel(kh_m, kh_n, h=1.0, g=9.81):
    """MF12/Fuhrman second-order eta sum-interaction kernel, from Lambda2."""
    k_m = kh_m / h
    k_n = kh_n / h
    omega_m = np.sqrt(g * k_m * np.tanh(k_m * h))
    omega_n = np.sqrt(g * k_n * np.tanh(k_n * h))
    omega_sum = omega_m + omega_n
    k_sum = k_m + k_n
    alpha = omega_sum * np.cosh(h * k_sum)
    gamma = k_sum * np.sinh(h * k_sum)
    beta = omega_sum**2 * np.cosh(h * k_sum) - g * k_sum * np.sinh(h * k_sum)
    dot = k_m * k_n
    numerator = (
        g * alpha * (omega_m * (k_n**2 + dot) + omega_n * (k_m**2 + dot))
        + gamma * (g**2 * dot + omega_m**2 * omega_n**2 - omega_m * omega_n * omega_sum**2)
    )
    return h / (2 * omega_m * omega_n * beta) * numerator


def eta_vwa_self_kernel(kh, h=1.0):
    k = kh / h
    th = np.tanh(k * h)
    return k * (3 - th**2) / (4 * th**3)


def eta_kernel_shade(kh_m, kh_n):
    exact = abs(eta_exact_kernel(kh_m, kh_n))
    # Fixed log scaling over the kh range used in compare_eta_phi_kernel_ratio.m.
    shade = (np.log1p(exact) - 0.75) / 1.95
    return float(np.clip(shade, 0.10, 0.95))


def quiet_fade(mob, shift=DOWN * 0.03):
    return FadeIn(mob, shift=shift)


def load_kernel_grid(case_name):
    data = np.genfromtxt(KERNEL_DATA_DIR / f"kernel_grid_{case_name}.csv", delimiter=",", names=True)
    km_vals = np.unique(data["km"])
    kn_vals = np.unique(data["kn"])
    rows = len(km_vals)
    cols = len(kn_vals)
    return {
        "km": km_vals,
        "kn": kn_vals,
        "G_exact": data["G_exact"].reshape(rows, cols),
        "G_vwa": data["G_vwa"].reshape(rows, cols),
        "rel_error": data["rel_error"].reshape(rows, cols),
    }


def signed_heat_color(value, limit):
    if not np.isfinite(value):
        return GREY_E
    scaled = max(-1.0, min(1.0, float(value) / max(limit, 1e-12)))
    if scaled >= 0:
        return interpolate_color(BLACK, C_EXACT, scaled)
    return interpolate_color(BLACK, C_LINEAR, -scaled)


def error_heat_color(value, limit):
    if not np.isfinite(value):
        return GREY_E
    scaled = max(0.0, min(1.0, float(value) / max(limit, 1e-12)))
    return interpolate_color(BLACK, C_VWA, scaled)


def kernel_magnitude_color(value, limit):
    if not np.isfinite(value):
        return GREY_E
    scaled = max(0.0, min(1.0, np.log1p(abs(float(value))) / max(np.log1p(limit), 1e-12)))
    if scaled < 0.42:
        return interpolate_color(BLACK, BLUE_E, scaled / 0.42)
    if scaled < 0.78:
        return interpolate_color(BLUE_E, TEAL_E, (scaled - 0.42) / 0.36)
    return interpolate_color(TEAL_E, YELLOW_D, (scaled - 0.78) / 0.22)


def kernel_heatmap_panel(case_name, field_name, title, width=3.05, height=2.18, max_cells=34):
    grid = load_kernel_grid(case_name)
    values = grid[field_name]
    row_idx = np.linspace(0, values.shape[0] - 1, max_cells).astype(int)
    col_idx = np.linspace(0, values.shape[1] - 1, max_cells).astype(int)
    sampled = values[np.ix_(row_idx, col_idx)]
    if field_name == "rel_error":
        finite = sampled[np.isfinite(sampled)]
        limit = float(np.nanpercentile(finite, 96)) if finite.size else 1.0
    else:
        exact = grid["G_exact"][np.isfinite(grid["G_exact"])]
        limit = float(np.nanpercentile(np.abs(exact), 96)) if exact.size else 1.0

    cells = VGroup()
    cell_w = width / len(col_idx)
    cell_h = height / len(row_idx)
    for r, row in enumerate(row_idx):
        for c, col in enumerate(col_idx):
            value = values[row, col]
            color = error_heat_color(value, limit) if field_name == "rel_error" else signed_heat_color(value, limit)
            rect = Rectangle(width=cell_w + 0.002, height=cell_h + 0.002, stroke_width=0, fill_color=color, fill_opacity=1)
            rect.move_to([
                -width / 2 + (c + 0.5) * cell_w,
                -height / 2 + (len(row_idx) - r - 0.5) * cell_h,
                0,
            ])
            cells.add(rect)

    border = Rectangle(width=width, height=height, stroke_color=GREY_C, stroke_width=1.0, fill_opacity=0)
    title_mob = Text(title, font_size=22, color=WHITE).next_to(border, UP, buff=0.10)
    x_lab = MathTex(r"k_n/k_p", font_size=20, color=C_MUTED).next_to(border, DOWN, buff=0.08)
    y_lab = MathTex(r"k_m/k_p", font_size=20, color=C_MUTED).rotate(90 * DEGREES).next_to(border, LEFT, buff=0.08)
    return VGroup(cells, border, title_mob, x_lab, y_lab)


def split_kernel_panel(case_name, title, width=3.52, height=3.52, max_cells=200):
    grid = load_kernel_grid(case_name)
    exact = grid["G_exact"]
    vwa = grid["G_vwa"]
    km_values = grid["km"]
    kn_values = grid["kn"]
    row_idx = np.linspace(0, exact.shape[0] - 1, max_cells).astype(int)
    col_idx = np.linspace(0, exact.shape[1] - 1, max_cells).astype(int)
    km_mesh, kn_mesh = np.meshgrid(km_values, kn_values, indexing="ij")
    exact_display = np.abs(exact) / np.maximum(km_mesh * kn_mesh, 1e-12)
    vwa_display = np.abs(vwa) / np.maximum(km_mesh * kn_mesh, 1e-12)
    finite = exact_display[np.isfinite(exact_display)]
    limit = float(np.nanpercentile(np.abs(finite), 96)) if finite.size else 1.0

    n = len(row_idx)
    combined_sampled = np.zeros((n, n))
    cell_w = width / len(col_idx)
    cell_h = height / len(row_idx)
    for r, row in enumerate(row_idx):
        for c, col in enumerate(col_idx):
            # Origin is at the lower left: upper triangle uses exact, lower triangle uses VWA.
            use_exact = r >= c
            value = exact_display[row, col] if use_exact else vwa_display[row, col]
            combined_sampled[r, c] = value

    image_size = 420
    rgb = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    for iy in range(image_size):
        r = int(round((image_size - 1 - iy) / (image_size - 1) * (n - 1)))
        for ix in range(image_size):
            c = int(round(ix / (image_size - 1) * (n - 1)))
            color = kernel_magnitude_color(combined_sampled[r, c], limit).to_rgb()
            rgb[iy, ix, :] = np.clip(np.array(color) * 255, 0, 255).astype(np.uint8)

    heatmap = ImageMobject(rgb)
    heatmap.set_resampling_algorithm(RESAMPLING_ALGORITHMS["lanczos"])
    heatmap.set_width(width)
    heatmap.stretch_to_fit_height(height)

    border = Rectangle(width=width, height=height, stroke_color=GREY_C, stroke_width=1.0, fill_opacity=0)
    diag = Line(border.get_corner(DL), border.get_corner(UR), color=WHITE, stroke_width=2.1)
    title_mob = MathTex(title, font_size=28, color=WHITE).next_to(border, UP, buff=0.10)
    exact_label = Text("MF12", font_size=22, color=WHITE, weight=BOLD).move_to(border.get_center() + LEFT * 0.98 + UP * 0.88)
    vwa_label = Text("VWA", font_size=22, color=YELLOW_C, weight=BOLD).move_to(border.get_center() + RIGHT * 0.98 + DOWN * 0.82)
    x_lab = MathTex(r"k_n/k_p", font_size=22, color=C_MUTED).next_to(border, DOWN, buff=0.16)
    y_lab = MathTex(r"k_m/k_p", font_size=22, color=C_MUTED).rotate(90 * DEGREES).next_to(border, LEFT, buff=0.08)
    ticks = VGroup(
        MathTex("0.2", font_size=18, color=WHITE).next_to(border.get_corner(DL), DOWN, buff=0.04).shift(LEFT * 0.06),
        MathTex("2.5", font_size=18, color=WHITE).next_to(border.get_corner(DR), DOWN, buff=0.04).shift(RIGHT * 0.06),
        MathTex("0.2", font_size=18, color=WHITE).next_to(border.get_corner(DL), LEFT, buff=0.07),
        MathTex("2.5", font_size=18, color=WHITE).next_to(border.get_corner(UL), LEFT, buff=0.07),
    )
    levels = np.nanpercentile(
        np.log1p(np.abs(combined_sampled[np.isfinite(combined_sampled)])),
        [15, 25, 35, 45, 55, 65, 75, 85, 92],
    )
    contours = VGroup()
    contour_field = np.log1p(np.abs(combined_sampled))

    def interp_point(p0, p1, v0, v1, level):
        if abs(v1 - v0) < 1e-12:
            alpha = 0.5
        else:
            alpha = float((level - v0) / (v1 - v0))
        alpha = max(0.0, min(1.0, alpha))
        return p0 + alpha * (p1 - p0)

    for level in levels:
        for r in range(n - 1):
            for c in range(n - 1):
                v00 = contour_field[r, c]
                v10 = contour_field[r, c + 1]
                v11 = contour_field[r + 1, c + 1]
                v01 = contour_field[r + 1, c]
                x0 = -width / 2 + c * cell_w
                x1 = -width / 2 + (c + 1) * cell_w
                y0 = -height / 2 + r * cell_h
                y1 = -height / 2 + (r + 1) * cell_h
                p00 = np.array([x0, y0, 0])
                p10 = np.array([x1, y0, 0])
                p11 = np.array([x1, y1, 0])
                p01 = np.array([x0, y1, 0])
                crossings = []
                edges = [(p00, p10, v00, v10), (p10, p11, v10, v11), (p01, p11, v01, v11), (p00, p01, v00, v01)]
                for p_a, p_b, v_a, v_b in edges:
                    if (v_a - level) * (v_b - level) <= 0 and v_a != v_b:
                        crossings.append(interp_point(p_a, p_b, v_a, v_b, level))
                if len(crossings) == 2:
                    contours.add(Line(crossings[0], crossings[1], color=WHITE, stroke_width=1.25, stroke_opacity=0.62))
                elif len(crossings) == 4:
                    contours.add(Line(crossings[0], crossings[1], color=WHITE, stroke_width=1.20, stroke_opacity=0.58))
                    contours.add(Line(crossings[2], crossings[3], color=WHITE, stroke_width=1.20, stroke_opacity=0.58))
    return Group(heatmap, contours, border, diag, title_mob, exact_label, vwa_label, x_lab, y_lab, ticks)


def make_split_kernel_comparison_slide():
    title = Text("Split kernel comparison", font_size=34, weight=BOLD)
    subtitle = Text("upper triangle: exact theory (MF12); lower triangle: VWA kernel", font_size=22, color=C_MUTED)
    colour_note = MathTex(r"\hbox{colour and contours: } |G|/(k_m k_n)", font_size=22, color=C_MUTED)
    header = VGroup(title, subtitle, colour_note).arrange(DOWN, buff=0.06).to_edge(UP, buff=0.18)

    clean = split_kernel_panel("kph_5p0", r"k_p h=5.0")
    hard = split_kernel_panel("kph_0p5", r"k_p h=0.5")
    panels = Group(clean, hard).arrange(RIGHT, buff=0.92).next_to(header, DOWN, buff=0.20)
    panels.scale_to_fit_width(10.7)

    formula = MathTex(
        r"G_{\rm VWA}(k_m,k_n)={1\over2}\left[G(k_m,k_m)+G(k_n,k_n)\right]",
        font_size=28,
        color=C_VWA,
    ).next_to(panels, DOWN, buff=0.18)
    takeaway = Text(
        "Normalization only makes the kernel shape easier to compare; waveform errors are assessed separately.",
        font_size=20,
        color=C_MUTED,
    ).next_to(formula, DOWN, buff=0.12)
    return Group(header, panels, formula, takeaway)


def make_amplitude_approximation_question_slide():
    title = Text("So what still needs to be checked?", font_size=36, weight=BOLD)
    subtitle = Text(
        "VWA is fast, and it preserves the pair phase structure.",
        font_size=25,
        color=C_MUTED,
    )
    header = VGroup(title, subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.28)

    left = VGroup(
        Text("phase structure", font_size=25, color=C_PHASE, weight=BOLD),
        MathTex(r"\theta_m+\theta_n,\quad k_m+k_n", font_size=34, color=C_PHASE),
        Text("kept pair by pair", font_size=23, color=C_MUTED),
    ).arrange(DOWN, buff=0.12)
    left_box = SurroundingRectangle(left, color=C_PHASE, buff=0.22, corner_radius=0.08).set_fill(C_PHASE, opacity=0.07)
    left.add_to_back(left_box)

    right = VGroup(
        Text("cost", font_size=25, color=C_WEIGHT, weight=BOLD),
        MathTex(r"\mathcal O(N_c^2)\quad\longrightarrow\quad\mathcal O(N_c\log N_c)", font_size=31, color=C_WEIGHT),
        Text("exact summation avoided", font_size=23, color=C_MUTED),
    ).arrange(DOWN, buff=0.12)
    right.scale_to_fit_width(5.35)
    right_box = SurroundingRectangle(right, color=C_WEIGHT, buff=0.22, corner_radius=0.08).set_fill(C_WEIGHT, opacity=0.07)
    right.add_to_back(right_box)

    known = VGroup(left, right).arrange(RIGHT, buff=0.58).next_to(header, DOWN, buff=0.46)

    question = VGroup(
        Text("The remaining question is amplitude.", font_size=30, color=WHITE, weight=BOLD),
        MathTex(
            r"G(k_m,k_n)",
            r"\quad \hbox{vs.} \quad",
            r"{1\over2}\left[G(k_m,k_m)+G(k_n,k_n)\right]",
            font_size=34,
        ),
        Text("How good or bad is that approximation across the kernel plane?", font_size=24, color=C_MUTED),
    ).arrange(DOWN, buff=0.16).next_to(known, DOWN, buff=0.50)
    question[1][0].set_color(C_EXACT)
    question[1][2].set_color(C_VWA)

    arrow = Arrow(question.get_bottom() + DOWN * 0.08, question.get_bottom() + DOWN * 0.48, color=C_VWA, stroke_width=3)
    next_note = Text("next: split kernel comparison", font_size=25, color=C_VWA, weight=BOLD).next_to(arrow, DOWN, buff=0.10)

    return VGroup(header, known, question, arrow, next_note)


def load_q_metric_rows():
    if not Q_DATA_PATH.exists():
        return None
    return np.genfromtxt(Q_DATA_PATH, delimiter=",", names=True, dtype=None, encoding="utf-8")


def q_series(quantity="eta22", method="VWA", kpd=1.0):
    data = load_q_metric_rows()
    if data is None:
        return np.array([]), np.array([])
    mask = (
        (data["quantity"] == quantity)
        & (data["method"] == method)
        & np.isclose(data["kpd"].astype(float), kpd)
    )
    rows = data[mask]
    if rows.size == 0:
        return np.array([]), np.array([])
    order = np.argsort(rows["alpha"].astype(float))
    return rows["alpha"].astype(float)[order], rows["Q"].astype(float)[order]


def curve_from_xy(axes, xs, ys, color, stroke_width=4.0):
    curve = VMobject(color=color, stroke_width=stroke_width)
    points = [axes.c2p(float(x), float(y)) for x, y in zip(xs, ys) if np.isfinite(y)]
    if len(points) >= 2:
        curve.set_points_smoothly(points)
    return curve


def load_waveform_rows():
    if not WAVEFORM_DATA_PATH.exists():
        return None
    return np.genfromtxt(WAVEFORM_DATA_PATH, delimiter=",", names=True, dtype=None, encoding="utf-8")


def make_waveform_comparison_space_slide(image_index=0):
    if image_index < len(WAVEFORM_IMAGE_PATHS) and WAVEFORM_IMAGE_PATHS[image_index].exists():
        image = ImageMobject(str(WAVEFORM_IMAGE_PATHS[image_index]))
        image.set_width(13.25)
        image.to_edge(UP, buff=0.08)
        return Group(image)

    title = Text("Waveform comparison", font_size=35, weight=BOLD)
    subtitle = Text(
        "export a Manim-style waveform PNG to populate this slide",
        font_size=22,
        color=C_MUTED,
    )
    placeholder = RoundedRectangle(
        width=10.6,
        height=4.75,
        corner_radius=0.08,
        stroke_color=C_EXACT,
        fill_color=C_EXACT,
        fill_opacity=0.06,
    )
    label = Text("waiting for waveform figure", font_size=28, color=C_MUTED).move_to(placeholder)
    return VGroup(title, subtitle, placeholder, label).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.22)


def make_q_metric_slide():
    title = Text("A spectrum-level error metric", font_size=35, weight=BOLD)
    subtitle = Text(
        "Q compares the resolved second-order field against MF12 in Fourier space",
        font_size=22,
        color=C_MUTED,
    )
    header = VGroup(title, subtitle).arrange(DOWN, buff=0.07).to_edge(UP, buff=0.22)

    formula = MathTex(
        r"Q(f,g)=",
        r"{\sum_{k>0}\left|\widehat f(k)-\widehat g(k)\right|",
        r"\over",
        r"\sum_{k>0}\left(\left|\widehat f(k)\right|+\left|\widehat g(k)\right|\right)}",
        font_size=38,
    ).next_to(header, DOWN, buff=0.55)
    formula[0].set_color(C_VWA)

    ref = VGroup(
        MathTex(r"f=\eta^{(22)}_{\rm MF12}", font_size=29, color=C_EXACT),
        MathTex(r"g=\eta^{(22)}_{\rm model}", font_size=29, color=C_VWA),
    ).arrange(RIGHT, buff=0.72).next_to(formula, DOWN, buff=0.40)

    low = VGroup(
        Text("Q = 0", font_size=27, color=C_VWA, weight=BOLD),
        Text("spectra match", font_size=22, color=C_MUTED),
    ).arrange(DOWN, buff=0.05)
    high = VGroup(
        Text("larger Q", font_size=27, color=C_EXACT, weight=BOLD),
        Text("more spectral mismatch", font_size=22, color=C_MUTED),
    ).arrange(DOWN, buff=0.05)
    cards = VGroup(low, high).arrange(RIGHT, buff=1.15).next_to(ref, DOWN, buff=0.48)
    for card, color in [(low, C_VWA), (high, C_EXACT)]:
        box = SurroundingRectangle(card, color=color, buff=0.18, corner_radius=0.08).set_fill(color, opacity=0.08)
        card.add_to_back(box)

    return VGroup(header, formula, ref, cards)


def make_q_sweep_slide():
    if Q_SWEEP_IMAGE_PATH.exists():
        image = ImageMobject(str(Q_SWEEP_IMAGE_PATH))
        image.set_height(6.85)
        image.to_edge(UP, buff=0.08)
        return Group(image)

    title = Text("Q sweep over bandwidth and depth", font_size=34, weight=BOLD)
    subtitle = Text(
        r"same 2x3 structure as the MATLAB result: columns are water depth",
        font_size=21,
        color=C_MUTED,
    )
    header = VGroup(title, subtitle).arrange(DOWN, buff=0.06).to_edge(UP, buff=0.18)

    method_styles = {
        "VWA": (C_VWA, 3.0),
        "NLS": (GREEN_B, 2.6),
        "Walker": (PURPLE_A, 2.6),
        "Creamer": (GREY_A, 2.4),
    }

    def mini_panel(quantity, kpd, title_tex, row_label=None, show_x=False, show_y=False):
        axes = Axes(
            x_range=[0.5, 8.0, 2.5],
            y_range=[0.0, 0.70, 0.35],
            x_length=3.15,
            y_length=1.50,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 1.1},
            x_axis_config={"numbers_to_include": [0.5, 4, 8] if show_x else []},
            y_axis_config={"numbers_to_include": [0, 0.35, 0.7] if show_y else []},
        )
        curves = VGroup()
        methods = ["VWA", "NLS", "Walker", "Creamer"] if quantity == "eta22" else ["VWA"]
        for method in methods:
            xs, ys = q_series(quantity, method, kpd)
            if not xs.size:
                continue
            color, stroke = method_styles.get(method, (BLUE_B, 2.6))
            if quantity == "phi22":
                color, stroke = BLUE_B, 3.0
            curves.add(curve_from_xy(axes, xs, ys, color=color, stroke_width=stroke))
        title_mob = MathTex(title_tex, font_size=20, color=WHITE).next_to(axes, UP, buff=0.05)
        label_group = VGroup(title_mob, axes, curves)
        if row_label:
            row_mob = MathTex(row_label, font_size=22, color=C_MUTED).rotate(90 * DEGREES)
            row_mob.next_to(axes, LEFT, buff=0.34)
            label_group.add(row_mob)
        if show_x:
            x_lab = MathTex(r"\alpha", font_size=20, color=C_MUTED).next_to(axes.x_axis, DOWN, buff=0.12)
            label_group.add(x_lab)
        if show_y:
            y_lab = MathTex(r"Q", font_size=20, color=C_MUTED).next_to(axes.y_axis, LEFT, buff=0.11)
            label_group.add(y_lab)
        return label_group

    depths = [(5.0, r"k_p h=5"), (2.0, r"k_p h=2"), (1.0, r"k_p h=1")]
    top = VGroup(*[
        mini_panel("eta22", kpd, label, row_label=r"\eta^{(22)}" if i == 0 else None, show_y=i == 0)
        for i, (kpd, label) in enumerate(depths)
    ]).arrange(RIGHT, buff=0.38, aligned_edge=DOWN)
    bottom = VGroup(*[
        mini_panel("phi22", kpd, label, row_label=r"\phi_s^{(22)}" if i == 0 else None, show_x=True, show_y=i == 0)
        for i, (kpd, label) in enumerate(depths)
    ]).arrange(RIGHT, buff=0.38, aligned_edge=DOWN)
    panels = VGroup(top, bottom).arrange(DOWN, buff=0.32).next_to(header, DOWN, buff=0.24)
    panels.scale_to_fit_width(11.1)

    legend_items = VGroup()
    for name in ["VWA", "NLS", "Walker", "Creamer"]:
        color, stroke = method_styles[name]
        legend_items.add(
            VGroup(Line(LEFT * 0.20, RIGHT * 0.20, color=color, stroke_width=stroke), Text(name, font_size=17, color=WHITE)).arrange(RIGHT, buff=0.08)
        )
    legend_items.add(
        VGroup(Line(LEFT * 0.20, RIGHT * 0.20, color=BLUE_B, stroke_width=3.0), MathTex(r"VWA\ \phi_s^{(22)}", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.08)
    )
    legend = legend_items.arrange(RIGHT, buff=0.28)
    legend.next_to(panels, DOWN, buff=0.18)
    note = Text("lower Q means closer to the MF12 reference", font_size=19, color=C_MUTED).next_to(legend, DOWN, buff=0.08)

    return VGroup(header, panels, legend, note)


def make_kernel_validation_slide(case_name, heading, show_challenge=False):
    summary = KERNEL_SUMMARY[case_name]
    title = Text(heading, font_size=34, weight=BOLD)
    subtitle = MathTex(summary["label"], font_size=28, color=C_VWA)
    header = VGroup(title, subtitle).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.22)

    exact_panel = kernel_heatmap_panel(case_name, "G_exact", "exact kernel")
    vwa_panel = kernel_heatmap_panel(case_name, "G_vwa", "self-kernel average")
    err_panel = kernel_heatmap_panel(case_name, "rel_error", "relative error")
    panels = VGroup(exact_panel, vwa_panel, err_panel).arrange(RIGHT, buff=0.44).next_to(header, DOWN, buff=0.26)
    panels.scale_to_fit_width(11.3)

    formula = MathTex(
        r"G_{\rm VWA}(k_m,k_n)",
        r"={1\over2}\left[G(k_m,k_m)+G(k_n,k_n)\right]",
        font_size=30,
        color=C_VWA,
    )
    formula.next_to(panels, DOWN, buff=0.20)
    stats = VGroup(
        VGroup(Text("median rel. error", font_size=19, color=C_MUTED), Text(summary["median_rel"], font_size=25, color=C_VWA)).arrange(DOWN, buff=0.04),
        VGroup(Text("max rel. error", font_size=19, color=C_MUTED), Text(summary["max_rel"], font_size=25, color=C_EXACT if show_challenge else C_MUTED)).arrange(DOWN, buff=0.04),
        Text(summary["note"], font_size=20, color=C_MUTED),
    ).arrange(RIGHT, buff=0.50)
    stats.next_to(formula, DOWN, buff=0.18)
    stats.scale_to_fit_width(10.9)
    return VGroup(header, panels, formula, stats)


def play_product_average_bridge(scene, fade_out=True, nav=None, nav_progress=None):
    """Show the analytic convolution/product bridge as a standalone beat."""
    def pause(progress=None, duration=0.8):
        if hasattr(scene, "slide_pause"):
            scene.slide_pause(nav_progress, progress)
        else:
            scene.wait(duration)

    bridge_title = Text("Why the product gives the average", font_size=34, weight=BOLD)
    bridge_subtitle = Text("the phase structure is unchanged; only the kernel is approximated", font_size=22, color=C_MUTED)
    VGroup(bridge_title, bridge_subtitle).arrange(DOWN, buff=0.10).to_edge(UP, buff=0.20)
    scene.play(quiet_fade(bridge_title), quiet_fade(bridge_subtitle), run_time=0.7)

    exact_exp = VGroup(
        Text("exact theory", font_size=22, color=C_EXACT),
        MathTex(
            r"\eta_{\rm exact}^{(22)}",
            r"=",
            r"\Re\!\left\{\sum_m\sum_n",
            r"a_m a_n",
            r"G(k_m,k_n)",
            r"e^{i(\theta_m+\theta_n)}",
            r"\right\}",
            font_size=24,
        ),
    ).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
    exact_exp[1][4].set_color(C_EXACT)
    exact_exp[1][5].set_color(C_PHASE)
    exact_kernel_box = SurroundingRectangle(exact_exp[1][4], color=C_EXACT, buff=0.06, corner_radius=0.04)
    exact_kernel_box.set_stroke(width=2.0)
    exact_exp.add(exact_kernel_box)
    exact_exp.scale_to_fit_width(9.2)
    exact_exp.next_to(bridge_subtitle, DOWN, buff=0.18)

    vwa_title = Text("VWA analytical product", font_size=23, color=C_VWA)
    vwa_line_m = MathTex(
        r"\Re\!\left\{\eta_{a,G}^{(11)}\eta_a^{(11)}\right\}",
        r"=",
        r"\Re\!\left\{\sum_m\sum_n",
        r"a_m a_n",
        r"G(k_m,k_m)",
        r"e^{i(\theta_m+\theta_n)}",
        r"\right\}",
        font_size=18,
    )
    vwa_line_n = MathTex(
        r"=",
        r"\Re\!\left\{\sum_m\sum_n",
        r"a_m a_n",
        r"G(k_n,k_n)",
        r"e^{i(\theta_m+\theta_n)}",
        r"\right\}",
        font_size=18,
    )
    vwa_line_avg = MathTex(
        r"=",
        r"\Re\!\left\{\sum_m\sum_n",
        r"a_m a_n",
        r"{1\over2}\left[G(k_m,k_m)+G(k_n,k_n)\right]",
        r"e^{i(\theta_m+\theta_n)}",
        r"\right\}",
        font_size=18,
    )
    vwa_line_m[4].set_color(C_WEIGHT)
    vwa_line_m[5].set_color(C_PHASE)
    vwa_line_n[3].set_color(C_WEIGHT)
    vwa_line_n[4].set_color(C_PHASE)
    vwa_line_avg[3].set_color(C_WEIGHT)
    vwa_line_avg[4].set_color(C_PHASE)
    vwa_product = VGroup(vwa_title, vwa_line_m, vwa_line_n, vwa_line_avg).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    avg_amp_box = SurroundingRectangle(vwa_line_avg[3], color=C_WEIGHT, buff=0.05, corner_radius=0.04)
    avg_amp_box.set_stroke(width=2.0)
    vwa_product.add(avg_amp_box)
    vwa_product.scale_to_fit_width(8.2)
    vwa_product.next_to(exact_exp, DOWN, buff=0.10, aligned_edge=LEFT)

    match_note = VGroup(
        Text("matched phase", font_size=24, color=C_PHASE),
        MathTex(
            r"a_m a_n\,e^{i(\theta_m+\theta_n)}",
            font_size=24,
            color=C_PHASE,
        ),
        Text("amplitude", font_size=18, color=C_WEIGHT),
        Text("changes", font_size=18, color=C_WEIGHT),
    ).arrange(DOWN, buff=0.04)
    match_note.move_to([5.05, -0.82, 0.0])

    exact_kernel_focus = VGroup(exact_exp[1][4], exact_kernel_box)
    avg_kernel_focus = VGroup(vwa_line_avg[3], avg_amp_box)

    scene.play(quiet_fade(exact_exp), run_time=0.8)
    scene.play(quiet_fade(vwa_title), quiet_fade(vwa_line_m), run_time=0.8)
    pause(duration=4.0)
    scene.play(quiet_fade(vwa_line_n), run_time=0.7)
    pause(duration=1.6)
    scene.play(quiet_fade(vwa_line_avg), run_time=0.8)
    pause(duration=1.4)
    scene.play(
        exact_kernel_focus.animate.scale(1.18),
        avg_kernel_focus.animate.scale(1.18),
        run_time=0.45,
    )
    scene.wait(0.35)
    scene.play(
        exact_kernel_focus.animate.scale(1 / 1.18),
        avg_kernel_focus.animate.scale(1 / 1.18),
        run_time=0.45,
    )
    scene.wait(0.3)
    scene.play(quiet_fade(match_note), run_time=0.7)
    pause(progress=4.0, duration=3.5)
    if fade_out:
        scene.play(*[FadeOut(mob) for mob in keep_nav(list(scene.mobjects), nav)] if nav is not None else [FadeOut(mob) for mob in list(scene.mobjects)])
        scene.clear()
        if nav is not None:
            if nav_progress is not None:
                scene.add(nav_progress, nav)
            else:
                scene.add(nav)


class TheVWAIdeaBridgePreview(Scene):
    def construct(self):
        play_product_average_bridge(self, fade_out=False)


class S3KernelSplitPreview(Scene):
    def construct(self):
        self.add(make_split_kernel_comparison_slide())


class S3WaveformAndQPreview(Scene):
    def construct(self):
        slides = VGroup(
            make_waveform_comparison_space_slide(0),
            make_waveform_comparison_space_slide(1),
            make_q_metric_slide(),
            make_q_sweep_slide(),
        ).arrange(DOWN, buff=0.8)
        slides.scale_to_fit_height(config.frame_height - 0.5)
        self.add(slides)


class S3WaveformSpacePreview(Scene):
    def construct(self):
        previews = Group(
            make_waveform_comparison_space_slide(0),
            make_waveform_comparison_space_slide(1),
        ).arrange(DOWN, buff=0.55)
        previews.scale_to_fit_height(config.frame_height - 0.25)
        self.add(previews)


class S3QMetricPreview(Scene):
    def construct(self):
        self.add(make_q_metric_slide())


class S3QSweepPreview(Scene):
    def construct(self):
        self.add(make_q_sweep_slide())


class S3VWAStructureSlides(Slide):
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
        title = Text("The VWA idea", font_size=36, weight=BOLD)
        subtitle = Text("from pairwise kernels to spectral products", font_size=24, color=C_MUTED)
        VGroup(title, subtitle).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.18)
        nav_progress = ValueTracker(0)
        nav = bottom_progress_nav(
            3,
            6,
            "VWA structure",
            SCENARIO3_SUBSCENARIOS,
            nav_progress,
            accent=C_VWA,
            detail_label_color=WHITE,
            detail_font_size=16,
            detail_label_stroke=False,
        )
        self.add(nav_progress, nav)
        self.play(quiet_fade(title), quiet_fade(subtitle), run_time=0.7)
        self.slide_pause(nav_progress, 0.35)

        # Act 1: put the explicit second-order sum on screen, then explain one term.
        exact_intro = VGroup(
            Text("Start from the exact second-order sum", font_size=28, color=WHITE),
            MathTex(
                r"\eta_{\rm exact}^{(22)}(x,t)",
                r"=",
                r"\sum_{m=1}^{N_c}\sum_{n=1}^{N_c}",
                r"a_m a_n",
                r"G_{m+n}(k_m,k_n)",
                r"\cos(\theta_m+\theta_n)",
                font_size=30,
            ),
        ).arrange(DOWN, buff=0.22).move_to([0.0, 1.55, 0.0])
        exact_intro[1][4].set_color(C_EXACT)
        exact_intro[1][5].set_color(C_PHASE)
        exact_intro.scale_to_fit_width(11.2)
        self.play(quiet_fade(exact_intro))
        self.slide_pause(nav_progress, 1.0)

        pair_title = Text("Each term has two jobs", font_size=28, color=WHITE).move_to([0.0, 1.52, 0.0])
        km_card = VGroup(
            MathTex(r"k_m,\ a_m,\ \theta_m", font_size=31, color=C_LINEAR),
            Text("component m", font_size=22, color=C_MUTED),
        ).arrange(DOWN, buff=0.08)
        kn_card = VGroup(
            MathTex(r"k_n,\ a_n,\ \theta_n", font_size=31, color=C_LINEAR),
            Text("component n", font_size=22, color=C_MUTED),
        ).arrange(DOWN, buff=0.08)
        plus = MathTex("+", font_size=42, color=C_MUTED)
        pair_group = VGroup(km_card, plus, kn_card).arrange(RIGHT, buff=0.40).next_to(pair_title, DOWN, buff=0.24)

        phase_card = VGroup(
            Text("where the bound wave appears", font_size=22, color=C_PHASE),
            MathTex(r"\theta_m+\theta_n", font_size=38, color=C_PHASE),
        ).arrange(DOWN, buff=0.10)
        amp_card = VGroup(
            Text("how strongly it appears", font_size=22, color=C_EXACT),
            MathTex(r"a_m a_n\,G(k_m,k_n)", font_size=33, color=C_EXACT),
        ).arrange(DOWN, buff=0.10)
        term = MathTex(
            r"a_m a_n\,G(k_m,k_n)",
            r"\cos(\theta_m+\theta_n)",
            font_size=34,
        )
        term[0].set_color(C_EXACT)
        term[1].set_color(C_PHASE)

        decomposition = VGroup(amp_card, phase_card).arrange(RIGHT, buff=0.70).next_to(pair_group, DOWN, buff=0.46)
        term.next_to(decomposition, DOWN, buff=0.38)
        term.scale_to_fit_width(6.6)
        term_box = SurroundingRectangle(term, color=C_PANEL, buff=0.16, corner_radius=0.08).set_fill(BLACK, opacity=0.08)

        self.play(ReplacementTransform(exact_intro[0], pair_title), FadeOut(exact_intro[1]))
        self.play(FadeIn(pair_group, shift=DOWN * 0.08))
        self.play(FadeIn(amp_card, shift=LEFT * 0.10), FadeIn(phase_card, shift=RIGHT * 0.10))
        self.play(Create(term_box), quiet_fade(term))
        self.slide_pause(nav_progress, 1.45)

        bridge_line = Text(
            "Exact theory repeats this lookup for every component pair.",
            font_size=24,
            color=C_MUTED,
        ).to_edge(DOWN, buff=0.92)
        self.play(quiet_fade(bridge_line))
        self.slide_pause(nav_progress, 1.85)
        self.play(
            *[FadeOut(mob) for mob in [pair_title, pair_group, decomposition, term, term_box, bridge_line]],
        )

        # Act 2: exact second-order theory as a full pairwise lookup table.
        rows = cols = 9
        grid_w = 3.60
        grid_h = 3.05
        exact_grid = VGroup()
        for row in range(rows):
            for col in range(cols):
                exact_grid.add(make_kernel_cell(row, col, rows, cols, grid_w, grid_h, kernel_value(row, col, rows, cols)))
        exact_grid.to_edge(LEFT, buff=0.82).shift(DOWN * 0.36)
        exact_box = SurroundingRectangle(exact_grid, color=C_EXACT, buff=0.06, corner_radius=0.06)
        exact_head = Text("exact second-order theory", font_size=26, color=C_EXACT).next_to(exact_grid, UP, buff=0.20)
        exact_x = MathTex("k_n", font_size=24, color=C_MUTED).next_to(exact_grid, DOWN, buff=0.10)
        exact_y = MathTex("k_m", font_size=24, color=C_MUTED).rotate(90 * DEGREES).next_to(exact_grid, LEFT, buff=0.12)
        exact_caption = VGroup(
            MathTex(r"G_{m+n}(k_m,k_n)", font_size=28, color=C_EXACT),
            Text("MF12/Fuhrman eta kernel", font_size=23, color=C_MUTED),
        ).arrange(DOWN, buff=0.08).next_to(exact_grid, DOWN, buff=0.42)

        exact_eq = VGroup(
            MathTex(
                r"\eta_{\rm exact}^{(22)}",
                r"=",
                r"\sum_{m=1}^{N_c}\sum_{n=1}^{N_c}",
                r"a_m a_n",
                r"G_{m+n}(k_m,k_n)",
                r"\cos(\theta_m+\theta_n)",
                font_size=28,
            ),
            Text("accurate, but the kernel is a two-index object", font_size=22, color=C_MUTED),
        ).arrange(DOWN, buff=0.18).to_edge(RIGHT, buff=0.56).shift(UP * 1.40)
        exact_eq.scale_to_fit_width(6.0)
        exact_eq[0][4].set_color(C_EXACT)
        exact_eq[0][5].set_color(C_PHASE)

        sample_row = 2
        sample_col = 6
        sample_cell = exact_grid[sample_row * cols + sample_col]
        row_line = Line(exact_grid[sample_row * cols].get_left(), exact_grid[sample_row * cols + cols - 1].get_right(), color=WHITE, stroke_width=2)
        col_line = Line(exact_grid[sample_col].get_bottom(), exact_grid[(rows - 1) * cols + sample_col].get_top(), color=WHITE, stroke_width=2)
        sample_dot = Dot(sample_cell.get_center(), color=WHITE, radius=0.065)
        sample_label = MathTex(r"G(k_m,k_n)", font_size=25, color=WHITE).next_to(sample_dot, UR, buff=0.12)

        cost_exact = VGroup(
            MathTex(r"N_c^2", font_size=44, color=C_EXACT),
            Text("kernel entries", font_size=23, color=C_MUTED),
        ).arrange(DOWN, buff=0.08).next_to(exact_eq, DOWN, buff=0.64)

        self.play(
            FadeIn(exact_grid, lag_ratio=0.02),
            Create(exact_box),
            quiet_fade(exact_head),
            quiet_fade(exact_x),
            quiet_fade(exact_y),
        )
        self.play(quiet_fade(exact_caption), quiet_fade(exact_eq))
        self.play(Create(row_line), Create(col_line), FadeIn(sample_dot), quiet_fade(sample_label))
        self.play(quiet_fade(cost_exact))
        self.slide_pause(nav_progress, 2.0)

        # Act 3: introduce the variable wavenumber before the kernel approximation.
        phase_head = Text("First: the pair fixes the bound phase", font_size=25, color=C_PHASE)
        phase_eq = MathTex(
            r"\theta_m+\theta_n",
            r"\quad\Rightarrow\quad",
            r"k_m+k_n",
            font_size=35,
        )
        phase_eq[0].set_color(C_PHASE)
        phase_eq[2].set_color(C_WEIGHT)
        phase_note = Text(
            "different pairs give different bound wavenumbers",
            font_size=22,
            color=C_MUTED,
        )
        phase_panel = VGroup(phase_head, phase_eq, phase_note).arrange(DOWN, buff=0.18)
        phase_panel.to_edge(RIGHT, buff=0.58).shift(UP * 0.95)
        phase_box = SurroundingRectangle(phase_panel, color=C_PHASE, buff=0.18, corner_radius=0.08).set_fill(BLACK, opacity=0.08)

        self.play(FadeOut(exact_eq), FadeOut(cost_exact))
        self.play(FadeIn(phase_box), quiet_fade(phase_panel), run_time=1.0)
        self.slide_pause(nav_progress, 3.0)

        vwa_head = Text("VWA keeps that variable phase", font_size=31, color=C_VWA)
        vwa_head.to_edge(RIGHT, buff=0.52).shift(UP * 2.12)
        phase_stays = VGroup(
            Text("kept", font_size=24, color=C_PHASE),
            MathTex(r"\cos(\theta_m+\theta_n),\quad k_m+k_n", font_size=29, color=C_PHASE),
        ).arrange(DOWN, buff=0.06)
        kernel_reduced = VGroup(
            Text("reuse a one-index amplitude kernel", font_size=22, color=C_VWA),
            MathTex(
                r"G(k_m,k_n)\quad\longrightarrow\quad G_2(k)",
                font_size=30,
                color=C_VWA,
            ),
        ).arrange(DOWN, buff=0.06)
        vwa_rule = VGroup(phase_stays, kernel_reduced).arrange(DOWN, buff=0.28).next_to(vwa_head, DOWN, buff=0.30)
        vwa_rule_box = SurroundingRectangle(vwa_rule, color=C_VWA, buff=0.18, corner_radius=0.08).set_fill(BLACK, opacity=0.08)

        self.play(
            FadeOut(row_line),
            FadeOut(col_line),
            FadeOut(sample_label),
            FadeOut(phase_panel),
            FadeOut(phase_box),
        )
        self.play(quiet_fade(vwa_head), FadeIn(vwa_rule_box), quiet_fade(vwa_rule), run_time=1.0)
        self.slide_pause(nav_progress, 4.0)
        self.play(FadeOut(vwa_rule), FadeOut(vwa_rule_box), run_time=0.6)

        diag_start = exact_grid[0].get_center()
        diag_end = exact_grid[(rows - 1) * cols + cols - 1].get_center()
        diag_line = Line(diag_start, diag_end, color=C_VWA, stroke_width=5)
        diag_label = Text("two diagonal kernel samples", font_size=22, color=C_VWA).next_to(exact_grid, DOWN, buff=0.36)
        diag_m = Dot(exact_grid[sample_row * cols + sample_row].get_center(), color=C_WEIGHT, radius=0.075)
        diag_n = Dot(exact_grid[sample_col * cols + sample_col].get_center(), color=C_WEIGHT, radius=0.075)
        pair_dot = Dot(sample_cell.get_center(), color=WHITE, radius=0.075)
        pair_ring = Circle(radius=0.16, color=WHITE, stroke_width=2).move_to(pair_dot)
        avg_overlay = Square(
            side_length=grid_w / cols,
            stroke_color=C_VWA,
            stroke_width=3.0,
            fill_opacity=0.0,
        ).move_to(sample_cell)

        avg_rule = VGroup(
            Text("VWA reuses a one-dimensional self kernel", font_size=22, color=C_MUTED),
            MathTex(r"G_2(k_n)=G(k_n,k_n)", font_size=31, color=C_WEIGHT),
            MathTex(r"G_2(k_m)=G(k_m,k_m)", font_size=31, color=C_WEIGHT),
            MathTex(
                r"G_2(k)={k(3-\tanh^2kh)\over4\tanh^3kh}",
                font_size=28,
                color=C_VWA,
            ),
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT).to_edge(RIGHT, buff=0.50).shift(UP * 0.12)
        avg_group = VGroup(avg_rule)
        avg_rule_box = SurroundingRectangle(avg_group, color=C_WEIGHT, buff=0.16, corner_radius=0.08).set_fill(BLACK, opacity=0.08)
        pair_est_label = Text("off-diagonal pair", font_size=19, color=WHITE).next_to(pair_ring, DOWN, buff=0.08)
        diag_n_arrow = Arrow(diag_n.get_right(), avg_rule[1].get_left(), buff=0.06, color=C_WEIGHT, stroke_width=2.0, max_tip_length_to_length_ratio=0.08)
        diag_m_arrow = Arrow(diag_m.get_right(), avg_rule[2].get_left(), buff=0.06, color=C_WEIGHT, stroke_width=2.0, max_tip_length_to_length_ratio=0.08)
        avg_arrow = Arrow(avg_rule[3].get_left(), pair_ring.get_right(), buff=0.06, color=C_VWA, stroke_width=2.4, max_tip_length_to_length_ratio=0.08)

        diag_head = Text("two-index to one-index", font_size=24, color=C_VWA).next_to(exact_grid, UP, buff=0.20)
        self.play(
            ReplacementTransform(exact_head, diag_head),
            FadeOut(exact_caption),
            FadeOut(exact_x),
            FadeOut(exact_y),
        )
        self.play(
            Create(diag_line),
            quiet_fade(diag_label),
            FadeIn(diag_m),
            FadeIn(diag_n),
            ReplacementTransform(sample_dot, pair_dot),
            Create(pair_ring),
            FadeIn(avg_rule_box),
            quiet_fade(avg_group),
            run_time=1.8,
        )
        self.play(Create(diag_m_arrow), Create(diag_n_arrow), run_time=0.9)
        self.play(FadeIn(avg_overlay), Create(avg_arrow), quiet_fade(pair_est_label), run_time=1.0)
        self.slide_pause(nav_progress, 4.45)

        self.play(
            *[FadeOut(mob) for mob in [
                exact_grid,
                exact_box,
                diag_head,
                diag_line,
                diag_label,
                diag_m,
                diag_n,
                pair_dot,
                pair_ring,
                avg_group,
                avg_rule_box,
                avg_overlay,
                diag_m_arrow,
                diag_n_arrow,
                avg_arrow,
                pair_est_label,
                vwa_head,
                title,
                subtitle,
            ]]
        )
        self.clear()
        self.add(nav_progress, nav)

        # Act 3b: show the analytic convolution in exponential form.
        play_product_average_bridge(self, nav=nav, nav_progress=nav_progress)

        # Act 4: show the FFT route used by the implementation.
        alg_title = Text("Why the VWA form is fast", font_size=35, weight=BOLD)
        alg_title.to_edge(UP, buff=0.22)
        self.play(quiet_fade(alg_title), run_time=0.7)

        spectrum = VGroup(
            MathTex(r"\widehat{\eta}(k)", font_size=42, color=C_LINEAR),
            Text("input spectrum", font_size=22, color=C_MUTED),
        ).arrange(DOWN, buff=0.08).next_to(alg_title, DOWN, buff=0.38)

        weighted_signal = VGroup(
            MathTex(r"\eta_{a,G}^{(11)}=\mathcal F^{-1}\!\left\{G_2(k)\widehat{\eta}(k)\right\}", font_size=33, color=C_WEIGHT),
            Text("weighted inverse FFT", font_size=23, color=C_MUTED),
        ).arrange(DOWN, buff=0.08)
        plain_signal = VGroup(
            MathTex(r"\eta_a^{(11)}=\mathcal F^{-1}\!\left\{\widehat{\eta}(k)\right\}", font_size=33, color=C_LINEAR),
            Text("ordinary inverse FFT", font_size=23, color=C_MUTED),
        ).arrange(DOWN, buff=0.08)
        signal_cards = VGroup(weighted_signal, plain_signal).arrange(DOWN, buff=0.25).next_to(spectrum, DOWN, buff=0.36)
        signal_box = SurroundingRectangle(signal_cards, color=C_PANEL, buff=0.20, corner_radius=0.08).set_fill(BLACK, opacity=0.08)
        self.play(quiet_fade(spectrum), run_time=0.6)
        self.play(FadeIn(signal_box), FadeIn(weighted_signal, shift=DOWN * 0.08), FadeIn(plain_signal, shift=DOWN * 0.08), run_time=1.2)

        product = MathTex(
            r"\eta_{\rm VWA}^{(22)}(x,t)",
            r"=",
            r"\Re\left\{\eta_{a,G}^{(11)}(x,t)\,\eta_a^{(11)}(x,t)\right\}",
            font_size=34,
            color=C_VWA,
        ).next_to(signal_cards, DOWN, buff=0.48)
        product.scale_to_fit_width(9.4)
        product[0].set_color(WHITE)
        self.play(quiet_fade(product))
        self.slide_pause(nav_progress, 4.45)

        def labeled_arrow(line1, line2):
            arrow = Arrow(LEFT, RIGHT, buff=0.12, color=C_MUTED, stroke_width=3)
            text = VGroup(
                Text(line1, font_size=15, color=C_MUTED),
                Text(line2, font_size=15, color=C_MUTED),
            ).arrange(DOWN, buff=0.00)
            text.next_to(arrow, UP, buff=0.06)
            return VGroup(arrow, text)

        cost_panel = VGroup(
            VGroup(
                Text("spectrum", font_size=23, color=C_LINEAR),
                MathTex(r"\widehat{\eta}(k)", font_size=34, color=C_LINEAR),
                Text("stored in wavenumber", font_size=18, color=C_MUTED),
            ).arrange(DOWN, buff=0.06),
            labeled_arrow("weight", "and copy"),
            VGroup(
                Text("two inverse FFTs", font_size=23, color=C_VWA),
                MathTex(r"\eta_{a,G}^{(11)},\ \eta_a^{(11)}", font_size=27, color=C_VWA),
                Text("linear cost per transform", font_size=18, color=C_MUTED),
            ).arrange(DOWN, buff=0.06),
            labeled_arrow("multiply", "in physical space"),
            VGroup(
                Text("VWA field", font_size=23, color=C_WEIGHT),
                MathTex(r"\mathcal O(N_c\log N_c)", font_size=31, color=C_WEIGHT),
                Text("FFT dominated", font_size=18, color=C_MUTED),
            ).arrange(DOWN, buff=0.06),
        ).arrange(RIGHT, buff=0.34).to_edge(DOWN, buff=0.86)
        cost_panel.scale_to_fit_width(11.3)
        cost_box = SurroundingRectangle(cost_panel, color=C_PANEL, buff=0.15, corner_radius=0.08).set_fill(BLACK, opacity=0.08)
        self.play(FadeIn(cost_box), LaggedStart(*[FadeIn(mob) for mob in cost_panel], lag_ratio=0.18))
        self.slide_pause(nav_progress, 4.80)

        self.play(*[FadeOut(mob) for mob in keep_nav(list(self.mobjects), nav)])
        self.clear()
        self.add(nav_progress, nav)

        compare_title = Text("Second order grows with spectral components", font_size=33, weight=BOLD)
        compare_title.to_edge(UP, buff=0.25)

        def pair_term(i, j):
            if i == j:
                return rf"a_{i}^{2}G_{{{i}{i}}}\cos(2\theta_{i})"
            return rf"a_{i}a_{j}G_{{{i}{j}}}\cos(\theta_{i}+\theta_{j})"

        def pair_line(pairs, font_size=24):
            tex = "+".join(pair_term(i, j) for i, j in pairs)
            return MathTex(tex, font_size=font_size, color=WHITE)

        def columns_for_component_count(count):
            pairs = [(i, j) for i in range(1, count + 1) for j in range(i, count + 1)]
            if count <= 3:
                col_count = 1
            elif count <= 5:
                col_count = 2
            else:
                col_count = 5
            columns = [[] for _ in range(col_count)]
            for index, pair in enumerate(pairs):
                columns[index % col_count].append([pair])
            return columns

        def term_block(count):
            total = count * (count + 1) // 2
            label = f"{count} components: {total} unique interactions"
            columns = columns_for_component_count(count)
            col_groups = []
            for lines in columns:
                col_groups.append(
                    VGroup(*[pair_line(line) for line in lines]).arrange(DOWN, buff=0.055, aligned_edge=LEFT)
                )
            line_group = VGroup(*col_groups).arrange(RIGHT, buff=0.38, aligned_edge=UP)
            block = VGroup(
                Text(label, font_size=23, color=C_MUTED),
                line_group,
            ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            if block.width > 11.35:
                block.scale_to_fit_width(11.35)
            if block.height > 3.38:
                block.scale_to_fit_height(3.38)
            return block

        component_blocks = [term_block(count) for count in range(2, 11)]

        term_slot = Rectangle(width=11.55, height=3.52, stroke_width=0, fill_opacity=0)
        exact_col = VGroup(
            Text("exact second-order formula", font_size=23, color=C_EXACT),
            term_slot,
            VGroup(
                MathTex(r"{N_c(N_c+1)\over2}\ \mathrm{unique\ interactions}", font_size=25, color=C_EXACT),
                MathTex(r"\mathcal O(N_c^2)", font_size=34, color=C_EXACT),
            ).arrange(RIGHT, buff=0.85),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        exact_col.next_to(compare_title, DOWN, buff=0.22)

        vwa_col = VGroup(
            Text("VWA: same variable phase, compact product", font_size=24, color=C_VWA),
            MathTex(
                r"\eta_{\rm VWA}^{(22)}",
                r"=",
                r"\Re\{\eta_{a,G}^{(11)}\eta_a^{(11)}\}",
                font_size=28,
                color=C_VWA,
            ),
            MathTex(r"\mathcal O(N_c\log N_c)", font_size=34, color=C_WEIGHT),
        ).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.98)
        vwa_col.scale_to_fit_width(10.9)

        exact_panel = SurroundingRectangle(exact_col, color=C_EXACT, buff=0.22, corner_radius=0.08).set_fill(BLACK, opacity=0.10)
        vwa_panel = SurroundingRectangle(vwa_col, color=C_VWA, buff=0.22, corner_radius=0.08).set_fill(BLACK, opacity=0.10)
        block_anchor = term_slot.get_top()
        for block in component_blocks:
            block.move_to(block_anchor, aligned_edge=UP)

        self.play(quiet_fade(compare_title), run_time=0.7)
        self.play(FadeIn(exact_panel), quiet_fade(exact_col[0]))
        self.play(quiet_fade(component_blocks[0]), run_time=0.8)
        for previous, current in zip(component_blocks, component_blocks[1:]):
            self.play(ReplacementTransform(previous, current), run_time=1.25)
            self.wait(0.45)
        self.play(quiet_fade(exact_col[-1]))
        self.play(FadeIn(vwa_panel), quiet_fade(vwa_col))
        self.slide_pause(nav_progress, 5.75)

        self.play(*[FadeOut(mob) for mob in keep_nav(list(self.mobjects), nav)])
        self.clear()
        self.add(nav_progress, nav)

        # Act 5: after the VWA route and cost growth are clear, show result checks.
        amplitude_question = make_amplitude_approximation_question_slide()
        self.play(FadeIn(amplitude_question, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 6.05)
        self.play(FadeOut(amplitude_question), run_time=0.55)
        self.clear()
        self.add(nav_progress, nav)

        split_kernel = make_split_kernel_comparison_slide()
        self.play(FadeIn(split_kernel, shift=DOWN * 0.05), run_time=0.9)
        self.slide_pause(nav_progress, 6.25)
        self.play(FadeOut(split_kernel), run_time=0.6)
        self.clear()
        self.add(nav_progress, nav)

        waveform_space = make_waveform_comparison_space_slide(0)
        self.play(FadeIn(waveform_space, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 7.0)
        self.play(FadeOut(waveform_space), run_time=0.55)
        self.clear()
        self.add(nav_progress, nav)

        waveform_space = make_waveform_comparison_space_slide(1)
        self.play(FadeIn(waveform_space, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 7.18)
        self.play(FadeOut(waveform_space), run_time=0.55)
        self.clear()
        self.add(nav_progress, nav)

        q_metric = make_q_metric_slide()
        self.play(FadeIn(q_metric, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 7.45)
        self.play(FadeOut(q_metric), run_time=0.55)
        self.clear()
        self.add(nav_progress, nav)

        q_sweep = make_q_sweep_slide()
        self.play(FadeIn(q_sweep, shift=DOWN * 0.05), run_time=0.8)
        self.slide_pause(nav_progress, 7.78)
