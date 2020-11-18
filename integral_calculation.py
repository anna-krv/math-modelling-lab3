"""Functions for calculating an integral in 3d"""

import numpy as np
from scipy import integrate


def integrate_monte_carlo(f, volume, n=40):  # decrease n for faster computation, increase for better approx
    # Draw n**3 random points in the volume
    x1_list = np.random.uniform(volume['a'], volume['b'], n)
    x2_list = np.random.uniform(volume['c'], volume['d'], n)
    t_list = np.random.uniform(volume['t0'], volume['T'], n)
    # Compute sum of f values inside the integration domain
    f_mean = 0
    for i in range(len(x1_list)):
        for j in range(len(x2_list)):
            for k in range(len(t_list)):
                try:
                    f_mean += f(x1_list[i], x2_list[j], t_list[k])
                except:
                    x1, x2, t = x1_list[i], x2_list[j], t_list[k]
                    print(x1, x2, t, t**2-x1**2-x2**2)
    f_mean = f_mean / float(n ** 3)
    volume_measure = (volume['b'] - volume['a']) * (volume['d'] - volume['c']) * (volume['T'] - volume['t0'])
    return volume_measure * f_mean


def integrate_(func_, volume):  # very slow, could take up to 7 min
    options = {'limit': 50}
    return integrate.nquad(func_,
                           [
                               [volume['a'], volume['b']],
                               [volume['c'], volume['d']],
                               [volume['t0'], volume['T']]
                           ],
                           opts=[options, options, options]
                           )[0]
