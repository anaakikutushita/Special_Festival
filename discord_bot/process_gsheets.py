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
WRITING_SHEET = workbook.get_worksheet(len(worksheet_list)-1)
ROUND_SHEET = workbook.get_worksheet(0)
TEAM_SHEET = workbook.get_worksheet(1)

# discord_idを書き込む列番号を取得
DISCORD_ID_COL = WRITING_SHEET.find('discord_id').col

# プレイヤー数を書き込む列番号の配列を取得
WRITING_TARGET_COL = [
    0, #0という値は取得しないが、インデックスを参照するのが1～3のためダミーで入れておく
    WRITING_SHEET.find('s1_pn').col,
    WRITING_SHEET.find('s2_pn').col,
    WRITING_SHEET.find('s3_pn').col
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
    values_list = WRITING_SHEET.col_values(DISCORD_ID_COL)
    print(values_list)

class ResultArrayDataRecorder():
    def __init__(self, result_array):
        self._result_array = result_array

    def record(self):
        """受け取った情報をスプレッドシートに書き込む"""
        row = self._get_writing_row_number()
        
        #[0],つまりdiscord_idを書き込む列番号は固定
        WRITING_SHEET.update_cell(row, DISCORD_ID_COL, self._result_array[0])

        #[1],つまりローマ字のステージ名から、スペシャル回数などを書き込む列番号を取得
        target_col = self._get_writing_col_number(self._result_array[1])

        writing_list = self._result_array[2:]
        for i, val in enumerate(writing_list):
            #あとは順番に書き込む
            col = i + target_col
            WRITING_SHEET.update_cell(row, col, val)

        self._mark_as_reference_record(row, self._result_array[0])

        return True

    def _get_writing_row_number(self):
        return get_writing_row_number(self._result_array[0])

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

    def _mark_as_reference_record(self, recording_row, discord_id):
        """
        結果を記録したとき、そのチームが勝ち上がりでない場合は「順位」列の式を削除して「参考」という文字列に置き換える
        チーム登録していない場合も同様
        """
        #discord_idから参加状況を取得する。"o"以外の場合は参考記録にする
        target_row = 1
        try:
            target_row = TEAM_SHEET.find(discord_id).row
        except gspread.exceptions.CellNotFound: #参加チーム一覧に載っていない場合
            target_row = 1 #絶対にoが書いてない行
        
        target_col = 4 #参加状況が書いてあるのは4列目で固定
        status = TEAM_SHEET.cell(target_row, target_col).value

        if status != "o":
            WRITING_SHEET.update_cell(recording_row, 1, "参考")

def get_writing_row_number(discord_id):
    target_row = 0
    # これから書き込む #0000 という値が既に存在する場合はその行をセット
    try:
        cell = WRITING_SHEET.find(discord_id)
        target_row = cell.row
    except:
        # 存在しない場合は例外が発生するので、列を上から探索して最初にブランクになる行をセット
        target_row = get_first_blank_row_number(DISCORD_ID_COL)

    return target_row

def get_first_blank_row_number(col_num):
    # 行1から12まで詰まっている場合、要素数12の配列になる。
    # 新規行を取得するにはlenを調べて+1すればよい
    values_list = WRITING_SHEET.col_values(col_num)
    return len(values_list) + 1

class RankReader():
    def read(self, discord_id) -> int:
        row = get_writing_row_number(discord_id)
        # 順位を記録しているのは1列目で固定
        rank = WRITING_SHEET.cell(row, 1).value
        # 順位にはint以外も入ってくることがあるが、例外が発生するのはOK
        return int(rank)

def get_rule_and_stages():
    round_num_col = 1
    values_list = ROUND_SHEET.col_values(round_num_col)
    latest_round_row = len(values_list)
    row_list = ROUND_SHEET.row_values(latest_round_row)
    return f'ルール：{row_list[1]}\r\nステージ：\r\n①⇒{row_list[2]}\r\n②⇒{row_list[3]}\r\n③⇒{row_list[4]}'

if __name__ == "__main__":
    main()
