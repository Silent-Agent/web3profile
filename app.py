import streamlit as st
from web3 import Web3

# Title
st.title("Blockchain Portfolio Dashboard")

# Inject MetaMask connection using JavaScript
st.markdown("""
<script>
    async function connectMetaMask() {
        if (typeof window.ethereum !== "undefined") {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            document.getElementById("wallet_address").value = account;
        } else {
            alert("MetaMask not detected. Please install MetaMask!");
        }
    }
</script>
""", unsafe_allow_html=True)

# Input field to capture wallet address
wallet_address = st.text_input("Wallet Address", key="wallet_address", disabled=True)
st.button("Connect MetaMask", on_click=lambda: st.script("connectMetaMask()"))

# Web3 Connection
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if wallet_address:
    # Display wallet address
    st.success(f"Connected wallet: {wallet_address}")

    # Fetch ETH balance
    balance = web3.eth.get_balance(wallet_address)
    eth_balance = web3.fromWei(balance, "ether")
    st.metric("Ethereum Balance", f"{eth_balance:.4f} ETH")

    # Placeholder: Token and Portfolio data
    st.info("Token portfolio coming soon...")

def fetch_token_balance(contract_address, wallet_address, abi):
    # Load token contract
    contract = web3.eth.contract(address=contract_address, abi=abi)
    decimals = contract.functions.decimals().call()
    symbol = contract.functions.symbol().call()
    balance = contract.functions.balanceOf(wallet_address).call()
    return balance / (10 ** decimals), symbol

token_contracts = [
    {"name": "Tether (USDT)", "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"},
    {"name": "Dai (DAI)", "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F"}
]

erc20_abi = [...]  # Use the standard ERC-20 ABI

if wallet_address:
    token_balances = []
    for token in token_contracts:
        balance, symbol = fetch_token_balance(token["address"], wallet_address, erc20_abi)
        token_balances.append({"name": token["name"], "balance": balance, "symbol": symbol})

    # Display token balances in a table
    st.write("### Token Portfolio")
    st.table(token_balances)

import requests

ETHERSCAN_API_KEY = "Your Etherscan API Key"
etherscan_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&apikey={ETHERSCAN_API_KEY}"

response = requests.get(etherscan_url)
if response.status_code == 200:
    transactions = response.json()["result"]
    st.write("### Recent Transactions")
    st.table(transactions[:10])  # Display the first 10 transactions
else:
    st.error("Failed to fetch transactions")
