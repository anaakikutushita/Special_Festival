# discord用
import discord
import asyncio

# ダウンロード用
import urllib.request
import sys

# 画像処理用
import process_image

# エラーレポート用
import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    channel_id_testing = 526950365887987722
    channel_id_production = 520061986898313216

    #botはこのチャンネルの中にのみ反応・書き込みする
    target_channel = client.get_channel(channel_id_testing)

    # botは次の条件を全て満たした場合のみ作動する
    # 1：target_channel内に送信されたメッセージである
    # 2：bot以外からのメッセージである
    # 3：メッセージに添付ファイルが含まれている
    if not ((message.channel == target_channel) \
            and (message.author != client.user) \
            and (message.attachments)):
        return

    url = message.attachments[0].url
    filename = message.attachments[0].filename

    # FireFoxに偽装して正常にアクセス可能にする
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }

    request = urllib.request.Request(url=url, headers=headers)

    # アクセス開始
    await target_channel.send('提出記録を処理しています……')
    succeeded = False

    attached_data = urllib.request.urlopen(request).read()

    with open("saved_attachments/{0}".format(filename), mode="wb") as f:
        f.write(attached_data)

    recorder = process_image.SpecialWeaponUsingTimesRecorder(attached_data)
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
client.run(token)