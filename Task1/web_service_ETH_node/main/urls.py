from django.urls import path
from .views import *

urlpatterns = [
    path('', getBlockchainInfo, name='BlockchainInfo'),
    path('/Block Info', getETHBlockInfo, name='ETHBlockInfo'),
]