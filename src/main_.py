from sim_v3 import simulator
from RL_train_functions import train
from numpy import array, copy
import time
start_time = time.time()
in_theta = train(10, 20, 0.2)
in_theta2 = copy(in_theta)
in_theta2[2] = 0
print(in_theta, in_theta2)


su1 = 0
su2 = 0
su3 = 0
for i in range(5):
    A, X, total_reward = simulator(in_theta, 5)
    A2, X2, total_reward2 = simulator([0, 0, 0], 4)
    A3, X3, total_reward3 = simulator(in_theta2, 5)
    su1 += total_reward
    su2 += total_reward2
    su3 += total_reward3

print(su1 / 5, su2 / 5, su3/5)

print("--- %s seconds ---" % (time.time() - start_time))


