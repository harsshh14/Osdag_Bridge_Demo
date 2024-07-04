# # Step 1: Initialize an empty list
# matrix = []

# # Step 2: Define rows (lists) to append to the matrix
# row1 = [1, 2, 3]
# row2 = [4, 5, 6]
# row3 = [7, 8, 9]

# # Step 3: Append rows to the matrix
# matrix.append(row1)
# matrix.append(row2)
# matrix.append(row3)

# # Printing the resulting matrix
# print(matrix[1][1])


import numpy as np

# def create_k_matrix(E,I,girder_space):
#     k_mat=np.zeros((4, 4))
#     k_mat[0][0]=k_mat[2][2]=12/girder_space**3
#     k_mat[0][1]=k_mat[1][0]=k_mat[0][3]=k_mat[3][0]=6/girder_space**2
#     k_mat[0][2]=k_mat[2][0]=-12/girder_space**3
#     k_mat[1][1]=k_mat[3][3]=4/girder_space
#     k_mat[1][2]=k_mat[2][1]=k_mat[2][3]=k_mat[3][2]=-6/girder_space**2
#     k_mat[1][3]=k_mat[3][1]=2/girder_space
#     return k_mat

# def K_matrix(num_supp, I,E, girder_space):
#     #supp is the no of supp(girders). for a three girder bridge, num_supp=3
#     K= np.zeros((num_supp*2,num_supp*2 ))
#     k_1=create_k_matrix(E,I,girder_space)
#     temp=num_supp
#     l=1
#     while temp>1:
#         i=0
#         for x in [num_supp+l,l,num_supp+l+1,l+1]:
#             j=0
#             for y in [num_supp+l,l,num_supp+l+1,l+1]:
#                 K[x-1][y-1]+=k_1[i][j]
#                 j+=1
#             i+=1
#         l+=1
#         temp =temp- 1


#     print(K)        

# K_matrix(3,0,0,2.5)
n=3
print(np.zeros(2*n))


A=[[1.25],[0],[0]]
C=np.array([[1.25, 0, 0]])

# Reshape the array to 3x1
C = C.reshape((3, 1))
print(C)
B=[[1.6,0.8,0],[0.8,3.2,0.8],[0,0.8,1.6]]
B_inv=np.linalg.inv(B)
print(np.matmul(B_inv,A))