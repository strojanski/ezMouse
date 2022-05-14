import numpy
import scipy
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

#path for test data 
path = os.getcwd() +"/testData"

csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
for f in csv_files:

  #pandanize csv data and print
  data = pd.read_csv(f)
  #print(data)

  #plot data
  #data.plot(x='Time (s)')
  #plt.show()

  #set initial values (TODO - adjust when live data)
  hitrost = 0
  diffTime = 0
  diffX = 0

  for i in range(len(data)):
    diffTime = data.loc[i, "Time (s)"] - diffTime
    diffX = data.loc[i, "Linear Acceleration x (m/s^2)"]
    hitrost +=  diffTime * diffX
    data.loc[i,"hitrost"] = hitrost

  data.plot(x='Time (s)')
  plt.show()
