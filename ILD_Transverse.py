import numpy as np
import math


def ILD_Transverse_two_girders(width,space_vectorization,overhang_len,girder_space):
    #loc_A=overhang length, loc_B= overhang length + spacing between girder
#function to find the support reactions
#width= width of bridge, space_vectorization = space of load during vectorization
    #num_points=(width/space_vectorization)+1
    rxn_A=np.empty(math.ceil(width/space_vectorization)+1)
    rxn_B=np.empty(math.ceil(width/space_vectorization)+1)

    for x in range(len(rxn_A)):
        rxn_B[x]=(x*space_vectorization-overhang_len)/girder_space
        rxn_A[x]=1-rxn_B[x]    

# ILD_Transverse_two_girders(5,0.25,1.25,2.5)

def create_k_matrix(E,I,girder_space):
    k_mat=np.zeros((4, 4))
    k_mat[0][0]=k_mat[2][2]=12/girder_space**3
    k_mat[0][1]=k_mat[1][0]=k_mat[0][3]=k_mat[3][0]=6/girder_space**2
    k_mat[0][2]=k_mat[2][0]=-12/girder_space**3
    k_mat[1][1]=k_mat[3][3]=4/girder_space
    k_mat[1][2]=k_mat[2][1]=k_mat[2][3]=k_mat[3][2]=-6/girder_space**2
    k_mat[1][3]=k_mat[3][1]=2/girder_space
    return k_mat

def K_matrix(num_supp, I,E, girder_space):
    #supp is the no of supp(girders). for a three girder bridge, num_supp=3
    K= np.zeros((num_supp*2,num_supp*2 ))
    k_1=create_k_matrix(E,I,girder_space)
    temp=num_supp
    l=1
    while temp>1:
        i=0
        for x in [num_supp+l,l,num_supp+l+1,l+1]:
            j=0
            for y in [num_supp+l,l,num_supp+l+1,l+1]:
                K[x-1][y-1]+=k_1[i][j]
                j+=1
            i+=1
        l+=1
        temp =temp- 1
    return K

def ILD_Transverse_three_girder(width,space_vectorization,overhang_len,girder_space, height_slab,fck,num_supp):
    #height of slab is needed to calculate I(Moment of inertia)
    #Grade of concrete is needed to calculate E
    #num_supp is the number of supports(girders)
    b=1000 #mm (length of 1 m section of road is considered )
    E=5000*math.sqrt(fck)  #MPa
    I=b*height_slab**3/12 #mm4

    #a code for K matrix has been created in the trial.py file. check it
    K= K_matrix(num_supp,I,E,girder_space)
    print(K)

ILD_Transverse_three_girder(0,0,0,2.5,0,0,3)
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
# vectorize_load(10,0.25,16,9.5,10)