<div class="titlingpage">

<div class="adjustwidth*">

-

</div>

</div>

# Introduction

Matter bends light. The theory of general relativity predicts that the
presence of matter or energy changes the geometry of space and time,
which in turn can cause what would otherwise be the straight path of a
beam of light to curve. Take a distant source of light. If we assume the
universe not to be empty, then between us and said source there exists a
non trivial matter disposition. As light travels through everything that
is in between us and the source, it gets blocked, bent and distorted. We
call this phenomenon weak lensing. In practice what we measure is the
shape of distant galaxies. These images do not show a distinct lensing
feature individually, as such tiny changes can only be seen with a large
number of sources. For example, we observe that galaxies have a tendency
of aligning along a preferred axis, causing a statistical discrepancy in
an otherwise seemingly isotropic universe. For further details on
lensing, please refer to (Kilbinger 2015) (Bartelmann and Maturi 2017);
for weak lensing (Blandford et al. 1991). The image of a distant galaxy
can change shape or size. Changes in shape are fully characterised by
the shear distortion $`\Vec{\gamma}`$ vector field, where the change in
size is given by its magnitude, the convergence field $`\kappa`$. We lay
out a theoretical framework for weak lensing in *Sec.*
<a href="#sec:weak lensing" data-reference-type="ref"
data-reference="sec:weak lensing">2.1</a> as well as details on the
cosmology used in this thesis in *Sec.*
<a href="#subsec:cosmology" data-reference-type="ref"
data-reference="subsec:cosmology">3.1.1</a>.

A lot of work goes into translating a measurement of distant galaxies to
its mathematically friendly counterpart $`\Vec{\gamma}`$. This is one of
the reasons why we will not be dealing with it in this thesis, as it is
outside of our scope. Instead we will be simulating our own convergence
fields. We use a *Gaussian random field (GRF)* algorithm for the
creation of Gaussianly distributed data. As well as lognormal
transformations to create fields with a distribution that resembles more
closely that in our universe. These transformations are listed in *Sec.*
<a href="#sec:field generation" data-reference-type="ref"
data-reference="sec:field generation">2.2</a>; we then use them to
simulate our data as explained in *Sec.*
<a href="#sec:data simulation" data-reference-type="ref"
data-reference="sec:data simulation">3.1</a>. We also verify that the
generated fields recover the fiducial power spectrum in *Sec.*
<a href="#sec:gaussian and lognormal fields" data-reference-type="ref"
data-reference="sec:gaussian and lognormal fields">4.1.1</a>.

<div class="wrapfigure">

r0.45

</div>

A *Gaussian process (GP)* usually assumes little prior knowledge about
the data it is applied to. Current research in the field of cosmology
views GPs as a machine learning tool to be trained. It is used to
accelerate and optimise models (Mootoovaloo et al. 2020) (Supranta S.
Boruah et al. 2022) (Karchev, Coogan, and Weniger 2022), as well as for
its interpolation qualities applied to the reconstruction of functions
determining the evolution of the universe (Shafieloo, Kim, and Linder
2012) (Seikel, Clarkson, and Smith 2012) (Holsclaw et al. 2010). Our
work, however, is based on a different approach. We apply our prior
knowledge about 2-point statistics in cosmology to create a fully
informed GP. Restricting ourselves to 2D flat-sky weak lensing
convergence fields, as shown in *Fig.*
<a href="#tik:GP pipeline" data-reference-type="ref"
data-reference="tik:GP pipeline">[tik:GP pipeline]</a>, we can:

- compute the angular power spectrum $`C(\Theta)`$ from a set of
  cosmological parameters $`\Theta`$,

- transform it in the convergence angular autocorrelation function
  $`w(\Theta)`$,

- create a zero mean GP with kernel given by said correlation function,

- evaluate the likelihood $`\mathcal{L}`$ of $`\Theta`$ given a set of
  data points $`y`$.

With a Bayesian approach we make use of this pipeline to infer the
values of the cosmological parameters. Running a *Markov chain Monte
Carlo (MCMC)* we can sample the posterior distribution of the
cosmological parameters, in particular we will get contours for
$`\Omega_m`$, $`\sigma_8`$ and $`S_8`$. Other than that, GPs have
several other interesting properties at the field level. They are not
only able to generate fields that recover the fiducial 2-point
statistics, but are also able to reconstruct masked fields, a task that
usually brings many challenges to $`C_\ell`$ estimation (Chon et al.
2004) (Brown, Castro, and Taylor 2005). In the field of weak lensing in
particular, foreground objects like bright stars or galaxies can
contaminate measurements, leading to the need of masking such a region,
essentially removing the signal.

Here we list the advantages of our method:

- minimal information loss, as it is a map based method we use all
  available data points,

- it can be used as a likelihood for cosmological parameters inference,

- easily deals with masked fields, providing estimates with an
  associated uncertainty for the masked points.

Whilst some of the disadvantages:

- the conditioning process depends on the inverse of a correlation
  matrix, with a computational effort that grows as
  $`\sim \mathcal{O}(n^3)`$ for $`n\propto`$ data points, indicating
  possible scaling issues;

- due to the intrinsic Gaussianity of GPs, the distribution of the
  samples will be Gaussian, making it hard to apply them to other
  fields, say for example lognormal fields.

GPs in this thesis are presented in a general introduction in *Sec.*
<a href="#sec:gaussian process" data-reference-type="ref"
data-reference="sec:gaussian process">2.3</a>, followed by a detailed
account of the computational methods used to recover a working kernel
for GPs in *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">3.2</a>. In our results we
show their ability to create maps that follow the desired statistic
*Sec.* <a href="#sec:gaussian process priors" data-reference-type="ref"
data-reference="sec:gaussian process priors">4.1.2</a> and reconstruct
data *Sec.* <a href="#sec:gaussian process map reconstruction"
data-reference-type="ref"
data-reference="sec:gaussian process map reconstruction">4.2</a>. We
also present our attempt at cosmological parameters inference with GPs
in *Sec.* <a href="#sec:inference of cosmological parameters"
data-reference-type="ref"
data-reference="sec:inference of cosmological parameters">4.3</a>.

It is important to note that throughout the thesis we follow the
extremely useful guidelines set by the `Miko` pipeline (Zhou et al.
2023) on how to deal with discrete maps in weak lensing.

# Theoretical Framework

## Weak lensing

### Convergence field

Let’s introduce what can only be defined as the protagonist cosmological
field of this thesis: the convergence field (Dodelson and Schmidt 2021)
(Blandford et al. 1991) (Kilbinger 2015) (Bartelmann and Maturi 2017).
As explained in the introduction weak lensing happens due to the
presence of matter between us and a distant source. In mathematical
terms we write this as an integral over the line of sight of the matter
overdensity field, weighted accordingly.
``` math
\kappa(\theta) = \int_0^{\chi*}d\chi W(\chi)\delta_m(\chi \theta, \chi),
```
``` math
W(\chi)=\tfrac{3}{2}H_0^2\Omega_m(1+z(\chi))\chi \int_\chi^{\chi*}d\chi' n(z(\chi'))\left(1-\frac{\chi}{\chi'}\right).
    \label{eq:lensing weight}
```
With $`W(\chi)`$ being a measure of the lensing weights; $`W(\chi)`$
incorporates all of the relevant cosmological parameters, as well as
knowledge of the redshift distribution of the source galaxies $`n(z)`$.

### 2-point statistics

2-point statistics such as correlation functions and power spectra are
arguably the most powerful tool of analysis in cosmology. They work as a
way to summarise raw data into something simpler, while still retaining
most of the relevant information; for examples, allowing us to extract
constraints on cosmological parameters.

#### Full sky

Let us start by introducing the statistics of a 3D spherically symmetric
field, also known as a full sky field. The 2-point autocorrelation
function is defined as the expectation value $`\mathbb{E}`$ of the
product of a random field with its complex conjugate
``` math
w(\bm{x}, \bm{y}) \equiv \mathbb{E}[\phi(\bm{x})\phi^*(\bm{y})].
```
Where $`\phi(\bm{x})`$ is the 2D projection of a spherically symmetric
3D field. We can now perform a decomposition in spherical harmonics
$`Y_{\ell m}`$. Such a decomposition gives rise to the correlation
function associated to the harmonic coefficients $`\phi_{\ell m}`$, the
2D power spectrum $`C_\ell`$,
``` math
\begin{gathered}
    \phi(\bm{x}) = \sum_{\ell m}\phi_{\ell m} Y_{\ell m}(\hat{\bm{x}}),\\
    C_\ell \equiv \delta_{\ell m}\delta_{\ell'm'}\mathbb{E}[ \phi_{\ell m}\phi^*_{\ell'm'}].
\end{gathered}
```
In this setup correlation function and power spectrum are therefore
related by,
``` math
\begin{aligned}
    & \mathbb{E}[\phi(\bm{x})\phi^*(\bm{y})] \\
    =& \sum_{\ell m}\sum_{\ell'm'}Y_{\ell m}(\hat{\bm{x}})Y^*_{\ell'm'}(\hat{\bm{y}}) \mathbb{E}[ \phi_{\ell m}\phi^*_{\ell'm'} ]\\
    =& \sum_{\ell m}Y_{\ell m}(\hat{\bm{x}})Y^*_{\ell m}(\hat{\bm{y}}) C_\ell\\
    =& \sum_{\ell}\frac{2\ell+1}{4\pi}C_\ell P_\ell(\hat{\bm{x}}\cdot\hat{\bm{y}}),
\end{aligned}
```
where we have used the identity relating Legendre polynomials to
spherical harmonics
$`P_\ell(\hat{\bm{x}}\cdot\hat{\bm{y}}) = \frac{4\pi}{2\ell+1} \sum_m Y_{\ell m}(\hat{\bm{x}})Y^*_{\ell m}(\hat{\bm{y}})`$.
Cleaning up the equations we are just left with the well known full sky
equation
``` math
w(\theta) = \sum_{\ell}\frac{2\ell+1}{4\pi}C_\ell P_\ell (\cos(\theta)),
    \label{eq:fullsky}
```
which relates the angular correlation function to the angular power
spectrum.

