from re import L
from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter 
import os             #TODO remove when mergin -> just for testing
import glob           # -||--

# function for signal filtering
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def gladi(a, kolicina):
    gladek = np.empty(200, dtype=float)
    for i in range(200):
        j = max((kolicina - i), 0)
        k = max(i-kolicina,0)
        l = sum(a[k:max(0,i-1)])
        gladek[i] = (j * gladek[k] + l)/kolicina
    return gladek

# path for test data  #TODO remove when mergin -> just for testing with imported data
path = os.getcwd() + "/Testdata"
csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files TODO when live data, change to while recieve data(pandas dataframo) do...
for f in csv_files:

    # pandanize csv data and renaming columns TODO remove when live data (we will recieve pandas dataframe)
    data = pd.read_csv(f)
    data.columns = ['time', 'accX', 'accY', 'accZ', 'abs']

    # set initial values (TODO - adjust when live data)
    velocityX = velocityY = timeDiff = distanceX = distanceY = accX = accY = threshX = threshY = 0
    speedCheckX = speedCheckY = False

    # parameters (TODO adjust this parameters for best results )
    smoothening = 30  # shows how agresive is smoothening
    thresh = 0.1  # treshold for acceleration (possible values between 0 and 2)
    threshMovment = 5  # How many times over the tresh before starting to mesure 
    stall = 10  # For corrupt data 
    stallUpper = 40  # stallUpper - stall = times under the tresh before velocity is set to 0

    # filtering signal
<<<<<<< HEAD
    data["accX"] = smooth(data['accX'], smoothening)
    data["accX"] = smooth(data['accX'], smoothening)
    data["accY"] = smooth(data['accY'], smoothening)
    data["accY"] = smooth(data['accY'], smoothening)
=======
    # data["accX"] = smooth(data['accX'], smoothening)
    # data["accY"] = smooth(data['accY'], smoothening)

    timeDiff = 0.005

    for j in range(len(data)):
        data.loc[j, "time"] = j * timeDiff

    prejx = prejy = 0
    for h in range(0, len(data) - 199, 200):
        time = data.loc[h:h+200, "time"].values
        xos = data.loc[h:h+200, "accX"].values
        yos = data.loc[h:h+200, "accY"].values
        xos = gladi(xos, 30)
        yos = gladi(yos, 30)
        prejx = xos[199]
        prejy = yos[199]
        data.loc[h:h+199, "accX"] = xos
        data.loc[h:h+199, "accY"] = yos
        
    # data.plot(x="time", y=['accX', 'accY'])
    # plt.title(h)
    # plt.show
>>>>>>> 9d12068139fde2cb691e3c2e1136711c3fa26470

    for i in range(len(data)):
        #time differenc between mesurments (for velocity and distance calculation)

        # X axis acceleration
        accX = data.loc[i, "accX"]

        # threshold for data cleanup. Recognize big changes in acceleration, and start messuring velocity
        if(abs(accX) > thresh and threshX < stallUpper):
            threshX += 1
        elif(threshX > 0):
            threshX -= 1

        # if a bit of time no acceleration change and before begining of movement, set acceleration to 0
        if(threshX < threshMovment):
            accX = 0
        
        # if long time no data change, then mouse is not moving and data is corupt, set velocity to 0 
        if(threshX < stall):
            speedCheckX = False
            velocityX = 0

        # Recognize pattern (big acceleration change then oposite acceleration => set vel to 0 after that) TODO
        # This should be partially handeled by previous if statement

        # velocity and distance calc
        velocityX += (timeDiff * accX)*10

        # if acc change prefix reset speedCheck
        # if(i > 0 and (data.loc[i - 1, "accX"]*accX) < 0):
        #    speedCheckX = False

        # velocity adjustment for hard stop
        if(i > 0 and (data.loc[i-1, "velocityX"] * velocityX) < 0):
            speedCheckX = True

        # velocity to 0
        if(speedCheckX):
            velocityX = 0

        distanceX += (velocityX*timeDiff)
        data.loc[i, "velocityX"] = velocityX
        data.loc[i, "distanceX"] = distanceX

        # Y axis (everything the same as X axis, put in function perhaps?)
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
        if(threshY <= stall):
            speedCheckY = False
            velocityY = 0

        velocityY += (timeDiff * accY)*10

        # if acc change prefix reset speedCheck
        # if(i > 0 and (data.loc[i - 1, "accY"]*accY) < 0):
        #     speedCheckY = False
        
        # velocity adjustment for hard stop
        if(i > 0 and (data.loc[i-1, "velocityY"] * velocityY) < 0):
            speedCheckY = True

        # velocity to 0
        if(speedCheckY):
            velocityY = 0

        distanceY += (velocityY*timeDiff)
        data.loc[i, "velocityY"] = velocityY
        data.loc[i, "distanceY"] = distanceY

    #ploting all info, dependent on time, adjust y columns as needed for best ploting
    data.plot(x='time', y=['accX', 'velocityX',
              'distanceX', 'accY', 'velocityY', 'distanceY'])
    plt.title(f.removeprefix(path+"/"))
    plt.show()

    #ploting path over x and y coordinates
    data.plot(x='distanceX', y='distanceY')
    plt.title(f.removeprefix(path+"/") + "koordinate poti")
    plt.show()
