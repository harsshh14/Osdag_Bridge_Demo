import numpy as np
import math


def ILD_Transverse_two_girders(width,space_vectorization,overhang_len,girder_space):
    #loc_A=overhang length, loc_B= overhang length + spacing between girder
#function to find the support reactions
#width= width of bridge, space_vectorization = space of load during vectorization
    #num_points=(width/space_vectorization)+1
    rxn_A=[None]*(math.ceil(width/space_vectorization)+1)
    rxn_B=[None]*(math.ceil(width/space_vectorization)+1)

    for x in range(len(rxn_A)):
        rxn_B[x]=(x*space_vectorization-overhang_len)/girder_space
        rxn_A[x]=1-rxn_B[x]    
    


#ILD_Transverse_two_girders(5,0.25,1.25,2.5)
################################################################


#function to vectorize the loads on the deck slab
##CONVERT ALL THE LOAD IN A SINGLE ARRAY SO THAT THIS FUNCTION IS RUN ONLY ONE TIME FOR DEAD LOADS
def vectorize_load(width, space_vectorization,load,x_min, x_max):
    #load= is the load in KN/m2, x_min and x_max are the end points of the applied loads
    load_vec=[]
    temp_load_vec=[0]*(math.ceil(width/space_vectorization)+1)
    for x in range(round(x_min/space_vectorization),round(x_max/space_vectorization)+1):
        if (x==(round(x_max/space_vectorization)) or x==(round(x_min/space_vectorization)) ):
            temp_load_vec[x]=load*space_vectorization/2
        else:
            temp_load_vec[x]=load*space_vectorization
    load_vec.append(temp_load_vec)
    print(load_vec)
vectorize_load(10,0.25,16,9.5,10)