#### Flat-sky

Most analysis of weak lensing data actually use the flat-sky
approximation (Nicola et al. 2021) (Gao, Raccanelli, and Vlah 2023)
(Matthewson and Durrer 2021) (Gao, Vlah, and Challinor 2023)
(García-García, Alonso, and Bellini 2019) (Schneider, P. et al. 2002),
our work will not be an exception. Such an approximation essentially
changes our setup to a flat-sky 2D field, instead of the 2D projection
of a 3D one, allowing for simpler analytical expressions. In this setup,
harmonic decomposition will not work, we will have to Fourier transform
our space instead. To do so, we can assume the existence of a function
$`C(l)`$ which is the continuous extension of $`C_\ell`$. Then we say
that $`C(l)`$ is the result of a 2D inverse Fourier transformation
$`\mathcal{F}`$,
``` math
\{\mathcal{F}^{-1}C\}(\theta)=\int\frac{d^2l}{4\pi^2}e^{i\bm{l}\cdot\bm{\theta}}C(l).
    \label{eq:flatsky fft}
```
To prove that $`\{\mathcal{F}^{-1}C\}(\theta)`$ is none other than the
angular correlation function, we make use of the radial symmetry of the
cosmological field. Which simplifies the equation into a 1D integral.
Consider the polar coordinate substitution from $`(l_x,l_y)`$ to
$`(l,\phi)`$, the integral becomes
``` math
\int \frac{dl}{2\pi} l C(l) \int\frac{d\phi}{2\pi}e^{il\theta \cos{\phi}}.
```
Lastly, we make use of the identity
$`\int d\phi e^{il\theta \cos{\phi}} = 2\pi J_0(l\theta)`$, where
$`J_0`$ is the zeroth order Bessel function. Which leaves us with
``` math
\{\mathcal{F}^{-1}C\}(\theta) = \int \frac{dl}{2\pi} l C(l) J_0(l\theta).
    \label{eq:flatsky hankel}
```
In this form it is clear that *Eq.*
<a href="#eq:fullsky" data-reference-type="eqref"
data-reference="eq:fullsky">[eq:fullsky]</a> and *Eq.*
<a href="#eq:flatsky hankel" data-reference-type="eqref"
data-reference="eq:flatsky hankel">[eq:flatsky hankel]</a> are
asymptotically equivalent, since it is known that
$`J_0(\ell\theta) \xrightarrow{\quad} P_\ell (\cos(\theta))`$ as
$`\ell \rightarrow \infty`$. This concludes our heuristic proof that the
angular correlation function is recovered from an inverse Fourier
transformation of the angular power spectrum
$`w(\theta) \sim \{\mathcal{F}^{-1}C\}(\theta)`$ in the flat-sky
approximation. Physically speaking this approximation makes sense when
we consider a patch of sky of size L. The wavenumber of the flat-sky
angular power spectrum is related to its dimensionless counterpart p by
``` math
l = \frac{2\pi}{L}p,
    \label{eq:ell px}
```
in other words, it is inversely proportional to the size of the map.
Just as we would expect the geometry of a sphere to become flat when
zooming in, the flat-sky approximation holds as $`L \rightarrow 0`$.

#### Limber approximation

The way we computationally obtain $`\kappa`$’s 2-point statistics is
with the Limber approximation. We use the code `jaxcosmo` (Campagne et
al. 2023) to compute the 2D power spectrum $`C(l)`$ from the 3D matter
power spectrum $`P_\delta(k)`$ with the efficient Limber approximation,
``` math
C(l)=C_{\kappa\kappa}(l)=\int_0^{\chi*}\frac{d\chi}{\chi} W(\chi)W(\chi)P_\delta(k=\frac{l}{\chi},\chi).
    \label{eq:limber}
```
The assumptions of the Limber approximation are:

- flat-sky, as described previously and

- the matter power spectrum depends only on modes on the field
  $`\bm{k}_\perp`$, essentially setting the modes parallel to the line
  of sight to zero, $`k_\parallel=0`$.

Such assumptions allow to simplify the relation between $`C(l)`$ and
$`P_\delta(k)`$ to a one line integral, *Eq.*
<a href="#eq:limber" data-reference-type="eqref"
data-reference="eq:limber">[eq:limber]</a>. It is noteworthy to mention
that the Limber approximation introduces significant errors only for
modes $`l<10`$, as explained in detail in (Gao, Vlah, and Challinor
2023). As far as this work is concerned, we only deal with patches of
size $`10^{\circ}`$, which means we have $`l>36`$ according to *Eq.*
<a href="#eq:ell px" data-reference-type="eqref"
data-reference="eq:ell px">[eq:ell px]</a>, well within the range for a
good approximation.

## Field generation

### Gaussian random field

In order to simulate cosmological fields with a specific power spectrum,
we make use of Gaussian random fields. They are fast to generate and
only need information about the 2-point power spectrum of the field. The
algorithm we use for the generation of GRFs is common to most packages
and is explained in detail in (Bertschinger 2001) (Lang and Potthoff
2011). In 1D, assume a pair of functions functions $`\xi`$ and $`P`$,
related by a Fourier transformation
``` math
\xi(x,y)=\int \frac{dk}{2\pi} e^{i k(x-y)} P(k).
```
Let $`W(x)`$ be a Gaussian white noise field and let $`\mathcal{F}`$
denote a Fourier transformation, we then define
``` math
\phi(x) \equiv (\mathcal{F}^{-1} P^{1/2}\mathcal{F}W)(x)
    \label{eq:grf 1D}
```
to be a Gaussian random field. Such a procedure ensures that the
covariance $`\mathbb{E}\left[\phi(x)\phi(y)\right]`$ of the GRF recovers
the correlation function $`\xi(x,y)`$,
``` math
\begin{aligned}
 &\mathbb{E}\left[\phi(x)\phi(y)\right] \\
=&\iiiint dx' dy' \frac{dk}{2\pi} \frac{dl}{2\pi}  \, e^{i(kx + ly)} P(k)^{1/2} P(l)^{1/2} e^{-i(kx' + ly')} \mathbb{E}[W(x')W(y')] \\
=& \iint \frac{dk}{2\pi} \frac{dl}{2\pi} \, e^{i(kx + ly)} P(k)^{1/2} P(l)^{1/2} \int dx' \, e^{-i(k+l)x'}   \\
=& \int \frac{dk}{2\pi} \, e^{i k(x-y)} P(k)  \\
=& \, \xi(x, y).
\end{aligned}
```
Where we have used $`\mathbb{E}[W(x')W(y')] = \delta(x'-y')`$, as white
noise is defined by a constant power spectrum.

#### Rayleigh distribution

Since we are dealing with 2D maps, our algorithm will have to be
implemented in two dimensions. To do so, we decide to implement the
algorithm in *Eq.* <a href="#eq:grf 1D" data-reference-type="eqref"
data-reference="eq:grf 1D">[eq:grf 1D]</a> with the use of the Rayleigh
distribution $`\mathcal{R}(\sigma)`$. Given two independent Gaussian
random variables $`X`$ and $`Y`$, the random variable $`R`$ given by
``` math
R=\sqrt{X^2+Y^2},
```
is said to be Rayleigh distributed. If we then multiply $`R`$ by the
complex exponential $`e^{i\theta}`$ of a uniformly distributed random
variable $`\theta \sim \mathcal{U}(0,2\pi)`$, we obtain a map of
Gaussianly distributed complex numbers, which will substitute the
$`\mathcal{F}W`$ term in *Eq.*
<a href="#eq:grf 1D" data-reference-type="eqref"
data-reference="eq:grf 1D">[eq:grf 1D]</a>. We showcase this equivalency
in *Fig.* <a href="#fig:rayleigh" data-reference-type="ref"
data-reference="fig:rayleigh">2.1</a> for distributions of $`\mu=0`$ and
$`\sigma=1`$. The sequence of transformations in 2D therefore becomes,
``` math
\phi(x) \equiv (\mathcal{F}^{-1} P^{1/2} R e^{i\theta})(x).
    \label{eq:grf 2D}
```

<figure id="fig:rayleigh">
<embed src="images/7_rayleigh.pdf" />
<figcaption><span id="fig:rayleigh" data-label="fig:rayleigh"></span>
Sampling a 2D Gaussian against a Rayleigh distributed amplitude with
uniform complex phase. In purple is the complex number <span
class="math inline">\(X+iY\)</span> with <span class="math inline">\(X,Y
\sim \mathcal{N}(0,1)\)</span>, in cyan is <span
class="math inline">\(Re^{i\theta}\)</span> with <span
class="math inline">\(R\sim\mathcal{R}(1)\)</span> and <span
class="math inline">\(\theta \sim
\mathcal{U}(0,2\pi)\)</span>.</figcaption>
</figure>

### Lognormal field

