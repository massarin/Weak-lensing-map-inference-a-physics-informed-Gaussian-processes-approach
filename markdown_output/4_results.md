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
data-reference="fig:fields dist">1.1</a>, Gaussian on left and lognormal
on the right. There’s a visible difference between the two, as it can be
seen clearly from the distribution plot. The main check to perform is
for testing whether the generated fields recover the theoretical power
spectrum. *Fig.* <a href="#fig:check fields" data-reference-type="ref"
data-reference="fig:check fields">1.2</a> shows that this is the case
for the Gaussian fields. They recover the fiducial $`C(l)`$ within a few
percent error, with larger deviations $`\sim 5\%`$ at the low and high
ends of the $`l`$-range. Instead, lognormal fields present deviations
$`\gtrsim 10\%`$. As the lognormal transformations we use have been
reported by different sources (Zhou et al. 2023)(Boruah, Rozo, and
Fiedorowicz 2022), the issue must lie with our implementation of the
Hankel transformation. Resolving such issues could be achieved by future
iterations of this work. In this work, we restrict ourselves to the use
of Gaussian fields, as it is enough to prove our thesis and show that
Gaussian processes can be applied to cosmological fields.

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
data-reference="sec:gaussian process kernel">[sec:gaussian process
kernel]</a> to recover the power spectrum of our cosmology.

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
data-reference="fig:check methods">1.3</a>: integration, FFTlog,
full-range FFT, half-range FFT and sinc FFTlog. The first four methods
are described in the Gaussian process kernels *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">[sec:gaussian process
kernel]</a>, whereas the sinc FFTlog referes to a FFTlog model on which
we applied smoothing, by multiplying the power spectrum by a factor of
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
data-reference="fig:check cosmology">1.4</a> shows, the model is
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
data-reference="fig:GP reconstruction summary">1.5</a> lists the result
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
in accordance with the release (Campagne et al. 2023). The likelihood of
the model is given by a Gaussian process distribution conditioned on
*Data*, with a standard deviation equal to the noise applied to the map.
The analysis is coded with (Phan, Pradhan, and Jankowiak 2019) (Bingham
et al. 2019), using a the *No-U-Turn Sampler (NUTS)* method with , . We
simulate 8 chains for the $`32\times32`$ grid and 4 chains for the
$`64\times64`$. Each chain performs 1000 warmup steps and 3000 samples.

### One parameter

As a first step and for a consistency check, we run the inference model
for one cosmological parameter, keeping all others fixed. Using a
$`64\times64`$ grid with $`n_g=10 \text{ galaxies}/\text{arcmin}^2`$. In
*Fig.* <a href="#fig:MCMC one parameter" data-reference-type="ref"
data-reference="fig:MCMC one parameter">1.6</a> we show the inferred
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
data-reference="tab:inferred cosmological parameters">1.1</a>. Here we
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
data-reference="tab:inferred cosmological parameters (64,64)">1.2</a>.

<div id="tab:inferred cosmological parameters (64,64)">

|      $`S_8`$      |   $`\sigma_8`$    |   $`\Omega_m`$    |
|:-----------------:|:-----------------:|:-----------------:|
| $`0.762\pm0.028`$ | $`0.745\pm0.151`$ | $`0.353\pm0.143`$ |

Mean and sigma values recovered from the inferred distributions of the
cosmological parameters.

</div>

*Fig.* <a href="#fig:MCMC two parameters" data-reference-type="ref"
data-reference="fig:MCMC two parameters">1.7</a> shows the inferred
posterior distributions and contours for the three cosmological
parameters $`\sigma_8`$, $`\Omega_m`$ and $`S_8`$. Looking at the
contours, we obtain the well known banana-shaped degeneracy between
$`\sigma_8`$ and $`\Omega_m`$. The $`S_8`$ and $`\Omega_m`$ contour
presents sharp cuts for high and low $`\Omega_m`$, indicating an issue
with the bounds of the uniform priors imposed. Unfortunately the package
does not allow for the choice of priors to be wider than what shown in
*Tab.* <a href="#tab:priors" data-reference-type="ref"
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
data-reference="fig:MCMC summary">1.9</a> sums up the ability of the
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
data-reference="fig:residuals vs noise">1.8</a>, its distribution is in
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

<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-numpyro2" class="csl-entry">

Bingham, Eli, Jonathan P. Chen, Martin Jankowiak, Fritz Obermeyer,
Neeraj Pradhan, Theofanis Karaletsos, Rohit Singh, Paul A. Szerlip, Paul
Horsfall, and Noah D. Goodman. 2019. “Pyro: Deep Universal Probabilistic
Programming.” *J. Mach. Learn. Res.* 20: 28:1–6.
<http://jmlr.org/papers/v20/18-403.html>.

</div>

<div id="ref-lognormal" class="csl-entry">

Boruah, Supranta Sarma, Eduardo Rozo, and Pier Fiedorowicz. 2022.
“Map-Based Cosmology Inference with Lognormal Cosmic Shear Maps.”
<https://arxiv.org/abs/2204.13216>.

</div>

<div id="ref-jaxcosmo" class="csl-entry">

Campagne, Jean-Eric, François Lanusse, Joe Zuntz, Alexandre Boucaud,
Santiago Casas, Minas Karamanis, David Kirkby, Denise Lanzieri, Austin
Peel, and Yin Li. 2023. “JAX-COSMO: An End-to-End Differentiable and GPU
Accelerated Cosmology Library.” *The Open Journal of Astrophysics* 6
(April). <https://doi.org/10.21105/astro.2302.05163>.

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

<div id="ref-fwdmodel" class="csl-entry">

Zhou, Alan Junzhe, Xiangchong Li, Scott Dodelson, and Rachel Mandelbaum.
2023. “Accurate Field-Level Weak Lensing Inference for Precision
Cosmology.” <https://arxiv.org/abs/2312.08934>.

</div>

</div>
