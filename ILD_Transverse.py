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

def load_location_vec(overhang_len, num_supp, girder_space):
    i = 0
    end = overhang_len * 2 + (num_supp - 1) * girder_space +0.25
    load_location=[]    
    while i < end:
        load_location.append(i)
        i += 0.25
    return load_location

def create_P_matrix(load_loc,overhang_len,girder_space,num_supp):
    P=np.zeros(num_supp) #contains the values required for solving matrix
    P_vert_supp=np.zeros(num_supp) #contains the values for the vertical reactions on supports
    if load_loc<overhang_len:
        P[0]=overhang_len-load_loc
        P_vert_supp[0]=1
    elif load_loc>(overhang_len+(num_supp-1)*girder_space):
        P[num_supp-1]=-(load_loc-(overhang_len+(num_supp-1)*girder_space))
        P_vert_supp[num_supp-1]=1
    elif (load_loc-overhang_len)%(girder_space)==0:
        P_vert_supp[int((load_loc-overhang_len)/(girder_space))]=1
    else:
        P_vert_supp[int((load_loc-overhang_len)/(girder_space))]=(overhang_len+(int((load_loc-overhang_len)/(girder_space))+1)*girder_space-load_loc)/girder_space
        P_vert_supp[int((load_loc-overhang_len)/(girder_space))+1]=1-(overhang_len+(int((load_loc-overhang_len)/(girder_space))+1)*girder_space-load_loc)/girder_space
        P[int((load_loc-overhang_len)/(girder_space))]=(load_loc-overhang_len-int((load_loc-overhang_len)/(girder_space))*girder_space)*(overhang_len+int((load_loc-overhang_len)/(girder_space)+1)*girder_space-load_loc)**2/girder_space**2
        P[int((load_loc-overhang_len)/(girder_space))+1]=(overhang_len+int((load_loc-overhang_len)/(girder_space)+1)*girder_space-load_loc)*(load_loc-overhang_len-int((load_loc-overhang_len)/(girder_space))*girder_space)**2/girder_space**2
    # print(P_vert_supp)
    # print(P)    
    return P, P_vert_supp
    # a=(load_loc-overhang_len-int((load_loc-overhang_len)/(girder_space))*girder_space)
    # b=(overhang_len+int((load_loc-overhang_len)/(girder_space)+1)*girder_space-load_loc)
    # print("")

# create_P_matrix(7.5,1.25,2.5,3)

def ILD_Transverse_three_girder(space_vectorization,overhang_len,girder_space, height_slab,fck,num_supp):
    #height of slab is needed to calculate I(Moment of inertia)
    #Grade of concrete is needed to calculate E
    #num_supp is the number of supports(girders)
    width=(num_supp-1)*girder_space+2*overhang_len
    b=1000 #mm (length of 1 m section of road is considered )
    E=5000*math.sqrt(fck)  #MPa
    I=b*height_slab**3/12 #mm4

    #a code for K matrix has been created in the trial.py file. check it
    K= K_matrix(num_supp,I,E,girder_space)    
    K_11=np.zeros((num_supp,num_supp)) #the upper matrix of K, which is used in load_loc calculation
    for i in range(num_supp):
        for j in range(num_supp):
            K_11[i][j]=K[i][j]
    K_21=np.zeros((num_supp,num_supp))
    for i in range(num_supp):
        for j in range(num_supp):
            K_21[i][j]=K[num_supp+i][j]
    # print(K_21)
    K_11_inv=np.linalg.inv(K_11)
    ILD_array=[]
    for load_loc in load_location_vec(overhang_len,num_supp,girder_space):
    #load_loc is the location of load on the beam
        # print(load_loc)
        P,P_vert_supp=create_P_matrix(load_loc,overhang_len,girder_space,num_supp)
        P=P.reshape((num_supp,1))
        P_unknown=np.zeros((num_supp,1))
        P_vert_supp=P_vert_supp.reshape((num_supp,1))
        disp_vector=np.matmul(K_11_inv,P)
        P_unknown=(np.matmul(K_21,disp_vector)+P_vert_supp)
        ILD_array.append(P_unknown)
        ILD_array_rounded= np.round(ILD_array, 3)

    print(ILD_array_rounded)



ILD_Transverse_three_girder(0,1.25,3,250,50,3)
# ILD_Transverse_three_girder(0,1.25,2.5,)
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