The universe today is not Gaussian. GRFs are able to capture the 2-point
statistics of cosmological fields, but they cannot capture their skewed
distribution. A possible way to get closer to the true distribution of
the convergence field is with a lognormal transformation (Supranta Sarma
Boruah, Rozo, and Fiedorowicz 2022) (Leclercq and Heavens 2021)
(Hilbert, S., Hartlap, J., and Schneider, P. 2011) (Zhou et al. 2023).
In this work we will denote lognormal transformations as $`\mathcal{L}`$
and adopt the following convention for both the field and the
correlation function,
``` math
\begin{gathered}
    \label{eq:L_w}
    \mathcal{L}_w^{-1}(w^{L}, a) \equiv \log \left(\frac{w^{L}}{a^2}+1\right) = w^G,\\
    \label{eq:L_k}
    \mathcal{L}_\kappa(\kappa^G, a) \equiv a\left(\exp(\kappa^G-\tfrac{1}{2}\text{Var}(\kappa^G)) -1\right) = \kappa^{L}.
\end{gathered}
```
Where the superscripts L and G respectively stand for lognormal and
Gaussian, Var($`\cdot`$) stands for the variance of the field and $`a`$
is the so-called shift parameter, which is an indicator of the
non-Gaussianity of the resulting field.

## Gaussian process

One way to think of Gaussian processes is as an extension of random
vectors to infinite dimensions. Following this train of thought, let’s
begin with the concept of a random variable following a normal
distribution. We say,
``` math
X \sim \mathcal{N}\left(\mu, \sigma^2\right),
```
to mean that $`X`$ is a sample of a Gaussian of mean $`\mu`$ and
variance $`\sigma^2`$. If we were to get enough samples $`X`$, we would
eventually recover its distribution. The generalisation of this concept
to n-dimensions is a collection of random variables, described by a
so-called multivariate normal distribution,
``` math
\bm{X} \sim \mathcal{N}\left(\bm{\mu}, \bm{K}\right).
```
Where $`\bm{X}=(X_0,X_1,...)`$ is a vector of random variables,
$`\bm{\mu}`$ is the mean vector and $`\bm{K}`$ the covariance matrix.
For a zero mean field, the covariance matrix is formed by the variance
of each of the random variables on its diagonal, while the cross
correlation terms populate the rest of the matrix.

### Definition

Adopting the philosophy of Rasmussen (Rasmussen and Williams 2005),
functions can be thought of as very long vectors of the form
$`\left(f(x_1), f(x_2), ...\right)`$. Such a view allows us to extend
the definition of multivariate Gaussians, to functions. Defining
$`\mathcal{GP}`$ a Gaussian process, a sample function $`f`$ will be
given by:
``` math
f(\bm{x}) \sim \mathcal{GP}\left(m(\bm{x}), k(\bm{x}, \bm{x'})\right)
```
with $`m(\bm{x})`$ and $`k(\bm{x}, \bm{x'})`$ defined as,
``` math
\begin{gathered}
    m(\bm{x})=\mathbb{E}[f(\bm{x})],\\
    k(\bm{x}, \bm{x'})=\mathbb{E}[(f(\bm{x})-m(\bm{x}))(f(\bm{x}')-m(\bm{x}'))],
\end{gathered}
```
Mathematically a GP is defined for a continuous function.
Computationally this is not possible and we must treat space as a
discrete grid.

### Prior and posterior samples

Given some $`m(\cdot)`$ and $`k(\cdot,\cdot)`$ which define a GP, a
random sample from said GP would be a function $`\bm{f}_*`$ defined on a
domain $`D_*`$, which is our grid.
``` math
\bm{f}_* \sim \mathcal{N}(\bm{m}, \bm{K}_{**}).
    \label{eq:gp prior}
```
Here we adopt the convention $`\bm{K} = k(D_*,D_*)`$. When drawing a
sample function from *Eq.*
<a href="#eq:gp prior" data-reference-type="eqref"
data-reference="eq:gp prior">[eq:gp prior]</a>, computationally the
operation is equivalent to drawing a vector from a multivariate
Gaussian. What we obtain is a so-called prior, or priors, see *Fig.*
<a href="#fig:priors" data-reference-type="ref"
data-reference="fig:priors">2.2</a>.

