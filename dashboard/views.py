import ast
import os
import datetime
from django.shortcuts import redirect, render
# import requests
from intelliTrade.config import *
from django.shortcuts import render
from intelliTrade.config import api_key
import subprocess
from .models import Watchlist
import plotly.offline as opy
import plotly.graph_objs as go
from newsapi import NewsApiClient

streamControl = None
wlStreamControl = None


#Home page
def home(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session:
        newsapi = NewsApiClient(api_key='693a4d6974254e0d901e46d85e304df7')
        # articles = {}
        # response = requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=693a4d6974254e0d901e46d85e304df7")
        # if response.status_code == 200:
        #     articles = response.json()['articles']
        articles = newsapi.get_everything(q='trading OR stock OR finance OR market OR investment OR share',
                                    sources='google-news-in,the-hindu,the-times-of-india',
                                    language='en',
                                    from_param=(datetime.datetime.now()).strftime("%Y-%m-%d"),
                                    to=(datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
                                    sort_by='relevancy')['articles']
        
        return render(request, 'home.html', {'name' : request.session['name'], 'clientId' : request.session['clientId'], 'articles' : articles})
    else:
        return render(request, 'error.html')



#Watchlist page
def watchlist(request, viewSymbol=None):
    global streamControl, wlStreamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session:
        list = Watchlist.objects.filter(clientId = request.session['clientId']).order_by('symbol').values()
        if viewSymbol == None and len(list) > 0:
            viewSymbol = list[0]['symbol']

        if viewSymbol != None:
            viewToken = Watchlist.objects.filter(clientId = request.session['clientId'], symbol = viewSymbol).values_list('token')
            getTokens = Watchlist.objects.values('token')
            allTokens = []
            for token in getTokens:
                allTokens.append(token['token'])

            connect = {
                'AUTH_TOKEN' : request.session['jwtToken'],
                'CLIENT_CODE' : request.session['clientId'],
                'API_KEY' : api_key,
                'FEED_TOKEN' : request.session['feedToken'],
            }
            quote = { 
                'correlation_id' : "abc123", 
                'action' : 1, 
                'mode' : 3, 
                'token_list' : [{
                    "exchangeType": 1, 
                    "tokens": [viewToken[0][0]],
                }]
            }
            userWatchlist = {
                'correlation_id' : "abc123", 
                'action' : 1, 
                'mode' : 3, 
                'token_list' : [{
                    "exchangeType": 1, 
                    "tokens": allTokens,
                }]
            }
            
            with open('connect', 'w') as details:
                details.write(str(connect))
            with open('quote', 'w') as details:
                details.write(str(quote))
            with open('userWatchlist', 'w') as details:
                details.write(str(userWatchlist))
            
            historicDataParams = {
                'exchange' : 'NSE',
                'symboltoken' : viewToken[0][0],
                'interval' : 'ONE_DAY',
                'fromdate' : (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d %H:%M"),
                'todate' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            # print(historicDataParams)
            historicData = smartApi.getCandleData(historicDataParams)['data']
            date, o, h, l, c = [], [], [], [], []
            for row in historicData:
                date.append(row[0])
                o.append(row[1])
                h.append(row[2])
                l.append(row[3])
                c.append(row[4])
            layout = go.Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width = 1120,
                height = 700,
            )
            figure = go.Figure(data=[go.Candlestick(x=date,open=o, high=h,low=l, close=c)], layout=layout)
            divCandle = opy.plot(figure, auto_open=False, output_type='div')
            
            nearbyDataParams = {
                'exchange' : 'NSE',
                'symboltoken' : viewToken[0][0],
                'interval' : 'ONE_HOUR',
                'fromdate' : (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M"),
                'todate' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            nearbyData = smartApi.getCandleData(nearbyDataParams)['data']
            date, c = [], []
            for row in nearbyData:
                date.append(row[0])
                c.append(row[4])
            figure = go.Figure(layout=layout)
            scatter = go.Scatter(x=date, y=c, mode='lines', name=viewSymbol)
            figure.add_trace(scatter)
            divLine = opy.plot(figure, auto_open=False, output_type='div')

            streamControl = subprocess.Popen(['python3', 'stream.py'])
            subprocess.Popen(['python3', 'manage.py', 'collectstatic'])
            # wlStreamControl = subprocess.Popen(['python3', 'wlStream.py'])
            return render(request, 'watchlist.html', {'name' : request.session['name'], 'clientId' : request.session['clientId'], 'list' : list, 'viewSymbol' : viewSymbol, 'divCandle': divCandle, 'divLine': divLine, 'tkn' : request.session['feedToken'][::-1], 'viewToken' : viewToken[0][0]})
        else:
            return render(request, 'watchlist.html', {'name' : request.session['name'], 'clientId' : request.session['clientId'], 'list' : list})
    else:
        return render(request, 'error.html')



def rgOrder(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session and request.method == "POST":
        orderType = request.POST.get('ordertype')
        if orderType is None:
            orderType = "LIMIT"
        else:
            orderType = "MARKET"
        orderparams = {
            "variety" : "NORMAL",
            "tradingsymbol" : request.POST.get('tradingsymbol'),
            "symboltoken" : request.POST.get('symboltoken'),
            "transactiontype" : request.POST.get('transactiontype'),
            "exchange" : "NSE",
            "ordertype" : orderType,
            "producttype" : "MARGIN",
            "duration" : "DAY",
            "price" : request.POST.get('price'),
            "quantity" : request.POST.get('quantity'),
        }
        # print(request.POST.get('ordertype'), request.POST.get('producttype'))
        smartApi.placeOrder(orderparams)
        return redirect('getWatchlist', viewSymbol=request.POST.get('tradingsymbol'))
    else:
        return render(request, 'error.html')

def slOrder(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session and request.method == "POST":
        orderType = request.POST.get('ordertype')
        if orderType is None:
            orderType = "STOPLOSS_LIMIT"
        else:
            orderType = "STOPLOSS_MARKET"
        orderparams = {
            "variety" : "STOPLOSS",
            "tradingsymbol" : request.POST.get('tradingsymbol'),
            "symboltoken" : request.POST.get('symboltoken'),
            "transactiontype" : request.POST.get('transactiontype'),
            "exchange" : "NSE",
            "ordertype" : orderType,
            "producttype" : "MARGIN",
            "duration" : "DAY",
            "price" : request.POST.get('price'),
            "quantity" : request.POST.get('quantity'),
        }
        # print(request.POST.get('ordertype'), request.POST.get('producttype'))
        smartApi.placeOrder(orderparams)
        return redirect('getWatchlist', viewSymbol=request.POST.get('tradingsymbol'))
    else:
        return render(request, 'error.html')



#Holdings page
def holdings(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session:
        holding = smartApi.holding()
        if holding['data'] is not None:
            data = sorted(holding['data'], key=lambda x: x['tradingsymbol'])
        #with open('static/assets/holdings', 'r') as f:
        #    data = ast.literal_eval(f.read())
        auth = {
            'Authorization' : request.session['jwtToken'],
            'apikey' : api_key
        }
        return render(request,'holdings.html', {'data' : data, 'auth' : auth, 'name' : request.session['name'], 'clientId' : request.session['clientId']})
    else:
        return render(request, 'error.html')



#Orders page
def orders(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session:
        book = smartApi.orderBook()['data']
        #book = []
        #with open('static/assets/orderBook', 'r') as f:
        #    book = ast.literal_eval(f.read())
        orderBook, tradeBook, crOrders = [] , [] , []
        if book is not None:
            for i in book:
                if i['status'] == 'open':
                    orderBook.append(i)
                elif i['status'] == 'complete':
                    tradeBook.append(i)
                else:
                    crOrders.append(i)
        # tradeBook = smartApi.tradeBook()
        # print(orderBook['data'])
        # print(tradeBook)

        return render(request, 'orders.html', {'name' : request.session['name'], 'clientId' : request.session['clientId'], 'orderBook' : orderBook, 'tradeBook' : tradeBook, 'crOrders' : crOrders})
    else:
        return render(request, 'error.html')



#Account page
def account(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session:
        userProfile = smartApi.getProfile(request.session['refreshToken'])
        print(userProfile)
        return render(request, 'account.html', {'name' : request.session['name'], 'clientId' : request.session['clientId'], 'userProfile' : userProfile['data']})
    else:
        return render(request, 'error.html')



#Signout Logic
def signout(request):
    global streamControl, wlStreamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if wlStreamControl is not None:
        wlStreamControl.terminate()
        wlStreamControl = None
    try:
        if os.path.exists('static/users/'+request.session['feedToken'][::-1]+'_stream'):
            os.remove('static/users/'+request.session['feedToken'][::-1]+'_stream')
        if 'clientId' in request.session:
            smartApi.terminateSession(request.session['clientId'])
            del request.session['jwtToken']
            del request.session['feedToken']
            del request.session['clientId']
            del request.session['name']
            del request.session['refreshToken']
    except:
        return render(request, 'error.html')
    return redirect('signin')



#To add a stock to watchlist
def addToWatchlist(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session:
        if request.method == "POST" and 'token' in request.POST and 'symbol' in request.POST:
            clientId = request.session['clientId']
            token = request.POST.get('token')
            symbol = request.POST.get('symbol')
            print(clientId, token, symbol)
            if Watchlist.objects.filter(clientId = clientId, token = token, symbol = symbol).exists():
                return redirect('getWatchlist', viewSymbol=symbol)
            list = Watchlist(clientId = clientId, token = token, symbol = symbol)
            list.save()
            return redirect('getWatchlist', viewSymbol=symbol)
    else:
        return render(request, 'error.html')
    


#To delete a stock from watchlist
def doWatchlist(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session and request.method == "POST":
        if 'deleteId' in request.POST:
            id = request.POST.get('deleteId')
            list = Watchlist.objects.get(id=id)
            list.delete()
        elif 'viewSymbol' in request.POST:
            symbol = request.POST.get('viewSymbol')
            return redirect('getWatchlist', viewSymbol=symbol)
        return redirect('watchlist')
    else:
        return render(request, 'error.html')
    

#To cancel an order
def cancelOrder(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session and request.method == "POST":
        variety, orderid = '', ''
        if 'NORMAL' in request.POST:
            variety = 'NORMAL'
            orderid = request.POST.get('NORMAL')
        elif 'STOPLOSS' in request.POST:
            variety = 'STOPLOSS'
            orderid = request.POST.get('STOPLOSS')
        cancelParams = {
            'variety' : variety,
            'orderid' : orderid,
        }
        print(cancelParams)
        return redirect('orders')
    else:
        return render(request, 'error.html')
    
#To modify an order
def modifyOrder(request):
    global streamControl
    if streamControl is not None:
        streamControl.terminate()
        streamControl = None
    if 'clientId' in request.session and request.method == "POST":
        variety = request.POST.get('variety')
        orderid = request.POST.get('orderid')
        ordertype = ''
        if(variety == 'NORMAL'):
            if 'ordertype' not in request.POST:
                ordertype = 'LIMIT'
            else:
                ordertype = 'MARKET'
        elif(variety == 'STOPLOSS'):
            if 'ordertype' not in request.POST:
                ordertype = 'STOPLOSS_LIMIT'
            else:
                ordertype = 'STOPLOSS_MARKET'
        # ordertype = request.POST.get('ordertype')
        producttype = request.POST.get('producttype')
        duration = "DAY"
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        tradingsymbol = request.POST.get('tradingsymbol')
        symboltoken = request.POST.get('symboltoken')
        exchange = "NSE"

        modifyParams = {
            'variety' : variety,
            'orderid' : orderid,
            'ordertype' : ordertype,
            'producttype' : producttype,
            'duration' : duration,
            'price' : price,
            'quantity' : quantity,
            'tradingsymbol' : tradingsymbol,
            'symboltoken' : symboltoken,
            'exchange' : exchange,
        }
        print(modifyParams)
        return redirect('orders')
    else:
        return render(request, 'error.html')