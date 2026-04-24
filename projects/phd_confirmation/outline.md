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

## Scenario 2: Why Exact Interactions Become Expensive

Goal: explain why component-resolved bound-wave theory becomes computationally expensive before introducing VWA.

### Qi - Setup
- Start from a realistic linear wave group represented by many spectral components.
- Write the linear component sum:
  `eta^(11) = sum a_m cos(theta_m)`.

### Cheng - Build
- Show that second-order superharmonics arise from all component pairs:
  `(k_m, k_n) -> k_m + k_n`.
- Write the component-resolved second-order expression:
  `eta_exact^(22) = sum_m sum_n a_m a_n G_{m+n}(k_m,k_n) cos(theta_m + theta_n)`.
- Visualize the full pair interaction grid.

### Zhuan - Core insight
- Emphasize that the number of interactions grows as:
  `N_c^2` for second order,
  `N_c^3` for third order,
  and `N_c^n` at order `n`.
- The exact approach is accurate, but repeated evaluation becomes the bottleneck for broadband wave groups and higher-order harmonics.

### He - Takeaway
- The next method should preserve the physically important sum-phase structure while avoiding the full interaction grid.
- Bridge to VWA:
  `keep the phases, approximate the kernel amplitude, separate the sums`.

### Visual / implementation notes
- Current low-quality preview command:
  `manim -ql scenario2_exact_interactions.py WhyExactInteractionsAreExpensive`

---

## Scenario 3: The VWA Idea (TBD)

Goal: introduce the exact second-order superharmonic formulation and the VWA formulation side by side, so the kernel reduction and cost reduction are visible in one step.

### Qi - Setup
- Start from the exact second-order superharmonic expression:
  `eta_exact^(22) = sum_m sum_n a_m a_n G_{m+n}(k_m,k_n) cos(theta_m + theta_n)`.
- Remind the audience that the expensive part is the fully pair-dependent interaction kernel over all component pairs.

### Cheng - Build
- Introduce the VWA substitution as a reduced kernel representation built from monochromatic / Stokes-informed coefficients.
- Keep the exact quadratic sum phase `theta_m + theta_n` visible during the comparison.
- Show visually that the change is in the kernel amplitude representation, not in the superharmonic phase structure.

### Zhuan - Core insight
- Derive or reveal the separated / convolutional structure of the VWA second-order formulation.
- Emphasize that the exact pairwise interaction grid is replaced by a reduced spectral synthesis structure.
- Bridge directly from this structural reduction to FFT-based evaluation.

### He - Takeaway
- Summarize in this order:
  1. exact theory: component-resolved and expensive
  2. VWA: reduced kernel representation for the same second-order superharmonic problem
  3. the algebra separates, enabling `O(N log N)` evaluation
- Keep the wording modest at this stage:
  introduce the reduced formulation first, then reserve the stronger claims about exact phase preservation and kernel-amplitude approximation for the following scene if needed.

---

## Scenario 4: What Is Preserved, What Is Approximated? (TBD)

Goal: explain that VWA preserves the exact superharmonic phase structure and approximates only the interaction-kernel amplitude.

---

## Scenario 5: Higher-Order Extension and Validation Bridge (TBD)

Goal: connect the compact VWA product form to second-, third-, fourth-, and fifth-order validation, then hand off to PPT result figures.

---

## Scenario 6: Future / Broader Uses of VWA (Draft)

Goal: briefly record possible broader uses beyond the present animation sequence.

Candidate directions:
- Directional waves: extend the same kernel-reduction idea to directionally spread wave groups.
- Time series: reconstruct bound harmonics directly from gauge records or temporal spectra where appropriate.
- Surface kinematics: use VWA to estimate surface velocity potential and related kinematic quantities, not only free-surface elevation.
- Inverse problems: use the fast forward model inside fitting, separation, or reconstruction workflows where repeated evaluations are required.
