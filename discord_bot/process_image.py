
"""
画像解析から記録の保存まで全てを担うモジュール。source.pyから利用することが前提。
"""
# -*- coding: utf-8 -*-

# 丸め処理
from decimal import Decimal, ROUND_DOWN

# 数字認識
import pytesseract
from PIL import Image

# その他画像処理
import cv2

class SpecialWeaponUsingTimesRecorder():
    """
    報告画像を解析し、スプレッドシートに記録する
    """
    def __init__(self, result_image):
        self._result_image = result_image

    def record(self):
        """
        画像解析から記録の保存まで全て行う。
        記録まで成功した場合はTrue、そうでない場合はFalseを返す。
        """
        # 画像の解像度を統一
        resizer = ImageResizer()
        self._result_image = resizer.get_resized_image(self._result_image)

        # 画像の形式が合っているか判定する
        # ルールとステージが大会の指定に沿っているか判定する
        # タイムスタンプが大会の進行に沿っているか判定する
        checker = ValidImageChecker(self._result_image)
        if not checker.is_valid_image:
            return False

        # 部屋に参加しているプレイヤー数を求める
        counter = PlayerNumCounter(self._result_image)
        player_num = counter.count()

        # 全プレイヤーのスペシャル発動数の合計を求める
        calclator = UsingTimesCalclator(self._result_image)
        temp_sp_num = calclator.calc()

        # 8人換算した場合のスペシャル発動数を求める
        converter = UsingTimesConverter()
        using_times = converter.convert(temp_sp_num, player_num)

        # 取得できた情報をスプレッドシートに書き込む

        # 記録が成功したかどうかの結果を返す
        return True

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
        return 2

class UsingTimesCalclator():
    """リザルト画像から、スペシャル発動回数の合計を計算する"""
    def __init__(self, result_image):
        self.whole_image = result_image

    def calc(self):
        """スペシャル発動回数の合計を計算して返す"""
        area_image_list = self._get_list_of_cropped_narrow_areas_from_whole_image()

        using_times = int(0)
        for area in area_image_list:
            using_times += self._get_number_inside_image(area)

        return using_times

    def _get_list_of_cropped_narrow_areas_from_whole_image(self):
        """リザルト画像の中で、スペシャル発動数が記されている領域を指定する"""
        pos_dic = {
            'x1':926, 'x2':961,
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
            narrow_area = self.whole_image[eval("pos_dic['y1_p" + var + "']"):eval("pos_dic['y2_p" + var + "']"),
                                           pos_dic['x1']:pos_dic['x2']]
            img_list.append(narrow_area)

        return img_list

    def _get_number_inside_image(self, narrow_area_image):
        """画像内に含まれる数字を識別して返す"""
        return 1

class UsingTimesConverter():
    """
    スペシャル発動数の合計を8人換算する
    """
    def convert(self, using_times, player_num):
        """スペシャル発動数 / プレイヤー数 * 8 を整数に丸めて返す。小数点以下切り捨て"""
        max_player_num = 8
        integral_value = Decimal('0')

        converted = Decimal(using_times / player_num * max_player_num)
        rounded = converted.quantize(integral_value, rounding=ROUND_DOWN)

        return rounded


if __name__ == '__main__':
    print('source.pyから実行してください')
