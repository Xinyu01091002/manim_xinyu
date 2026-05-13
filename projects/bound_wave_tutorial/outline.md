# Bound Waves From Free-Surface Boundary Conditions

## Project Goal

Build a derivation-led Manim tutorial that introduces bound waves from the
finite-depth potential-flow water-wave problem.

The tutorial should be visual enough that the physical meaning of each boundary
condition is clear, but it should remain a derivation lecture rather than a
purely qualitative explainer. Equations should appear at the points where they
clarify the logic.

The target viewer is a master's-level student or researcher who is comfortable
with perturbation expansions and Taylor expansion, but who has not necessarily
studied water waves before.

## Scope To Preserve

- Use finite depth from the start.
- Stay unidirectional.
- Introduce bound waves through monochromatic Stokes waves first.
- Later contrast a Stokes wave with a wave group.
- Extend from the monochromatic case to polychromatic second-order interaction
  theory.
- Do not mention VWA, Creamer transforms, or the PhD confirmation project.
- Do not insert final exact interaction coefficients until the user supplies
  the preferred coefficient form.

## Core Message

A bound wave is a nonlinear correction forced by the primary wave field. Its
phase and motion are tied to the primary wave components that generate it,
rather than being an independently prescribed free wave.

In a monochromatic Stokes wave, the simplest bound wave is the second harmonic.
In a polychromatic sea, bound waves arise from pairwise sum and difference
interactions between primary linear components.

## Narrative Spine

The tutorial has two nested arcs:

1. Mathematical arc:
   `potential-flow free-boundary problem -> nonlinear surface conditions ->
   perturbation expansion -> linear theory -> second-order forcing`.
2. Conceptual arc:
   `single Stokes wave -> bound harmonic -> wave group -> bound
   sum/difference waves`.

The first arc explains why bound waves appear. The second arc explains what they
mean physically.

---

## Part 1: The Physical Problem

Goal: introduce water waves as a finite-depth potential-flow free-boundary
problem.

Set the domain:

```tex
-h \le z \le \eta(x,t)
```

Introduce the velocity potential:

```tex
u = \phi_x,\qquad w = \phi_z
```

Use incompressibility and irrotationality to obtain:

```tex
\phi_{xx} + \phi_{zz} = 0
```

Physical meaning to explain:

- Potential flow works when the fluid is treated as inviscid, incompressible,
  and irrotational.
- The velocity field is determined by one scalar potential.
- The unknown surface elevation `eta(x,t)` is part of the solution.

Visual anchor:

- A finite-depth fluid domain.
- Bottom at `z=-h`.
- Still-water level `z=0`.
- Moving free surface `z=eta(x,t)`.
- Velocity arrows generated from the potential.

Takeaway:

The water-wave problem is not just a surface curve; it is a fluid-domain problem
whose upper boundary moves with the solution.

---

## Part 2: Boundary Conditions And Their Physical Meaning

Goal: explain the three essential boundary conditions before doing any
perturbation expansion.

Bottom boundary condition:

```tex
\phi_z = 0 \qquad \text{at } z=-h
```

Physical meaning:

The seabed is impermeable, so fluid cannot flow through it.

Kinematic free-surface condition:

```tex
\eta_t + \phi_x \eta_x = \phi_z
\qquad \text{at } z=\eta(x,t)
```

Physical meaning:

A particle on the free surface stays on the free surface. The surface is not a
painted curve that water crosses; it is a material boundary.

Dynamic free-surface condition:

```tex
\phi_t + \frac{1}{2}(\phi_x^2+\phi_z^2) + g\eta = 0
\qquad \text{at } z=\eta(x,t)
```

Physical meaning:

Pressure at the free surface matches atmospheric pressure. This is Bernoulli's
equation evaluated at the unknown surface, after choosing the atmospheric
pressure constant.

Visual anchor:

- Highlight the bottom condition with vertical arrows blocked at the bed.
- Highlight the kinematic condition by tracking a point on the moving surface.
- Highlight the dynamic condition by showing pressure balance at the surface.

Takeaway:

The boundary conditions are physical statements: no penetration at the bed,
surface particles remain on the surface, and pressure balances at the surface.

---

## Part 3: Why The Problem Is Hard

