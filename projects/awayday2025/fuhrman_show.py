from manim import *
import numpy as np

class FuhrmanShow(Scene):
    def construct(self):
        

        # Displaying the transformation from the long formula to the short formula
        long_formula = MathTex(r"""
        \begin{aligned}
        G_{n+m+p}=\Lambda_3[\bullet] \equiv & \frac{h^2}{4 \beta_{n+m+p}}\left(\alpha _ { n + m + p } \left(\omega_{1 n}\left(k_n \cdot k_m+k_n \cdot k_p+\kappa_n^2\right)\right.\right. \\
        & \left.+\omega_{1 m}\left(k_m \cdot k_n+k_m \cdot k_p+\kappa_m^2\right)+\omega_{1 p}\left(k_p \cdot k_n+k_p \cdot k_m+\kappa_p^2\right)\right) \\
        & +\gamma_{n+m+p}\left(\frac{g}{\omega_{1 n}}\left(\omega_{1 m} k_m \cdot k_n+\omega_{1 p} k_p \cdot k_n-\omega_{n+m+p} \kappa_n^2\right)\right. \\
        & +\frac{g}{\omega_{1 m}}\left(\omega_{1 n} k_n \cdot k_m+\omega_{1 p} k_p \cdot k_m-\omega_{n+m+p} \kappa_m^2\right) \\
        & \left.\left.+\frac{g}{\omega_{1 p}}\left(\omega_{1 n} k_n \cdot k_p+\omega_{1 m} k_m \cdot k_p-\omega_{n+m+p} \kappa_p^2\right)\right)\right) \\
        & -\frac{h F_{n+m}}{2 \beta_{n+m+p}}\left(\alpha_{n+m+p} \cosh \left(h \kappa_{n+m}\right)\left(k_n \cdot k_p+k_m \cdot k_p+\kappa_{n+m}^2\right)\right. \\
        & \left.+\gamma_{n+m+p}\left(\frac{g}{\omega_{1 p}}\left(k_n \cdot k_p+k_m \cdot k_p\right) \cosh \left(h \kappa_{n+m}\right)-\gamma_{n+m} \omega_{n+m+p}\right)\right) \\
        & -\frac{h F_{n+p}}{2 \beta_{n+m+p}}\left(\alpha_{n+m+p} \cosh \left(h \kappa_{n+p}\right)\left(k_n \cdot k_m+k_m \cdot k_p+\kappa_{n+p}^2\right)\right. \\
        & \left.+\gamma_{n+m+p}\left(\frac{g}{\omega_{1 m}}\left(k_n \cdot k_m+k_m \cdot k_p\right) \cosh \left(h \kappa_{n+p}\right)-\gamma_{n+p} \omega_{n+m+p}\right)\right) \\
        & -\frac{h F_{m+p}}{2 \beta_{n+m+p}}\left(\alpha_{n+m+p} \cosh \left(h \kappa_{m+p}\right)\left(k_n \cdot k_m+k_n \cdot k_p+\kappa_{m+p}^2\right)\right.
        \end{aligned}
        """)
        short_formula = MathTex(r"\eta^{(33)}=\frac{3}{8}(k*\eta^{(11)})^2 \cdot \eta^{(11)}")

        # Adjusting the size of both formulas
        long_formula.scale(0.4)
        short_formula.scale(1.5)

        # Adding the long formula first
        self.add(long_formula)
        self.wait(2)

        # Transforming to the short formula
        self.play(Transform(long_formula, short_formula))
        self.wait(2)
