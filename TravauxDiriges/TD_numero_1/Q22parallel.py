# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 20:55:28 2024

@author: Eduardo
"""
from timeit import default_timer as timer
import numpy as np #easy random number generator
import matplotlib.pyplot as plt
from mpi4py import MPI

comm=MPI.COMM_WORLD
rank=comm.Get_rank()#again, size is the number of cores we'll be using
size=comm.Get_size()




n=1000000 #amount of points to generate


block = n//(size-1) #we'll use this in the loop, to cut it into different parts
#we are basically dividing ur initial data in size - 1 blocks, each will execute the loop and send the results 
#back to rank 0, our 'master' in this loop

#numpy already does this in a super efficient way


counter = 0 #where we'll save the results


#we send the points to the many threads


begin = timer()
if (rank == 0 ):
    points_rec_in=np.empty(size)
    #he's the master, so we make him create de array and share it
    all_points = np.random.uniform(-1,1,(n,2))
    for i in range(1,size):#he'll comunicate with the others
        comm.Send(all_points[(i-1)*block:i*block], dest = i, tag = i)

else:
    counter_p=0
    process_points = np.empty((block,2))
    comm.Recv(process_points,source = 0, tag = rank)
    for i in range(len(process_points)):
        if (np.linalg.norm((process_points[i][1],process_points[i][0]))<1):
            counter_p+=1
            
        else:
            counter_p+=0
    comm.send(counter_p,dest= 0, tag=rank)  
end=timer()
if rank==0:
    for i in range(1,size):
        counter+=comm.recv(source = i, tag = i)
    fig, axs = plt.subplots(1,1,layout='constrained')
    axs.set_title('Monte Carlo Pi')
    axs.set_aspect('equal')
    axs.add_patch(plt.Circle((0,0),1,color='b'))
    axs.set_xticks([-1,0,1])
    axs.set_yticks([-1,0,1])
    for i in range(1,size):
        axs.scatter(all_points.transpose()[0][(i-1)*block:i*block],all_points.transpose()[1][(i-1)*block:i*block], label='task' + str(i))

    plt.legend()
    print(f'The value we found is: {4*(counter/n):.4}')
    print(f'The elapsed time is {(end-begin)}')
    plt.show()

