royalsocietypublishing.org/journal/rspa 

# Research

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/2bd9e14ed1e46f9b25fb2df2e984392729f2ddb574839e7ad68ee23d1d2e9ec7.jpg)


Check for updates 

Cite this article: Zhao K, Liu PL-F. 2022 On 

Stokes wave solutions. Proc. R. Soc. A 478: 20210732. 

https://doi.org/10.1098/rspa.2021.0732 

Received: 14 September 2021 

Accepted: 14 December 2021 

# Subject Areas:

oceanography, ocean engineering, wave motion 

# Keywords:

Stokes waves, perturbation, nonlinear and dispersive waves 

# Author for correspondence:

Philip L.-F. Liu 

e-mail: philip.liu@nus.edu.sg 

Electronic supplementary material is available online at https://doi.org/10.6084/m9.figshare.c.5777469. 

# On Stokes wave solutions

Kuifeng Zhao<sup>1</sup> and Philip L.-F. Liu<sup>1,2,3,4</sup> 

$^{1}$ Department of Civil and Environmental Engineering, National University of Singapore, Singapore 117576, Republic of Singapore 

$^{2}$ School of Civil and Environmental Engineering, Cornell University, Ithaca, NY, USA 

$^{3}$ Institute of Hydrological and Oceanic Sciences, National Central University, Taoyuan City, 32001, Taiwan 

$^{4}$ Department of Hydraulic and Ocean Engineering, National Cheng Kung University, Tainan City, 70101, Taiwan 

KZ, 0000-0001-8159-870X; PL-FL, 0000-0002-2170-5507 

Using a perturbation method with the aid of MATLAB® Symbolic Toolbox, a new set of Stokes wave solutions, up to the fifth order, are derived. The new solutions are expressed in terms of free surface profile, velocity potential and wave celerity (or frequency dispersion relation). The solutions in the deep water limit are also deduced and discussed. The new solutions are compared with the existing solutions up to the fifth order. Differences appear among the existing and the present solutions, starting at the third order. The causes for the differences are identified. The characteristic differences were highlighted in the figures for high order solutions of Stokes waves. Numerical examples are provided to quantify the differences between the new fifth-order solutions and Fenton's, and Skjelbreia and Hendrickson's solutions. 

# 1. Introduction

In many ocean and coastal engineering applications, Stokes waves are considered as the design waves. Information on free surface profile, wave celerity and velocity field is necessary for further analysing wave-structure interactions and other coastal processes. 

The development of Stokes wave solutions has a long history. Stokes [1] presented a perturbation method to find solutions for periodic waves propagating in a constant depth. The free surface profile, velocity potential, and wave celerity are expanded in terms of a small amplitude parameter. Stokes showed that the first-order solutions are the same as those of Airy [2], in which the free surface profile and velocity potential 

are simple harmonic functions in time and the direction of wave propagation. The wave celerity depends on wavenumber, wave frequency and water depth, which is the linear frequency dispersion relation. Stokes then presented the second-order solutions in finite depth, which only contain a second harmonic component, suggesting that his coordinate system was set on the mean (averaged over a wave period) water level, which is different from the still water level (i.e. the water level in the absence of waves) by the amount of mean free surface set-down. More importantly, it was realized that up to the second order the linear frequency dispersion relation remains the same as that of the first-order solution. After deriving the second-order solutions, Stokes [1] remarked that 'there is no difficulty in proceeding to the higher orders of approximation, except what arises from the length of the formulae'. Indeed, Stokes [1] was able to provide the third-order solutions for the free surface profile and the corresponding velocity potential function in deep water (infinite depth). In the supplement to his original 1847 paper, Stokes [3] presented a different approach for obtaining perturbation solutions, in which the complex potential, consisting of the potential function as the real part and the stream function as the imaginary part, was solved. In the supplement [3], Stokes derived the fourth-order solutions for the free surface profile and the velocity potential function in infinite depth, and the third-order solutions in intermediate depth in implicit forms. 

Rayleigh [4] further studied the higher-order Stokes wave solutions in infinite depth, and Levi-Civita [5] provided a rigorous treatment of the perturbation expansions. Using a method similar to that of Levi-Civita [5], Struik [6] found the third-order Stokes wave solutions in intermediate depth. Several errors in Struik's paper were corrected by Hunt [7]. De [8] used Stokes' second method (i.e. solving the complex potential function) and obtained Stokes wave solutions up to the fifth order. On the other hand, Skjelbreia & Hendrickson [9] used Stokes' first method (i.e. solving the potential function) and presented their solutions up to the fifth order as well. 

Laitone [10] followed Stokes' first method [1] to obtain the third-order Stokes wave solutions in intermediate depth. Instead of fixing the coordinate on the mean water level, Laitone placed the coordinate on the still water level. Consequently, the mean free surface set-down showed up in his second-order free surface elevation solution because of the quadratic nonlinearity. This second-order and other higher-order mean free surface set-downs vanish in the deep water limit. At the same time, Laitone's solutions for the velocity potential, free surface profile and wave celerity are all expressed in terms of the still water depth, not the mean water depth. Both De [8] and Laitone [10] showed that the solutions using different coordinate systems can be converted from one to the other within the framework of the perturbation scheme. 

Fenton [11] derived the fifth-order Stokes wave solutions by hand in 1985, but later on he wrote a computer code using Maple® to check the hand-derivations (J. D. Fenton 2021, personal communication). Fenton's solutions were based on the steady-state stream function formulation in the coordinate system moving with the wave celerity whose origin was fixed on the bottom. Fenton's solutions were expressed in terms of the mean water depth. In the final presentation, the stream function was converted to the corresponding potential function. 

In his book, Dingemans [12] re-derived the third-order Stokes wave solutions with detailed explanations on the needs for expanding the wave frequency in perturbation series so as to avoid the secular solutions in the third-order potential function. The mean water depth was used in Dingemans' solutions. Examining Dingemans' derivation carefully, several typographical errors and missing terms have been discovered. In this paper, we shall first correct Dingemans' third-order solutions and then expand the derivation to the fifth order. 

Based on the literature review given above, the existing Stokes wave solutions can first be categorized by the solution approach and the definition of water depth used in the derivation. As shown in table 1, solution approaches include solving potential function (P), complex potential function (CP) or stream function (S). As for the water depth, some solutions are expressed in terms of mean water depth (MWL) and others in terms of still water depth (SWL). Finally, the existing Stokes wave solutions have been presented in two different formats. In group A, the final 


Table 1. Summary of various existing Stokes wave solutions and their approaches.


<table><tr><td>author</td><td>Stokes [1,3]</td><td>De [8]</td><td>Laitone [10]</td><td>S &amp; H [9]</td><td>Fenton [11]</td><td>Dingemans [12]</td></tr><tr><td>solutiona</td><td>P, CP</td><td>CP</td><td>P</td><td>P</td><td>S</td><td>P</td></tr><tr><td>water depthb</td><td>MWL</td><td>SWL, MWL</td><td>SWL</td><td>MWL</td><td>MWL</td><td>MWL</td></tr><tr><td>presentationc</td><td>group A, B</td><td>group A</td><td>group A</td><td>group B</td><td>group A</td><td>group A</td></tr></table>


aPotential function (P), complex potential function (CP) or stream function (S). 



bMean water depth (MWL) and still water depth (SWL). 



Group A: the final solutions are expressed in terms of the wave amplitude of the first-order and first harmonic and group B: the final solutions for the free surface elevation and the potential function are normalized by the amplitude of the first harmonic. 


solutions for the free surface profile and the potential function are expressed in terms of the wave amplitude of the first harmonic at the first order, while in group B the solutions are normalized by the amplitude of the first harmonic in the final solutions. In this paper, we shall show that these different presentations can be converted from one to the other approximately within the accuracy of the perturbation scheme. 

Using the Padé approximation with the aid of computer program (FORTRAN IV), Schwartz [13] and Cokelet [14] carried out Stokes wave solutions to very high order. Similarly, Dallaston & McCue [15] used the Maple® program to solve for the series solutions of Stokes waves, focusing on the amplitude and wave celerity near the limiting wave conditions. There are also other interesting aspects of Stokes waves that have been investigated by various researchers. For example, Longuet-Higgins [16] studied the integral properties of Stokes waves, including mean surface, mean velocity, momentum and mean energy flux; Crew & Trinh [17] presented the findings on the singularities of Stokes waves; and Zhong & Liao [18] made use of the homotopy analysis method and gained convergent results of limiting Stokes waves in arbitrary depth. These topics are, however, beyond the scope of the present paper. 

