from mpi4py import MPI   
import numpy as np
from timeit import default_timer as timer#pour calculer le temps de calcul
from math import floor

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()#nbp

n=10000000 #taille du vecteur initial

initial_index= floor(rank * n/size)
final_index=floor((rank+1)*n/size)

bucket= []
sort_original=None
rec=None
bucket_values=np.empty(size)
sendbuf=[]
result=[]

if rank==0:
    begin = timer()
    sort_original = np.random.rand(n)
    for i in range(size):
        sendbuf.append(sort_original[floor(i * n/size):floor((i+1)*n/size)])
    #on cree un array qui divise [0,1] en npb valeurs, ce qui nous donne nbp-1 buckets
rec=comm.scatter(sendbuf,root=0)
rec=np.array(rec)

value_for_bucket = rec[np.random.permutation(range(len(rec)))[:size+1]]
value_for_bucket.sort()
#print('For processus {}, the value is: \n'.format(rank),value_for_bucket)

bucket_values=comm.gather(value_for_bucket,root=0)

if rank==0:
    bucket_values=np.hstack(bucket_values)
    bucket_values=np.sort(bucket_values)
    bucket_values =np.random.choice(bucket_values,size+1,replace=False)
    bucket_values.sort()
    for i in range(np.shape(bucket_values)[0]-1):
        bucket.append(sort_original[(sort_original<bucket_values[i+1])&(sort_original>bucket_values[i])])

bucket = comm.scatter(bucket,root=0)
bucket.sort()
result=comm.gather(bucket,root=0)

if rank==0:
    result=np.hstack(result)
    end = timer()
    print("time elapsed is\n",end-begin)
    #print("the result is\n",result)