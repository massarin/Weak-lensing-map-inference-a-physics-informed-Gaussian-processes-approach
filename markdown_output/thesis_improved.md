# Introduction

Matter bends light. The theory of general relativity predicts that the presence of matter or energy changes the geometry of space and time, which in turn can cause what would otherwise be the straight path of a beam of light to curve. Take a distant source of light. If we assume the universe not to be empty, then between us and said source there exists a non trivial matter disposition. As light travels through everything that is in between us and the source, it gets blocked, bent and distorted. We call this phenomenon weak lensing. In practice what we measure is the shape of distant galaxies. These images do not show a distinct lensing feature individually, as such tiny changes can only be seen with a large number of sources. For example, we observe that galaxies have a tendency of aligning along a preferred axis, causing a statistical discrepancy in an otherwise seemingly isotropic universe. For further details on lensing, please refer to (Kilbinger 2015) (Bartelmann and Maturi 2017); for weak lensing (Blandford et al. 1991). The image of a distant galaxy can change shape or size. Changes in shape are fully characterised by the shear distortion $\Vec{\gamma}$ vector field, where the change in size is given by its magnitude, the convergence field $\kappa$. We lay out a theoretical framework for weak lensing in *Sec.* [2.1](#sec:weak lensing){reference-type="ref" reference="sec:weak lensing"} as well as details on the cosmology used in this thesis in *Sec.* [3.1.1](#subsec:cosmology){reference-type="ref" reference="subsec:cosmology"}.

A lot of work goes into translating a measurement of distant galaxies to its mathematically friendly counterpart $\Vec{\gamma}$. This is one of the reasons why we will not be dealing with it in this thesis, as it is outside of our scope. Instead we will be simulating our own convergence fields. We use a *Gaussian random field (GRF)* algorithm for the creation of Gaussianly distributed data. As well as lognormal transformations to create fields with a distribution that resembles more closely that in our universe. These transformations are listed in *Sec.* [2.2](#sec:field generation){reference-type="ref" reference="sec:field generation"}; we then use them to simulate our data as explained in *Sec.* [3.1](#sec:data simulation){reference-type="ref" reference="sec:data simulation"}. We also verify that the generated fields recover the fiducial power spectrum in *Sec.* [4.1.1](#sec:gaussian and lognormal fields){reference-type="ref" reference="sec:gaussian and lognormal fields"}.

::: wrapfigure
r0.45
:::

A *Gaussian process (GP)* usually assumes little prior knowledge about the data it is applied to. Current research in the field of cosmology views GPs as a machine learning tool to be trained. It is used to accelerate and optimise models (Mootoovaloo et al. 2020) (Supranta S. Boruah et al. 2022) (Karchev, Coogan, and Weniger 2022), as well as for its interpolation qualities applied to the reconstruction of functions determining the evolution of the universe (Shafieloo, Kim, and Linder 2012) (Seikel, Clarkson, and Smith 2012) (Holsclaw et al. 2010). Our work, however, is based on a different approach. We apply our prior knowledge about 2-point statistics in cosmology to create a fully informed GP. Restricting ourselves to 2D flat-sky weak lensing convergence fields, as shown in *Fig.* [\[tik:GP pipeline\]](#tik:GP pipeline){reference-type="ref" reference="tik:GP pipeline"}, we can:

- compute the angular power spectrum $C(\Theta)$ from a set of cosmological parameters $\Theta$,

- transform it in the convergence angular autocorrelation function $w(\Theta)$,

- create a zero mean GP with kernel given by said correlation function,

- evaluate the likelihood $\mathcal{L}$ of $\Theta$ given a set of data points $y$.

With a Bayesian approach we make use of this pipeline to infer the values of the cosmological parameters. Running a *Markov chain Monte Carlo (MCMC)* we can sample the posterior distribution of the cosmological parameters, in particular we will get contours for $\Omega_m$, $\sigma_8$ and $S_8$. Other than that, GPs have several other interesting properties at the field level. They are not only able to generate fields that recover the fiducial 2-point statistics, but are also able to reconstruct masked fields, a task that usually brings many challenges to $C_\ell$ estimation (Chon et al. 2004) (Brown, Castro, and Taylor 2005). In the field of weak lensing in particular, foreground objects like bright stars or galaxies can contaminate measurements, leading to the need of masking such a region, essentially removing the signal.

Here we list the advantages of our method:

- minimal information loss, as it is a map based method we use all available data points,

- it can be used as a likelihood for cosmological parameters inference,

- easily deals with masked fields, providing estimates with an associated uncertainty for the masked points.

Whilst some of the disadvantages:

- the conditioning process depends on the inverse of a correlation matrix, with a computational effort that grows as $\sim \mathcal{O}(n^3)$ for $n\propto$ data points, indicating possible scaling issues;

- due to the intrinsic Gaussianity of GPs, the distribution of the samples will be Gaussian, making it hard to apply them to other fields, say for example lognormal fields.

GPs in this thesis are presented in a general introduction in *Sec.* [2.3](#sec:gaussian process){reference-type="ref" reference="sec:gaussian process"}, followed by a detailed account of the computational methods used to recover a working kernel for GPs in *Sec.* [3.2](#sec:gaussian process kernel){reference-type="ref" reference="sec:gaussian process kernel"}. In our results we show their ability to create maps that follow the desired statistic *Sec.* [4.1.2](#sec:gaussian process priors){reference-type="ref" reference="sec:gaussian process priors"} and reconstruct data *Sec.* [4.2](#sec:gaussian process map reconstruction){reference-type="ref" reference="sec:gaussian process map reconstruction"}. We also present our attempt at cosmological parameters inference with GPs in *Sec.* [4.3](#sec:inference of cosmological parameters){reference-type="ref" reference="sec:inference of cosmological parameters"}.

It is important to note that throughout the thesis we follow the extremely useful guidelines set by the `Miko` pipeline (Zhou et al. 2023) on how to deal with discrete maps in weak lensing.

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

The way we computationally obtain $\kappa$'s 2-point statistics is with the Limber approximation. We use the code `jaxcosmo` (Campagne et al. 2023) to compute the 2D power spectrum $C(l)$ from the 3D matter power spectrum $P_\delta(k)$ with the efficient Limber approximation, $$C(l)=C_{\kappa\kappa}(l)=\int_0^{\chi*}\frac{d\chi}{\chi} W(\chi)W(\chi)P_\delta(k=\frac{l}{\chi},\chi).
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

Since we are dealing with 2D maps, our algorithm will have to be implemented in two dimensions. To do so, we decide to implement the algorithm in *Eq.* [\[eq:grf 1D\]](#eq:grf 1D){reference-type="eqref" reference="eq:grf 1D"} with the use of the Rayleigh distribution $\mathcal{R}(\sigma)$. Given two independent Gaussian random variables $X$ and $Y$, the random variable $R$ given by $$R=\sqrt{X^2+Y^2},$$ is said to be Rayleigh distributed. If we then multiply $R$ by the complex exponential $e^{i\theta}$ of a uniformly distributed random variable $\theta \sim \mathcal{U}(0,2\pi)$, we obtain a map of Gaussianly distributed complex numbers, which will substitute the $\mathcal{F}W$ term in *Eq.* [\[eq:grf 1D\]](#eq:grf 1D){reference-type="eqref" reference="eq:grf 1D"}. We showcase this equivalency in *Fig.* [2.1](#fig:rayleigh){reference-type="ref" reference="fig:rayleigh"} for distributions of $\mu=0$ and $\sigma=1$. The sequence of transformations in 2D therefore becomes, $$\phi(x) \equiv (\mathcal{F}^{-1} P^{1/2} R e^{i\theta})(x).
    \label{eq:grf 2D}$$

![[]{#fig:rayleigh label="fig:rayleigh"} Sampling a 2D Gaussian against a Rayleigh distributed amplitude with uniform complex phase. In purple is the complex number $X+iY$ with $X,Y \sim \mathcal{N}(0,1)$, in cyan is $Re^{i\theta}$ with $R\sim\mathcal{R}(1)$ and $\theta \sim \mathcal{U}(0,2\pi)$.](images/7_rayleigh.pdf){#fig:rayleigh width="\\textwidth"}

### Lognormal field

The universe today is not Gaussian. GRFs are able to capture the 2-point statistics of cosmological fields, but they cannot capture their skewed distribution. A possible way to get closer to the true distribution of the convergence field is with a lognormal transformation (Supranta Sarma Boruah, Rozo, and Fiedorowicz 2022) (Leclercq and Heavens 2021) (Hilbert, S., Hartlap, J., and Schneider, P. 2011) (Zhou et al. 2023). In this work we will denote lognormal transformations as $\mathcal{L}$ and adopt the following convention for both the field and the correlation function, $$\begin{gathered}
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
    \label{eq:gp prior}$$ Here we adopt the convention $\bm{K} = k(D_*,D_*)$. When drawing a sample function from *Eq.* [\[eq:gp prior\]](#eq:gp prior){reference-type="eqref" reference="eq:gp prior"}, computationally the operation is equivalent to drawing a vector from a multivariate Gaussian. What we obtain is a so-called prior, or priors, see *Fig.* [2.2](#fig:priors){reference-type="ref" reference="fig:priors"}.

![Prior samples of a GP with mean $m(\bm{x})=0$ and squared exponential kernel $k(\bm{x},\bm{x'})=e^{-(\bm{x}-\bm{x'})^2}$.](images/1_priors.pdf){#fig:priors width="\\textwidth"}

Let's now see how we can introduce knowledge of data points in this system. We divide the grid in training points $D$ and test points $D_*$. To each training point is associated a known value $\bm{y}$ and variance $\sigma_n^2$, whereas the values of the function at the test points $\bm{f}_*$ are unknown. We can summarise this as, $$\begin{bmatrix}
    \bm{y} \\
    \bm{f}_* \\
    \end{bmatrix}
    \sim \mathcal{N}\left(\bm{m}, \begin{bmatrix}
    \bm{K} + \sigma_n^2 I & \bm{K}_* \\
    \bm{K}^T_* & \bm{K}_{**} \\
    \end{bmatrix}\right)$$ where we have once again adopted the notation $\bm{K}=k(D,D)$, $\bm{K_{*}}=k(D,D*)$, $\bm{K_{**}}=k(D_*,D_*)$. At this point, one way to find samples that follow the data would be to blindly draw priors until we get something that goes through all data points. This would be inefficient and computationally wasteful. Instead, we make a better guess for the test function values. This operation is called conditioning, because we condition the joint Gaussians on the training points, this gives $$\bm{f}_* \mid D_*, D, \bm{y} \sim \mathcal{N}\left( \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{y} , \bm{K}_{**} - \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{K}_* \right).
\label{eq:conditioning}$$ Conditioning can therefore give rise to what is called a posterior sample, *Fig.* [2.3](#fig:posteriors){reference-type="ref" reference="fig:posteriors"}. The result is still a multivariate Gaussian, but the mean and variance given by *Eq.* [\[eq:conditioning\]](#eq:conditioning){reference-type="eqref" reference="eq:conditioning"} generate samples that are a better guess of the behaviour of the function outside of the training points.

![[]{#fig:posteriors label="fig:posteriors"} Summary plot of a GP conditioned to some data. The cyan line is the mean of the GP and the filled region corresponds to $1\sigma$. The purple lines are posterior samples, which are distributed Gaussianly around the mean. The data points are clearly marked in black, they are also the points where all samples converge to.](images/1_posteriors.pdf){#fig:posteriors width="\\textwidth"}

# Methods

## Data simulation {#sec:data simulation}

### Cosmology {#subsec:cosmology}

::: wraptable
r2.8cm

               Fiducial
  ------------ ----------
  $\Omega_m$   0.3
  $\Omega_b$   0.05
  $\Omega_k$   0
  $h$          0.7
  $n_s$        0.97
  $\sigma_8$   0.8
  $w_0$        -1
  $w_a$        0
:::

This work follows in the general footsteps of data analysis of weak lensing surveys like *HSC* (Hikage et al. 2019) and *KiDS* (Köhlinger et al. 2017)(Asgari, Marika et al. 2021), as we aim to replicate their methodologies. Throughout the work, we assume a fiducial cosmology of fixed parameter values as shown in *Tab.* [\[tab:fiducial_cosmology\]](#tab:fiducial_cosmology){reference-type="ref" reference="tab:fiducial_cosmology"}. In particular, all data maps will be generated from a power spectrum following this cosmology. We will refer to this power spectrum as the fiducial power spectrum $C(l)$. A leading modelling choice comes with the redshift distribution $n(z)$. We model it as a Smail-type distribution (Smail et al. 1995)(Kirk et al. 2012), $$n(z)=z^\alpha \exp{\left[-\left(\frac{z}{z_0}\right)^\beta\right]}.$$ The choice of parameters has been made to emulate bin 5 of the *KiDS1000* survey (Hildebrandt, H. et al. 2021), with parameters $\alpha=3.5$, $\beta=4.5$, $z_0=1$.

<figure id="fig:smail">
<p><embed src="images/2_smail.pdf" /> <span id="fig:smail" data-label="fig:smail"></span></p>
</figure>

### Map making pipeline {#sec:map making pipeline}

When dealing with maps of finite size $(L, L)$ and pixel resolution $(N,N)$, Fourier space is going to have boundaries, just as real space does. These limits are given by $$\begin{gathered}
    l_{\text{min}} = \frac{2\pi}{L},\\
    l_{\text{max}} = \frac{2\pi}{L} N.
\end{gathered}$$ Therefore, a map of size $(10^{\circ},10^{\circ})$ and a grid $64\times64$ will have limits $(l_{\text{min}}, l_{\text{max}}) = (36, 2304)\text{rad}^{-1}$. Now that we have the physical range for the power spectrum, we can generate data.

<figure id="tik:cw">

<figcaption>Sequence of transformations used to generate Gaussian and lognormal maps starting from the fiducial angular power spectrum. The top branch shows how to generate a GRF which when transformed to a lognormal field, follows the fiducial <span class="math inline">\(C(l)\)</span>. The bottom branch is a standard GRF realisation starting from the fiducial <span class="math inline">\(C(l)\)</span>. <span class="math inline">\(L\)</span> and <span class="math inline">\(G\)</span> stand for lognormal and Gaussian respectively. <span class="math inline">\(\mathcal{H}\)</span> is the Hankel transformation, and tilde refers to intermediate results.</figcaption>
</figure>

To generate a GRF, we employ the algorithm mentioned in *Eq.* [\[eq:grf 2D\]](#eq:grf 2D){reference-type="eqref" reference="eq:grf 2D"}. However, in making a lognormal field, the matter is a bit more complicated. Any GRF on which we apply the lognormal transformation $\mathcal{L}_\kappa$, from *Eq.* [\[eq:L_k\]](#eq:L_k){reference-type="eqref" reference="eq:L_k"}, becomes a lognormal field. The reason we do not just lognormal transform any field is given by the fact that they would not recover the fiducial power spectrum $C(l)$. Our goal is therefore to find a transfer GRF $\tilde{\kappa}^G$ which, when transformed lognormally, gives rise to a lognormal field $\kappa^L$ that recovers $C(l)$. To do so, we follow the sequence of transformations illustrated in the top branch of *Fig.* [3.2](#tik:cw){reference-type="ref" reference="tik:cw"}.

### Noise and mask

![Approximately $10\%$ mask applied to the data. Size $(10^{\circ},10^{\circ})$ and grid $64\times64$.](images/5_random_and_blocks_mask.pdf){#fig:mask width="50%"}

As all data is being simulated, we only take into account the so-called shape noise, which is due to the intrinsic distribution of ellipticities and angle formed with respect to us. GPs will treat each pixel of the map as a random variable Gaussianly distributed with standard deviation given by (Croft et al. 2017), $$\sigma_\text{noise} = \frac{\sigma_e}{\sqrt{n_g A_{px}}}.
    \label{eq:noise}$$ We use values of $\sigma_e=0.26$, $n_g= 4, 10, 30, 100 \text{ galaxies}/\text{arcmin}^2$, and a pixel area given by the pixel resolution squared, $A_{px}=(L/N)^2$. For our highest-resolution run, we have $N=64$ and use $n_g = 10 \text{ galaxies}/\text{arcmin}^2$, which results in a noise standard deviation of $\sigma_\text{noise} \sim 0.0088$. The mask being used as seen in *Fig.* [3.3](#fig:mask){reference-type="ref" reference="fig:mask"}, covers approximately $10\%$ of the patch (Grewal, Zuntz, and Tröster 2024). We keep the noise and mask random seeds fixed throughout the work.

## Kernel {#sec:gaussian process kernel}

The kernel of a Gaussian process is given by a function of the form $k(x,y)$. It takes in two points, $x$ and $y$, and returns the value of their correlation. In our case, specifically, $x$ and $y$ will be two points in a grid of shape $(N,N)$, and the kernel function will be the convergence angular autocorrelation function. As all code used for this paper is written in `JAX` (Bradbury et al. 2018) we opt for the use of the library `tinygp` (Foreman-Mackey et al. 2024) for all Gaussian process computations. `tinygp` allows for the use of a custom kernel with a custom `evaluate` method, which takes two points on the grid and returns the correlation value. We follow with two `Python` pseudocodes of our kernel implementations.

``` {#lst:hankel .python language="Python" label="lst:hankel" caption="\\lstinline[keepspaces=true" breaklines=""}
{kernel_Hankel} uses the helper function \code{Hankel} which returns a 1D callable correlation function \code{w}. Then finds the euclidean distance between $x$ and $y$ and evaluates the correlation function at that point. We will discuss how we perform the Hankel transformation in the following section.]
class kernel_Hankel:
    def __init__(self, cl, N, L):
        self.w   = Hankel(cl, N, L)
        self.r   = L / N
        
    def evaluate(self, x, y):
        theta    = self.r * sqrt(sum(x - y))
        return self.w(theta)
```

``` {#lst:FFT .python language="Python" label="lst:FFT" caption="\\lstinline[keepspaces=true" breaklines=""}
{kernel_FFT} performs a 2D Fourier transform on the power spectrum \code{cl2D}. This returns a 2D array that is the correlation function. Then to evaluate \code{w2D} we need two indices. These are given by the difference of $x$ and $y$ component wise. Furthermore we have to be careful about possible mismatches between the shape of \code{cl2D} and the grid of our map. For this we have the renormalisation factor \code{r}. We will discuss further how we get \code{cl2D} in the following section.]
class kernel_FFT:
    def __init__(self, cl2D, N, L):
        M        = sqrt(cl2D.size)
        self.w2D = abs(ifft2(cl2D)) * M**2 / L**2
        self.r   = M / N
        
    def evaluate(self, x, y):
        d0       = self.r * abs(x[0] - y[0])
        d1       = self.r * abs(x[1] - y[1])
        return self.w2D[int(d0)][int(d1)]
```

### Hankel transform {#sec:Hankel transform}

In order to build a Gaussian process kernel, we need to find the correlation function that best describes the data. The way we do this is by computing the angular power spectrum and transforming it in the corresponding angular correlation function. Let's explore the previously discussed flat-sky relation between angular power spectrum and correlation function given by *Eq.* [\[eq:flatsky hankel\]](#eq:flatsky hankel){reference-type="eqref" reference="eq:flatsky hankel"}. This particular integral of a Bessel function is also known as a zeroth order Hankel transformation, $$w(\theta) = \int \frac{dl}{2\pi} l C(l) J_0(l\theta).
    \label{eq:C-w hankel}$$ We will explore two methods for computing this integral: the *integration* method *Sec.* [3.2.1.1](#sec:integration method){reference-type="ref" reference="sec:integration method"} and the *FFTlog* method *Sec.* [3.2.1.2](#sec:FFTlog method){reference-type="ref" reference="sec:FFTlog method"}.

#### Integration {#sec:integration method}

Integration is the most straight forward way to evaluate the integral, but it requires to implement an algorithm for the approximation of the Bessel function $J_0$. The advantages of this method:

- it is easy to integrate over the correct $l$-range, from $l_{\text{min}}$ and $l_{\text{max}}$, a freedom that we do not have with the FFTlog.

The disadvantages:

- integration is computationally slow, especially when dealing with highly oscillatory behaviour introduced by the Bessel function, which requires fine sampling.

#### FFTlog {#sec:FFTlog method}

The FFTlog method (Simonović et al. 2018) is a fast implementation of the Hankel transformation. In fact it simplifies *Eq.* [\[eq:C-w hankel\]](#eq:C-w hankel){reference-type="eqref" reference="eq:C-w hankel"} by assuming a power decomposition of $C(l)$. Such a decomposition is achievable by taking the *fast Fourier transformation (FFT)* in $\log k$, hence the name FFTlog. The power spectrum becomes, $$C(l)=\sum_\alpha c_\alpha l^{\upsilon + i\eta_\alpha}.$$ Substituting in *Eq.* [\[eq:C-w hankel\]](#eq:C-w hankel){reference-type="eqref" reference="eq:C-w hankel"}, $$w(\theta) = \sum_\alpha c_\alpha \int_0^\infty \frac{dl}{2\pi} l^{\upsilon + i\eta_\alpha+1} J_0(l\theta).$$ Take $x=l\theta$ and $s_\alpha-1=\upsilon + i\eta_\alpha+1$, $$w(\theta) = \sum_\alpha c_\alpha \theta^{-s_\alpha} \int_0^\infty \frac{dx}{2\pi} x^{s_\alpha-1} J_0(x).$$ Lastly we recognise $\int_0^\infty dx x^{s-1}J_0(x) = \frac{2^{s-1}}{\pi}\sin(\pi s/2) [\Gamma(s/2)]^2$, a Mellin transform. Using this tabulated result we conclude that the correlation is given by the sum, $$w(\theta) = \frac{1}{2\pi^2}\sum_\alpha c_\alpha \theta^{-s_\alpha}2^{s_\alpha-1}\sin(\pi s_\alpha/2) [\Gamma(s_\alpha/2)]^2.$$ For the Mellin transform identity to hold analytically, the integral bounds have to go from 0 to $\infty$. Although computationally we don't need to consider such a wide range, we still have to broaden the integration limits to something larger than our $l$-range; so as to avoid ringing effects. Experimentally we have found that extending the $l$-range between $l_{\text{min}}/4$ and $l_{\text{max}}$, is enough to compensate for such effects. The advantages of this method:

- the FFTlog method is ultimately much faster than the integration method.

The disadvantages:

- the widening of the $l$-range needed to avoid ringing effects inevitably adds power to the correlation function resulting in a higher variance and overall amplitude.

### Fourier transform

The second transformation that we can use to go from power spectrum to correlation function, is the Fourier transformation discussed in *Eq.* [\[eq:flatsky fft\]](#eq:flatsky fft){reference-type="eqref" reference="eq:flatsky fft"}. It is a more fundamental relation than the Hankel transformation as it does not assume that $l$ is radially symmetric. In our case, low resolution, coupled with a square map, means that the radial assumption might not apply. Note that, the lowest resolution grid we use is $32\times32$, with $L/N \sim 19$ arcmin; which is one order of magnitude worse than today's weak lensing data, around $\sim 3$ arcmin according to (Zhou et al. 2023). In the following *Sec.* [3.2](#sec:gaussian process kernel){reference-type="ref" reference="sec:gaussian process kernel"} we will find experimentally that the Hankel methods described above do not work well with our GP setup. For this reason, we explore this method of conversion between angular power spectrum and correlation function, $$w(\theta)=\int\frac{d^2l}{4\pi^2}e^{-i\bm{l}\cdot\bm{\theta}}C(l).
    \label{eq:C-w fft}$$ As computers can only deal with discrete functions, it is important to note that we will be performing a *discrete Fourier transformation (DFT)*. We will use the widely known FFT algorithm to compute DFTs. In particular we use JAX's implementation of the 2D FFT algorithm, `jax.numpy.fft.ifft2`.

Let us find the relation between continuous Fourier transformation and DFT. The definitions of continuous and discrete Fourier transformations in 1D, are respectively: $$\begin{aligned}
    \mathcal{F}^{-1}&=\int\frac{dk}{2\pi}e^{ikx}, \label{eq:F}\\
    \text{F}^{-1}&=\frac{1}{N}\sum_p e^{ik_px}. \label{eq:DFT}
\end{aligned}$$ First of all, a DFT is dimensionless. Secondly, it is discrete and bounded. We can therefore rewrite *Eq.* [\[eq:F\]](#eq:F){reference-type="eqref" reference="eq:F"} using the substitution $k(p)=2\pi \frac{p}{L}$ to discretise k-space, $$\int\frac{dk}{2\pi}e^{ikx} = \int\frac{dp}{L} e^{ik(p)x} = \frac{1}{L}\sum_p e^{ik_px}.$$ Applying the definition of DFT as seen in *Eq.* [\[eq:DFT\]](#eq:DFT){reference-type="eqref" reference="eq:DFT"}, it follows that in 1D $$\mathcal{F}^{-1}=\frac{N}{L}\text{F}^{-1}.$$ Which means that the correlation function is given by a *backwards* normalised inverse DFT to be scaled by a factor $(N/L)^d$, where $d$ is the dimension of the considered space. In our case, $d=2$.

In order to perform a FFT in 2D, we will need a two dimensional extension of the angular power spectrum. We make use of its radial symmetry with respect to $\bm{l}=(l_x,l_y)$ and create a 2D grid of shape $(M,M)$ as shown in *Fig.* [3.4](#tik:1D to 2D){reference-type="ref" reference="tik:1D to 2D"}.

<figure id="tik:1D to 2D">

<figcaption>1D to 2D extension of the power spectrum <span class="math inline">\(C(l)\)</span></figcaption>
</figure>

Now that we have a 2D power spectrum we can take the inverse two dimensional fast Fourier transformation to obtain a 2D correlation function. In practice, we will test two grids, which we name *full-range FFT* method and *half-range FFT* method.

#### Full-range FFT

The full-range FFT is defined by a grid of shape $(2N,2N)$. Since the grid is radial, it will be centered. This implies that if we want to keep information of all $N$ modes, $$\frac{2\pi}{L},\, \frac{4\pi}{L},\,\cdot\cdot\cdot\,,\, \frac{2\pi}{L}N,$$ the grid will have to be at least of shape $M=2N$. The advantages of this method:

- it keeps information on the full range of modes.

The disadvantages:

- it introduces rounding errors, as the field has shape $(N,N)$ and not all of the possible distance combinations of such a grid are covered bya grid of shape $(2N,2N)$.

#### Half-range FFT

The half-range FFT is defined by a grid of shape $(N,N)$. The advantages of this method:

- has the perk of having no shape mismatch between field and correlation function.

The disadvantages:

- it loses half of the $l$-range, missing information on small scales.

# Results

## Power spectrum recovery

### Gaussian and lognormal fields {#sec:gaussian and lognormal fields}

We begin by testing the consistency of our Gaussian and lognormal maps generation pipeline.

![[]{#fig:fields dist label="fig:fields dist"} Comparison of a Gaussian map, on the left, with a lognormal map on the right. Both maps arise from the same random seed. The colorbar has been adjusted to enhance the differences between the two. The histogram plot shows the clear difference in the map distributions.](images/4_Gaussian_lognormal_dist.pdf){#fig:fields dist width="100%"}

We show example realisations of the two fields in *Fig.* [4.1](#fig:fields dist){reference-type="ref" reference="fig:fields dist"}, Gaussian on left and lognormal on the right. There's a visible difference between the two, as it can be seen clearly from the distribution plot. The main check to perform is for testing whether the generated fields recover the theoretical power spectrum. *Fig.* [4.2](#fig:check fields){reference-type="ref" reference="fig:check fields"} shows that this is the case for the Gaussian fields. They recover the fiducial $C(l)$ within a few percent error, with larger deviations $\sim 5\%$ at the low and high ends of the $l$-range. Instead, lognormal fields present deviations $\gtrsim 10\%$. As the lognormal transformations we use have been reported by different sources (Zhou et al. 2023)(Supranta Sarma Boruah, Rozo, and Fiedorowicz 2022), the issue must lie with our `JAX` implementation of the Hankel transformation. Resolving such issues could be achieved by future iterations of this work. In this work, we restrict ourselves to the use of Gaussian fields, as it is enough to prove our thesis and show that Gaussian processes can be applied to cosmological fields.

![[]{#fig:check fields label="fig:check fields"} Power spectrum estimation from Gaussian and lognormal maps. Mean and standard deviation are calculated with 500 realisation of both fields.](images/4_Gaussian_lognormal_check.pdf){#fig:check fields width="100%"}

### Gaussian process priors {#sec:gaussian process priors}

First, we test the ability of the kernels we have built in *Sec.* [3.2](#sec:gaussian process kernel){reference-type="ref" reference="sec:gaussian process kernel"} to recover the power spectrum of our cosmology.

![[]{#fig:check methods label="fig:check methods"} Reconstructed power spectrum from prior sample of GP with the four proposed kernels: integration, FFTlog, full-range FFT, half-range FFT and sinc FFTlog. Mean and standard deviation are calculated with 500 prior samples from each GP. ](images/3_kernel_comparison.pdf){#fig:check methods width="\\textwidth"}

We test five models in *Fig.* [4.3](#fig:check methods){reference-type="ref" reference="fig:check methods"}: integration, FFTlog, full-range FFT, half-range FFT and sinc FFTlog. The first four methods are described in the Gaussian process kernels *Sec.* [3.2](#sec:gaussian process kernel){reference-type="ref" reference="sec:gaussian process kernel"}, whereas the sinc FFTlog referes to a FFTlog model on which we applied smoothing, by multiplying the power spectrum by a factor of $sinc^4(l\frac{L}{2\pi N})$. The recovered power spectra are plotted against the fiducial power spectrum, or smoothed power spectrum for the sinc FFTlog. Mean and standard deviation associated to the plots are calculated from 500 samples. As expected the integration, FFTlog and full-range FFT perform similarly, as they all contain the same ammount of information. As these models deviate so strongly from the fiducial power spectrum we tried applying smoothing, which helps to recover half of the $l$-range at large scales. The only method that seems to be consistently recovering the fiducial power spectrum is the half-range FFT. One could argue that due to the inherent discreteness and boundedness of the fields we are working with, using FFTs is the most natural choice; also, half-range FFT uses the only grid that recovers a correlation function of the same shape as the field without having to perform binning.

![[]{#fig:check cosmology label="fig:check cosmology"} Reconstructed power spectrum from prior samples of a GP, as a function of $\{\sigma_8, S_8\}$. Mean and standard deviation are calculated with 500 prior samples for each different cosmology.](images/3_cosmology_comparison.pdf){#fig:check cosmology width="\\textwidth"}

We have also tested the efficacy of the half-range FFT model for different cosmologies of values $\{\sigma_8, S_8\}$ equal to $\{0.4,0.2\}$, $\{1.2,1.5\}$ and, our fiducial cosmology, $\{0.8,0.8\}$. As *Fig.* [4.4](#fig:check cosmology){reference-type="ref" reference="fig:check cosmology"} shows, the model is independent of the choice of cosmology. From here on the results will be presented assuming a kernel built with the half-range FFT model.

## Gaussian process map reconstruction {#sec:gaussian process map reconstruction}

Armed with a reliable kernel, let's embark upon the journey of reconstructing a heavily masked cosmological field. What we will do is: create a noiseless GRF in the fiducial cosmology *Tab.* [\[tab:fiducial_cosmology\]](#tab:fiducial_cosmology){reference-type="ref" reference="tab:fiducial_cosmology"}, *True* map; apply a mask to obtain the *Data* map; condition a Gaussian process which assumes the fiducial cosmology. *Fig.* [4.5](#fig:GP reconstruction summary){reference-type="ref" reference="fig:GP reconstruction summary"} lists the result of this operation, showing the resulting mean $\mu$ and standard deviation $\sigma$ of the conditioned GP. We also plot the ratio between residuals $\Delta=\mu-$*True* and standard deviation squared, to test the goodness of fit of our model, the values of the map sum up to $\chi^2 \sim 2495$. With the mask covering $\nu=2353$ pixels, we obtain $\chi^2 / \nu = 1.06$. Of course, this is just a noiseless application, which is unreasonable for a real application.

![[]{#fig:GP reconstruction summary label="fig:GP reconstruction summary"}Summary of field reconstruction abilities of a Gaussian process conditioned on data. The left column shows the masked GRF, which is our data. The middle column shows the true GRF without masks and a posterior sample drawn from the conditioned GP. The right column shows maps of the mean, standard deviation and residuals over standard deviation squared of the conditioned GP. Regions of higher uncertainty correspond to the masked regions. The residuals over standard deviation map also shows how regions with low mask recover the data.](images/2_summary.pdf){#fig:GP reconstruction summary width="\\textwidth"}

## Inference of cosmological parameters {#sec:inference of cosmological parameters}

To test the ability of Gaussian processes to recover cosmological parameters without any prior knowledge except a noisy and masked map, we perform a MCMC simulation to infer the posterior distributions of $\sigma_8$ and $S_8$. We use the convention $$S_8 = \sigma_8 \sqrt{\frac{\Omega_m}{0.3}},
    \label{eq:S8}$$

::: wraptable
l3.7cm

               Prior
  ------------ ---------------------------
  $S_8$        $\mathcal{U}[0.565,1.78]$
  $\sigma_8$   $\mathcal{U}[0.4,1]$
  $\Omega_m$   $\mathcal{U}[0.15,0.95]$
:::

to infer deterministically a posterior for $\Omega_m$. Such a reparametrisation is needed due to the strong degeneracy between $\sigma_8$ and $\Omega_m$. *Eq.* [\[eq:S8\]](#eq:S8){reference-type="eqref" reference="eq:S8"} breaks this degeneracy, changing the geometry of the sampling space and making the sampling more consistent. The model assumes uninformed flat priors for the cosmological parameters, as shown in *Tab.* [\[tab:priors\]](#tab:priors){reference-type="ref" reference="tab:priors"}, such prior bounds are also in accordance with the `jaxcosmo` release (Campagne et al. 2023). The likelihood of the model is given by a Gaussian process distribution conditioned on *Data*, with a standard deviation equal to the noise applied to the map. The analysis is coded with `numpyro` (Phan, Pradhan, and Jankowiak 2019) (Bingham et al. 2019), using a the *No-U-Turn Sampler (NUTS)* method with `max_tree_depth=16`, `target_accept_prob=0.8`. We simulate 8 chains for the $32\times32$ grid and 4 chains for the $64\times64$. Each chain performs 1000 warmup steps and 3000 samples.

### One parameter

As a first step and for a consistency check, we run the inference model for one cosmological parameter, keeping all others fixed. Using a $64\times64$ grid with $n_g=10 \text{ galaxies}/\text{arcmin}^2$. In *Fig.* [4.6](#fig:MCMC one parameter){reference-type="ref" reference="fig:MCMC one parameter"} we show the inferred distribution for both $\sigma_8$ and $\Omega_m$. We find that we are able to recover the true value for both parameters within two sigmas, $\sigma_8 = 0.776\pm0.015$ and $\Omega_m = 0.284\pm0.010$. We notice a slight tendency of the inferred distribution to be biased low; a tendency we also observe next for both sampled parameters, $S_8$ and $\sigma_8$.

<figure id="fig:MCMC one parameter">
<div class="minipage">
<embed src="images/6_MCMC_sigma_parameters.pdf" />
</div>
<div class="minipage">
<embed src="images/6_MCMC_omega_parameters.pdf" />
</div>
<figcaption><span id="fig:MCMC one parameter" data-label="fig:MCMC one parameter"></span> Inferred posterior distribution of <span class="math inline">\(\sigma_8\)</span> on the left and <span class="math inline">\(\Omega_m\)</span> on the right. Dotted lines indicate the <span class="math inline">\(1\sigma\)</span> level. Truth values corresponding to the fiducial cosmology are indicated in blue.</figcaption>
</figure>

### Two parameters

#### Effect of noise

::: {#tab:inferred cosmological parameters}
  $\sigma_\text{noise}$       $0.0069$          $0.0044$          $0.0025$          $0.0014$
  ----------------------- ----------------- ----------------- ----------------- -----------------
  $S_8$                    $0.716\pm0.043$   $0.733\pm0.040$   $0.747\pm0.041$   $0.752\pm0.042$
  $\sigma_8$               $0.645\pm0.157$   $0.628\pm0.158$   $0.632\pm0.166$   $0.631\pm0.170$
  $\Omega_m$               $0.423\pm0.164$   $0.469\pm0.175$   $0.485\pm0.186$   $0.497\pm0.193$

  : List of inferred cosmological parameters inferred by the model with a small $32\times32$ grid and for a fixed true GRF realisation. We present the cosmological parameters inferred as we increase the noise level, corresponding to $n_g = 4$, $10$, $30$ and $100 \text{ galaxies}/\text{arcmin}^2$.
:::

We perform some tests on low resolution $32\times32$ grids to see the effect that the noise level has on the recovered parameters, see *Tab.* [4.1](#tab:inferred cosmological parameters){reference-type="ref" reference="tab:inferred cosmological parameters"}. Here we report the inferred cosmological parameters for one data realisation and different noise levels, corresponding respectively to $n_g = 4$, $10$, $30$ and $100 \text{ galaxies}/\text{arcmin}^2$, see *Eq.* [\[eq:noise\]](#eq:noise){reference-type="eqref" reference="eq:noise"}. The inferred value of $S_8$ can vary as much as a full $\sigma$ between high and low noise runs. Keeping in mind that $\sigma_8$ and $\Omega_m$ are extremely unreliable due to relative uncertainties of $\sim 25-30\%$ caused by the degeneracy: as a general trend we notice $\Omega_m$ gets bigger when $\sigma_8$ gets smaller with less noise.

#### Inferred cosmological parameters

Running the model for a larger $64\times64$ grid with $n_g=10 \text{ galaxies}/\text{arcmin}^2$, gives much better constraints on the cosmological parameters. We present the values recovered by the posterior distributions, listed as follows in *Tab.* [4.2](#tab:inferred cosmological parameters (64,64)){reference-type="ref" reference="tab:inferred cosmological parameters (64,64)"}.

::: {#tab:inferred cosmological parameters (64,64)}
        $S_8$          $\sigma_8$        $\Omega_m$
  ----------------- ----------------- -----------------
   $0.762\pm0.028$   $0.745\pm0.151$   $0.353\pm0.143$

  : Mean and sigma values recovered from the inferred distributions of the cosmological parameters.
:::

*Fig.* [4.7](#fig:MCMC two parameters){reference-type="ref" reference="fig:MCMC two parameters"} shows the inferred posterior distributions and contours for the three cosmological parameters $\sigma_8$, $\Omega_m$ and $S_8$. Looking at the contours, we obtain the well known banana-shaped degeneracy between $\sigma_8$ and $\Omega_m$. The $S_8$ and $\Omega_m$ contour presents sharp cuts for high and low $\Omega_m$, indicating an issue with the bounds of the uniform priors imposed. Unfortunately the `jaxcosmo` package does not allow for the choice of priors to be wider than what shown in *Tab.* [\[tab:priors\]](#tab:priors){reference-type="ref" reference="tab:priors"}, as the model then starts to have divergent samples.

![[]{#fig:MCMC two parameters label="fig:MCMC two parameters"} Inferred posterior distributions of $S_8$, $\sigma_8$ and $\Omega_m$. For noise level $\sigma_\text{noise}\sim 0.0088$. Contours indicate the $1\sigma$ and $2\sigma$ credible interval respectively. Dotted lines indicate the $1\sigma$ level. Truth values corresponding to the fiducial cosmology are indicated in blue.](images/5_MCMC_two_parameters.pdf){#fig:MCMC two parameters width="\\textwidth"}

### Posterior checks

Following the two parameter inference model, we perform some posterior checks at the map level (Porqueres et al. 2021). *Fig.* [4.9](#fig:MCMC summary){reference-type="ref" reference="fig:MCMC summary"} sums up the ability of the model to recover the true map, noiseless and unmasked. Here we present the run with noise level $\sigma_\text{noise}\sim 0.0088$ and a $64\times64$ grid. We show the mean and standard deviation for the sample with highest likelihood out of the $12000$. The mean field $\mu$ is visibly different to the true field in the masked regions and it seems to be of overall lower amplitude. The sample map is comparable to the noisy data; which is to be expected, as the internal noise given to the Gaussian process is the same as the noise level of the data. The standard deviation map $\sigma$ presents an overall amplitude comparable to the noise level $\sim 0.010$, with higher values for the masked regions. Summing up the map values of the residuals divided by standard deviation squared, we obtain a $\chi^2\sim 1297.4$. Compared to the number of free parameters $\nu$ in our inference model, which for a $10\%$ mask and a $64\times64$ grid, is $\nu=3689$. The value of $\chi^2$ therefore seems to be low, indicating that the noise level assumed by the GP is overestimated. This is supported by the fact that the sample map looks just as noisy as the data, according to *Fig.* [4.8](#fig:residuals vs noise){reference-type="ref" reference="fig:residuals vs noise"}, its distribution is in fact just as wide as the noise.

<figure id="fig:residuals vs noise">
<embed src="images/5_residuals_vs_noise.pdf" style="width:50.0%" />
<p><em>Residuals</em></p>
<figcaption><span id="fig:residuals vs noise" data-label="fig:residuals vs noise"></span> Residual distributions of the mean and sample compared to noise. The mean is less spread, whereas the sample is wider.</figcaption>
</figure>

![[]{#fig:MCMC summary label="fig:MCMC summary"} Summary of the two parameter inference at the map level. The left column shows the masked and noisy GRF realisation used, which is our data. The middle column shows the true GRF and a sample from the conditioned GP. The right column shows maps of the mean, standard deviation and residuals over standard deviation squared resulting from the numpyro model sample with highest likelihood. Regions of higher uncertainty correspond to the masked regions.](images/5_summary.pdf){#fig:MCMC summary width="\\textwidth"}

# Conclusion

We have hereby introduced the tool of Gaussian processes to the landscape of map inference of cosmological fields, in particular weak lensing convergence. We considered how the 2-point statistics of cosmological fields changes when we are dealing with bounded and discrete maps in *Sec.* [2.1](#sec:weak lensing){reference-type="ref" reference="sec:weak lensing"}. We discussed the realisation of Gaussian and lognormal fields in *Sec.* [2.2](#sec:field generation){reference-type="ref" reference="sec:field generation"}, and showed their ability to recover the 2-point statistics that they encode, in *Sec.* [4.1.1](#sec:gaussian and lognormal fields){reference-type="ref" reference="sec:gaussian and lognormal fields"}. We have included masking and noise to the data to simulate realistic maps in *Sec.* [3.1](#sec:data simulation){reference-type="ref" reference="sec:data simulation"}. We have shown that it is possible to apply physical knowledge about the 2-point correlation function of a cosmological field in order to set up a Gaussian process able to produce a Gaussian realisation of such a field. We considered different set ups for the Gaussian process kernel in *Sec.* [3.2](#sec:gaussian process kernel){reference-type="ref" reference="sec:gaussian process kernel"} and showed how they fare against one another in *Sec.* [4.1.2](#sec:gaussian process priors){reference-type="ref" reference="sec:gaussian process priors"}, ultimately proving empirically that the half-range FFT model is the best. In *Sec.* [4.2](#sec:gaussian process map reconstruction){reference-type="ref" reference="sec:gaussian process map reconstruction"} we present an application of Gaussian processes to a noiseless masked convergence map, in order to showcase its ability to reconstruct a heavily masked map. Finally we present our results for the cosmological parameters inference with GPs, conditioning on noisy and masked data. When running the inference model on one cosmological parameter we recover both parameters within two sigmas, $\sigma_8 = 0.776\pm0.015$ and $\Omega_m = 0.284\pm0.010$. For the two parameter inference we observe the well known banana-shaped degeneracy between $\sigma_8$ and $\Omega_m$, as well as recovering $0.762\pm0.028$ within two sigmas.

In future studies GPs could be tested on maps with larger grids. In order to achieve a resolution of $\sim 3$ arcmin with a map of size $(10^\circ,10^\circ)$, a $200\times200$ grid is needed. Too big for a GP. The bottleneck is given by the inversion of the kernel matrix, see [\[eq:conditioning\]](#eq:conditioning){reference-type="eqref" reference="eq:conditioning"}. Approximations of this operation could enable the use of GPs on larger grids. This can lead to the possibility of applying this method on current weak lensing catalogues and perhaps even full sky catalogues. Another pathway to explore are lognormal fields, as they do a much better job at simulating data than GRFs. Due to GPs being Gaussian, their associated likelihood is not suitable to treat lognormal fields. A modified likelihood could therefore unlock a correct application of GPs to lognormal fields.

## Acknowledgments {#acknowledgments .unnumbered}

This project wouldn't have been possible without the author of the idea, Dr. Tilman Tröster. You guided me through my first real research experience and I am grateful. Thank you Veronika Oehl for always being there and for the very helpful discussions. I also express my gratitude to the Cosmology group at ETH, led by Prof. Alexandre Réfrégier. Hearing about my every progress every Monday morning for six months, couldn't have been easy, thank you. It has been an incredible experience, long and grinding, which I embarked upon with my friends and colleagues Tommaso and Pietro. Thank you for making these past few months memorable. Thanks to Guido van Rossum for giving us `Python`. Thank you Mia, for your unconditional support, *you* keep me grounded. Non sarei qua senza di te mamma, grazie.

\[Interactive diagram - see LaTeX source\]

::::::::::::::::::::::::::::::::::::::::::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}
::: {#ref-cosmology:kids1000 .csl-entry}
Asgari, Marika, Lin, Chieh-An, Joachimi, Benjamin, Giblin, Benjamin, Heymans, Catherine, Hildebrandt, Hendrik, Kannawadi, Arun, et al. 2021. "KiDS-1000 Cosmology: Cosmic Shear Constraints and Comparison Between Two Point Statistics." *A&A* 645: A104. <https://doi.org/10.1051/0004-6361/202039070>.
:::

::: {#ref-cosmology:lensing2 .csl-entry}
Bartelmann, M., and M. Maturi. 2017. "Weak Gravitational Lensing." *Scholarpedia* 12 (1): 32440. <https://doi.org/10.4249/scholarpedia.32440>.
:::

::: {#ref-grf .csl-entry}
Bertschinger, Edmund. 2001. "Multiscale Gaussian Random Fields and Their Application to Cosmological Simulations." *The Astrophysical Journal Supplement Series* 137 (1): 1. <https://doi.org/10.1086/322526>.
:::

::: {#ref-numpyro2 .csl-entry}
Bingham, Eli, Jonathan P. Chen, Martin Jankowiak, Fritz Obermeyer, Neeraj Pradhan, Theofanis Karaletsos, Rohit Singh, Paul A. Szerlip, Paul Horsfall, and Noah D. Goodman. 2019. "Pyro: Deep Universal Probabilistic Programming." *J. Mach. Learn. Res.* 20: 28:1--6. <http://jmlr.org/papers/v20/18-403.html>.
:::

::: {#ref-weaklensing .csl-entry}
Blandford, R. D., A. B. Saust, T. G. Brainerd, and J. V. Villumsen. 1991. "[The distortion of distant galaxy images by large scale structure]{.nocase}." *AIP Conference Proceedings* 222 (1): 455--58. <https://doi.org/10.1063/1.40414>.
:::

::: {#ref-lognormal .csl-entry}
Boruah, Supranta Sarma, Eduardo Rozo, and Pier Fiedorowicz. 2022. "Map-Based Cosmology Inference with Lognormal Cosmic Shear Maps." <https://arxiv.org/abs/2204.13216>.
:::

::: {#ref-gp:acceleration2 .csl-entry}
Boruah, Supranta S, Tim Eifler, Vivian Miranda, and P M Sai Krishanth. 2022. "[Accelerating cosmological inference with Gaussian processes and neural networks -- an application to LSST Y1 weak lensing and galaxy clustering]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 518 (4): 4818--31. <https://doi.org/10.1093/mnras/stac3417>.
:::

::: {#ref-jax .csl-entry}
Bradbury, James, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula, et al. 2018. "JAX: Composable Transformations of Python+NumPy Programs." <http://github.com/google/jax>.
:::

::: {#ref-cellestim2 .csl-entry}
Brown, M. L., P. G. Castro, and A. N. Taylor. 2005. "[Cosmic microwave background temperature and polarization pseudo-$C_\ell$ estimators and covariances]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 360 (4): 1262--80. <https://doi.org/10.1111/j.1365-2966.2005.09111.x>.
:::

::: {#ref-jaxcosmo .csl-entry}
Campagne, Jean-Eric, François Lanusse, Joe Zuntz, Alexandre Boucaud, Santiago Casas, Minas Karamanis, David Kirkby, Denise Lanzieri, Austin Peel, and Yin Li. 2023. "JAX-COSMO: An End-to-End Differentiable and GPU Accelerated Cosmology Library." *The Open Journal of Astrophysics* 6 (April). <https://doi.org/10.21105/astro.2302.05163>.
:::

::: {#ref-cellestim .csl-entry}
Chon, Gayoung, Anthony Challinor, Simon Prunet, Eric Hivon, and István Szapudi. 2004. "[Fast estimation of polarization power spectra using correlation functions]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 350 (3): 914--26. <https://doi.org/10.1111/j.1365-2966.2004.07737.x>.
:::

::: {#ref-noise .csl-entry}
Croft, Rupert A. C., Peter E. Freeman, Thomas S. Schuster, and Chad M. Schafer. 2017. "[Prediction of galaxy ellipticities and reduction of shape noise in cosmic shear measurements]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 469 (4): 4422--27. <https://doi.org/10.1093/mnras/stx1206>.
:::

::: {#ref-dodelson .csl-entry}
Dodelson, Scott, and Fabian Schmidt. 2021. "13 - Probes of Structure: Lensing." In *Modern Cosmology (Second Edition)*, edited by Scott Dodelson and Fabian Schmidt, Second Edition, 373--99. Academic Press. https://doi.org/<https://doi.org/10.1016/B978-0-12-815948-4.00019-X>.
:::

::: {#ref-tinygp .csl-entry}
Foreman-Mackey, Daniel, Weixiang Yu, Sachin Yadav, McCoy Reynolds Becker, Neven Caplar, Daniela Huppenkothen, Thomas Killestein, René Tronsgaard, Theo Rashid, and Steve Schmerler. 2024. "[dfm/tinygp: The tiniest of Gaussian Process libraries]{.nocase}." Zenodo. <https://doi.org/10.5281/zenodo.10463641>.
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

::: {#ref-pixel .csl-entry}
Grewal, Nisha, Joe Zuntz, and Tilman Tröster. 2024. "Comparing Mass Mapping Reconstruction Methods with Minkowski Functionals." <https://arxiv.org/abs/2402.13912>.
:::

::: {#ref-cosmology:hsc .csl-entry}
Hikage, Chiaki, Masamune Oguri, Takashi Hamana, Surhud More, Rachel Mandelbaum, Masahiro Takada, Fabian Köhlinger, et al. 2019. "[Cosmology from cosmic shear power spectra with Subaru Hyper Suprime-Cam first-year data]{.nocase}." *Publications of the Astronomical Society of Japan* 71 (2): 43. <https://doi.org/10.1093/pasj/psz010>.
:::

::: {#ref-lognormal3 .csl-entry}
Hilbert, S., Hartlap, J., and Schneider, P. 2011. "Cosmic Shear Covariance: The Log-Normal Approximation." *A&A* 536: A85. <https://doi.org/10.1051/0004-6361/201117294>.
:::

::: {#ref-cosmology:kids1000_bins .csl-entry}
Hildebrandt, H., van den Busch, J. L., Wright, A. H., Blake, C., Joachimi, B., Kuijken, K., Tröster, T., et al. 2021. "KiDS-1000 Catalogue: Redshift Distributions and Their Calibration." *A&A* 647: A124. <https://doi.org/10.1051/0004-6361/202039018>.
:::

::: {#ref-gp:expansion3 .csl-entry}
Holsclaw, Tracy, Ujjaini Alam, Bruno Sansó, Herbert Lee, Katrin Heitmann, Salman Habib, and David Higdon. 2010. "Nonparametric Reconstruction of the Dark Energy Equation of State." *Phys. Rev. D* 82 (November): 103502. <https://doi.org/10.1103/PhysRevD.82.103502>.
:::

::: {#ref-gp:acceleration3 .csl-entry}
Karchev, Konstantin, Adam Coogan, and Christoph Weniger. 2022. "[Strong-lensing source reconstruction with variationally optimized Gaussian processes]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 512 (1): 661--85. <https://doi.org/10.1093/mnras/stac311>.
:::

::: {#ref-cosmology:lensing .csl-entry}
Kilbinger, Martin. 2015. "Cosmology with Cosmic Shear Observations: A Review." *Reports on Progress in Physics* 78 (8): 086901. <https://doi.org/10.1088/0034-4885/78/8/086901>.
:::

::: {#ref-smail2 .csl-entry}
Kirk, Donnacha, Anais Rassat, Ole Host, and Sarah Bridle. 2012. "[The cosmological impact of intrinsic alignment model choice for cosmic shear]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 424 (3): 1647--57. <https://doi.org/10.1111/j.1365-2966.2012.21099.x>.
:::

::: {#ref-cosmology:kids450 .csl-entry}
Köhlinger, F., M. Viola, B. Joachimi, H. Hoekstra, E. van Uitert, H. Hildebrandt, A. Choi, et al. 2017. "[KiDS-450: the tomographic weak lensing power spectrum and constraints on cosmological parameters]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 471 (4): 4412--35. <https://doi.org/10.1093/mnras/stx1820>.
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

::: {#ref-gp:acceleration .csl-entry}
Mootoovaloo, Arrykrishna, Alan F Heavens, Andrew H Jaffe, and Florent Leclercq. 2020. "[Parameter inference for weak lensing using Gaussian Processes and MOPED]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 497 (2): 2213--26. <https://doi.org/10.1093/mnras/staa2102>.
:::

::: {#ref-flatsky .csl-entry}
Nicola, Andrina, Carlos García-García, David Alonso, Jo Dunkley, Pedro G. Ferreira, Anže Slosar, and David N. Spergel. 2021. "Cosmic Shear Power Spectra in Practice." *Journal of Cosmology and Astroparticle Physics* 2021 (03): 067. <https://doi.org/10.1088/1475-7516/2021/03/067>.
:::

::: {#ref-numpyro .csl-entry}
Phan, Du, Neeraj Pradhan, and Martin Jankowiak. 2019. "[Composable Effects for Flexible and Accelerated Probabilistic Programming in NumPyro]{.nocase}." *arXiv e-Prints*, October, arXiv:1912.11554. <https://doi.org/10.48550/arXiv.1912.11554>.
:::

::: {#ref-fwdmodel2 .csl-entry}
Porqueres, Natalia, Alan Heavens, Daniel Mortlock, and Guilhem Lavaux. 2021. "[Bayesian forward modelling of cosmic shear data]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 502 (2): 3035--44. <https://doi.org/10.1093/mnras/stab204>.
:::

::: {#ref-rasmussen .csl-entry}
Rasmussen, Carl Edward, and Christopher K. I. Williams. 2005. *[Gaussian Processes for Machine Learning]{.nocase}*. The MIT Press. <https://doi.org/10.7551/mitpress/3206.001.0001>.
:::

::: {#ref-flatsky6 .csl-entry}
Schneider, P., van Waerbeke, L., Kilbinger, M., and Mellier, Y. 2002. "Analysis of Two-Point Statistics of Cosmic Shear - i. Estimators and Covariances." *A&A* 396 (1): 1--19. <https://doi.org/10.1051/0004-6361:20021341>.
:::

::: {#ref-gp:expansion2 .csl-entry}
Seikel, Marina, Chris Clarkson, and Mathew Smith. 2012. "Reconstruction of Dark Energy and Expansion Dynamics Using Gaussian Processes." *Journal of Cosmology and Astroparticle Physics* 2012 (06): 036. <https://doi.org/10.1088/1475-7516/2012/06/036>.
:::

::: {#ref-gp:expansion .csl-entry}
Shafieloo, Arman, Alex G. Kim, and Eric V. Linder. 2012. "Gaussian Process Cosmography." *Phys. Rev. D* 85 (June): 123530. <https://doi.org/10.1103/PhysRevD.85.123530>.
:::

::: {#ref-fftlog .csl-entry}
Simonović, Marko, Tobias Baldauf, Matias Zaldarriaga, John Joseph Carrasco, and Juna A. Kollmeier. 2018. "Cosmological Perturbation Theory Using the FFTLog: Formalism and Connection to QFT Loop Integrals." *Journal of Cosmology and Astroparticle Physics* 2018 (04): 030. <https://doi.org/10.1088/1475-7516/2018/04/030>.
:::

::: {#ref-smail .csl-entry}
Smail, Ian, David W. Hogg, Lin Yan, and Judith G. Cohen. 1995. "Deep Optical Galaxy Counts with the Keck Telescope\*." *The Astrophysical Journal* 449 (2): L105. <https://doi.org/10.1086/309647>.
:::

::: {#ref-fwdmodel .csl-entry}
Zhou, Alan Junzhe, Xiangchong Li, Scott Dodelson, and Rachel Mandelbaum. 2023. "Accurate Field-Level Weak Lensing Inference for Precision Cosmology." <https://arxiv.org/abs/2312.08934>.
:::
:::::::::::::::::::::::::::::::::::::::::::
