# A note on finite depth second-order wave-wave interactions

J.F. Dalzell* 

5, Countryside Court, Silver Spring, MD 20905-4516, USA 

Received 2 December 1998; accepted 5 March 1999 

# Abstract

This note summarizes results which were obtained in an extension of existing deep-water wave-wave interaction theory to the second-order wave-wave interaction coefficients for finite depth. © 1999 Elsevier Science Ltd. All rights reserved. 

Keywords: Wave-wave interaction; Second-order; Finite depth; Set-down 

# Nomenclature

$a_{j}$ Amplitude of first-order wave $j$ 

$A_{ij}$ Undetermined coefficients in potential function. 

$A_{p}(\cdot)$ Sum frequency potential interaction coefficient. 

$A_{m}(\cdot)$ Difference frequency potential interaction coefficient. 

$B_{ij}$ Undetermined coefficients in elevation function. 

$B_{p}(\cdot)$ Sum frequency elevation interaction coefficient. 

$B_{m}(\cdot)$ Difference frequency elevation interaction coefficient. 

$g$ Gravitational constant. 

$h$ Fluid depth. 

$t$ Time. 

$u$ Vector velocity in the fluid. 

$x,y,z$ Coordinate system. 

$\bar{X}$ Vector position, $x - y$ plane. 

$\epsilon_{j}$ Arbitrary phase, wave $j$ 

$\zeta$ Free surface elevation. 

$\zeta_{l}$ Superposition of linear waves. 

$\kappa_{j}$ Vector wave number, wave $j$ 

$\mu_{j}$ Direction of propagation, wave $j$ 

$\phi$ Potential function. 

$\phi_l$ Superposition of linear potential functions. 

$\psi_{j}$ Phase function, wave $j$ $(\kappa_{j}\cdot \bar{X} -\omega_{j}t + \varepsilon_{j})$ 

$\omega_{j}$ Wave frequency, wave $j$ 

# 1. Introduction

The subject of the present note arose as a result of a brief 

inquiry into the magnitude and character of the "set-down" which should have been evident in the results of some experiments which involved laboratory generated irregular waves in rather shallow water. A search for analytical results for second-order, finite depth, wave-wave interaction coefficients turned up no specific formulae in the time available, and, as a consequence, a derivation of second-order wave-wave interaction coefficients for finite depth was undertaken. 

To obtain second-order wave-wave interaction coefficients, it suffices to consider the problem of two superimposed monochromatic wave trains. The basic approach to the problem was that of Longuet-Higgins [1] for the deep water problem. The most important difference of the present study from the early work of Longuet-Higgins is the employment of symbolic computations to cope with the welter of hyperbolic functions which arise immediately in finite depth problems. 

In the sections to follow, the derivation will be outlined, the final results stated, and the results of some rudimentary sanity checks will be given. 

# 2. Derivation

# 2.1. General equations

A body of water with depth, $h$ , and indefinite lateral extent is assumed. Locations within the fluid are defined using an $x, y, z$ coordinate system with the origin located on the undisturbed equilibrium free surface, and the $z$ coordinate is vertical, positive upwards. 

The dynamic position of the free surface will be denoted by $\zeta$ , the gravitational constant by $g$ , and time by $t$ . 

Irrotational, incompressible and inviscid flow is assumed. Accordingly, a potential, $\phi$ , is assumed to define the vector velocity in the fluid, $u = \nabla \phi$ , and satisfy 

$$
\nabla^ {2} \phi = 0 \tag {1}
$$

within the fluid. The bottom boundary condition is then 

$$
\frac {\partial \phi}{\partial z} = 0 \quad \text {o n} \quad z = - h. \tag {2}
$$

With the notation, 

$$
\left| u \right| ^ {2} = \left(\frac {\partial \phi}{\partial x}\right) ^ {2} + \left(\frac {\partial \phi}{\partial y}\right) ^ {2} + \left(\frac {\partial \phi}{\partial z}\right) ^ {2},
$$

and with the assumption of zero atmospheric pressure on the free surface, the exact dynamic boundary condition on the free surface is written: 

$$
g \zeta + \frac {\partial \phi}{\partial t} + \frac {1}{2} | u | ^ {2} = 0 \quad (\text {o n} z = \zeta). \tag {3}
$$

The requirement that a fluid particle on the free surface stay on the free surface results in the exact kinematic boundary condition on the free surface: 

$$
\frac {\partial \zeta}{\partial t} - \frac {\partial \phi}{\partial z} + \frac {\partial \phi}{\partial x} \frac {\partial \zeta}{\partial x} + \frac {\partial \phi}{\partial y} \frac {\partial \zeta}{\partial y} = 0 \quad (\text {o n} z = \zeta). \tag {4}
$$

The dynamic and kinematic boundary conditions, Eqs. (3) and (4), involve the potential on the unknown free surface. In order to obtain solutions, a conventional procedure (see e.g. Longuet-Higgins [1], Newman [2]) is to expand the boundary conditions in a Taylor's series about $z = 0$ , and seek solutions for $\phi$ and $\zeta$ which will satisfy the expanded boundary conditions to some pre-determined order. Expanding Eq. (3), and writing out the terms to second-order, the approximate dynamic boundary condition to be satisfied becomes: 

$$
g \zeta + \left\{\frac {\partial \phi}{\partial t} + \zeta \frac {\partial^ {2} \phi}{\partial z \partial t} \right\} + \left\{\frac {1}{2} | u | ^ {2} \right\} = 0 \quad (\text {o n} z = 0). \tag {5}
$$

A similar expansion of Eq. (4) results in the approximate kinematic boundary condition to second-order: 

