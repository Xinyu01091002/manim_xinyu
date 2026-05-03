# Bound Waves for a Beginner PhD Student

## Project Goal

Build a Manim lecture segment that explains where bound waves come from, starting
from the finite-depth potential-flow problem and ending with the difference
between monochromatic Stokes-wave harmonics and bound waves in multi-frequency
wave groups.

The project should feel like a guided derivation with visual support, not a
research-result presentation. The central message is:

`Bound waves are nonlinear corrections forced by the primary free waves through
the free-surface boundary conditions. They are phase-locked to the waves that
generate them, rather than independent free waves satisfying the dispersion
relation on their own.`

Use finite depth throughout:

`\omega^2 = gk\tanh(kh)`.

Use explicit second-order Stokes coefficients for the monochromatic part, while
keeping the multi-frequency coefficients schematic enough to avoid drowning the
first explanation in kernel notation.

---

## Core Interpretation To Preserve

- The fluid interior is simple: `\nabla^2\phi = 0`.
- The hard part is the free surface: the boundary conditions are nonlinear and
  applied at the unknown surface `z=\eta(x,t)`.
- Linearization gives free waves whose frequency and wavenumber satisfy the
  finite-depth dispersion relation.
- Perturbation theory uses wave steepness, e.g. `\epsilon = ak`, to organize the
  correction terms.
- At second order, products of first-order waves force new surface components.
- For a monochromatic Stokes wave, the second-order correction is mainly a
  phase-locked `2k,2\omega` harmonic.
- For a wave group, second order is not one harmonic: every pair of primary
  components can generate sum-frequency and difference-frequency bound content.

---

## Notation Convention

Use 2D finite-depth waves:

- horizontal coordinate: `x`
- vertical coordinate: `z`
- still water level: `z=0`
- flat bottom: `z=-h`
- free surface: `z=\eta(x,t)`
- velocity potential: `\phi(x,z,t)`
- phase: `\theta = kx-\omega t`
- finite-depth factor: `\sigma = \tanh(kh)`

Linear dispersion:

`\omega^2 = gk\sigma`.

For the finite-depth second-order Stokes free surface, use the standard
monochromatic coefficient:

`\eta(x,t)=a\cos\theta+\frac{ka^2}{4}\frac{3-\sigma^2}{\sigma^3}\cos(2\theta)+O(a^3k^2)`.

This form has the right deep-water limit:

`\sigma\to1 \quad\Rightarrow\quad \eta=a\cos\theta+\frac{1}{2}ka^2\cos(2\theta)+\cdots`.

Implementation note: if the lecture later needs the potential correction, verify
the chosen convention for mean level, phase sign, and normalization before
committing coefficients to animation text.

---

## Narrative Structure

## Scene 0: The Finite-Depth Free-Surface Problem

Goal: define the mathematical problem and locate the source of difficulty.

### Qi - Setup

- Draw a finite-depth water domain with bottom `z=-h`, still water level `z=0`,
  and free surface `z=\eta(x,t)`.
- Introduce the velocity potential `\phi`.
- State assumptions quietly:
  inviscid, incompressible, irrotational, 2D.

### Cheng - Build

Show the governing equation and boundary conditions:

- interior:
  `\phi_{xx}+\phi_{zz}=0,\quad -h<z<\eta`
- bottom:
  `\phi_z=0,\quad z=-h`
- kinematic free-surface condition:
  `\eta_t+\phi_x\eta_x-\phi_z=0,\quad z=\eta`
- dynamic free-surface condition:
  `\phi_t+\frac{1}{2}(\phi_x^2+\phi_z^2)+g\eta=0,\quad z=\eta`

### Zhuan - Core Insight

- Highlight that the interior equation is linear.
- Highlight that nonlinearity enters through:
  - products such as `\phi_x\eta_x`
  - quadratic velocity terms
  - evaluating the boundary conditions at `z=\eta`

### He - Takeaway

The wave problem is nonlinear because the free boundary moves and the boundary
conditions multiply wave quantities together.

Visual priorities:

- Use one stable water-domain sketch.
- Keep equations to the side in a vertical stack.
- Animate only the highlight from interior equation to free-surface conditions.

---

## Scene 1: Linearization and the First Free Wave

Goal: recover finite-depth linear theory as the baseline.

### Qi - Setup

- Start from small amplitude: `|\eta|/h\ll1`, `ak\ll1`.
- Move the free-surface conditions from `z=\eta` to `z=0`.

### Cheng - Build

Keep only first-order terms:

- kinematic:
  `\eta_t-\phi_z=0,\quad z=0`
- dynamic:
  `\phi_t+g\eta=0,\quad z=0`

Use a monochromatic ansatz:

- `\eta_1=a\cos(kx-\omega t)`
- `\phi_1=\frac{a\omega}{k\sinh(kh)}\cosh k(z+h)\sin(kx-\omega t)`

Then reveal:

`\omega^2=gk\tanh(kh)`.

### Zhuan - Core Insight

