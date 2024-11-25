from web3 import Web3

def init_web3(infura_url):
    return Web3(Web3.HTTPProvider(infura_url))

def fetch_eth_balance(web3, address):
    balance = web3.eth.get_balance(address)
    return web3.fromWei(balance, "ether")
