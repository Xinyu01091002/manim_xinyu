"""
Scenario 1 — Bound Harmonics in a Wave Group  (v5)
===================================================
Changes from v4:
  - A reduced 0.35 → 0.20 (ε ≈ 0.30, more physically realistic)
  - Equations labelled "(lab frame)" to avoid confusion with group-frame animation
  - Time-evolution note rewritten in MathTex with explicit group-frame phase
  - eq1–eq4 fade out before eq_tot is revealed (cleaner 承→合 transition)
  - 合 (Resolution) takeaway text added at the end — the key message
  - Time evolution extended to t=15 (run_time=12) for multiple visible oscillations
  - self.wait() durations increased throughout for better pacing
  - Legend shifted inward to avoid axis-edge overlap
"""

from manim import *
import numpy as np

g = 9.81

# ── Physical parameters ────────────────────────────────────────────────────────
K0      = 1.5           # carrier wavenumber  [rad/m]
A       = 0.20          # amplitude           [m]   → ε = A·K0 ≈ 0.30
SIGMA_X = 4.0           # group width (1σ)    [m]
OMEGA0  = np.sqrt(g * K0)
CG      = OMEGA0 / (2.0 * K0)
EPS     = A * K0        # steepness ≈ 0.30

# Colours
C1  = BLUE
C2P = ORANGE
C2M = GREEN
C3P = PURPLE

# ── Spectral display (shifted log scale: y_display = log10(amp) − LOG_FLOOR) ──
SK        = 0.18
LOG_FLOOR = -2.0           # minimum log10 amplitude shown
Y_SPEC    = -LOG_FLOOR + 0.25   # = 2.25, y_range top of spectrum axes
GAMMA_JS  = 3.3            # JONSWAP peak-enhancement factor

def _jonswap_raw(k, k_p):
    """JONSWAP spectral density in k-space (deep water, unnormalised)."""
    if k <= 1e-6:
        return 0.0
    omega   = np.sqrt(g * k)
    omega_p = np.sqrt(g * k_p)
    sigma   = 0.07 if omega <= omega_p else 0.09
    base    = omega ** (-5) * np.exp(-1.25 * (omega_p / omega) ** 4)
    peak    = GAMMA_JS ** np.exp(-0.5 * ((omega - omega_p) / (sigma * omega_p)) ** 2)
    dw_dk   = np.sqrt(g / k) / 2.0   # |dω/dk| for ω = √(gk)
    return float(base * peak * dw_dk)

# Pre-compute per-peak JONSWAP normalisations (peak raw → 1)
_JS_NORM_1 = max(_jonswap_raw(k, K0)   for k in np.linspace(0.3*K0,   3.0*K0,   1000))
_JS_NORM_2 = max(_jonswap_raw(k, 2*K0) for k in np.linspace(0.6*K0,   6.0*K0,   1000))
_JS_NORM_3 = max(_jonswap_raw(k, 3*K0) for k in np.linspace(0.9*K0,   9.0*K0,   1000))

def _lspec_js(raw):
    return max(np.log10(max(float(raw), 10 ** LOG_FLOOR)) - LOG_FLOOR, 0.0)

def lspec_js(k):
    """Primary JONSWAP peak at k₀ — peak displays at y = 2.0."""
    return _lspec_js(_jonswap_raw(k, K0) / _JS_NORM_1)

def lspec_js2p(k):
    """2nd-order super-harmonic: JONSWAP centred at 2k₀, amplitude ~ ε."""
    return _lspec_js(_jonswap_raw(k, 2*K0) / _JS_NORM_2 * EPS)

def lspec_js3p(k):
    """3rd-order super-harmonic: JONSWAP centred at 3k₀, amplitude ~ ε²."""
    return _lspec_js(_jonswap_raw(k, 3*K0) / _JS_NORM_3 * EPS**2)

def lspec_setdown(k):
    """Set-down: broad-banded hump near k ≈ 0, amplitude ~ ε."""
    raw = EPS * 0.8 * np.exp(-k**2 / (2.0 * 0.55**2))
    return _lspec_js(raw)


# ── Group-frame wave functions (envelope ALWAYS centred at x = 0) ─────────────
# In the group frame the carrier phase is θ_g = k₀x − (ω₀/2)t  (Doppler shift).
def genv(x):
    return np.exp(-x ** 2 / (2.0 * SIGMA_X ** 2))

def geta1(x, t=0):
    return A * genv(x) * np.cos(K0 * x - OMEGA0 * t / 2)

def geta2p(x, t=0):
    """2nd-order super-harmonic  η₂⁺ = (k₀/2)·A²·cos(2θ_g)"""
    return (K0 / 2) * A ** 2 * genv(x) ** 2 * np.cos(2 * (K0 * x - OMEGA0 * t / 2))