This paper has multiple objectives. The first objective is to correct Dingemans' [12] solutions at the third order and then extend the derivations to the fifth order. The second objective is to compare the present fifth-order Stokes wave solutions with the existing solutions and discuss the differences among them. The final objective is to illustrate how to use these solutions in different applications. In the following section, §2, the governing equation and boundary conditions for Stokes wave solutions are presented in terms of the velocity potential and the free surface profile. Following Dingemans [12], we introduce the perturbation expansions for the potential function, free surface profile and the wave frequency. The Taylor series expansions are also applied to the nonlinear free surface boundary conditions. In §3, we illustrate that the Stokes wave solutions at each order, up to the fifth order, can be obtained with the aid of MATLAB® Symbolic Toolbox. For brevity, the details of the derivations are presented in the electronic supplementary material and only the key results are provided in the main text. The final solutions of the fifth-order Stokes wave are summarized in the formats of group A and B (table 1). However, only the group A solutions are discussed in the main text, and the group B solutions are presented in the electronic supplementary material. Finally, the solutions in the deep water limit are presented. In §4, the present solutions for free surface profile, potential function and dispersion relation (wave celerity) are compared with various existing solutions in both intermediate and infinite water depth. Comparisons are conducted for both solution formats, groups A and B. In §4c, several numerical examples are presented to demonstrate quantitatively the differences between the present solutions and Fenton's solutions. Section 5 provides a summary of the findings in the paper with some additional concluding remarks. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/e415ff3528b45fddcbf4037856fe02334d8e65c876300926cca5425998f5eacd.jpg)



Figure 1. Sketch of different water depth definitions and coordinate systems used by different authors: (a) Stokes [1] and De [8], (b) Dingemans [12], Skjelbreia & Hendrickson [9], and present study, (c) Laitone [10] and (d) Fenton [11]. The scale of the free surface elevation has been exaggerated. (Online version in colour.)


# 2. Governing equations and boundary conditions

In this paper, we derive Stokes wave solutions in terms of free surface profile, $\eta (x,t)$ , velocity potential, $\phi (x,z,t)$ , and wave celerity, $c$ . As shown in figure 1, the coordinate system is fixed on the MWL with the $z$ -axis pointing upwards and the $x$ -axis pointing in the direction of wave propagation. Therefore, the 'mean water depth', $h$ , is used in the solutions. For continuity, the potential function satisfies the Laplace equation in the flow domain, i.e. 

$$
\frac {\partial^ {2} \phi}{\partial x ^ {2}} + \frac {\partial^ {2} \phi}{\partial z ^ {2}} = 0, \quad \text {i n} - \infty <   x <   \infty , - h <   z <   \eta (x, t). \tag {2.1}
$$

Along the sea bottom, $z = -h$ , the no-flux boundary condition must be satisfied: 

$$
\frac {\partial \phi}{\partial z} = 0, \quad \text {o n} z = - h. \tag {2.2}
$$

On the free surface, $z = \eta$ , the combined kinematic and dynamic free surface boundary condition (CKDFSBC) can be expressed as [12] 

$$
\frac {\partial^ {2} \phi}{\partial t ^ {2}} + g \frac {\partial \phi}{\partial z} + \left[ \frac {\partial}{\partial t} + \frac {1}{2} \left(\frac {\partial \phi}{\partial x} \frac {\partial}{\partial x} + \frac {\partial \phi}{\partial z} \frac {\partial}{\partial z}\right) \right] \left[ \left(\frac {\partial \phi}{\partial x}\right) ^ {2} + \left(\frac {\partial \phi}{\partial z}\right) ^ {2} \right] = 0, \quad \mathrm {a t} z = \eta , \tag {2.3}
$$

which is nonlinear and is applied on the boundary to be determined. Note that the atmospheric pressure has been assumed to be zero. 

Following Dingemans' approach [12], we seek for Stokes wave solutions in terms of free surface profile and velocity potential in the following perturbation forms: 

$$
\eta = \sum_ {m = 1} ^ {\infty} \varepsilon^ {m} \eta_ {m} (x, t) \tag {2.4}
$$

and 

$$
\phi = \sum_ {m = 1} ^ {\infty} \varepsilon^ {m} \phi_ {m} (x, z, t), \tag {2.5}
$$

in which $\varepsilon$ is an ordering parameter. In the final solutions, $\varepsilon$ is set to unity. 

The Stokes wave solutions are periodic in both time, $t$ , and the horizontal axis, $x$ . More specifically, we anticipate that the solutions can be expressed in terms of combinations of different harmonics, $\sin m\theta$ or $\cos m\theta$ , at different order, in which 

$$
\theta = k x - \omega t \quad \text {a n d} \quad c = \frac {\omega}{k} \tag {2.6}
$$

are the phase function and the wave celerity, respectively, with $k$ being the wavenumber and $\omega$ being the wave angular frequency. To ensure the solvability of the approach [12], the frequency 

or wave celerity needs to be expanded in the following forms as well: 

$$
\omega = \omega_ {0} \left(1 + \sum_ {m = 1} ^ {\infty} \varepsilon^ {2 m} \omega_ {2 m}\right) \tag {2.7}
$$

and 

$$
c ^ {2} = c _ {0} ^ {2} \left(1 + \sum_ {m = 1} ^ {\infty} \varepsilon^ {2 m} c _ {2 m} ^ {2}\right). \tag {2.8}
$$

In the present derivation, the first-order free surface profile is prescribed as a first harmonic function in which the wave amplitude is denoted as $a$ , i.e. 

$$
\eta_ {1} = a \cos \theta , \tag {2.9}
$$

where the angular frequency, $\omega$ , is related to the wave amplitude, wavenumber and water depth through the dispersion relation to be determined; either the angular frequency or the wavenumber should be specified. 

Since the leading order term of the free surface profile, $\eta$ , is of $O(\varepsilon)$ (see (2.4)) and is small, the CKDFSBC, (2.3), can be approximated by the Taylor series expansion as [12] 

$$
\sum_ {m = 0} ^ {\infty} \frac {\eta^ {m}}{m !} \frac {\partial^ {m}}{\partial z ^ {m}} \left\{\frac {\partial^ {2} \phi}{\partial t ^ {2}} + g \frac {\partial \phi}{\partial z} + \left[ \frac {\partial}{\partial t} + \frac {1}{2} \left(\frac {\partial \phi}{\partial x} \frac {\partial}{\partial x} + \frac {\partial \phi}{\partial z} \frac {\partial}{\partial z}\right) \right] \left[ \left(\frac {\partial \phi}{\partial x}\right) ^ {2} + \left(\frac {\partial \phi}{\partial z}\right) ^ {2} \right] \right\} = 0, \tag {2.10}
$$

which is applied on a known location, $z = 0$ . Since the frequency, $\omega$ , has been expanded in a power series of $\varepsilon$ in (2.7), we introduce a stretched time variable 

$$
\tau = \beta t, \quad \text {w i t h} \beta = 1 + \sum_ {m = 1} ^ {\infty} \varepsilon^ {2 m} \omega_ {2 m}. \tag {2.11}
$$

Thus, (2.10) can be expressed in terms of the new time variable as 

$$
\sum_ {m = 0} ^ {\infty} \frac {\eta^ {m}}{m !} \frac {\partial^ {m}}{\partial z ^ {m}} \left\{\beta^ {2} \frac {\partial^ {2} \phi}{\partial \tau^ {2}} + g \frac {\partial \phi}{\partial z} + \left[ \beta \frac {\partial}{\partial \tau} + \frac {1}{2} \left(\frac {\partial \phi}{\partial x} \frac {\partial}{\partial x} + \frac {\partial \phi}{\partial z} \frac {\partial}{\partial z}\right) \right] \left[ \left(\frac {\partial \phi}{\partial x}\right) ^ {2} + \left(\frac {\partial \phi}{\partial z}\right) ^ {2} \right] \right\} = 0, \tag {2.12}
$$

on $z = 0$ . Finally, the dynamic free surface boundary can also be expressed in the Taylor series form in terms of the stretched time variable, $\tau$ , as [12] 

$$
g \eta = - \sum_ {m = 0} ^ {\infty} \frac {\eta^ {m}}{m !} \frac {\partial^ {m}}{\partial z ^ {m}} \left\{\beta \frac {\partial \phi}{\partial \tau} + \frac {1}{2} \left[ \left(\frac {\partial \phi}{\partial x}\right) ^ {2} + \left(\frac {\partial \phi}{\partial z}\right) ^ {2} \right] \right\}, \quad \text {o n} z = 0. \tag {2.13}
$$

# 3. Fifth-order Stokes wave solutions

To find the Stokes wave solutions, the perturbation expansions for the free surface profile, (2.4), the velocity potential, (2.5), and the frequency, (2.7), are substituted into the governing equation, (2.1), and the boundary conditions, (2.2), (2.12) and (2.13), and the terms with the same order of $\varepsilon^m$ ( $m = 1, 2, \ldots$ ) are collected, forming the $m$ th order boundary value problem for $\eta_m$ , $\phi_m$ and $\omega_m$ . As stated in Stokes [1], the procedure in finding the solutions of higher order is straightforward, but very lengthy and tedious. Mistakes could be easily made if the operations are manipulated by 

hand. Here, we have used the MATLAB® Symbolic Toolbox to perform the necessary operations. The MATLAB code is provided in the electronic supplementary material. 

The first-order and second-order Stokes wave solutions are well known and can be found in most textbooks for water wave theories. The governing equation and boundary conditions for the third-order solutions can also be found in Dingemans [12]. However, we have identified some typographic errors in Dingemans' second-order solutions and a mistake in his third-order combined free surface boundary condition, resulting in incorrect third-order solutions. For clarity, the details of the procedure for deriving third-order solutions are given in the electronic supplementary material. We have also provided the information of the typographic errors and the mistake associated with Dingemans' derivation in the electronic supplementary material. 

