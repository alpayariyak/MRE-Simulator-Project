import numpy as np
from functions import sigma
from sim_v3 import simulator


def baseline(X_T, A_T, total_reward_T, Yhat_T, input_theta):
    b = np.zeros(input_theta.shape)
    sum_gradlog_unsquared = []
    for run_n in range(len(X_T)):
        sum_gradlog_unsquared.append(X_T[run_n].T.dot(A_T[run_n] - Yhat_T[run_n]))

    numerator = 0
    denominator = 0
    for run_n in range(len(X_T)):
        squared = np.square(sum_gradlog_unsquared[run_n])
        numerator += squared * total_reward_T[run_n]
        denominator += squared

    return numerator / denominator, sum_gradlog_unsquared


def gradient_function(sum_gradlog_unsquared, total_reward_T, b):
    gradient = np.zeros(b.shape)

    for run_n in range(len(total_reward_T)):
        gradient += sum_gradlog_unsquared[run_n] * (np.full(gradient.shape, total_reward_T[run_n]) - b)

    return gradient / len(total_reward_T)


def train(epochs, minibatches, epsilon, theta=np.random.randn(7, 4)):
    for epoch in range(epochs):
        A_T, X_T, total_reward_T, Yhat_T = [], [], [], []
        for minibatch in range(1, minibatches + 1):
            A, X, total_reward, Yhat = simulator(theta, 5)
            A_T.append(A), X_T.append(X), total_reward_T.append(total_reward), Yhat_T.append(Yhat)

        b, sum_gradlog_unsquared = baseline(X_T, A_T, total_reward_T, Yhat_T, theta)
        gradient = gradient_function(sum_gradlog_unsquared, total_reward_T, b)
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
        print('training: ', i * 100 / n, '%')
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
