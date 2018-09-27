import sys

def apriori(T, I, minSup):
    F = 1
    k = 2
    while F != NULL:
        C = candidateGen(F, k-1)
        for c in C:
            count[c] = 0
        for t in T:
            for c in C:
                if c == t:
                    count[c] + 1
        k = k + 1
    return F