# -*- coding: utf-8 -*-
import unittest
import cv2

import process_image
from Utility.general_opencv_image_processing import AllJpgImageImporterInsideFolder

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

        # 4
        expected_num = 3
        img4 = cv2.imread("unittest_resource/Issues/4/region1.jpg")
        calclator = process_image.UsingTimesCalclator(img4)
        num = calclator._get_number_inside_image(img4)
        self.assertEqual(num, expected_num)

        # 5
        expected_num = [x for x in range(11)]
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/5")
        img_list5 = importer.get_image_list_jpg()
        num_list = []
        for img5 in img_list5:
            num = calclator._get_number_inside_image(img5)
            num_list.append(num)
        print(num_list)
        print(expected_num)
        for var in range(0, 11):
            self.assertEqual(num_list[var], expected_num[var])

        # 6
        expected_num = 0
        img6 = cv2.imread("unittest_resource/Issues/6/0.jpg")
        calclator = process_image.UsingTimesCalclator(img6)
        num = calclator._get_number_inside_image(img6)
        self.assertEqual(num, expected_num)

        # 7
        expected_num = 6+4+7+2+1+10+3+3
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/7")
        img_list7 = importer.get_image_list_jpg()
        using_times = 0
        for img7 in img_list7:
            num = calclator._get_number_inside_image(img7)
            using_times += num
        self.assertEqual(using_times, expected_num)

        # 8
        expected_num = 4+0+0+0+9+0+0+0
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/8")
        img_list8 = importer.get_image_list_jpg()
        using_times = 0
        for img8 in img_list8:
            num = calclator._get_number_inside_image(img8)
            using_times += num
        self.assertEqual(using_times, expected_num)


if __name__ == '__main__':
    unittest.main()