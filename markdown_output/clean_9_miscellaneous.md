# Miscellaneous
## Fourier Transform
For a continuous and unbounded field, Fourier Transform (FT) can be applied: $$f(\bm{x}) = \int_\Omega d^p\bm{k} F(\bm{k}) e^{i2\pi\bm{k}\cdot\bm{x}}.$$ $$\begin{aligned}
    \bm{\theta} &\equiv \bm{x}\\
    \bm{l} &\equiv 2\pi\bm{k}.
\end{aligned}$$ We obtain, $$\begin{aligned}
    f(\bm{\theta}) &= \int_\Omega d^p \left(\frac{\bm{l}}{2\pi}\right) F(\bm{l}) e^{i\bm{l}\cdot\bm{\theta}}\\
    & = \frac{1}{(2\pi)^p}\int_\Omega d^p\bm{l} F(\bm{l}) e^{i\bm{l}\cdot\bm{\theta}}.
\end{aligned}$$ In fact, in the flat sky approximation we can treat $C(l)$ as a 2D power spectrum on a plane, which gives (Dodelson and Schmidt 2021): $$w(\theta)=\frac{1}{4\pi^2}\int_\Omega d^2\bm{l} C(l) e^{i\bm{l}\cdot\bm{\theta}}$$
## Full vs Flat
Full sky $$\begin{aligned}
    w(X,Y) &=\langle \hat{\delta}(X), \hat{\delta}(Y)\rangle 
onumber \\
    &= \sum_{ll'}\sum_{mm'} Y^m_l \overline{Y}^{m'}_{l'} \langle \hat{\delta}_{mm'}\hat{\delta}_{ll'} \rangle 
onumber \\
    &= \sum_{ll'}\sum_{mm'} Y^m_l \overline{Y}^{m'}_{l'}\delta_{mm'}\delta_{ll'}C_l 
onumber \\
    &= \sum_{l}C_l\sum_{m} Y^m_l \overline{Y}^{m}_{l} 
onumber \\
    &=
\end{aligned}$$
$$\begin{aligned}
    w(\mu) &=\sum_{l}\frac{2l+1}{4\pi}C_lP_l(\mu)\\
    \implies \int \mu w(\mu) P_{l'}(\mu) &= \sum_{l}\frac{2l+1}{4\pi}C_l\int \mu P_{l'}(\mu)P_l(\mu)=\frac{1}{2\pi}C_{l'} 
onumber \\
    C_l &= 2\pi \int \mu w(\mu) P_{l}(\mu)
    \label{eq:fullcltow}
\end{aligned}$$ Flat sky $$\begin{aligned}
    w(\theta)
    &=FT^{-1}C(\bm l)\\
    &=\int \frac{d^2l}{(2\pi)^2} e^{i\bm l \cdot \bm \theta}C(\bm l) 
onumber\\
    &=\int \frac{dl}{(2\pi)^2} l C(l)\int d\phi e^{il\theta cos(\phi)} 
onumber\\
    &=\int \frac{dl}{2\pi} l C(l) J_0(l\theta)
\end{aligned}$$ Now to prove the equivalence between the flat sky and full sky relation, plug in the full sky Eq. [\[eq:fullcltow\]](#eq:fullcltow){reference-type="ref" reference="eq:fullcltow"}, $$\begin{aligned}
    C_l &= 2\pi \int \mu \int \frac{dl'}{2\pi} l' C(l') J_0(l'\theta(\mu)) P_{l}(\mu) 
onumber\\
    &= \int dl' l' C(l') \int \mu J_0(l'\theta(\mu)) P_{l}(\mu) 
onumber
\end{aligned}$$ for $l\gg1, J_0(l'\theta)\rightarrow P_{l'}(\mu)$ $$\begin{aligned}
    &\sim \int dl' l' C(l') \int \mu P_{l'}(\mu) P_{l}(\mu) 
onumber\\
    &\sim \int dl' l' C(l') \frac{\delta_{ll'}}{l} 
onumber\\
    &= C(l)
\end{aligned}$$
## Discrete Fourier Transform
Moving to the discrete and bounded case, a Discrete Fuorier Transform (DFT) approach is needed: $$f(\bm{n}) = \frac{1}{N_1N_2...N_p}\sum_{\bm{p}=0}^{\bm{N}-1} F(\bm{p}) e^{i2\pi\bm{p}\cdot \left( \bm{n}\circ \bm{N}^{\circ -1}\right)}.$$ $$\begin{aligned}
    \bm{\theta} &\equiv \bm{L}\circ \bm{n}\circ \bm{N}^{\circ -1}\\
    \bm{l} &\equiv 2\pi\bm{p}\circ\bm{L^{\circ-1}}
\end{aligned}$$ We obtain, $$f(\bm{\bm{\theta}}) = \frac{1}{N_1N_2...N_p}\sum_{\bm{l}=0}^{2\pi\bm{L^{\circ-1}}(\bm{N}-1)} F(\bm{l}) e^{i\bm{l}\cdot\bm{\theta}}$$ where we have made use of the properties of the Hadamard Product $\circ$, a pair-wise product operation. We can additionally define $$\bm{l_{max}} \equiv 2\pi\bm{L^{\circ-1}}(\bm{N}-1)$$ to obtain $$f(\bm{\bm{\theta}}) = \frac{1}{N_1N_2...N_p}\sum_{\bm{l}=0}^{\bm{l_{max}}} F(\bm{l}) e^{i\bm{l}\cdot\bm{\theta}}$$
Applying this general equation to our 2D flat sky case of a field defined on a square box of size and pixels . $$\begin{aligned}
    \bm{\theta} &\equiv \bm{n}\frac{L}{N}\\
    \bm{l} &\equiv 2\pi\frac{\bm{p}}{L}\\
    l_{max} &\equiv 2\pi\frac{N-1}{L}
\end{aligned}$$ $$w(\theta)=\frac{1}{N^2}\sum_{\bm{l}=0}^{l_{max}} C(l) e^{i\bm{l}\cdot\bm{\theta}}
    \label{eq:DFTcl}$$
:::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}
::: {#ref-dodelson .csl-entry}
Dodelson, Scott, and Fabian Schmidt. 2021. "13 - Probes of Structure: Lensing." In *Modern Cosmology (Second Edition)*, edited by Scott Dodelson and Fabian Schmidt, Second Edition, 373--99. Academic Press. https://doi.org/<https://doi.org/10.1016/B978-0-12-815948-4.00019-X>.
:::
::::
