game_length = 180
s_to_ms = 1000
timestep = 0.1
create_interval = 0.5 * s_to_ms  # 5 seconds
cnvheight, cnvwidth = 1230, 3024  # or 800
fatigue_constant = 0.00005

from functions import *


def simulator(input_theta, input_policy, seconds=180, cells=(0, 1, 2, 3, 4)):
    enum_cells = cells_enum(cells)
    import global_
    trash_id, reward, i, fatigue, timeout = 0, 0, 0, 0, 0
    score, total_reward = 100, 100
    global_.trash_objects = {}
    global_.trash_id = 0
    a_t = False  # for i = 0
    state = {'trash_objects': global_.trash_objects, 'score': score, 'fatigue': fatigue,
             'timeout': timeout, 't': i,
             'grid': {
                 'Full Grid': [[[0, 0] for _ in range(33)] for _ in range(3)],
                 'Element Grid': [[[] for _ in range(33)] for _ in range(3)]}}
    X = []
    A = []
    Yhat_H = []

    for i in range(seconds * s_to_ms):
        reward = reward_function(state, A)
        total_reward += reward
        state = transition(state, a_t, X, cells)
        a_t = action_function(state, X[-1], A, input_theta, input_policy,enum_cells)
    return A, X, total_reward, rewards_H, state['score']

