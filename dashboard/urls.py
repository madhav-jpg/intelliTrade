from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home),
    path('home', views.home, name='home'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist/', views.watchlist),
    path('watchlist/<viewSymbol>', views.watchlist, name='getWatchlist'),
    path('holdings', views.holdings, name='holdings'),
    path('orders', views.orders, name='orders'),
    path('account', views.account, name='account'),
    path('signout', views.signout, name='signout'),
    path('addToWatchlist', views.addToWatchlist, name='addToWatchlist'),
    path('doWatchlist', views.doWatchlist, name='doWatchlist'),
    path('rgOrder', views.rgOrder, name='rgOrder'),
    path('slOrder', views.slOrder, name='slOrder'),
    path('cancelOrder', views.cancelOrder, name='cancelOrder'),
    path('modifyOrder', views.modifyOrder, name='modifyOrder'),
]