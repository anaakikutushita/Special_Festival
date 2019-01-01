"""受け取った情報をGsheetsに書き込むためのプログラム"""
# -*- coding: utf-8 -*-

# Gsheets用
import json
import gspread
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials
#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('../auth/Special-Festival-453b5819ef42.json', scope)
#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1aWJ4qOF6-LHhtlO7Ev9EUk2st4-6lBUnMuGsODT7FaE'

############################################################
#書き込み先のシートは常に「一番右端のシート」となる。ラウンド終了ごとに新しいワークシートを手動で追加すること。
############################################################
workbook = gc.open_by_key(SPREADSHEET_KEY)
worksheet_list = workbook.worksheets()
TARGET_WORK_SHEET = workbook.get_worksheet(len(worksheet_list)-1)

class ResultArrayDataRecorder():
    def __init__(self, result_array):
        self._result_array = result_array

    def record(self):
        """受け取った情報をスプレッドシートに書き込む"""
        for i, val in enumerate(self._result_array):
            #最初に書き込む列が8であり、順に書き込むだけだからこうしてる
            #そのうち修正が必要
            col = i + 8
            TARGET_WORK_SHEET.update_cell(2, col, val)
        
        return True

