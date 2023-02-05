from django import forms
from .models import *


class AddETHBlockchainInfo(forms.Form):
    node = forms.CharField(max_length=255)
    blockNumber = forms.IntegerField()
    price = forms.IntegerField()
    protocol = forms.IntegerField()
    id_chain = forms.IntegerField()
    hashrate = forms.IntegerField()
    mining = forms.BooleanField()
    maxFee = forms.IntegerField()


class ETHNode(forms.Form):
    node_url = forms.CharField(widget=forms.Textarea(attrs={'cols': 45, 'rows': 1}), label="Enter Node url")