In this section, we summarize the solutions up to fifth order and group them in terms of different harmonics. Thus, the velocity potential and free surface profile can be written in the following dimensionless form, respectively: 

$$
\begin{array}{l} \frac {\phi}{\omega_ {0} a / k} = \left(A _ {1 1} + k ^ {2} a ^ {2} A _ {3 1} + k ^ {4} a ^ {4} A _ {5 1}\right) \cosh k (z + h) \sin \theta \\ + k a \left(A _ {2 2} + k ^ {2} a ^ {2} A _ {4 2}\right) \cosh 2 k (z + h) \sin 2 \theta \\ + k ^ {2} a ^ {2} \left(A _ {3 3} + k ^ {2} a ^ {2} A _ {5 3}\right) \cosh 3 k (z + h) \sin 3 \theta + k ^ {3} a ^ {3} A _ {4 4} \cosh 4 k (z + h) \sin 4 \theta \\ + k ^ {4} a ^ {4} A _ {5 5} \cosh 5 k (z + h) \sin 5 \theta + \frac {1}{\sigma} \left(k a C _ {2} + k ^ {3} a ^ {3} C _ {4}\right) \omega_ {0} t, \tag {3.1} \\ \end{array}
$$

where 

$$
\begin{array}{l} \begin{array}{l} A _ {1 1} = \frac {1}{\sinh k h}, A _ {3 1} = A _ {5 1} = 0, \\ A _ {2 2} = \frac {3}{8 \sinh^ {4} k h}, A _ {4 2} = \frac {1 2 \alpha_ {1} ^ {4} + 2 2 \alpha_ {1} ^ {3} - 8 4 \alpha_ {1} ^ {2} - 1 3 5 \alpha_ {1} + 1 0 4}{2 4 (\alpha_ {1} - 1) ^ {5}}, \end{array} \\ A _ {3 3} = \frac {9 - 4 \sinh^ {2} k h}{6 4 \sinh^ {7} k h}, \\ A _ {5 3} = \frac {8 \alpha_ {1} ^ {6} + 1 3 8 \alpha_ {1} ^ {5} + 3 8 4 \alpha_ {1} ^ {4} - 5 6 8 \alpha_ {1} ^ {3} - 2 3 8 8 \alpha_ {1} ^ {2} + 2 3 7 \alpha_ {1} + 9 7 4}{6 4 (\alpha_ {1} - 1) ^ {6} (3 \alpha_ {1} + 2) \sinh k h}, \tag {3.2} \\ A _ {4 4} = \frac {1 0 \alpha_ {1} ^ {3} - 1 7 4 \alpha_ {1} ^ {2} + 2 9 1 \alpha_ {1} + 2 7 8}{4 8 (3 \alpha_ {1} + 2) (\alpha_ {1} - 1) ^ {5}}, \\ A _ {5 5} = \frac {- 6 \alpha_ {1} ^ {5} + 2 7 2 \alpha_ {1} ^ {4} - 1 5 5 2 \alpha_ {1} ^ {3} + 8 5 2 \alpha_ {1} ^ {2} + 2 0 2 9 \alpha_ {1} + 4 3 0}{6 4 (\alpha_ {1} - 1) ^ {6} (3 \alpha_ {1} + 2) (4 \alpha_ {1} + 1) \sinh k h}, \\ C _ {2} = \frac {\sigma^ {2} - 1}{4 \sigma} \\ \end{array}
$$

and $C_4 = \frac{-9}{4(\alpha_1 - 1)^3\sinh 2kh}$ 

and 

$$
\begin{array}{l} \frac {\eta}{a} = \left(1 + k ^ {2} a ^ {2} B _ {3 1} + k ^ {4} a ^ {4} B _ {5 1}\right) \cos \theta + k a \left(B _ {2 2} + k ^ {2} a ^ {2} B _ {4 2}\right) \cos 2 \theta \\ + k ^ {2} a ^ {2} \left(B _ {3 3} + k ^ {2} a ^ {2} B _ {5 3}\right) \cos 3 \theta + k ^ {3} a ^ {3} B _ {4 4} \cos 4 \theta + k ^ {4} a ^ {4} B _ {5 5} \cos 5 \theta , \tag {3.3} \\ \end{array}
$$

where 

$$
B _ {3 1} = \frac {3 + 8 \sigma^ {2} - 9 \sigma^ {4}}{1 6 \sigma^ {4}},
$$

$$
B _ {5 1} = \frac {1 2 1 \alpha_ {1} ^ {5} + 2 6 3 \alpha_ {1} ^ {4} + 3 7 6 \alpha_ {1} ^ {3} - 1 9 9 9 \alpha_ {1} ^ {2} + 2 5 0 9 \alpha_ {1} - 1 1 0 8}{1 9 2 (\alpha_ {1} - 1) ^ {5}},
$$

$$
B _ {2 2} = \frac {3 - \sigma^ {2}}{4 \sigma^ {3}}, B _ {4 2} = \frac {6 0 \alpha_ {1} ^ {6} + 2 3 2 \alpha_ {1} ^ {5} - 1 1 8 \alpha_ {1} ^ {4} - 9 8 9 \alpha_ {1} ^ {3} - 6 0 7 \alpha_ {1} ^ {2} + 3 5 2 \alpha_ {1} + 2 6 0}{2 4 (3 \alpha_ {1} + 2) (\alpha_ {1} - 1) ^ {4} \sinh 2 k h},
$$

$$
B _ {3 3} = \frac {2 7 - 9 \sigma^ {2} + 9 \sigma^ {4} - 3 \sigma^ {6}}{6 4 \sigma^ {6}},
$$

$$
B _ {5 3} = \frac {9 (5 7 \alpha_ {1} ^ {7} + 2 0 4 \alpha_ {1} ^ {6} - 5 3 \alpha_ {1} ^ {5} - 7 8 2 \alpha_ {1} ^ {4} - 7 4 1 \alpha_ {1} ^ {3} - 5 2 \alpha_ {1} ^ {2} + 3 7 1 \alpha_ {1} + 1 8 6)}{1 2 8 (\alpha_ {1} - 1) ^ {6} (3 \alpha_ {1} + 2)},
$$

$$
B _ {4 4} = \frac {2 4 \alpha_ {1} ^ {6} + 1 1 6 \alpha_ {1} ^ {5} + 2 1 4 \alpha_ {1} ^ {4} + 1 8 8 \alpha_ {1} ^ {3} + 1 3 3 \alpha_ {1} ^ {2} + 1 0 1 \alpha_ {1} + 3 4}{2 4 (3 \alpha_ {1} + 2) (\alpha_ {1} - 1) ^ {4} \sinh 2 k h}
$$

and $B_{55} = \frac{5(300\alpha_1^8 + 1579\alpha_1^7 + 3176\alpha_1^6 + 2949\alpha_1^5 + 1188\alpha_1^4 + 675\alpha_1^3 + 1326\alpha_1^2 + 827\alpha_1 + 130)}{384(\alpha_1 - 1)^6(12\alpha_1^2 + 11\alpha_1 + 2)},$ (3.4) 

in which 

$$
\omega_ {0} = \sqrt {g k \sigma}, \quad \sigma = \tanh  k h, \quad \alpha_ {1} = \cosh 2 k h = \frac {1 + \sigma^ {2}}{1 - \sigma^ {2}}, \tag {3.5}
$$

and the wavenumber $k$ needs to be determined from the dispersion relation, which will be discussed later. 

Clearly, in the free surface expression the fifth-order solutions contribute to the first and third harmonics, while the fourth-order solution contributes to the second harmonic. However, in the potential function, the first harmonic only contains the first-order solution, i.e. $A_{31} = A_{51} = 0$ . This is the direct result of removing the secular terms appearing in the third-order and fifth-order governing equations. This procedure also determines the higher-order contributions to the dispersion relation, i.e. the expressions for $\omega_{2}$ and $\omega_{4}$ . The details can be found in the electronic supplementary material. We reiterate that since the water depth employed in the present derivation is the mean water depth, the mean sea level, $\overline{\eta} = 0$ . The difference between the still water depth and mean water depth represents the mean free surface set-down, i.e. $h - d = -C_2 / g - C_4 / g$ , which can be explicitly expressed as 

$$
h - d = - k a ^ {2} \frac {\sigma^ {2} - 1}{4 \sigma} + k ^ {3} a ^ {4} \left[ \frac {9}{4 (\alpha_ {1} - 1) ^ {3} \sinh 2 k h} \right]. \tag {3.6}
$$

The mean free surface set-down vanishes in the deep water limit, $kh \to \infty$ . 

Finally, the dispersion relation, up to the fifth order, can be organized into the following form: 

