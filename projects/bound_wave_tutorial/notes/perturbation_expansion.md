# Perturbation Expansion

## Purpose

The perturbation expansion converts the nonlinear free-boundary problem into a
sequence of fixed-boundary problems posed at the still-water level `z=0`.

## Expansion

Introduce a small parameter:

```tex
\epsilon \ll 1
```

Expand the surface elevation and potential:

```tex
\eta = \epsilon \eta_1 + \epsilon^2\eta_2 + \epsilon^3\eta_3+\cdots
```

```tex
\phi = \epsilon \phi_1 + \epsilon^2\phi_2 + \epsilon^3\phi_3+\cdots
```

## Taylor Expansion About The Still-Water Level

For any surface quantity evaluated at `z=eta`, use:

```tex
f(x,\eta,t)
=
f(x,0,t)
+ \eta f_z(x,0,t)
+ \frac{1}{2}\eta^2 f_{zz}(x,0,t)
+ \cdots
```

This is the step that moves the boundary conditions from the unknown free
surface to the fixed plane `z=0`.

## First Order

At first order:

```tex
\eta_{1t} = \phi_{1z}
\qquad \text{at } z=0
```

```tex
\phi_{1t}+g\eta_1=0
\qquad \text{at } z=0
```

with:

```tex
\phi_{1xx}+\phi_{1zz}=0,
\qquad
\phi_{1z}=0 \text{ at } z=-h
```

A sinusoidal mode:

```tex
\eta_1=a\cos(kx-\omega t)
```

leads to the finite-depth dispersion relation:

```tex
\omega^2=gk\tanh(kh)
```

## Second Order

At second order, the equations for `eta_2` and `phi_2` are linear in the
second-order unknowns, but forced by products of first-order quantities.

Representative terms:

```tex
\eta_1\phi_{1zz},
\qquad
\phi_{1x}\eta_{1x},
\qquad
\eta_1\phi_{1tz},
\qquad
\frac{1}{2}(\phi_{1x}^2+\phi_{1z}^2)
```

This is the first point where bound waves naturally appear.
