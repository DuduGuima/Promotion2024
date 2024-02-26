# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:27:14 2024

@author: Eduardo
"""
from timeit import default_timer as timer
import numpy as np #easy random number generator
import matplotlib.pyplot as plt


n=1000000 #amount of points to generate
t = 4 #number of threads we want to work simultaneously

block = n//t #we'll use this in the loop, to cut it into different parts

points=np.random.uniform(-1,1,(2,n))#I left this here because 
#numpy already does this in a super efficient way


points_out=[[],[]]
points_in=[[],[]]


begin = timer()
for i in range(n):
    if (np.linalg.norm((points[0][i],points[1][i]))<1):
        points_in[0].append(points[0][i])
        points_in[1].append(points[1][i])
    else:
        points_out[0].append(points[0][i])
        points_out[1].append(points[1][i])
       
end = timer()
        
fig, axs = plt.subplots(1,1,layout='constrained')
axs.set_title('Monte Carlo Pi')
axs.set_aspect('equal')
axs.add_patch(plt.Circle((0,0),1,color='b'))
axs.set_xticks([-1,0,1])
axs.set_yticks([-1,0,1])
axs.scatter(points_in[:][0],points_in[:][1],color='red',linewidths=0.5)     
axs.scatter(points_out[:][0],points_out[:][1],color= 'green',linewidths=0.5)
print('Number of points we used: ',n)
print(f'The value we found is: {4*(len(points_in[0])/n):.4}') 
print(f'The elapsed time is {(end-begin)}')
plt.show()
