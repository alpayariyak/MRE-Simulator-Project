def g_t(rewards, t, gamma, T):
    g = 0
    j = t
    while j < T:
        g = rewards[t] + gamma*g_t(rewards, t+1, gamma, T)
        j += 1
    return g



print(g_t([-3, 5, 2, 7, 1], 0, 0.8, 5))