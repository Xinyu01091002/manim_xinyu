"""
Scenario 0 — Why Do Nonlinear Waves Matter?  (v5)
==================================================
Changes from v4:
  - Probe marker on spatial axes: vertical dashed line + label at x = X_FIXED,
    shown from the moment the axes appear
  - Spatial wave group animates in sync with the growing time series (both
    driven by the same ValueTracker t_grow)
  - Moving probe dots (blue = linear, yellow = nonlinear) ride the wave surface
    at the measurement point, visually connecting spatial panel to time series
  - Dynamic spatial header updates to show current time "t = X.X s"
  - phase_note repositioned into the gap between upper panels and time series
    to eliminate overlap with head_t
  - 合 takeaway replaces the spectrum panel (FadeOut ax_k, Write takeaway in
    that area) so it never overlaps the time series axes
"""

from manim import *
import numpy as np

g = 9.81

# ── Physical parameters ───────────────────────────────────────────────────────
K0       = 1.5
A        = 0.345         # tuned so crest enhancement is ~10%
SIGMA_X  = 4.0
OMEGA0   = np.sqrt(g * K0)          # ≈ 3.836 rad/s
CG       = OMEGA0 / (2.0 * K0)     # ≈ 1.279 m/s
EPS      = A * K0                   # ≈ 0.52
PHASE_DRIFT_SCALE = 0.28            # keep timing drift visible but realistic
OMEGA_NL = OMEGA0 * (1.0 + PHASE_DRIFT_SCALE * EPS**2 / 2.0)

X_FIXED  = 11.0  # measurement / probe location [m]
T_END    = 18.0  # time series length [s]

# Colours
C_LIN = BLUE
C_NL  = YELLOW
C2P   = ORANGE
C2M   = GREEN
C3P   = PURPLE
LOG_FLOOR = -2.0
Y_SPEC    = 2.25
GAMMA_JS  = 3.3

def _tex_escape(text):
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def T(text, **kwargs):
    weight = kwargs.pop("weight", NORMAL)
    body = _tex_escape(text)
    if weight == BOLD:
        body = rf"\textbf{{{body}}}"
    else:
        body = rf"\text{{{body}}}"
    return Tex(body, **kwargs)

# ── Wave functions — Eulerian (lab) frame ─────────────────────────────────────
def _env(xg):
    return np.exp(-xg**2 / (2.0 * SIGMA_X**2))

def eta_lin(x, t):
    """Linear: envelope moves at c_g, carrier at ω₀."""
    return A * _env(x - CG * t) * np.cos(K0 * x - OMEGA0 * t)

def eta_nl(x, t):
    """Stokes: same envelope velocity, carrier phase at ω_NL = ω₀(1 + ε²/2)."""
    xg  = x - CG * t
    env = _env(xg)
    ph  = K0 * x - OMEGA_NL * t
    e1  = A            * env    * np.cos(ph)
    e2p = (K0/2)*A**2  * env**2 * np.cos(2*ph)
    e2m = -(K0/2)*A**2 * env**2
    e3p = (3*K0**2/8)*A**3 * env**3 * np.cos(3*ph)
    return e1 + e2p + e2m + e3p

# ── Spectral helpers ──────────────────────────────────────────────────────────
def _jonswap_raw(k, k_p):
    if k <= 1e-6:
        return 0.0
    omega, omega_p = np.sqrt(g*k), np.sqrt(g*k_p)
    sigma = 0.07 if omega <= omega_p else 0.09
    base  = omega**(-5) * np.exp(-1.25*(omega_p/omega)**4)
    peak  = GAMMA_JS**np.exp(-0.5*((omega-omega_p)/(sigma*omega_p))**2)
    return float(base * peak * np.sqrt(g/k)/2.0)

_JS1 = max(_jonswap_raw(k, K0)   for k in np.linspace(0.3*K0, 3.0*K0, 1000))
_JS2 = max(_jonswap_raw(k, 2*K0) for k in np.linspace(0.6*K0, 6.0*K0, 1000))
_JS3 = max(_jonswap_raw(k, 3*K0) for k in np.linspace(0.9*K0, 9.0*K0, 1000))

def _ls(raw):
    return max(np.log10(max(float(raw), 10**LOG_FLOOR)) - LOG_FLOOR, 0.0)

def spec_lin(k):  return _ls(_jonswap_raw(k, K0)   / _JS1)
def spec_2p(k):   return _ls(_jonswap_raw(k, 2*K0) / _JS2 * EPS)
def spec_3p(k):   return _ls(_jonswap_raw(k, 3*K0) / _JS3 * EPS**2)
def spec_sd(k):   return _ls(EPS * 0.8 * np.exp(-k**2 / (2.0*0.55**2)))


