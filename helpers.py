#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# This program uses python2-krakenex api package

import krakenex
import os
import pprint
import operator
import webbrowser

# Set default encoding to allow currency symbols
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

DEBUG = False

url = "https://cryptowat.ch/kraken/btceur"
pp = pprint.PrettyPrinter(indent=2)
keyPath = os.path.dirname(os.path.realpath(__file__)) + '/kraken.key'
k = krakenex.API()
k.load_key(keyPath)

###
# Private(?) methods

def _currencyStr(value):
    currencySymbol = "€"
    return currencySymbol + str(round(float(value), 2))

# Converts pairs "XBTEUR" into result property pairs "XXBTZEUR"
def _magicPair(pair):
    o = list(pair)
    o.insert(3, "Z")
    o.insert(0, "X")
    return ''.join(o)

# Takes order string and returns {vol: ..., limit: ...}
def dissectOrder(order):
    o = order.split(' ')
    return { 'vol': o[1], 'limit': o[len(o) - 1] }

def openChart():
    webbrowser.open(url,new="2")
    return { 'txt': "Opening chart in browser..." }

###
# Kraken Queries

# Get Trade Balance (sum of all btc and fiat assets)
def getTradeBalance(asset='ZEUR'):
    if DEBUG: print "\n" + "Querying TradeBalance..."
    q = k.query_private('TradeBalance', {'asset': asset})
    balance = _currencyStr(q['result']['tb'])
    txt = "Trade Balance = %(balance)s" % locals()
    return { 'txt': txt }

def getAccountBalance():
    if DEBUG: print "\n" + "Querying Account Balance..."
    q = k.query_private('Balance')
    btc = q['result']['XXBT']
    eur = _currencyStr(q['result']['ZEUR'])
    txt = "BTC = %(btc)s\n" % locals()
    txt += "EUR = %(eur)s" % locals()
    return { 'txt': txt, 'data': { 'btc': btc, 'eur': q['result']['ZEUR'] } }

# Returns last trade closing value
def getTicker(pair='XBTEUR'):
    if DEBUG: print "\n" + "Querying Ticker..."
    q = k.query_public('Ticker', {'pair': pair})
    high = _currencyStr(q['result'][_magicPair(pair)]['h'][0])
    last = _currencyStr(q['result'][_magicPair(pair)]['c'][0])
    low = _currencyStr(q['result'][_magicPair(pair)]['l'][0])
    txt = "%(pair)s\n\n" % locals()
    txt += "High: %(high)s\n" % locals()
    txt += "Last: %(last)s\n" % locals()
    txt += "Low : %(low)s\n" % locals()
    return { 'txt': txt }

# Returns open orders
def getOrders(includeTrades=False):
    if DEBUG: print "\n" + "Querying Orders..."

    q = k.query_private('OpenOrders', {'trades': includeTrades})
    orders = { 'buy': [], 'sell': [], 'buyNet': 0, 'sellNet': 0 }

    # Parse orders
    for orderKey  in q['result']['open']:
        orderDesc = q['result']['open'][orderKey]['descr']
        orders[orderDesc['type']].append(orderDesc)

        # Calculate net buy value (volume * limit price)
        _order = dissectOrder(orderDesc['order'])
        orders[orderDesc['type'] + 'Net'] += float(_order['vol']) * float(_order['limit'])

    # Sort buy and sell orders in reverse order
    orders['buy'].sort(key=operator.itemgetter('price'), reverse=True)
    orders['sell'].sort(key=operator.itemgetter('price'), reverse=True)

    output = "# Sell Orders (Total: " + str(len(orders['sell'])) + ", Net: " + _currencyStr(orders['sellNet']) + ")\n\n"

    # Output Sell Orders
    for sellOrder in orders['sell']:
        output += sellOrder['order'] + "\n"

    output += "\nEstimate Balance if all sell orders execute = " + _currencyStr(float(getAccountBalance()['data']['eur']) + float(orders['sellNet'])) + '\n'

    output += "\n# Buy Orders (Total: " + str(len(orders['buy'])) + ", Net: " + _currencyStr(orders['buyNet']) + ")\n\n"

    # Output Buy Orders
    for buyOrder in orders['buy']:
        output += buyOrder['order'] + "\n"

    return { 'txt': output }
