import cv2
import mediapipe as mp
import time
from play import play_drum
from play import display_drum


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# For webcam input:
cap = cv2.VideoCapture(0)


# Font and color for FPS display
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_color = (255, 0, 0)  # Red color

# Initialize FPS counter
start_time = time.time()
fps_count = 0
fps = 0

x,y=0,0

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        sw, sh = image.shape[1], image.shape[0]

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                x, y = hand_landmarks.landmark[8].x*sw, hand_landmarks.landmark[8].y*sh

                cv2.circle(image, (int(x), int(y)), 10, (0, 0, 255), -1)

                play_drum(x,y)
                
        
        # Calculate and display FPS
        elapsed_time = time.time() - start_time
        fps_count += 1

        if elapsed_time >= 1:  # Update FPS every second
            fps = fps_count
            fps_count = 0
            start_time = time.time()

        # Display FPS in the top right corner
        text_size, _ = cv2.getTextSize(str(fps), font, font_scale, 1)
        text_origin = (image.shape[1] - text_size[0], text_size[1])
        cv2.putText(image, str(fps), text_origin, font, font_scale, font_color, 1, cv2.LINE_AA)


        image = display_drum(image)
        


        cv2.imshow('MediaPipe Hands', image)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
