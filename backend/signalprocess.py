import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import json

with open('data.json','r') as f:
    x = np.array(json.load(f))
# x = electrocardiogram()[2000:4000]

peaks, _ = find_peaks(x, height=0)
plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()


def peak_calc(datas, lookback = 2, combine_dist=50, cutoff = 50):
    """calculate the number of repeats in gesture detected

    Args:
        datas (_type_): all graph data for peak detection
        lookback (int, optional): how mnay gestures to look back at. Defaults to 2.
        combine_dist (int, optional): max dist between each gesture. Defaults to 50.
        cutoff (int, optional): least distance for gesture - prevents ignorning a double/triple gesture. Defaults to 50.

    Returns:
        int: gesture count
    """
    peaks, _ = find_peaks(datas, height=0)
    last_n = peaks[-min(len(peaks),lookback):]
    distances = np.diff(last_n)
    print(distances, last_n, peaks)
    if (len(datas)- last_n[::-1])[0] > cutoff:
        relevant = np.argwhere(distances[::-1] <= combine_dist)
        relevant = relevant[relevant <= lookback]
        return len(relevant) + 1
    return 0
    