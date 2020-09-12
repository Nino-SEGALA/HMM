#File containing everything needed to work on matrix
import sys

def mult(M, N):  # calculate M*N
    p, q = len(M), len(M[0])
    r, s = len(N), len(N[0])
    R = [[0 for x in range(s)] for y in range(p)]
    if q == r:
        for i in range(p):
            for j in range(s):
                for k in range(q):
                    R[i][j] += M[i][k] * N[k][j]
                    #print(M[i][k]," ",N[k][j])
    return R

def transpose(M): #calculate the transposed of M
    res = [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    return res

def column(M, j):  # return the column j of M
    i = len(M)
    Mj = [[0] for k in range(i)]
    for k in range(i):
        Mj[k][0] = M[k][j]
    return Mj

def mult_block_by_block(u, v):
    #calculate a new vector where each block is equal to the multiplication of
    # the same block in u and the same block in v
    p = len(u)
    w = [[0] for j in range(p)]
    for j in range(p):
        w[j][0] = u[j][0]*v[j][0]
    return w


def make_matrix(lst):
    #return the matrix corresponding to lst, where the first 2 elements of lst are the size of M
    #and what follow are the rows of the matrix
    lst = [float(i) for i in lst]
    n = int(lst[0]) #M matrix n_rows * p_columns (n states; p emissions)
    p = int(lst[1])
    M = [[0 for j in range(p)] for i in range(n)]
    for i in range(n):
        for j in range(p):
            M[i][j] = lst[2 + p*i + j]
    return M

def make_vector(lst):

    # return the vector corresponding to lst, where the first element of lst is the length of M

    # and what follow are the rows of the vector

    lst = [int(i) for i in lst]

    p = int(lst[0]) #M matrix p_columns (p emissions)

    M = [0 for j in range(p)]

    for j in range(p):

        M[j] = lst[1 + j]

    return M

#---------------------------------------------
#Bennis Part


def input_hmm1():
    #return A, B, q and O
    res = [] #[A, B, q, O]
    i = 0
    for line in sys.stdin:
        lst = line.split()
        if i < 3:
            res.append(make_matrix(lst))
        else: #the last line in the sequence of emissions vector
            res.append(make_vector(lst))
        i += 1
    return res

def print_matrix(mat):
    for ele in mat:
        print(ele)
    print()



#what exactley do they mean by intializing?
def initialize():
    res = input_hmm1()
    
    A = res[0] #Transision matrix
    B = res[1] #Emission matrix
    pi = res[2] #initial state probability
    E = res[3] #emission itself
    
    return A,B,pi,E


#Plan: mach erstmal den forward pass(ohne scaling) und dann vergleiche es mit der Lösung
def alpha(A,B,pi,E):
    #Compute a0(i) alpha ist immer ein vektor der länge N 
    c0 = 0
    bi0zero = column(B, E[0])
    
    #compute alpha0  
    alpha0 = [transpose(pi)[i][0] * bi0zero[i][0] for i in range(len(A))]
    print(pi)
    print(transpose(pi))
    print(bi0zero)
    c0  = sum(alpha0)
    
    #scale alpha0
    c0 = 1/c0
    alpha0 = [c0*alpha0[i] for i in range(len(A))]

    #compute alphaT(i)
    alphaTminusOne = alpha0
    for t in range(1,len(E)):
        alphaT = []
        for i in range(len(A)):
            alphaI = 0
            for j in range(len(A)):
                alphaI = alphaI + alphaTminusOne[j]*A[j][i]
                print(alphaTminusOne[j],A[j][i])
                print(alphaI)

            alphaT.append(alphaI)
            alphaT[i] = alphaT[i] *  column(B, E[t])[i][0]
            print(alphaT[i])
            print("COLUMN",column(B, E[t])[i])
##        scale alpha t
        if sum(alphaT) != 0:
            c0  = 1/sum(alphaT)
        else:
            c0 = 0
        alphaT = [c0*alphaT[i] for i in range(len(A))]
        print("ALPHA TIER ",alphaT)
        alphaTminusOne = alphaT

    return sum(alphaT)




def beta(A,B,pi,E):

    #I dont get the scaling part here
    for i in range(len(E)):
        betaT-1 = alpha(A,B,pi,E)
        
        

        
    
    for t in reversed(range(len(E)-1)):
        for i in range(len(A)-1):
            betaT = []
            for j in range(len(A)):
                betaTI = 0# betaTI
                for j in range(len(A)):
                    betaTi = betaTi + A[i,j]*column(B, E[0])[t+1][0]*1###WHAT HAPPENS HERE
                

    


def compute(A,B,pi,E):
    #print(alpha(A,B,pi,E))
    print(beta(A,B,pi,E))
    
    return 0,0,0,0



def hmm3(maxIters):
    iters = 0
    oldLogProb = -1000
    #goal: Recalculate transission matrix until convergence
    A,B,pi,E = initialize() #Step 1
    alpha, beta, gammaIJ, gammaI = compute(A,B,pi,E) #step 2
    #step 3
    #step 4
    

    

    

hmm3(1000)
