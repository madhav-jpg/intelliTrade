from django.shortcuts import render,redirect
from SmartApi import SmartConnect
import pyotp
from intelliTrade.config import token, smartApi

def signin(request):    
    if 'clientId' in request.session:
        return redirect('/dashboard')
    totp=pyotp.TOTP(token).now()
    try:
        if request.method == "POST":
            clientId = request.POST.get('clientId')
            pwd = request.POST.get('password')
            response = smartApi.generateSession(clientId, pwd, totp)
            request.session['jwtToken'] = response['data']['jwtToken']
            request.session['feedToken'] = response['data']['feedToken']
            request.session['refreshToken'] = response['data']['refreshToken']
            request.session['clientId'] = clientId
            request.session['name'] = response['data']['name']          
            return redirect('/dashboard')
    except:
        pass
    return render(request, 'signin.html')