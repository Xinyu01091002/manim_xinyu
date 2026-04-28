# PhD Confirmation Render Log

## 2026-04-28

Finalized the S0-S5 Manim sequence with the new persistent two-tier navigation
bar and restrained text animation style.

### Navigation

- All scenarios now use `bottom_progress_nav` from `presentation_nav.py`.
- The top bar shows whole-talk progress across `S0`-`S5`.
- The lower bar shows subscenario progress inside the active scenario.
- The nav bar is built once and only fill widths / label opacities update per frame.
- `keep_nav` skips `ValueTracker` objects so scene clears do not accidentally fade out
  progress trackers.

### Animation Style

- Ordinary labels, titles, equations, and takeaways use quiet `FadeIn` / stable
  placement instead of distracting text animation.
- Visual animation effort is reserved for waves, spectra, probes, arrows, phase
  matching, kernel comparisons, and product/FFT structure.

### High-Quality Outputs

| Scenario | Scene | File | Duration |
| --- | --- | --- | ---: |
| S0 | `WhyNonlinearWaves` | `media/videos/scenario0_why_nonlinear/1080p60/WhyNonlinearWaves.mp4` | `00:00:52.15` |
| S1 | `BoundHarmonicsIntro` | `media/videos/scenario1_bound_harmonics/1080p60/BoundHarmonicsIntro.mp4` | `00:00:42.53` |
| S2 | `WhyExactInteractionsAreExpensive` | `media/videos/scenario2_exact_interactions/1080p60/WhyExactInteractionsAreExpensive.mp4` | `00:00:39.58` |
| S3 | `TheVWAIdea` | `media/videos/scenario3_vwa_structure/1080p60/TheVWAIdea.mp4` | `00:01:27.28` |
| S4 | `HigherOrderVWA` | `media/videos/scenario4_higher_order_vwa/1080p60/HigherOrderVWA.mp4` | `00:00:53.53` |
| S5 | `SurfaceKinematicsVWA` | `media/videos/scenario5_surface_kinematics/1080p60/SurfaceKinematicsVWA.mp4` | `00:00:30.00` |

Combined output:

- `media/videos/phd_confirmation_full_1080p60.mp4`
- Duration: `00:05:05.08`
- Size: about `40.7 MB`

### Verification

- `python -m py_compile` passed for `presentation_nav.py` and scenarios `0`-`5`.
- High-quality scenarios rendered with Manim `-qh`.
- S2 navigation timing was corrected to the high-quality duration and rerendered with
  `--disable_caching` before final merge.
- Final merge used ffmpeg concat with `-c copy` to avoid recompression.
