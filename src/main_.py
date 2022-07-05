import psutil

from sim_v3 import simulator
from RL_train_functions import train, train_umbrella, theta_metric, alt_umbrella, grid_search, output_configs
from numpy import array, copy, random, argmax
import time

start_time = time.time()
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

if __name__ == '__main__':
    start_time = time.time()
    params = {
        'epochs': [80, 100],
        'minibatch size': [50, 30],
        'epsilon': [0.7, 0.8, 0.5, 1000]
    }
    print(grid_search(params))

#print(theta_metric(train(5, 15, 0.3), 20))
#[5, 15, 0.3] best so far
#[20, 8, 0.1]

# print(len(output_configs(params)))



# # alt_umbrella(10, 5, 20, 0.2)
# # trained_theta = train(5, 30, 0.3)
# a, x, r, Yhat = simulator(array([[-1.16778246,  0.72984809, -0.04524764, -2.71033267],
#  [ 0.76662222,  0.02748385,  1.16494243, -0.96301335],
#  [-1.30129364,  1.12192298,  7.40470291, -5.63792408],
#  [ 1.28928343,  7.00284978, -7.09029932,  1.88767191],
#  [ 0.0804976,   5.08767801, -0.23981209, -2.73047897],
#  [-2.70800845, -2.52037032,  1.44247708,  4.21364908],
#  [-1.13940943, -1.17240092,  4.4804686,  -3.0590391 ]]), 5)


# a, x, r, Yhat = simulator(array([
#     [-12, 0, 0, 0],
#     [12, 0, 0, 0],
#     [0, -12, 0 ,0],
#     [0, 12, 0, 0],
#     [0, 0, -12, 0],
#     [0, 0, 12, 0],
#     [0, 0, 0, 10]
# ]), 5)


# #
# for n in range(len(x)):
#     state = x[n]
#     for idx, belt in {0:0, 2:1, 4:2}.items():
#         if state[idx] == 1 and a[n+1][belt] == 1:
#             print(state, a[n], argmax(Yhat[n]))

print("--- %s seconds ---" % (time.time() - start_time))

# print(array(x))
# print(array(a))
# print(r)
# print(Yhat)
