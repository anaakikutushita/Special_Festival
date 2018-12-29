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
        """#4 ~ #8"""

        # 4
        expected_num = 3
        img4 = "unittest_resource/Issues/4/region1.jpg"
        img = cv2.imread(img4)
        calclator = process_image.UsingTimesCalclator(img)
        num = calclator._get_number_inside_image(img)
        self.assertEqual(num, expected_num)

        # 5
        expected_num = [x for x in range(11)]
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/5/")
        img_list5 = importer.get_numpy_array_image_list_jpg()
        print('img_list5 :')
        print(img_list5)
        num_list = []
        for img5 in img_list5:
            num = calclator._get_number_inside_image(img5)
            num_list.append(num)
        print('num_list : ')
        print(num_list)
        print('expected_num : ')
        print(expected_num)
        for var in range(0, 11):
            self.assertEqual(num_list[var], expected_num[var])

        # 6
        expected_num = 0
        img6 = "unittest_resource/Issues/6/0.jpg"
        img6 = cv2.imread(img6)
        calclator = process_image.UsingTimesCalclator(img6)
        num = calclator._get_number_inside_image(img6)
        self.assertEqual(num, expected_num)

        # 7
        expected_num = 6+4+7+2+1+10+3+3
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/7/")
        img_list7 = importer.get_numpy_array_image_list_jpg()
        using_times = 0
        for img7 in img_list7:
            num = calclator._get_number_inside_image(img7)
            using_times += num
        self.assertEqual(using_times, expected_num)

        # 8
        expected_num = 4+0+0+0+9+0+0+0
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/8/")
        img_list8 = importer.get_numpy_array_image_list_jpg()
        using_times = 0
        for img8 in img_list8:
            num = calclator._get_number_inside_image(img8)
            print(num)
            using_times += num
        self.assertEqual(using_times, expected_num)

    def test_calc(self):
        """# 9"""
        expected_nums = [
            4+3+3+2+0+1+2+2,
            6+3+3+2+2+5+6+4,
            5+3+4+4+4+7+1+1,
            7+2+4+3+2+6+1+1,
            5+5+7+3+7+8+4+3,
            2+9+0+2+1+5+2+4,
            3+10+3+1+3+3+4+3,
            4+0+0+0+9+0+0+0
            ]
        
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/9/")
        img_list9 = importer.get_numpy_array_image_list_jpg()
        
        using_times = 0
        using_times_list = []
        for img9 in img_list9:
            calclator = process_image.UsingTimesCalclator(img9)
            num = calclator.calc()
            using_times_list.append(num)

        print('expected_nums')
        print(expected_nums)
        print('using_times_list')
        print(using_times_list)

        for var in range(0, 8):
            self.assertEqual(using_times_list[var], expected_nums[var])

if __name__ == '__main__':
    unittest.main()
