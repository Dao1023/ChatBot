def speak(text):
    wsParam = Ws_Param(
        APPID = appid,
        APISecret = api_secret,
        APIKey = api_key,
        Text = text
    )
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})