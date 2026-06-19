

import requests
from flask import Flask, request, abort

app = Flask(__name__)

# 👑 貼上你的 LINE 權杖密碼 (跟之前一樣)
LINE_TOKEN = "4DUX3hDY+H3E3F3nAqxzEtJoU2xCyTgIOcUxEEo3/6zl3R4sgZoIDGt7GmOJvtyVpOYndZqvHC74TouCs3uYvb VgFOQqWUjymrnUaWSwRihWfUZt2qnsCYpdkREZeAT8LDJ3WK2YTiC5nbpdK+OO8gdB04t89/1O/w1cDnyilFU="

@app.route("/callback", methods=['POST'])
def callback():
    # 接收 LINE 官方傳過來的訊息
    body = request.get_json()
    
    try:
        # 抓取使用者傳來的文字事件
        events = body.get("events", [])
        for event in events:
            if event.get("type") == "message" and event["message"]["type"] == "text":
                user_msg = event["message"]["text"]      # 這是使用者在手機上打的字
                reply_token = event["replyToken"]        # 這是用來回覆的臨時鑰匙
                
                # 判斷關鍵字
                if "查詢植物" in user_msg or "植物" in user_msg:
                    report = "🌱 本地高級植物的即時回報：\n- 土壤濕度：45% (良好)\n- 環境溫度：28°C\n- 日照強度：適中"
                    send_line_reply(reply_token, report)
                else:
                    send_line_reply(reply_token, "🤖 (電腦已讀) ⚠️ 請輸入「查詢植物」測試發送功能。")
                    
    except Exception as e:
        print(f"發生錯誤: {e}")
        
    return 'OK'

# 🚀 負責把回覆訊息射回手機的函式
def send_line_reply(reply_token, text_message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text_message}]
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"回覆狀態碼: {response.status_code}")

if __name__ == "__main__":
    # 讓程式在 5000 Port 監聽網路連線
    app.run(port=5000)
