import math
import random

#

game_length = 180
s_to_ms = 1000
timestep = 1
create_interval = 0.5 * s_to_ms  # 5 seconds
cnvheight, cnvwidth = 1230, 3024  # or 800
fatigue_constant = 0.0000018

from functions import *


def simulator(input_theta, input_policy):
    import global_
    trash_id, reward, i, fatigue, timeout = 0, 0, 0, 0, 0
    score, total_reward = 100, 100
    global_.trash_objects = {}
    global_.trash_id = 0
    a_t = False  # for i = 0
    state = {'trash_objects': global_.trash_objects, 'score': score, 'fatigue': fatigue,
             'timeout': timeout, 't': i}

    X = []
    A = []


    for i in range(180 * s_to_ms):
        reward = reward_function(state, a_t)
        total_reward += reward
        state = transition(state, a_t)
        state['t'] = i
        X_t = simple_state(state, X)
        a_t = action_function(state, X_t, A, input_theta, input_policy)
    from global_ import total_rejects
    print(state['score'], total_reward, total_rejects, state)
