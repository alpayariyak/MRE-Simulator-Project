from sim_v3 import simulator
from RL_train_functions import train
from numpy import array, copy
import time
start_time = time.time()
in_theta = train(10, 20, 0.2)
print(in_theta)
su1 = 0
su2 = 0

for i in range(20):
    A, X, total_reward = simulator(array(in_theta), 5)

    # for j in range(180):
    #     if X[j] == [0, 1, 1] and A[j] == 0 or X[j] == [1, 0, 1] and A[j] != 0:
    #         print("Wrong action 1")
    #         print(X[j], A[j])

    A2, X2, total_reward2 = simulator([0, 0, 0], 4)
    #
    # for j in range(180):
    #     if X2[j] == [0, 1, 1] and A2[j] == 0 or X2[j] == [1, 0, 1] and A2[j] != 0:
    #         print("Wrong action")
    #         print(X2[j], A2[j])

    su1 += total_reward
    su2 += total_reward2

print((su2 - su1)/20)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#

