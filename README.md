# Weak lensing map inference: a physics-informed Gaussian process approach

**Master Thesis**  
Nicolò Massari  
ETH Zurich, April 2024

## Abstract

This thesis introduces Gaussian processes (GPs) as a novel tool for weak gravitational lensing map inference in cosmology. We develop a physics-informed approach that incorporates knowledge of 2-point statistics directly into the GP kernel, enabling accurate reconstruction of masked convergence fields and inference of cosmological parameters.

## Key Results

- Successfully applied GPs to reconstruct heavily masked (10%) convergence maps
- Recovered cosmological parameters within 2σ: σ₈ = 0.776±0.015 and Ωₘ = 0.284±0.010
- Demonstrated the half-range FFT method as optimal for GP kernel construction
- Achieved χ²/ν = 1.06 for noiseless field reconstruction

## Repository Structure

- [`github_md/thesis.md`](github_md/thesis.md) - (Attempted) Full thesis content in GitHub-compatible Markdown

## Quick Links

- [Read the full thesis](thesis.pdf)

## Citation

```bibtex
@mastersthesis{massari2024weak,
  title={Weak lensing map inference: a physics-informed Gaussian process approach},
  author={Massari, Nicolò},
  year={2024},
  school={ETH Zurich}
}
```