import pandas as pd
import numpy as np

def gauss_kernel(x, h):
    return np.exp(-(x**2) / (2 * h**2))

def nadaraya_watson_non_repainting(src, h, mult):
    """
    Non-repainting version of Nadaraya-Watson Envelope (End-point method).
    """
    n = len(src)
    out = np.zeros(n)

    # Precompute coefficients for up to 500 bars back
    window_size = 500
    coefs = np.array([gauss_kernel(i, h) for i in range(window_size)])
    den = np.sum(coefs)

    # For each point, calculate the weighted sum of the last 500 bars
    for i in range(n):
        if i < window_size:
            current_coefs = coefs[:i+1]
            current_den = np.sum(current_coefs)
            window = src[0:i+1][::-1]
            out[i] = np.sum(window * current_coefs) / current_den
        else:
            window = src[i-window_size+1:i+1][::-1]
            out[i] = np.sum(window * coefs) / den

    # MAE calculation: Simple Moving Average of absolute differences
    abs_diff = np.abs(src - out)
    mae = pd.Series(abs_diff).rolling(window=499, min_periods=1).mean().values * mult

    upper = out + mae
    lower = out - mae
    return out, upper, lower

def nadaraya_watson_repainting(src, h, mult):
    """
    Repainting version (full kernel regression over the entire window).
    """
    n = len(src)
    nwe = np.zeros(n)
    sae = 0.

    for i in range(n):
        sum_val = 0.
        sum_w = 0.
        for j in range(n):
            w = gauss_kernel(i - j, h)
            sum_val += src[j] * w
            sum_w += w
        y = sum_val / sum_w
        nwe[i] = y
        sae += abs(src[i] - y)

    sae = (sae / n) * mult
    upper = nwe + sae
    lower = nwe - sae
    return nwe, upper, lower