$$
\left. \begin{array}{l} \frac {\omega}{\omega_ {0}} = 1 + k ^ {2} a ^ {2} \omega_ {2} + k ^ {4} a ^ {4} \omega_ {4}, \\ \omega_ {0} = \sqrt {g k \sigma}, \quad \omega_ {2} = \frac {2 \alpha_ {1} ^ {2} + 7}{4 (\alpha_ {1} - 1) ^ {2}} \\ \omega_ {4} = \frac {2 0 \alpha_ {1} ^ {5} + 1 1 2 \alpha_ {1} ^ {4} - 1 0 0 \alpha_ {1} ^ {3} - 6 8 \alpha_ {1} ^ {2} - 2 1 1 \alpha_ {1} + 3 2 8}{3 2 (\alpha_ {1} - 1) ^ {5}}. \end{array} \right\} \tag {3.7}
$$

As indicated before, the perturbation expansion for the wave frequency is necessary for eliminating the secular terms in the third-order and fifth-order governing equations. Physically, it means that the wave celerity (and the wavenumber) depends not only on the frequency but also on the wave amplitude. Thus, if $a$ and $k$ are known, the dispersion relation given above can be used to calculate $\omega$ directly. However, if $a$ and $\omega$ are prescribed, the dispersion relation is a 

transcendental function for $k$ . Once $k$ is known, the free surface profile and the potential function are completely determined. 

From a user's point of view, it might be more practical to specify the wave height of the free surface profile according to the final solution, i.e. $H = [\eta(\theta = 0) - \eta(\theta = \pi)]$ . In other words, $H$ is given, but $a$ is not. From (3.3), we obtain 

$$
\frac {H}{2 a} = 1 + \left(B _ {3 1} + B _ {3 3}\right) k ^ {2} a ^ {2} + \left(B _ {5 1} + B _ {5 3} + B _ {5 5}\right) k ^ {4} a ^ {4}. \tag {3.8}
$$

It is clear that $a$ is not equal to $H / 2$ . The dispersion relation, (3.7), and the wave height equation above must be solved simultaneously for $a$ and $k$ , when $H$ and $\omega$ are prescribed. In certain other applications, it might be desirable to specify the wave amplitude of the first harmonic in the final solution. In other words, from (3.3) 

$$
\tilde {a} = a \left(1 + k ^ {2} a ^ {2} B _ {3 1} + k ^ {4} a ^ {4} B _ {5 1}\right) \tag {3.9}
$$

is prescribed instead of $a$ . In this situation, the dispersion relation, (3.7), must be solved together with the equation above to determine the corresponding $a$ and $k$ . 

The fluid particle velocity components can be calculated by taking the spatial derivatives of the potential function $\phi$ . In the electronic supplementary material, a MATLAB program code for calculating $\eta, \phi$ , and the corresponding velocity components is presented. Separate MATLAB functions for solving the dispersion relationship, (3.7), coupled with either (3.8) or (3.9) are also provided. 

# (a) Fifth-order Stokes wave solutions in deep water

The Stokes wave solutions in deep water can be obtained by taking the limit, $kh\to \infty$ , of the intermediate water depth solutions presented in the previous section. The resulting free surface profile takes the following form: 

$$
\begin{array}{l} {\frac {\eta}{a}} = \left(1 + {\frac {1}{8}} k ^ {2} a ^ {2} + {\frac {1 2 1}{1 9 2}} k ^ {4} a ^ {4}\right) \cos \theta + \left({\frac {1}{2}} k a + {\frac {5}{6}} k ^ {3} a ^ {3}\right) \cos 2 \theta \\ + \left(\frac {3}{8} k ^ {2} a ^ {2} + \frac {1 7 1}{1 2 8} k ^ {4} a ^ {4}\right) \cos 3 \theta + \frac {1}{3} k ^ {3} a ^ {3} \cos 4 \theta + \frac {1 2 5}{3 8 4} k ^ {4} a ^ {4} \cos 5 \theta . (3. 1 0) \\ \end{array}
$$

Similarly, the potential function solution in the deep water can be expressed as 

$$
\frac {\phi}{\omega_ {0} a / k} = \mathrm {e} ^ {k z} \sin \theta + \frac {1}{2} k ^ {3} a ^ {3} \mathrm {e} ^ {2 k z} \sin 2 \theta + \frac {1}{1 2} k ^ {4} a ^ {4} \mathrm {e} ^ {3 k z} \sin 3 \theta . \tag {3.11}
$$

It is interesting to point out that while the free surface profiles contain the fourth and fifth harmonics, the potential functions do not. The dispersion relation in deep water becomes 

$$
\frac {\omega}{\omega_ {0}} = 1 + \frac {1}{2} k ^ {2} a ^ {2} + \frac {5}{8} k ^ {4} a ^ {4}, \tag {3.12}
$$

in terms of $a$ . Finally, the corresponding wave height expressions in the deep water limit can be deduced from (3.8) as 

$$
\frac {H}{2 a} = 1 + \frac {1}{2} k ^ {2} a ^ {2} + \frac {5 5}{2 4} k ^ {4} a ^ {4}. \tag {3.13}
$$

# 4. Comparisons between present and existing Stokes wave solutions

Up to the third order, our solutions are identical to those of Laitone [10]. In this section, we shall focus on comparing the present fifth-order solutions in the intermediate water depth with those of Skjelbreia & Hendrickson [9] and Fenton [11]. The comparisons for the deep water solutions will then follow. 

# (a) Intermediate water depth

Fenton [11] derived stream function solutions in the moving coordinate that moved with the wave celerity of the final solution. He converted the stream function solutions to the corresponding velocity potential function solutions, which were presented together with free surface profile, and dispersion relation (see also (4.1), (4.3) and (4.5), respectively, below in the reformed form). The relationship between the potential function and stream function is well known: $\partial \phi / \partial x = \partial \psi / \partial z$ and $\partial \phi / \partial z = -\partial \psi / \partial z$ , implying that the stream function and potential function have the one-to-one correspondence in harmonics. To make the direct comparisons between present and Fenton's solutions, we have reorganized Fenton's solutions in the same forms with the same symbols as those shown in (3.1), (3.3) and (3.7). The conversions of Fenton's solutions to the present solution forms are straightforward using hyperbolic function identities. We have included the conversion process in the electronic supplementary material. 

When Fenton's potential function solutions are converted into the same form as that shown in (3.1), some of the coefficients in front of different harmonics are different from those in the present solutions. For completeness and clarity, all of them are listed here: 

$$
\left. \begin{array}{l} (A _ {1 1}) ^ {F} = \frac {1}{\sinh k h}, \quad (A _ {3 1}) ^ {F} = - \frac {4 \alpha_ {1} ^ {3} + 2 0 \alpha_ {1} ^ {2} - 1 0 \alpha_ {1} + 1 3}{6 4 \sinh^ {7} k h}, \\ (A _ {5 1}) ^ {F} = \frac {- 1 1 8 4 \alpha_ {1} ^ {8} + 3 2 \alpha_ {1} ^ {7} + 1 3 2 3 2 \alpha_ {1} ^ {6} + 2 1 7 1 2 \alpha_ {1} ^ {5} + 2 0 9 4 0 \alpha_ {1} ^ {4} + 1 2 5 5 4 \alpha_ {1} ^ {3} - 5 0 0 \alpha_ {1} ^ {2} - 3 3 4 1 \alpha_ {1} - 6 7 0}{4 0 9 6 (1 2 \alpha_ {1} ^ {2} + 1 1 \alpha_ {1} + 2) \sinh^ {1 3} k h}, \\ (A _ {2 2}) ^ {F} = \frac {3}{8 \sinh^ {4} k h}, \quad (A _ {4 2}) ^ {F} = \frac {1 2 \alpha_ {1} ^ {4} - 1 4 \alpha_ {1} ^ {3} - 2 6 4 \alpha_ {1} ^ {2} - 4 5 \alpha_ {1} - 1 3}{2 4 (\alpha_ {1} - 1) ^ {5}}, \\ (A _ {3 3}) ^ {F} = - \frac {2 \cosh 2 k h - 1 1}{6 4 \sinh^ {7} k h}, \\ (A _ {5 3}) ^ {F} = \frac {4 \alpha_ {1} ^ {6} + 1 0 5 \alpha_ {1} ^ {5} + 1 9 8 \alpha_ {1} ^ {4} - 1 3 7 6 \alpha_ {1} ^ {3} - 1 3 0 2 \alpha_ {1} ^ {2} - 1 1 7 \alpha_ {1} + 5 8}{3 2 (3 \alpha_ {1} + 2) (\alpha_ {1} - 1) ^ {6} \sinh k h}, \\ (A _ {4 4}) ^ {F} = \frac {1 0 \alpha_ {1} ^ {3} - 1 7 4 \alpha_ {1} ^ {2} + 2 9 1 \alpha_ {1} + 2 7 8}{4 8 (3 \alpha_ {1} + 2) (\alpha_ {1} - 1) ^ {5}} \\ (A _ {5 5}) ^ {F} = \frac {- 6 \alpha_ {1} ^ {5} + 2 7 2 \alpha_ {1} ^ {4} - 1 5 5 2 \alpha_ {1} ^ {3} + 8 5 2 \alpha_ {1} ^ {2} + 2 0 2 9 \alpha_ {1} + 4 3 0}{6 4 (\alpha_ {1} - 1) ^ {6} (3 \alpha_ {1} + 2) (4 \alpha_ {1} + 1) \sinh k h}, \end{array} \right\} \tag {4.1}
$$

