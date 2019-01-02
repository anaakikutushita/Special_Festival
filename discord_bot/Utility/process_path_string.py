"""ファイルパスに対する操作を担うモジュール"""
# -*- coding: utf-8 -*-

import os.path

def get_file_name_without_extension(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]
