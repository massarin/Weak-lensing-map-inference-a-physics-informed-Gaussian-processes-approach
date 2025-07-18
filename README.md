# Weak lensing map inference: a physics-informed Gaussian process approach

**Master Thesis**  
Nicolò Massari  
ETH Zurich, April 2024

## Abstract

In this work we propose the use of physically informed Gaussian processes (GP) to analyse cosmological fields at the map level. We will show that GPs can capture the statistical behaviour of cosmological fields, providing us with a likelihood as a function of the cosmological parameters conditioned to the map. In practice, we set the Gaussian process kernel to be the 2-point autocorrelation function associated to a 2D discrete flat-sky convergence map. We find that a GP in this setup is not only able to generate maps with the wanted 2-point statistics, but also to reconstruct masked data with an associated uncertainty. Additionally, we perform a Bayesian inference analysis in order to test the ability of Gaussian processes to recover cosmological parameters. We find that we are able to consistently recover the σ8 and Ωm degeneracy, recovering S8 within two sigma uncertainty. The data is simulated by a Gaussian random field realisation of a convergence map of size $(10^◦, 10^◦)$, $64×64$ grid, mask $∼10\%$ and noise given by a galaxy density of $n_g = 10 galaxies/arcmin^2$.

- [Read the full thesis](thesis.pdf)
- [Read the full thesis in markdown](github_md/thesis.md) (Beta version)