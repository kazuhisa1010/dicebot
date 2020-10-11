# -*- coding: utf-8 -*-

# インストールした discord.py を読み込む
import discord
import os
import json
from dice import Dice

if __name__ == "__main__": 
    json_read = open('config.json','r')
    botmessage = json.load(json_read)['messages']
    # .bash_profileに記述
    TOKEN = os.environ.get("DISCORD_TOKEN")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")

    # 接続に必要なオブジェクトを生成
    client = discord.Client()

    # 起動時に動作する処理
    @client.event
    async def on_ready():

        print(botmessage['login'])
        # 起動したらhelpメッセージを送信
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('\n'.join((botmessage['start']+botmessage['help'])))

    # メッセージ受信時に動作する処理
    @client.event
    async def on_message(message):
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        
        # 「dice」から発言を始めたらサイコロを回す
        if message.content.startswith('dice'): 
            dice = Dice()
            botText = dice.selectRollType(message.content)
            
            await message.channel.send(botText)

        # 「create」から発言を始めたらキャラシ用のダイスを回す
        if message.content.startswith('dice'): 
            return

        # 「help」と発言したら、ヘルプを出す
        if message.content == 'help':
            await message.channel.send(botmessage['help'])

    # Botの起動とDiscordサーバーへの接続
    client.run(TOKEN)