<figure id="fig:priors">
<embed src="images/1_priors.pdf" />
<figcaption>Prior samples of a GP with mean <span
class="math inline">\(m(\bm{x})=0\)</span> and squared exponential
kernel <span
class="math inline">\(k(\bm{x},\bm{x&#39;})=e^{-(\bm{x}-\bm{x&#39;})^2}\)</span>.</figcaption>
</figure>

Let’s now see how we can introduce knowledge of data points in this
system. We divide the grid in training points $`D`$ and test points
$`D_*`$. To each training point is associated a known value $`\bm{y}`$
and variance $`\sigma_n^2`$, whereas the values of the function at the
test points $`\bm{f}_*`$ are unknown. We can summarise this as,
``` math
\begin{bmatrix}
    \bm{y} \\
    \bm{f}_* \\
    \end{bmatrix}
    \sim \mathcal{N}\left(\bm{m}, \begin{bmatrix}
    \bm{K} + \sigma_n^2 I & \bm{K}_* \\
    \bm{K}^T_* & \bm{K}_{**} \\
    \end{bmatrix}\right)
```
where we have once again adopted the notation $`\bm{K}=k(D,D)`$,
$`\bm{K_{*}}=k(D,D*)`$, $`\bm{K_{**}}=k(D_*,D_*)`$. At this point, one
way to find samples that follow the data would be to blindly draw priors
until we get something that goes through all data points. This would be
inefficient and computationally wasteful. Instead, we make a better
guess for the test function values. This operation is called
conditioning, because we condition the joint Gaussians on the training
points, this gives
``` math
\bm{f}_* \mid D_*, D, \bm{y} \sim \mathcal{N}\left( \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{y} , \bm{K}_{**} - \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{K}_* \right).
\label{eq:conditioning}
```
Conditioning can therefore give rise to what is called a posterior
sample, *Fig.* <a href="#fig:posteriors" data-reference-type="ref"
data-reference="fig:posteriors">2.3</a>. The result is still a
multivariate Gaussian, but the mean and variance given by *Eq.*
<a href="#eq:conditioning" data-reference-type="eqref"
data-reference="eq:conditioning">[eq:conditioning]</a> generate samples
that are a better guess of the behaviour of the function outside of the
training points.

<figure id="fig:posteriors">
<embed src="images/1_posteriors.pdf" />
<figcaption><span id="fig:posteriors"
data-label="fig:posteriors"></span> Summary plot of a GP conditioned to
some data. The cyan line is the mean of the GP and the filled region
corresponds to <span class="math inline">\(1\sigma\)</span>. The purple
lines are posterior samples, which are distributed Gaussianly around the
mean. The data points are clearly marked in black, they are also the
points where all samples converge to.</figcaption>
</figure>

# Methods

## Data simulation

### Cosmology

<div class="wraptable">

r2.8cm

|              | Fiducial |
|:-------------|:---------|
| $`\Omega_m`$ | 0.3      |
| $`\Omega_b`$ | 0.05     |
| $`\Omega_k`$ | 0        |
| $`h`$        | 0.7      |
| $`n_s`$      | 0.97     |
| $`\sigma_8`$ | 0.8      |
| $`w_0`$      | -1       |
| $`w_a`$      | 0        |

</div>

This work follows in the general footsteps of data analysis of weak
lensing surveys like *HSC* (Hikage et al. 2019) and *KiDS* (Köhlinger et
al. 2017)(Asgari, Marika et al. 2021), as we aim to replicate their
methodologies. Throughout the work, we assume a fiducial cosmology of
fixed parameter values as shown in *Tab.*
<a href="#tab:fiducial_cosmology" data-reference-type="ref"
data-reference="tab:fiducial_cosmology">[tab:fiducial_cosmology]</a>. In
particular, all data maps will be generated from a power spectrum
following this cosmology. We will refer to this power spectrum as the
fiducial power spectrum $`C(l)`$. A leading modelling choice comes with
the redshift distribution $`n(z)`$. We model it as a Smail-type
distribution (Smail et al. 1995)(Kirk et al. 2012),
``` math
n(z)=z^\alpha \exp{\left[-\left(\frac{z}{z_0}\right)^\beta\right]}.
```
The choice of parameters has been made to emulate bin 5 of the
*KiDS1000* survey (Hildebrandt, H. et al. 2021), with parameters
$`\alpha=3.5`$, $`\beta=4.5`$, $`z_0=1`$.

<figure id="fig:smail">
<p><embed src="images/2_smail.pdf" /> <span id="fig:smail"
data-label="fig:smail"></span></p>
</figure>

### Map making pipeline

When dealing with maps of finite size $`(L, L)`$ and pixel resolution
$`(N,N)`$, Fourier space is going to have boundaries, just as real space
does. These limits are given by
``` math
\begin{gathered}
    l_{\text{min}} = \frac{2\pi}{L},\\
    l_{\text{max}} = \frac{2\pi}{L} N.
\end{gathered}
```
Therefore, a map of size $`(10^{\circ},10^{\circ})`$ and a grid
$`64\times64`$ will have limits
$`(l_{\text{min}}, l_{\text{max}}) = (36, 2304)\text{rad}^{-1}`$. Now
that we have the physical range for the power spectrum, we can generate
data.

<figure id="tik:cw">

<figcaption>Sequence of transformations used to generate Gaussian and
lognormal maps starting from the fiducial angular power spectrum. The
top branch shows how to generate a GRF which when transformed to a
lognormal field, follows the fiducial <span
class="math inline">\(C(l)\)</span>. The bottom branch is a standard GRF
realisation starting from the fiducial <span
class="math inline">\(C(l)\)</span>. <span
class="math inline">\(L\)</span> and <span
class="math inline">\(G\)</span> stand for lognormal and Gaussian
respectively. <span class="math inline">\(\mathcal{H}\)</span> is the
Hankel transformation, and tilde refers to intermediate
results.</figcaption>
</figure>

To generate a GRF, we employ the algorithm mentioned in *Eq.*
<a href="#eq:grf 2D" data-reference-type="eqref"
data-reference="eq:grf 2D">[eq:grf 2D]</a>. However, in making a
lognormal field, the matter is a bit more complicated. Any GRF on which
we apply the lognormal transformation $`\mathcal{L}_\kappa`$, from *Eq.*
<a href="#eq:L_k" data-reference-type="eqref"
data-reference="eq:L_k">[eq:L_k]</a>, becomes a lognormal field. The
reason we do not just lognormal transform any field is given by the fact
that they would not recover the fiducial power spectrum $`C(l)`$. Our
goal is therefore to find a transfer GRF $`\tilde{\kappa}^G`$ which,
when transformed lognormally, gives rise to a lognormal field
$`\kappa^L`$ that recovers $`C(l)`$. To do so, we follow the sequence of
transformations illustrated in the top branch of *Fig.*
<a href="#tik:cw" data-reference-type="ref"
data-reference="tik:cw">3.2</a>.

### Noise and mask

<figure id="fig:mask">
<embed src="images/5_random_and_blocks_mask.pdf" style="width:50.0%" />
<figcaption>Approximately <span class="math inline">\(10\%\)</span> mask
applied to the data. Size <span
class="math inline">\((10^{\circ},10^{\circ})\)</span> and grid <span
class="math inline">\(64\times64\)</span>.</figcaption>
</figure>

As all data is being simulated, we only take into account the so-called
shape noise, which is due to the intrinsic distribution of ellipticities
and angle formed with respect to us. GPs will treat each pixel of the
map as a random variable Gaussianly distributed with standard deviation
given by (Croft et al. 2017),
``` math
\sigma_\text{noise} = \frac{\sigma_e}{\sqrt{n_g A_{px}}}.
    \label{eq:noise}
```
We use values of $`\sigma_e=0.26`$,
$`n_g= 4, 10, 30, 100 \text{ galaxies}/\text{arcmin}^2`$, and a pixel
area given by the pixel resolution squared, $`A_{px}=(L/N)^2`$. For our
highest-resolution run, we have $`N=64`$ and use
$`n_g = 10 \text{ galaxies}/\text{arcmin}^2`$, which results in a noise
standard deviation of $`\sigma_\text{noise} \sim 0.0088`$. The mask
being used as seen in *Fig.*
<a href="#fig:mask" data-reference-type="ref"
data-reference="fig:mask">3.3</a>, covers approximately $`10\%`$ of the
patch (Grewal, Zuntz, and Tröster 2024). We keep the noise and mask
random seeds fixed throughout the work.

## Kernel

The kernel of a Gaussian process is given by a function of the form
$`k(x,y)`$. It takes in two points, $`x`$ and $`y`$, and returns the
value of their correlation. In our case, specifically, $`x`$ and $`y`$
will be two points in a grid of shape $`(N,N)`$, and the kernel function
will be the convergence angular autocorrelation function. As all code
used for this paper is written in `JAX` (Bradbury et al. 2018) we opt
for the use of the library `tinygp` (Foreman-Mackey et al. 2024) for all
Gaussian process computations. `tinygp` allows for the use of a custom
kernel with a custom `evaluate` method, which takes two points on the
grid and returns the correlation value. We follow with two `Python`
pseudocodes of our kernel implementations.

``` python
{kernel_Hankel} uses the helper function \code{Hankel} which returns a 1D callable correlation function \code{w}. Then finds the euclidean distance between $x$ and $y$ and evaluates the correlation function at that point. We will discuss how we perform the Hankel transformation in the following section.]
class kernel_Hankel:
    def __init__(self, cl, N, L):
        self.w   = Hankel(cl, N, L)
        self.r   = L / N
        
    def evaluate(self, x, y):
        theta    = self.r * sqrt(sum(x - y))
        return self.w(theta)
```

``` python
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

### Hankel transform

In order to build a Gaussian process kernel, we need to find the
correlation function that best describes the data. The way we do this is
by computing the angular power spectrum and transforming it in the
corresponding angular correlation function. Let’s explore the previously
discussed flat-sky relation between angular power spectrum and
correlation function given by *Eq.*
<a href="#eq:flatsky hankel" data-reference-type="eqref"
data-reference="eq:flatsky hankel">[eq:flatsky hankel]</a>. This
particular integral of a Bessel function is also known as a zeroth order
Hankel transformation,
``` math
w(\theta) = \int \frac{dl}{2\pi} l C(l) J_0(l\theta).
    \label{eq:C-w hankel}
```
We will explore two methods for computing this integral: the
*integration* method *Sec.*
<a href="#sec:integration method" data-reference-type="ref"
data-reference="sec:integration method">3.2.1.1</a> and the *FFTlog*
method *Sec.* <a href="#sec:FFTlog method" data-reference-type="ref"
data-reference="sec:FFTlog method">3.2.1.2</a>.

#### Integration

Integration is the most straight forward way to evaluate the integral,
but it requires to implement an algorithm for the approximation of the
Bessel function $`J_0`$. The advantages of this method:

- it is easy to integrate over the correct $`l`$-range, from
  $`l_{\text{min}}`$ and $`l_{\text{max}}`$, a freedom that we do not
  have with the FFTlog.

The disadvantages:

- integration is computationally slow, especially when dealing with
  highly oscillatory behaviour introduced by the Bessel function, which
  requires fine sampling.

#### FFTlog

The FFTlog method (Simonović et al. 2018) is a fast implementation of
the Hankel transformation. In fact it simplifies *Eq.*
<a href="#eq:C-w hankel" data-reference-type="eqref"
data-reference="eq:C-w hankel">[eq:C-w hankel]</a> by assuming a power
decomposition of $`C(l)`$. Such a decomposition is achievable by taking
the *fast Fourier transformation (FFT)* in $`\log k`$, hence the name
FFTlog. The power spectrum becomes,
``` math
C(l)=\sum_\alpha c_\alpha l^{\upsilon + i\eta_\alpha}.
```
Substituting in *Eq.*
<a href="#eq:C-w hankel" data-reference-type="eqref"
data-reference="eq:C-w hankel">[eq:C-w hankel]</a>,
``` math
w(\theta) = \sum_\alpha c_\alpha \int_0^\infty \frac{dl}{2\pi} l^{\upsilon + i\eta_\alpha+1} J_0(l\theta).
```
Take $`x=l\theta`$ and $`s_\alpha-1=\upsilon + i\eta_\alpha+1`$,
``` math
w(\theta) = \sum_\alpha c_\alpha \theta^{-s_\alpha} \int_0^\infty \frac{dx}{2\pi} x^{s_\alpha-1} J_0(x).
```
Lastly we recognise
$`\int_0^\infty dx x^{s-1}J_0(x) = \frac{2^{s-1}}{\pi}\sin(\pi s/2) [\Gamma(s/2)]^2`$,
a Mellin transform. Using this tabulated result we conclude that the
correlation is given by the sum,
``` math
w(\theta) = \frac{1}{2\pi^2}\sum_\alpha c_\alpha \theta^{-s_\alpha}2^{s_\alpha-1}\sin(\pi s_\alpha/2) [\Gamma(s_\alpha/2)]^2.
```
For the Mellin transform identity to hold analytically, the integral
bounds have to go from 0 to $`\infty`$. Although computationally we
don’t need to consider such a wide range, we still have to broaden the
integration limits to something larger than our $`l`$-range; so as to
avoid ringing effects. Experimentally we have found that extending the
$`l`$-range between $`l_{\text{min}}/4`$ and $`l_{\text{max}}`$, is
enough to compensate for such effects. The advantages of this method:

- the FFTlog method is ultimately much faster than the integration
  method.

The disadvantages:

- the widening of the $`l`$-range needed to avoid ringing effects
  inevitably adds power to the correlation function resulting in a
  higher variance and overall amplitude.

### Fourier transform

The second transformation that we can use to go from power spectrum to
correlation function, is the Fourier transformation discussed in *Eq.*
<a href="#eq:flatsky fft" data-reference-type="eqref"
data-reference="eq:flatsky fft">[eq:flatsky fft]</a>. It is a more
fundamental relation than the Hankel transformation as it does not
assume that $`l`$ is radially symmetric. In our case, low resolution,
coupled with a square map, means that the radial assumption might not
apply. Note that, the lowest resolution grid we use is $`32\times32`$,
with $`L/N \sim 19`$ arcmin; which is one order of magnitude worse than
today’s weak lensing data, around $`\sim 3`$ arcmin according to (Zhou
et al. 2023). In the following *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">3.2</a> we will find
experimentally that the Hankel methods described above do not work well
with our GP setup. For this reason, we explore this method of conversion
between angular power spectrum and correlation function,
``` math
w(\theta)=\int\frac{d^2l}{4\pi^2}e^{-i\bm{l}\cdot\bm{\theta}}C(l).
    \label{eq:C-w fft}
```
As computers can only deal with discrete functions, it is important to
note that we will be performing a *discrete Fourier transformation
(DFT)*. We will use the widely known FFT algorithm to compute DFTs. In
particular we use JAX’s implementation of the 2D FFT algorithm,
`jax.numpy.fft.ifft2`.

Let us find the relation between continuous Fourier transformation and
DFT. The definitions of continuous and discrete Fourier transformations
in 1D, are respectively:
``` math
\begin{aligned}
    \mathcal{F}^{-1}&=\int\frac{dk}{2\pi}e^{ikx}, \label{eq:F}\\
    \text{F}^{-1}&=\frac{1}{N}\sum_p e^{ik_px}. \label{eq:DFT}
\end{aligned}
```
First of all, a DFT is dimensionless. Secondly, it is discrete and
bounded. We can therefore rewrite *Eq.*
<a href="#eq:F" data-reference-type="eqref"
data-reference="eq:F">[eq:F]</a> using the substitution
$`k(p)=2\pi \frac{p}{L}`$ to discretise k-space,
``` math
\int\frac{dk}{2\pi}e^{ikx} = \int\frac{dp}{L} e^{ik(p)x} = \frac{1}{L}\sum_p e^{ik_px}.
```
Applying the definition of DFT as seen in *Eq.*
<a href="#eq:DFT" data-reference-type="eqref"
data-reference="eq:DFT">[eq:DFT]</a>, it follows that in 1D
``` math
\mathcal{F}^{-1}=\frac{N}{L}\text{F}^{-1}.
```
Which means that the correlation function is given by a *backwards*
normalised inverse DFT to be scaled by a factor $`(N/L)^d`$, where $`d`$
is the dimension of the considered space. In our case, $`d=2`$.

In order to perform a FFT in 2D, we will need a two dimensional
extension of the angular power spectrum. We make use of its radial
symmetry with respect to $`\bm{l}=(l_x,l_y)`$ and create a 2D grid of
shape $`(M,M)`$ as shown in *Fig.*
<a href="#tik:1D to 2D" data-reference-type="ref"
data-reference="tik:1D to 2D">3.4</a>.

<figure id="tik:1D to 2D">

<figcaption>1D to 2D extension of the power spectrum <span
class="math inline">\(C(l)\)</span></figcaption>
</figure>

Now that we have a 2D power spectrum we can take the inverse two
dimensional fast Fourier transformation to obtain a 2D correlation
function. In practice, we will test two grids, which we name *full-range
FFT* method and *half-range FFT* method.

#### Full-range FFT

The full-range FFT is defined by a grid of shape $`(2N,2N)`$. Since the
grid is radial, it will be centered. This implies that if we want to
keep information of all $`N`$ modes,
``` math
\frac{2\pi}{L},\, \frac{4\pi}{L},\,\cdot\cdot\cdot\,,\, \frac{2\pi}{L}N,
```
the grid will have to be at least of shape $`M=2N`$. The advantages of
this method:

- it keeps information on the full range of modes.

The disadvantages:

- it introduces rounding errors, as the field has shape $`(N,N)`$ and
  not all of the possible distance combinations of such a grid are
  covered bya grid of shape $`(2N,2N)`$.

#### Half-range FFT

The half-range FFT is defined by a grid of shape $`(N,N)`$. The
advantages of this method:

- has the perk of having no shape mismatch between field and correlation
  function.

The disadvantages:

- it loses half of the $`l`$-range, missing information on small scales.

# Results

## Power spectrum recovery

### Gaussian and lognormal fields

We begin by testing the consistency of our Gaussian and lognormal maps
generation pipeline.

<figure id="fig:fields dist">
<embed src="images/4_Gaussian_lognormal_dist.pdf"
style="width:100.0%" />
<figcaption><span id="fig:fields dist"
data-label="fig:fields dist"></span> Comparison of a Gaussian map, on
the left, with a lognormal map on the right. Both maps arise from the
same random seed. The colorbar has been adjusted to enhance the
differences between the two. The histogram plot shows the clear
difference in the map distributions.</figcaption>
</figure>

We show example realisations of the two fields in *Fig.*
<a href="#fig:fields dist" data-reference-type="ref"
data-reference="fig:fields dist">4.1</a>, Gaussian on left and lognormal
on the right. There’s a visible difference between the two, as it can be
seen clearly from the distribution plot. The main check to perform is
for testing whether the generated fields recover the theoretical power
spectrum. *Fig.* <a href="#fig:check fields" data-reference-type="ref"
data-reference="fig:check fields">4.2</a> shows that this is the case
for the Gaussian fields. They recover the fiducial $`C(l)`$ within a few
percent error, with larger deviations $`\sim 5\%`$ at the low and high
ends of the $`l`$-range. Instead, lognormal fields present deviations
$`\gtrsim 10\%`$. As the lognormal transformations we use have been
reported by different sources (Zhou et al. 2023)(Supranta Sarma Boruah,
Rozo, and Fiedorowicz 2022), the issue must lie with our `JAX`
implementation of the Hankel transformation. Resolving such issues could
be achieved by future iterations of this work. In this work, we restrict
ourselves to the use of Gaussian fields, as it is enough to prove our
thesis and show that Gaussian processes can be applied to cosmological
fields.

<figure id="fig:check fields">
<embed src="images/4_Gaussian_lognormal_check.pdf"
style="width:100.0%" />
<figcaption><span id="fig:check fields"
data-label="fig:check fields"></span> Power spectrum estimation from
Gaussian and lognormal maps. Mean and standard deviation are calculated
with 500 realisation of both fields.</figcaption>
</figure>

### Gaussian process priors

First, we test the ability of the kernels we have built in *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">3.2</a> to recover the
power spectrum of our cosmology.

<figure id="fig:check methods">
<embed src="images/3_kernel_comparison.pdf" />
<figcaption><span id="fig:check methods"
data-label="fig:check methods"></span> Reconstructed power spectrum from
prior sample of GP with the four proposed kernels: integration, FFTlog,
full-range FFT, half-range FFT and sinc FFTlog. Mean and standard
deviation are calculated with 500 prior samples from each GP.
</figcaption>
</figure>

We test five models in *Fig.*
<a href="#fig:check methods" data-reference-type="ref"
data-reference="fig:check methods">4.3</a>: integration, FFTlog,
full-range FFT, half-range FFT and sinc FFTlog. The first four methods
are described in the Gaussian process kernels *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">3.2</a>, whereas the sinc
FFTlog referes to a FFTlog model on which we applied smoothing, by
multiplying the power spectrum by a factor of
$`sinc^4(l\frac{L}{2\pi N})`$. The recovered power spectra are plotted
against the fiducial power spectrum, or smoothed power spectrum for the
sinc FFTlog. Mean and standard deviation associated to the plots are
calculated from 500 samples. As expected the integration, FFTlog and
full-range FFT perform similarly, as they all contain the same ammount
of information. As these models deviate so strongly from the fiducial
power spectrum we tried applying smoothing, which helps to recover half
of the $`l`$-range at large scales. The only method that seems to be
consistently recovering the fiducial power spectrum is the half-range
FFT. One could argue that due to the inherent discreteness and
boundedness of the fields we are working with, using FFTs is the most
natural choice; also, half-range FFT uses the only grid that recovers a
correlation function of the same shape as the field without having to
perform binning.

<figure id="fig:check cosmology">
<embed src="images/3_cosmology_comparison.pdf" />
<figcaption><span id="fig:check cosmology"
data-label="fig:check cosmology"></span> Reconstructed power spectrum
from prior samples of a GP, as a function of <span
class="math inline">\(\{\sigma_8, S_8\}\)</span>. Mean and standard
deviation are calculated with 500 prior samples for each different
cosmology.</figcaption>
</figure>

We have also tested the efficacy of the half-range FFT model for
different cosmologies of values $`\{\sigma_8, S_8\}`$ equal to
$`\{0.4,0.2\}`$, $`\{1.2,1.5\}`$ and, our fiducial cosmology,
$`\{0.8,0.8\}`$. As *Fig.*
<a href="#fig:check cosmology" data-reference-type="ref"
data-reference="fig:check cosmology">4.4</a> shows, the model is
independent of the choice of cosmology. From here on the results will be
presented assuming a kernel built with the half-range FFT model.

## Gaussian process map reconstruction

Armed with a reliable kernel, let’s embark upon the journey of
reconstructing a heavily masked cosmological field. What we will do is:
create a noiseless GRF in the fiducial cosmology *Tab.*
<a href="#tab:fiducial_cosmology" data-reference-type="ref"
data-reference="tab:fiducial_cosmology">[tab:fiducial_cosmology]</a>,
*True* map; apply a mask to obtain the *Data* map; condition a Gaussian
process which assumes the fiducial cosmology. *Fig.*
<a href="#fig:GP reconstruction summary" data-reference-type="ref"
data-reference="fig:GP reconstruction summary">4.5</a> lists the result
of this operation, showing the resulting mean $`\mu`$ and standard
deviation $`\sigma`$ of the conditioned GP. We also plot the ratio
between residuals $`\Delta=\mu-`$*True* and standard deviation squared,
to test the goodness of fit of our model, the values of the map sum up
to $`\chi^2 \sim 2495`$. With the mask covering $`\nu=2353`$ pixels, we
obtain $`\chi^2 / \nu = 1.06`$. Of course, this is just a noiseless
application, which is unreasonable for a real application.

<figure id="fig:GP reconstruction summary">
<embed src="images/2_summary.pdf" />
<figcaption><span id="fig:GP reconstruction summary"
data-label="fig:GP reconstruction summary"></span>Summary of field
reconstruction abilities of a Gaussian process conditioned on data. The
left column shows the masked GRF, which is our data. The middle column
shows the true GRF without masks and a posterior sample drawn from the
conditioned GP. The right column shows maps of the mean, standard
deviation and residuals over standard deviation squared of the
conditioned GP. Regions of higher uncertainty correspond to the masked
regions. The residuals over standard deviation map also shows how
regions with low mask recover the data.</figcaption>
</figure>

## Inference of cosmological parameters

To test the ability of Gaussian processes to recover cosmological
parameters without any prior knowledge except a noisy and masked map, we
perform a MCMC simulation to infer the posterior distributions of
$`\sigma_8`$ and $`S_8`$. We use the convention
``` math
S_8 = \sigma_8 \sqrt{\frac{\Omega_m}{0.3}},
    \label{eq:S8}
```

<div class="wraptable">

l3.7cm

|              | Prior                       |
|:-------------|:----------------------------|
| $`S_8`$      | $`\mathcal{U}[0.565,1.78]`$ |
| $`\sigma_8`$ | $`\mathcal{U}[0.4,1]`$      |
| $`\Omega_m`$ | $`\mathcal{U}[0.15,0.95]`$  |

</div>

to infer deterministically a posterior for $`\Omega_m`$. Such a
reparametrisation is needed due to the strong degeneracy between
$`\sigma_8`$ and $`\Omega_m`$. *Eq.*
<a href="#eq:S8" data-reference-type="eqref"
data-reference="eq:S8">[eq:S8]</a> breaks this degeneracy, changing the
geometry of the sampling space and making the sampling more consistent.
The model assumes uninformed flat priors for the cosmological
parameters, as shown in *Tab.*
<a href="#tab:priors" data-reference-type="ref"
data-reference="tab:priors">[tab:priors]</a>, such prior bounds are also
in accordance with the `jaxcosmo` release (Campagne et al. 2023). The
likelihood of the model is given by a Gaussian process distribution
conditioned on *Data*, with a standard deviation equal to the noise
applied to the map. The analysis is coded with `numpyro` (Phan, Pradhan,
and Jankowiak 2019) (Bingham et al. 2019), using a the *No-U-Turn
Sampler (NUTS)* method with `max_tree_depth=16`,
`target_accept_prob=0.8`. We simulate 8 chains for the $`32\times32`$
grid and 4 chains for the $`64\times64`$. Each chain performs 1000
warmup steps and 3000 samples.

### One parameter

As a first step and for a consistency check, we run the inference model
for one cosmological parameter, keeping all others fixed. Using a
$`64\times64`$ grid with $`n_g=10 \text{ galaxies}/\text{arcmin}^2`$. In
*Fig.* <a href="#fig:MCMC one parameter" data-reference-type="ref"
data-reference="fig:MCMC one parameter">4.6</a> we show the inferred
distribution for both $`\sigma_8`$ and $`\Omega_m`$. We find that we are
able to recover the true value for both parameters within two sigmas,
$`\sigma_8 = 0.776\pm0.015`$ and $`\Omega_m = 0.284\pm0.010`$. We notice
a slight tendency of the inferred distribution to be biased low; a
tendency we also observe next for both sampled parameters, $`S_8`$ and
$`\sigma_8`$.

<figure id="fig:MCMC one parameter">
<div class="minipage">
<embed src="images/6_MCMC_sigma_parameters.pdf" />
</div>
<div class="minipage">
<embed src="images/6_MCMC_omega_parameters.pdf" />
</div>
<figcaption><span id="fig:MCMC one parameter"
data-label="fig:MCMC one parameter"></span> Inferred posterior
distribution of <span class="math inline">\(\sigma_8\)</span> on the
left and <span class="math inline">\(\Omega_m\)</span> on the right.
Dotted lines indicate the <span class="math inline">\(1\sigma\)</span>
level. Truth values corresponding to the fiducial cosmology are
indicated in blue.</figcaption>
</figure>

### Two parameters

#### Effect of noise

<div id="tab:inferred cosmological parameters">

| $`\sigma_\text{noise}`$ | $`0.0069`$ | $`0.0044`$ | $`0.0025`$ | $`0.0014`$ |
|:---|:--:|:--:|:--:|:--:|
| $`S_8`$ | $`0.716\pm0.043`$ | $`0.733\pm0.040`$ | $`0.747\pm0.041`$ | $`0.752\pm0.042`$ |
| $`\sigma_8`$ | $`0.645\pm0.157`$ | $`0.628\pm0.158`$ | $`0.632\pm0.166`$ | $`0.631\pm0.170`$ |
| $`\Omega_m`$ | $`0.423\pm0.164`$ | $`0.469\pm0.175`$ | $`0.485\pm0.186`$ | $`0.497\pm0.193`$ |

List of inferred cosmological parameters inferred by the model with a
small $`32\times32`$ grid and for a fixed true GRF realisation. We
present the cosmological parameters inferred as we increase the noise
level, corresponding to $`n_g = 4`$, $`10`$, $`30`$ and
$`100 \text{ galaxies}/\text{arcmin}^2`$.

</div>

We perform some tests on low resolution $`32\times32`$ grids to see the
effect that the noise level has on the recovered parameters, see *Tab.*
<a href="#tab:inferred cosmological parameters"
data-reference-type="ref"
data-reference="tab:inferred cosmological parameters">4.1</a>. Here we
report the inferred cosmological parameters for one data realisation and
different noise levels, corresponding respectively to $`n_g = 4`$,
$`10`$, $`30`$ and $`100 \text{ galaxies}/\text{arcmin}^2`$, see *Eq.*
<a href="#eq:noise" data-reference-type="eqref"
data-reference="eq:noise">[eq:noise]</a>. The inferred value of $`S_8`$
can vary as much as a full $`\sigma`$ between high and low noise runs.
Keeping in mind that $`\sigma_8`$ and $`\Omega_m`$ are extremely
unreliable due to relative uncertainties of $`\sim 25-30\%`$ caused by
the degeneracy: as a general trend we notice $`\Omega_m`$ gets bigger
when $`\sigma_8`$ gets smaller with less noise.

#### Inferred cosmological parameters

Running the model for a larger $`64\times64`$ grid with
$`n_g=10 \text{ galaxies}/\text{arcmin}^2`$, gives much better
constraints on the cosmological parameters. We present the values
recovered by the posterior distributions, listed as follows in *Tab.*
<a href="#tab:inferred cosmological parameters (64,64)"
data-reference-type="ref"
data-reference="tab:inferred cosmological parameters (64,64)">4.2</a>.

<div id="tab:inferred cosmological parameters (64,64)">

|      $`S_8`$      |   $`\sigma_8`$    |   $`\Omega_m`$    |
|:-----------------:|:-----------------:|:-----------------:|
| $`0.762\pm0.028`$ | $`0.745\pm0.151`$ | $`0.353\pm0.143`$ |

Mean and sigma values recovered from the inferred distributions of the
cosmological parameters.

</div>

*Fig.* <a href="#fig:MCMC two parameters" data-reference-type="ref"
data-reference="fig:MCMC two parameters">4.7</a> shows the inferred
posterior distributions and contours for the three cosmological
parameters $`\sigma_8`$, $`\Omega_m`$ and $`S_8`$. Looking at the
contours, we obtain the well known banana-shaped degeneracy between
$`\sigma_8`$ and $`\Omega_m`$. The $`S_8`$ and $`\Omega_m`$ contour
presents sharp cuts for high and low $`\Omega_m`$, indicating an issue
with the bounds of the uniform priors imposed. Unfortunately the
`jaxcosmo` package does not allow for the choice of priors to be wider
than what shown in *Tab.*
<a href="#tab:priors" data-reference-type="ref"
data-reference="tab:priors">[tab:priors]</a>, as the model then starts
to have divergent samples.

<figure id="fig:MCMC two parameters">
<embed src="images/5_MCMC_two_parameters.pdf" />
<figcaption><span id="fig:MCMC two parameters"
data-label="fig:MCMC two parameters"></span> Inferred posterior
distributions of <span class="math inline">\(S_8\)</span>, <span
class="math inline">\(\sigma_8\)</span> and <span
class="math inline">\(\Omega_m\)</span>. For noise level <span
class="math inline">\(\sigma_\text{noise}\sim 0.0088\)</span>. Contours
indicate the <span class="math inline">\(1\sigma\)</span> and <span
class="math inline">\(2\sigma\)</span> credible interval respectively.
Dotted lines indicate the <span class="math inline">\(1\sigma\)</span>
level. Truth values corresponding to the fiducial cosmology are
indicated in blue.</figcaption>
</figure>

### Posterior checks

Following the two parameter inference model, we perform some posterior
checks at the map level (Porqueres et al. 2021). *Fig.*
<a href="#fig:MCMC summary" data-reference-type="ref"
data-reference="fig:MCMC summary">4.9</a> sums up the ability of the
model to recover the true map, noiseless and unmasked. Here we present
the run with noise level $`\sigma_\text{noise}\sim 0.0088`$ and a
$`64\times64`$ grid. We show the mean and standard deviation for the
sample with highest likelihood out of the $`12000`$. The mean field
$`\mu`$ is visibly different to the true field in the masked regions and
it seems to be of overall lower amplitude. The sample map is comparable
to the noisy data; which is to be expected, as the internal noise given
to the Gaussian process is the same as the noise level of the data. The
standard deviation map $`\sigma`$ presents an overall amplitude
comparable to the noise level $`\sim 0.010`$, with higher values for the
masked regions. Summing up the map values of the residuals divided by
standard deviation squared, we obtain a $`\chi^2\sim 1297.4`$. Compared
to the number of free parameters $`\nu`$ in our inference model, which
for a $`10\%`$ mask and a $`64\times64`$ grid, is $`\nu=3689`$. The
value of $`\chi^2`$ therefore seems to be low, indicating that the noise
level assumed by the GP is overestimated. This is supported by the fact
that the sample map looks just as noisy as the data, according to *Fig.*
<a href="#fig:residuals vs noise" data-reference-type="ref"
data-reference="fig:residuals vs noise">4.8</a>, its distribution is in
fact just as wide as the noise.

<figure id="fig:residuals vs noise">
<embed src="images/5_residuals_vs_noise.pdf" style="width:50.0%" />
<p><em>Residuals</em></p>
<figcaption><span id="fig:residuals vs noise"
data-label="fig:residuals vs noise"></span> Residual distributions of
the mean and sample compared to noise. The mean is less spread, whereas
the sample is wider.</figcaption>
</figure>

<figure id="fig:MCMC summary">
<embed src="images/5_summary.pdf" />
<figcaption><span id="fig:MCMC summary"
data-label="fig:MCMC summary"></span> Summary of the two parameter
inference at the map level. The left column shows the masked and noisy
GRF realisation used, which is our data. The middle column shows the
true GRF and a sample from the conditioned GP. The right column shows
maps of the mean, standard deviation and residuals over standard
deviation squared resulting from the numpyro model sample with highest
likelihood. Regions of higher uncertainty correspond to the masked
regions.</figcaption>
</figure>

# Conclusion

We have hereby introduced the tool of Gaussian processes to the
landscape of map inference of cosmological fields, in particular weak
lensing convergence. We considered how the 2-point statistics of
cosmological fields changes when we are dealing with bounded and
discrete maps in *Sec.*
<a href="#sec:weak lensing" data-reference-type="ref"
data-reference="sec:weak lensing">2.1</a>. We discussed the realisation
of Gaussian and lognormal fields in *Sec.*
<a href="#sec:field generation" data-reference-type="ref"
data-reference="sec:field generation">2.2</a>, and showed their ability
to recover the 2-point statistics that they encode, in *Sec.*
<a href="#sec:gaussian and lognormal fields" data-reference-type="ref"
data-reference="sec:gaussian and lognormal fields">4.1.1</a>. We have
included masking and noise to the data to simulate realistic maps in
*Sec.* <a href="#sec:data simulation" data-reference-type="ref"
data-reference="sec:data simulation">3.1</a>. We have shown that it is
possible to apply physical knowledge about the 2-point correlation
function of a cosmological field in order to set up a Gaussian process
able to produce a Gaussian realisation of such a field. We considered
different set ups for the Gaussian process kernel in *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">3.2</a> and showed how they
fare against one another in *Sec.*
<a href="#sec:gaussian process priors" data-reference-type="ref"
data-reference="sec:gaussian process priors">4.1.2</a>, ultimately
proving empirically that the half-range FFT model is the best. In *Sec.*
<a href="#sec:gaussian process map reconstruction"
data-reference-type="ref"
data-reference="sec:gaussian process map reconstruction">4.2</a> we
present an application of Gaussian processes to a noiseless masked
convergence map, in order to showcase its ability to reconstruct a
heavily masked map. Finally we present our results for the cosmological
parameters inference with GPs, conditioning on noisy and masked data.
When running the inference model on one cosmological parameter we
recover both parameters within two sigmas, $`\sigma_8 = 0.776\pm0.015`$
and $`\Omega_m = 0.284\pm0.010`$. For the two parameter inference we
observe the well known banana-shaped degeneracy between $`\sigma_8`$ and
$`\Omega_m`$, as well as recovering $`0.762\pm0.028`$ within two sigmas.

In future studies GPs could be tested on maps with larger grids. In
order to achieve a resolution of $`\sim 3`$ arcmin with a map of size
$`(10^\circ,10^\circ)`$, a $`200\times200`$ grid is needed. Too big for
a GP. The bottleneck is given by the inversion of the kernel matrix, see
<a href="#eq:conditioning" data-reference-type="eqref"
data-reference="eq:conditioning">[eq:conditioning]</a>. Approximations
of this operation could enable the use of GPs on larger grids. This can
lead to the possibility of applying this method on current weak lensing
catalogues and perhaps even full sky catalogues. Another pathway to
explore are lognormal fields, as they do a much better job at simulating
data than GRFs. Due to GPs being Gaussian, their associated likelihood
is not suitable to treat lognormal fields. A modified likelihood could
therefore unlock a correct application of GPs to lognormal fields.

## Acknowledgments

This project wouldn’t have been possible without the author of the idea,
Dr. Tilman Tröster. You guided me through my first real research
experience and I am grateful. Thank you Veronika Oehl for always being
there and for the very helpful discussions. I also express my gratitude
to the Cosmology group at ETH, led by Prof. Alexandre Réfrégier. Hearing
about my every progress every Monday morning for six months, couldn’t
have been easy, thank you. It has been an incredible experience, long
and grinding, which I embarked upon with my friends and colleagues
Tommaso and Pietro. Thank you for making these past few months
memorable. Thanks to Guido van Rossum for giving us `Python`. Thank you
Mia, for your unconditional support, *you* keep me grounded. Non sarei
qua senza di te mamma, grazie.

<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-cosmology:kids1000" class="csl-entry">

Asgari, Marika, Lin, Chieh-An, Joachimi, Benjamin, Giblin, Benjamin,
Heymans, Catherine, Hildebrandt, Hendrik, Kannawadi, Arun, et al. 2021.
“KiDS-1000 Cosmology: Cosmic Shear Constraints and Comparison Between
Two Point Statistics.” *A&A* 645: A104.
<https://doi.org/10.1051/0004-6361/202039070>.

</div>

<div id="ref-cosmology:lensing2" class="csl-entry">

Bartelmann, M., and M. Maturi. 2017. “Weak Gravitational Lensing.”
*Scholarpedia* 12 (1): 32440.
<https://doi.org/10.4249/scholarpedia.32440>.

</div>

<div id="ref-grf" class="csl-entry">

Bertschinger, Edmund. 2001. “Multiscale Gaussian Random Fields and Their
Application to Cosmological Simulations.” *The Astrophysical Journal
Supplement Series* 137 (1): 1. <https://doi.org/10.1086/322526>.

</div>

<div id="ref-numpyro2" class="csl-entry">

Bingham, Eli, Jonathan P. Chen, Martin Jankowiak, Fritz Obermeyer,
Neeraj Pradhan, Theofanis Karaletsos, Rohit Singh, Paul A. Szerlip, Paul
Horsfall, and Noah D. Goodman. 2019. “Pyro: Deep Universal Probabilistic
Programming.” *J. Mach. Learn. Res.* 20: 28:1–6.
<http://jmlr.org/papers/v20/18-403.html>.

</div>

<div id="ref-weaklensing" class="csl-entry">

Blandford, R. D., A. B. Saust, T. G. Brainerd, and J. V. Villumsen.
1991. “<span class="nocase">The distortion of distant galaxy images by
large scale structure</span>.” *AIP Conference Proceedings* 222 (1):
455–58. <https://doi.org/10.1063/1.40414>.

</div>

<div id="ref-lognormal" class="csl-entry">

Boruah, Supranta Sarma, Eduardo Rozo, and Pier Fiedorowicz. 2022.
“Map-Based Cosmology Inference with Lognormal Cosmic Shear Maps.”
<https://arxiv.org/abs/2204.13216>.

</div>

<div id="ref-gp:acceleration2" class="csl-entry">

Boruah, Supranta S, Tim Eifler, Vivian Miranda, and P M Sai Krishanth.
2022. “<span class="nocase">Accelerating cosmological inference with
Gaussian processes and neural networks – an application to LSST Y1 weak
lensing and galaxy clustering</span>.” *Monthly Notices of the Royal
Astronomical Society* 518 (4): 4818–31.
<https://doi.org/10.1093/mnras/stac3417>.

</div>

<div id="ref-jax" class="csl-entry">

Bradbury, James, Roy Frostig, Peter Hawkins, Matthew James Johnson,
Chris Leary, Dougal Maclaurin, George Necula, et al. 2018. “JAX:
Composable Transformations of Python+NumPy Programs.”
<http://github.com/google/jax>.

</div>

<div id="ref-cellestim2" class="csl-entry">

Brown, M. L., P. G. Castro, and A. N. Taylor. 2005.
“<span class="nocase">Cosmic microwave background temperature and
polarization pseudo-$`C_\ell`$ estimators and covariances</span>.”
*Monthly Notices of the Royal Astronomical Society* 360 (4): 1262–80.
<https://doi.org/10.1111/j.1365-2966.2005.09111.x>.

</div>

<div id="ref-jaxcosmo" class="csl-entry">

Campagne, Jean-Eric, François Lanusse, Joe Zuntz, Alexandre Boucaud,
Santiago Casas, Minas Karamanis, David Kirkby, Denise Lanzieri, Austin
Peel, and Yin Li. 2023. “JAX-COSMO: An End-to-End Differentiable and GPU
Accelerated Cosmology Library.” *The Open Journal of Astrophysics* 6
(April). <https://doi.org/10.21105/astro.2302.05163>.

</div>

<div id="ref-cellestim" class="csl-entry">

Chon, Gayoung, Anthony Challinor, Simon Prunet, Eric Hivon, and István
Szapudi. 2004. “<span class="nocase">Fast estimation of polarization
power spectra using correlation functions</span>.” *Monthly Notices of
the Royal Astronomical Society* 350 (3): 914–26.
<https://doi.org/10.1111/j.1365-2966.2004.07737.x>.

</div>

<div id="ref-noise" class="csl-entry">

Croft, Rupert A. C., Peter E. Freeman, Thomas S. Schuster, and Chad M.
Schafer. 2017. “<span class="nocase">Prediction of galaxy ellipticities
and reduction of shape noise in cosmic shear measurements</span>.”
*Monthly Notices of the Royal Astronomical Society* 469 (4): 4422–27.
<https://doi.org/10.1093/mnras/stx1206>.

</div>

<div id="ref-dodelson" class="csl-entry">

Dodelson, Scott, and Fabian Schmidt. 2021. “13 - Probes of Structure:
Lensing.” In *Modern Cosmology (Second Edition)*, edited by Scott
Dodelson and Fabian Schmidt, Second Edition, 373–99. Academic Press.
https://doi.org/<https://doi.org/10.1016/B978-0-12-815948-4.00019-X>.

</div>

<div id="ref-tinygp" class="csl-entry">

Foreman-Mackey, Daniel, Weixiang Yu, Sachin Yadav, McCoy Reynolds
Becker, Neven Caplar, Daniela Huppenkothen, Thomas Killestein, René
Tronsgaard, Theo Rashid, and Steve Schmerler. 2024.
“<span class="nocase">dfm/tinygp: The tiniest of Gaussian Process
libraries</span>.” Zenodo. <https://doi.org/10.5281/zenodo.10463641>.

</div>

<div id="ref-flatsky2" class="csl-entry">

Gao, Zucheng, Alvise Raccanelli, and Zvonimir Vlah. 2023. “Asymptotic
Connection Between Full- and Flat-Sky Angular Correlators.” *Phys. Rev.
D* 108 (August): 043503. <https://doi.org/10.1103/PhysRevD.108.043503>.

</div>

<div id="ref-flatsky4" class="csl-entry">

Gao, Zucheng, Zvonimir Vlah, and Anthony Challinor. 2023. “Flat-Sky
Angular Power Spectra Revisited.” <https://arxiv.org/abs/2307.13768>.

</div>

<div id="ref-flatsky5" class="csl-entry">

García-García, Carlos, David Alonso, and Emilio Bellini. 2019.
“Disconnected Pseudo-$`C_\ell`$ Covariances for Projected Large-Scale
Structure Data.” *Journal of Cosmology and Astroparticle Physics* 2019
(11): 043. <https://doi.org/10.1088/1475-7516/2019/11/043>.

</div>

<div id="ref-pixel" class="csl-entry">

Grewal, Nisha, Joe Zuntz, and Tilman Tröster. 2024. “Comparing Mass
Mapping Reconstruction Methods with Minkowski Functionals.”
<https://arxiv.org/abs/2402.13912>.

</div>

<div id="ref-cosmology:hsc" class="csl-entry">

Hikage, Chiaki, Masamune Oguri, Takashi Hamana, Surhud More, Rachel
Mandelbaum, Masahiro Takada, Fabian Köhlinger, et al. 2019.
“<span class="nocase">Cosmology from cosmic shear power spectra with
Subaru Hyper Suprime-Cam first-year data</span>.” *Publications of the
Astronomical Society of Japan* 71 (2): 43.
<https://doi.org/10.1093/pasj/psz010>.

</div>

<div id="ref-lognormal3" class="csl-entry">

Hilbert, S., Hartlap, J., and Schneider, P. 2011. “Cosmic Shear
Covariance: The Log-Normal Approximation.” *A&A* 536: A85.
<https://doi.org/10.1051/0004-6361/201117294>.

</div>

<div id="ref-cosmology:kids1000_bins" class="csl-entry">

Hildebrandt, H., van den Busch, J. L., Wright, A. H., Blake, C.,
Joachimi, B., Kuijken, K., Tröster, T., et al. 2021. “KiDS-1000
Catalogue: Redshift Distributions and Their Calibration.” *A&A* 647:
A124. <https://doi.org/10.1051/0004-6361/202039018>.

</div>

<div id="ref-gp:expansion3" class="csl-entry">

Holsclaw, Tracy, Ujjaini Alam, Bruno Sansó, Herbert Lee, Katrin
Heitmann, Salman Habib, and David Higdon. 2010. “Nonparametric
Reconstruction of the Dark Energy Equation of State.” *Phys. Rev. D* 82
(November): 103502. <https://doi.org/10.1103/PhysRevD.82.103502>.

</div>

<div id="ref-gp:acceleration3" class="csl-entry">

Karchev, Konstantin, Adam Coogan, and Christoph Weniger. 2022.
“<span class="nocase">Strong-lensing source reconstruction with
variationally optimized Gaussian processes</span>.” *Monthly Notices of
the Royal Astronomical Society* 512 (1): 661–85.
<https://doi.org/10.1093/mnras/stac311>.

</div>

<div id="ref-cosmology:lensing" class="csl-entry">

Kilbinger, Martin. 2015. “Cosmology with Cosmic Shear Observations: A
Review.” *Reports on Progress in Physics* 78 (8): 086901.
<https://doi.org/10.1088/0034-4885/78/8/086901>.

</div>

<div id="ref-smail2" class="csl-entry">

Kirk, Donnacha, Anais Rassat, Ole Host, and Sarah Bridle. 2012.
“<span class="nocase">The cosmological impact of intrinsic alignment
model choice for cosmic shear</span>.” *Monthly Notices of the Royal
Astronomical Society* 424 (3): 1647–57.
<https://doi.org/10.1111/j.1365-2966.2012.21099.x>.

</div>

<div id="ref-cosmology:kids450" class="csl-entry">

Köhlinger, F., M. Viola, B. Joachimi, H. Hoekstra, E. van Uitert, H.
Hildebrandt, A. Choi, et al. 2017. “<span class="nocase">KiDS-450: the
tomographic weak lensing power spectrum and constraints on cosmological
parameters</span>.” *Monthly Notices of the Royal Astronomical Society*
471 (4): 4412–35. <https://doi.org/10.1093/mnras/stx1820>.

</div>

<div id="ref-grf2" class="csl-entry">

Lang, Annika, and Jürgen Potthoff. 2011. *Monte Carlo Methods and
Applications* 17 (3): 195–214.
<https://doi.org/doi:10.1515/mcma.2011.009>.

</div>

<div id="ref-lognormal2" class="csl-entry">

Leclercq, Florent, and Alan Heavens. 2021. “<span class="nocase">On the
accuracy and precision of correlation functions and field-level
inference in cosmology</span>.” *Monthly Notices of the Royal
Astronomical Society: Letters* 506 (1): L85–90.
<https://doi.org/10.1093/mnrasl/slab081>.

</div>

<div id="ref-flatsky3" class="csl-entry">

Matthewson, William L., and Ruth Durrer. 2021. “The Flat Sky
Approximation to Galaxy Number Counts.” *Journal of Cosmology and
Astroparticle Physics* 2021 (02): 027.
<https://doi.org/10.1088/1475-7516/2021/02/027>.

</div>

<div id="ref-gp:acceleration" class="csl-entry">

Mootoovaloo, Arrykrishna, Alan F Heavens, Andrew H Jaffe, and Florent
Leclercq. 2020. “<span class="nocase">Parameter inference for weak
lensing using Gaussian Processes and MOPED</span>.” *Monthly Notices of
the Royal Astronomical Society* 497 (2): 2213–26.
<https://doi.org/10.1093/mnras/staa2102>.

</div>

<div id="ref-flatsky" class="csl-entry">

Nicola, Andrina, Carlos García-García, David Alonso, Jo Dunkley, Pedro
G. Ferreira, Anže Slosar, and David N. Spergel. 2021. “Cosmic Shear
Power Spectra in Practice.” *Journal of Cosmology and Astroparticle
Physics* 2021 (03): 067.
<https://doi.org/10.1088/1475-7516/2021/03/067>.

</div>

<div id="ref-numpyro" class="csl-entry">

Phan, Du, Neeraj Pradhan, and Martin Jankowiak. 2019.
“<span class="nocase">Composable Effects for Flexible and Accelerated
Probabilistic Programming in NumPyro</span>.” *arXiv e-Prints*, October,
arXiv:1912.11554. <https://doi.org/10.48550/arXiv.1912.11554>.

</div>

<div id="ref-fwdmodel2" class="csl-entry">

Porqueres, Natalia, Alan Heavens, Daniel Mortlock, and Guilhem Lavaux.
2021. “<span class="nocase">Bayesian forward modelling of cosmic shear
data</span>.” *Monthly Notices of the Royal Astronomical Society* 502
(2): 3035–44. <https://doi.org/10.1093/mnras/stab204>.

</div>

<div id="ref-rasmussen" class="csl-entry">

Rasmussen, Carl Edward, and Christopher K. I. Williams. 2005.
*<span class="nocase">Gaussian Processes for Machine Learning</span>*.
The MIT Press. <https://doi.org/10.7551/mitpress/3206.001.0001>.

</div>

<div id="ref-flatsky6" class="csl-entry">

Schneider, P., van Waerbeke, L., Kilbinger, M., and Mellier, Y. 2002.
“Analysis of Two-Point Statistics of Cosmic Shear - i. Estimators and
Covariances.” *A&A* 396 (1): 1–19.
<https://doi.org/10.1051/0004-6361:20021341>.

</div>

<div id="ref-gp:expansion2" class="csl-entry">

Seikel, Marina, Chris Clarkson, and Mathew Smith. 2012. “Reconstruction
of Dark Energy and Expansion Dynamics Using Gaussian Processes.”
*Journal of Cosmology and Astroparticle Physics* 2012 (06): 036.
<https://doi.org/10.1088/1475-7516/2012/06/036>.

</div>

<div id="ref-gp:expansion" class="csl-entry">

Shafieloo, Arman, Alex G. Kim, and Eric V. Linder. 2012. “Gaussian
Process Cosmography.” *Phys. Rev. D* 85 (June): 123530.
<https://doi.org/10.1103/PhysRevD.85.123530>.

</div>

<div id="ref-fftlog" class="csl-entry">

Simonović, Marko, Tobias Baldauf, Matias Zaldarriaga, John Joseph
Carrasco, and Juna A. Kollmeier. 2018. “Cosmological Perturbation Theory
Using the FFTLog: Formalism and Connection to QFT Loop Integrals.”
*Journal of Cosmology and Astroparticle Physics* 2018 (04): 030.
<https://doi.org/10.1088/1475-7516/2018/04/030>.

</div>

<div id="ref-smail" class="csl-entry">

Smail, Ian, David W. Hogg, Lin Yan, and Judith G. Cohen. 1995. “Deep
Optical Galaxy Counts with the Keck Telescope\*.” *The Astrophysical
Journal* 449 (2): L105. <https://doi.org/10.1086/309647>.

</div>

<div id="ref-fwdmodel" class="csl-entry">

Zhou, Alan Junzhe, Xiangchong Li, Scott Dodelson, and Rachel Mandelbaum.
2023. “Accurate Field-Level Weak Lensing Inference for Precision
Cosmology.” <https://arxiv.org/abs/2312.08934>.

</div>

</div>
