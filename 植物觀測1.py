from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# --- 設定區 (長期記憶中的規則) ---
# 這是你之前提供的管理員 ID，我已將其寫入白名單
ADMIN_IDS = ["U52d8acc19e5942939b3f5cfd8437df9c"] 

is_watering = False       # 狀態鎖：防止多人重複觸發
last_water_time = 0       # 記錄上次澆水時間
COOLDOWN_SECONDS = 3600   # 冷卻時間 1 小時

# 模擬澆水執行函式 (未來會改為對 ESP32 發送請求)
def execute_watering():
    global is_watering
    print("【系統】開始執行澆水程序...")
    is_watering = True
    
    # 這裡未來會放入發送 HTTP 請求給 ESP32 的邏輯
    # 例如: requests.get("http://你的ESP32_IP/water")
    time.sleep(3) # 模擬澆水 3 秒
    
    is_watering = False
    print("【系統】澆水程序結束，已解鎖。")

# --- LINE Webhook 路由 ---
@app.route("/callback", methods=['POST'])
def callback():
    global last_water_time
    
    # 取得 LINE 傳來的訊息內容
    body = request.json
    event = body['events'][0]
    user_id = event['source']['userId']
    message_text = event['message']['text']

    # 只有當訊息為「澆水」時才觸發邏輯
    if message_text == "澆水":
        
        # 1. 權限檢查 (白名單)
        if user_id not in ADMIN_IDS:
            return jsonify({"status": "error", "message": "權限不足，僅限管理員操作。"}), 403

        # 2. 狀態鎖檢查
        if is_watering:
            return jsonify({"status": "error", "message": "系統正在澆水中，請勿重複觸發。"}), 429
        
        # 3. 冷卻時間檢查
        if time.time() - last_water_time < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - (time.time() - last_water_time))
            return jsonify({"status": "error", "message": f"冷卻中，請 {remaining} 秒後再試。"}), 429

        # 4. 執行澆水 (使用執行緒背景處理)
        last_water_time = time.time()
        threading.Thread(target=execute_watering).start()
        
        return jsonify({"status": "success", "message": "澆水指令已啟動，系統將澆水 3 秒。"}), 200

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
