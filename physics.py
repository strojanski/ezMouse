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

# if two integers have opposite signs.
def oppositeSigns(x, y):
    return x*y >= 0.0

# path for test data
path = os.getcwd() + "/Testdata"

csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
for f in csv_files:

    # pandanize csv data and renaming columns TODO adjust when live data
    data = pd.read_csv(f)
    data.columns = ['time', 'accX', 'accY', 'accZ', 'abs']

    # set initial values (TODO - adjust when live data)
    velocityX = velocityY = timeDiff = distanceX = distanceY = accX = accY = threshX = threshY = 0
    par = 1

    # parameters (TODO adjust this parameters for best results)
    smoothening = 15  # shows how agresive is smoothening
    thresh = 0.2  # treshold for acceleration (possible values between 0 and 2)
    threshMovment = 3  # How many times over the tresh before starting to mesure
    stall = 10  # For corrupt data
    stallUpper = 25  # stallUpper - stall = times under the tresh before velocity is set to 0

    #corrupt velocity debuging
    velocityXDebug = accXDebug = 0
    XDebug = False


    # filtering signal
    data["accX"] = smooth(data['accX'], smoothening)
    data["accY"] = smooth(data['accY'], smoothening)
    # for i in range(0, (len(data) - par), par):
    for i in range(len(data)):

        # print("prejsni cikel", data.loc[i, "time"], timeDiff)
        timeDiff = data.loc[i, "time"] - data.loc[max(i - 1, 0), "time"]
        # print(data.loc[i, "time"], timeDiff)

        # X axis
        accX = data.loc[i, "accX"]

        # threshold for data cleanup. Recognize big changes in accel, and start messuring velocity
        if(abs(accX) > thresh and threshX < stallUpper):
            threshX += 1
        elif(threshX > 0):
            threshX -= 1

        # if a bit of time no accel change and before begining of movement set accel to 0
        if(threshX < threshMovment):
            accX = 0
        
        # if long time no data change, then mouse is not moving and data is corupt, set velocity to 0
        if(threshX < stall):
            velocityX = 0
        """
        #fix for corrupt velocity 2 (if velocity changes sign => set velocity do 0 until acceleration changes sign)
        if(oppositeSigns(velocityX, velocityXDebug)):
            velocityX = 0
            XDebug = True
        if(XDebug == True and not oppositeSigns(accX, accXDebug)):
            velocityX = 0
            XDebug = False
        velocityXDebug = velocityX
        accXDebug = accX"""

        velocityX += (timeDiff * accX)*10
        distanceX += (velocityX*timeDiff)
        data.loc[i, "velocityX"] = velocityX
        data.loc[i, "distanceX"] = distanceX

        # Y axis
        accY = data.loc[i, "accY"]

        # threshold for data cleanup. Recognize big changes in accel, and start messuring velocity
        if(abs(accY) > thresh and threshY < stallUpper):
            threshY += 1
        elif(threshY > 0):
            threshY -= 1

        # if a bit of time no accel change and before begining of movement set accel to 0
        if(threshY < threshMovment):
            accY = 0

        # if long time no data change, then mouse is not moving and data is corupt, set velocity to 0
        if(threshY < stall):
            velocityY = 0

        velocityY += (timeDiff * accY)*10
        distanceY += (velocityY*timeDiff)
        data.loc[i, "velocityY"] = velocityY
        data.loc[i, "distanceY"] = distanceY

    #ploting all info, dependent on time
    data.plot(x='time', y=['accX', 'velocityX',
              'distanceX', 'accY', 'velocityY', 'distanceY'])
    plt.title(f.removeprefix(path+"/"))
    plt.show()

    #ploting path over x and y coordinates
    data.plot(x='distanceX', y='distanceY')
    plt.title(f.removeprefix(path+"/") + "koordinate poti")
    plt.show()
