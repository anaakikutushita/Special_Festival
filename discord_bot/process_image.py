
"""
画像解析から記録の保存まで全てを担うモジュール。source.pyから利用することが前提。
"""
# -*- coding: utf-8 -*-

# 丸め処理
from decimal import Decimal, ROUND_DOWN

# 数字認識
import re
import cv2
import pytesseract
from PIL import Image
from Utility.general_opencv_image_processing import AllJpgImageImporterInsideFolder

pytesseract.pytesseract.tesseract_cmd = r"E:/PgLang/Python/Tesseract-OCR/tesseract.exe"

class SpecialWeaponUsingTimesDetecter():
    """
    報告画像を解析し、スプレッドシートに記録する
    """
    def __init__(self, result_image_numpy_array):
        self._result_image_numpy_array = result_image_numpy_array

    def get_player_num_and_using_times_array(self):
        """
        画像解析し、プレイヤー数と個別のスペシャル回数を認識する。
        """
        # 画像の解像度を統一
        resizer = ImageResizer()
        self._result_image_numpy_array = resizer.get_resized_image(self._result_image_numpy_array)

        # 画像の形式が合っているか判定する
        # ルールとステージが大会の指定に沿っているか判定する
        # タイムスタンプが大会の進行に沿っているか判定する
        checker = ValidImageChecker(self._result_image_numpy_array)
        if not checker.is_valid_image:
            return False

        # 部屋に参加しているプレイヤー数を求める
        counter = PlayerNumCounter(self._result_image_numpy_array)
        player_num = counter.count()

        # プレイヤー1から8までそれぞれのスペシャル回数を求める
        detecter = UsingTimesDetecter(self._result_image_numpy_array)
        using_times_array = detecter.get_all_players_using_times_array()

        result_array = using_times_array
        result_array.insert(0, player_num)
        return result_array

class ImageResizer():
    """
    システム上、画像の大きさが統一されてないとうまく処理できない。そのために拡縮する。
    拡縮しないと、画像の特定領域を解析するといった処理が行えなくなる。
    """
    def get_resized_image(self, result_image):
        """
        OpenCVのライブラリで単純に拡縮
        サイズは決め打ち
        """
        return cv2.resize(result_image, (1024, 640))

class ValidImageChecker():
    """
    送信された画像がそもそも規定に則ったものかどうかを判定する
    現状は未実装なので常にTrueを返す
    """
    def __init__(self, result_image):
        self.img = result_image

    def is_valid_image(self):
        """判定関数"""
        return True

class PlayerNumCounter():
    """
    リザルト画像に載っているプレイヤー数を求める
    未実装
    """
    def __init__(self, result_image):
        self.whole_image = result_image

    def count(self):
        """プレイヤー数を計算する"""
        area_array_list = self._get_list_of_cropped_narrow_areas_from_whole_image()
        player_num = self._get_player_count(area_array_list)

        return player_num

    def _get_list_of_cropped_narrow_areas_from_whole_image(self):
        """リザルト画像の中で、ウデマエやランクが記されている領域を指定する"""
        pos_dic = {
            'x1':642, 'x2':676,
            'y1_p1':116, 'y2_p1':137,
            'y1_p2':166, 'y2_p2':186,
            'y1_p3':216, 'y2_p3':236,
            'y1_p4':266, 'y2_p4':286,
            'y1_p5':391, 'y2_p5':412,
            'y1_p6':441, 'y2_p6':462,
            'y1_p7':491, 'y2_p7':512,
            'y1_p8':541, 'y2_p8':562,
        }

        img_list = []

        for var in range(1, 9): #これでvarは1～8の間繰り返される
            narrow_area = self.whole_image[eval("pos_dic['y1_p" + str(var) + "']"):eval("pos_dic['y2_p" + str(var) + "']"),
                                           pos_dic['x1']:pos_dic['x2']]
            img_list.append(narrow_area)

        return img_list
    
    def _get_player_count(self, img_list):
        """img_listのうち、プレイヤーあり判定されたものの数をカウントする"""
        player_counter = 0
        for img in img_list:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if exists_any_player_in_image(gray):
                player_counter += 1

        return player_counter

