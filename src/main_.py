from sim_v3 import simulator
from RL_train_functions import train
from numpy import array, copy
import time
# start_time = time.time()
# in_theta = train(10, 10, 0.1)
# print(in_theta)


su1 = 0
su2 = 0
for i in range(20):
    A, X, total_reward = simulator(array([ -100, +100, -50 ]), 5)
    A2, X2, total_reward2 = simulator([0, 0, 0], 4)
    su1 += total_reward
    su2 += total_reward2

print(su1 / 20, su2 / 20)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
#
# A, X, total_reward = simulator(array([ -9.51130263,  -1.89338268, -12.07633676]), 5)
# print(A)