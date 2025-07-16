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
data-reference="sec:weak lensing">[sec:weak lensing]</a> as well as
details on the cosmology used in this thesis in *Sec.*
<a href="#subsec:cosmology" data-reference-type="ref"
data-reference="subsec:cosmology">[subsec:cosmology]</a>.

A lot of work goes into translating a measurement of distant galaxies to
its mathematically friendly counterpart $`\Vec{\gamma}`$. This is one of
the reasons why we will not be dealing with it in this thesis, as it is
outside of our scope. Instead we will be simulating our own convergence
fields. We use a *Gaussian random field (GRF)* algorithm for the
creation of Gaussianly distributed data. As well as lognormal
transformations to create fields with a distribution that resembles more
closely that in our universe. These transformations are listed in *Sec.*
<a href="#sec:field generation" data-reference-type="ref"
data-reference="sec:field generation">[sec:field generation]</a>; we
then use them to simulate our data as explained in *Sec.*
<a href="#sec:data simulation" data-reference-type="ref"
data-reference="sec:data simulation">[sec:data simulation]</a>. We also
verify that the generated fields recover the fiducial power spectrum in
*Sec.*
<a href="#sec:gaussian and lognormal fields" data-reference-type="ref"
data-reference="sec:gaussian and lognormal fields">[sec:gaussian and
lognormal fields]</a>.

<div class="wrapfigure">

r0.45

</div>

A *Gaussian process (GP)* usually assumes little prior knowledge about
the data it is applied to. Current research in the field of cosmology
views GPs as a machine learning tool to be trained. It is used to
accelerate and optimise models (Mootoovaloo et al. 2020) (Boruah et al.
2022) (Karchev, Coogan, and Weniger 2022), as well as for its
interpolation qualities applied to the reconstruction of functions
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
data-reference="sec:gaussian process">[sec:gaussian process]</a>,
followed by a detailed account of the computational methods used to
recover a working kernel for GPs in *Sec.*
<a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">[sec:gaussian process
kernel]</a>. In our results we show their ability to create maps that
follow the desired statistic *Sec.*
<a href="#sec:gaussian process priors" data-reference-type="ref"
data-reference="sec:gaussian process priors">[sec:gaussian process
priors]</a> and reconstruct data *Sec.*
<a href="#sec:gaussian process map reconstruction"
data-reference-type="ref"
data-reference="sec:gaussian process map reconstruction">[sec:gaussian
process map reconstruction]</a>. We also present our attempt at
cosmological parameters inference with GPs in *Sec.*
<a href="#sec:inference of cosmological parameters"
data-reference-type="ref"
data-reference="sec:inference of cosmological parameters">[sec:inference
of cosmological parameters]</a>.

It is important to note that throughout the thesis we follow the
extremely useful guidelines set by the pipeline (Zhou et al. 2023) on
how to deal with discrete maps in weak lensing.

<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-cosmology:lensing2" class="csl-entry">

Bartelmann, M., and M. Maturi. 2017. “Weak Gravitational Lensing.”
*Scholarpedia* 12 (1): 32440.
<https://doi.org/10.4249/scholarpedia.32440>.

</div>

<div id="ref-weaklensing" class="csl-entry">

Blandford, R. D., A. B. Saust, T. G. Brainerd, and J. V. Villumsen.
1991. “<span class="nocase">The distortion of distant galaxy images by
large scale structure</span>.” *AIP Conference Proceedings* 222 (1):
455–58. <https://doi.org/10.1063/1.40414>.

</div>

<div id="ref-gp:acceleration2" class="csl-entry">

Boruah, Supranta S, Tim Eifler, Vivian Miranda, and P M Sai Krishanth.
2022. “<span class="nocase">Accelerating cosmological inference with
Gaussian processes and neural networks – an application to LSST Y1 weak
lensing and galaxy clustering</span>.” *Monthly Notices of the Royal
Astronomical Society* 518 (4): 4818–31.
<https://doi.org/10.1093/mnras/stac3417>.

</div>

<div id="ref-cellestim2" class="csl-entry">

Brown, M. L., P. G. Castro, and A. N. Taylor. 2005.
“<span class="nocase">Cosmic microwave background temperature and
polarization pseudo-$`C_\ell`$ estimators and covariances</span>.”
*Monthly Notices of the Royal Astronomical Society* 360 (4): 1262–80.
<https://doi.org/10.1111/j.1365-2966.2005.09111.x>.

</div>

<div id="ref-cellestim" class="csl-entry">

Chon, Gayoung, Anthony Challinor, Simon Prunet, Eric Hivon, and István
Szapudi. 2004. “<span class="nocase">Fast estimation of polarization
power spectra using correlation functions</span>.” *Monthly Notices of
the Royal Astronomical Society* 350 (3): 914–26.
<https://doi.org/10.1111/j.1365-2966.2004.07737.x>.

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

<div id="ref-gp:acceleration" class="csl-entry">

Mootoovaloo, Arrykrishna, Alan F Heavens, Andrew H Jaffe, and Florent
Leclercq. 2020. “<span class="nocase">Parameter inference for weak
lensing using Gaussian Processes and MOPED</span>.” *Monthly Notices of
the Royal Astronomical Society* 497 (2): 2213–26.
<https://doi.org/10.1093/mnras/staa2102>.

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

<div id="ref-fwdmodel" class="csl-entry">

Zhou, Alan Junzhe, Xiangchong Li, Scott Dodelson, and Rachel Mandelbaum.
2023. “Accurate Field-Level Weak Lensing Inference for Precision
Cosmology.” <https://arxiv.org/abs/2312.08934>.

</div>

</div>
