from sim_v3 import simulator
from RL_train_functions import train, train_umbrella, check_wrong_moves, alt_umbrella
from RL_train_functions_V2 import baseline, gradient_function
from numpy import array, random
from numpy.random import rand
import time

# # in_theta = train(10, 20, 0.2)
# in_theta = array([-100, 100, -50])
# print(in_theta)
# su1 = 0
# su2 = 0
# with open('readme.txt', 'w') as f:
#     f.write(f"{train_umbrella(100, 10, 20)}")


#
# for i in range(1):
#     A, X, total_reward = simulator(in_theta, 5)
#     A2, X2, total_reward2 = simulator([0, 0, 0], 6)
#     print(f"Policy 6: {check_wrong_moves(X2, A2)}")
#     su1 += total_reward
#     su2 += total_reward2

# print((su2 - su1) / 1)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#

# alt_umbrella(10, 5, 10, 0.2)
start_time = time.time()
a, x, r, Yhat_1 = simulator(train(5, 10, 0.3), 5)
print("--- %s seconds ---" % (time.time() - start_time))

print(r)
print(a)
print(x)