import math
import random
import copy
import numpy as np











def transition(state, action=False):
    new_state = state



def policy(state, X_t, a_theta, policy_n=0):
    action = False
    deletecalled = False
    ybelts = [650, 450, 250]
    for trash_obj_id, trash_obj in state['trash_objects'].items():
        if policy_n == 0:
            action = False
        elif policy_n == 1:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                         ybelt) and trash_obj.obj_class == 'reject' and not deletecalled:
                    action = trash_obj
        elif policy_n == 2:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                         ybelt) and trash_obj.obj_class != 'reject' and not deletecalled:
                    action = trash_obj
        elif policy_n == 3:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and not deletecalled:
                    action = trash_obj
        elif policy_n == 4:
            if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                     450) and trash_obj.obj_class == 'reject' and not deletecalled:
                action = trash_obj
        elif policy_n == 5:
            if probability(sigma(a_theta.T.dot(X_t))) and trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                                                                450) and not deletecalled:
                action = trash_obj
    return action


def simulator(input_theta, pol=5):
    global trash_id
    trash_id = 0
    global trash_objects
    trash_objects = {}# id:object
    total_reward = 100
    reward = 0
    state = {'trash_objects': trash_objects, 'score': score, 'fatigue': fatigue,
             'timeout': timeout, 'timestep': i}
    new_state = state

    X = []
    A = []
    timeouts = []

    for i in range(180000):  # 180000 ms in 3 minutes



        new_state = transition(state, action_t)

        if timestep_bool:
            A.append(A_t)
            X.append(X_t)
            reward = reward_function(new_state, action_t)
            total_reward += reward
            for trash_id, trash_obj in copy.copy(state['trash_objects']).items():
                if trash_obj.deleted:
                    del new_state['trash_objects'][trash_id]

    return A, X, total_reward, timeouts





def baseline(X_T, total_reward_T, theta):
    b = np.zeros((len(theta),))
    for k in range(theta.shape[0]):
        theta_k = theta[k]
        numerator_sum = 0
        denomenator_sum = 0
        i = 1

        for X in X_T:
            sum_grad_thetak_log_policy_k_run = 0
            for x_t in X:
                x_k_t = x_t[k]
                sum_grad_thetak_log_policy_k_run += (1 - sigma(theta.T.dot(x_t))) * x_k_t
                #print(f"{k}         {i}         {(1 - sigmoid_function(theta.T.dot(x_t))) * x_k_t}")
            numerator_sum += np.square(sum_grad_thetak_log_policy_k_run) * total_reward_T[i-1]
            denomenator_sum += np.square(sum_grad_thetak_log_policy_k_run)
            i += 1
        b[k] = (numerator_sum/i) / (denomenator_sum/i)

    return b


def grad_theta(X_T, total_reward_T, theta, b):
    gradient = np.zeros((len(theta),))
    for k in range(theta.shape[0]):
        theta_k = theta[k]
        grad_sum = 0
        i = 1
        for X in X_T:
            sum_grad_thetak_log_policy_k_run = 0
            for x_t in X:
                x_k_t = x_t[k]
                sum_grad_thetak_log_policy_k_run += (1 - sigma(theta.T.dot(x_t))) * x_k_t

            grad_sum += np.square(sum_grad_thetak_log_policy_k_run) * total_reward_T[i - 1]

        gradient[k] = (sum_grad_thetak_log_policy_k_run * (total_reward_T[i - 1] - b[k])) / len(X_T)
    return gradient


def train(epochs, minibatches, epsilon):
    theta = np.random.randn(3, )
    print(score_difference_in_reward(theta, 3))
    for epoch in range(epochs):

        A_T, X_T, total_reward_T, timeouts_T = [], [], [], []

        for minibatch in range(1, minibatches + 1):
            total_reward = 100
            A, X, total_reward, timeouts = simulator(theta)
            A_T.append(A), X_T.append(X), total_reward_T.append(total_reward), timeouts_T.append(timeouts)

        b = baseline(X_T, total_reward_T, theta)
        gradient = grad_theta(X_T, total_reward_T, theta, b)
        theta += epsilon * gradient
        print(score_difference_in_reward(theta, 3), theta)
    return theta


def score_difference_in_reward(theta, folds, pol=4):
    metrics = []
    for fold in range(folds):
        metrics.append(metric_function(theta, folds))
    return np.average(metrics)


def metric_function(theta, folds, pol=4):
    metric = 0
    A_train, X_train, total_reward_train, timeouts = simulator(theta, 1)
    for t in range(len(A_train)):
        if X_train[t][0] == 1 and A_train[t] == 1:
            metric -= 1
        elif X_train[t][1] == 1 and A_train[t] == 0 and not timeouts[t]:
            metric -= 1
        elif X_train[t][1] == 0 and  X_train[t][0] == 0 and A_train[t] == 1 and not timeouts[t]:
            metric -= 1
    return metric


if __name__ == '__main__':
    train(4, 10, 0.6)
    X_T = [ [[0,0,1], [0,1,1], [1,0,1], [1,1,1]],
            [[0,0,1], [0,0,1], [1,0,1], [1,0,1]],
            [[1,0,1], [0,0,1], [0,0,1], [0,0,1]]]

    A_T = [ [0, 1, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1] ]

    arewardlist = [-2, -1, 4]
    atheta = np.random.randn(3, )

    #print(f"k         run            grad_theta_k log pi(u_k | x_k)")
    b = baseline(X_T, arewardlist, atheta)
    print(grad_theta(X_T, arewardlist, atheta, b))
