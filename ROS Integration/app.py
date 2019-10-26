import argparse
import cv2
from inference import Network
import numpy as np
import time
from unitvec import calc_unit_vector
import pickle
import math
import socket
import paho.mqtt.client as mqtt
import signal

gesture_model = pickle.load(open("model/5gestmodelright.pkl", 'rb'))
gesture_model_labels = pickle.load(open("model/5gestmodellabelsright.pkl", 'rb'))

nPoints=22
threshold = 0.1
CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"
GPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libclDNNPlugin.so  "
INPUT_STREAM ="/videos/main_testingaa.avi"

POSE_PAIRS = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]




def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Run inference on an input video")
    # -- Create the descriptions for the commands
    m_desc = "The location of the model XML file"
    i_desc = "The location of the input file"
    d_desc = "The device name, if not 'CPU'"
    ### TODO: Add additional arguments and descriptions for:
    ###       1) Different confidence thresholds used to draw bounding boxes
    ###       2) The user choosing the color of the bounding boxes
    
    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    # -- Create the arguments
    required.add_argument("-m", help=m_desc, required=True)
    #optional.add_argument("-i", help=i_desc, default=INPUT_STREAM)
    optional.add_argument("-d", help=d_desc, default='CPU')
    args = parser.parse_args()
    
    return args


def infer_on_video(args):
    angle_degrees=0
    extension = None
    nn = Network()
    if(args.d=="CPU"):
        extension = CPU_EXTENSION
    else:
        extension = GPU_EXTENSION
    nn.load_model(args.m,args.d,extension)
    shape = nn.get_input_shape()
    
    client = mqtt.Client()
    
    client.connect("localhost", 1883, 60)
    
    
    signal.signal(signal.SIGINT, shutdown)
    
    cap = cv2.VideoCapture(0)
    while(True):
        flag,frame = cap.read()
        t = time.time()
    
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        frameCopy = np.copy(frame)
        aspect_ratio = frameWidth/frameHeight

        inHeight = 368
        inWidth = int(((aspect_ratio*inHeight)*8)//8)
    
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inHeight, inWidth),
                              (0, 0, 0), swapRB=False, crop=False)
        
        #Async Inference        
        nn.async_inference(inpBlob)
        output = nn.extract_outputs()
        
        #Sync Inference
        #output = nn.sync_inference(inpBlob)
        
        points = []
        
        for i in range(nPoints):
            # confidence map of corresponding body's part.
            
            probMap = output[0, i, :, :]
            probMap = cv2.resize(probMap, (frameWidth, frameHeight))
            
            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
    
            if prob > threshold :
                
                points.append((int(point[0]), int(point[1])))
            else :
               points.append(None)
    
            
        
        if(points[14]!=None and points[15]!=None):
            x1, y1 = points[14]
            x2, y2 = points[15]
            if(x1!=None and x2!=None and y1!=None and y2!=None):            
                if((x2-x1)!=0):
                    angle = math.atan((y2 - y1) / (x2 - x1))
                    angle_degrees = math.degrees(angle)
                    
                    print("ANGLE = ", angle_degrees)
                else:
                    angle_degrees = 0
                    print("Improper points recieved")
                
            else:
                angle_degrees = 0
                print("Improper points recieved")
        else:
            angle_degrees = 0
            print("Improper points recieved")
    
        np_embed = np.array(calc_unit_vector(points))
        nx, ny, each = np_embed.shape
        flattened_embed = np_embed.reshape((1, nx * ny * each))
        gesture_pred = gesture_model.predict(flattened_embed)
        
        gesture = gesture_model_labels[gesture_pred.tolist()[0]]
        
        cv2.putText(frame, "Angle = {:.5f} degrees".format(angle_degrees), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8,
                    (255, 50, 0), 2,
                    lineType=cv2.LINE_AA)
    
        cv2.putText(frame, "Gesture = "+gesture, (50, 100), cv2.FONT_HERSHEY_COMPLEX, .8,
                    (255, 50, 0), 2,
                    lineType=cv2.LINE_AA)
        print("Time Taken for frame = {}".format(time.time() - t))
        
        
        cv2.imshow("window",frame)
        client.publish("merce", angle_degrees)
        
        key = cv2.waitKey(1)
        if(key==27):
            
            break

    

def shutdown(signal_num, frame):
	print("Shutting down publisher")
	client.publish("merce", "Q")
	client.disconnect()
	exit()

def main():
    
    
    args = get_args()
    infer_on_video(args)
     
if __name__=="__main__":
	main()
	
