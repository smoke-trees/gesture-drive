# Gesture-drive
An autonomous vehicle solution for people who are physically challenged, calibrates limb angle to drive steering wheel and operate pedals. Made by team Smoketrees for SIH 2020 and Mercedes Benz Hack 2020.

<span class="c11 c20"></span>

<span class="c11 c20"></span>

# Download Entire Project: [link](https://drive.google.com/folderview?id=1HREBvGL-ueK6oai9B22IkoWd7Gd94VQY)
# Requirements:

*   <span class="c12">[Python 2](https://www.google.com/url?q=https://www.python.org/downloads/release/python-272/&sa=D&ust=1578845012132000)</span><span class="c10">and</span> <span class="c12">[Python 3](https://www.google.com/url?q=https://www.python.org/downloads/release/python-381/&sa=D&ust=1578845012133000)</span><span class="c11 c10"> </span>
*   <span class="c12">[OpenVINO Toolkit](https://www.google.com/url?q=https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_windows.html%23Install-Core-Components&sa=D&ust=1578845012133000)</span><span class="c11 c10"> (For Inference Speedup)</span>
*   <span class="c12">[ROS](https://www.google.com/url?q=https://www.ros.org/install/&sa=D&ust=1578845012133000)</span><span class="c11 c10">  (For Simulation on Ubuntu)</span>
*   <span class="c12">[Catkin wokspace](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)</span><span class="c11 c10">  (For settin up ROS)</span>
*   <span class="c12">[Gazebo ROS](http://gazebosim.org/tutorials?tut=ros_installing&cat=connect_ros)</span><span class="c11 c10">  (Simulation Environment)</span>

<span class="c5"></span>

# Dataset Used:

<span class="c12">[CMU Perception Computing Lab’s OpenPose Hand Keypoint Dataset](https://www.google.com/url?q=http://domedb.perception.cs.cmu.edu/handdb.html&sa=D&ust=1578845012133000)</span>

<span class="c11 c27"></span>

# Machine Learning Models:

*   <span class="c12">[Hand Keypoint Detection Model](https://www.google.com/url?q=https://drive.google.com/open?id%3D1i8cahIVGcG52EDCr1s2y8hNNnDctcG_n&sa=D&ust=1578845012133000)</span><span class="c11 c10"> (Google Drive, download and keep in model/ folder)</span>

*   <span class="c12">[Gesture Detection Model](https://www.google.com/url?q=https://drive.google.com/open?id%3D1k4i21ckAwomgV0HOYhn4NaeOswJJpPQ-&sa=D&ust=1578845012134000)</span><span class="c11 c10"> (Google Drive)</span>
*   <span class="c11 c10">Drowsiness and Emotion Detection Model (Present in Project Files)</span>

<span class="c11 c20"></span>

# SUBPROJECTS:

*   <span class="c12">[Angle and Gesture Detection Project](https://www.google.com/url?q=https://drive.google.com/drive/folders/1HREBvGL-ueK6oai9B22IkoWd7Gd94VQY?usp%3Dsharing&sa=D&ust=1578845012134000)</span>
*   <span class="c11 c15">ROS Integration</span>
*   <span class="c11 c15">Drowsiness and Emotion Detection</span>


<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

# ANGLE AND GESTURE DETECTION PROJECT:

<span class="c3"></span>

<span class="c21">Pre-requisites:</span>

*   <span class="c17">Download</span> <span class="c12">[Angle and Gesture Detection Project](https://www.google.com/url?q=https://drive.google.com/drive/folders/1HREBvGL-ueK6oai9B22IkoWd7Gd94VQY?usp%3Dsharing&sa=D&ust=1578845012135000)</span>
*   <span class="c3">Install Python 3 and the requirements for the project</span>

<span class="c3"></span>

<span class="c24 c21">Training:</span>

*   <span class="c3">Record video of the gesture you want to feed into the model using the video_recorder.py</span>
*   <span class="c3">Run the handPoseVideo.py to create embeddings of the recorded video</span>
*   <span class="c3">Run the classifier.py to to create an XGBoost Classifier of all the saved embeddings for detecting gestures.</span>

<span class="c3"></span>

<span class="c21 c24">Usage:</span>

*   <span class="c3">Run rotator.py to simulate a steering wheel which rotates according to the angle received.</span>
*   <span class="c3">Run shifter.py to simulate changing of gear, indicator etc. according to the gesture received.</span>
*   <span class="c3">Run gesture_predict.py to start a camera feed or read a recorded video to detect the angle and gesture and send them to rotator.py and shifter.py</span>
*   <span class="c3">All these communications are done using sockets.</span>
*   <span class="c3">Run angler.py if you just wish to view the angle of your hand.</span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

# ROS INTEGRATION:

<span class="c3">Steps to run:</span>

*   <span class="c3">> Initialize OPENVINO environment using the command:-</span>
<span class="c3">source /opt/intel/openvino/bin/setupvars.sh</span>

*   <span class="c3">>Make sure to add the commands :</span>
<span class="c3">source /opt/ros/kinetic/setup.bash</span>
<span class="c3">source ~/gesture_ros/gesture_ws/devel/setup.bash</span>
<span class="c3">In your bash file. If not then add them, close the terminal and</span>

*   <span class="c3">> cd into gesture_ros/ folder</span>

*   <span class="c3">> Run app.py from the command line using the following command:-</span>
<span class="c3">python3  app.py -m “model/pose_iter_102000.xml” -d “GPU”</span>
<span class="c3">-d is and optional requirement</span>

*   <span class="c3">>Open another terminal:-</span>
<span class="c3">Run the file named keypoint_ros.py using the following command</span>
<span class="c3">rosrun test keypoint_ros.py</span>

*   <span class="c3">> In another terminal window run the file named velocity_mapper.py</span>

*   <span class="c3">> Open a new terminal window and launch an empty world in gazebo:</span>
<span class="c3">roslaunch gazebo_ros empty_world.launch</span>

*   <span class="c3">> In another new terminal type the command</span>
<span class="c3">roslaunch m2wr_description spawn.launch</span>

*   <span class="c3">> Try out the project by holding your palm in front of the laptop at different angles. The two wheeled bot will move according to your arm gestures.</span>

<span class="c3"></span>

<span class="c3"></span>

<span class="c3"></span>

# EMOTION AND DROWSINESS DETECTION SUBPROJECT:

*   <span class="c3"> If running emotion detection type:</span>
<span class="c3">                        python emotions_sleepiness.py</span>
<span class="c3">(Please be aware of [dlib](dlib.net) setup)</span>

<span class="c3"></span>

<span class="c3"></span>
