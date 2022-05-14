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


# path for test data
path = os.getcwd() + "/testData"

csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
for f in csv_files:

    # pandanize csv data and print
    data = pd.read_csv(f)
    #data.rename(columns={"Time (s)": "time", "Linear Acceleration x (m/s^2)": "x", "Linear Acceleration y (m/s^2)":"y"}) Not working

    # print(data)

    # set initial values (TODO - adjust when live data)
    hitrost = 0
    diffTime = 0
    pot = 0
    X = 0
    par = 1

    for i in range(0, (len(data) - par), par):

        if par != 1: #taking bigger sample size for inetgrate
            df = data.loc[(i):(i+par)]  #data frame 
            #print(df)
            spremembaHitrosti = integrate(
                df["Time (s)"].values, df["Linear Acceleration x (m/s^2)"].values)  # "integrate"
            hitrost += spremembaHitrosti
            data.loc[i:i+par, "hitrost"] = hitrost
            #print(round((i + i + par)/2))

        else:  # take every sample for "integration"
            diffTime = data.loc[i, "Time (s)"] - diffTime
            X = data.loc[i, "Linear Acceleration x (m/s^2)"]

            # treshold
            if(abs(X) < 0.5):
                X = 0
            hitrost += diffTime * X
            pot += hitrost*diffTime
            data.loc[i, "hitrost"] = hitrost
            data.loc[i, "pot"] = pot

    data.plot(x='Time (s)', y={'Linear Acceleration x (m/s^2)', 'hitrost'})
    plt.show()
