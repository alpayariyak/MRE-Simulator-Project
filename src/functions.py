
import numpy as np

from sim_v3 import cnvwidth, s_to_ms, timestep, create_interval, fatigue_constant
from random import choice, randint, random
from numpy import exp, array, cumsum
from math import sqrt, ceil, floor
from scipy.special import softmax
import RL_v2
from copy import copy
from global_ import timeout_multiplier
belt_indexes = {0:250,
                1:450,
                2:650}

# Math related
def probability(*probs):
    for prob in probs:
        if prob < random():
            return False
    return True


def sigma(x):
    return 1 / (1 + exp(-x))


def get_dist_from_trash(x, y):
    return sqrt((y - 90) ** 2 + (cnvwidth / 2 - x) ** 2)


# Object Creation

from classes import Trash_Object, Belt
from assets import trash_classes, belts, trash_bin, speed_probability, visibility_probability
speed_belt = {belts[0].belt_speed: 0,
                      belts[1].belt_speed: 1,
                      belts[2].belt_speed: 2}

def makeRandomTrash(beltNumber):
    from global_ import trash_id, trash_objects
    if beltNumber == 1:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            choice(trash_classes),
            -100 - randint(0, 150),
            200,
            speedx=belts[0].belt_speed,
            speedy=0,
            rot=randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']
    elif beltNumber == 2:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            choice(trash_classes),
            -100 - randint(0, 150),
            400,
            speedx=belts[1].belt_speed,
            speedy=0,
            rot=randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']
    else:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            choice(trash_classes),
            -100 - randint(0, 150),
            600,
            speedx=belts[2].belt_speed,
            speedy=0,
            rot=randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']


def auto_speed(trash):
    if 300 > trash.hitbox['y'] > 200:
        trash.setSpeed(belts[0].belt_speed)
    elif 500 > trash.hitbox['y'] > 400:
        trash.setSpeed(belts[1].belt_speed)
    elif 700 > trash.hitbox['y'] > 600:
        trash.setSpeed(belts[2].belt_speed)
    else:
        trash.setSpeed(0)


# RL Environment Helpers
def timestep_bool(state):
    return state['t'] % (timestep * s_to_ms) == 0


def timeout_bool(state):
    return state['timeout'] > 0


def clean_up(state):
    from global_ import to_delete
    if to_delete:
        for i in range(len(to_delete)):
            trash_id = to_delete.pop()
            del state['trash_objects'][trash_id]


# RL Environment
def reward_function(state, A, rewards_H):
    from global_ import fatigue_multiplier
    if timestep_bool(state) and not state['t'] == 0:
        reward = 0
        for trash_id_state, trash_obj in state['trash_objects'].items():
            if trash_obj.x > cnvwidth and trash_obj.obj_class == 'reject' and not trash_obj.deleted:
                reward += -1

            elif trash_obj in trash_bin and trash_obj.obj_class != 'reject' and not trash_obj.deleted:
                reward += -1
        rewards_H.append(reward)
        return reward
    elif state['t'] == 0:
        rewards_H.append(0)
        return 0
    else:
        return 0


def fatigue_function(action):
    return action.y * fatigue_constant


def timeout_function(action):
    from global_ import enum_cells

    if isinstance(action, Trash_Object):
        x, y = action.x, action.y
        belt = speed_belt[action.speedx]

    else:
        belt, col = enum_cells[action]
        x = col * 100 -250
        y = belt*200 + 250

    dist = get_dist_from_trash(x, y)
    beltspeed_t = {0: 0.26 * dist + 533.24,
                   1: 0.15 * dist + 752.35,
                   2: 0.15 * dist + 952.35
                   }
    return int(beltspeed_t[belt])


def action_function(state, X_t, A, input_theta, input_policy, timeout_timestep_indexes):
    from global_ import enum_cells
    tstep_bool = timestep_bool(state)

    if timeout_bool(state):
        a_t = False
        if tstep_bool:
            A.append(array([0 for _ in range(len(enum_cells) + 1)]))
            timeout_timestep_indexes.append(len(A) - 1)
    else:
        if tstep_bool:
            action_vector = array([0 for _ in range(len(enum_cells) + 1)])
            a_t, a_t_index = policy(state, input_policy, X_t, input_theta, enum_cells)  # returns 0-15 or trash obj
            action_vector[a_t_index] = 1
            A.append(action_vector)

        else:
            a_t = False

    if tstep_bool:
        clean_up(state)
    return a_t


