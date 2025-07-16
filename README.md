# Weak Lensing Map Inference: A Physics-Informed Gaussian Processes Approach

This repository contains the master's thesis on applying Gaussian processes to weak lensing convergence field inference, combining physics-informed priors with Bayesian parameter estimation.

## Abstract

This thesis introduces Gaussian processes (GPs) to the landscape of map inference for cosmological fields, specifically weak lensing convergence. Unlike traditional GP applications that assume minimal prior knowledge, we apply physical knowledge about 2-point statistics in cosmology to create fully informed GPs. Our approach uses the convergence angular autocorrelation function as the GP kernel, enabling both field reconstruction and cosmological parameter inference.

Key contributions:
- Physics-informed GP kernels based on cosmological 2-point statistics
- Map-based inference method that uses all available data points
- Masked field reconstruction with uncertainty quantification
- Bayesian inference of cosmological parameters (Ωₘ, σ₈, S₈)

## Repository Structure

```
├── markdown_output/           # Converted thesis chapters
│   ├── thesis_complete.md    # Complete thesis in one file
│   ├── 0_abstract.md        # Abstract
│   ├── 1_introduction.md     # Introduction
│   ├── 2_theoretical_framework.md
│   ├── 3_methods.md
│   ├── 4_results.md
│   ├── 5_conclusion.md
│   ├── 8_appendix.md
│   └── 9_miscellaneous.md
├── images/                   # Figures and plots
├── setup/                    # LaTeX setup files
├── refs.bib                  # Bibliography
├── thesis.tex               # Main LaTeX file
└── [chapter].tex            # Individual LaTeX chapters
```

## Key Results

### Field Reconstruction
- Successfully reconstructed heavily masked (10%) convergence fields
- Provided uncertainty estimates for masked regions
- Achieved χ²/ν ≈ 1.06 for noiseless reconstruction

### Parameter Inference
- **Single parameter**: Recovered σ₈ = 0.776±0.015 and Ωₘ = 0.284±0.010 within 2σ
- **Two parameters**: Recovered S₈ = 0.762±0.028 within 2σ
- Observed expected banana-shaped degeneracy between σ₈ and Ωₘ

### Methodological Advances
- Developed half-range FFT kernel method for optimal power spectrum recovery
- Created preprocessing pipeline for multi-file LaTeX thesis structure
- Implemented MCMC sampling with JAX/NumPyro for efficient inference

## Technical Implementation

### Dependencies
- **Cosmology**: jaxcosmo (power spectrum computation)
- **Gaussian Processes**: tinygp (JAX-based GP library)
- **MCMC**: NumPyro (Bayesian inference)
- **Computation**: JAX (autodifferentiation and GPU acceleration)

### Key Algorithms
1. **Gaussian Random Field Generation**: Rayleigh distribution with complex exponentials
2. **Kernel Construction**: Half-range FFT transformation of angular power spectrum
3. **Field Reconstruction**: GP conditioning on masked, noisy data
4. **Parameter Inference**: NUTS sampling of posterior distributions

## Usage

### Reading the Thesis
The complete thesis is available in markdown format:
- [Complete thesis](markdown_output/thesis_complete.md) - Single file version
- Individual chapters in `markdown_output/` directory

### Mathematical Notation
- Inline math: `$\kappa$` for convergence field
- Display equations: Fenced code blocks with `math` language
- Figures: Embedded PDF files with captions

## Key Equations

**Convergence Field Definition:**
```math
\kappa(\theta) = \int_0^{\chi*}d\chi W(\chi)\delta_m(\chi \theta, \chi)
```

**Flat-sky Correlation Function:**
```math
w(\theta) = \int \frac{dl}{2\pi} l C(l) J_0(l\theta)
```

**GP Conditioning:**
```math
\bm{f}_* \mid D_*, D, \bm{y} \sim \mathcal{N}\left( \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{y} , \bm{K}_{**} - \bm{K}^T_* [\bm{K} + \sigma_n^2 I]^{-1} \bm{K}_* \right)
```

## Figures

Key visualizations include:
- Gaussian vs lognormal field comparisons
- Power spectrum recovery validation
- GP reconstruction examples
- MCMC parameter constraints
- Posterior distribution contours

## Future Work

- **Scalability**: Implement GP approximations for larger grids (>64×64)
- **Lognormal Fields**: Develop modified likelihoods for non-Gaussian data
- **Real Data**: Apply to current weak lensing surveys (HSC, KiDS)
- **Full Sky**: Extend to full-sky cosmological analyses

## Citation

If you use this work, please cite:
```
@mastersthesis{massari2024weaklensing,
  title={Weak Lensing Map Inference: A Physics-Informed Gaussian Processes Approach},
  author={Massari, Nicola},
  year={2024},
  school={ETH Zurich},
  type={Master's Thesis}
}
```

## Acknowledgments

This project was supervised by Dr. Tilman Tröster and conducted within the Cosmology group at ETH Zurich, led by Prof. Alexandre Réfrégier. The work follows methodologies established by leading weak lensing surveys including HSC and KiDS.

## License

This thesis is made available for academic and research purposes. Please respect appropriate citation practices when using this work.