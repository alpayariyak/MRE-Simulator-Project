from sim_v3 import simulator

import time
from RL_v2 import training_policy

import global_


if __name__ == '__main__':
    start_time = time.time()

    simulator(training_policy, 5)
    # # trained_theta = train(5, 30, 0.3)
    print("--- %s seconds ---" % (time.time() - start_time))
