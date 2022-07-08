from sim_v3 import simulator
from RL_train_functions import train, train_umbrella, theta_metric, alt_umbrella, grid_search, output_configs
from numpy import array, full  # , copy, random, argmax
import time
from RL_v2 import Policy
import global_

start_time = time.time()

if __name__ == '__main__':
    start_time = time.time()
    policy = Policy()
    # params = {
    #     'epochs': [80, 100],
    #     'minibatch size': [50, 30],
    #     'epsilon': [0.7, 0.8, 0.5]
    # }
    # print(grid_search(params))
    simulator(policy, 5)
    #
    # e = 0.1
    # epsilon = full((7,4), e)
    # epsilon[-1].fill(e*0.1)
    # print(epsilon)
    # # trained_on_180 = alt_umbrella(10, 20, 15, epsilon)
    # global_.fatigue_multiplier = 1
    # trained_on_20 = alt_umbrella(10, 20, 10, epsilon, seconds=20, multiprocessing_bool=False)
    # #print("180: " + f"{theta_metric(trained_on_180, 40)}")
    # print(f"m: {1}:  " + f"r, s = {theta_metric(trained_on_20, 20)}")
    # print(trained_on_20)
    # # [5, 15, 0.3] best so far
    # # [20, 8, 0.1]

    # # alt_umbrella(10, 5, 20, 0.2)
    # # trained_theta = train(5, 30, 0.3)
    print("--- %s seconds ---" % (time.time() - start_time))
