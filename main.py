import os
import time
import threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# 設定 LINE API
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

# 管理員清單
ADMIN_IDS = ["U52d8acc19e5942939b3f5cfd8437df9c"]
is_watering = False
last_water_time = 0
COOLDOWN_SECONDS = 3600

def execute_watering():
    global is_watering
    is_watering = True
    time.sleep(3) 
    is_watering = False

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception:
        return 'OK'
    return 'OK'

@handler.add(message_event=True)
def handle_message(event):
    global last_water_time
    user_id = event.source.user_id
    if event.message.text == "澆水":
        if user_id not in ADMIN_IDS:
            return
        if is_watering or (time.time() - last_water_time < COOLDOWN_SECONDS):
            return
        last_water_time = time.time()
        threading.Thread(target=execute_watering).start()

if __name__ == "__main__":
    app.run()
