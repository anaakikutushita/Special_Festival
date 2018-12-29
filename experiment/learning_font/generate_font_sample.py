import cv2
_THRESHOLD_VALUE = 215
_MAX_VALUE = 255

img = cv2.imread('learning_font.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,threshold = cv2.threshold(gray, _THRESHOLD_VALUE, _MAX_VALUE, cv2.THRESH_BINARY)
threshold = cv2.bitwise_not(threshold)

cv2.imwrite('thresh.jpg', threshold)