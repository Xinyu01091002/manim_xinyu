# Beginner Bound-Wave Explanation Subproject Plan

## Requirements Summary

Create a new Manim subproject that explains bound waves to a beginning PhD student who is already familiar with potential flow basics. The project should be concept-first and derivation-guided, not a full research presentation. No video needs to be rendered yet.

The intended pedagogical flow is:

1. Define the water-wave problem from governing equation and boundary conditions.
2. Linearize about the still free surface and recover the linear wave solution.
3. Introduce wave steepness, typically `epsilon = ak`, as the small parameter.
4. Expand the potential and free-surface elevation perturbatively.
5. Keep second-order boundary-condition terms and derive or motivate the second-order Stokes correction.
6. Briefly show the higher-order pattern.
7. Move from one frequency to many frequencies, i.e. wave groups.
8. Explain why wave groups matter and how bound waves differ between monochromatic Stokes waves and multi-frequency wave groups.

## Repository Context

- Existing project structure is one folder per topic under `projects/`.
- `projects/phd_confirmation/outline.md` already has a high-level bound-harmonics scenario, but it assumes the viewer is ready for the research story.
- `projects/phd_confirmation/scenario1_bound_harmonics.py` contains reusable visual ideas: linear group, spectrum, set-down, second harmonic, third harmonic, and the message that bound components stay locked to the group.
- `projects/creamer_transform/outline.md` is a good model for a staged tutorial outline with conceptual spine, scenario goals, and takeaways.
- Repo style guidance asks for restrained text motion and animation effort concentrated on physical mechanisms, wave motion, spectra, phase locking, transforms, and diagrams.

## Recommended Subproject Shape

Suggested folder:

`projects/bound_waves_beginner/`

Suggested files:

- `README.md`: project goal, render commands, assumptions, mathematical scope.
- `outline.md`: scenario-by-scenario narrative.
- `common.py`: shared colors, `quiet_fade`, axes helpers, water-domain sketches, equation panel helpers.
- `scenario0_problem_setup.py`
- `scenario1_linear_solution.py`
- `scenario2_perturbation_and_stokes.py`
- `scenario3_bound_harmonics.py`
- `scenario4_wave_groups.py`
- `scenario5_stokes_vs_groups.py`

The existing `presentation_nav.py` could be copied or adapted only if this becomes a polished multi-scene presentation. For a first tutorial draft, a simpler shared title/progress label is likely enough.

## Proposed Outline

### Scenario 0: The Free-Surface Problem

Goal: establish the mathematical object without overwhelming the viewer.

Start from a 2D inviscid, incompressible, irrotational fluid. Show the fluid domain, free surface `z = eta(x,t)`, bottom condition, and velocity potential `phi`.

Core equations:

- `nabla^2 phi = 0` in the fluid.
- Dynamic free-surface condition from Bernoulli.
- Kinematic free-surface condition.
- Bottom condition, e.g. finite depth `phi_z = 0` at `z=-h`, or deep water decay.

Takeaway:

The difficulty is not Laplace's equation alone. The hard part is that the boundary conditions are applied on the moving unknown surface.

### Scenario 1: Linear Theory as the Baseline

Goal: recover the familiar first-order wave and identify what linear theory throws away.

Flatten the free surface to `z=0`, linearize the free-surface boundary conditions, and show the standard linear solution:

- `eta_1 = a cos(kx - omega t)`
- `phi_1` with vertical structure
- dispersion relation, either `omega^2 = gk tanh(kh)` or deep-water `omega^2 = gk`

Visual:

One clean sinusoid, one spectral spike at `k`, and a small note that every component satisfies the linear dispersion relation.

Takeaway:

Linear theory gives free waves: each Fourier component propagates according to the dispersion relation.

### Scenario 2: Small Parameter and Perturbation Bookkeeping

Goal: make the perturbation logic feel mechanical rather than mysterious.

Introduce `epsilon = ak` as wave steepness. Expand:

- `eta = epsilon eta_1 + epsilon^2 eta_2 + epsilon^3 eta_3 + ...`
- `phi = epsilon phi_1 + epsilon^2 phi_2 + epsilon^3 phi_3 + ...`

Then show why the boundary conditions must be Taylor-expanded from `z=eta` back to `z=0`.

Visual:

A moving free surface projected down to `z=0`, with second-order terms appearing as highlighted products of first-order quantities.

Takeaway:

Bound waves appear because nonlinear boundary conditions multiply first-order waves together.

### Scenario 3: Second-Order Stokes Wave

Goal: show the first bound harmonic in the simplest possible setting.

For a single carrier wave, keep the second-order terms and show that products such as `cos(theta)^2` generate:

- a mean contribution
- a `cos(2 theta)` contribution

Use the trigonometric identity as the visual bridge:

`cos^2(theta) = (1 + cos(2 theta))/2`

Then show the second-order free-surface structure schematically:

`eta = a cos(theta) + O(ka^2) cos(2 theta) + ...`

Visual:

Start with a sine wave. Add the second harmonic. The crest sharpens, trough flattens, and the spectrum gains a `2k` peak.

Takeaway:

In a Stokes wave, the second harmonic is not a new independent free wave. It is phase-locked to the primary wave.

### Scenario 4: Higher-Order Pattern

Goal: avoid a full derivation while making the extension intuitive.

Show that repeated nonlinear products create `3theta`, `4theta`, and higher harmonics, with amplitudes ordered by powers of steepness.

Visual:

A ladder:

- first order: `theta`, amplitude scale `a`
- second order: `2theta`, scale `ka^2`
- third order: `3theta`, scale `k^2 a^3`

Takeaway:

Higher-order Stokes theory is the same bookkeeping idea repeated: nonlinear boundary conditions generate phase-locked harmonics with progressively smaller amplitude for small steepness.

### Scenario 5: From One Frequency to a Wave Group

Goal: move from monochromatic thinking to realistic multi-component seas.

Replace one wave with:

`eta_1 = sum_m a_m cos(k_m x - omega_m t + alpha_m)`

Explain why this matters:

- laboratory wave packets
- focused wave groups
- ocean spectra
- initialization of nonlinear simulations
- separating free and bound content in measurements

Visual:

A narrow-banded spectrum becomes a spatial wave group. Use a simple group envelope and a spectrum panel.

Takeaway:

A wave group is not just "one Stokes wave with an envelope"; it contains many interacting components.

### Scenario 6: Bound Waves in Groups Are Interaction Products

Goal: explain the crucial difference between Stokes-wave harmonics and wave-group bound components.

For one frequency, second order mainly means `k + k = 2k`.

For many frequencies, second order includes many pair interactions:

- sum-frequency: `(k_m, k_n) -> k_m + k_n`
- difference-frequency / set-down: `(k_m, k_n) -> k_m - k_n`

Visual:

Show a pair-interaction grid beside the spectrum. Highlight one diagonal for sum frequencies and a near-zero region for difference-frequency set-down.

Takeaway:

In a Stokes wave, "second order" looks like a single second harmonic. In a wave group, "second order" is a whole family of bound components generated by pairs of free waves.

### Scenario 7: Final Synthesis

Goal: leave the student with the minimum durable mental model.

Three-panel summary:

1. Linear waves: free components satisfy dispersion.
2. Stokes wave: one carrier creates phase-locked harmonics.
3. Wave group: many carriers create sum- and difference-frequency bound structure.

Final sentence:

Bound waves are nonlinear corrections forced by the free waves; they travel with, and are locked to, the wave system that generated them.

## Acceptance Criteria

- The outline distinguishes free waves from bound waves explicitly.
- The perturbation expansion uses `ak` or equivalent steepness as the small parameter.
- The second-order Stokes explanation includes both the boundary-condition origin and the `cos^2(theta)` harmonic-generation intuition.
- The wave-group section explains both sum-frequency and difference-frequency bound components.
- The comparison between Stokes waves and wave groups is concrete: single self-interaction versus many pair interactions.
- The planned visuals follow repo style: quiet text, stable layouts, spectrum panels, wave profiles, and physical diagrams.

## Open Questions

Resolved from user feedback:

1. Use finite depth throughout with `\tanh(kh)`.
2. Use explicit coefficients for the second-order Stokes-wave part.
3. Target a lecture-segment length rather than a very short explainer.
4. Do not bridge to VWA or the other existing projects yet.

Remaining:

1. Decide whether implementation should be one continuous scene or multiple renderable scenarios.
2. Decide whether notation should exactly match the PhD confirmation project or use simpler teaching notation first.

## Recommended First Implementation Pass

Project outline now lives in `projects/bound_waves_beginner/outline.md`.

Start implementation with four scenes first:

1. `scenario0_problem_setup.py`: finite-depth governing equation and boundary conditions.
2. `scenario1_linear_solution.py`: finite-depth linear solution and dispersion relation.
3. `scenario2_second_order_stokes.py`: perturbation expansion and explicit second-order Stokes bound harmonic.
4. `scenario5_group_bound_waves.py`: sum- and difference-frequency bound waves in groups.

After those are visually working, fill the higher-order pattern, wave-group setup, and final synthesis scenes.

## Risks and Mitigations

- Risk: too much algebra too early.
  Mitigation: keep equations grouped by purpose: governing problem, linear baseline, perturbation bookkeeping, second-order forcing.

- Risk: students confuse second harmonic with a free wave.
  Mitigation: repeatedly contrast "satisfies dispersion independently" with "forced and phase-locked."

- Risk: wave-group section becomes computational/VWA too soon.
  Mitigation: first teach the pair-interaction picture; save cost reduction and VWA for a later project or final bridge.

- Risk: finite-depth coefficients distract from the core idea.
  Mitigation: choose deep water for first draft unless finite depth is central to your teaching goal.

## Verification Steps

Before rendering any final video:

- Review `outline.md` for mathematical continuity from boundary conditions to bound harmonics.
- Render low-quality previews scene by scene.
- Check equations for size and placement on 16:9 slides.
- Extract representative frames to confirm no overlap with bottom labels or navigation.
- Ask whether a beginner PhD student could answer:
  "What is bound about a bound wave?"
  "Where did the second harmonic come from?"
  "Why is a wave group different from a Stokes wave?"