Goal: make the free-boundary nonlinearity explicit.

The free surface is unknown:

```tex
z = \eta(x,t)
```

but the boundary conditions must be applied exactly there:

```tex
\text{free-surface conditions at } z=\eta(x,t)
```

This gives two kinds of difficulty:

1. The boundary is part of the solution.
2. The equations contain nonlinear terms such as:

```tex
\phi_x \eta_x,
\qquad
\frac{1}{2}(\phi_x^2+\phi_z^2)
```

There is also nonlinearity hidden in evaluating quantities at `z=eta`, because
the evaluation height is itself unknown.

Visual anchor:

- Show boundary conditions attached to the moving free surface.
- Then show the desire to replace the moving evaluation level with the fixed
  still-water level `z=0`.

Takeaway:

The hard part is not Laplace's equation alone; it is the nonlinear moving
boundary where the surface conditions live.

---

## Part 4: Small-Amplitude Expansion

Goal: introduce perturbation theory as the way to replace the unknown boundary
by a hierarchy of problems on a known boundary.

Introduce a small parameter:

```tex
\epsilon \ll 1
```

Use expansions:

```tex
\eta = \epsilon \eta_1 + \epsilon^2 \eta_2 + \epsilon^3 \eta_3 + \cdots
```

```tex
\phi = \epsilon \phi_1 + \epsilon^2 \phi_2 + \epsilon^3 \phi_3 + \cdots
```

Taylor expand surface quantities about `z=0`:

```tex
\phi(x,\eta,t)
=
\phi(x,0,t)
+ \eta \phi_z(x,0,t)
+ \frac{1}{2}\eta^2\phi_{zz}(x,0,t)
+ \cdots
```

Visual anchor:

- The moving surface collapses to `z=0`.
- Successive correction terms appear as ordered layers.

Takeaway:

Perturbation theory turns one nonlinear free-boundary problem into a sequence of
fixed-boundary problems.

---

## Part 5: First Order And Linear Wave Theory

Goal: derive the linear theory checkpoint and the finite-depth dispersion
relation.

At first order, the free-surface conditions become:

```tex
\eta_{1t} = \phi_{1z}
\qquad \text{at } z=0
```

```tex
\phi_{1t} + g\eta_1 = 0
\qquad \text{at } z=0
```

The potential still satisfies:

```tex
\phi_{1xx} + \phi_{1zz} = 0,
\qquad
\phi_{1z}=0 \text{ at } z=-h
```

For a unidirectional sinusoidal mode:

```tex
\eta_1 = a\cos(kx-\omega t)
```

the dispersion relation is:

```tex
\omega^2 = gk\tanh(kh)
```

Visual anchor:

- A sinusoidal surface wave.
- A finite-depth vertical structure beneath it.
- A small dispersion panel showing that `omega` is tied to `k`.

Takeaway:

Linear theory gives independent free-wave components, each obeying the
finite-depth dispersion relation.

---

## Part 6: Second Order And The First Nonlinear Forcing

Goal: show where bound waves are born.

At second order, the unknowns `eta_2` and `phi_2` satisfy a linear
boundary-value problem, but the right-hand side is forced by products of
first-order fields.

Representative forcing terms include:

```tex
\eta_1 \phi_{1zz},
\qquad
\phi_{1x}\eta_{1x},
\qquad
\frac{1}{2}(\phi_{1x}^2+\phi_{1z}^2)
```

Key identity for a monochromatic wave:

```tex
\cos^2(kx-\omega t)
=
\frac{1}{2}
+ \frac{1}{2}\cos(2kx-2\omega t)
```

Visual anchor:

- Two first-order wave quantities multiply.
- A second harmonic appears from the product.
- The forcing arrows should point from first-order fields to second-order
  response.

Takeaway:

Second-order waves are forced by nonlinear products of the first-order wave
field.

---

## Part 7: Monochromatic Stokes Wave

Goal: introduce bound waves in the simplest setting.

Let:

```tex
\theta = kx-\omega t
```

Write the Stokes surface schematically as:

```tex
\eta
=
a\cos\theta
+ a^2 C_2(k,h)\cos(2\theta)
+ O(a^3)
```