where the superscript, $(\mathbf{\Lambda})^F$ , denotes the coefficients for Fenton's solutions. The mean free surface set-down is also zero in Fenton's solution, which is accomplished by adjusting the Bernoulli constant, $R$ , in his derivation. The Bernoulli constant is equivalent to $C_2$ and $C_4$ in the present study. The equivalent $(C_2)^F$ and $(C_4)^F$ can be expressed as 

$$
\left. \begin{array}{l} (C _ {2}) ^ {F} = \frac {2 \alpha_ {1} ^ {2} + 2 \alpha_ {1} + 5}{4 (\alpha_ {1} - 1) \sinh 2 k h} = \frac {9 - 6 \sigma^ {2} + 5 \sigma^ {4}}{1 6 \sigma^ {3}} \\ (C _ {4}) ^ {F} = \frac {8 \alpha_ {1} ^ {5} + 1 2 \alpha_ {1} ^ {4} - 1 5 2 \alpha_ {1} ^ {3} - 3 0 8 \alpha_ {1} ^ {2} - 4 2 \alpha_ {1} + 7 7}{3 2 (\alpha_ {1} - 1) ^ {4} \sinh 2 k h}. \end{array} \right\} \tag {4.2}
$$

When Fenton's free surface profile is expressed in the form of (3.3), the coefficients in front of each harmonic can be expressed as 

$$
\left. \begin{array}{l} \left(B _ {3 1}\right) ^ {F} = - \left(B _ {3 3}\right) ^ {F} = - \frac {3 \left(\alpha_ {1} ^ {3} + 3 \alpha_ {1} ^ {2} + 3 \alpha_ {1} + 2\right)}{8 \left(\alpha_ {1} - 1\right) ^ {3}} = - \frac {2 7 - 9 \sigma^ {2} + 9 \sigma^ {4} - 3 \sigma^ {6}}{6 4 \sigma^ {6}}, \\ \left(B _ {5 1}\right) ^ {F} = - \left(B _ {5 3}\right) ^ {F} - \left(B _ {5 5}\right) ^ {F} \\ = - \frac {2 5 3 2 \alpha_ {1} ^ {8} + 4 1 7 7 \alpha_ {1} ^ {7} - 2 1 9 7 6 \alpha_ {1} ^ {6} - 7 2 2 3 7 \alpha_ {1} ^ {5} - 8 1 9 7 2 \alpha_ {1} ^ {4} - 3 4 5 8 7 \alpha_ {1} ^ {3} + 5 9 3 4 \alpha_ {1} ^ {2} + 8 3 7 2 \alpha_ {1} + 1 4 3 2}{1 9 2 \left(\alpha_ {1} - 1\right) ^ {6} \left(1 2 \alpha_ {1} ^ {2} + 1 1 \alpha_ {1} + 2\right)}, \\ \left(B _ {2 2}\right) ^ {F} = \frac {3 - \sigma^ {2}}{4 \sigma^ {3}}, \\ \left(B _ {4 2}\right) ^ {F} = - \frac {\left(\alpha_ {1} + 1\right) \left(- 6 \alpha_ {1} ^ {5} + 2 6 \alpha_ {1} ^ {4} + 1 8 2 \alpha_ {1} ^ {3} + 2 0 4 \alpha_ {1} ^ {2} + 2 5 \alpha_ {1} - 2 6\right)}{\left(1 8 \alpha_ {1} + 1 2\right) \left(\alpha_ {1} - 1\right) ^ {4} \sinh 2 k h}, \\ \left(B _ {5 3}\right) ^ {F} = - \frac {9 \left(- 3 3 \alpha_ {1} ^ {7} + 4 \alpha_ {1} ^ {6} + 5 5 3 \alpha_ {1} ^ {5} + 1 3 3 6 \alpha_ {1} ^ {4} + 1 2 3 9 \alpha_ {1} ^ {3} + 3 6 2 \alpha_ {1} ^ {2} - 1 3 9 \alpha_ {1} - 8 2\right)}{1 2 8 \left(3 \alpha_ {1} + 2\right) (\alpha_ {1} - 1) ^ {6}}, \\ \left(B _ {4 4}\right) ^ {F} = \frac {\left(\alpha_ {1} + 1\right) \left(2 4 \alpha_ {1} ^ {5} + 9 2 \alpha_ {1} ^ {4} + 1 2 2 \alpha_ {1} ^ {3} + 6 6 \alpha_ {1} ^ {2} + 6 7 \alpha_ {1} + 3 4\right)}{2 4 \left(3 \alpha_ {1} + 2\right) (\alpha_ {1} - 1) ^ {4} \sinh 2 k h}, \\ \left(B _ {5 5}\right) ^ {F} = \frac {5 \left(3 0 0 \alpha_ {1} ^ {8} + 1 5 7 9 \alpha_ {1} ^ {7} + 3 1 7 6 \alpha_ {1} ^ {6} + 2 9 4 9 \alpha_ {1} ^ {5} + 1 1 8 8 \alpha_ {1} ^ {4} + 6 7 5 \alpha_ {1} ^ {3} + 1 3 2 6 \alpha_ {1} ^ {2} + 8 2 7 \alpha_ {1} + 1 3 0\right)}{3 8 4 (3 \alpha_ {1} + 2) (4 \alpha_ {1} + 1) (\alpha_ {1} - 1) ^ {6}}. \end{array} \right\} \tag {4.3}
$$

Similar to (3.9) the amplitude of the first harmonic component of the free surface expression can be expressed as 

$$
(\tilde {a}) ^ {F} = a \left[ 1 + k ^ {2} a ^ {2} \left(B _ {3 1}\right) ^ {F} + k ^ {4} a ^ {4} \left(B _ {5 1}\right) ^ {F} \right]. \tag {4.4}
$$

Finally, the dispersion relationship of Fenton's solutions can also be written in the same form as (3.7): 

$$
\left. \begin{array}{l} \frac {(\omega) ^ {F}}{\omega_ {0}} = [ 1 + k ^ {2} a ^ {2} (\omega_ {2}) ^ {F} + k ^ {4} a ^ {4} (\omega_ {4}) ^ {F} ], \\ (\omega_ {2}) ^ {F} = \frac {2 \alpha_ {1} ^ {2} + 7}{4 (\alpha_ {1} - 1) ^ {2}} \\ (\omega_ {4}) ^ {F} = \frac {4 \alpha_ {1} ^ {5} + 3 2 \alpha_ {1} ^ {4} - 1 1 6 \alpha_ {1} ^ {3} - 4 0 0 \alpha_ {1} ^ {2} - 7 1 \alpha_ {1} + 1 4 6}{3 2 (\alpha_ {1} - 1) ^ {5}}. \end{array} \right\} \tag {4.5}
$$

There are two fundamental differences between the present solutions and those of Fenton. First, in the present potential function solutions the third- and fifth-order solutions do not contribute to the first harmonic (i.e. $A_{31} = A_{51} = 0$ ), while Fenton's solutions contain both contributions. Second, in Fenton's free surface profile solution, the condition, $H = 2a$ was imposed as an a priori condition, resulting in $(B_{31})^F = -(B_{33})^F$ and $(B_{51})^F = -(B_{53})^F - (B_{55})^F$ , while our solutions did not make such an assumption and showed that the wave height was a function of $a$ and $k$ . These two differences are connected. The assumption that $H = 2a$ is the root cause of the problem. In deriving his solutions, Fenton expanded the stream function in the same format as those shown in (3.1). In solving for the coefficients in front of different harmonic functions (i.e. $\cos \theta$ , $\cos 2\theta$ , etc.) in the moving coordinate, an additional physical condition is required to solve the system of equations for the coefficients. Instead of assuming $H = 2a$ , which is non-physical, the correct condition should have been that the third-order and fifth-order stream function solutions make no contribution to the first harmonic, which is equivalent to require $A_{31} = A_{51} = 0$ in the present solutions. The reason for imposing this necessary condition is to remove the secular terms in the third- and fifth-order problems. Because of this incorrect assumption, Fenton's solutions cannot satisfy the boundary value problems for the potential function derived in this paper. 


Table 2. Stokes wave solutions for free surface profile in deep water limit-amplitude coefficients in front of each harmonic.


