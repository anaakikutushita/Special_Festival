import unittest
import cv2

import process_image

class Test_ImageResizer(unittest.TestCase):
    def setUp(self):
        self.orig_size_image = cv2.imread("unittest_resource/Issues/1/same_size.jpg")
        self.larger_image = cv2.imread("unittest_resource/Issues/2/larger.png")
        self.smaller_image = cv2.imread("unittest_resource/Issues/3/smaller.jpg")

    def test_get_resized_image(self):
        """#1, #2, #3"""

        orig_h, orig_w, orig_c = self.orig_size_image.shape
        resizer = process_image.ImageResizer()

        imgs = [self.orig_size_image, self.larger_image, self.smaller_image]
        for img in imgs:
            new_img = resizer.get_resized_image(img)
            new_h, new_w, new_c = new_img.shape
            self.assertEqual(new_h, orig_h)
            self.assertEqual(new_w, orig_w)

class Test_UsingTimesCalclator(unittest.TestCase):
    def test_get_number_inside_image(self):
        """#4 ~ #7"""
        

if __name__ == '__main__':
    unittest.main()
