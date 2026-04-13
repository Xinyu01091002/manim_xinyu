# PhD Confirmation - Manim Animation Outline

## Scenario 0: Why Do Nonlinear Waves Matter?

Goal: motivate why linear wave theory is not enough before introducing bound harmonics.
The scene should show an observable mismatch between linear and nonlinear wave groups in both space and at a fixed probe.

### Qi - Setup
- Show a linear wave group in the lab frame.
- Use a Gaussian envelope with a narrow-band carrier.
- Introduce the spatial panel, the wavenumber-spectrum panel, and a fixed probe location.

### Cheng - Build
- Overlay the nonlinear/Stokes wave on top of the linear wave at `t = 0`.
- Emphasize the spatial shape difference first:
  sharper crests and flatter troughs.
- Keep the nonlinear enhancement modest, about a 10% crest increase relative to the linear case.
- Show the spectral fingerprint with energy at `2k_0`, `3k_0`, and near `k ≈ 0`.

### Zhuan - Core insight
- Animate the group propagating across the spatial domain while the probe records the full time series.
- Use a larger spatial domain and a farther probe so the full wave group is visible in both panels.
- Highlight that the nonlinear crests reach the probe slightly earlier than linear theory predicts.
- Treat the timing difference as visible but realistic, not exaggerated.

### He - Takeaway
- Return the spatial panel to a clean `t = 0` comparison between linear and nonlinear waves.
- Keep the time-series result visible at the bottom during the takeaway.
- Summarize in this order:
  1. nonlinear shape at `t = 0`: sharper crests and flatter troughs
  2. nonlinear propagation at a fixed gauge: earlier crest arrival and accumulated timing mismatch
- Bridge to the next scene with:
  `What generates these extra components? -> Bound harmonics`

### Visual / implementation notes
- Prefer TeX-rendered text for consistent spacing with equations.
- Figure-internal text should be clearly readable in presentation mode:
  axis labels, tick numbers, spectrum labels, probe labels, and in-figure equations all need to be large enough.
- Default development render is low quality from the project directory:
  `manim -ql scenario0_why_nonlinear.py WhyNonlinearWaves`
- Final export is high quality:
  `manim -qh scenario0_why_nonlinear.py WhyNonlinearWaves`

---

## Scenario 1: What Are Bound Harmonics?

Goal: explain what the extra nonlinear components actually are, after Scenario 0 has established why they matter.

### Qi - Setup
- Start from a clean linear wave group in space and spectrum.
- Write the linear form explicitly:
  `eta_lin`.

### Cheng - Build
- Add the bound components one by one:
  second-order superharmonic,
  second-order set-down,
  and third-order contribution.
- Show where each term appears in the spectrum.

### Zhuan - Core insight
- Write the total nonlinear form explicitly as `eta_nl`, not only the linear expression.
- Reveal that the full nonlinear structure sharpens crests and flattens troughs.
- Emphasize that these components remain locked to the group rather than propagating independently as free waves.

### He - Takeaway
- Bound harmonics are phase-locked, group-bound nonlinear structure.
- They do not behave like separate free waves satisfying the dispersion relation on their own.

---

## Scenario 2: Why Does the Approximation Work? (TBD)

## Scenario 3: Asymptotic Consistency with Exact Theory (TBD)
