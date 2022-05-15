import socket
from multiprocessing.connection import Listener
import time
import sys
import _thread
import signal
import numpy as np
import pandas as pd
import pyautogui

pd.options.mode.chained_assignment = None  # default='warn'

# function for signal filtering
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def gladi(a, kolicina):
    len = a.shape[0]   
    gladek = np.empty(len, dtype=float)
    for i in range(len):
        j = max((kolicina - i), 0)
        k = max(i-kolicina,0)
        l = sum(a[k:max(0,i-1)])
        gladek[i] = (j * gladek[k] + l)/kolicina
    return gladek

def input_thread(list_of_inputs):
    input()
    list_of_inputs.append(True)

listen_ip = socket.gethostbyname(socket.gethostname())
listen_port = 4444     

listener = Listener((listen_ip, listen_port), authkey=b'password')
print (f"Listening on {listen_ip}:{listen_port}")

print ("Ready to connect")

# Accept a connection
conn = listener.accept()

SENSITIVITY = 800

run = True

count = 0
start = time.time()
list_of_inputs = []
_thread.start_new_thread(input_thread, (list_of_inputs,))
df = pd.DataFrame()
prev = pd.DataFrame()
while not list_of_inputs:
    while conn.poll():
        try:
            msg = conn.recv()
            
            # data = f"{sensor_data}, {self.left_value}, {self.right_value}"
            # (3-tuple) bool bool = (float, float, float) bool bool
            #print(f"received: {msg}")
            
            if not prev.empty:
                prev = df

            print(msg.head())
            print("")
            df = msg.iloc[1:, :]
            data = df
            print(df.head())

            # set initial values (TODO - adjust when live data)
            velocityX = velocityY = timeDiff = distanceX = distanceY = accX = accY = threshX = threshY = 0

            # parameters (TODO adjust this parameters for best results )
            smoothening = 15  # shows how aggressive is smoothening
            thresh = 0.5  # treshold for acceleration (possible values between 0 and 2)
            threshMovment = 1  # How many times over the tresh before starting to mesure 
            stall = 10  # For corrupt data 
            stallUpper = 25  # stallUpper - stall = times under the tresh before velocity is set to 0

            # filtering signal
            data.loc[:,"accX"] = gladi(data.loc[:,'accX'], smoothening)
            data.loc[:,"accY"] = gladi(data.loc[:,'accY'], smoothening)

            for i in range(1, len(data)):
                #time differenc between mesurments (for velocity and distance calculation)
                timeDiff = 0.005

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
                    velocityX = 0

                # Recognize pattern (big acceleration change then oposite acceleration => set vel to 0 after that) TODO
                # This should be partially handeled by previous if statement

                #velicity and distance calc
                velocityX += (timeDiff * accX)*10
                distanceX += (velocityX*timeDiff)
                #data.loc[i, "velocityX"] = velocityX
                #data.loc[i, "distanceX"] = distanceX

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
                    velocityY = 0

                velocityY += (timeDiff * accY)*10
                distanceY += (velocityY*timeDiff)

            #if (pyautogui.position()[0]+distanceX*SENSITIVITY >= pyautogui.):
            #    distanceX = 0
            #if not pyautogui.onSscreen(pyautogui.position()[1]+distanceY*SENSITIVITY):
            #    distanceY = 0
            pyautogui.moveRel(distanceX*SENSITIVITY, distanceY*SENSITIVITY*-1)
            
            if True in df["left_value"].unique():
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp()
            if True in df["right_value"].unique():
                pyautogui.mouseDown(button="right")
            else:
                pyautogui.mouseUp(button="right")


            conn.send(b"thx")
            
            print(count)
            count += 1
        except EOFError as err:
            run = False

