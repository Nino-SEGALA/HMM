# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import matrixOperations as matOp

def input_hmm0():
    #return A, B and q
    res = [] #[A, B, q]
    for line in sys.stdin:
        lst = line.split()
        res.append(make_matrix(lst))
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

#print("[A, B, q] = ", input_hmm0())

def emissions(A, B, q):
    #calculate the probability of each emission at the next step (q*A*B)
    qA = matOp.mult(q, A)
    return matOp.mult(qA, B)

def hmm0():
    #solve the hmm0 problem
    [A, B, q] = input_hmm0() #we convert the input into 3 matrix
    em = emissions(A, B, q) #we calculate the probability of each emission at the next step
    n, p = len(em), len(em[0])
    res = "" #we convert the matrix em to the recquired type of output
    res += str(n)
    res += " "
    res += str(p)
    for i in range(n):
        for j in range(p):
            res += " "
            res += str(em[i][j])
    return res

print(hmm0())