import numpy as np
from time import time

l = (1, 2)
n = 3
print(l + (n,))

lag_data = [(44, 32), (42, 57), (41, 527), (40, 163), (43, 20)]
poss_lag = [527, 163, 57, 32, 20]
ans = round(128 * sum([l[0] * l[1] for l in lag_data]) / sum(poss_lag))
print(ans / 128)


l = [1, 2, 3, 4]
print(l[3:])

print(type(True))

l = []
data = np.array([1, 2, 3])
start = time()
for i in range(10**6):
    l.extend(data)
print(time() - start)
l = []
data = [1, 2, 3]
start = time()
for i in range(10**6):
    l.extend(data)
print(time() - start)