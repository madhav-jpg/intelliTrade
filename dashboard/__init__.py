# from SmartApi.smartWebSocketV2 import SmartWebSocketV2
# import authenticate.views
# import dashboard.views
# import intelliTrade.config
# print(authenticate.views.AUTH_TOKEN, intelliTrade.config.api_key, authenticate.views.CLIENT_CODE, authenticate.views.FEED_TOKEN)
# sws = SmartWebSocketV2(authenticate.views.AUTH_TOKEN, intelliTrade.config.api_key, authenticate.views.CLIENT_CODE, authenticate.views.FEED_TOKEN)

# def on_data(wsapp, message):
#     # try:
#     #     with open('../static/stream.txt','w') as stream:
#     #         stream.write(str(message))
#     #         stream.close()
#     # except Exception as e:
#     #     print(e)
#     print(message)
#     # close_connection()

# def on_open(wsapp):
#     # logger.info("on open")
#     sws.subscribe(dashboard.views.correlation_id, dashboard.views.mode, dashboard.views.token_list)
#     # sws.unsubscribe(correlation_id, mode, token_list1)


# def on_error(wsapp, message):
#     # logger.error(error)
#     print(message)

# def on_close(wsapp):
#     # logger.info("Close")
#     # stream.close()
#     pass


# def close_connection():
#     sws.close_connection()


# # Assign the callbacks.
# sws.on_open = on_open
# sws.on_data = on_data
# sws.on_error = on_error
# sws.on_close = on_close

# sws.connect()