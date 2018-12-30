import cv2
import process_image

#img = cv2.imread("unittest_resource/Issues/11/4_12_2.jpg")
img = cv2.imread("unittest_resource/Issues/11/8_18_1.jpg")
detecter = process_image.SpecialWeaponUsingTimesDetecter(img)
result_num = detecter.get_player_num_and_using_times_array()
print("result_num is " + str(result_num))