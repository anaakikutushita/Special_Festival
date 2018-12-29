# -*- coding: utf-8 -*-
"""画像処理をするときに汎用的に使えるコードをまとめたモジュール"""

import glob
import cv2

class AllJpgImageImporterInsideFolder():
    """特定のフォルダ内に存在する全ての画像ファイルのフルパスを取得する"""
    def __init__(self, image_folder_path):
        #あとで、フォルダの区切り文字とか末尾の文字を揃える処理が必要になるはず
        #今のところは「スラッシュ1文字区切り」「フォルダパスの最後にスラッシュが入っている」条件で決め打ちする
        self._image_folder_path = image_folder_path

    def get_numpy_array_image_list_jpg(self):
        """フォルダ内の.jpg拡張子のみ取得"""
        return self._get_numpy_array_image_list("*.jpg")

    def get_image_file_path_list_jpg(self):
        """フォルダ内の.jpg拡張子のみ取得"""
        return self._get_image_file_path_list("*.jpg")

    def get_numpy_array_image_list_png(self):
        """フォルダ内の.png拡張子のみ取得"""
        return self._get_numpy_array_image_list("*.png")

    def _get_image_file_path_list(self, ext):
        """
        拡張子が一致する画像ファイルのフルパスのリストを返す。
        extには "*.jpg" などを指定する。
        "*.*" を指定した場合、 jpg, png, gif, bmp, ico, svg, tiff の7種まで対応
        """
        image_file_path_list = glob.glob(self._image_folder_path + ext)

        return image_file_path_list

    def _get_numpy_array_image_list(self, ext):
        """
        拡張子が一致する画像のnumpy.arrayのリストを返す。
        extには "*.jpg" などを指定する。
        "*.*" を指定した場合、 jpg, png, gif, bmp, ico, svg, tiff の7種まで対応
        """
        image_file_path_list = self._get_image_file_path_list(ext)
        
        img_list = []
        for image_file_path in image_file_path_list:
            img = cv2.imread(image_file_path)
            img_list.append(img)

        return img_list
