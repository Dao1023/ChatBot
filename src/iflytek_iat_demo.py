from . import iflytek_iat_api

def run():
    Ws_Param = iflytek_iat_api.Ws_Param()
    return Ws_Param.run()