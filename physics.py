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

    # parameters (TODO adjust this parameters for best results)
    smoothening = 15  # shows how agresive is smoothening
    thresh = 0.3  # treshold for acceleration (possible values between 0 and 2)
    threshMovment = 3  # How many times over the tresh before starting to mesure
    stall = 10  # For corrupt data
    stallUpper = 15  # stallUpper - stall = times under the tresh before velocity is set to 0


    # filtering signal
    data["accX"] = smooth(data['accX'], smoothening)
    data["accY"] = smooth(data['accY'], smoothening)
    # for i in range(0, (len(data) - par), par):
    for i in range(len(data)):

        timeDiff = data.loc[i, "time"] - timeDiff

        # X axis
        accX = data.loc[i, "accX"]

        # threshold for data cleanup. Recognize big changes in accel, and start messuring speed
        if(abs(accX) > thresh and threshX < stallUpper):
            threshX += 1
        elif(threshX > 0):
            threshX -= 1

        # if a bit of time no accel change and before begining of movement set accel to 0
        if(threshX < threshMovment):
            accX = 0

        # if long time no data change, then mouse is not moving and data is corupt, set speed to 0
        if(threshX < stall):
            speedX = 0

        speedX += (timeDiff * accX)/100
        distanceX += (speedX*timeDiff)/10
        data.loc[i, "speedX"] = speedX
        data.loc[i, "distanceX"] = distanceX

        # Y axis
        accY = data.loc[i, "accY"]

        # threshold for data cleanup. Recognize big changes in accel, and start messuring speed
        if(abs(accY) > thresh and threshY < stallUpper):
            threshY += 1
        elif(threshY > 0):
            threshY -= 1

        # if a bit of time no accel change and before begining of movement set accel to 0
        if(threshY < threshMovment):
            accY = 0

        # if long time no data change, then mouse is not moving and data is corupt, set speed to 0
        if(threshY < stall):
            speedY = 0

        speedY += (timeDiff * accY)/100

        distanceY += (speedY*timeDiff)/100
        data.loc[i, "speedY"] = speedY
        data.loc[i, "distanceY"] = distanceY

    data.plot(x='time', y=['accX', 'speedX',
              'distanceX', 'accY', 'speedY', 'distanceY'])
    plt.title(f.removeprefix(path+"/"))
    plt.show()
