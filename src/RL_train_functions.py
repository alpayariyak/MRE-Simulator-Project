import numpy as np
from functions import sigma
from sim_v3 import simulator


def b_k_function(theta, X_T, total_reward_T, k):
    sum_grad_theta_k_log = 0
    numerator_sum = 0
    denomenator_sum = 0
    i = 0
    k_list_sum_grad_theta_k_log = []
    for X in X_T:
        i += 1
        sum_grad_theta_k_log = 0
        for x_t in X:
            sum_grad_theta_k_log += (1 - sigma(theta.T.dot(x_t))) * x_t[k]
        numerator_sum += np.square(sum_grad_theta_k_log) * total_reward_T[i - 1]
        denomenator_sum += np.square(sum_grad_theta_k_log)
        k_list_sum_grad_theta_k_log.append(sum_grad_theta_k_log)

    return (numerator_sum / i) / (denomenator_sum / i), k_list_sum_grad_theta_k_log


def g_k_function(list_of_sum_grad_theta_k_log, total_reward_T, theta, b, k):
    g_k_sum = 0
    i = 0
    for run in range(len(total_reward_T)):
        i += 1
        g_k_sum += list_of_sum_grad_theta_k_log[k][run] * (total_reward_T[run] - b[k])
    return g_k_sum / i


def baseline(X_T, total_reward_T, theta):

    b = np.zeros((len(theta),))
    list_of_sum_grad_theta_k_log = []
    for k in range(theta.shape[0]):

        b_k, k_list_of_sum_grad_theta_k_log = b_k_function(theta, X_T, total_reward_T, k)
        list_of_sum_grad_theta_k_log.append(k_list_of_sum_grad_theta_k_log)
        b[k] = b_k
    return b, list_of_sum_grad_theta_k_log


def gradient_function(list_of_sum_grad_theta_k_log, total_reward_T, theta, b):
    gradient = np.zeros((len(theta),))
    for k in range(theta.shape[0]):
        g_k = g_k_function(list_of_sum_grad_theta_k_log, total_reward_T, theta, b, k)
        gradient[k] = g_k
    return gradient


def train(epochs, minibatches, epsilon):
    theta = np.random.randn(3, )

    for epoch in range(epochs):
        A_T, X_T, total_reward_T = [], [], []
        for minibatch in range(1, minibatches + 1):
            total_reward = 100
            A, X, total_reward = simulator(theta, 5)
            A_T.append(A), X_T.append(X), total_reward_T.append(total_reward)

        b, a_list_of_sum_grad_theta_k_log = baseline(X_T, total_reward_T, theta)
        gradient = gradient_function(a_list_of_sum_grad_theta_k_log, total_reward_T, theta, b)
        theta += epsilon * gradient

    return theta


