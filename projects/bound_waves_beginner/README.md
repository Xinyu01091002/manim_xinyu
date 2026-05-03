# Bound Waves Beginner Lecture Segment

This subproject is a planned Manim lecture segment for explaining bound waves to
a beginning PhD student who already knows the basics of potential flow.

The scope is finite-depth water waves throughout. Use
`\omega^2 = g k \tanh(kh)` as the linear dispersion relation, keep explicit
second-order Stokes coefficients, and avoid bridging into VWA or the other
research-presentation projects.

## Intended Audience

- Beginning PhD student in water waves / offshore hydrodynamics.
- Familiar with velocity potential, Laplace equation, and free-surface boundary
  conditions.
- Not yet comfortable with how nonlinear boundary conditions generate bound
  harmonics.

## Proposed Files

- `outline.md`: lecture narrative and scene plan.
- `common.py`: shared helpers once implementation starts.
- `scenario0_problem_setup.py`: finite-depth potential-flow problem.
- `scenario1_linear_solution.py`: linearization and dispersion.
- `scenario2_second_order_stokes.py`: perturbation expansion and finite-depth
  second-order Stokes correction.
- `scenario3_higher_order_pattern.py`: how the harmonic hierarchy continues.
- `scenario4_wave_groups.py`: multi-frequency wave groups.
- `scenario5_group_bound_waves.py`: sum- and difference-frequency bound waves.

## Style Notes

Use the restrained presentation style from the repository:

- quiet text entrances with `FadeIn`, `Write`, or direct placement
- stable equation layouts
- animation effort spent on the water-domain sketch, surface profile, Taylor
  expansion geometry, spectra, and pair-interaction diagrams
- no decorative motion unless it clarifies the physics

## Development Render Pattern

When scene files exist, render from this directory:

```powershell
cd projects/bound_waves_beginner
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim -ql scenario0_problem_setup.py FiniteDepthProblemSetup
```
