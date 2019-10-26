import argparse
import cv2
import numpy as np
from skimage import img_as_bool
from skimage import img_as_ubyte
from skimage.morphology import skeletonize

IMG_HEIGHT = 270
IMG_WIDTH = 480


def adjust_sharpness(imgIn):
    kernel = np.zeros((9, 9), np.float32)
    kernel[4, 4] = 2.0
    boxFilter = np.ones((9, 9), np.float32) / 81.0
    kernel = kernel - boxFilter
    custom = cv2.filter2D(imgIn, -1, kernel)
    return custom

# Argument parsing eye video
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="path to video", )
args = vars(ap.parse_args())

# Recieveing stream and parsing to opencv
#vs = cv2.VideoCapture('http://192.168.43.253:8000/eyel.mjpeg')

# Argument Video Feeding
vs = cv2.VideoCapture(args["video"])

a = 0
while vs is not None:
    a = a + 1
    (grabbed, frame) = vs.read()

    frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
    # print("[INFO] Resizing")
    M = np.ones(frame.shape, dtype="uint8") * 50
    added = cv2.add(frame, M)
    added = cv2.cvtColor(added, cv2.COLOR_BGR2GRAY)
    print("[INFO] Converted from RGB to GRAY for interation=", a)
    added = cv2.flip(added, 0)
    img = cv2.equalizeHist(added)
    # img = cv2.bilateralFilter(img, 20, 12, 12, cv2.BORDER_DEFAULT)
    img = cv2.medianBlur(img, 41)
    # img = cv2.GaussianBlur(img, (17, 17), 3, 3)
    # img = adjust_sharpness(img)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 47, 6)
    img = cv2.GaussianBlur(img, (5, 5), 0, 0)
    rows, cols = img.shape

    pts3 = np.float32([[0, 0], [IMG_WIDTH, 0], [0, IMG_HEIGHT], [IMG_WIDTH, IMG_HEIGHT]])
    pts4 = np.float32(
        [[0, 0], [IMG_WIDTH, 0], [(IMG_WIDTH*0.14), IMG_HEIGHT], [(IMG_WIDTH*0.86), IMG_HEIGHT]])

    M = cv2.getPerspectiveTransform(pts3, pts4)

    img = cv2.warpPerspective(img,M,(IMG_WIDTH,IMG_HEIGHT))

    added = cv2.warpPerspective(added,M,(IMG_WIDTH,IMG_HEIGHT))
    # img = cv2.bitwise_not(img)
    img = img_as_bool(img)
    img = skeletonize(img)
    img = img_as_ubyte(img)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, minDist=1200000, param1=50, param2=6, minRadius=27, maxRadius=62)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            if x > (IMG_WIDTH * 0.3) and (IMG_HEIGHT * 0) < y < (IMG_HEIGHT * 1):
                cv2.circle(added, (x, y), r, (255, 255, 255), 1)
                cv2.rectangle(added, (x - 5, y - 5), (x + 5, y + 5), (255, 255, 255), 1)
                print("[INFO] Computing for (", x, ",", y, ",", r, ")")
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(added, 'x:' + str(x), (20, 20), font, 0.6, (255, 255, 255), 1)
            cv2.putText(added, 'y:' + str(y), (20, 40), font, 0.6, (255, 255, 255), 1)
            cv2.putText(added, 'r:' + str(r), (20, 60), font, 0.6, (255, 255, 255), 1)
    # img = cv2.addWeighted(added, 1, img, 1, 1)
    cv2.imshow("img", img)
    cv2.imshow("Added", added)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
