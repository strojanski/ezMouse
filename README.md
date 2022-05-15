# ezMouse
super duper ez mouse

# Installing Dependencies and Running the PC Side App
Install dependencies by and start listener by running install-dependecies.sh. 
*Attention:* The IP Address for server is currently hardcoded in *main.py*. To use the app for yourself your phone needs to be on the same subnet as your PC and you need to set the value of variable *server_ip* (line 51) in *main.py* to the private IP of your computer.
After the *wifi_comm_server.py* script has been run on PC you should install the apk in /bin/still_trying-0.1-arm64-v8a_armeabi-v7a-debug.apk to your Android device and run it. After the app starts you should be connected to the PC and for the app to work right you first need to press the *Activate Accelerometer* button on the main screen and then you're free to use the ezMouse. The *Goto Mouse* button will take you to a simple screen representing that of a classic computer mouse in 2D. At this point the app supports left and right click and cursor control by gently tilting the device.  

# Compiling the apk
To compile *main.py* after editing it install *buildozer* tool and use *buildozer android debug* command to compile files into an apk found in /bin/still_trying-...apk
