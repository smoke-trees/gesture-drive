import cv2

input_source = 0
output = "videos/main_testing.avi"
cap = cv2.VideoCapture(input_source)
vid_writer = cv2.VideoWriter(output,cv2.VideoWriter_fourcc('M','J','P','G'), 20, (640,480))


while True:

    _,frame = cap.read()
    vid_writer.write(frame)
    cv2.imshow('Recording...', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break


vid_writer.release()
cap.release()
cv2.destroyAllWindows()
