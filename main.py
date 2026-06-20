@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        # 接收到的訊息內容
        msg = event.message.text
        
        # 強制輸出到 Log，方便你隨時確認
        print(f"收到訊息: {msg}")
        
        # 決定要回覆什麼
        if "植物狀態" in msg:
            reply_text = "目前植物狀態：濕度 65%，狀況良好！"
        elif "澆水" in msg:
            reply_text = "收到指令！系統正在執行澆水程序..."
        else:
            reply_text = f"機器人已連線！你剛剛說的是：{msg}"
            
        # 回覆訊息
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )
