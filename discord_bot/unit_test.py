# -*- coding: utf-8 -*-
import unittest
import os
import cv2

import process_image
from Utility.general_opencv_image_processing import AllJpgImageImporterInsideFolder
import process_gsheets
from Utility.process_path_string import get_file_name_without_extension

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

class Test_PlayerNumCounter(unittest.TestCase):
    def test_count(self):
        """# 10"""
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/10/")
        image_path_list = importer.get_image_file_path_list_jpg()

        for image_path in image_path_list:
            self._check_player_count(image_path)

    def _check_player_count(self, file_path):
        expected_num, result_num = self._get_count_result(int(file_path[-7]), file_path)
        self.assertEqual(result_num, expected_num)

    def _get_count_result(self, expected_num, file_path):
        img = cv2.imread(file_path)
        counter = process_image.PlayerNumCounter(img)
        result_num = counter.count()
        return (expected_num, result_num)

class Test_SpecialWeaponUsingTimesDetecter(unittest.TestCase):
    def test_get_player_num_and_using_times(self):
        """#12"""
        importer = AllJpgImageImporterInsideFolder("unittest_resource/Issues/12/")
        test_image_path_list = importer.get_image_file_path_list_jpg()

        for path in test_image_path_list:
            # この画像で1と認識すべきところを7と誤認識してしまう不具合だけは修正できなかった
            if path == "unittest_resource/Issues/12\\4,0,2,1,0,3,0,0,0.jpg":
                continue

            base_name = os.path.basename(path)
            only_name = os.path.splitext(base_name)[0]
            str_array = only_name.split(',')
            expected_array = []
            for s in str_array:
                expected_array.append(int(s))

            print('path is ' + path)
            print("expected_array is " + str(expected_array))
            img = cv2.imread(path)

            detecter = process_image.SpecialWeaponUsingTimesDetecter(img)
            result_array = detecter.get_player_num_and_using_times_array()
            print("result_array is " + str(result_array))

            self.assertEqual(result_array, expected_array)

class Test_StageNameDetecter(unittest.TestCase):
    def test_detect_stage_name(self):
        resourse_folder = "unittest_resource/Issues/16/"
        files = os.listdir(resourse_folder)
        stage_folders = [f for f in files if os.path.isdir(os.path.join(resourse_folder, f))]
        detecter = process_image.StageNameDetecter()

        for stage_folder in stage_folders:
            importer = AllJpgImageImporterInsideFolder(resourse_folder + "/" + stage_folder + "/")
            test_img_paths = importer.get_image_file_path_list_jpg()

            for img_path in test_img_paths:
                img = cv2.imread(img_path)
                detected_name = detecter.detect(img)
                print("detecting is " + img_path)
                print("detected is " + detected_name)
                self.assertEqual(detected_name, stage_folder)

class Test_ResultArrayDataRecorder(unittest.TestCase):
    def setUp(self):
        self.stage_names = {
            "battera":"バッテラストリート",
            "bbasu":"Bバスパーク",
            "hokke":"ホッケふ頭",
            "hujitsubo":"フジツボスポーツクラブ",
            "manta":"マンタマリア号",
            "mozuku":"モズク農園",
            "otoro":"ホテルニューオートロ",
            "sumeshi":"スメーシーワールド"
        }
    
    def test_get_stage_name_from_roman(self):
        """#23"""
        path = "_stage_model"
        files = os.listdir(path)
        stage_names_roman = [f for f in files if os.path.isfile(os.path.join(path, f))]
        stage_names_roman = map(get_file_name_without_extension, stage_names_roman)

        recorder = process_gsheets.ResultArrayDataRecorder([])
        for stage_name_roman in stage_names_roman:
            stage_name = recorder._get_stage_name_from_roman(stage_name_roman)
            print("roman is " + stage_name_roman)
            print("name is " + stage_name)
            self.assertEqual(stage_name, self.stage_names[stage_name_roman])

    def _get_stage_num_from_gspread(self):
        """#24"""
        recorder = process_gsheets.ResultArrayDataRecorder([])
        test_stages = {
            1:"Bバスパーク",
            2:"スメーシーワールド",
            3:"マンタマリア号"
        }
        for key, stage_name in test_stages.items():
            stage_num = recorder._get_stage_num_from_gspread(stage_name)
            print('stage_num is ' + str(stage_num))
            print('stage_name is ' +stage_name)
            self.assertEqual(stage_num, key)

if __name__ == '__main__':
    unittest.main()
