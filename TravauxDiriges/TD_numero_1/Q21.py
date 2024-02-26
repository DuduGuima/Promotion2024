# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 01:56:04 2024

@author: Eduardo
"""

#on commence par importer la librairie

from mpi4py import MPI

comm=MPI.COMM_WORLD
size= comm.Get_size() # nbp = size
rank = comm.Get_rank()#on découvre le processus

#on unilise les recv pour blocker le processus:
if (rank == 0):
    jeton = 1
    comm.send(jeton, dest =1 ,tag=10)
    jeton = comm.recv(source = size-1 , tag = 10)
    print('Le jeton est: ',jeton)
elif ((rank > 0 ) and (rank < size -1)):
    jeton = comm.recv(source=rank-1,tag =10)
    jeton +=1
    comm.send(jeton, dest = rank+1, tag= 10)

elif (rank == size -1 ):
    jeton = comm.recv(source=rank-1, tag=10)
    comm.send(jeton,dest=0,tag=10)


