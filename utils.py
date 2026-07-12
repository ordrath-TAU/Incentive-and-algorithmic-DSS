import numpy as np
from scipy.stats import norm

def v_ratio_round(value, decimals=2):
    """
    Rounds the value ratio to the specified number of decimals.
    """
    # Insert your specific rounding logic here if it differs from np.round
    return np.round(value, decimals)

def SDT(hits, misses, false_alarms, correct_rejections):
    """
    Calculates standard Signal Detection Theory (SDT) metrics.
    Returns d-prime (sensitivity) and c (criterion/bias).
    """
    # Calculate hit rate and false alarm rate
    hit_rate = hits / (hits + misses)
    fa_rate = false_alarms / (false_alarms + correct_rejections)
    
    # Adjust extreme values to avoid infinity in z-scores
    hit_rate = np.clip(hit_rate, 0.01, 0.99)
    fa_rate = np.clip(fa_rate, 0.01, 0.99)
    
    # Calculate Z-scores
    z_hit = norm.ppf(hit_rate)
    z_fa = norm.ppf(fa_rate)
    
    # Calculate d-prime and criterion
    d_prime = z_hit - z_fa
    c = -(z_hit + z_fa) / 2.0
    
    return d_prime, c
