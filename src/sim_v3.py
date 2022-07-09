game_length = 180
s_to_ms = 1000
timestep = 0.5
create_interval = 0.5 * s_to_ms  # 5 seconds
cnvheight, cnvwidth = 1230, 3024  # or 800
fatigue_constant = 0.000008

from functions import *


def simulator(input_theta, input_policy, seconds=180, fatigue_multiplier=0.1):
    import global_
    trash_id, reward, i, fatigue, timeout = 0, 0, 0, 0, 0
    score, total_reward = 100, 100
    global_.trash_objects = {}
    global_.trash_id = 0
    a_t = False  # for i = 0
    state = {'trash_objects': global_.trash_objects, 'score': score, 'fatigue': fatigue,
             'timeout': timeout, 't': i, 'old score': 100}

    X = []
    A = []
    rewards_H = []

    for i in range(seconds * s_to_ms):
        reward = reward_function(state, A, rewards_H)
        total_reward += reward
        state = transition(state, a_t, X)
        a_t = action_function(state, X[-1], A, input_theta, input_policy)
    return A, X, total_reward, rewards_H, state['score']
