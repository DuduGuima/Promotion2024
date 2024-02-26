from mpi4py import MPI   
import numpy as np
from timeit import default_timer as timer#pour calculer le temps de calcul

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()#nbp

n=100 #taille du vecteur initial
number_blocks=n//size

bucket= []
sort_original=None
rec=np.zeros(number_blocks)
begin = timer()
bucket_values=np.empty(size)
if rank==0:
    count=np.zeros(size,dtype=int)
    sort_original = np.random.rand(size,number_blocks)
    #on cree un array qui divise [0,1] en npb valeurs, ce qui nous donne nbp-1 buckets
    #(le processus 0 est le maitre)
    # buckets_values= np.linspace(0,1,size)
    # for i in range(len(buckets_values)-1):
    #     bucket=sort_original[(sort_original < buckets_values[i+1])&(sort_original > buckets_values[i])]
    #     count[i+1] = len(bucket)
    #     # print('valores de bucket \n',bucket)
    #     # print('valor de count',count[i+1])
    #     comm.Send(bucket, dest=i+1, tag= i+1)
    # displ = [sum(count[:p]) for p in range(size)]
    # displ = np.array(displ)
# else:
#     count=np.zeros(size,dtype=int)
#     displ=None
comm.Scatter(sort_original,rec,root=0)

rec=np.sort(rec)

value_for_bucket = rec[np.random.randint(len(rec),size=size+1)]
#print('For processus {}, the value is: \n'.format(rank),value_for_bucket)
bucket_values=comm.gather(value_for_bucket,root=0)




if rank==0:
    bucket_values=np.hstack(bucket_values)
    bucket_values=np.sort(bucket_values)
    #print('bucket values: \n',bucket_values)
#     sort_original=np.hstack(sort_original)
    for i in range(np.shape(bucket_values)[0]-1):
        bucket.append(sort_original[(sort_original<bucket_values[i+1])&(sort_original>bucket_values[i])])
    print('Processo 0 tem: \n',bucket)

rec_sort = np.zeros(size)
comm.Scatter(bucket,rec_sort,root=0)
print('For processus {}, the value is: \n'.format(rank),bucket)

# comm.Bcast(count,root=0)

# bucket_rec=np.zeros(count[rank])

# if rank!=0:

#     comm.Recv(bucket_rec,source=0,tag=rank)
#     bucket_rec=np.sort(bucket_rec)

# result = np.zeros(sum(count))

# comm.Gatherv(bucket_rec,[result,count,displ,MPI.DOUBLE],root=0)
# end = timer()
# if rank == 0:
#     print("la durée d'exécution: \n", end-begin)
#     #print('resultat: \n', result)
