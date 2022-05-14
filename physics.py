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
  print(data)