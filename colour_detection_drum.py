import cv2 as cv
from play import play_drum
from play import display_drum


max_value = 255
max_value_H = 360 // 2
low_H = 90
low_S = 85
low_V = 140
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


cap = cv.VideoCapture(0)
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)


pause = False


while True:
    

    # to get feed from pc's webcam
    ret, frame = cap.read()
    # print(frame.shape)
    # frame = cv.resize(frame, (1280, 960))

    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))


    # construct a closing kernel and apply it to the thresholded image
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (45, 15))
    closed = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed = cv.erode(closed, None, iterations = 1)
    closed = cv.dilate(closed, None, iterations = 1)

    # Find contours
    contours, _ = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area < 500:
            continue

        
        (x,y),radius = cv.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv.circle(frame,center,radius,(0,255,0),2)
        cv.circle(frame, center, radius=3, color=(0, 0, 255), thickness=-1)

        cv.putText(frame, str(int(x)) + ", " + str(int(y)), (int(x),int(y)-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)


    # frame = display_drum(frame)
    # play_drum(x,y)

    # Check if the currently playing sound has finished
    # for i in range(len(playing_channels)):
    #     if playing_channels[i] and not playing_channels[i].get_busy():
    #         playing_channels[i] = None
        

    cv.imshow(window_capture_name, frame)
    cv.imshow(window_detection_name, closed)

    key = cv.waitKey(30)

    if key == ord('q'):
        break

    