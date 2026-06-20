import os
import time
import threading
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# 從 Render 的環境變數讀取安全金鑰
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

# 管理員清單與狀態鎖
ADMIN_IDS = ["U52d8acc19e5942939b3f5cfd8437df9c"]
is_watering = False
last_water_time = 0
COOLDOWN_SECONDS = 3600

def execute_watering():
    global is_watering
    print("【系統】開始執行澆水程序...")
    is_watering = True
    time.sleep(3)  # 模擬澆水動作
    is_watering = False
    print("【系統】澆水程序結束，已解鎖。")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(message_event=True)
def handle_message(event):
    global last_water_time
    user_id = event.source.user_id
    message_text = event.message.text
    
    if message_text == "澆水":
        if user_id not in ADMIN_IDS:
            line_bot_api.reply_message(event.reply_token, {"type": "text", "text": "權限不足，僅限管理員操作。"})
            return
        if is_watering:
            line_bot_api.reply_message(event.reply_token, {"type": "text", "text": "系統正在澆水中，請勿重複觸發。"})
            return
        if time.time() - last_water_time < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - (time.time() - last_water_time))
            line_bot_api.reply_message(event.reply_token, {"type": "text", "text": f"冷卻中，需 {remaining} 秒後再試。"})
            return
            
        last_water_time = time.time()
        threading.Thread(target=execute_watering).start()
        line_bot_api.reply_message(event.reply_token, {"type": "text", "text": "澆水指令已啟動！系統澆水 3 秒。"})

if __name__ == "__main__":
    app.run()