def policy(state, policy_n, X_t, input_theta, enumCells):
    action = False
    ybelts = [250, 450, 650]

    if policy_n == 5:
        action_index = RL_v2.select_action(X_t, input_theta)
        if action_index == len(enumCells):
            return len(enumCells), len(enumCells)
        action_cell_index = enumCells[action_index]
        action_cell = state['grid']['Element Grid'][action_cell_index[0]][action_cell_index[1]]
        if action_cell:
            return action_cell[0], action_index  # hit
        else:
            return action_index, action_index  # miss

    elif policy_n == 0:
        return len(enumCells), len(enumCells)
    elif policy_n == 1:
        for trash_obj_id, trash_obj in state['trash_objects'].items():
            #     if policy_n == 0:
            #         action = False
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and trash_obj.obj_class == 'reject':
                    return trash_obj, 3
                else:
                    action = len(enumCells), len(enumCells)

        return action


def reset_grid(state):
    state['grid']['Full Grid'] = [[[0, 0] for _ in range(33)] for _ in range(3)]
    state['grid']['Element Grid'] = [[[] for _ in range(33)] for _ in range(3)]


def cells_enum(cells):
    cell_list = []
    for r in range(3):
        for c in cells:
            cell_list.append([r, c])
    cells_dictionary = {cell_n: cell_list[cell_n] for cell_n in range(len(cell_list))}
    return cells_dictionary


def record_state(state, X, cells):
    result = []
    for y in range(3):
        for x_cell in cells:
            for element in range(2):
                result.append(state['grid']['Full Grid'][y][x_cell][element])
    result.append(state['fatigue'])
    result.append(state['t'] / 180000)
    X.append(array(result))


def transition(state, a_t, X, cells):
    new_state = state
    state['timeout'] -= min(1, state['timeout'])

    if new_state['t'] % create_interval == 0:
        makeRandomTrash(1)
        makeRandomTrash(2)
        makeRandomTrash(3)

    if timestep_bool(new_state):
        reset_grid(new_state)

        to_delete = []
        to_delete_bool = False
        if type(a_t) != bool and a_t != len(cells) * 3:
                new_state['timeout'] += timeout_function(a_t) *timeout_multiplier
                if isinstance(a_t, int):
                    new_state['fatigue'] += 0.00009 * (floor(a_t / 5) + 1)
                else:
                    new_state['fatigue'] += fatigue_function(a_t)
                    if probability(1 - new_state['fatigue'], speed_probability[a_t.speedx],
                                   visibility_probability[a_t.visibility]):
                        a_t.dragToTrash()
                        a_t.deleted = True


        from global_ import to_delete
        for trash_obj_id, trash_obj in new_state['trash_objects'].items():

            if trash_obj.x > cnvwidth:
                if (trash_obj.obj_class == 'reject' and not trash_obj.deleted) \
                        or (trash_obj in trash_bin and trash_obj.obj_class != 'reject'):
                    new_state['score'] -= 1
                trash_obj.deleted = True

            if not trash_obj.deleted:
                auto_speed(trash_obj)
                trash_obj.update_position(new_state)
            else:
                to_delete.append(trash_obj_id)
        record_state(new_state, X, cells)

    state['t'] += 1
    return new_state


def clean_RL_output(X_H, A_H, rewards_H, timeout_idx):
    for idx in timeout_idx:
        if idx < len(rewards_H)-1:
            rewards_H[idx+1] += rewards_H[idx]

    delete_multiple_element(X_H, timeout_idx)
    delete_multiple_element(A_H, timeout_idx)
    delete_multiple_element(rewards_H, timeout_idx)


def delete_multiple_element(list_object, indices):
    indices = sorted(indices, reverse=True)
    for idx in indices:
        if idx < len(list_object):
            list_object.pop(idx)