$$
\frac {\partial \zeta}{\partial t} - \left\{\frac {\partial \phi}{\partial z} + \zeta \frac {\partial^ {2} \phi}{\partial z ^ {2}} \right\} + \left\{\frac {\partial \phi}{\partial x} \frac {\partial \zeta}{\partial x} + \frac {\partial \phi}{\partial y} \frac {\partial \zeta}{\partial y} \right\} = 0 \tag {6}
$$

(on $z = 0$ 

# 2.2. First-order wave definition

The present objective is to find the second-order interactions between two first-order (linear) waves in water of finite depth, $h$ . The first-order solutions are summarized as follows. 

The amplitudes of the two first-order waves will be denoted by $a_{j}, j = 1,2$ , their frequencies by $\omega_{j}, j = 1,2$ , and their vector wave numbers by $\kappa_{j}, j = 1,2$ . The notation, 

$\left|\kappa_{j}\right|$ will denote the corresponding scalar wave numbers. The two waves will be assumed to be propagating in directions $\mu_j, j = 1,2$ in the horizontal, $x - y$ plane, where in accordance with the right-hand rule, $\mu_{j}$ is measured positive in the counterclockwise direction looking down. Accordingly, the wave number components in the $x$ and $y$ directions in the horizontal plane are denoted by $\left|\kappa_{j}\right|\cos \mu_{j}$ and $\left|\kappa_{j}\right|\sin \mu_{j}$ respectively. 

It is convenient to define "phase functions", $\psi_j, j = 1,2,$ for each of the two waves; 

$$
\psi_ {j} = \kappa_ {j} \vec {X} - \omega_ {j} t + \varepsilon_ {j}, \tag {7}
$$

where $\vec{X}$ denotes a position vector in the $x - y$ plane, and $\epsilon_{j}$ denotes an arbitrary constant phase for zero time at the origin of the $x - y$ coordinate system. With these definitions, the wave elevation resulting from the linear superposition of the two waves in the $x - y$ plane is simply; 

$$
\zeta_ {l} = \sum_ {j = 1} ^ {2} a _ {j} \cos \psi_ {j}. \tag {8}
$$

From the solution of the linear boundary value problem, the dispersion relation in present notation is: 

$$
\omega_ {j} ^ {2} = g | \kappa_ {j} | \tanh  (| \kappa_ {j} | h). \tag {9}
$$

This relation is correct to the second-order according to the standard treatment of monochromatic second-order waves. 

Similarly, in the present notation the linearly superimposed potential function is: 

$$
\phi_ {l} = \sum_ {j = 1} ^ {2} a _ {j} \frac {g}{\omega_ {j}} \frac {\cosh \left\{\left| \kappa_ {j} \right| (z + h) \right\}}{\cosh \left\{\left| \kappa_ {j} \right| h \right\}} \sin \psi_ {j}. \tag {10}
$$

# 2.3. Form of second-order solutions

From the known solutions for infinite depth for second-order waves (Longuet-Higgins [1], Dalzell [3]), from the general characteristics of quadratic systems, and from Whitham's [4] discussion of the second-order Stokes expansion, the solution for the wave elevation is expected to be at most of the form: 

$$
\begin{array}{l} \zeta = \sum_ {j = 1} ^ {2} a _ {j} \cos \psi_ {j} + \sum_ {j = 1} ^ {2} a _ {j} ^ {2} B _ {j 0} + \sum_ {j = 1} ^ {2} a _ {j} ^ {2} B _ {j 2} \cos (2 \psi_ {j}) \\ + a _ {1} a _ {2} B _ {p} \cos (\psi_ {1} + \psi_ {2}) + a _ {1} a _ {2} B _ {m} \cos (\psi_ {1} - \psi_ {2}) \tag {11} \\ \end{array}
$$

where the “ $B$ ” coefficients are to-be-determined functions of the first-order wave numbers and frequencies. 

Similarly, the solution for the corresponding potential 

function is expected to be at most of the form: 

$$
\begin{array}{l} \phi = \sum_ {j = 1} ^ {2} a _ {j} A _ {j 1} \cosh \left\{\left| \kappa_ {j} \right| (z + h) \right\} \sin \psi_ {j} \\ + \sum_ {j = 1} ^ {2} a _ {j} ^ {2} A _ {j 0} t \\ + \sum_ {j = 1} ^ {2} a _ {j} ^ {2} A _ {j 2} \cosh \left\{2 \mid \kappa_ {j} \mid (z + h) \right\} \sin (2 \psi_ {j}) \\ + a _ {1} a _ {2} A _ {p} \cosh \left\{\left| \kappa_ {1} + \kappa_ {2} \right| (z + h) \right\} \sin \left(\psi_ {1} + \psi_ {2}\right) \\ + a _ {1} a _ {2} A _ {m} \cosh \left\{\left| \kappa_ {1} - \kappa_ {2} \right| (z + h) \right\} \sin \left(\psi_ {1} - \psi_ {2}\right), \tag {12} \\ \end{array}
$$

where the "A" coefficients are to-be-determined functions of the first-order wave numbers and frequencies. As required, this expression for the potential satisfies the Laplace equation, Eq. (1), and the bottom boundary condition, Eq. (2). 

Note that Eq. (11) represents a non-zero mean wave elevation if the coefficients $B_{j0}$ are not equal to zero, and that Eq. (12) represents a non-zero mean potential if the coefficients $A_{j0}$ are not zero. Whitham [4] points out in his discussion of the solution for the second-order Stokes wave for finite depth that the mean wave-elevation and the mean potential for the second-order Stokes wave cannot both be zero—and that one or the other must be non-zero. According to Whitham's treatment, if the mean elevation is zero, the potential must at least have a term proportional to $t$ , and this is the origin of the $A_{j0}t$ terms in Eq. (12). 

Thus, Eqs. (11) and (12) represent two possible solutions according to the decision either to allow the mean elevation to be zero and accept the non-zero potential (equivalent to setting $B_{j0} = 0$ for $j = 1,2$ ) or accepting a non-zero wave elevation (equivalent to setting $A_{j0} = 0$ for $j = 1,2$ ) where the corresponding potential terms would be zero. Though a solution for a non-zero mean wave elevation raises concerns about continuity in some applications, there is substantial precedent in the literature where a non-zero mean elevation has been called the "mean sea-level set-down" (Mei [5; Section 12.3]). 

# 2.4. Approach

The rest of the problem involves determining the undetermined coefficients of Eqs. (11) and (12) so that the second-order dynamic and kinematic boundary conditions, Eqs. (5) and (6), are satisfied. The brute force approach adopted is reasonably practical only with the aid of symbolic computation. In the present problem the software employed was Maple $\mathbf{V}^{\mathrm{TM}}$ [6,7]. The steps taken are outlined as follows: 

- Substitute Eqs. (11) and (12) as written into the left hand sides of the boundary conditions, Eqs. (5) and (6), and, once the partials are evaluated, set $z = 0$ . 

- The resulting expressions were regarded as polynomials in $a_1$ and $a_2$ . The coefficients of each of the powers and products of $a_1$ and $a_2$ were collected, and only the terms of first and second "order" were retained. In fact, the terms retained involved only $a_1$ , $a_2$ , $a_1^2$ , $a_2^2$ and $a_1a_2$ . 

- Each of the coefficients of the terms in the resulting expressions was in turn regarded as a function of the phase functions, $\psi_{1}$ and $\psi_{2}$ , and simplified to the extent possible. 

- The net result of the preceding operations on the left hand side of the dynamic boundary condition, Eq. (5), may be denoted by $D$ , and is of the following form: 

$$
\begin{array}{l} D = a _ {1} f _ {1 1} \left(A _ {1 1}\right) \cos \psi_ {1} + a _ {2} f _ {2 1} \left(A _ {2 1}\right) \cos \psi_ {2} \\ + a _ {1} ^ {2} f _ {1 0} \left(A _ {1 0}, B _ {1 0}, A _ {1 1}\right) + a _ {1} ^ {2} f _ {1 2} \left(A _ {1 2}, B _ {1 2}, A _ {1 1}\right) \cos 2 \psi_ {1} \\ + a _ {2} ^ {2} f _ {2 0} \left(A _ {2 0}, B _ {2 0}, A _ {2 1}\right) + a _ {2} ^ {2} f _ {2 2} \left(A _ {2 2}, B _ {2 2}, A _ {2 1}\right) \cos 2 \psi_ {2} \\ + a _ {1} a _ {2} f _ {p} \left(A _ {p}, B _ {p}, A _ {1 1}, A _ {2 1}\right) \cos \left(\psi_ {1} + \psi_ {2}\right) \\ + a _ {1} a _ {2} f _ {m} \left(A _ {m}, B _ {m}, A _ {1 1}, A _ {2 1}\right) \cos \left(\psi_ {1} - \psi_ {2}\right) \tag {13} \\ \end{array}
$$

where in addition to the unknowns, the functions, $f_{ij}(\cdot)$ involve only the wave numbers and frequencies of the assumed first-order waves. 

The result of similar operations on the left hand side of the kinematic boundary condition, Eq. (6), may be denoted by $K$ , and was of the following form: 

$$
\begin{array}{l} K = a _ {1} g _ {1 1} \left(A _ {1 1}\right) \sin \psi_ {1} + a _ {2} g _ {2 1} \left(A _ {2 1}\right) \sin \psi_ {2} \\ + a _ {1} ^ {2} g _ {1 2} \left(A _ {1 2}, B _ {1 2}, A _ {1 1}\right) \sin 2 \psi_ {1} \\ + a _ {2} ^ {2} g _ {2 2} \left(A _ {2 2}, B _ {2 2}, A _ {2 1}\right) \sin 2 \psi_ {2} \\ + a _ {1} a _ {2} g _ {p} \left(A _ {p}, B _ {p}, A _ {1 1}, A _ {2 1}\right) \sin \left(\psi_ {1} + \psi_ {2}\right) \\ + a _ {1} a _ {2} g _ {m} \left(A _ {m}, B _ {m}, A _ {1 1}, A _ {2 1}\right) \sin \left(\psi_ {1} - \psi_ {2}\right) \tag {14} \\ \end{array}
$$

Because neither the trigonometric functions or the amplitudes can be identically zero, the boundary conditions can only be satisfied if each of the functions $f_{ij}(\cdot)$ and $g_{ij}(\cdot)$ are identically equal to zero. Formally setting each of these functions to zero yields 14 equations in the 14 unknowns defined in Eqs. (11) and (12). 

- The unknowns $A_{j1}$ correspond to the linear problem for the two waves, and appear alone in the equations: $f_{j1}(\cdot) = 0$ and $g_{j1}(\cdot) = 0$ . As expected, these equations could only be satisfied if the dispersion relation, Eq. (9), was assumed, and the results for $A_{j1}$ were those implied by the equation for the linearly superimposed potential, Eq. (10). 

- Once $A_{11}$ and $A_{21}$ are known and substituted into the remaining 10 equations, there results an equation in $A_{10}$ 

and $B_{10}$ , an equation in $A_{20}$ and $B_{20}$ , and four pairs of equations in $(A_{12}, B_{12})$ , $(A_{22}, B_{22})$ , $(A_p, B_p)$ and $(A_m, B_m)$ . 

- The decision noted earlier about whether or not to accept a non-zero mean elevation determines whether to set $A_{10}$ and $A_{20}$ to zero and solve the two equations then involved for $B_{10}$ and $B_{20}$ , or the reverse. 

- Finally, the four pairs of equations for the remaining unknowns were straight forward (in Maple V) to solve and simplify to the point that the final simplification of results could be done in the old fashioned way. In this part of the procedure, the dispersion relation, Eq. (9), was taken to be accurate up to second-order and used freely in the simplification. 

# 3. Results

The final expression for the potential function, up to second-order, for the superposition of two waves becomes: 

$$
\begin{array}{l} \phi = \sum_ {j = 1} ^ {2} a _ {j} \frac {g}{\omega_ {j}} \frac {\cosh \left\{\left| \kappa_ {j} \right| (z + h) \right\}}{\cosh \left\{\left| \kappa_ {j} \right| h \right\}} \sin \psi_ {j} \\ + \sum_ {j = 1} ^ {2} a _ {j} ^ {2} \frac {3 \omega_ {j}}{8} \frac {\cosh \left\{2 \mid \kappa_ {j} \mid (z + h) \right\}}{\sinh^ {4} \left\{\mid \kappa_ {j} \mid h \right\}} \sin (2 \psi_ {j}) \\ + a _ {1} a _ {2} A _ {p} \left(\kappa_ {1}, \kappa_ {2}\right) \frac {\cosh \left\{\left| \kappa_ {1} + \kappa_ {2} \right| (z + h) \right\}}{\cosh \left\{\left| \kappa_ {1} + \kappa_ {2} \right| h \right\}} \sin \left(\psi_ {1} + \psi_ {2}\right) \\ + a _ {1} a _ {2} A _ {m} \left(\kappa_ {1}, \kappa_ {2}\right) \frac {\cosh \left\{\left| \kappa_ {1} - \kappa_ {2} \right| (z + h) \right\}}{\cosh \left\{\left| \kappa_ {1} - \kappa_ {2} \right| h \right\}} \sin \left(\psi_ {1} - \psi_ {2}\right). \tag {15} \\ \end{array}
$$

Similarly, the final expression for the wave elevation, up to second-order, for the superposition of two waves becomes: 

$$
\begin{array}{l} \zeta = \sum_ {j = 1} ^ {2} a _ {j} \cos \psi_ {j} \\ + \sum_ {j = 1} ^ {2} \frac {a _ {j} ^ {2} | \kappa_ {j} |}{4 \tanh (| \kappa_ {j} | h)} \bigg [ 2 + \frac {3}{\sinh^ {2} (| \kappa_ {j} | h)} \bigg ] \cos (2 \psi_ {j}) \\ - \sum_ {j = 1} ^ {2} \frac {a _ {j} ^ {2} | \kappa_ {j} |}{2 \sinh (2 | \kappa_ {j} | h)} + a _ {1} a _ {2} B _ {p} (\kappa_ {1}, \kappa_ {2}) \cos (\psi_ {1} + \psi_ {2}) \\ + a _ {1} a _ {2} B _ {m} \left(\kappa_ {1}, \kappa_ {2}\right) \cos \left(\psi_ {1} - \psi_ {2}\right). \tag {16} \\ \end{array}
$$

These solutions are obtained for the non-zero mean wave elevation case. It turns out that the zero mean wave decision affects only the constant terms in Eq. (16). Eqs. (15) and (16) may be turned into those appropriate for the zero mean wave elevation case by eliminating the constant terms in Eq. (16) and adding to Eq. (15) the term: 

$$
- \sum_ {j = 1} ^ {2} \frac {a _ {j} ^ {2} g | \kappa_ {j} | t}{2 \sinh (2 | \kappa_ {j} | h)}
$$

The results for the wave-wave interaction coefficients are completely unaffected by the choice for the mean values, and the results are as follows: 

$$
\begin{array}{l} A _ {p} (\kappa_ {1}, \kappa_ {2}) \\ = - \frac {\omega_ {1} \omega_ {2} \left(\omega_ {1} + \omega_ {2}\right)}{D _ {p} \left(\kappa_ {1} , \kappa_ {2}\right)} \left[ 1 - \frac {\cos \left(\mu_ {1} - \mu_ {2}\right)}{\tanh  \left(| \kappa_ {1} | h\right) \tanh  \left(| \kappa_ {2} | h\right)} \right] \tag {17} \\ + \frac {1}{2 D _ {p} \left(\kappa_ {1} , \kappa_ {2}\right)} \left[ \frac {\omega_ {1} ^ {3}}{\sinh^ {2} \left(\left| \kappa_ {1} \right| h\right)} + \frac {\omega_ {2} ^ {3}}{\sinh^ {2} \left(\left| \kappa_ {2} \right| h\right)} \right] \\ \end{array}
$$

$$
\begin{array}{l} A _ {m} (\kappa_ {1}, \kappa_ {2}) \\ = \frac {\omega_ {1} \omega_ {2} \left(\omega_ {1} - \omega_ {2}\right)}{D _ {m} \left(\kappa_ {1} , \kappa_ {2}\right)} \left[ 1 + \frac {\cos \left(\mu_ {1} - \mu_ {2}\right)}{\operatorname {t a n h} \left(| \kappa_ {1} | h\right) \operatorname {t a n h} \left(| \kappa_ {2} | h\right)} \right] \tag {18} \\ + \frac {1}{2 D _ {m} \left(\kappa_ {1} , \kappa_ {2}\right)} \left[ \frac {\omega_ {1} ^ {3}}{\sinh^ {2} \left(\left| \kappa_ {1} \right| h\right)} - \frac {\omega_ {2} ^ {3}}{\sinh^ {2} \left(\left| \kappa_ {2} \right| h\right)} \right] \\ \end{array}
$$

$$
\begin{array}{l} B _ {p} (\kappa_ {1}, \kappa_ {2}) \\ = \frac {\left(\omega_ {1} ^ {2} + \omega_ {2} ^ {2}\right)}{2 g} - \frac {\omega_ {1} \omega_ {2}}{2 g} \left[ 1 - \frac {\cos \left(\mu_ {1} - \mu_ {2}\right)}{\tanh  \left(| \kappa_ {1} | h\right) \tanh  \left(| \kappa_ {2} | h\right)} \right] \\ \times \left[ \frac {\left(\omega_ {1} + \omega_ {2}\right) ^ {2} + g \left| \kappa_ {1} + \kappa_ {2} \right| \tanh  \left(\left| \kappa_ {1} + \kappa_ {2} \right| h\right)}{D _ {p} \left(\kappa_ {1} , \kappa_ {2}\right)} \right] \tag {19} \\ + \frac {\left(\omega_ {1} + \omega_ {2}\right)}{2 g D _ {p} \left(\kappa_ {1} , \kappa_ {2}\right)} \left[ \frac {\omega_ {1} ^ {3}}{\sinh^ {2} \left(\left| \kappa_ {1} \right| h\right)} + \frac {\omega_ {2} ^ {3}}{\sinh^ {2} \left(\left| \kappa_ {2} \right| h\right)} \right] \\ \end{array}
$$

and 

$$
\begin{array}{l} B _ {m} (\kappa_ {1}, \kappa_ {2}) \\ = \frac {\left(\omega_ {1} ^ {2} + \omega_ {2} ^ {2}\right)}{2 g} + \frac {\omega_ {1} \omega_ {2}}{2 g} \left[ 1 + \frac {\cos \left(\mu_ {1} - \mu_ {2}\right)}{\tanh  \left(| \kappa_ {1} | h\right) \tanh  \left(| \kappa_ {2} | h\right)} \right] \\ \times \left[ \frac {\left(\omega_ {1} - \omega_ {2}\right) ^ {2} + g \left| \kappa_ {1} - \kappa_ {2} \right| \tanh  \left(\left| \kappa_ {1} - \kappa_ {2} \right| h\right)}{D _ {m} \left(\kappa_ {1} , \kappa_ {2}\right)} \right] \tag {20} \\ + \frac {(\omega_ {1} - \omega_ {2})}{2 g D _ {m} (\kappa_ {1} , \kappa_ {2})} \left[ \frac {\omega_ {1} ^ {3}}{\sinh^ {2} (| \kappa_ {1} | h)} - \frac {\omega_ {2} ^ {3}}{\sinh^ {2} (| \kappa_ {2} | h)} \right] \\ \end{array}
$$

with the functions, $D_{p}(\kappa_{1},\kappa_{2})$ and $D_{m}(\kappa_{1},\kappa_{2})$ defined by: 

$$
D _ {p} \left(\kappa_ {1}, \kappa_ {2}\right) = \left(\omega_ {1} + \omega_ {2}\right) ^ {2} - g \left| \kappa_ {1} + \kappa_ {2} \right| \tanh  \left(\left| \kappa_ {1} + \kappa_ {2} \right| h\right) \tag {21}
$$

and 

$$
D _ {m} \left(\kappa_ {1}, \kappa_ {2}\right) = \left(\omega_ {1} - \omega_ {2}\right) ^ {2} - g \left| \kappa_ {1} - \kappa_ {2} \right| \tanh  \left(\left| \kappa_ {1} - \kappa_ {2} \right| h\right). \tag {22}
$$

# 4. Discussion

As might have been expected from the way the problem was set up, the first four terms of the expression for the 

potential, Eq. (15), and the first six terms of the expression for the elevation, Eq. (16), represent a straight forward sum of the results for two second-order Stokes waves according to the results of Mei [5] where the non-zero mean wave elevation convention is followed. Eqs. (17)-(20) are the finite depth second-order wave-wave interaction coefficients sought. 

# 4.1. The deep-water result

If all is well with the present solution, it should reduce to the known results for deep water as $h \to \infty$ . The form of the solutions sufficiently parallels those for deep water so that no special tricks are necessary in carrying out the limit. Letting $h \to \infty$ in Eq. (15), the potential function, to second-order, for the superposition of two deep water waves becomes: 

$$
\begin{array}{l} \phi_ {d} = \sum_ {j = 1} ^ {2} a _ {j} \frac {g}{\omega_ {j}} \exp \left[ | \kappa_ {j} | z \right] \sin \psi_ {j} \\ + a _ {1} a _ {2} A _ {p} ^ {\infty} (\kappa_ {1}, \kappa_ {2}) \mathrm {e x p} [ | \kappa_ {1} + \kappa_ {2} | z ] \mathrm {s i n} (\psi_ {1} + \psi_ {2}) \\ + a _ {1} a _ {2} A _ {m} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) \exp \left[ \left| \kappa_ {1} - \kappa_ {2} \right| z \right] \sin \left(\psi_ {1} - \psi_ {2}\right) \tag {23} \\ \end{array}
$$

where $A_{p}^{\infty}(\kappa_{1},\kappa_{2})$ and $A_{m}^{\infty}(\kappa_{1},\kappa_{2})$ are the corresponding interaction coefficients for deep water, and the dispersion relation, Eq. (9) becomes $\omega_{j}^{2} = g|\kappa_{j}|$ . Similarly, letting $h\to \infty$ in Eq. (16), the wave elevation for the superposition of two deep water waves, up to second-order, becomes: 

$$
\begin{array}{l} \zeta_ {d} = \sum_ {j = 1} ^ {2} a _ {j} \cos \psi_ {j} + \sum_ {j = 1} ^ {2} \frac {a _ {j} ^ {2} | \kappa_ {j} |}{2} \cos (2 \psi_ {j}) \\ + a _ {1} a _ {2} B _ {p} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) \cos \left(\psi_ {1} + \psi_ {2}\right) + a _ {1} a _ {2} B _ {m} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) \cos \left(\psi_ {1} - \psi_ {2}\right) \tag {24} \\ \end{array}
$$

where $B_p^\infty(\kappa_1, \kappa_2)$ and $B_m^\infty(\kappa_1, \kappa_2)$ are the corresponding interaction coefficients for deep water. 

Letting $h \to \infty$ in Eqs. (17)-(20), the wave-wave interaction coefficients for deep water become, 

$$
A _ {p} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) = - \frac {\omega_ {1} \omega_ {2} \left(\omega_ {1} + \omega_ {2}\right) \left[ 1 - \cos \left(\mu_ {1} - \mu_ {2}\right) \right]}{\left(\omega_ {1} + \omega_ {2}\right) ^ {2} - g \left| \kappa_ {1} + \kappa_ {2} \right|}, \tag {25}
$$

$$
A _ {m} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) = \frac {\omega_ {1} \omega_ {2} \left(\omega_ {1} - \omega_ {2}\right) \left[ 1 + \cos \left(\mu_ {1} - \mu_ {2}\right) \right]}{\left(\omega_ {1} - \omega_ {2}\right) ^ {2} - g \left| \kappa_ {1} - \kappa_ {2} \right|}, \tag {26}
$$

$$
\begin{array}{l} B _ {p} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) = \frac {\left(\omega_ {1} ^ {2} + \omega_ {2} ^ {2}\right)}{2 g} - \frac {\omega_ {1} \omega_ {2}}{2 g} \left[ 1 - \cos \left(\mu_ {1} - \mu_ {2}\right) \right] \\ \times \left[ \frac {\left(\omega_ {1} + \omega_ {2}\right) ^ {2} + g \left| \kappa_ {1} + \kappa_ {2} \right|}{\left(\omega_ {1} + \omega_ {2}\right) ^ {2} - g \left| \kappa_ {1} + \kappa_ {2} \right|} \right] \tag {27} \\ \end{array}
$$

and 

$$
\begin{array}{l} B _ {m} ^ {\infty} \left(\kappa_ {1}, \kappa_ {2}\right) = \frac {\left(\omega_ {1} ^ {2} + \omega_ {2} ^ {2}\right)}{2 g} + \frac {\omega_ {1} \omega_ {2}}{2 g} \left[ 1 + \cos \left(\mu_ {1} - \mu_ {2}\right) \right] \\ \times \left[ \frac {\left(\omega_ {1} - \omega_ {2}\right) ^ {2} + g \left| \kappa_ {1} - \kappa_ {2} \right|}{\left(\omega_ {1} - \omega_ {2}\right) ^ {2} - g \left| \kappa_ {1} - \kappa_ {2} \right|} \right]. \tag {28} \\ \end{array}
$$

As would be hoped, the above expressions for $A_{p}^{\infty}(\kappa_{1},\kappa_{2})$ and $A_{m}^{\infty}(\kappa_{1},\kappa_{2})$ are those derived for deep water by Longuet-Higgins [1], and the expressions for $B_{p}^{\infty}(\kappa_{1},\kappa_{2})$ and $B_{m}^{\infty}(\kappa_{1},\kappa_{2})$ check with the result of a completion of the Longuet-Higgins derivation [3]. 

# 4.2. A limiting form: progressive waves

A further check on the results is that the limit, as one set of wave characteristics approach the other, should represent a single second-order progressive wave. For this exercise, it is first assumed that the wave directions are the same; that is, $\mu_{2} = \mu_{1}$ . No loss in generality results if in addition $\mu_{1}$ is assumed to be zero. Equivalently, with both directions the same, the vector wave numbers may be treated as scalars by a rotation of the coordinate system; that is, for these purposes $\kappa_{j} = k_{j}$ , and accordingly, $\omega_{j}^{2} = g k_{j} \tanh k_{j} h$ without loss in generality. 

Because of the negative sign in the function $D_{m}(\kappa_{1},\kappa_{2})$ Eq. (22), which appears in the denominator of $A_{m}$ , Eq. (18), the limit of $A_{m}$ must be taken. It needs to be assumed that $\omega_{1} > \omega_{2}$ before carrying out this limiting process; that is, that $\omega_{2}$ and $k_{2}$ approach $\omega_{1}$ and $k_{1}$ from below. In justification of this assumption, it is noted that no assumptions about the relative magnitudes of the two frequencies have been made in the original derivation, and it is evident from Eq. (22) that it is permissible to re-define the meaning of the indices at will. For this case, the limit involving $A_{m}$ becomes 

$$
\lim  _ {k _ {2} \rightarrow k _ {1}} \left[ \frac {A _ {m} \left(k _ {1} , k _ {2}\right)}{\cosh \left(\left| k _ {1} - k _ {2} \right| h\right)} \right] = 0. \tag {29}
$$

Substituting this limit into the corresponding part of Eq. (15), and letting $a_2 = a_1$ , $\psi_{2} = \psi_{1}$ , $\omega_{2} = \omega_{1}$ and $\kappa_{2} = \kappa_{1} = k_{1}$ in Eqs. (15) and (16) results in the following expressions for the progressive wave potential, $\phi_p$ , and wave elevation, $\zeta_p$ , 

$$
\begin{array}{l} \phi_ {p} = \left(2 a _ {1}\right) \frac {g}{\omega_ {1}} \frac {\cosh \left[ k _ {1} (z + h) \right]}{\cosh \left(k _ {1} h\right)} \sin \psi_ {1} \\ + \left(2 a _ {1}\right) ^ {2} \frac {3 \omega_ {1}}{8} \frac {\cosh \left[ 2 k _ {1} (z + h) \right]}{\sinh^ {4} \left(k _ {1} h\right)} \sin \left(2 \psi_ {1}\right), \tag {30} \\ \end{array}
$$

