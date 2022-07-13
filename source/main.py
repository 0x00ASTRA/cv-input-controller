import cv2
from cv2 import sqrt
import mediapipe as mp
import time
import numpy as np
# from threading import Threading as thr
import pynput.mouse as pnm


def mainloop():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    mp_draw = mp.solutions.drawing_utils

    p_time = 0
    c_time = 0
    mouse = pnm.Controller()

    while True:
        sucess, img = cap.read()
        img_blk = np.empty(img.shape)
        img_blk.fill(0)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_lndmrks in results.multi_hand_landmarks:
                pressed = False
                for id, lm in enumerate(hand_lndmrks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img_blk, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
                    cv2.putText(img_blk, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                    if id == 8:
                        index_pos = (cx,cy)
                        mouse.position = index_pos
                        index_x = cx
                        index_y = cy
                    if id == 4:
                        thumb_pos  = (cx, cy)
                        thumb_x = cx
                        thumb_y = cy 
                
                    # print(id, cx, cy)q
                # print(mouse.position)
                distance = sqrt(((thumb_x - index_x)**2) + ((thumb_y - index_y)**2))
                # print('Distance: ' + str(distance))
                if distance[0] < 40 and pressed == False:
                    print('CONDITION 1')
                    mouse.press(pnm.Button.left)
                    pressed = True
                if pressed == True and distance[0] > 40:
                    print('CONDITION 2')
                    mouse.release(pnm.Button.left)
                    pressed = False
                mp_draw.draw_landmarks(img_blk, hand_lndmrks, mp_hands.HAND_CONNECTIONS)
                          

        c_time = time.time()
        fps = 1/(c_time - p_time)
        p_time = c_time
        
        cv2.putText(img_blk,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)q
        cv2.imshow('img', img_blk)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    mainloop()