<table><tr><td>\( \mathbf{authors^a} \)</td><td>a cos θ</td><td>a cos 2θ</td><td>a cos 3θ</td><td>a cos 4θ</td><td>a cos 5θ</td></tr><tr><td>D [8]</td><td>1 + \( \frac{9}{8}k^2a^2 + \frac{769}{192}k^4a^4 \)</td><td>\( \frac{1}{2}ka + \frac{11}{6}k^3a^3 \)</td><td>\( \frac{3}{8}k^2a^2 + \frac{315}{128}k^4a^4 \)</td><td>\( \frac{1}{3}k^3a^3 \)</td><td>\( \frac{125}{384}k^4a^4 \)</td></tr><tr><td>L [10]b</td><td>1 + \( \frac{1}{8}k^2a^2 \)</td><td>\( \frac{1}{2}ka \)</td><td>\( \frac{3}{8}k^2a^2 \)</td><td>n.a.</td><td>n.a.</td></tr><tr><td>F [11]</td><td>1 - \( \frac{3}{8}k^2a^2 - \frac{211}{192}k^4a^4 \)</td><td>\( \frac{1}{2}ka + \frac{1}{3}k^3a^3 \)</td><td>\( \frac{3}{8}k^2a^2 + \frac{99}{128}k^4a^4 \)</td><td>\( \frac{1}{3}k^3a^3 \)</td><td>\( \frac{125}{384}k^4a^4 \)</td></tr><tr><td>(3.10)</td><td>1 + \( \frac{1}{8}k^2a^2 + \frac{121}{192}k^4a^4 \)</td><td>\( \frac{1}{2}ka + \frac{5}{6}k^3a^3 \)</td><td>\( \frac{3}{8}k^2a^2 + \frac{171}{128}k^4a^4 \)</td><td>\( \frac{1}{3}k^3a^3 \)</td><td>\( \frac{125}{384}k^4a^4 \)</td></tr></table>


<sup>a</sup>Authors' names have been abbreviated: D (De); L (Laitone); F (Fenton). 



bLaitone's [10] solution is only up to the third order. 



Table 3. Stokes wave velocity potential function in deep water.


<table><tr><td>authors</td><td>φ/ω0a/k</td></tr><tr><td>S &amp; H [9]</td><td>(1 - 1/8 k2a2 - 7/12 k4a4)e kz sin θ + 1/2 k3a3 e2kz sin 2θ + 1/12 k4a4 e3kz sin 3θ</td></tr><tr><td>Laitone [10]a</td><td>e kz sin θ</td></tr><tr><td>Fenton [11]</td><td>(1 - 1/2 k2a2 - 37/24 k4a4)e kz sin θ + 1/2 k3a3 e2kz sin 2θ + 1/12 k4a4 e3kz sin 3θ</td></tr><tr><td>(3.11)</td><td>e kz sin θ + 1/2 k3a3 e2kz sin 2θ + 1/12 k4a4 e3kz sin 3θ</td></tr></table>


a Laitone's [10] solution is only up to the third order. 


# (b) Deep water

In this section, Stokes wave solutions in deep water are compared with those of Skjelbreia & Hendrickson [9], Fenton [11], De [8] and Laitone [10]. As mentioned in §1, there are authors who derived Stokes wave solutions using the still water depth, and others used the mean water depth. In the deep water limit the mean free surface set-down vanishes and these two coordinate systems become identical. All the existing solutions could be compared directly. 

Table 2 lists the amplitude coefficients of each harmonic in the Stokes wave solutions developed by De [8], Laitone [10] and Fenton [11]. The present solution, (3.10), is also included in the table for comparison. Note that Laitone's solutions are only available up to the third order, which have the same expressions as those of the present solutions. On the other hand, both De's and Fenton's third-, fourth- and fifth-order solutions are slightly different from each other and from the present solution, affecting the amplitudes of first, second and third harmonics. For example, in the first harmonic solution, the third- and fifth-order contributions are different among existing solutions. Using the wave height definition for the final Stokes wave solution given in (3.10), different theories give different wave height values. The wave height, calculated from De's solution, gives 

$$
(H) ^ {D e} = 2 a \left(1 + \frac {3}{2} k ^ {2} a ^ {2} + \frac {1 6 3}{2 4} k ^ {4} a ^ {4}\right), \tag {4.6}
$$

which is different from the present solution, (3.13). 

The corresponding potential function solutions in deep water, derived by Laitone [10], Fenton [11] and Skjelbreia & Hendrickson [9], are shown in table 3. 

De's [8] solutions are in the implicit form and cannot be included here. The present solution, (3.11), is listed for comparison. In the deep water, up to the third order, all solutions show that potential functions (and the corresponding velocity fields) contain only the first harmonic, while the free surface profiles have the second and third harmonic components (table 2). Up to the fifth order, the solutions derived by Skjelbreia & Hendrickson [9] and Fenton [11] differ slightly from the present solutions only in the coefficients of the first harmonic. The second and third harmonics are identical and the fourth and fifth harmonics are in the absence in all solutions. We reiterate here that since the present approach follows that of Dingemans [12], the first harmonic forcing 


Table 4. Wave celerity or dispersion relations in deep water.


<table><tr><td>authors</td><td>\(\left(\frac{c}{\omega_0/k}\right)^2=\left(\frac{\omega}{\omega_0}\right)^2\)</td></tr><tr><td>De [8]</td><td>1+k2a2+7/2k4a4</td></tr><tr><td>S &amp; H [9]</td><td>1+k2a2+5/4k4a4</td></tr><tr><td>Laitone [10]a</td><td>1+k2a2</td></tr><tr><td>Fenton [11]</td><td>1+k2a2+1/2k4a4</td></tr><tr><td>(3.12)</td><td>1+k2a2+3/2k4a4</td></tr></table>


a Laitone's [10] solution is only up to the third order. 


terms in the third-order and fifth-order governing equations have been removed by changing the time scale to get rid of the secular terms. Consequently, in the first harmonic, there is no contribution from the third- and fifth-order solutions in the present potential function results. Laitone's [10] third-order solutions have the same feature, but the solutions of Skjelbreia & Hendrickson [9] and Fenton [11] do not observe this important characteristic. 

Up to the fifth order, the wave celerity and the dispersion relation are tabulated in table 4. Being expressed in terms of $a$ , all the solutions for the wave celerity (or dispersion relation) are different slightly in the $O(k^4 a^4)$ . 

# (c) Numerical examples

In engineering applications, the wave period (or frequency), $T$ (or $\omega$ ), and water depth, $h$ , are usually prescribed. However, there are different options for specifying the design wave condition. In some cases, the wave height, $H$ , is given. In other cases, the wave amplitude of the first harmonic, $\tilde{a}$ , is specified. In less frequent situations, some users might prefer to specify $a$ , the wave amplitude of the first-order solution. Because of the page limit, we shall only show the first two applications in the main text. For the last application, the comparisons are presented in the electronic supplementary material. 

In the first example, $h = 30\mathrm{m}$ , $T = 2\pi /\omega = 5\mathrm{s}$ and $H = 5\mathrm{m}$ are fixed. The present solutions for wave height, (3.8), and dispersion relationship, (3.7), are solved simultaneously to obtain $k = 0.1428\mathrm{m}^{-1}$ and $a = 2.311\mathrm{m}$ . The free surface profile is then calculated from (3.3). On the other hand, using Fenton's solutions, $a = H / 2 = 2.5\mathrm{m}$ , and the dispersion relation (4.5) is then used to find $k = 0.1420\mathrm{m}^{-1}$ ; both $k$ and $a$ are different from our solutions. To illustrate other fundamental differences between the present solutions and Fenton's solutions, figure 2 plots the free surface elevations at different order. The first-order and second-order solutions, $\eta_{1} / H$ and $\eta_{2} / H$ , show slightly different shapes due to the difference in $a$ values. For $\eta_{3} / H$ and $\eta_{5} / H$ , Fenton's solutions are zero at $\theta = 0$ , which is the result of Fenton's requirement, $H = 2a$ . 

In the same figure, the total free surface profiles, up to the fifth order, are also plotted. The percentage differences are about $-1.31\%$ at the wave crest and $2.02\%$ at the wave trough. Several fundamental properties, such as the wavelength and the wave celerity, are also slightly different (table 5). 

Another characteristic difference between the present solutions and those of Fenton lies in the higher-order solutions of the potential function, i.e. $\phi_3$ and $\phi_5$ , which affect the velocity field. As an illustration, in figure 3, the time histories of the horizontal velocity solutions at $z / h = -0.0833$ (below the wave trough) are plotted for different order. Equations (3.1) are used for the present solutions and (4.1) for Fenton's solutions. Because of the treatment of secular terms in our derivation, there is no first harmonic contribution from the third-order and the fifth-order $\phi$ solutions (i.e. $A_{31} = A_{51} = 0$ ), resulting in relatively small $u_3 / \sqrt{gh}$ and $u_5 / \sqrt{gh}$ values. By contrast, Fenton's solutions show that the third-order and fifth-order solutions contain finite first harmonic component. The differences are dramatic in these orders. The overall differences between these 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/f6a2658006adb8ab585929a04029832242b36bb6ca8fab6ad2cbc18d9a0f4de2.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/a705a5743cde531aaaf9c2ed215dbae3ee2ffbbe39d72eeac819aa18ce9e4812.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/73346dbe049cf303fe6556138363013e7c7318cb18b8448f5dc4e656003ab015.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/3ee6462969c949f2b846f8a6c9259fcd4161c8ab2ed95f72cfcb74a602697ec8.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/054540e8b7225f4fbb1a3e630096bac9eb044566513893d67adc41a303ba1699.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/bb812bf08b406f97cc2e36d5c3e58fa6478a1bbee106f1bf72b0684c246146e1.jpg)



