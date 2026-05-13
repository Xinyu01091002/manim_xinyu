# Governing Equations

## Assumptions

Use finite-depth, unidirectional potential-flow water waves.

The baseline assumptions are:

- incompressible fluid,
- inviscid flow,
- irrotational motion,
- constant density,
- flat impermeable bottom,
- free surface exposed to atmospheric pressure.

With irrotational flow, introduce a velocity potential:

```tex
u = \phi_x,\qquad w = \phi_z
```

Incompressibility gives Laplace's equation:

```tex
\phi_{xx}+\phi_{zz}=0
```

The fluid domain is:

```tex
-h \le z \le \eta(x,t)
```

## Bottom Boundary Condition

For a flat bottom at `z=-h`:

```tex
\phi_z = 0 \qquad \text{at } z=-h
```

Physical meaning:

The vertical velocity at the bed is zero, so fluid does not pass through the
bottom.

## Kinematic Free-Surface Condition

The free surface is:

```tex
F(x,z,t)=z-\eta(x,t)=0
```

Particles on the free surface remain on it:

```tex
\frac{DF}{Dt}=0
```

This gives:

```tex
\eta_t + \phi_x \eta_x = \phi_z
\qquad \text{at } z=\eta(x,t)
```

Physical meaning:

The surface moves with the fluid. Fluid particles do not cross the free surface.

## Dynamic Free-Surface Condition

Bernoulli's equation for unsteady potential flow gives:

```tex
\phi_t + \frac{1}{2}(\phi_x^2+\phi_z^2) + gz + \frac{p}{\rho} = C(t)
```

At the free surface, set pressure equal to atmospheric pressure and absorb the
time-only constant into the potential gauge. With `z=eta`:

```tex
\phi_t + \frac{1}{2}(\phi_x^2+\phi_z^2) + g\eta = 0
\qquad \text{at } z=\eta(x,t)
```

Physical meaning:

The pressure on the free surface balances atmospheric pressure.

## Why This Is A Free-Boundary Problem

The unknowns are:

```tex
\phi(x,z,t),\qquad \eta(x,t)
```

The boundary conditions for `eta` and `phi` are applied on:

```tex
z=\eta(x,t)
```

which is itself unknown. This coupling is the source of the free-boundary
nonlinearity.
