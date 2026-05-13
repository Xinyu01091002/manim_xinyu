# Two-Component Second-Order Interactions

## Purpose

Extend the bound-wave idea from a monochromatic Stokes wave to a unidirectional
polychromatic wave field.

## Polychromatic Linear Field

The first-order wave field is:

```tex
\eta_1(x,t)
=
\sum_j a_j\cos(k_jx-\omega_jt+\alpha_j)
```

Each primary component obeys the finite-depth linear dispersion relation:

```tex
\omega_j^2 = gk_j\tanh(k_jh)
```

## Two-Component Case

Start with:

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

The important product identity is:

```tex
\cos\theta_1\cos\theta_2
=
\frac{1}{2}\cos(\theta_1+\theta_2)
+ \frac{1}{2}\cos(\theta_1-\theta_2)
```

## Sum And Difference Components

The second-order response contains forced components with:

```tex
k_1+k_2,\qquad \omega_1+\omega_2
```

and:

```tex
k_1-k_2,\qquad \omega_1-\omega_2
```

Use signed difference phases in the derivation, and use absolute wavenumber
only when drawing a one-sided spectrum.

For a larger spectrum, the same logic applies pairwise across components.

## Coefficients

Leave the exact coefficient notation open for now. The tutorial should later
insert the user's preferred exact analytical interaction coefficients.

Schematic form:

```tex
\eta_2
=
\sum_{i,j}
A_{ij}^{+}\cos(\theta_i+\theta_j)
+
A_{ij}^{-}\cos(\theta_i-\theta_j)
```

## Bound-Wave Interpretation

The sum and difference waves are bound components because they are forced by
the primary free-wave field. They inherit their phase from pairs of primary
components, rather than being independently chosen free waves.

## Visual Idea

Use two linked views:

1. Physical space: two waves form a group or modulation.
2. Spectral space: primary dots at `k_1`, `k_2`, with generated dots at
   `k_1+k_2` and `|k_1-k_2|`.
