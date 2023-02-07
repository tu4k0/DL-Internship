from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib import messages
from main.services.blockchain.blockchain_interface import *

from .forms import *
from .models import *


def getBlockchainInfo(request):
    if request.method == 'GET':
        if not request.GET.get('node_url'):
            form = ETHNode()
            return render(request, 'main/BlockchainInfo.html', {'form': form})
        else:
            if str(request.GET.get('node_url')).find('infura') == 0 or str(request.GET.get('node_url')).find('ganache') == 0:
                return HttpResponseNotFound('<h1>Bitcoin monitoring form</h1>')
            else:
                form = ETHNode(data=request.GET or {})
                ethNode = EthBlockchain(request.GET.get('node_url'))
                blockchain = 'ETH'
                if ethNode.status:
                    response = render(request, 'main/BlockchainInfo.html', {'ethNode': ethNode, 'form': form,
                                                                                'ethNode.getBlockchainInfo': ethNode.getBlockchainInfo(), 'blockchain': blockchain})
                    response.set_cookie('provider_url', ethNode.nodeUrl)
                    response.set_cookie('status', ethNode.status)
                    ethInfo = list(ethNode.getBlockchainInfo().__dict__.keys())
                    for value in ethInfo:
                        response.set_cookie(value, ethNode.getBlockchainInfo().__dict__.get(value))
                    return response
                if not ethNode.status:
                    return HttpResponseNotFound('<h1>Error 500: Node not found/connected</h1>')
    if request.method == 'POST':
        form = ETHNode(data=request.GET or {})
        ethNode = EthBlockchain(request.GET.get('node_url'))
        provider_url = request.COOKIES.get('provider_url')
        blockNumber = request.COOKIES.get('blockNumber')
        price = request.COOKIES.get('price')
        protocol = request.COOKIES.get('protocol')
        chainId = request.COOKIES.get('chainId')
        hashrate = request.COOKIES.get('hashrate')
        mining = request.COOKIES.get('mining')
        maxFee = request.COOKIES.get('maxFee')
        info = ETHBlockchainInfo(node=provider_url, blockNumber=blockNumber, price=price, protocol=protocol,
                                 id_chain=chainId, hashrate=hashrate, mining=mining, maxFee=maxFee)
        info.save()
        messages.success(request, 'ETH statistics successfully saved in Database')
        return render(request, 'main/BlockchainInfo.html', {'ethNode': ethNode, 'form': form, 'ethNode.getBlockchainInfo': ethNode.getBlockchainInfo()})
    else:
        form = ETHNode()
    return render(request, 'main/BlockchainInfo.html', {'form': form})


def getETHBlockInfo(request):
    if request.method == 'POST':
        block_number = request.POST['block_number']
        ethNode = EthBlockchain(request.COOKIES.get('provider_url'))
        if str(block_number).isalpha():
            return HttpResponseNotFound('<h1>Error 515: Entered block number invalid</h1>')
        if int(block_number) > ethNode.web3.eth.get_block_number():
            return HttpResponseNotFound('<h1>Error 510: Entered block number not exist</h1>')
        else:
            if ethNode.status == True:
                block = ethNode.web3.eth.get_block(int(block_number))
                block_info = dict(block)
                block_hash = block_info.get('hash').hex()
                prev_block_hash = block_info.get('parentHash').hex()
                timestamp = block_info.get('timestamp')
                size = block_info.get('size')
                miner = block_info.get('miner')
                difficulty = block_info.get('difficulty')
                nonce = int(block_info.get('nonce').hex(), 16)
                txcount = int(ethNode.web3.eth.get_block_transaction_count(int(block_number)))
                txroot = block_info.get('transactionsRoot').hex()
                context = {'block_number': block_number, 'block_hash': block_hash,
                           'prev_block_hash': prev_block_hash, 'timestamp': timestamp, 'size': size, 'miner': miner,
                           'difficulty': difficulty, 'nonce': nonce, 'txcount': txcount, 'txroot': txroot}
                return render(request, 'main/ETHBlockInfo.html', context)
            else:
                return HttpResponseNotFound('<h1>Error 500: Node not found/connected</h1>')
    return render(request, 'main/ETHBlockInfo.html')
