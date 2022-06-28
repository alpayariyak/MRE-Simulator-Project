from sim_v3 import simulator
from RL_train_functions import train, train_umbrella, check_wrong_moves, alt_umbrella
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
trained_theta = train(5, 5, 0.3)
print('done')
a, x, r, Yhat_1 = simulator(trained_theta, 5)
a2, x2, r2, Yhat_2 = simulator(trained_theta, 5)
a3, x3, r3, Yhat_3 = simulator(trained_theta, 5)
print("--- %s seconds ---" % (time.time() - start_time))

print(r, r2, r3)
print(a, a2, a3)
print(x, x2, x3)
print(Yhat_1, Yhat_2, Yhat_3)