# ══════════════════════════════════════════════════════════════════════════════
class WhyNonlinearWaves(Scene):
    def construct(self):

        # ── Title ──────────────────────────────────────────────────────────────
        title = T("Why Do Nonlinear Waves Matter?", font_size=34, weight=BOLD)
        title.to_edge(UP, buff=0.18)
        self.play(Write(title))

        # ══ Spatial axes (upper-left) ═════════════════════════════════════════
        ax_s = Axes(
            x_range=[-14, 14, 7],
            y_range=[-0.45, 0.45, 0.20],
            x_length=6.8,
            y_length=2.4,
            axis_config={"include_tip": False},
            x_axis_config={
                "numbers_to_include": [-10, 0, 10],
                "font_size": 26,
            },
            y_axis_config={
                "numbers_to_include": [-0.20, 0.0, 0.20],
                "font_size": 24,
            },
        ).to_edge(LEFT, buff=0.5).shift(UP * 1.05)

        head_s = T("Spatial snapshot  (t = 0 s)", font_size=20, color=GREY_B)\
            .next_to(ax_s, UP, buff=0.22)
        lab_xs = ax_s.get_x_axis_label(MathTex("x\\ (\\mathrm{m})", font_size=26))
        lab_ys = ax_s.get_y_axis_label(MathTex("\\eta\\ (\\mathrm{m})", font_size=26))

        # ── Probe marker — shown from the moment axes appear ──────────────────
        # Vertical dashed line spans the full y range of ax_s at x = X_FIXED
        probe_vline = DashedLine(
            ax_s.c2p(X_FIXED, -0.44), ax_s.c2p(X_FIXED, 0.44),
            stroke_width=1.5, color=GREY_C, dash_length=0.08,
        )
        # Label sits below the bottom tick of the probe line
        probe_lbl_s = VGroup(
            T("probe", font_size=15, color=GREY_C),
            MathTex(rf"x={X_FIXED:.0f}\,\mathrm{{m}}", font_size=15, color=GREY_C),
        ).arrange(DOWN, buff=0.04)\
         .next_to(ax_s.c2p(X_FIXED, -0.44), DOWN, buff=0.10)

        # ══ Spectrum axes (upper-right) ═══════════════════════════════════════
        ax_k = Axes(
            x_range=[0.0, 5.5, K0],
            y_range=[0.0, Y_SPEC, 1.0],
            x_length=4.2,
            y_length=2.4,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.5).shift(UP * 1.05)

        head_k = T("Wavenumber spectrum  (log)", font_size=20, color=GREY_B)\
            .next_to(ax_k, UP, buff=0.22)
        lab_xk = ax_k.get_x_axis_label(MathTex("k", font_size=26))
        lab_yk = ax_k.get_y_axis_label(MathTex("\\log|\\hat{\\eta}|", font_size=26))

        lbl_k0  = MathTex("k_0",  font_size=26, color=C_LIN)\
            .next_to(ax_k.c2p(K0,   0), DOWN, buff=0.12)
        lbl_2k0 = MathTex("2k_0", font_size=26, color=C2P)\
            .next_to(ax_k.c2p(2*K0, 0), DOWN, buff=0.12)
        lbl_3k0 = MathTex("3k_0", font_size=26, color=C3P)\
            .next_to(ax_k.c2p(3*K0, 0), DOWN, buff=0.12)
        lbl_sd  = MathTex("k{\\approx}0", font_size=22, color=C2M)\
            .next_to(ax_k.c2p(0.2, 0), DOWN + RIGHT*0.3, buff=0.12)

        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_s), Write(lab_xs), Write(lab_ys), Write(head_s)),
                AnimationGroup(Create(ax_k), Write(lab_xk), Write(lab_yk), Write(head_k)),
                lag_ratio=0.3,
            )
        )
        # Probe appears with the axes — establishes where the gauge is before
        # any wave is drawn
        self.play(Create(probe_vline), Write(probe_lbl_s))
        self.wait(0.8)

        # ══ ① Linear wave (t = 0) ═════════════════════════════════════════════
        lin0 = ax_s.plot(lambda x: eta_lin(x, 0),
                         x_range=[-14, 14, 0.05], color=C_LIN, stroke_width=2.5)
        env_u = ax_s.plot(lambda x:  A*_env(x), x_range=[-14, 14, 0.15],
                          color=BLUE_A, stroke_width=1.0, stroke_opacity=0.5)
        env_l = ax_s.plot(lambda x: -A*_env(x), x_range=[-14, 14, 0.15],
                          color=BLUE_A, stroke_width=1.0, stroke_opacity=0.5)
        spec_lin_c = ax_k.plot(spec_lin, x_range=[0.05, 5.5, 0.02],
                               color=C_LIN, stroke_width=2.5)

        lin_eq = MathTex(r"\eta_{\rm lin} = A(x)\cos(k_0 x - \omega_0 t)",
                         font_size=28, color=C_LIN).move_to([0, -0.96, 0])

        self.play(Create(lin0), Create(env_u), Create(env_l))
        self.play(Create(spec_lin_c), Write(lbl_k0))
        self.play(Write(lin_eq))
        self.wait(2.6)

        # ══ ② Overlay Stokes wave (t = 0) ════════════════════════════════════
        nl0 = ax_s.plot(lambda x: eta_nl(x, 0),
                        x_range=[-10, 10, 0.05], color=C_NL, stroke_width=2.5)

        nl_eq = MathTex(
            r"\eta_{\rm nl}:\ \omega_{\rm NL}>\omega_0\ \mathrm{(slightly)}",
            font_size=28, color=C_NL,
        ).move_to([0, -1.46, 0])

        self.play(Create(nl0))
        self.play(Write(nl_eq))
        self.wait(2.2)

        # ══ ③ Crest-height annotation ═════════════════════════════════════════
        xs   = np.linspace(-2.5, 2.5, 600)
        x_cl = xs[np.argmax([eta_lin(x, 0) for x in xs])]
        x_cn = xs[np.argmax([eta_nl(x, 0)  for x in xs])]
        h_lin = eta_lin(x_cl, 0)
        h_nl  = eta_nl(x_cn, 0)

        ref_line = DashedLine(
            ax_s.c2p(-4.0, h_lin), ax_s.c2p(4.0, h_lin),
            stroke_width=1.2, color=C_LIN, dash_length=0.10,
        )
        arr = DoubleArrow(
            ax_s.c2p(x_cn, h_lin), ax_s.c2p(x_cn, h_nl),
            buff=0, stroke_width=2.0, color=C_NL, tip_length=0.12,
        )
        pct = (h_nl - h_lin) / h_lin * 100
        pct_lbl = T(f"+{pct:.0f}%", font_size=28, color=C_NL)\
            .next_to(arr, RIGHT, buff=0.08)

        self.play(Create(ref_line))
        self.play(GrowArrow(arr), Write(pct_lbl))
        self.wait(3.2)

        # ══ ④ Spectral fingerprint ════════════════════════════════════════════
        spec_2p_c = ax_k.plot(spec_2p, x_range=[0.05, 5.5, 0.02],
                               color=C2P, stroke_width=2.5)
        spec_3p_c = ax_k.plot(spec_3p, x_range=[0.05, 5.5, 0.02],
                               color=C3P, stroke_width=2.5)
        spec_sd_c = ax_k.plot(spec_sd, x_range=[0.01, 3.0,  0.02],
                               color=C2M, stroke_width=2.5)
        self.play(
            LaggedStart(
                AnimationGroup(Create(spec_2p_c), Write(lbl_2k0)),
                AnimationGroup(Create(spec_sd_c), Write(lbl_sd)),
                AnimationGroup(Create(spec_3p_c), Write(lbl_3k0)),
                lag_ratio=0.4,
            )
        )
        self.wait(2.8)

        # ══ ⑤ Animated wave + growing time series ════════════════════════════
        # Clear the annotation / equation overlays and the envelope guides
        self.play(
            FadeOut(lin_eq), FadeOut(nl_eq),
            FadeOut(ref_line), FadeOut(arr), FadeOut(pct_lbl),
            FadeOut(env_u), FadeOut(env_l),
        )

        # ── Time series axes (bottom panel) ───────────────────────────────────
        # Slightly left of centre — leaves right margin clear for annotations
        ax_t = Axes(
            x_range=[0, T_END, 3],
            y_range=[-0.40, 0.40, 0.20],
            x_length=10.3,
            y_length=1.9,
            axis_config={"include_tip": False},
            x_axis_config={
                "numbers_to_include": [3, 6, 9, 12, 15, 18],
                "font_size": 26,
            },
            y_axis_config={
                "numbers_to_include": [-0.20, 0.0, 0.20],
                "font_size": 24,
            },
        ).move_to([-0.15, -2.42, 0])

        head_t = T(f"Wave gauge record  at  x = {X_FIXED:.0f} m",
                      font_size=20, color=GREY_B).next_to(ax_t, UP, buff=0.14)
        lab_xt = ax_t.get_x_axis_label(MathTex("t\\ (\\mathrm{s})", font_size=26))
        lab_yt = ax_t.get_y_axis_label(MathTex("\\eta", font_size=26))

        self.play(Create(ax_t), Write(head_t), Write(lab_xt), Write(lab_yt))
        self.wait(1.0)

        # ── Single ValueTracker drives BOTH spatial animation and time series ─
        t_grow = ValueTracker(0.001)

        # Spatial: wave group moves to the right
        lin_live = always_redraw(lambda: ax_s.plot(
            lambda x: eta_lin(x, t_grow.get_value()),
            x_range=[-14, 14, 0.05], color=C_LIN, stroke_width=2.5,
        ))
        nl_live = always_redraw(lambda: ax_s.plot(
            lambda x: eta_nl(x, t_grow.get_value()),
            x_range=[-14, 14, 0.05], color=C_NL, stroke_width=2.5,
        ))
        # Header shows current time
        head_s_live = always_redraw(lambda:
            T(
                f"Spatial snapshot  (t = {t_grow.get_value():.1f} s)",
                font_size=20, color=GREY_B,
            ).next_to(ax_s, UP, buff=0.22)
        )

        # Probe dots: coloured circles that ride the wave surface at x = X_FIXED.
        # Their vertical position traces exactly what the time series records.
        probe_dot_lin = always_redraw(lambda: Dot(
            ax_s.c2p(X_FIXED, eta_lin(X_FIXED, t_grow.get_value())),
            radius=0.09, color=C_LIN,
        ).set_stroke(WHITE, width=1.5))
        probe_dot_nl = always_redraw(lambda: Dot(
            ax_s.c2p(X_FIXED, eta_nl(X_FIXED, t_grow.get_value())),
            radius=0.09, color=C_NL,
        ).set_stroke(WHITE, width=1.5))

        # Time series: grow from left as t_grow advances
        live_ts_lin = always_redraw(lambda: ax_t.plot(
            lambda t: eta_lin(X_FIXED, t),
            x_range=[0, t_grow.get_value(), 0.04],
            color=C_LIN, stroke_width=2.2,
        ))
        live_ts_nl = always_redraw(lambda: ax_t.plot(
            lambda t: eta_nl(X_FIXED, t),
            x_range=[0, t_grow.get_value(), 0.04],
            color=C_NL, stroke_width=2.2,
        ))

        # Swap static spatial plots → animated; start both panels together
        self.play(FadeOut(lin0), FadeOut(nl0), FadeOut(head_s))
        self.add(
            lin_live, nl_live, head_s_live,
            probe_dot_lin, probe_dot_nl,
            live_ts_lin, live_ts_nl,
        )
        self.play(t_grow.animate.set_value(T_END), run_time=11, rate_func=linear)
        self.wait(1.4)

        # ── Annotate phase offset in the time series ──────────────────────────
        # NL carrier is faster → its crests arrive a little earlier
        t_group = X_FIXED / CG   # group centre passes the probe here
        t_region = np.linspace(t_group + 0.5, t_group + 2.5, 500)
        t_lin_crest = t_region[np.argmax([eta_lin(X_FIXED, t) for t in t_region])]
        t_nl_crest  = t_region[np.argmax([eta_nl(X_FIXED,  t) for t in t_region])]
        dt = t_lin_crest - t_nl_crest   # > 0: NL crest arrives earlier

        vl_lin = DashedLine(
            ax_t.c2p(t_lin_crest, -0.38), ax_t.c2p(t_lin_crest, 0.38),
            stroke_width=1.5, color=C_LIN, dash_length=0.10,
        )
        vl_nl = DashedLine(
            ax_t.c2p(t_nl_crest, -0.38), ax_t.c2p(t_nl_crest, 0.38),
            stroke_width=1.5, color=C_NL, dash_length=0.10,
        )
        dt_arrow = DoubleArrow(
            ax_t.c2p(t_nl_crest, 0.32), ax_t.c2p(t_lin_crest, 0.32),
            buff=0, stroke_width=2.0, color=WHITE, tip_length=0.10,
        )
        dt_lbl = MathTex(
            rf"\Delta t \approx {abs(dt)*1000:.0f}\ \mathrm{{ms}}",
            font_size=24, color=WHITE,
        ).next_to(dt_arrow, UP, buff=0.08)

        self.play(Create(vl_lin), Create(vl_nl))
        self.play(GrowArrow(dt_arrow), Write(dt_lbl))
        self.wait(3.2)

        # Phase-drift formula — placed in the gap between upper and lower panels
        # (below ax_s bottom ≈ y −0.15, above head_t ≈ y −1.49)
        phase_note = MathTex(
            r"\text{Small nonlinear phase-speed increase}"
            r"\quad\Rightarrow\quad"
            r"\text{arrival-time drift builds up gradually}",
            font_size=24, color=YELLOW,
        ).move_to([-1.5, -0.82, 0])   # left-of-centre, clear of spectrum labels
        self.play(Write(phase_note))
        self.wait(2.8)

        # ══ ⑥ 合 — Takeaway (replaces spectrum panel) ════════════════════════
        self.play(FadeOut(phase_note))

        # Collect and fade out all spectrum-panel elements
        spec_group = VGroup(
            ax_k, head_k, lab_xk, lab_yk,
            spec_lin_c, spec_2p_c, spec_3p_c, spec_sd_c,
            lbl_k0, lbl_2k0, lbl_3k0, lbl_sd,
        )

        self.play(FadeOut(spec_group), FadeOut(probe_vline), FadeOut(probe_lbl_s))

        # Return to a clean t = 0 comparison in the spatial panel before the bridge.
        ts_final_lin = ax_t.plot(
            lambda t: eta_lin(X_FIXED, t),
            x_range=[0, T_END, 0.04], color=C_LIN, stroke_width=2.2,
        )
        ts_final_nl = ax_t.plot(
            lambda t: eta_nl(X_FIXED, t),
            x_range=[0, T_END, 0.04], color=C_NL, stroke_width=2.2,
        )
        self.remove(
            lin_live, nl_live, head_s_live,
            probe_dot_lin, probe_dot_nl,
            live_ts_lin, live_ts_nl,
        )
        self.add(ts_final_lin, ts_final_nl)
        lin_reset = ax_s.plot(lambda x: eta_lin(x, 0),
                              x_range=[-14, 14, 0.05], color=C_LIN, stroke_width=2.5)
        nl_reset = ax_s.plot(lambda x: eta_nl(x, 0),
                             x_range=[-14, 14, 0.05], color=C_NL, stroke_width=2.5)
        head_s_reset = T("Spatial snapshot  (t = 0 s)", font_size=20, color=GREY_B)\
            .next_to(ax_s, UP, buff=0.22)
        curve_labels = VGroup(
            T("linear", font_size=18, color=C_LIN),
            T("nonlinear", font_size=18, color=C_NL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to(ax_s.c2p(-10.5, 0.34))
        self.play(Create(lin_reset), Create(nl_reset), FadeIn(head_s_reset), Write(curve_labels))

        shape_takeaway = VGroup(
            T("Nonlinear shape at t = 0", font_size=20, color=YELLOW, weight=BOLD),
            T("Sharper crests and flatter troughs than linear theory predicts",
                 font_size=16, color=GREY_A),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)

        timing_takeaway = VGroup(
            T("Nonlinear propagation at a fixed gauge", font_size=20, color=YELLOW, weight=BOLD),
            T("Crests reach the probe earlier than linear theory predicts",
                 font_size=16, color=GREY_A),
            T("That timing mismatch accumulates as the wave group passes",
                 font_size=16, color=GREY_A),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)

        bridge = T(
            "What generates these extra components?  ->  Bound harmonics",
            font_size=15, color=GREY_B,
        )

        takeaway_content = VGroup(
            shape_takeaway,
            timing_takeaway,
            bridge,
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to(ax_k.get_center())

        takeaway_panel = SurroundingRectangle(
            takeaway_content,
            buff=0.22,
            corner_radius=0.12,
            stroke_color=GREY_D,
            stroke_width=1.2,
            fill_color=BLACK,
            fill_opacity=0.22,
        )

        spatial_box = SurroundingRectangle(ax_s, color=YELLOW, buff=0.12, corner_radius=0.06)
        time_box = SurroundingRectangle(ax_t, color=YELLOW, buff=0.12, corner_radius=0.06)

        self.play(FadeIn(takeaway_panel), Write(shape_takeaway), Create(spatial_box))
        self.wait(1.8)
        self.play(Write(timing_takeaway), ReplacementTransform(spatial_box, time_box))
        self.wait(1.8)
        self.play(Write(bridge))
        self.wait(4.8)
