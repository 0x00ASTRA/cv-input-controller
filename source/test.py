import cv2 as cv
import time

cap = cv.VideoCapture(0)
p_time = 0

while True:
	success, img = cap.read()
	imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	c_time = time.time()
	fps = 1/(c_time - p_time)
	p_time = c_time
	cv.putText(img, f'FPS: {int(fps)}', (20, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
	cv.imshow("TEST", img)
	cv.waitKey(1)

