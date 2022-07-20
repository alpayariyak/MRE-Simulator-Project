game_length = 180
s_to_ms = 1000
timestep = 0.1
create_interval = 0.5 * s_to_ms  # 5 seconds
cnvheight, cnvwidth = 1230, 3024  # or 800
fatigue_constant = 0.000001

from functions import *
from global_ import cells

def simulator(input_theta, input_policy, seconds=180, cells=cells, print_state = False):
    import global_
    timeout_timestep_indexes = []
    trash_id, reward, i, fatigue, timeout = 0, 0, 0, 0, 0
    score, total_reward = 100, 100
    global_.trash_objects = {}
    global_.trash_id = 0
    global_.enum_cells = cells_enum(cells)
    a_t = False  # for i = 0
    state = {'trash_objects': global_.trash_objects, 'score': score, 'fatigue': fatigue,
             'timeout': timeout, 't': i,
             'grid': {
                 'Full Grid': [[[0, 0] for _ in range(33)] for _ in range(3)],
                 'Element Grid': [[[] for _ in range(33)] for _ in range(3)]}}
    X = []
    A = []
    rewards_H = []

    for i in range(seconds * s_to_ms):
        reward = reward_function(state, A, rewards_H)
        total_reward += reward
        state = transition(state, a_t, X, cells)
        a_t = action_function(state, X[-1], A, input_theta, input_policy, timeout_timestep_indexes)
    if(print_state):
        print(state['fatigue'], state['timeout'], len(timeout_timestep_indexes))
    clean_RL_output(X, A, rewards_H, timeout_timestep_indexes)
    return A, X, total_reward, rewards_H, state['score']



