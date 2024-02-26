from mpi4py import MPI
import numpy as np

comm=MPI.COMM_WORLD
rank = comm.Get_rank()
size= comm.Get_size()



if rank == 0:
    valeur = int(input("Le valeur choisi est: "))
    jeton = valeur
    print("La tache maitre a un jeton: ",jeton)
    comm.send(jeton,dest=1, tag=1)

if rank == 1:
    jeton = comm.recv(source = 0, tag = 1)
    print (f'La tache {rank} a le jeton: {jeton}')