import numpy as np

from sim_v3 import cnvwidth, s_to_ms, timestep, create_interval, fatigue_constant
from random import choice, randint, random
from numpy import exp, array, cumsum
from math import sqrt, ceil
from scipy.special import softmax
from copy import copy
from global_ import fatigue_multiplier
import RL_v2
belt_indexes = {250: [0, 1],
                450: [2, 3],
                650: [4, 5]}


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

def reward_function(state, A, r_H):
    if timestep_bool(state) and not state['t'] == 0:
        reward = 0
        if A[-1][-1] != 1:
            reward += -fatigue_multiplier * (1 + np.argmax(A[-1]))
        for trash_id_state, trash_obj in state['trash_objects'].items():
            if trash_obj.x > cnvwidth and trash_obj.obj_class == 'reject' and not trash_obj.deleted:
                reward += -1

            elif trash_obj in trash_bin and trash_obj.obj_class != 'reject' and not trash_obj.deleted:
                reward += -1
        r_H.append(reward)
        return reward
    else:
        return 0


def fatigue_function(action):
    return action.y * fatigue_constant


def timeout_function(action):
    dist = get_dist_from_trash(action.x, action.y)
    t = 0
    if action.speedx == belts[0].belt_speed:  # belt 1
        t = 0.26 * dist + 533.24
    if action.speedx == belts[1].belt_speed:  # belt 2
        t = 0.15 * dist + 752.35
    if action.speedx == belts[2].belt_speed:  # belt 3
        t = 0.08 * dist + 1140.88
    return int(ceil((t / s_to_ms) / timestep))


def action_function(state, X_t, A, input_theta, input_policy):
    tstep_bool = timestep_bool(state)
    if timeout_bool(state):
        a_t = False
        state['timeout'] -= 1

        if tstep_bool:
            A.append([0, 0, 0, 1])

    else:
        if tstep_bool:
            belt_action_vector = {200: [1, 0, 0, 0],
                                  400: [0, 1, 0, 0],
                                  600: [0, 0, 1, 0]}
            a_t = policy(state, input_policy, X_t, input_theta)  # returns 0, 1, 2 or trash obj

            if isinstance(a_t, int):
                action_vector = [0, 0, 0, 0]
                action_vector[a_t] = 1
                A.append(action_vector)
            else:
                A.append(belt_action_vector[a_t.y])

        else:
            a_t = False
    if tstep_bool:
        clean_up(state)
    return a_t


def pick_action_index(input_theta, X_t, Yhat_H):
    Yhat = softmax(input_theta.T.dot(X_t))
    Yhat_H.append(Yhat)

    cumsum_Yhat = cumsum(Yhat)
    random_number = random()

    for index in range(len(cumsum_Yhat)):
        action_probability = cumsum_Yhat[index]
        if random_number < action_probability:
            return index
    return 3


def policy(state, policy_n, X_t, input_theta):
    action = False
    ybelts = [250, 450, 650]

    if policy_n == 5:
        action_index = RL_v2.select_action(X_t, input_theta)
        action = action_index
        if action_index == 3:
            return 3

    for trash_obj_id, trash_obj in state['trash_objects'].items():
        if policy_n == 5:
            if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelts[action_index]):
                return trash_obj
        elif policy_n == 0:
            action = False
        elif policy_n == 1:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and trash_obj.obj_class == 'reject':
                    return trash_obj
                else:
                    action = 3
        ####################################

        ####################################
        elif policy_n == 6:
            if trash_obj.checkCoordinateIntersection(cnvwidth / 2, 450) and trash_obj.obj_class == 'reject' \
                    and X_t == [0, 1, 1]:
                return trash_obj

    return action


def transition(state, a_t, X):
    new_state = state
    if new_state['t'] % create_interval == 0:
        makeRandomTrash(1)
        makeRandomTrash(2)
        makeRandomTrash(3)

    if timestep_bool(new_state):
        RL_state = [0, 0, 0, 0, 0, 0, 1]
        new_state['old score'] = state['score']
        to_delete = []
        to_delete_bool = False
        if not a_t == 3:  # if not do nothing
            if a_t == 0:
                new_state['fatigue'] += 0.00036
                # new_state['timeout'] += 0
            elif a_t == 1:
                new_state['fatigue'] += 0.00036 * 2
                # new_state['timeout'] += 1
            elif a_t == 2:
                new_state['fatigue'] += 0.00036 * 3
                # new_state['timeout'] += 2
            else:
                if probability(1 - new_state['fatigue'], speed_probability[a_t.speedx],
                               visibility_probability[a_t.visibility]):
                    a_t.dragToTrash()
                    a_t.deleted = True
                new_state['fatigue'] += fatigue_function(a_t)
                # new_state['timeout'] += timeout_function(a_t)

        from global_ import to_delete
        for trash_obj_id, trash_obj in new_state['trash_objects'].items():

            if trash_obj.x > cnvwidth:
                if (trash_obj.obj_class == 'reject' and not trash_obj.deleted) \
                        or (trash_obj in trash_bin and trash_obj.obj_class != 'reject'):
                    new_state['score'] -= 1
                trash_obj.deleted = True

            if not trash_obj.deleted:
                auto_speed(trash_obj)
                trash_obj.update_position()

                for y_belt, indexes in belt_indexes.items():
                    if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                             y_belt) and trash_obj.obj_class != 'reject' and not trash_obj.deleted:
                        RL_state[belt_indexes[y_belt][0]] = 1
                    if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                             y_belt) and trash_obj.obj_class == 'reject' and not trash_obj.deleted:
                        RL_state[belt_indexes[y_belt][1]] = 1
            else:
                to_delete.append(trash_obj_id)
        X.append(array(RL_state))
    state['t'] += 1

    return new_state
