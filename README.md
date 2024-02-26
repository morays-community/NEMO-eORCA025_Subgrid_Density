# Subgrid Density


## Context and Motivation

Purpose of this experiment is to compute the density variation with the [Stanley & al. (2022)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020MS002185) closure model in an external python script on a 10 years global eORCA025 config.
The computed density is sent back to NEMO without retroaction on the solution. It is then written in a file with NEMO output system (XIOS).

## Experiments Requirements


### Compilation

- Code version : [NEMO_v4.2.1](https://forge.nemo-ocean.eu/nemo/nemo/-/releases/4.2.1) patched with [Morays]([https://github.com/alexis-barge/morays/tree/main) and local `CONFIG/src` sources.

- Compilation Manager : [pyOASIS-extended DCM_v4.2.1](https://github.com/alexis-barge/DCM/releases/tag/v4.2.1)


### Python

- Eophis version : [eophis_v0.9.0-beta](https://github.com/alexis-barge/eophis/tree/v0.9.0-beta)


### Run

- Production Manager : [pyOASIS-extended DCM_v4.2.1](https://github.com/alexis-barge/DCM/releases/tag/v4.2.1)


### Post-Process

- Post-Process libraries : [DMONTOOLS](https://github.com/alexis-barge/DMONTOOLS) (requires [CDFTOOLS](https://github.com/meom-group/CDFTOOLS))
  
- Plotting : custom scripts in `POSTPROCESS`, use `plots.yml`

