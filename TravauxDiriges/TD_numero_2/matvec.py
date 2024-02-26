# Produit matrice-vecteur v = A.u
import numpy as np

#mes imports
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Dimension du problème (peut-être changé)
dim = 120

#le Nloc de la question
n_loc = dim//size

# Initialisation de la matrice
#l'index i c'est pour les collones et l'index j c'est pour les lignes
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print(f"u = {u}")

# Produit matrice-vecteur
v = A.dot(u)
print(f"v = {v}")
