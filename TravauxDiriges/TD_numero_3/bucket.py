from mpi4py import MPI   
import numpy as np
from timeit import default_timer as timer#pour calculer le temps de calcul
from math import floor

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()#nbp

n=1000 #taille du vecteur initial

bucket= []
sort_original=None
rec=None
bucket_values=np.empty(size)
sendbuf=[]
result=[]

if rank==0:
    begin = timer()
    sort_original = np.random.rand(n)
    #ici on fait sendbuf une liste de arrays du numpy
    #comme ça, on peut utiliser le scatter normal pour partage
    #les donnees parmi les processeurs
    for i in range(size):
        sendbuf.append(sort_original[floor(i * n/size):floor((i+1)*n/size)])
        #le choix de l'index je l'ai vu dans un livre
        #comme ça, le nombre de valeurs pour chaque tache est bient distribue
rec=comm.scatter(sendbuf,root=0)
rec=np.array(rec)

#on fait une permutation pour prendre les valeurs possibles pour les intervals des buckets
value_for_bucket = rec[np.random.permutation(range(len(rec)))[:size+1]]
value_for_bucket.sort()
#print('For processus {}, the value is: \n'.format(rank),value_for_bucket)

#bucket_values a les valeurs possibles pour chaque bucket
bucket_values=comm.gather(value_for_bucket,root=0)

if rank==0:
    bucket_values=np.hstack(bucket_values)#juste pour fair un array de dimension correcte
    bucket_values=np.sort(bucket_values)
    bucket_values =np.random.choice(bucket_values,size+1,replace=False)#on choisit p+1 valeurs aleatoires
    bucket_values.sort()
    for i in range(np.shape(bucket_values)[0]-1):
        bucket.append(sort_original[(sort_original<bucket_values[i+1])&(sort_original>bucket_values[i])])
#bucket c est une list avec p np.arrays, un pour chaque processeur
#ces sont les valeurs que chaque processeur va trier
bucket = comm.scatter(bucket,root=0)
bucket.sort()
result=comm.gather(bucket,root=0)

if rank==0:
    result=np.hstack(result)
    end = timer()
    print("time elapsed is\n",end-begin)
    #print("the result is\n",result)