The coefficient `C_2(k,h)` should remain symbolic until the preferred exact
form is supplied.

Physical meaning:

- The second harmonic sharpens crests and flattens troughs.
- Its phase is `2theta`, so it is locked to the primary wave.
- It is not an independently chosen free wave.

First definition:

```text
A bound wave is a nonlinear wave component forced by the primary wave field,
with phase and motion tied to that primary field rather than independently
prescribed as a free wave.
```

Visual anchor:

- Linear sine wave.
- Isolated second harmonic.
- Combined Stokes wave with sharper crests and flatter troughs.

Takeaway:

The monochromatic Stokes wave is the first clean example of a bound harmonic.

---

## Part 8: Higher-Order Stokes Theory Preview

Goal: show that the same perturbative logic continues without deriving every
order.

Show a symbolic expansion:

```tex
\eta
=
a\cos\theta
+ a^2 C_2\cos(2\theta)
+ a^3 C_3\cos(3\theta)
+ \cdots
```

Visual anchor:

- Add harmonics one by one.
- Show the profile becoming more asymmetric.

Takeaway:

Higher-order Stokes theory continues the same order-by-order construction:
collect nonlinear forcing terms, solve for the next correction, and recover a
more nonlinear wave shape.

---

## Part 9: From Stokes Wave To Wave Group

Goal: transition from one primary wave to a real unidirectional wave field.

A real unidirectional wave field is polychromatic:

```tex
\eta_1(x,t)
=
\sum_j a_j\cos(k_jx-\omega_jt+\alpha_j)
```

Contrast:

- A Stokes wave starts with one primary component and develops bound harmonics.
- A wave group starts with multiple primary free components.
- Nonlinear products among those components create bound sum and difference
  waves.

Visual anchor:

- A single Stokes wave profile on one side.
- A wave group formed from nearby free components on the other side.
- Keep both unidirectional.

Takeaway:

The Stokes wave teaches the mechanism; the wave group shows why bound waves
matter in realistic seas.

---

## Part 10: Two-Component Interaction Theory

Goal: prepare for the explicit analytical form of second-order wave interaction
theory.

Start with two linear components:

```tex
\eta_1
=
a_1\cos\theta_1
+ a_2\cos\theta_2
```

where:

```tex
\theta_i = k_i x-\omega_i t+\alpha_i
```

Products generate:

```tex
\cos\theta_1\cos\theta_2
=
\frac{1}{2}\cos(\theta_1+\theta_2)
+ \frac{1}{2}\cos(\theta_1-\theta_2)
```

Thus the second-order response contains sum and difference components:

```tex
k_1+k_2,\quad \omega_1+\omega_2
```

and:

```tex
k_1-k_2,\quad \omega_1-\omega_2
```

The coefficient form is intentionally left open until the preferred exact
interaction coefficients are supplied.

For the eventual derivation lecture, reserve space here to distinguish a
**forced second-order component** from a **free wave at the same wavenumber**.
The forced component inherits `(k_1\pm k_2,\omega_1\pm\omega_2)` from products
of first-order phases; a free component would have to satisfy the linear
dispersion relation at its own wavenumber.

Visual anchor:

- Spectral dots at `k_1` and `k_2`.
- New generated dots at `k_1+k_2` and `|k_1-k_2|`.
- A physical-space view showing group modulation.

Takeaway:

In a polychromatic wave field, bound waves are the forced sum and difference
components generated by pairs of first-order free waves.

---

## Part 11: Closing Conceptual Summary

Goal: close the loop from free-boundary equations to bound waves.

Summary chain:

```text
unknown free surface
-> nonlinear boundary conditions
-> small-amplitude expansion
-> linear free waves
-> second-order products
-> bound harmonics and bound interactions
```

Final message:

Bound waves are not added by hand. They are the natural second-order response of
the free-surface boundary conditions.

## Open Questions Before Implementation

- Which exact finite-depth Stokes coefficient should be used for `C_2(k,h)`?
- Which exact two-component interaction coefficient notation should be used?
- Should the lecture derive the second-order boundary conditions in full, or
  show only the terms needed to motivate the forcing structure?
- Should the eventual Manim implementation be a single long scene, multiple
  scenario files, or a future `manim-slides` deck?
