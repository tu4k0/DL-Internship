from django.urls import path
from .views import *

urlpatterns = [
    path('', getETHBlockchainInfo, name='ETHBlockchainInfo'),
    path('/Block Info', getETHBlockInfo, name='ETHBlockInfo'),
]