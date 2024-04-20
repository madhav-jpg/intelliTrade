from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import ast
# print(authenticate.views.AUTH_TOKEN, intelliTrade.config.api_key, authenticate.views.CLIENT_CODE, authenticate.views.FEED_TOKEN)
connect = ''
subscription = ''
with open('connect', 'r') as details:
    connect = ast.literal_eval(details.read())

with open('quote', 'r') as details:
    subscription = ast.literal_eval(details.read())

sws = SmartWebSocketV2(connect["AUTH_TOKEN"], connect["API_KEY"], connect["CLIENT_CODE"], connect["FEED_TOKEN"])

def on_data(wsapp, message):
    if message != b'\x00':
        try:
            # data = str(message).replace("'", '"')
            with open('static/users/'+connect["FEED_TOKEN"][::-1]+'_stream','w') as stream:
                stream.write(str(message).replace("'", '"'))
                stream.close()
        except Exception as e:
            print(e)
    # print(message)
    # close_connection()

def on_open(wsapp):
    # logger.info("on open")
    sws.subscribe(subscription["correlation_id"], subscription["mode"], subscription["token_list"])
    # sws.unsubscribe(correlation_id, mode, token_list1)


def on_error(wsapp, message):
    # logger.error(error)
    print(message)

def on_close(wsapp):
    # logger.info("Close")
    # stream.close()
    pass

def close_connection():
    sws.close_connection()

# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()