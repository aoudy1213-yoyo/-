import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        # 使用官方 SDK 處理，它會自動處理驗證邏輯
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        # 這裡就是關鍵：遇到解析錯誤時直接回傳 OK，不讓程式崩潰
        print(f"Error: {e}")
        return 'OK'
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 你的機器人邏輯寫在這裡
    pass

if __name__ == "__main__":
    app.run()