$$
\begin{array}{l} \zeta_ {p} = \left(2 a _ {1}\right) \cos \psi_ {1} - \frac {\left(2 a _ {1}\right) ^ {2} k _ {1}}{2 \sinh \left(2 k _ {1} h\right)} \\ + \frac {\left(2 a _ {1}\right) ^ {2} k _ {1}}{4 \tanh  \left(k _ {1} h\right)} \left[ 2 + \frac {3}{\sinh^ {2} \left(k _ {1} h\right)} \right] \cos (2 \psi_ {1}). \tag {31} \\ \end{array}
$$

As required, these expressions correspond to those which 

represent a single second-order Stokes wave with amplitude $2a_{1}$ according to the non-zero mean elevation convention, see Mei [5]. It should be noted that the limiting form will not be correct if the zero mean elevation convention is followed for the starting point, Eqs. (15) and (16). Though the second harmonic terms are correctly represented, in this latter case, the limiting forms of $A_{m}$ and $B_{m}$ can compensate only partially for the swapped constant terms. 

# 4.3. A limiting form: standing waves

A similar check on the results is that the superposition of two waves which propagate in opposite directions should result in a single, second-order standing wave. 

In this case it is first assumed that the wave directions differ by $\pi$ . No loss in generality results if $\mu_{1}$ is assumed to be zero and $\mu_{2}$ is assumed to be $\pi$ . As in the progressive wave case, and with these assumptions, the vector wave numbers become scalars. Except in the case of the wave-wave interaction term involving $A_{m}$ , letting $a_{2} = a_{1}$ , $\epsilon_{2} = \epsilon_{1} = 0$ , $\omega_{2} = \omega_{1}$ and $\kappa_{2} = \kappa_{1} = k_{1}$ in Eqs. (15) and (16) results in tractable expressions. For the standing wave case, the limiting form of $A_{m}$ is the same as that for the progressive wave case; that is: 

$$
\lim  _ {k _ {2} \rightarrow k _ {1}} [ A _ {m} (k _ {1}, k _ {2}) / \cosh (| k _ {1} - k _ {2} | h) ] = 0.
$$

With this limit and some manipulations the following expressions for the standing wave potential, $\phi_s$ , and the wave elevation, $\zeta_s$ are: 

$$
\begin{array}{l} \phi_ {s} = - \left(2 a _ {1}\right) \frac {g}{\omega_ {1}} \frac {\cosh \left[ k _ {1} (z + h) \right]}{\cosh \left(k _ {1} h\right)} \cos \left(k _ {1} x\right) \sin \left(\omega_ {1} t\right) \\ + \left(2 a _ {1}\right) ^ {2} \frac {\omega_ {1}}{1 6} \left[ 3 + \coth^ {2} \left(k _ {1} h\right) \right] \sin \left(2 \omega_ {1} t\right) \\ - \left(2 a _ {1}\right) ^ {2} \frac {3 \omega_ {1}}{1 6} \frac {\cosh \left[ 2 k _ {1} (z + h) \right]}{\sinh^ {4} \left(k _ {1} h\right)} \cos \left(2 k _ {1} x\right) \sin \left(2 \omega_ {1} t\right), \tag {32} \\ \end{array}
$$

$$
\begin{array}{l} \zeta_ {s} = \left(2 a _ {1}\right) \cos \left(k _ {1} x\right) \cos \left(\omega_ {1} t\right) - \frac {\left(2 a _ {1}\right) ^ {2} k _ {1}}{4 \sinh \left(2 k _ {1} h\right)} \\ + \frac {\left(2 a _ {1}\right) ^ {2}}{8} k _ {1} \tanh  (k _ {1} h) [ 1 + \coth^ {2} (k _ {1} h) ] \cos (2 k _ {1} x) \\ + \frac {\left(2 a _ {1}\right) ^ {2}}{8} k _ {1} \coth \left(k _ {1} h\right) \\ \times \left[ 3 \coth^ {2} \left(k _ {1} h\right) - 1 \right] \cos \left(2 k _ {1} x\right) \cos \left(2 \omega_ {1} t\right). \tag {33} \\ \end{array}
$$

The results clearly represent a standing wave of first-order amplitude $2a_{1}$ . In detail, they are closest to those reproduced by Wehausen and Laitone [8; Section 27, p. 666] for second-order standing waves. The only difference from [8] in the potential, $\phi_{s}$ , is the sign of the third term. Similarly, there is a difference from [8] in the sign of the fourth term of $\zeta_{s}$ . Evidently, the result in Wehausen and Laitone [8] was 

obtained under the zero mean elevation convention since the second term in $\zeta_s$ shown above, traceable to the constant term appearing in Eq. (16), does not appear in [8]. It is apparent from the presentation in Wiegel [9] that the various classical results for higher-order standing waves differ in a number of non-trivial ways, so that it is perhaps not too surprising that the results given here (Eqs. (32) and (33)) contain sign inversions relative to the corresponding expressions given by Wehausen and Laitone. It was found that the expressions given in Wehausen and Laitone [8] for the second-order standing wave in finite depth do not satisfy the second-order boundary conditions unless the terms noted above are changed to conform with the present results. Accordingly, the standing wave limit given here is assumed to represent a reasonable check that the interaction coefficients are of the correct form. 

# 4.4. Qualitative behavior of numerical simulations

It was finally of interest to carry out some numerical simulations of second-order irregular waves to check the qualitative nature of the solutions. 

Eqs. (15)-(22) are straight forward programming exercises for the superposition of two defined linear wave components. A simulation of irregular wave elevations defined by $N$ linear components involves a simple summation of $N$ second-order Stokes waves (the first three summations of Eq. (16) with $n = N$ instead of 2) along with the summation of the wave-wave interaction components for all possible pairs of the linear wave components. 

