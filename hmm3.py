#File containing everything needed to work on matrix
import sys
import math

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



def calc(A,B,pi,E): #let us start here

##    print("--------------------------------------------------------")
##    print("ALPHA")
    
    cTs = []
    alpha_Ts = []
    #Compute a0(i) alpha ist immer ein vektor der länge N 
    c0 = 0
    bi0zero = column(B, E[0])
    
    #compute alpha0  
    alpha0 = [transpose(pi)[i][0] * bi0zero[i][0] for i in range(len(A))]
    for i in range(len(A)):
        aOI = transpose(pi)[i][0] * bi0zero[i][0]
        c0 = c0 + aOI
    
    #scale alpha0
    c0 = 1/c0
    for i in range(len(A)):#<---- len(A) == N
        alpha0[i] = alpha0[i]*c0
    cTs.append(c0)

    

    #compute alphaT(i)
    alphaTminusOne = alpha0
    alpha_Ts.append(alphaTminusOne)
    for t in range(1,len(E)):
        alphaT = []
        c0 = 0
        for i in range(len(A)):
            alphaI = 0
            for j in range(len(A)):
                alphaI = alphaI + alphaTminusOne[j]*A[j][i]

            alphaT.append(alphaI)
            alphaT[i] = alphaT[i] *  column(B, E[t])[i][0]  
        ##scale alpha t
        if sum(alphaT) != 0: #if division zero.. make sure you don't divide with zero
            c0  = 1/sum(alphaT)
        else:
            c0 = 0
        cTs.append(c0) #<--
        for i in range(len(A)):
            alphaT[i] = c0*alphaT[i]
        alphaTminusOne = alphaT
        alpha_Ts.append(alphaTminusOne)

##    print("ALPHA RESULTS")
##    for line in alpha_Ts:
##        print(line)
##        print(sum(line))
##
##
##    print("--------------------------------------------------------\nBETA")


    #Scale and Initialize
    betaTminus1 = []
    betaTs = [ -100 for j in range(len(E))  ]
    cTminus1 = cTs[-1]
    for i in range(len(E)):
        betaTminus1.append(cTminus1)
    betaTs[-1] = betaTminus1
    

    #Beta pass
    for t in reversed(range(len(E)-1)):
        betaT = []
        for i in range(len(A)):
            betaTi = 0
            for j in range(len(A)):
                betaTi = betaTi + A[i][j] * column(B, E[t+1])[j][0] * betaTs[t+1][j]#betaTminus1 stimmt nicht
            betaTi = betaTi * cTs[t]
            betaT.append(betaTi)
        betaTs[t] = betaT



##    print("BETA RESULTS")
##    for line in betaTs:
##        print(line)



##    print("--------------------------------------------------------\nGAMMA")
    gammaTIJ_list = [[ [ -100 for j in range(len(A)) ] for i in range(len(A)) ] for t in range(len(E)-1) ] #T Matrix auch noch!
    gammaTI_list = []
    for t in range(len(E)-1):
        gammaI = []
        for i in range(len(A)):
            gammaTI = 0
            for j in range(len(A)):
                gammaTIJ = alpha_Ts[t][i] * A[i][j] * column(B, E[t+1])[j][0] * betaTs[t+1][j] #Unclear issue 
                gammaTI = gammaTI + gammaTIJ
                gammaTIJ_list[t][i][j] = gammaTIJ
            gammaI.append(gammaTI)
        gammaTI_list.append(gammaI)


    gammaI = []    
    for i in range(len(A)):
        gammaI.append(alpha_Ts[len(E)-1][i])
    gammaTI_list.append(gammaI)
    

##    print("GAMMA RESULTS\nGAMMA TI")
##    for line in gammaTI_list:
##        print(line)
##    print("GAMMA TIJ")
##    for line in gammaTIJ_list:
##        print(line)
        
   

##    print("--------------------------------------------------------\nRE-ESTIMATION")

    #re-estimate pi
    for i in range(len(A)):
        pi[0][i] = gammaTI_list[0][i]
        
    #re-estimate A
    for i in range(len(A)):
        denom = 0
        for t in range(len(E)-1):
            denom = denom + gammaTI_list[t][i]
        for j in range(len(A)):
            numer = 0
            for t in range(len(E)-1):
                numer = numer + gammaTIJ_list[t][i][j]
            if denom != 0:
                A[i][j] = numer/denom
            else:
                A[i][j] = 0

    #re-estimate B
    for i in range(len(A)):
        denom = 0
        for t in range(len(E)):
            denom = denom + gammaTI_list[t][i]
        for j in range(len(B[0])):
            numer = 0
            for t in range(len(E)):
                if E[t] == j:
                    numer = numer + gammaTI_list[t][i]
            if denom != 0:
                B[i][j] = numer/denom
            else:
                B[i][j] = 0



##    print("GAMMA I RESULTS")
##    for line in gammaTI_list:
##        print(line)
##    print("GAMMA IJ RESULTS")
##    for line in gammaTIJ_list:
##        print(line)
                

    

    logProb = 0
    for i in range(len(E)):
        logProb = logProb + math.log(cTs[i])
    logProb = -logProb
        

    return A,B,pi,E,logProb
    


def return_format(mat):
    res = str(len(mat)) + " " +str(len(mat[0]))
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            res = res +" " + str(mat[i][j])
    return res


def hmm3(maxIters):
    iters = 0#max Iters already defined
    logProb = 0
    oldLogProb = float('-inf') 

    
    A,B,pi,E = initialize()
    A,B,pi,E,logProb = calc(A,B,pi,E) 

    
    
    while(iters < maxIters and logProb > oldLogProb):
        iters = iters +1
        oldLogProb = logProb
        A,B,pi,E,logProb = calc(A,B,pi,E)
##        print("\n\n\n\n\n\n\n\n\n\n\n")
    res = return_format(A)+"\n"
    res = res + return_format(B)
##        print("RESULTS:\n")
##        print(iters,"\n\n")
##        print_matrix(A)
##        print_matrix(B)
##        print_matrix(pi)
##        print("Log Probability: ",logProb)
##        print("\n"+res)
    print("HI")
    return res
    

print(hmm3(1000))
