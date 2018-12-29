#import cv2
#import pyocr
#
#_THRESHOLD_VALUE = 185
#_MAX_VALUE = 255
#
#img = cv2.imread("sample.jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#ret,threshold = cv2.threshold(gray, _THRESHOLD_VALUE, _MAX_VALUE, cv2.THRESH_BINARY)
#threshold = cv2.bitwise_not(threshold)
#
#cv2.imwrite("threshold.jpg", threshold)
#
#tools = pyocr.get_available_tools()
#tool = tools[0]
#
#number = tool.image_to_string(
#    threshold,
#    lang="jpn" #lang="spl2n"
#)

#---
import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r"E:/PgLang/Python/Tesseract-OCR/tesseract.exe"

_THRESHOLD_VALUE = 185
_MAX_VALUE = 255

def main():
    img = cv2.imread("sample.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray.jpg", gray)

    if not exists_any_player_in_image(gray):
        print(0)
        return

    ret,threshold = cv2.threshold(gray, _THRESHOLD_VALUE, _MAX_VALUE, cv2.THRESH_BINARY)
    threshold = cv2.bitwise_not(threshold)

    cv2.imwrite("threshold.jpg", threshold)

    img = Image.fromarray(threshold)
    number = pytesseract.image_to_string(img, lang="spl2n", config="--psm 7")

    print(number)

def exists_any_player_in_image(grayscaled_numpy_array):
    """スペシャル使用回数を示す真っ白いピクセルが存在したら、プレイヤーが存在すると判断する"""
    w, h = grayscaled_numpy_array.shape

    for h_pos in range(0, h):
        for w_pos in range(0, w):
            pixel_value = grayscaled_numpy_array.item(w_pos, h_pos)

            if pixel_value > 240:
                return True

    return False

if __name__ == "__main__":
    main()