Figure 2. Given $H$ , comparisons of $\eta / H$ (bottom right subplot) and $\eta_{1-5} / H$ (the other five subplots as labelled) between the present and Fenton's solutions. Fenton's solutions are shown in red dashed curve with open circles and the present solutions are in blue solid curves. (Online version in colour.)



Table 5. List of wave parameters calculated from the present, Fenton's and Skjelbreia & Hendrickson's solutions with $h = 30$ m, $T = 5$ s and $H = 5$ m. The percentage difference is defined as the ratio of difference between present solutions and Fenton's or Skjelbreia & Hendrickson's to the present solution.


<table><tr><td>given H</td><td>k (m-1)</td><td>a (m)</td><td>H (m)</td><td>c (ms-1)</td><td>u max (ms-1)</td><td>w max (ms-1)</td><td>ηθ=0 (m)</td><td>ηθ=π (m)</td><td>a (m)</td></tr><tr><td>present</td><td>0.1428</td><td>2.311</td><td>5.000</td><td>8.800</td><td>4.447</td><td>2.781</td><td>2.979</td><td>-2.021</td><td>2.360</td></tr><tr><td>Fenton</td><td>0.1420</td><td>2.500</td><td>5.000</td><td>8.851</td><td>4.489</td><td>2.748</td><td>3.019</td><td>-1.981</td><td>2.321</td></tr><tr><td>diff. (%)</td><td>0.58%</td><td>-8.19%</td><td>0%</td><td>-0.58%</td><td>-0.93%</td><td>1.17%</td><td>-1.34%</td><td>1.98%</td><td>1.65%</td></tr><tr><td>S &amp; H</td><td>0.1418</td><td>n.a.</td><td>5.000</td><td>8.860</td><td>4.625</td><td>2.836</td><td>3.086</td><td>-2.056</td><td>2.414</td></tr><tr><td>diff. (%)</td><td>0.70%</td><td>n.a.</td><td>0.00%</td><td>-0.68%</td><td>-4.00%</td><td>-1.98%</td><td>-3.59%</td><td>-1.73%</td><td>-2.29%</td></tr></table>

two solutions of the total $u / \sqrt{gh}$ up to the fifth order are small with the maximum percentage difference of $-0.93\%$ , appearing at the wave crest. 

In table 5, some additional numerical results are summarized, including the maximum vertical velocity component and the heights of wave crest and wave trough. The wave crest and wave trough are slightly lower than those in Fenton's solutions. The maximum percentage difference in the vertical velocity is $1.17\%$ . With the exception for the difference in $a$ , which is $-8.19\%$ , the differences for all other key parameters listed are less than $2\%$ . The last two rows show the Stokes wave solutions obtained by Skjelbreia and Hendrickson. The major differences appear in $u_{\mathrm{max}}$ and $\eta_{\theta = 0}$ , which are $-4\%$ and $-3.59\%$ , respectively. 

In the second numerical example, the wave amplitude of first harmonic is given as $\tilde{a} = 2.5\mathrm{m}$ together with $h = 30\mathrm{m}$ and $T = 2\pi /\omega = 5\mathrm{s}$ . For the present solutions, (3.9) and (3.7) are used to 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/4ec4d8b717fa8d800b11829f642e25f4d047eb056d517a07a7fb98fd77aec649.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/41daa5ec7a5fecaf94036d35440e5f3fd881de190dc381c9fcaed741acb64e1e.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/e726c550db223577fe03e63a4570211e1a167eae8a1c85371d3df992b7a0e8c3.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/f92b3546435ae172dcb3d75e36eff83825b0b5b0469ec183f9f2d1110ecf7be4.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/f409daff5670cdaac017adc81bc7a95ae073a7b11869c748506421eef955ce0f.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/8e3803ea01439e67134b5126e5575446c7f3db0e1651b5307af8ce663b92e973.jpg)



Figure 3. Given $H$ , comparisons of $u / \sqrt{gh}$ (bottom right subplot) and $u_{1-5} / \sqrt{gh}$ (the five other subplots as labelled) versus $\theta$ at $z / h = -0.0833$ , a point slightly lower than the trough. The blue lines are the present solutions, and the red dashed lines with open circles represent Fenton's solutions. (Online version in colour.)


find the wavenumber, $k = 0.1411\mathrm{m}^{-1}$ , and the wave amplitude of the first-order free surface elevation, $a = 2.442\mathrm{m}$ . The wave height equation, (3.8), is employed to find $H = 5.333\mathrm{m}$ . The corresponding free surface profiles at each order are shown in figure 4. Similarly, for Fenton's solutions, the dispersion relationship, (4.5), and the wave amplitude formula, (4.4), are employed to find the wavenumber and the wave amplitude as $k = 0.1407\mathrm{m}^{-1}$ and $a = 2.611\mathrm{m}$ , respectively. The corresponding wave height is $H = 2a = 5.222\mathrm{m}$ . To demonstrate clearly the differences among different solutions, figures 4 and 5 show the free surface profile and the horizontal velocity at $z / h = -0.0833$ (below the wave trough) for each order. The characteristic differences mentioned in the first example can also be seen in these figures. (1) For $\eta_3 / \tilde{a}$ and $\eta_5 / \tilde{a}$ , Fenton's solutions are zero at wave crest ( $\theta = 0$ ). On the other hand, in the present solutions, the higher order solutions have contributions to the crest elevation. The trend of the solutions of Skjelbreia and Hendrickson is in general similar to the present solutions with slight differences in magnitude. (2) For $u_3 / \sqrt{gh}$ and $u_5 / \sqrt{gh}$ , because of the necessary treatment of the secular terms in the derivation, in our solutions $A_{31} = A_{51} = 0$ , and $A_{33}, A_{53}$ and $A_{55}$ are very small. Hence, the present solutions for $u_3 / \sqrt{gh}$ and $u_5 / \sqrt{gh}$ are much smaller than those of Fenton. 

Additional comparisons are shown among different solutions are listed in table 6. The comparisons with Fenton's solution are in the first three rows and the bottom two rows show the comparisons with Skjelbreia & Hendrickson [9]. Note that Skjelbreia and Hendrickson's solutions are expressed in terms of $\tilde{a}$ directly; therefore, the information for $a$ is not relevant. More specifically, the difference of trough of the present and Fenton's solutions can be as large as $3.94\%$ . The maximum percentage differences in the velocity at the wave crest are $1.69\%$ and $3.06\%$ for the horizontal and vertical components, respectively. The first-order first harmonic wave amplitudes, 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/b432fd5e918880a324d7ad7f932ef7880173620aac6eeb2e0802bd6a89ca03ea.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/0009a363256aab95934c5fa84c560d2bd2397608d27287bedc25039a05b99086.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/b636d62e18c64a02325cf01f58ab7e357530c243a53ac12d212075c8ad62ba9f.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/dc638444d2b4b9d603e06559cf6c7d25837efbb8d3013015841530b8e1d115b1.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/3ed42a167a283f5ae6bb80cca0d5afc138c04a3a0ed98e005880eb3818f06308.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/344c3cd39964265f4bd4ecf9812c9221e60845792b2e3c808f851d05c0f5d8f8.jpg)



Figure 4. Given $\tilde{a}$ , comparisons of $\eta / \tilde{a}$ (bottom right subplot) and $\eta_{1-5} / \tilde{a}$ (the five other subplots as labelled) between the present, Fenton's and Skjelbreia & Hendrickson's solutions. Fenton's solutions are shown in red dashed curves with open circles, the present solutions are in blue solid curves, and Skjelbreia & Hendrickson's solutions are represented by the black dashed curve. (Online version in colour.)



Table 6. List of wave parameters calculated from the present, Fenton's and Skjelbreia & Hendrickson's solutions with $h = 30$ m, $T = 5$ s and $\tilde{a} = 2.5$ m. The percentage difference is defined as the ratio of difference between present solutions and Fenton's or Skjelbreia & Hendrickson's to the present solution.


<table><tr><td>given a</td><td>k (m-1)</td><td>a (m)</td><td>H (m)</td><td>c (m s-1)</td><td>u max (m s-1)</td><td>w max (m s-1)</td><td>ηθ=0 (m)</td><td>ηθ=π (m)</td><td>a (m)</td></tr><tr><td>present</td><td>0.1411</td><td>2.442</td><td>5.333</td><td>8.905</td><td>4.849</td><td>2.933</td><td>3.205</td><td>-2.128</td><td>2.5</td></tr><tr><td>Fenton</td><td>0.1407</td><td>2.611</td><td>5.222</td><td>8.931</td><td>4.768</td><td>2.843</td><td>3.178</td><td>-2.044</td><td>2.5</td></tr><tr><td>diff. (%)</td><td>0.29%</td><td>-6.94%</td><td>2.07%</td><td>-0.29%</td><td>1.69%</td><td>3.06%</td><td>0.83%</td><td>3.94%</td><td>0%</td></tr><tr><td>S &amp; H</td><td>0.1407</td><td>n.a.</td><td>5.195</td><td>8.928</td><td>4.727</td><td>2.836</td><td>3.229</td><td>-2.12</td><td>2.5</td></tr><tr><td>diff. (%)</td><td>0.26%</td><td>n.a.</td><td>2.59%</td><td>-0.26%</td><td>2.53%</td><td>3.3%</td><td>-0.77%</td><td>0.36%</td><td>0%</td></tr></table>