def geta2m(x):
    """2nd-order set-down  η₂⁻ = −(k₀/2)·A²  [time-independent in group frame]"""
    return -(K0 / 2) * A ** 2 * genv(x) ** 2

def geta3p(x, t=0):
    """3rd-order super-harmonic  η₃⁺ = (3k₀²/8)·A³·cos(3θ_g)"""
    return (3 * K0 ** 2 / 8) * A ** 3 * genv(x) ** 3 * np.cos(3 * (K0 * x - OMEGA0 * t / 2))

def geta_tot(x, t=0):
    return geta1(x, t) + geta2p(x, t) + geta2m(x) + geta3p(x, t)


# ══════════════════════════════════════════════════════════════════════════════
class BoundHarmonicsIntro(Scene):
    def construct(self):

        # ── Title ──────────────────────────────────────────────────────────────
        title = Text("Bound Harmonics in a Wave Group", font_size=26, weight=BOLD)
        title.to_edge(UP, buff=0.18)
        self.play(Write(title))

        # ══ Spatial axes (left, top half) ═════════════════════════════════════
        ax_s = Axes(
            x_range=[-10, 10, 5],
            y_range=[-0.50, 0.50, 0.25],
            x_length=5.8,
            y_length=2.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [-5, 0, 5]},
            y_axis_config={"numbers_to_include": [-0.25, 0.0, 0.25]},
        ).to_edge(LEFT, buff=0.85).shift(UP * 1.2)

        head_s = Text("Spatial  (group frame)", font_size=15, color=GREY_B).next_to(ax_s, UP, buff=0.30)
        lab_xs = ax_s.get_x_axis_label(MathTex("x\\ (\\mathrm{m})", font_size=17))
        lab_ys = ax_s.get_y_axis_label(MathTex("\\eta\\ (\\mathrm{m})", font_size=17))

        # ══ Spectrum axes (right, top half) — x-axis at BOTTOM ════════════════
        ax_k = Axes(
            x_range=[0.0, 5.5, K0],
            y_range=[0.0, Y_SPEC, 1.0],        # y=0 is the bottom → k-axis at bottom
            x_length=5.5,
            y_length=2.5,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},   # custom labels added below
            y_axis_config={"include_numbers": False},   # custom log labels added below
        ).to_edge(RIGHT, buff=0.65).shift(UP * 1.2)

        head_k = Text("Wavenumber spectrum  (log scale)", font_size=15, color=GREY_B).next_to(ax_k, UP, buff=0.08)
        lab_xk = ax_k.get_x_axis_label(MathTex("k\\ (\\mathrm{rad\\,m^{-1}})", font_size=17))
        lab_yk = ax_k.get_y_axis_label(MathTex("\\log_{10}|\\hat{\\eta}|", font_size=17))

        # Log y-axis tick marks + labels  (10^{-2}, 10^{-1}, 10^{0})
        log_y_labels = VGroup()
        for y_d, exp in [(0, -2), (1, -1), (2, 0)]:
            pt = ax_k.c2p(0.0, y_d)
            log_y_labels.add(
                Line(pt + LEFT * 0.10, pt, stroke_width=1.5),
                MathTex(f"10^{{{exp}}}", font_size=14).next_to(pt + LEFT * 0.10, LEFT, buff=0.05),
            )

        # k x-axis labels — written progressively, stored separately
        lbl_k0   = MathTex("k_0",         font_size=18, color=C1 ).next_to(ax_k.c2p(K0,    0), DOWN, buff=0.14)
        lbl_2k0  = MathTex("2k_0",        font_size=18, color=C2P).next_to(ax_k.c2p(2*K0,  0), DOWN, buff=0.14)
        lbl_setd = MathTex("k{\\approx}0", font_size=16, color=C2M).next_to(ax_k.c2p(0.20,  0), DOWN + RIGHT * 0.3, buff=0.13)
        lbl_3k0  = MathTex("3k_0",        font_size=18, color=C3P).next_to(ax_k.c2p(3*K0,  0), DOWN, buff=0.14)

        # ── Draw axes ──────────────────────────────────────────────────────────
        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_s), Write(lab_xs), Write(lab_ys), Write(head_s)),
                AnimationGroup(Create(ax_k), Write(lab_xk), Write(lab_yk),
                               Write(log_y_labels), Write(head_k)),
                lag_ratio=0.35,
            )
        )
        self.wait(1.0)   # let audience orient to the two-panel layout

        # ══ Equation area (bottom half) ════════════════════════════════════════
        # Label clarifying equations are written in lab-frame form
        eq_frame_note = Text("equations in lab frame  (t = 0 shown above)",
                             font_size=12, color=GREY_C)

        EQ_TOP = -0.70
        EQ_GAP =  0.55

        eq1 = MathTex(
            r"\eta_1 = A(x)\cos(k_0 x - \omega_0 t)",
            font_size=22, color=C1,
        ).move_to([0, EQ_TOP, 0])

        eq2 = MathTex(
            r"\eta_2^+ = \tfrac{k_0}{2}A^2\cos\!\bigl(2(k_0 x - \omega_0 t)\bigr)",
            font_size=22, color=C2P,
        ).move_to([0, EQ_TOP - EQ_GAP, 0])

        eq3 = MathTex(
            r"\eta_2^- = -\tfrac{k_0}{2}A^2",
            font_size=22, color=C2M,
        ).move_to([0, EQ_TOP - 2 * EQ_GAP, 0])

        eq4 = MathTex(
            r"\eta_3^+ = \tfrac{3k_0^2}{8}A^3\cos\!\bigl(3(k_0 x - \omega_0 t)\bigr)",
            font_size=22, color=C3P,
        ).move_to([0, EQ_TOP - 3 * EQ_GAP, 0])

        eq_frame_note.next_to(eq1, UP, buff=0.18)

        divider = Line(LEFT * 5.0, RIGHT * 5.0, stroke_width=1, color=GREY_D)
        divider.move_to([0, EQ_TOP - 3.55 * EQ_GAP, 0])

        eq_tot = VGroup(
            MathTex(r"\eta\ =",   font_size=24),
            MathTex(r"\eta_1",    font_size=24, color=C1),
            MathTex(r"+",         font_size=24),
            MathTex(r"\eta_2^+",  font_size=24, color=C2P),
            MathTex(r"+",         font_size=24),
            MathTex(r"\eta_2^-",  font_size=24, color=C2M),
            MathTex(r"+",         font_size=24),
            MathTex(r"\eta_3^+",  font_size=24, color=C3P),
        ).arrange(RIGHT, buff=0.14).move_to([-2.8, EQ_TOP - 3.85 * EQ_GAP, 0])

        eq_nl = MathTex(
            r"\eta_{\rm nl} = \eta_1 + \eta_2^+ + \eta_2^- + \eta_3^+",
            font_size=24, color=YELLOW,
        ).next_to(eq_tot, RIGHT, buff=0.45)

        # ══ ① Linear wave group ═══════════════════════════════════════════════
        c1   = ax_s.plot(lambda x: geta1(x, 0),  x_range=[-10, 10, 0.04], color=C1,    stroke_width=2.5)
        envu = ax_s.plot(lambda x:  A * genv(x), x_range=[-10, 10, 0.10], color=BLUE_A, stroke_width=1.0, stroke_opacity=0.45)
        envl = ax_s.plot(lambda x: -A * genv(x), x_range=[-10, 10, 0.10], color=BLUE_A, stroke_width=1.0, stroke_opacity=0.45)
        pk1  = ax_k.plot(lspec_js, x_range=[0.05, 5.5, 0.02], color=C1, stroke_width=2.5)

        self.play(Create(c1), Create(envu), Create(envl))
        self.play(Create(pk1), Write(lbl_k0))
        self.play(Write(eq_frame_note), Write(eq1))
        self.wait(2.0)   # let audience read the equation and match it to the wave

        # ══ ② 2nd-order super-harmonic ════════════════════════════════════════
        c2p  = ax_s.plot(lambda x: geta2p(x, 0), x_range=[-10, 10, 0.04], color=C2P,  stroke_width=2.0)
        pk2p = ax_k.plot(lspec_js2p, x_range=[0.05, 5.5, 0.02], color=C2P, stroke_width=2.5)

        self.play(Create(c2p), Create(pk2p), Write(lbl_2k0))
        self.play(Write(eq2))
        self.wait(2.0)   # note the new spectral peak at 2k₀

        # ══ ③ 2nd-order set-down ══════════════════════════════════════════════
        c2m  = ax_s.plot(lambda x: geta2m(x),    x_range=[-10, 10, 0.04], color=C2M,  stroke_width=2.0)
        pk2m = ax_k.plot(lspec_setdown, x_range=[0.01, 3.0, 0.02], color=C2M, stroke_width=2.5)

        self.play(Create(c2m), Create(pk2m), Write(lbl_setd))
        self.play(Write(eq3))
        self.wait(2.0)   # negative depression under the group is visible

        # ══ ④ 3rd-order super-harmonic ════════════════════════════════════════
        c3p  = ax_s.plot(lambda x: geta3p(x, 0), x_range=[-10, 10, 0.04], color=C3P,  stroke_width=1.8)
        pk3p = ax_k.plot(lspec_js3p, x_range=[0.05, 5.5, 0.02], color=C3P, stroke_width=2.5)

        self.play(Create(c3p), Create(pk3p), Write(lbl_3k0))
        self.play(Write(eq4))
        self.wait(2.0)   # small 3rd-order peak visible in spectrum

        # ══ ⑤ Show total wave ═════════════════════════════════════════════════
        c_tot = ax_s.plot(lambda x: geta_tot(x, 0), x_range=[-10, 10, 0.04], color=WHITE, stroke_width=2.8)

        # Fade individual component curves and equations; reveal total
        self.play(
            FadeOut(c1), FadeOut(envu), FadeOut(envl),
            FadeOut(c2p), FadeOut(c2m), FadeOut(c3p),
        )
        self.play(Create(c_tot))
        self.wait(1.0)   # show crests sharper, troughs flatter before the sum equation
        self.play(Create(divider), Write(eq_tot), Write(eq_nl))
        self.wait(2.5)   # let audience appreciate the full superposition

        # ══ ⑥ Time evolution in group frame ═══════════════════════════════════
        # Note: in the group frame the carrier Doppler-shifts to k₀x − (ω₀/2)t,
        # so the envelope stays fixed while the carrier oscillates beneath it.
        note = MathTex(
            r"\text{Group frame: envelope fixed,}\quad"
            r"\theta_g = k_0 x - \tfrac{\omega_0}{2}t",
            font_size=16, color=YELLOW,
        ).next_to(eq_tot, DOWN, buff=0.22)
        self.play(Write(note))
        self.wait(1.0)

        t_val = ValueTracker(0.0)

        # Static elements — time-independent in group frame
        s_envu = ax_s.plot(lambda x:  A * genv(x), x_range=[-10, 10, 0.08], color=BLUE_A, stroke_width=1.0, stroke_opacity=0.45)
        s_envl = ax_s.plot(lambda x: -A * genv(x), x_range=[-10, 10, 0.08], color=BLUE_A, stroke_width=1.0, stroke_opacity=0.45)
        s_sd   = ax_s.plot(lambda x: geta2m(x),     x_range=[-10, 10, 0.06], color=C2M,   stroke_width=1.6)

        # Dynamic: linear-only wave for comparison (dashed blue)
        live_eta1 = always_redraw(lambda: DashedVMobject(
            ax_s.plot(
                lambda x: geta1(x, t_val.get_value()),
                x_range=[-10, 10, 0.05], color=C1, stroke_width=2.8,
            ),
            num_dashes=35, dashed_ratio=0.5,
        ))

        # Dynamic: total nonlinear wave
        live_tot = always_redraw(lambda: ax_s.plot(
            lambda x: geta_tot(x, t_val.get_value()),
            x_range=[-10, 10, 0.05], color=WHITE, stroke_width=2.8,
        ))

        # Legend — placed inside ax_s, upper-right (shifted inward from edge)
        legend = VGroup(
            VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=WHITE, stroke_width=2.8),
                   Text("nonlinear", font_size=11, color=WHITE)).arrange(RIGHT, buff=0.06),
            VGroup(DashedVMobject(Line(LEFT * 0.22, RIGHT * 0.22, color=C1, stroke_width=2.8),
                                  num_dashes=5, dashed_ratio=0.5),
                   Text("linear  η₁", font_size=11, color=C1)).arrange(RIGHT, buff=0.06),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        legend.move_to(ax_s.c2p(5.5, 0.37))   # shifted inward from 6.8 to 5.5

        self.remove(c_tot)
        self.add(s_envu, s_envl, s_sd, live_eta1, live_tot)
        self.play(FadeIn(legend))
        self.wait(0.5)
        # Run ~2.5 carrier periods so the audience can see the locked co-travel clearly
        self.play(t_val.animate.set_value(15.0), run_time=12, rate_func=linear)
        self.wait(1.0)

        # ══ ⑦ 合 — Resolution: highlight sum and deliver takeaway ══════════════
        box = SurroundingRectangle(VGroup(eq_tot, eq_nl), color=YELLOW, buff=0.10, corner_radius=0.07)
        self.play(Create(box))
        self.wait(1.0)

        takeaway = VGroup(
            Text("Bound harmonics  ≠  free waves", font_size=19, color=YELLOW, weight=BOLD),
            Text("They do not satisfy the dispersion relation independently —", font_size=16, color=GREY_A),
            Text("they are slaved to the primary wave group.", font_size=16, color=GREY_A),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        takeaway.to_corner(DR, buff=0.45)
        self.play(Write(takeaway))
        self.wait(4.0)   # hold on the key message
