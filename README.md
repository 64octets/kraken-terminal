# kraken-terminal

A terminal utility written in Python that interacts with Bitcoin Exchange Kraken.com API.

## Screenshot
![alt tag](http://i.imgur.com/qwjT9jo.png)

## Description

Provides a quicker way for kraken.com users to interact with their account. All of the operations as of the moment are read-only.

## Installation

### Prerequisites

* [veox/python2-krakenex](https://github.com/veox/python2-krakenex)
  * Clone it and run `python ./setup.py install`.

### API Key

Go to your kraken.com account settings and generate an API key with the following permissions:
* Query Funds
* Query Open Orders & Trades
* Query Closed Orders & Trades
* Query Ledger Entries

### Install

Clone this project, then put your API Key and Private Key in kraken.key.

## Usage

`python kraken-terminal.py` then follow instructions.

## Todo
Suggestions for improvement:
- [ ] Support for multiple pairs
- [ ] Handle orders made in currency rather than btc
- [ ] Funding Information
- [ ] Ledger
- [ ] Error Handling
  * Handle network, API Key and query.
