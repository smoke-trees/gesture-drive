import cv2

img = cv2.imread('north_east.png')
import cv2
import math


protoFile1 = "hand_keypoint/testing.prototxt"
weightsFile1 = "hand_keypoint/hand/pose_iter_102000.caffemodel"

nPoints = 22
POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9], [9, 10], [10, 11], [11, 12],
              [0, 13], [13, 14], [14, 15], [15, 16], [0, 17], [17, 18], [18, 19], [19, 20]]

img = cv2.imread('straight.png')
threshold = 0.2

frameWidth = img.shape[1]
frameHeight = img.shape[0]

aspect_ratio = frameWidth / frameHeight

inHeight = 368
inWidth = int(((aspect_ratio * inHeight) * 8) // 8)

net = cv2.dnn.readNetFromCaffe(protoFile1, weightsFile1)

inpBlob = cv2.dnn.blobFromImage(img, 1.0 / 255, (inWidth, inHeight),
                                    (0, 0, 0), swapRB=False, crop=False)

net.setInput(inpBlob)

output = net.forward()
points = []

for i in range(nPoints):
    # confidence map of corresponding body's part.
    probMap = output[0, i, :, :]
    probMap = cv2.resize(probMap, (frameWidth, frameHeight))

    # Find global maxima of the probMap.
    minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

    if prob > threshold:
        cv2.circle(img, (int(point[0]), int(point[1])), 6, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
        cv2.putText(img, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, .8,
                    (0, 0, 255), 2, lineType=cv2.LINE_AA)

        # Add the point to the list if the probability is greater than the threshold
        points.append((int(point[0]), int(point[1])))
    else:
        points.append(None)

# Draw Skeleton
print(points)
#cv2.imshow('windowname', img)

x1,y1 = points[14]
x2,y2 = points[15]
angle = math.atan((y2-y1)/(x2-x1))
print(math.degrees(angle))
