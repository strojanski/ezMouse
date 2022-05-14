import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("Testdata/test1.csv")

#x = np.linspace(0,2*np.pi,100)
#y = np.sin(x) + np.random.random(100) * 0.8

x = data["Time (s)"]
y = data["Linear Acceleration x (m/s^2)"]

#print(x)
#print(y)

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

print(data)

data["Linear Acceleration x (m/s^2)"] = smooth(y,19)

plt.plot(x, y)
plt.plot(x, smooth(y,3))
plt.plot(x, smooth(y,19))
#plt.show()

print(data)