# Methods

## Data simulation {#sec:data simulation}

### Cosmology {#subsec:cosmology}

::: {#tab:fiducial_cosmology}
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

  : Fiducial cosmology values given to .
:::

This work follows in the general footsteps of data analysis of weak lensing surveys like *HSC* (Hikage et al. 2019) and *KiDS* (Köhlinger et al. 2017)(Asgari, Marika et al. 2021), as we aim to replicate their methodologies. Throughout the work, we assume a fiducial cosmology of fixed parameter values as shown in *Tab.* [1.1](#tab:fiducial_cosmology){reference-type="ref" reference="tab:fiducial_cosmology"}. In particular, all data maps will be generated from a power spectrum following this cosmology. We will refer to this power spectrum as the fiducial power spectrum $C(l)$. A leading modelling choice comes with the redshift distribution $n(z)$. We model it as a Smail-type distribution (Smail et al. 1995)(Kirk et al. 2012), $$n(z)=z^\alpha \exp{\left[-\left(\frac{z}{z_0}\right)^\beta\right]}.$$ The choice of parameters has been made to emulate bin 5 of the *KiDS1000* survey (Hildebrandt, H. et al. 2021), with parameters $\alpha=3.5$, $\beta=4.5$, $z_0=1$.

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

To generate a GRF, we employ the algorithm mentioned in *Eq.* [\[eq:grf 2D\]](#eq:grf 2D){reference-type="eqref" reference="eq:grf 2D"}. However, in making a lognormal field, the matter is a bit more complicated. Any GRF on which we apply the lognormal transformation $\mathcal{L}_\kappa$, from *Eq.* [\[eq:L_k\]](#eq:L_k){reference-type="eqref" reference="eq:L_k"}, becomes a lognormal field. The reason we do not just lognormal transform any field is given by the fact that they would not recover the fiducial power spectrum $C(l)$. Our goal is therefore to find a transfer GRF $\tilde{\kappa}^G$ which, when transformed lognormally, gives rise to a lognormal field $\kappa^L$ that recovers $C(l)$. To do so, we follow the sequence of transformations illustrated in the top branch of *Fig.* [1.2](#tik:cw){reference-type="ref" reference="tik:cw"}.

### Noise and mask

![Approximately $10\%$ mask applied to the data. Size $(10^{\circ},10^{\circ})$ and grid $64\times64$.](images/5_random_and_blocks_mask.pdf){#fig:mask width="50%"}

As all data is being simulated, we only take into account the so-called shape noise, which is due to the intrinsic distribution of ellipticities and angle formed with respect to us. GPs will treat each pixel of the map as a random variable Gaussianly distributed with standard deviation given by (Croft et al. 2017), $$\sigma_\text{noise} = \frac{\sigma_e}{\sqrt{n_g A_{px}}}.
    \label{eq:noise}$$ We use values of $\sigma_e=0.26$, $n_g= 4, 10, 30, 100 \text{ galaxies}/\text{arcmin}^2$, and a pixel area given by the pixel resolution squared, $A_{px}=(L/N)^2$. For our highest-resolution run, we have $N=64$ and use $n_g = 10 \text{ galaxies}/\text{arcmin}^2$, which results in a noise standard deviation of $\sigma_\text{noise} \sim 0.0088$. The mask being used as seen in *Fig.* [1.3](#fig:mask){reference-type="ref" reference="fig:mask"}, covers approximately $10\%$ of the patch (Grewal, Zuntz, and Tröster 2024). We keep the noise and mask random seeds fixed throughout the work.

## Kernel {#sec:gaussian process kernel}

The kernel of a Gaussian process is given by a function of the form $k(x,y)$. It takes in two points, $x$ and $y$, and returns the value of their correlation. In our case, specifically, $x$ and $y$ will be two points in a grid of shape $(N,N)$, and the kernel function will be the convergence angular autocorrelation function. As all code used for this paper is written in (Bradbury et al. 2018) we opt for the use of the library (Foreman-Mackey et al. 2024) for all Gaussian process computations. allows for the use of a custom kernel with a custom method, which takes two points on the grid and returns the correlation value. We follow with two pseudocodes of our kernel implementations.

``` {#lst:hankel .python language="Python" label="lst:hankel" caption="\\code{kernel_Hankel} uses the helper function \\code{Hankel} which returns a 1D callable correlation function \\code{w}. Then finds the euclidean distance between $x$ and $y$ and evaluates the correlation function at that point. We will discuss how we perform the Hankel transformation in the following section."}
class kernel_Hankel:
    def __init__(self, cl, N, L):
        self.w   = Hankel(cl, N, L)
        self.r   = L / N
        
    def evaluate(self, x, y):
        theta    = self.r * sqrt(sum(x - y))
        return self.w(theta)
```

``` {#lst:FFT .python language="Python" label="lst:FFT" caption="\\code{kernel_FFT} performs a 2D Fourier transform on the power spectrum \\code{cl2D}. This returns a 2D array that is the correlation function. Then to evaluate \\code{w2D} we need two indices. These are given by the difference of $x$ and $y$ component wise. Furthermore we have to be careful about possible mismatches between the shape of \\code{cl2D} and the grid of our map. For this we have the renormalisation factor \\code{r}. We will discuss further how we get \\code{cl2D} in the following section."}
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
    \label{eq:C-w hankel}$$ We will explore two methods for computing this integral: the *integration* method *Sec.* [1.2.1.1](#sec:integration method){reference-type="ref" reference="sec:integration method"} and the *FFTlog* method *Sec.* [1.2.1.2](#sec:FFTlog method){reference-type="ref" reference="sec:FFTlog method"}.

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

The second transformation that we can use to go from power spectrum to correlation function, is the Fourier transformation discussed in *Eq.* [\[eq:flatsky fft\]](#eq:flatsky fft){reference-type="eqref" reference="eq:flatsky fft"}. It is a more fundamental relation than the Hankel transformation as it does not assume that $l$ is radially symmetric. In our case, low resolution, coupled with a square map, means that the radial assumption might not apply. Note that, the lowest resolution grid we use is $32\times32$, with $L/N \sim 19$ arcmin; which is one order of magnitude worse than today's weak lensing data, around $\sim 3$ arcmin according to (Zhou et al. 2023). In the following *Sec.* [1.2](#sec:gaussian process kernel){reference-type="ref" reference="sec:gaussian process kernel"} we will find experimentally that the Hankel methods described above do not work well with our GP setup. For this reason, we explore this method of conversion between angular power spectrum and correlation function, $$w(\theta)=\int\frac{d^2l}{4\pi^2}e^{-i\bm{l}\cdot\bm{\theta}}C(l).
    \label{eq:C-w fft}$$ As computers can only deal with discrete functions, it is important to note that we will be performing a *discrete Fourier transformation (DFT)*. We will use the widely known FFT algorithm to compute DFTs. In particular we use JAX's implementation of the 2D FFT algorithm, .

Let us find the relation between continuous Fourier transformation and DFT. The definitions of continuous and discrete Fourier transformations in 1D, are respectively: $$\begin{aligned}
    \mathcal{F}^{-1}&=\int\frac{dk}{2\pi}e^{ikx}, \label{eq:F}\\
    \text{F}^{-1}&=\frac{1}{N}\sum_p e^{ik_px}. \label{eq:DFT}
\end{aligned}$$ First of all, a DFT is dimensionless. Secondly, it is discrete and bounded. We can therefore rewrite *Eq.* [\[eq:F\]](#eq:F){reference-type="eqref" reference="eq:F"} using the substitution $k(p)=2\pi \frac{p}{L}$ to discretise k-space, $$\int\frac{dk}{2\pi}e^{ikx} = \int\frac{dp}{L} e^{ik(p)x} = \frac{1}{L}\sum_p e^{ik_px}.$$ Applying the definition of DFT as seen in *Eq.* [\[eq:DFT\]](#eq:DFT){reference-type="eqref" reference="eq:DFT"}, it follows that in 1D $$\mathcal{F}^{-1}=\frac{N}{L}\text{F}^{-1}.$$ Which means that the correlation function is given by a *backwards* normalised inverse DFT to be scaled by a factor $(N/L)^d$, where $d$ is the dimension of the considered space. In our case, $d=2$.

In order to perform a FFT in 2D, we will need a two dimensional extension of the angular power spectrum. We make use of its radial symmetry with respect to $\bm{l}=(l_x,l_y)$ and create a 2D grid of shape $(M,M)$ as shown in *Fig.* [1.4](#tik:1D to 2D){reference-type="ref" reference="tik:1D to 2D"}.

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

::::::::::::::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}
::: {#ref-cosmology:kids1000 .csl-entry}
Asgari, Marika, Lin, Chieh-An, Joachimi, Benjamin, Giblin, Benjamin, Heymans, Catherine, Hildebrandt, Hendrik, Kannawadi, Arun, et al. 2021. "KiDS-1000 Cosmology: Cosmic Shear Constraints and Comparison Between Two Point Statistics." *A&A* 645: A104. <https://doi.org/10.1051/0004-6361/202039070>.
:::

::: {#ref-jax .csl-entry}
Bradbury, James, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula, et al. 2018. "JAX: Composable Transformations of Python+NumPy Programs." <http://github.com/google/jax>.
:::

::: {#ref-noise .csl-entry}
Croft, Rupert A. C., Peter E. Freeman, Thomas S. Schuster, and Chad M. Schafer. 2017. "[Prediction of galaxy ellipticities and reduction of shape noise in cosmic shear measurements]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 469 (4): 4422--27. <https://doi.org/10.1093/mnras/stx1206>.
:::

::: {#ref-tinygp .csl-entry}
Foreman-Mackey, Daniel, Weixiang Yu, Sachin Yadav, McCoy Reynolds Becker, Neven Caplar, Daniela Huppenkothen, Thomas Killestein, René Tronsgaard, Theo Rashid, and Steve Schmerler. 2024. "[dfm/tinygp: The tiniest of Gaussian Process libraries]{.nocase}." Zenodo. <https://doi.org/10.5281/zenodo.10463641>.
:::

::: {#ref-pixel .csl-entry}
Grewal, Nisha, Joe Zuntz, and Tilman Tröster. 2024. "Comparing Mass Mapping Reconstruction Methods with Minkowski Functionals." <https://arxiv.org/abs/2402.13912>.
:::

::: {#ref-cosmology:hsc .csl-entry}
Hikage, Chiaki, Masamune Oguri, Takashi Hamana, Surhud More, Rachel Mandelbaum, Masahiro Takada, Fabian Köhlinger, et al. 2019. "[Cosmology from cosmic shear power spectra with Subaru Hyper Suprime-Cam first-year data]{.nocase}." *Publications of the Astronomical Society of Japan* 71 (2): 43. <https://doi.org/10.1093/pasj/psz010>.
:::

::: {#ref-cosmology:kids1000_bins .csl-entry}
Hildebrandt, H., van den Busch, J. L., Wright, A. H., Blake, C., Joachimi, B., Kuijken, K., Tröster, T., et al. 2021. "KiDS-1000 Catalogue: Redshift Distributions and Their Calibration." *A&A* 647: A124. <https://doi.org/10.1051/0004-6361/202039018>.
:::

::: {#ref-smail2 .csl-entry}
Kirk, Donnacha, Anais Rassat, Ole Host, and Sarah Bridle. 2012. "[The cosmological impact of intrinsic alignment model choice for cosmic shear]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 424 (3): 1647--57. <https://doi.org/10.1111/j.1365-2966.2012.21099.x>.
:::

::: {#ref-cosmology:kids450 .csl-entry}
Köhlinger, F., M. Viola, B. Joachimi, H. Hoekstra, E. van Uitert, H. Hildebrandt, A. Choi, et al. 2017. "[KiDS-450: the tomographic weak lensing power spectrum and constraints on cosmological parameters]{.nocase}." *Monthly Notices of the Royal Astronomical Society* 471 (4): 4412--35. <https://doi.org/10.1093/mnras/stx1820>.
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
:::::::::::::::
