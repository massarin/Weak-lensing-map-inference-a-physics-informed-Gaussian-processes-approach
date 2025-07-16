# Theoretical Framework

## Weak lensing {#sec:weak lensing}

### Convergence field

Let's introduce what can only be defined as the protagonist cosmological field of this thesis: the convergence field (Dodelson and Schmidt 2021) (Blandford et al. 1991) (Kilbinger 2015) (Bartelmann and Maturi 2017). As explained in the introduction weak lensing happens due to the presence of matter between us and a distant source. In mathematical terms we write this as an integral over the line of sight of the matter overdensity field, weighted accordingly. $$\kappa(\theta) = \int_0^{\chi*}d\chi W(\chi)\delta_m(\chi \theta, \chi),$$ $$W(\chi)=\tfrac{3}{2}H_0^2\Omega_m(1+z(\chi))\chi \int_\chi^{\chi*}d\chi' n(z(\chi'))\left(1-\frac{\chi}{\chi'}\right).
    \label{eq:lensing weight}$$ With $W(\chi)$ being a measure of the lensing weights; $W(\chi)$ incorporates all of the relevant cosmological parameters, as well as knowledge of the redshift distribution of the source galaxies $n(z)$.

### 2-point statistics

2-point statistics such as correlation functions and power spectra are arguably the most powerful tool of analysis in cosmology. They work as a way to summarise raw data into something simpler, while still retaining most of the relevant information; for examples, allowing us to extract constraints on cosmological parameters.

#### Full sky

Let us start by introducing the statistics of a 3D spherically symmetric field, also known as a full sky field. The 2-point autocorrelation function is defined as the expectation value $\mathbb{E}$ of the product of a random field with its complex conjugate $$w(\bm{x}, \bm{y}) \equiv \mathbb{E}[\phi(\bm{x})\phi^*(\bm{y})].$$ Where $\phi(\bm{x})$ is the 2D projection of a spherically symmetric 3D field. We can now perform a decomposition in spherical harmonics $Y_{\ell m}$. Such a decomposition gives rise to the correlation function associated to the harmonic coefficients $\phi_{\ell m}$, the 2D power spectrum $C_\ell$, $$\begin{gathered}
    \phi(\bm{x}) = \sum_{\ell m}\phi_{\ell m} Y_{\ell m}(\hat{\bm{x}}),\\
    C_\ell \equiv \delta_{\ell m}\delta_{\ell'm'}\mathbb{E}[ \phi_{\ell m}\phi^*_{\ell'm'}].
\end{gathered}$$ In this setup correlation function and power spectrum are therefore related by, $$\begin{aligned}
    & \mathbb{E}[\phi(\bm{x})\phi^*(\bm{y})] \\
    =& \sum_{\ell m}\sum_{\ell'm'}Y_{\ell m}(\hat{\bm{x}})Y^*_{\ell'm'}(\hat{\bm{y}}) \mathbb{E}[ \phi_{\ell m}\phi^*_{\ell'm'} ]\\
    =& \sum_{\ell m}Y_{\ell m}(\hat{\bm{x}})Y^*_{\ell m}(\hat{\bm{y}}) C_\ell\\
    =& \sum_{\ell}\frac{2\ell+1}{4\pi}C_\ell P_\ell(\hat{\bm{x}}\cdot\hat{\bm{y}}),
\end{aligned}$$ where we have used the identity relating Legendre polynomials to spherical harmonics $P_\ell(\hat{\bm{x}}\cdot\hat{\bm{y}}) = \frac{4\pi}{2\ell+1} \sum_m Y_{\ell m}(\hat{\bm{x}})Y^*_{\ell m}(\hat{\bm{y}})$. Cleaning up the equations we are just left with the well known full sky equation $$w(\theta) = \sum_{\ell}\frac{2\ell+1}{4\pi}C_\ell P_\ell (\cos(\theta)),
    \label{eq:fullsky}$$ which relates the angular correlation function to the angular power spectrum.

#### Flat-sky