- Show a single spectral spike at `k`.
- Label it as a free wave.
- Add a small dispersion badge:
  `k -> \omega(k)`.

### He - Takeaway

Linear theory gives free waves: each component propagates with the finite-depth
dispersion relation.

Visual priorities:

- Pair the surface wave with a vertical-mode sketch.
- Keep the spectrum simple: one spike at `k`.
- Do not introduce bound waves yet.

---

## Scene 2: Perturbation Bookkeeping

Goal: explain why second-order terms are unavoidable once the original boundary
conditions are kept.

### Qi - Setup

Introduce steepness:

`\epsilon=ak`.

Write the expansions:

- `\eta=\epsilon\eta_1+\epsilon^2\eta_2+\epsilon^3\eta_3+\cdots`
- `\phi=\epsilon\phi_1+\epsilon^2\phi_2+\epsilon^3\phi_3+\cdots`

### Cheng - Build

Show Taylor expansion from the unknown surface to the still-water level:

`F(x,\eta,t)=F(x,0,t)+\eta F_z(x,0,t)+\frac{1}{2}\eta^2F_{zz}(x,0,t)+\cdots`.

Apply this visually to the free-surface boundary conditions.

### Zhuan - Core Insight

Reveal the types of second-order forcing:

- products from the kinematic condition:
  `\phi_x\eta_x`
- products from Bernoulli:
  `\frac{1}{2}(\phi_x^2+\phi_z^2)`
- Taylor-shift terms:
  `\eta\phi_{zt}`, `\eta\phi_{zz}`, etc.

The exact algebra can be shown as grouped forcing terms rather than line by line.

### He - Takeaway

Second-order waves are forced by products of first-order waves. They are not
added by hand.

Visual priorities:

- Use color to mark first-order quantities, then show their products becoming
  second-order forcing.
- Avoid filling the screen with a full derivation.

---

## Scene 3: Second-Order Finite-Depth Stokes Wave

Goal: make the first bound harmonic explicit for one frequency.

### Qi - Setup

Start with:

`\eta_1=a\cos\theta,\quad \theta=kx-\omega t`.

Remind the viewer:

`\omega^2=gk\tanh(kh)`.

### Cheng - Build

Show the key trigonometric mechanism:

`\cos^2\theta=\frac{1}{2}(1+\cos2\theta)`.

Then reveal the finite-depth second-order surface elevation:

`\eta=a\cos\theta+\frac{ka^2}{4}\frac{3-\sigma^2}{\sigma^3}\cos2\theta+O(a^3k^2),\quad \sigma=\tanh(kh)`.

Optionally show the coefficient as:

`C_2(kh)=\frac{1}{4}\frac{3-\sigma^2}{\sigma^3}`.

So:

`\eta=a\cos\theta+ka^2C_2(kh)\cos2\theta+\cdots`.

### Zhuan - Core Insight

- Add the second harmonic to the first-order sine wave.
- Show crest sharpening and trough flattening.
- In the spectrum, add a `2k` peak.
- Mark it as bound, not free.

Important explanation:

The second harmonic has phase `2\theta=2kx-2\omega t`. A free wave at wavenumber
`2k` would have frequency `\omega(2k)`, not necessarily `2\omega(k)`. Therefore
the second harmonic is locked to the primary wave rather than independently
obeying the linear dispersion relation.

### He - Takeaway

For one Stokes wave, the leading bound wave is a phase-locked second harmonic
with an explicit finite-depth coefficient.

Visual priorities:

- Show `\omega(2k)` versus `2\omega(k)` as a small dispersion-relation inset.
- Keep the coefficient visible but not dominant.
- The physical shape change should be the main visual payoff.

---

## Scene 4: Higher-Order Stokes Pattern

Goal: show extension without doing a full high-order derivation.

### Qi - Setup

Start from the second-order result and ask:

`What happens if we keep going?`

### Cheng - Build

Show the hierarchy:

- order 1:
  `a\cos\theta`
- order 2:
  `ka^2C_2(kh)\cos2\theta`
- order 3:
  `k^2a^3C_3(kh)\cos3\theta` plus corrections to the fundamental
- order 4:
  `k^3a^4C_4(kh)\cos4\theta` plus lower-harmonic corrections

Use coefficient placeholders after second order:

`C_3(kh), C_4(kh), ...`

### Zhuan - Core Insight

- Each order introduces new harmonics and also modifies lower harmonics.
- The harmonics remain phase-locked to the same base phase `\theta`.
- The expansion is ordered by powers of steepness.

### He - Takeaway

Higher-order Stokes theory repeats the same idea: nonlinear boundary conditions
generate a hierarchy of bound harmonics.

Visual priorities:

- Use a harmonic ladder, not a dense equation wall.
- Preserve the explicit second-order coefficient as the anchor.

---

## Scene 5: From a Single Wave to a Wave Group

Goal: move from monochromatic Stokes waves to realistic multi-frequency waves.

### Qi - Setup

Replace one phase with many:

`\eta_1(x,t)=\sum_m a_m\cos(k_mx-\omega_mt+\alpha_m)`.

with:

`\omega_m^2=gk_m\tanh(k_mh)`.

### Cheng - Build

Show why groups matter:

- wave flumes generate packets
- ocean waves are spectral
- focusing events involve many nearby frequencies
- measured time series contain both free and bound content

### Zhuan - Core Insight

Animate a narrow spectrum becoming a spatial group.

Important message:

A wave group is not just "a Stokes wave with an envelope." It is many free
components, and nonlinear products can couple every pair.

### He - Takeaway

The moment we move from one frequency to many, second order becomes a pairwise
interaction problem.

Visual priorities:

- Use spectrum panel plus surface-profile panel.
- Keep all components finite-depth dispersive.

---

## Scene 6: Bound Waves in a Multi-Frequency Group

Goal: explain the key difference between second-order Stokes waves and
second-order group-bound waves.

### Qi - Setup

Start with two linear components:

`\eta_1=a_1\cos\theta_1+a_2\cos\theta_2`.

Show product identities:

`\cos\theta_m\cos\theta_n=\frac{1}{2}\cos(\theta_m+\theta_n)+\frac{1}{2}\cos(\theta_m-\theta_n)`.

### Cheng - Build

Generalize to many components:

- sum-frequency terms:
  `(k_m+k_n,\omega_m+\omega_n)`
- difference-frequency terms:
  `(|k_m-k_n|,|\omega_m-\omega_n|)`

Represent the second-order group-bound surface schematically:

`\eta_2=\sum_m\sum_n a_ma_n\left[G^+_{mn}\cos(\theta_m+\theta_n)+G^-_{mn}\cos(\theta_m-\theta_n)\right]`.

Use `G^+_{mn}` and `G^-_{mn}` as finite-depth interaction coefficients, with a
note that they depend on `k_m`, `k_n`, and `h`.

### Zhuan - Core Insight

Contrast:

- monochromatic Stokes:
  one self-interaction, `k+k -> 2k`
- wave group:
  many pair interactions, `(k_m,k_n) -> k_m+k_n` and `k_m-k_n`

Show:

- high-frequency bound waves under crests from sum interactions
- long set-down / set-up under the group from difference interactions

### He - Takeaway

For a Stokes wave, "second order" looks like one phase-locked harmonic. For a
wave group, "second order" is a family of bound waves generated by pairs of
free-wave components.

Visual priorities:

- Pair-interaction grid.
- Spectrum panel with sum-frequency region and near-zero difference-frequency
  region.
- Spatial panel showing carrier-scale sharpening plus group-scale set-down.

---

## Scene 7: Final Synthesis

Goal: leave the student with a durable mental model.

Use three side-by-side panels:

1. Linear finite-depth free waves:
   `\omega^2=gk\tanh(kh)`.
2. Monochromatic Stokes wave:
   phase-locked `2\theta`, `3\theta`, ... harmonics.
3. Multi-frequency wave group:
   pairwise sum- and difference-frequency bound waves.

Final takeaway:

`Free waves choose their frequency from the dispersion relation. Bound waves
inherit their phase from the waves that force them.`

---

## Recommended Runtime

Target lecture-segment duration: about 10-15 minutes.

Suggested pacing:

- Scene 0: 1.5-2 min
- Scene 1: 1.5-2 min
- Scene 2: 2 min
- Scene 3: 2.5-3 min
- Scene 4: 1 min
- Scene 5: 1.5-2 min
- Scene 6: 2-3 min
- Scene 7: 0.5-1 min

If it needs to be shorter, compress Scenes 2 and 4, but keep Scene 3 and Scene 6
intact.

---

## Visual Priorities

- Use finite-depth geometry consistently; always show the bottom when drawing the
  fluid domain.
- Use one color for first-order/free waves and another for bound corrections.
- Pair every important equation with a visual:
  - boundary conditions with domain sketch
  - dispersion relation with spectrum spike
  - second-order coefficient with crest sharpening
  - pair sums/differences with interaction grid
- Keep text motion restrained.
- Use pauses after the dispersion relation, the second-order coefficient, and the
  Stokes-versus-group contrast.

---

## First Implementation Pass

Implement the first pass as static-to-lightly-animated Manim scenes:

1. `scenario0_problem_setup.py`
2. `scenario1_linear_solution.py`
3. `scenario2_second_order_stokes.py`
4. `scenario5_group_bound_waves.py`

These four scenes prove the core teaching path. The higher-order and final
synthesis scenes can be added after the main derivation and group contrast feel
clear.

---

## Checks Before Rendering Final Video

- The notation uses `\sigma=\tanh(kh)` consistently.
- The finite-depth dispersion relation appears before any bound-wave claim.
- The second-order Stokes coefficient has the correct deep-water limit.
- The animation explicitly says why `2k,2\omega` is bound rather than free.
- The group section includes both sum- and difference-frequency terms.
- The final comparison does not imply that wave groups are simply modulated
  monochromatic Stokes waves.
