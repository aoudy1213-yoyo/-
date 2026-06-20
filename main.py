from linebot.models import TextSendMessage # 記得補上這個 import

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text
    
    # 1. 處理澆水指令
    if msg == "澆水":
        if user_id not in ADMIN_IDS:
            return
        # 執行澆水邏輯...
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="收到！系統已開始執行澆水程序。")
        )
        
    # 2. 處理詢問狀態的指令 (新增的部分)
    elif msg == "植物狀態":
        # 這裡未來可以串接你的感測器數據
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="目前植物狀態：濕度 65%，土壤水分正常，狀況良好！")
        )
        
    # 3. 處理其他無效指令
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我不明白您的意思，請輸入「澆水」或「植物狀態」。")
        )
