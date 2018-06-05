# Human-tracking-Orbbec-Astra-ROS
## Description:
This package uses the skeleton tracking of the Astra Orbbec SDK to determine the position of a human in the camera frame. The position in the camera frame is converted to the a position in the map of the AGV. The package recognizes a person and sends 2D nav goals to the AGV to let him follow a human.
## Prerequisites:
-    Ros Kinetic on Ubuntu 16.04 or higher (package fully tested on Ubuntu 16.04 with Kinetic)
-    Orbbec Astra Pro camera
## Installation:
Before cloning and installing this package, the following programs and packages have to be installed on your system. 
-    CMake
-    OpenNI
-    Orbbec Astra SDK
-    astra_body_tracker
-    body_tracker_msgs
### CMake
You maybe already have CMake on your machine. If you don't have it, you need to dowload it from their webpage: https://cmake.org/download/. When the dowload is finished, make a new directory and past the downloaded file in this directory and unzip it.
```
cd
mkdir programs
cd programs/cmake-<your_version>
```
To install CMake run the following command (this can take a few minutes)
```
sudo ./bootstrap && make && make install
```
### OpenNI
Download the Orbbec OpenNI SDK from the following site: https://orbbec3d.com/develop/. Copy this zip file to the programs directory you've made with the installation of CMake. Unzip the file in this directry. Go to:
```
cd programs/OpenNI_<your_version>/Linux
```
Here unzip the OpenNI-Linux-x64-2.3 folder and run the following commands:
```
cd OpenNI-Linux-x64-2.3
chmod +x install.sh
sudo ./install.sh
```
Plug your camera and run:
```
source OpenNIDevEnvironment
```
Before you can test visual samples, you will need freeglut3 header and libaries, please install:
```
sudo apt-get install build-essential freeglut3 freeglut3-dev
```
Now freeglut3 is install, build sample and try if it works
```
cd Samples/SimpleViewer
make
cd Bin/x64-Release
./SimpleViewer
```
If the program is correctly installed a new window opens with a yellow depth video stream.
### Orbbec Astra SDK
Download the Orbbec astra SDK zip file for your machine from the the Orbbec site: https://orbbec3d.com/develop/. Copy this zip file to the directeroy 'programs' which you have made with the install of CMake and unzip the file. Rename the unzipped folder to Astra_SDK for easier navigation through the folders. Go to and run:
```
cd programs/Astra_SDK/install
chmod +x install.sh
sudo ./install.sh
```
To test if the Astra SDK is installed properly, you need to have the SFML libraries
```
sudo apt-get install libsfml-dev
```
Test the software with the following commands:
```
cd ..
cd bin
./ SimpleBodyViewer-SFML
```
If the program is installed correctly, a new window pops up wich recognizes a human and draws a skeleton in the picture.
### astra_body_msgs
The next step is to clone the package with the message type for the astra_body_tracker from this github repository: https://github.com/shinselrobots/body_tracker_msgs. In the terminal go to the source of your catkin_ws and clone and build this package:
```
cd catkin_ws/src
git clone https://github.com/shinselrobots/body_tracker_msgs.git
cd ..
catkin_make
```
### astra_body_tracker
First step is to clone the astra_body_tracker from this github repository: https://github.com/KrisPiters/astra_body_tracker. In the terminal go to the source of your catkin_ws and clone and build this package:
```
cd catkin_ws/src
git clone https://github.com/KrisPiters/astra_body_tracker.git
```
Before running catkin_make, make sure the path to the Astra_SDK in the CMakeLists.txt. Herefor, open the CMakeLists.txt
```
gedit CMakeLists.txt
```
Change the pahts at line 19 till 22 to the path to your Astra_SDK direcotry. When changed, build the package:
```
cd ..
catkin_make
```
### This package
The last part you have to install is this package. Go to the source of the catkin_ws and clone this repository:
```
cd catkin_ws/src
git clone https://github.com/wouter1006/Human-tracking-Orbbec-Astra-ROS.git
cd scripts
chmod +x human_tracking.py
chmod +x tf_listener.py
cd ../..
catkin_make
```
## Launch human tracker
To launch the package you have to launch the human_tracking.lauch file. Run the following code to do so:
```
roslaunch human_tracking_package human_tracking.launch
```
