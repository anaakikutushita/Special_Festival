# coding: utf-8
"""
一枚の画像から指定した領域をトリミングして保存する。
領域は複数指定可能。
保存先は、このソースコードと同じ階層。
ファイル名は実行日時yyyyMMdd-x.jpg
"""

import cv2
import os
from datetime import datetime

def main():
    loopable = True
    image_path_list = []

    while(loopable):
        print('画像のファイルパスを絶対パスで入力')
        path = input('>>>  ')
        if path == 'n':
            loopable = False
            continue

        if path.startswith('"'):
            path = path[1:]

        if path.endswith('"'):
            path = path[:-1]

        if not os.path.isfile(path):
            print('ファイルが存在しません')
            continue

        image_path_list.append(path)
        print('続けてファイルパスを入力。')
        print('全て入力し終わった場合はnを入力')

    print('画像内から切り抜く領域を入力')
    print('入力した領域が画像からはみ出る場合、何も処理しません')

    loopable = True
    area_list = []

    while(loopable):
        area = []

        y1 = input_area_info('y1')

        if y1 == 'n':
            loopable = False
            continue
        
        try:
            y1 = int(y1)
        except:
            print('整数を入力してください')
            continue
        area.append(y1)

        y2 = input_area_info('y2')
        try:
            y2 = int(y2)
        except:
            print('整数を入力してください')
            continue
        area.append(y2)

        x1 = input_area_info('x1')
        try:
            x1 = int(x1)
        except:
            print('整数を入力してください')
            continue
        area.append(x1)

        x2 = input_area_info('x2')
        try:
            x2 = int(x2)
        except:
            print('整数を入力してください')
            continue
        area.append(x2)

        area_list.append(area)
        print('続けて領域を入力。')
        print('全て入力し終わった場合はnを入力')

    print('画像の分割を開始します')
    now = '{0:%Y%m%d%H%M%S}'.format(datetime.now())
    for i, path in enumerate(image_path_list):
        for j, area in enumerate(area_list):
            try:
                img = cv2.imread(path)
                cropped_area = img[area[0]:area[1], area[2]:area[3]]
                cv2.imwrite(now + '-' + str(i) + '-' + str(j) + ".jpg", cropped_area)
            except:
                continue
    print('画像の分割が終了しました')

def input_area_info(pos):
    print(pos + 'を入力')
    return input('>>>  ')

if __name__ == "__main__":
    main()
