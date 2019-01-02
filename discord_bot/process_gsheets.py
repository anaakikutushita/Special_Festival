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
WRITING_WORK_SHEET = workbook.get_worksheet(len(worksheet_list)-1)
ROUND_SHEET = workbook.get_worksheet(0)

# discord_idを書き込む列番号を取得
DISCORD_ID_COL = WRITING_WORK_SHEET.find('discord_id').col

# プレイヤー数を書き込む列番号の配列を取得
WRITING_TARGET_COL = [
    0, #0という値は取得しないが、インデックスを参照するのが1～3のためダミーで入れておく
    WRITING_WORK_SHEET.find('s1_pn').col,
    WRITING_WORK_SHEET.find('s2_pn').col,
    WRITING_WORK_SHEET.find('s3_pn').col
]

def main():
    # 検索値がシート上になかった場合どうなるのか試したい
    # 結果は、gspread.exceptions.CellNotFound例外が発生する
    # cell = TARGET_WORK_SHEET.find('hoge')
    # row = cell.row
    # col = cell.col
    # print(row)
    # print(col)

    # 列の値を全て取得したとき、どんな配列になるのか試したい
    # 結果は、ブランク以降の要素は格納されない
    values_list = WRITING_WORK_SHEET.col_values(DISCORD_ID_COL)
    print(values_list)

class ResultArrayDataRecorder():
    def __init__(self, result_array):
        self._result_array = result_array

    def record(self):
        """受け取った情報をスプレッドシートに書き込む"""
        row = self._get_writing_row_number()
        
        #[0],つまりdiscord_idを書き込む列番号は固定
        WRITING_WORK_SHEET.update_cell(row, DISCORD_ID_COL, self._result_array[0])

        #[1],つまりローマ字のステージ名から、スペシャル回数などを書き込む列番号を取得
        target_col = self._get_writing_col_number(self._result_array[1])

        writing_list = self._result_array[2:]
        for i, val in enumerate(writing_list):
            #あとは順番に書き込む
            col = i + target_col
            WRITING_WORK_SHEET.update_cell(row, col, val)

        return True

    def _get_writing_row_number(self):
        target_row = 0
        # これから書き込む #0000 という値が既に存在する場合はその行をセット
        try:
            cell = WRITING_WORK_SHEET.find(self._result_array[0])
            target_row = cell.row
        except:
            # 存在しない場合は例外が発生するので、列を上から探索して最初にブランクになる行をセット
            target_row = self._get_first_blank_row_number(DISCORD_ID_COL)

        return target_row

    def _get_writing_col_number(self, stage_name_roman):
        # ローマ字ステージ名から日本語ステージ名を取得
        stage_name = self._get_stage_name_from_roman(stage_name_roman)

        # 日本語ステージ名をスプレッドシートから探索し、現在のラウンドにおけるステージ番号を特定する
        stage_num = self._get_stage_num_from_gspread(stage_name)

        # ステージ番号から、スプレッドシートに書き込む列番号を取得する
        target_col = self._get_target_col_num(stage_num)

        return target_col

    def _get_stage_name_from_roman(self, stage_name_roman):
        stage_names = {
            "battera":"バッテラストリート",
            "bbasu":"Bバスパーク",
            "hokke":"ホッケふ頭",
            "hujitsubo":"フジツボスポーツクラブ",
            "manta":"マンタマリア号",
            "mozuku":"モズク農園",
            "otoro":"ホテルニューオートロ",
            "sumeshi":"スメーシーワールド"
        }
        return stage_names[stage_name_roman]

    def _get_stage_num_from_gspread(self, stage_name):
        #ラウンド数の列から最終行を取得
        #round_num_col = rounds_sheet.find('ラウンド数').col
        #決め打ちでいいのでは
        round_num_col = 1
        values_list = ROUND_SHEET.col_values(round_num_col)
        latest_round_row = len(values_list)

        #最も新しいラウンドの行の値を全て取得
        row_list = ROUND_SHEET.row_values(latest_round_row)

        #配列の中からステージ名を探索
        for i, val in enumerate(row_list):
            if val == stage_name:
                #iは0スタート
                #ステージ1の列番号は3からスタート
                return i + 1 - 2

    def _get_target_col_num(self, stage_num):
        return WRITING_TARGET_COL[stage_num]

    def _get_first_blank_row_number(self, col_num):
        # 行1から12まで詰まっている場合、要素数12の配列になる。
        # 新規行を取得するにはlenを調べて+1すればよい
        values_list = WRITING_WORK_SHEET.col_values(col_num)
        return len(values_list) + 1

if __name__ == "__main__":
    main()
