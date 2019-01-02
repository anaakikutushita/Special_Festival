"""discord botで使用するメインプログラム"""
# -*- coding: utf-8 -*-
import datetime

# 画像処理用
import cv2
import process_image

# ダウンロード用
import urllib.request
import sys

# エラーレポート用
import logging
LOGGER = logging.getLogger('discord')
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
HANDLER.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(HANDLER)

# discord用
import asyncio
import discord

CLIENT = discord.Client()
MESSAGE_URL_HEAD = 'https://discordapp.com/channels/'
SERVER_ID = '520060780087869472' #スペシャル祭り杯サーバーのID
#CHANNEL_ID = '520061986898313216' #リザルト画像を送信するチャンネルのID(本番)
CHANNEL_ID = '526950365887987722' #リザルト画像を送信するチャンネルのID(テスト)

# Gsheets用
import process_gsheets

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('------')

@CLIENT.event
async def on_message(message):
    #botはこのチャンネルの中にのみ反応・書き込みする
    target_channel = CLIENT.get_channel(int(CHANNEL_ID))

    # botは次の条件を全て満たした場合のみ作動する
    # 1：target_channel内に送信されたメッセージである
    # 2：bot以外からのメッセージである
    # 3：メッセージに添付ファイルが含まれている
    if not ((message.channel == target_channel) \
            and (message.author != CLIENT.user) \
            and (message.attachments)):
        return

    url = message.attachments[0].url
    # ヘッダーをFireFoxに偽装して正常にアクセス可能にする
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }
    request = urllib.request.Request(url=url, headers=headers)

    # アクセス開始
    await target_channel.send('提出記録を処理しています……')
    attached_data = urllib.request.urlopen(request).read()

    # 添付ファイルを一度保存する
    now = datetime.datetime.now()
    file_name = "saved_attachments/{0:%Y%m%d%H%M%S}.jpg".format(now)
    with open(file_name, mode="wb") as f:
        f.write(attached_data)

    # cv2で添付ファイルを読み込みなおす。画像解析でスペシャル回数などを取得
    img = cv2.imread(file_name)
    detecter = process_image.SpecialWeaponUsingTimesDetecter(img)
    result_array = detecter.get_player_num_and_using_times_array()

    # 送信者IDを追加（配列の先端）
    result_array.insert(0, "#" + str(message.author.discriminator))

    # メッセージの固有URLを末尾に追加
    ids = [SERVER_ID, CHANNEL_ID, str(message.id)]
    connected_id = "/".join(ids)
    message_url = MESSAGE_URL_HEAD + connected_id
    result_array.append(message_url)

    # 取得できた情報をスプレッドシートに書き込む
    succeeded = False
    recorder = process_gsheets.ResultArrayDataRecorder(result_array)
    succeeded = recorder.record()

    if succeeded:
        await target_channel.send('記録は正常に処理されました！')
    else:
        # エラーが出たら運営にメンションを飛ばす。その後手動で回避する
        # 手動で処理するにあたって、どのメッセージでエラーが出たのか埋め込みで分かるようにする
        # descriptionにエラーの原因も載せられたら嬉しい
        embed = discord.Embed(
            title='この画像が自動処理できませんでした。', \
            description='', \
            colour=0x3498db
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_image(url=url)

        await target_channel.send('記録の自動処理に失敗しました。 <@193700834305900544> が手動で処理するのをお待ちください。', embed=embed)

token = "NTI2OTIyODM5MTAyNTg2ODgw.DwMWtA.zqPa3JlZS3Oq1kUxpwAzVIVUoOo"
CLIENT.run(token)
