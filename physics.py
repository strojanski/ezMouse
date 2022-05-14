import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

# functions


def integrate(x, y):
    area = np.trapz(y=y, x=x)
    return area

# function for signal filtering
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
    
# path for test data
path = os.getcwd() + "/Testdata"

csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
for f in csv_files:

    # pandanize csv data and renaming columns TODO adjust when live data
    data = pd.read_csv(f)
    data.columns = ['time', 'accX', 'accY', 'accZ', 'abs']

    # set initial values (TODO - adjust when live data)
    speedX = speedY = timeDiff = distanceX = distanceY = accX = accY = threshX = threshY = 0
    par = 1

    # filtering signal
    data["accX"] = smooth(data['accX'], 15)
    data["accY"] = smooth(data['accY'], 15)


    # for i in range(0, (len(data) - par), par):
    for i in range(len(data)):

        timeDiff = data.loc[i, "time"] - timeDiff

        #X axis
        accX = data.loc[i, "accX"]

        # threshold for data cleanup. Recognize big changes in accel, and start messuring speed
        if(abs(accX) > 1 and threshX < 20):
            threshX += 1
        elif(threshX > 0):
            threshX -= 1

        # if a bit of time no accel change and before begining of movement set accel to 0
        if(threshX < 5):
            accX = 0

        # if long time no data change, then mouse is not moving and data is corupt, set speed to 0
        if(threshX < 10):
            speedX = 0

        speedX += (timeDiff * accX)/100
        distanceX += (speedX*timeDiff)/100
        data.loc[i, "speedX"] = speedX
        data.loc[i, "distanceX"] = distanceX


        #Y axis
        accY = data.loc[i, "accY"]

        # threshold for data cleanup. Recognize big changes in accel, and start messuring speed
        if(abs(accY) > 1 and threshY < 20):
            threshY += 1
        elif(threshY > 0):
            threshY -= 1

        # if a bit of time no accel change and before begining of movement set accel to 0
        if(threshY < 5):
            accY = 0

        # if long time no data change, then mouse is not moving and data is corupt, set speed to 0
        if(threshY < 10):
            speedY = 0

        speedY += (timeDiff * accY)/100
        distanceY += (speedY*timeDiff)/100
        data.loc[i, "speedY"] = speedY
        data.loc[i, "distanceY"] = distanceY

    data.plot(x='time', y=['accX', 'speedX', 'distanceX', 'accY', 'speedY', 'distanceY'])
    plt.title(f.removeprefix(path+"/"))
    plt.show()

""" useless posibly
if par != 1:  # taking bigger sample size for inetgrate
    df = data.loc[(i):(i+par)]  # data frame
    spremembaspeedi = integrate(
        df["time"].values, df["accX"].values)  # "integrate"
    speed += spremembaspeedi
    data.loc[i:i+par, "speed"] = speed

else:  # take every sample for "integration
"""
