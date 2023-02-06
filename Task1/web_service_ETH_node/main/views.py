from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages
from web3 import Web3

from .forms import *
from .models import *


def getETHBlockchainInfo(request):
    if request.method == 'GET':
        if not request.GET.get('node_url'):
            form = ETHNode()
            return render(request, 'main/ETHBlockchainInfo.html', {'form': form})
        else:
            form = ETHNode(data=request.GET or {})
            if form.is_valid():
                provider_url = request.GET.get('node_url')
                w3 = Web3(Web3.HTTPProvider(provider_url))
                status = w3.isConnected()
                if status == True:
                    blockNumber = w3.eth.blockNumber
                    price = w3.eth.gas_price
                    protocol = w3.eth.protocol_version
                    chainId = w3.eth.chain_id
                    hashrate = w3.eth.hashrate
                    mining = w3.eth.mining
                    maxFee = w3.eth.max_priority_fee
                    response = render(request, 'main/ETHBlockchainInfo.html',
                                      {'status': status, 'blockNumber': blockNumber, 'price': price,
                                       'protocol': protocol,
                                       'chainId': chainId, 'hashrate': hashrate, 'mining': mining, 'maxFee': maxFee,
                                       'provider_url': provider_url, 'form': form})
                    response.set_cookie('provider_url', provider_url)
                    response.set_cookie('status', status)
                    response.set_cookie('blockNumber', blockNumber)
                    response.set_cookie('price', price)
                    response.set_cookie('protocol', protocol)
                    response.set_cookie('chainId', chainId)
                    response.set_cookie('hashrate', hashrate)
                    response.set_cookie('mining', mining)
                    response.set_cookie('maxFee', maxFee)
                    return response
                if status == False:
                    return HttpResponseNotFound('<h1>Error 500: Node not found/connected</h1>')
    if request.method == 'POST':
        form = ETHNode(data=request.GET or {})
        provider_url = request.COOKIES.get('provider_url')
        status = request.COOKIES.get('status')
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
        return render(request, 'main/ETHBlockchainInfo.html',
                      {'blockNumber': blockNumber, 'price': price, 'protocol': protocol,
                       'chainId': chainId, 'hashrate': hashrate, 'mining': mining, 'maxFee': maxFee,
                       'provider_url': provider_url, 'form': form, 'status': status})
    else:
        form = ETHNode()
    return render(request, 'main/ETHBlockchainInfo.html', {'form': form})


def getETHBlockInfo(request):
    if request.method == 'POST':
        block_number = int(request.POST['block_number'])
        provider_url = request.COOKIES.get('provider_url')
        w3 = Web3(Web3.HTTPProvider(provider_url))
        latest_block = int(w3.eth.get_block_number())
        if block_number > latest_block:
            return HttpResponseNotFound('<h1>Error 510: Entered block number don`t exist</h1>')
        else:
            status = w3.isConnected()
            if status == True:
                block = w3.eth.get_block(block_number)
                block_info = dict(block)
                block_hash = block_info.get('hash').hex()
                prev_block_hash = block_info.get('parentHash').hex()
                timestamp = block_info.get('timestamp')
                size = block_info.get('size')
                miner = block_info.get('miner')
                difficulty = block_info.get('difficulty')
                nonce = int(block_info.get('nonce').hex(), 16)
                txcount = int(w3.eth.get_block_transaction_count(block_number))
                txroot = block_info.get('transactionsRoot').hex()
                return render(request, 'main/ETHBlockInfo.html', {'block_number': block_number, 'block_hash': block_hash, 'prev_block_hash': prev_block_hash, 'timestamp': timestamp, 'size': size, 'miner': miner, 'difficulty': difficulty, 'nonce': nonce, 'txcount': txcount, 'txroot': txroot})
            else:
                return HttpResponseNotFound('<h1>Error 500: Node not found/connected</h1>')
    return render(request, 'main/ETHBlockInfo.html')