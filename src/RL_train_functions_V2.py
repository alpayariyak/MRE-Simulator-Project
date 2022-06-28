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

    return gradient/len(total_reward_T)
