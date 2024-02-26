from mpi4py import MPI
import numpy as np

comm=MPI.COMM_WORLD
rank = comm.Get_rank()
size= comm.Get_size()

 d=3 #taille du cube
# le cas d=1
if rank == 0:
    valeur = int(input("Le valeur choisi est: "))
    jeton = valeur
    print("La tache maitre a un jeton: ",jeton)
    comm.send(jeton,dest=1, tag=1)

if rank == 1:
    jeton = comm.recv(source = 0, tag = 1)
    print (f'La tache {rank} a le jeton: {jeton}')


#le cas d=2
#la racine envoye à 2 nodes

if rank == 0 :
    valeur = int(input("Le valeur choisi est: "))
    jeton = valeur
    nodes = [2**i for i in range(d)]
    print("La tache maitre a un jeton: ",jeton)
    for i in nodes:
       comm.send(jeton,dest=i,tag=i)#ici il envoye pour toutes les puissances de 2

else:
   comm.recv(jeton)
   print (f'La tache {rank} a le jeton: {jeton}')
   if (rank < size -1):
      
