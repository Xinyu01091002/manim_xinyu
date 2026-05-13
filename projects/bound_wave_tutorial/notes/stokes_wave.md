# Monochromatic Stokes Wave

## Purpose

Use the monochromatic Stokes wave as the first concrete example of a bound
wave.

## First-Order Wave

Let:

```tex
\theta = kx-\omega t
```

The first-order free surface is:

```tex
\eta_1=a\cos\theta
```

with finite-depth dispersion:

```tex
\omega^2=gk\tanh(kh)
```

## Second-Order Mechanism

Nonlinear products of first-order terms create second harmonics. The key
trigonometric identity is:

```tex
\cos^2\theta
=
\frac{1}{2}
+ \frac{1}{2}\cos 2\theta
```

The second-order surface therefore includes a component at:

```tex
2k,\qquad 2\omega
```

## Schematic Surface Form

Keep the coefficient symbolic for now:

```tex
\eta
=
a\cos\theta
+ a^2 C_2(k,h)\cos 2\theta
+ O(a^3)
```

The exact preferred expression for `C_2(k,h)` should be supplied later.

## Bound-Wave Interpretation

The second harmonic is bound because:

- it is forced by the primary wave,
- its phase is `2theta`,
- it travels with the primary wave pattern,
- it is not independently specified as a free wave component.

The physical effect is crest sharpening and trough flattening.

## Higher-Order Preview

The same perturbative construction continues:

```tex
\eta
=
a\cos\theta
+ a^2 C_2\cos 2\theta
+ a^3 C_3\cos 3\theta
+ \cdots
```

The tutorial should show this only as a glimpse, not as a full derivation.