class UsingTimesDetecter():
    """リザルト画像から、スペシャル発動回数を認識する。合計はしない"""
    def __init__(self, result_image):
        self.whole_image = result_image

    def get_all_players_using_times_array(self):
        """
        プレイヤー位置1から位置8まで、それぞれのスペシャル回数を画像から読み取って配列にする。
        プレイヤーがいない位置のスペシャル回数は0になる
        """
        area_array_list = self._get_list_of_cropped_narrow_areas_from_whole_image()

        using_times_array = []
        for area in area_array_list:
            using_times_array.append(self._get_number_inside_image(area))

        return using_times_array

    def _get_list_of_cropped_narrow_areas_from_whole_image(self):
        """リザルト画像の中で、スペシャル発動数が記されている領域を指定する"""
        pos_dic = {
            'x1':926, 'x2':956,
            'y1_p1':113, 'y2_p1':133,
            'y1_p2':163, 'y2_p2':183,
            'y1_p3':213, 'y2_p3':233,
            'y1_p4':263, 'y2_p4':283,
            'y1_p5':403, 'y2_p5':423,
            'y1_p6':454, 'y2_p6':474,
            'y1_p7':504, 'y2_p7':524,
            'y1_p8':554, 'y2_p8':574,
        }

        img_list = []

        for var in range(1, 9): #これでvarは1～8の間繰り返される
            narrow_area = self.whole_image[eval("pos_dic['y1_p" + str(var) + "']"):eval("pos_dic['y2_p" + str(var) + "']"),
                                           pos_dic['x1']:pos_dic['x2']]
            img_list.append(narrow_area)

        return img_list

    def _get_number_inside_image(self, narrow_area_numpy_array):
        """画像内に含まれる数字を識別して返す"""
        #img = self._get_grayscaled_numpy_array_object(narrow_area_numpy_array)
        img = cv2.cvtColor(narrow_area_numpy_array, cv2.COLOR_BGR2GRAY)

        if not exists_any_player_in_image(img):
            cv2.imwrite("no_white.jpg", img)
            return 0
        
        img = self._get_thresholded_numpy_array_object(img)
        img = self._get_inversed_numpy_array_object(img)
        number = pytesseract.image_to_string(img, lang="spl2n", config="--psm 7")
        number = self._get_remains_int_or_zero(re.sub(r'\D', '', number))
        return number

    def _get_grayscaled_numpy_array_object(self, numpy_array_image_object):
        """ファイルパスの画像をグレースケール変換して取得する"""
        gray = cv2.cvtColor(numpy_array_image_object, cv2.COLOR_BGR2GRAY)
        return gray

    def _get_thresholded_numpy_array_object(self, numpy_array_image_object):
        """画像を読み取り、白黒の2値化処理を行う"""
        threshold_value = 185
        max_value = 255

        ret,threshold = cv2.threshold(numpy_array_image_object, threshold_value, max_value, cv2.THRESH_BINARY)
        return threshold

    def _get_inversed_numpy_array_object(self, numpy_array_image_object):
        """ネガポジ反転した画像を取得する。主に二値化処理を済ませた画像の入力を想定。"""
        threshold = cv2.bitwise_not(numpy_array_image_object)
        return threshold

    def _get_image_object(self, numpy_array_image_object):
        """numpy.arrayのオブジェクトをimageに変換する"""
        img = Image.fromarray(numpy_array_image_object)
        return img

    def _get_remains_int_or_zero(self, int_suspended_str):
        """intに変換できる値はそのまま返し、それ以外は0を返す"""
        try:
            num = int(int_suspended_str)
        except:
            return 0

        return num

def exists_any_player_in_image(grayscaled_numpy_array):
    """真っ白いピクセルが存在したら、プレイヤーが存在すると判断する"""
    w, h = grayscaled_numpy_array.shape

    for h_pos in range(0, h):
        for w_pos in range(0, w):
            pixel_value = grayscaled_numpy_array.item(w_pos, h_pos)

            if pixel_value > 230:
                return True

    return False

if __name__ == '__main__':
    print('source.pyから実行してください')
