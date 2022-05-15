import numpy as np
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import pandas as pd

box = np.ones(5)/5
y = [1,2,3,4,5,6,7]
y_smooth = np.convolve(y, box, mode='same')
print(y_smooth)