# Subgrid Density


## Context and Motivation

Purpose of this experiment is to compute the density variation with the [Stanley & al. (2022)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020MS002185) closure model in an external python script on a 10 years global eORCA025 config.
The computed density is sent back to NEMO without retroaction on the solution. It is then written in a file with NEMO output system (XIOS).

## Experiments Requirements


### Compilation

- NEMO version : [v4.2.1](https://forge.nemo-ocean.eu/nemo/nemo/-/releases/4.2.1) patched with [morays](https://github.com/morays-community/morays-doc/tree/main/nemo_src) and local `CONFIG/src` sources.

- Compilation Manager : pyOASIS-extended [DCM_v4.2.1](https://github.com/alexis-barge/DCM/releases/tag/v4.2.1)


### Python

- Eophis version : [v0.9.0-beta](https://github.com/alexis-barge/eophis/tree/v0.9.0-beta)


### Run

- Production Manager : pyOASIS-extended [DCM_v4.2.1](https://github.com/alexis-barge/DCM/releases/tag/v4.2.1)


### Post-Process

- Post-Process libraries : [DMONTOOLS](https://github.com/alexis-barge/DMONTOOLS) (requires [CDFTOOLS](https://github.com/meom-group/CDFTOOLS))
  
- Plotting : custom scripts in `POSTPROCESS` with `plots.yml`

