import numpy as np
from scipy.stats import norm


def cdf_normal_distribution(x, mean, variance):
    # Calculate the standard deviation from the variance
    std_dev = variance ** 0.5

    # Standardize the variable x to Z
    z = (x - mean) / std_dev

    # Calculate the CDF using the standard normal distribution
    cdf_value = norm.cdf(z)

    return cdf_value


def d1_calc(r, sigma, T, t, S, K):
    # return d1 which serves as arg for cdf function
    return (np.log(S/K) + (r + sigma**2/2)*(T-t))/(sigma*np.sqrt(T-t))


def d2_calc(r, sigma, T, t, S, K):
    # return d1 which serves as arg for cdf function
    return (np.log(S/K) + (r - sigma**2/2)*(T-t))/(sigma*np.sqrt(T-t))


def d2_from_d1(d1, sigma, T, t):
    # return d2 which serves as arg for cdf function
    return d1 - sigma*np.sqrt(T-t)


def BSM_Europ_call(S, K, r, q, sigma, T, t):
    # return BSM Solution for European call option g = max(S-K, 0)
    d1 = d1_calc(r-q, sigma, T, t, S, K)
    d2 = d2_calc(r-q, sigma, T, t, S, K)

    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    # print('N_d1', N_d1)
    # print('N_d2', N_d2)

    C = S*np.exp(-q*(T-t))*N_d1 - K*np.exp(-r*(T-t))*N_d2

    return C


def BSM_Europ_put(S, K, r, q, sigma, T, t):
    # return BSM Solution for European put option g = max(K-S, 0)
    d1 = d1_calc(r-q, sigma, T, t, S, K)
    d2 = d2_calc(r-q, sigma, T, t, S, K)

    N_neg_d1 = norm.cdf(-d1)
    N_neg_d2 = norm.cdf(-d2)
    # print('N_d1', N_d1)
    # print('N_d2', N_d2)

    P = K*np.exp(-r*(T-t))*N_neg_d2 - S*np.exp(-q*(T-t))*N_neg_d1

    return P


if __name__ == "__main__":
    r = 0.05
    sigma = 0.2
    T = 0.5
    t = 0
    S_0 = 100
    K = 100
    q = 0.01
    d1 = d1_calc(r, sigma, T, t, S_0, K)
    # print('d1', d1)
    d2 = d2_calc(r, sigma, T, t, S_0, K)
    print('d2', d2)
    d2 = d2_from_d1(d1, sigma, T, t)
    print('d2', d2)
    mean = 0
    variance = 1

    # N_d1 = cdf_normal_distribution(d1, mean, variance)
    # N_d2 = cdf_normal_distribution(d2, mean, variance)
    Call = BSM_Europ_call(S_0, K, r, q, sigma, T, t)

    print('Call', Call)
