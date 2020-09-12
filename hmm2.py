import sys
import matrixOperations as matOp

def input_hmm2():
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

def delta_init(B, q, O):
    #calculate delta_1(i)
    em_prob = matOp.column(B, O[0])
    return [matOp.mult_block_by_block(matOp.transpose(q), em_prob)]

def delta_t(A, B, q, O):
    #calculate all vectors delta and delta_idx until t=len(O) steps
    delta = delta_init(B, q, O) #first delta
    delta_idx = []  #no need of index for the first step
    t = len(O)
    for k in range(1, t):
        deltaB = matOp.mult(matOp.column(B, O[k]), matOp.transpose(delta[-1])) #we multiply the column of B with the last delta
        V = matOp.mult_block_by_block(deltaB, matOp.transpose(A)) #we multiply block by blok the result with A
        dlt,  dlt_idx = matOp.maxi(V) #we calculate the new delta and delta_idx by taking the max value and his index
        delta.append(dlt)
        delta_idx.append(dlt_idx)
    return delta, delta_idx

def argmax(u):
    #give the index of the maximum value of a vector
    n = len(u)
    index, max_val = -1, -1
    for i in range(n):
        if u[i][0] > max_val:
            index, max_val = i, u[i][0]
    return index

def states_prob(delta, delta_idx):
    #calculate the states which has the higher probability to be at each step
    T = len(delta)
    n = len(delta[0])
    idx = argmax(delta[-1])
    res = [idx, delta_idx[T-2][idx][0]]
    for k in range(T-2):
        step = T-3-k
        res.append(delta_idx[step][res[-1]][0])
    res.reverse() #we put the result in the right way
    return res

def hmm2():
    #solve the hmm2 problem
    [A, B, q, O] = input_hmm2() #we convert the input into 4 matrix
    delta, delta_idx = delta_t(A, B, q, O)
    states = states_prob(delta, delta_idx)
    res = ""
    for st in states:
        res += str(st) + " "
    return res

print(hmm2())