however, are quite different: $-6.94\%$ in this case. The major differences of present and Skjelbreia and Hendrickson's results are in the velocity and wave height, being about $3\%$ . 

Additional numerical examples are provided in the electronic supplementary material. When $a$ is specified, the magnitudes of wave crest and trough of the present solutions are much larger than those of Fenton's solutions, leading to a much higher wave height (i.e. $> 2a$ ). The difference in wavenumber and wave celerity is relatively small. The most significant differences between the present and Fenton's solutions appear in the fluid particle velocity at wave crest and trough, where the percentage differences could be higher than $10\%$ for the case of given $a$ . 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/26f45c11d990d352dcf769d639fd70e5a4bad41af9aaf303a3144f9018503461.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/fffbe19bd5bb3785decd9d2bd1d2bfc181213ea3f41318e0718fe2bd92a34344.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/ba001362650feb2cd147046e5be76714520fe7371cc7e71d690bca4f38ed72f9.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/870569fbf8eb32a373f755392ca45440e2c950b9769d8e6a72c3c364376e3d5e.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/e919370232180da9cf58ae8b7540419b39357eaaa973c1c6a47a8e79e6049be4.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-18/0245ead8-d9d4-4bf5-b85a-cd2a68ac3ea5/f4a8f93f5af608b8479dd1b9da515206a33f95e320085933799e1fcb41e7d855.jpg)



Figure 5. Given $\tilde{a}$ , comparisons of $u / \sqrt{gh}$ (bottom right subplot) and $u_{1-5} / \sqrt{gh}$ (the five other subplots as labelled) versus $\theta$ at $z/h = -0.0833$ , a point slightly lower than the trough. The blue lines are the present solutions, the red dashed lines with open circles represent Fenton's solutions, and Skjelbreia and Hendrickson's solutions are shown by the black dashed curve. (Online version in colour.)


# 5. Concluding remarks

This paper provides a brief overview of the historical development of Stokes wave solutions up to the fifth order. The differences among existing solutions in terms of the definitions of the coordinate system and the water depth, the solution method and the format of final solution presentation are first discussed. The differences among the existing solutions are apparent. To compare them in a consistent manner, we have developed a new set of fifth-order Stokes wave solutions, using MATLAB® Symbolic Toolbox. We first confirm that all the results are the same up to the second order. At the third order, the present solutions are in complete agreement with those of Laitone [10]. However, differences among the other existing solutions are obvious, beginning at the third order. 

The causes for the differences between Fenton's and the present solutions have been identified. In deriving his stream function solutions, Fenton has imposed a condition on the wave height of the final free surface profile and the wave amplitude of the first harmonic at the first order, i.e. $H = 2a$ , which is non-physical. In the present solution, the wave height of the final free surface profile is a part of the solution and needs to be solved in conjunction with the dispersion relation. The second obvious difference between Fenton's and the present solutions lies on the fact that while the present third- and fifth-order solutions (i.e. $\phi_3$ , $\phi_5$ ) do not contain the first harmonic, Fenton's solutions do. In the present solution, the absence of first harmonic in the higher order solutions is the consequence of introducing perturbation series for frequency with the purpose of removing secular terms at the odd-orders. Therefore, Fenton's solutions cannot satisfy the third- and fifth-order free surface boundary conditions. Instead of requiring $H = 2a$ in his formulation, Fenton should have specified that the first harmonic terms vanish in his third- and fifth-order solutions. 

Several numerical examples have been given in the main text and the electronic supplementary material so as to quantify the differences between Fenton's and the present solutions. In these examples, $kh$ is approximately equal to 4.28, indicating that these are in the deep water depth. The most significant differences between the present and Fenton's solutions appear in the fluid particle velocity at wave crest and trough, where the percentage differences could be higher than $10\%$ for the case of given $a$ . The differences will increase when $kh$ value becomes smaller or when $ka$ value increases. 

Several other interesting findings are noted here. (1) Comparing Skjelbreia & Hendrickson's [9], Fenton's [11] and the present solutions, the expressions of free surface profile become identical after the original formulae are normalized by the amplitude of the first harmonic. However, the potential functions and the dispersion relations (wave celerity) are still different (see electronic supplementary material). (2) In deep water, the same feature is observed. However, the wave celerity also becomes the same. (3) In the deep water limit, while the free surface elevation contains fourth and fifth harmonics, the potential function is only related to the three lowest harmonic terms. This is true for all existing and present solutions. 

For completeness, a comprehensive electronic supplementary material has been created to document the detailed information on the derivation of the present solutions. The results for additional examples are also included. Moreover, a Web link is provided so that the reader can gain access to the MATLAB® functions created for the symbolic manipulations. 

Data accessibility. Additional data are available in the electronic supplementary material [19]. 

Authors' contributions. K.Z.: formal analysis, methodology, software, writing—original draft; P.L.-F.L.: conceptualization, investigation, project administration, supervision, writing—review and editing. 

Competing interests. We declare we have no competing interests. 

Funding. This research is supported by the National Research Foundation, Prime Minister's Office, Singapore under its Marine Science Research and Development Programme (award no. MSRDP-05). 

Acknowledgements. The authors would like to acknowledge the support provided by the National University of Singapore through an initiative grant. The authors would also like to thank reviewers for their valuable comments, and are especially grateful to Harry Yeh and Cheng-Jung Hsu for their efforts in checking solutions in the early draft and pointing out the typographical errors, which have been corrected. 

# References



1. Stokes GG. 1847 On the theory of oscillatory waves. Rep. Br. Assoc. VI, 441-455. 





2. Airy GB. 1845 Tides and waves. London, UK: Encyclopaedia Metropolitana. 





3. Stokes GG. 1880 Supplement to a paper on the theory of oscillatory waves. Math. Phys. Pap. 1, 14. 





4. Rayleigh L. 1917 XXXVIII. On periodic irrotational waves at the surface of deep water. Lond. Edinb. Dublin Phil. Mag. J. Sci. 33, 381-389. (doi:10.1080/14786440508635653) 





5. Levi-Civita T. 1925 Determination rigoureuse des ondes permanentes d'ampleur finie. Math. Ann. 93, 264-314. (doi:10.1007/BF01449965) 





6. Struik DJ. 1926 Détémination rigoureuse des ondes irrotationelles périodiques dans un canal à profondeur finie. Math. Ann. 95, 595-634. (doi:10.1007/BF01206629) 





7. Hunt J. 1953 A note on gravity waves of finite amplitude. Q. J. Mech. Appl. Math. 6, 336-343. (doi:10.1093/qjmam/6.3.336) 





8. De SC. 1955 Contributions to the theory of Stokes waves. Math. Proc. Cambridge Phil. Soc. 51, 713-736. (doi:10.1017/S0305004100030796) 





9. Skjelbreia L, Hendrickson J. 1960 Fifth order gravity wave theory. Coast. Eng. Proc. 1, 10. (doi:10.9753/icce.v7.10) 





10. Laitone E. 1962 Limiting conditions for cnoidal and Stokes waves. J. Geophys. Res. 67, 1555-1564. (doi:10.1029/JZ067i004p01555) 





11. Fenton JD. 1985 A fifth-order Stokes theory for steady waves. J. Waterway Port Coastal Ocean Eng. 111, 216-234. (doi:10.1061/(ASCE)0733-950X(1985)111:2(216)) 





12. Dingemans MW. 1997 Water wave propagation over uneven bottoms. Advanced Series on Ocean Engineering, vol. 13. Singapore: World Scientific. (doi:10.1142/1241) 





13. Schwartz LW. 1974 Computer extension and analytic continuation of Stokes' expansion for gravity waves. J. Fluid Mech. 62, 553-578. (doi:10.1017/S0022112074000802) 





14. Cokelet E. 1977 Steep gravity waves in water of arbitrary uniform depth. Phil. Trans. R. Soc. Lond. A 286, 183-230. (doi:10.1098/rsta.1977.0113) 





15. Dallaston MC, McCue SW. 2010 Accurate series solutions for gravity-driven Stokes waves. Phys. Fluids 22, 082104. (doi:10.1063/1.3480394) 





16. Longuet-Higgins HC. 1975 Integral properties of periodic gravity waves of finite amplitude. Proc. R. Soc. Lond. A 342, 157-174. (doi:10.1098/rspa.1975.0018) 





17. Crew SC, Trinh PH. 2016 New singularities for Stokes waves. J. Fluid Mech. 798, 256-283. (doi:10.1017/jfm.2016.309) 





18. Zhong X, Liao S. 2018 On the limiting Stokes wave of extreme height in arbitrary water depth. J. Fluid Mech. 843, 653-679. (doi:10.1017/jfm.2018.171) 





19. Zhao K, Liu PL-F. 2022 On Stokes wave solutions. Figshare. 

