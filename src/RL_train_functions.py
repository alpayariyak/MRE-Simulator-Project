import numpy as np
from functions import sigma
from sim_v3 import simulator


def b_k_function(theta, X_T, A_T, total_reward_T, k):
    sum_grad_theta_k_log = 0
    numerator_sum = 0
    denomenator_sum = 0
    i = 0
    k_list_sum_grad_theta_k_log = []
    for run_n in range(len(X_T)):
        X = X_T[run_n]
        A = A_T[run_n]
        i += 1
        sum_grad_theta_k_log = 0
        for state_h in range(len(X)):
            x_h = X[state_h]
            action_h = A[state_h]
            sum_grad_theta_k_log += (action_h - sigma(theta.T.dot(x_h))) * x_h[k]
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


def baseline(X_T, A_T, total_reward_T, theta):
    b = np.zeros((len(theta),))
    list_of_sum_grad_theta_k_log = []
    for k in range(theta.shape[0]):
        b_k, k_list_of_sum_grad_theta_k_log = b_k_function(theta, X_T, A_T, total_reward_T, k)
        list_of_sum_grad_theta_k_log.append(k_list_of_sum_grad_theta_k_log)
        b[k] = b_k
    return b, list_of_sum_grad_theta_k_log


def gradient_function(list_of_sum_grad_theta_k_log, total_reward_T, theta, b):
    gradient = np.zeros((len(theta),))
    for k in range(theta.shape[0]):
        g_k = g_k_function(list_of_sum_grad_theta_k_log, total_reward_T, theta, b, k)
        gradient[k] = g_k
    return gradient


def train(epochs, minibatches, epsilon, theta=np.random.randn(3, )):
    for epoch in range(epochs):
        A_T, X_T, total_reward_T = [], [], []
        for minibatch in range(1, minibatches + 1):
            total_reward = 100
            A, X, total_reward = simulator(theta, 5)
            A_T.append(A), X_T.append(X), total_reward_T.append(total_reward)

        b, a_list_of_sum_grad_theta_k_log = baseline(X_T, A_T, total_reward_T, theta)
        gradient = gradient_function(a_list_of_sum_grad_theta_k_log, total_reward_T, theta, b)
        theta += epsilon * gradient

    return theta


def check_wrong_moves(X, A):
    counter = 0
    right_moves = {(0, 0, 1): 0,
                   (0, 1, 1): 1,
                   (1, 0, 1): 0,
                   (1, 1, 1): 0}
    for j in range(180):
        if right_moves[tuple(X[j])] != A[j]:
            # print("Wrong action")
            counter += 1
    return counter


def theta_metric(theta, folds):
    avg_reward = 0
    avg_wrong_moves = 0
    for j in range(folds):
        A, X, total_reward = simulator(theta, 5)
        avg_reward += total_reward
        avg_wrong_moves += check_wrong_moves(X, A)

    avg_reward = avg_reward / folds
    avg_wrong_moves = avg_wrong_moves / folds

    return avg_reward, avg_wrong_moves


def train_umbrella(n, epochs=5, minibatches=10, epsilon=0.2):
    thetas = []
    for i in range(n):
        current_theta = train(epochs, minibatches, epsilon)
        thetas.append(current_theta)
    min_wrong_moves = 999
    min_wrong_moves_theta = []
    max_reward = -999
    max_reward_theta = []
    results = {}
    for theta in thetas:
        avg_reward, avg_wrong_moves = theta_metric(theta, 5)

        if min_wrong_moves > avg_wrong_moves:
            min_wrong_moves = avg_wrong_moves
            min_wrong_moves_theta = theta
        if max_reward < avg_reward:
            max_reward = avg_reward
            max_reward_theta = theta
    print(max_reward, min_wrong_moves, max_reward_theta, min_wrong_moves_theta)

    return min_wrong_moves_theta, max_reward, min_wrong_moves, max_reward_theta, min_wrong_moves_theta


def alt_umbrella(n, epochs=5, minibatches=10, epsilon=0.2):

    thetas = [np.random.randn(3, ) for i in range(n)]

    initial_rewards = []
    initial_wrong_moves = []
    for i in range(n):
        print('initializing: ', i * 100 / n, '%')
        theta = thetas[i]
        avg_reward, avg_wrong_moves = theta_metric(theta, 3)
        print(avg_wrong_moves, avg_reward)
        initial_rewards.append(avg_reward), initial_wrong_moves.append(avg_wrong_moves)

    for i in range(n):
        in_theta = thetas[i]
        print('training: ', i* 100/n, '%')
        current_theta = train(epochs, minibatches, epsilon, in_theta)
        thetas.append(current_theta)

    improved_rewards = 0
    improved_wrong_moves = 0

    for j in range(n):
        theta = thetas[j]
        avg_reward, avg_wrong_moves = theta_metric(theta, 3)
        print(avg_wrong_moves, avg_reward)
        if avg_reward > initial_rewards[j]:
            improved_rewards += 1
        if avg_wrong_moves < initial_wrong_moves[j]:
            improved_wrong_moves += 1

    print(improved_wrong_moves / n, improved_rewards / n)

    return improved_wrong_moves / n, improved_rewards / n
