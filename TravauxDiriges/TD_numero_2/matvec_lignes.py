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

#les index pour chaque processeur
index_min = rank*n_loc
index_max = (rank+1)*n_loc

#la list que chaque processeur auro pour sauveguarder le resultat final
result=[]

# Initialisation de la matrice
#l'index i c'est pour les collones et l'index j c'est pour les lignes
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(index_min,index_max)])
print("Pour le processeur {}, A est: \n".format(rank))
print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print("Pour le processeur {}, u est: \n".format(rank))
print(f"u = {u}")

# Produit matrice-vecteur
v = A.dot(u)
print(f"v = {v}")
print(type(v))

# comme A * u est de dimension (dim x n_lot ) * (n_lot x 1),
#le resultat est un vecter v de dim (dim x 1)
# pour obtenir le resultat il faut qu'on fasse la somme des v's de chaque processeur
# c'est une bonne situation pour utiliser le all gather 
result = comm.allgather(v)
print(np.shape(result))

#maintenant le result a uen dimension (3,40), on doit just 
#faire un 'reshape' de l array
result = np.hstack(result)
print(np.shape(result))

if rank==0:
    print("Le resultat final est: \n",result)