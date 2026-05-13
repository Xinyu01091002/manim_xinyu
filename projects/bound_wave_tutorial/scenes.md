# Bound Wave Tutorial Scene Plan

This project is now a presenter-controlled Manim Slides deck rather than only a
placeholder scaffold.

- Source file: `slides_bound_wave_intro.py`
- Full deck class: `BoundWaveIntroSlides`
- Scenario preview classes:
  - `BoundWaveIntroS0Problem`
  - `BoundWaveIntroS1Perturbation`
  - `BoundWaveIntroS2LinearTheory`
  - `BoundWaveIntroS3SecondOrderBC`
  - `BoundWaveIntroS4BoundHarmonics`
  - `BoundWaveIntroS5WaveGroups`

The deck uses a compact bottom navigation bar with 24 labelled navigation
checkpoints. Several checkpoints contain multiple presenter pauses, so the
rendered Manim Slides JSON may contain many more slide steps than the navigation
count.

## Narrative Arc

The tutorial explains bound waves through the finite-depth free-surface
boundary-value problem:

```text
potential flow -> moving free boundary -> perturbation expansion
-> linear theory -> second-order forcing -> bound harmonics and groups
```

The current editorial rule is to keep exact final interaction coefficients out
of the main deck until the preferred coefficient form is chosen. The deck should
use symbolic or qualitative coefficient language when explaining the mechanism.

## S0: Problem Description

Purpose: make clear that this is a fluid-domain free-boundary problem, not just
a surface-curve animation.

1. Potential flow as a useful first model.
2. What the velocity potential buys: one scalar unknown plus Laplace's equation.
3. Finite-depth domain with bottom, still-water level, and unknown surface.
4. Bottom no-penetration condition.
5. Kinematic free-surface condition from `DF/Dt=0`.
6. Dynamic free-surface condition from pressure balance and Bernoulli's equation.

Style notes:

- Keep the tank geometry stable.
- Let arrows and labels do the physical explanation.
- Do not over-animate text labels.

## S1: Perturbation And Linearization

Purpose: explain why the moving boundary is hard and how small amplitude moves
the boundary conditions to `z=0`.

7. Free-boundary difficulty: conditions are imposed at `z=eta(x,t)`.
8. Smallness assumptions: amplitude, steepness `epsilon=ka`, and `|eta|/h`.
9. Collect terms by order after substituting the perturbation expansion.
10. Taylor expansion around `z=0` and the first-order evaluation step.

Style notes:

- Keep the distinction between `z=eta` and `z=0` visually obvious.
- Use equations as checkpoints, not as a dense derivation wall.

## S2: Linear Waves And Groups

Purpose: derive the finite-depth first-order solution, then motivate why
realistic grouped wave shapes are the object we care about before introducing
second-order forcing.

11. Full first-order boundary-value problem on the fixed domain.
12. Sinusoidal mode ansatz and finite-depth vertical structure.
13. Dynamic condition determines the potential amplitude.
14. Kinematic condition recovers the dispersion relation.
15. Linear wave groups as superposition of free components.
16. Large random-wave crests average into a group-like conditional shape.
17. Why we keep wave groups in view: ocean waves come in groups, designed wave
    groups are easier to reproduce in the lab than random time series, and
    averaged extreme events recover a group-like shape.

Style notes:

- Preserve the finite-depth factor and bottom condition visually.
- Keep the wave-group slides qualitative. They provide the physical target for
  the later second-order pairwise calculation.

## S3: Second-Order Boundary Conditions

Purpose: show where bound-wave forcing first appears.

18. Transition from linear theory to second order.
19. Taylor-expanded second-order dynamic and kinematic conditions.
20. Quadratic products of first-order fields force second-order right-hand
    sides.

Style notes:

- This section is the mathematical hinge of the tutorial.
- Emphasize products such as `cos(theta)cos(theta)` becoming a mean plus
  `cos(2theta)`.

## S4: Bound Harmonics

Purpose: explain the bound-wave mechanism without committing to a final
coefficient notation.

21. Monochromatic Stokes-wave schematic: primary wave plus symbolic second
    harmonic.
22. Free-wave versus bound-wave dispersion-space distinction.
23. Two-component interaction: self-products and cross-products generate
    harmonic, sum, and difference components.

Style notes:

- Keep final exact coefficient formulas out of this scenario for now.
- The viewer should leave with phase-locking and forced-response intuition.

## S5: Wave Groups

Purpose: apply the pairwise bound-wave idea to a focused or grouped wave field.

24. Second-order wave-group map: the left side shows the linear spectrum, while
    the right side separates the second superharmonic branch (`k_m+k_n`) and
    second subharmonic branch (`|k_m-k_n|`). The spectra use a shared magnitude
    scale. The bottom rows accumulate `eta22`, `eta20` with visible set-down near
    `K=0`, and their sum.
25. Waveform/spectrum bridge: the left side reveals `eta11`, `eta22`, and
    `eta33` as group-bound waveform components while the right side reveals the
    corresponding spectral components at the same time. The second-order
    component uses the summed phase relation, `eta22+ ~ cos(2 theta)`, and marks
    that the bound harmonic carries `omega = 2 omega0` rather than the free
    dispersion value at `2 k0`.

The final checkpoint keeps the all-pairs construction and then moves directly to
the waveform/spectrum interpretation with a light higher-order continuation.

Style notes:

- Treat this as the bridge from clean derivation to research intuition.
- Keep this ending visual-first; use equations and captions as labels, not as a
  text recap.
- Do not introduce VWA, Creamer transforms, or unrelated PhD confirmation
  material.

## Current Open Decisions

- Which exact finite-depth Stokes coefficient should eventually replace the
  symbolic second-harmonic coefficient?
- Which exact two-component interaction coefficient notation should be used?
- Whether the full production version should remain one deck file or be split
  into shared helpers plus scenario-specific files.

## Render Workflow

Use the repo clean-render helper for iterative preview renders from the repo
root:

```powershell
python tools\manim_slides_clean_render.py projects\bound_wave_tutorial\slides_bound_wave_intro.py BoundWaveIntroS4BoundHarmonics -q l --no-flush-cache
```

Then export or rebuild the corresponding HTML preview when the scene is ready
for browser review.
