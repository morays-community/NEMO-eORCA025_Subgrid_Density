# NEMO-Subgrid_Density.STD 
# ------------------------
# Commands used to make the plots in ./RES
#
default: means snapshots

means: means_1d means_5d

means_1d:
	python3 ./plot_means.py -f 1d -y 1959-1969

means_5d:
	python3 ./plot_means.py -f 5d -y 1959-1969

snapshots:
	python3 ./plot_snpsht.py -f 1d -y 1964 -m 5 -d 2


