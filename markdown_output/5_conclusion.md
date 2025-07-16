# Conclusion

We have hereby introduced the tool of Gaussian processes to the
landscape of map inference of cosmological fields, in particular weak
lensing convergence. We considered how the 2-point statistics of
cosmological fields changes when we are dealing with bounded and
discrete maps in *Sec.*
<a href="#sec:weak lensing" data-reference-type="ref"
data-reference="sec:weak lensing">[sec:weak lensing]</a>. We discussed
the realisation of Gaussian and lognormal fields in *Sec.*
<a href="#sec:field generation" data-reference-type="ref"
data-reference="sec:field generation">[sec:field generation]</a>, and
showed their ability to recover the 2-point statistics that they encode,
in *Sec.*
<a href="#sec:gaussian and lognormal fields" data-reference-type="ref"
data-reference="sec:gaussian and lognormal fields">[sec:gaussian and
lognormal fields]</a>. We have included masking and noise to the data to
simulate realistic maps in *Sec.*
<a href="#sec:data simulation" data-reference-type="ref"
data-reference="sec:data simulation">[sec:data simulation]</a>. We have
shown that it is possible to apply physical knowledge about the 2-point
correlation function of a cosmological field in order to set up a
Gaussian process able to produce a Gaussian realisation of such a field.
We considered different set ups for the Gaussian process kernel in
*Sec.* <a href="#sec:gaussian process kernel" data-reference-type="ref"
data-reference="sec:gaussian process kernel">[sec:gaussian process
kernel]</a> and showed how they fare against one another in *Sec.*
<a href="#sec:gaussian process priors" data-reference-type="ref"
data-reference="sec:gaussian process priors">[sec:gaussian process
priors]</a>, ultimately proving empirically that the half-range FFT
model is the best. In *Sec.*
<a href="#sec:gaussian process map reconstruction"
data-reference-type="ref"
data-reference="sec:gaussian process map reconstruction">[sec:gaussian
process map reconstruction]</a> we present an application of Gaussian
processes to a noiseless masked convergence map, in order to showcase
its ability to reconstruct a heavily masked map. Finally we present our
results for the cosmological parameters inference with GPs, conditioning
on noisy and masked data. When running the inference model on one
cosmological parameter we recover both parameters within two sigmas,
$`\sigma_8 = 0.776\pm0.015`$ and $`\Omega_m = 0.284\pm0.010`$. For the
two parameter inference we observe the well known banana-shaped
degeneracy between $`\sigma_8`$ and $`\Omega_m`$, as well as recovering
$`0.762\pm0.028`$ within two sigmas.

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
memorable. Thanks to Guido van Rossum for giving us . Thank you Mia, for
your unconditional support, *you* keep me grounded. Non sarei qua senza
di te mamma, grazie.