Most analysis of weak lensing data actually use the flat-sky approximation (Nicola et al. 2021) (Gao, Raccanelli, and Vlah 2023) (Matthewson and Durrer 2021) (Gao, Vlah, and Challinor 2023) (García-García, Alonso, and Bellini 2019) (Schneider, P. et al. 2002), our work will not be an exception. Such an approximation essentially changes our setup to a flat-sky 2D field, instead of the 2D projection of a 3D one, allowing for simpler analytical expressions. In this setup, harmonic decomposition will not work, we will have to Fourier transform our space instead. To do so, we can assume the existence of a function $C(l)$ which is the continuous extension of $C_\ell$. Then we say that $C(l)$ is the result of a 2D inverse Fourier transformation $\mathcal{F}$, $$\{\mathcal{F}^{-1}C\}(\theta)=\int\frac{d^2l}{4\pi^2}e^{i\bm{l}\cdot\bm{\theta}}C(l).
    \label{eq:flatsky fft}$$ To prove that $\{\mathcal{F}^{-1}C\}(\theta)$ is none other than the angular correlation function, we make use of the radial symmetry of the cosmological field. Which simplifies the equation into a 1D integral. Consider the polar coordinate substitution from $(l_x,l_y)$ to $(l,\phi)$, the integral becomes $$\int \frac{dl}{2\pi} l C(l) \int\frac{d\phi}{2\pi}e^{il\theta \cos{\phi}}.$$ Lastly, we make use of the identity $\int d\phi e^{il\theta \cos{\phi}} = 2\pi J_0(l\theta)$, where $J_0$ is the zeroth order Bessel function. Which leaves us with $$\{\mathcal{F}^{-1}C\}(\theta) = \int \frac{dl}{2\pi} l C(l) J_0(l\theta).
    \label{eq:flatsky hankel}$$ In this form it is clear that *Eq.* [\[eq:fullsky\]](#eq:fullsky){reference-type="eqref" reference="eq:fullsky"} and *Eq.* [\[eq:flatsky hankel\]](#eq:flatsky hankel){reference-type="eqref" reference="eq:flatsky hankel"} are asymptotically equivalent, since it is known that $J_0(\ell\theta) \xrightarrow{\quad} P_\ell (\cos(\theta))$ as $\ell \rightarrow \infty$. This concludes our heuristic proof that the angular correlation function is recovered from an inverse Fourier transformation of the angular power spectrum $w(\theta) \sim \{\mathcal{F}^{-1}C\}(\theta)$ in the flat-sky approximation. Physically speaking this approximation makes sense when we consider a patch of sky of size L. The wavenumber of the flat-sky angular power spectrum is related to its dimensionless counterpart p by $$l = \frac{2\pi}{L}p,
    \label{eq:ell px}$$ in other words, it is inversely proportional to the size of the map. Just as we would expect the geometry of a sphere to become flat when zooming in, the flat-sky approximation holds as $L \rightarrow 0$.

#### Limber approximation

The way we computationally obtain $\kappa$'s 2-point statistics is with the Limber approximation. We use the code (Campagne et al. 2023) to compute the 2D power spectrum $C(l)$ from the 3D matter power spectrum $P_\delta(k)$ with the efficient Limber approximation, $$C(l)=C_{\kappa\kappa}(l)=\int_0^{\chi*}\frac{d\chi}{\chi} W(\chi)W(\chi)P_\delta(k=\frac{l}{\chi},\chi).
    \label{eq:limber}$$ The assumptions of the Limber approximation are:

- flat-sky, as described previously and

- the matter power spectrum depends only on modes on the field $\bm{k}_\perp$, essentially setting the modes parallel to the line of sight to zero, $k_\parallel=0$.

Such assumptions allow to simplify the relation between $C(l)$ and $P_\delta(k)$ to a one line integral, *Eq.* [\[eq:limber\]](#eq:limber){reference-type="eqref" reference="eq:limber"}. It is noteworthy to mention that the Limber approximation introduces significant errors only for modes $l<10$, as explained in detail in (Gao, Vlah, and Challinor 2023). As far as this work is concerned, we only deal with patches of size $10^{\circ}$, which means we have $l>36$ according to *Eq.* [\[eq:ell px\]](#eq:ell px){reference-type="eqref" reference="eq:ell px"}, well within the range for a good approximation.

## Field generation {#sec:field generation}

### Gaussian random field

In order to simulate cosmological fields with a specific power spectrum, we make use of Gaussian random fields. They are fast to generate and only need information about the 2-point power spectrum of the field. The algorithm we use for the generation of GRFs is common to most packages and is explained in detail in (Bertschinger 2001) (Lang and Potthoff 2011). In 1D, assume a pair of functions functions $\xi$ and $P$, related by a Fourier transformation $$\xi(x,y)=\int \frac{dk}{2\pi} e^{i k(x-y)} P(k).$$ Let $W(x)$ be a Gaussian white noise field and let $\mathcal{F}$ denote a Fourier transformation, we then define $$\phi(x) \equiv (\mathcal{F}^{-1} P^{1/2}\mathcal{F}W)(x)
    \label{eq:grf 1D}$$ to be a Gaussian random field. Such a procedure ensures that the covariance $\mathbb{E}\left[\phi(x)\phi(y)\right]$ of the GRF recovers the correlation function $\xi(x,y)$, $$\begin{aligned}
 &\mathbb{E}\left[\phi(x)\phi(y)\right] \\
=&\iiiint dx' dy' \frac{dk}{2\pi} \frac{dl}{2\pi}  \, e^{i(kx + ly)} P(k)^{1/2} P(l)^{1/2} e^{-i(kx' + ly')} \mathbb{E}[W(x')W(y')] \\
=& \iint \frac{dk}{2\pi} \frac{dl}{2\pi} \, e^{i(kx + ly)} P(k)^{1/2} P(l)^{1/2} \int dx' \, e^{-i(k+l)x'}   \\
=& \int \frac{dk}{2\pi} \, e^{i k(x-y)} P(k)  \\
=& \, \xi(x, y).
\end{aligned}$$ Where we have used $\mathbb{E}[W(x')W(y')] = \delta(x'-y')$, as white noise is defined by a constant power spectrum.

#### Rayleigh distribution

Since we are dealing with 2D maps, our algorithm will have to be implemented in two dimensions. To do so, we decide to implement the algorithm in *Eq.* [\[eq:grf 1D\]](#eq:grf 1D){reference-type="eqref" reference="eq:grf 1D"} with the use of the Rayleigh distribution $\mathcal{R}(\sigma)$. Given two independent Gaussian random variables $X$ and $Y$, the random variable $R$ given by $$R=\sqrt{X^2+Y^2},$$ is said to be Rayleigh distributed. If we then multiply $R$ by the complex exponential $e^{i\theta}$ of a uniformly distributed random variable $\theta \sim \mathcal{U}(0,2\pi)$, we obtain a map of Gaussianly distributed complex numbers, which will substitute the $\mathcal{F}W$ term in *Eq.* [\[eq:grf 1D\]](#eq:grf 1D){reference-type="eqref" reference="eq:grf 1D"}. We showcase this equivalency in *Fig.* [1.1](#fig:rayleigh){reference-type="ref" reference="fig:rayleigh"} for distributions of $\mu=0$ and $\sigma=1$. The sequence of transformations in 2D therefore becomes, $$\phi(x) \equiv (\mathcal{F}^{-1} P^{1/2} R e^{i\theta})(x).
    \label{eq:grf 2D}$$

![[]{#fig:rayleigh label="fig:rayleigh"} Sampling a 2D Gaussian against a Rayleigh distributed amplitude with uniform complex phase. In purple is the complex number $X+iY$ with $X,Y \sim \mathcal{N}(0,1)$, in cyan is $Re^{i\theta}$ with $R\sim\mathcal{R}(1)$ and $\theta \sim \mathcal{U}(0,2\pi)$.](images/7_rayleigh.pdf){#fig:rayleigh width="\\textwidth"}

### Lognormal field

The universe today is not Gaussian. GRFs are able to capture the 2-point statistics of cosmological fields, but they cannot capture their skewed distribution. A possible way to get closer to the true distribution of the convergence field is with a lognormal transformation (Boruah, Rozo, and Fiedorowicz 2022) (Leclercq and Heavens 2021) (Hilbert, S., Hartlap, J., and Schneider, P. 2011) (Zhou et al. 2023). In this work we will denote lognormal transformations as $\mathcal{L}$ and adopt the following convention for both the field and the correlation function, $$\begin{gathered}
    \label{eq:L_w}
    \mathcal{L}_w^{-1}(w^{L}, a) \equiv \log \left(\frac{w^{L}}{a^2}+1\right) = w^G,\\
    \label{eq:L_k}
    \mathcal{L}_\kappa(\kappa^G, a) \equiv a\left(\exp(\kappa^G-\tfrac{1}{2}\text{Var}(\kappa^G)) -1\right) = \kappa^{L}.
\end{gathered}$$ Where the superscripts L and G respectively stand for lognormal and Gaussian, Var($\cdot$) stands for the variance of the field and $a$ is the so-called shift parameter, which is an indicator of the non-Gaussianity of the resulting field.

## Gaussian process {#sec:gaussian process}

One way to think of Gaussian processes is as an extension of random vectors to infinite dimensions. Following this train of thought, let's begin with the concept of a random variable following a normal distribution. We say, $$X \sim \mathcal{N}\left(\mu, \sigma^2\right),$$ to mean that $X$ is a sample of a Gaussian of mean $\mu$ and variance $\sigma^2$. If we were to get enough samples $X$, we would eventually recover its distribution. The generalisation of this concept to n-dimensions is a collection of random variables, described by a so-called multivariate normal distribution, $$\bm{X} \sim \mathcal{N}\left(\bm{\mu}, \bm{K}\right).$$ Where $\bm{X}=(X_0,X_1,...)$ is a vector of random variables, $\bm{\mu}$ is the mean vector and $\bm{K}$ the covariance matrix. For a zero mean field, the covariance matrix is formed by the variance of each of the random variables on its diagonal, while the cross correlation terms populate the rest of the matrix.

### Definition

Adopting the philosophy of Rasmussen (Rasmussen and Williams 2005), functions can be thought of as very long vectors of the form $\left(f(x_1), f(x_2), ...\right)$. Such a view allows us to extend the definition of multivariate Gaussians, to functions. Defining $\mathcal{GP}$ a Gaussian process, a sample function $f$ will be given by: $$f(\bm{x}) \sim \mathcal{GP}\left(m(\bm{x}), k(\bm{x}, \bm{x'})\right)$$ with $m(\bm{x})$ and $k(\bm{x}, \bm{x'})$ defined as, $$\begin{gathered}
    m(\bm{x})=\mathbb{E}[f(\bm{x})],\\
    k(\bm{x}, \bm{x'})=\mathbb{E}[(f(\bm{x})-m(\bm{x}))(f(\bm{x}')-m(\bm{x}'))],
\end{gathered}$$ Mathematically a GP is defined for a continuous function. Computationally this is not possible and we must treat space as a discrete grid.

### Prior and posterior samples

Given some $m(\cdot)$ and $k(\cdot,\cdot)$ which define a GP, a random sample from said GP would be a function $\bm{f}_*$ defined on a domain $D_*$, which is our grid. $$\bm{f}_* \sim \mathcal{N}(\bm{m}, \bm{K}_{**}).
    \label{eq:gp prior}$$ Here we adopt the convention $\bm{K} = k(D_*,D_*)$. When drawing a sample function from *Eq.* [\[eq:gp prior\]](#eq:gp prior){reference-type="eqref" reference="eq:gp prior"}, computationally the operation is equivalent to drawing a vector from a multivariate Gaussian. What we obtain is a so-called prior, or priors, see *Fig.* [1.2](#fig:priors){reference-type="ref" reference="fig:priors"}.

![Prior samples of a GP with mean $m(\bm{x})=0$ and squared exponential kernel $k(\bm{x},\bm{x'})=e^{-(\bm{x}-\bm{x'})^2}$.](images/1_priors.pdf){#fig:priors width="\\textwidth"}

Let's now see how we can introduce knowledge of data points in this system. We divide the grid in training points $D$ and test points $D_*$. To each training point is associated a known value $\bm{y}$ and variance $\sigma_n^2$, whereas the values of the function at the test points $\bm{f}_*$ are unknown. We can summarise this as, $$\begin{bmatrix}
    \bm{y} \\
    \bm{f}_* \\
    \end{bmatrix}
    \sim \mathcal{N}\left(\bm{m}, \begin{bmatrix}
    \bm{K} + \sigma_n^2 I & \bm{K}_* \\
    \bm{K}^T_* & \bm{K}_{**} \\
    \end{bmatrix}\right)$$ where we have once again adopted the notation $\bm{K}=k(D,D)$, $\bm{K_{*}}=k(D,D*)$, $\bm{K_{**}}=k(D_*,D_*)$. At this point, one way to find samples that follow the data would be to blindly draw priors until we get something that goes through all data points. This would be inefficient and computationally wasteful. Instead, we make a better guess for the test function values. This operation is called conditioning, because we condition the joint Gaussians on the training points, this gives $$\bm{f}_* \mid D_*, D, \bm{y} \sim \mathcal{N}\left( \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{y} , \bm{K}_{**} - \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{K}_* \right).
\label{eq:conditioning}$$ Conditioning can therefore give rise to what is called a posterior sample, *Fig.* [1.3](#fig:posteriors){reference-type="ref" reference="fig:posteriors"}. The result is still a multivariate Gaussian, but the mean and variance given by *Eq.* [\[eq:conditioning\]](#eq:conditioning){reference-type="eqref" reference="eq:conditioning"} generate samples that are a better guess of the behaviour of the function outside of the training points.

![[]{#fig:posteriors label="fig:posteriors"} Summary plot of a GP conditioned to some data. The cyan line is the mean of the GP and the filled region corresponds to $1\sigma$. The purple lines are posterior samples, which are distributed Gaussianly around the mean. The data points are clearly marked in black, they are also the points where all samples converge to.](images/1_posteriors.pdf){#fig:posteriors width="\\textwidth"}

::::::::::::::::::::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}
::: {#ref-cosmology:lensing2 .csl-entry}
Bartelmann, M., and M. Maturi. 2017. "Weak Gravitational Lensing." *Scholarpedia* 12 (1): 32440. <https://doi.org/10.4249/scholarpedia.32440>.
:::

::: {#ref-grf .csl-entry}
Bertschinger, Edmund. 2001. "Multiscale Gaussian Random Fields and Their Application to Cosmological Simulations." *The Astrophysical Journal Supplement Series* 137 (1): 1. <https://doi.org/10.1086/322526>.
:::

::: {#ref-weaklensing .csl-entry}
Blandford, R. D., A. B. Saust, T. G. Brainerd, and J. V. Villumsen. 1991. "[The distortion of distant galaxy images by large scale structure]{.nocase}." *AIP Conference Proceedings* 222 (1): 455--58. <https://doi.org/10.1063/1.40414>.
:::

::: {#ref-lognormal .csl-entry}
Boruah, Supranta Sarma, Eduardo Rozo, and Pier Fiedorowicz. 2022. "Map-Based Cosmology Inference with Lognormal Cosmic Shear Maps." <https://arxiv.org/abs/2204.13216>.
:::

::: {#ref-jaxcosmo .csl-entry}
Campagne, Jean-Eric, François Lanusse, Joe Zuntz, Alexandre Boucaud, Santiago Casas, Minas Karamanis, David Kirkby, Denise Lanzieri, Austin Peel, and Yin Li. 2023. "JAX-COSMO: An End-to-End Differentiable and GPU Accelerated Cosmology Library." *The Open Journal of Astrophysics* 6 (April). <https://doi.org/10.21105/astro.2302.05163>.
:::

::: {#ref-dodelson .csl-entry}
Dodelson, Scott, and Fabian Schmidt. 2021. "13 - Probes of Structure: Lensing." In *Modern Cosmology (Second Edition)*, edited by Scott Dodelson and Fabian Schmidt, Second Edition, 373--99. Academic Press. https://doi.org/<https://doi.org/10.1016/B978-0-12-815948-4.00019-X>.
:::

::: {#ref-flatsky2 .csl-entry}
Gao, Zucheng, Alvise Raccanelli, and Zvonimir Vlah. 2023. "Asymptotic Connection Between Full- and Flat-Sky Angular Correlators." *Phys. Rev. D* 108 (August): 043503. <https://doi.org/10.1103/PhysRevD.108.043503>.
:::

::: {#ref-flatsky4 .csl-entry}
Gao, Zucheng, Zvonimir Vlah, and Anthony Challinor. 2023. "Flat-Sky Angular Power Spectra Revisited." <https://arxiv.org/abs/2307.13768>.
:::

::: {#ref-flatsky5 .csl-entry}
García-García, Carlos, David Alonso, and Emilio Bellini. 2019. "Disconnected Pseudo-$C_\ell$ Covariances for Projected Large-Scale Structure Data." *Journal of Cosmology and Astroparticle Physics* 2019 (11): 043. <https://doi.org/10.1088/1475-7516/2019/11/043>.
:::

::: {#ref-lognormal3 .csl-entry}
Hilbert, S., Hartlap, J., and Schneider, P. 2011. "Cosmic Shear Covariance: The Log-Normal Approximation." *A&A* 536: A85. <https://doi.org/10.1051/0004-6361/201117294>.
:::

::: {#ref-cosmology:lensing .csl-entry}
Kilbinger, Martin. 2015. "Cosmology with Cosmic Shear Observations: A Review." *Reports on Progress in Physics* 78 (8): 086901. <https://doi.org/10.1088/0034-4885/78/8/086901>.
:::

::: {#ref-grf2 .csl-entry}
Lang, Annika, and Jürgen Potthoff. 2011. *Monte Carlo Methods and Applications* 17 (3): 195--214. <https://doi.org/doi:10.1515/mcma.2011.009>.
:::

::: {#ref-lognormal2 .csl-entry}
Leclercq, Florent, and Alan Heavens. 2021. "[On the accuracy and precision of correlation functions and field-level inference in cosmology]{.nocase}." *Monthly Notices of the Royal Astronomical Society: Letters* 506 (1): L85--90. <https://doi.org/10.1093/mnrasl/slab081>.
:::

::: {#ref-flatsky3 .csl-entry}
Matthewson, William L., and Ruth Durrer. 2021. "The Flat Sky Approximation to Galaxy Number Counts." *Journal of Cosmology and Astroparticle Physics* 2021 (02): 027. <https://doi.org/10.1088/1475-7516/2021/02/027>.
:::

::: {#ref-flatsky .csl-entry}
Nicola, Andrina, Carlos García-García, David Alonso, Jo Dunkley, Pedro G. Ferreira, Anže Slosar, and David N. Spergel. 2021. "Cosmic Shear Power Spectra in Practice." *Journal of Cosmology and Astroparticle Physics* 2021 (03): 067. <https://doi.org/10.1088/1475-7516/2021/03/067>.
:::

::: {#ref-rasmussen .csl-entry}
Rasmussen, Carl Edward, and Christopher K. I. Williams. 2005. *[Gaussian Processes for Machine Learning]{.nocase}*. The MIT Press. <https://doi.org/10.7551/mitpress/3206.001.0001>.
:::

::: {#ref-flatsky6 .csl-entry}
Schneider, P., van Waerbeke, L., Kilbinger, M., and Mellier, Y. 2002. "Analysis of Two-Point Statistics of Cosmic Shear - i. Estimators and Covariances." *A&A* 396 (1): 1--19. <https://doi.org/10.1051/0004-6361:20021341>.
:::

::: {#ref-fwdmodel .csl-entry}
Zhou, Alan Junzhe, Xiangchong Li, Scott Dodelson, and Rachel Mandelbaum. 2023. "Accurate Field-Level Weak Lensing Inference for Precision Cosmology." <https://arxiv.org/abs/2312.08934>.
:::
:::::::::::::::::::::
