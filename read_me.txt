monte_carlo_base.py will run a generic ising model for a given lattice size, temperature and dynamic
to run: python monte_carlo_base.py <size> <temperature> <glauber/kawasaki>

monte_carlo_glauber.py and monte_carlo_kawasaki.py will run an ising model between T = 1 and 3 for each dynamic respectively and save
observables to .npy files which can then be plotted with plot.py. 
to run: monte_carlo_glauber/kawasaki.py <size>