In order to ensure very long, or no, periodicity in the simulations, an incommensurate frequency approach to the definition of the linear components was adopted. In this approach, an hypothesized wave spectrum is divided into $N$ equi-energy bands, and the center frequencies of each band are taken to be the wave frequency of the corresponding component. When the water depth is known, the dispersion relation can be solved for the required wave number of each of the linear components. The amplitude of each of the linear components is made a constant such that the variance of the sum of all components equals the total wave elevation variance defined by the hypothesized wave spectrum. The phases of each linear component relative to the spatial and time origins are chosen randomly. For long-crested wave elevation simulations, the directions of all linear components are set equal to zero. For short-crested wave elevation simulations, a fairly crude approximation to a cosinesquared spreading function normalized over directions of $\pm \mu_{\mathrm{s}}$ is made by a systematic perturbation about zero of the directions of successive linear components. Starting with the five lowest frequency components, the directions are set equal to $-0.482\mu_{\mathrm{s}}$ , $-0.207\mu_{\mathrm{s}}$ , 0.0, $0.207\mu_{\mathrm{s}}$ and $0.482\mu_{\mathrm{s}}$ , and this sequence is repeated for each succeeding higher frequency group of 5 linear components. 

For the present study, 50-wave incommensurate frequency realizations of the JONSWAP spectrum with a 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-31/444bac4e-df10-40ab-85f2-978d75d5cd84/368c22ecebf7eeca7a071eecae01f5a109f969f45b492c974bdbcf593ba8a2b3.jpg)



(a) Long-crested, deep water


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-31/444bac4e-df10-40ab-85f2-978d75d5cd84/270ab7c79c1ae96614628514970e47f1d82fd697f95d2b4b254d00a4c8f2d51c.jpg)



(b) Long-crested, depth 15m


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-31/444bac4e-df10-40ab-85f2-978d75d5cd84/10dce7048bb8798be5cea07da30c4ea9208bfe155f9700270c743535a743cbde.jpg)



(c) Short-crested, depth 15m



Fig. 1. Samples of simulated irregular wave elevations and the sum of the low frequency second-order components (dashed).


modal period of $10\mathrm{~s~}$ and peak enhancement factor of $\gamma = 3.3$ were produced for various significant wave heights. Thus, including the mean values shown in Eq. (16), $N = 50$ defined linear components resulted in a total of $N(N + 2) = 2600$ linear and quadratic wave components in the sum which defines the wave elevation to second-order. In order to simulate the "set-down" which occasioned the present, work a summation was also made of all the second-order wave components whose frequency was less than the lowest of the defined linear wave component frequencies. 

Thirty-minute simulations were made at the origin of the wave field for a number of combinations of the free parameters, including the significant wave height, the water depth, short or long-crested waves, and the "seed" of the random number generator. If the random number generator seed is held constant, the qualitative nature of the simulated elevations appears the same regardless of the significant wave height, water depth or short or long-crestedness. 

Some short sections of three simulated wave elevations and the summations of the corresponding low frequency components are shown in Fig. 1. In the simulations of Fig. 1, the random number generator seed was constant, as was the significant wave height of $5\mathrm{m}$ . As may be seen from the figure, the three samples are qualitatively similar despite the 

fact that the sample (a) elevations are for long-crested deep water waves, the sample (b) elevations are for long-crested waves in water depth of $15\mathrm{m}$ , and the sample (c) elevations are for short-crested waves with $\mu_{\mathrm{s}} = 45^{\circ}$ in water depth of $15\mathrm{m}$ . 

The most basic qualitative feature which would be expected of the simulations to second-order is the asymmetry of crest and trough deviation from the mean. In general, the asymmetry grows stronger with significant height and, as is visible in the samples of Fig. 1, with decreasing water depth. The low frequency second-order response is expected to depress the mean free surface in regions of groups of exceptionally high waves. The qualitative indications of Fig. 1(a) and other simulations for the deep water case suggest that "set-down" should be small or nil for deep water waves of "practical" heights. Simulated instances of the expected "set-down" behavior started to appear as water depth was reduced toward $20\mathrm{m}$ . Fig. 1(b) for $15\mathrm{m}$ water depth is typical of the longer simulations, and indicates water depressions of the order of $1\mathrm{m}$ corresponding to the high groups of waves. Negligible, or slightly positive, fluctuations are observed elsewhere in the time series. The low frequency fluctuations of Fig. 1(c) are substantially reduced relative to the long-crested case (b) even though the spread of component directions is quite narrow (the range of directions of the individual linear wave components for this case was less than $\pm 22^{\circ}$ ). In general, it appears that the magnitude of "set-down" for a given significant height and water depth could be reduced substantially if the waves are short-crested. 

# References



[1] Longuet-Higgins MS. Resonant interactions between two trains of gravity waves. Journal of Fluid Mechanics 1962;12:321. 





[2] Newman JN. Marine hydrodynamics. Cambridge, MA: MIT Press, 1977. 





[3] Dalzell JF, Effect of short crested seas on quadratic response. DTNSRDC Report DTNSRDC-85/102, December 1985. 





[4] Whitham GB. Linear and nonlinear waves. New York: Wiley, 1974. 





[5] Mei CC. The applied dynamics of ocean surface waves. Singapore: World Scientific, 1989. 





[6] Char BW, Geddes KO, Gonnet GH, Leong BL, Monagan MB, Watt SM. Maple $\{\mathrm{V}\}$ : language reference manual. New York: Springer, 1991. 





[7] Redfern D. The Maple handbook: Maple $\{\mathrm{V}\}$ release 4. New York: Springer, 1996. 





[8] Wehausen JV, Laitone EV. Surface waves. In: Flügge S, editor. Encyclopedia of physics, 9. Berlin: Springer, 1960. 





[9] Wiegel RL. Oceanographical engineering. Englewood Cliffs, NJ: Prentice-Hall, 1964. 

