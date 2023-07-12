import math
pi=math.fsum(4*(math.pow(-1,k)/(2*k+1)) for k in range(100000000))
print(pi)