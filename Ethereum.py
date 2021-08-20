from web3 import Web3
from web3.auto import w3
from binascii import hexlify
from Core import *


class Ethereum:
    web3_instance = None
    current_account = None

    def __init__(self, http_provider_url: str = None, pri_key: str = None):
        if http_provider_url is not None:
            self.set_provider(http_provider_url)
        if pri_key is not None:
            self.set_current_account(pri_key)

    @staticmethod
    def get_smart_contract(abi, bytecode=None, address=None):
        if not Web3.isChecksumAddress(address):
            address = Web3.toChecksumAddress(address)
        if address is not None and bytecode is not None:
            return w3.eth.contract(abi=abi, bytecode=bytecode, address=address)
        elif address is not None and bytecode is None:
            return w3.eth.contract(abi=abi, address=address)
        else:
            return w3.eth.contract(abi=abi, bytecode=bytecode)

    def get_fee(self, gas_used=21000):
        gas_price = self.web3_instance.eth.gas_price
        return ((gas_price/10**9)*gas_used)/10**9

    def set_provider(self, url_provider: str):
        self.web3_instance = Web3(Web3.HTTPProvider(url_provider))
        if self.web3_instance.isConnected():
            return {"connected": True}
        else:
            return {"connected": False}

    def check_balance(self, address: str = None):
        if self.current_account is None and address is None:
            raise TFBlockchainError(GET_BALANCE, "Not address given and not account set")
        balance = None
        if address is not None:
            balance = float(self.web3_instance.eth.getBalance(self.web3_instance.toChecksumAddress(address)))
        elif self.current_account is not None:
            balance = float(
                self.web3_instance.eth.getBalance(self.web3_instance.toChecksumAddress(self.current_account.address)))
        return {"amount": self.web3_instance.fromWei(balance, "ether")}

    def create_account(self):
        self.current_account = self.web3_instance.eth.account.create()
        return {"address": self.current_account.address,
                "private-key": self.current_account.privateKey}

    def get_current_account_pri_key(self):
        if self.current_account is None:
            raise TFBlockchainError(SET_ACCOUNT, "Please set an account before try to get a private key... ")
        return {"private-key": hexlify(self.current_account.privateKey).decode()}

    def get_current_account_address(self):
        assert self.current_account is not None
        return {"address": self.current_account.address}

    def set_current_account(self, pri_key: str):
        self.current_account = self.web3_instance.eth.account.privateKeyToAccount(pri_key)
        if self.current_account is None:
            raise TFBlockchainError(SET_ACCOUNT, "Please check your private key and your connection and try again...")
        return {"address": self.current_account.address}

    def transfer(self, amount, to_wallet: str, private_key: str, gas_price: str,
                 from_wallet: str = None, gas_limit: int = 21000):
        if from_wallet is None and self.current_account is None:
            raise TFBlockchainError(TRANSFER, "Please ensure you had gave it to me a valid source address or your are"
                                              "currently working over one account..")
        if not self.web3_instance.isChecksumAddress(to_wallet):
            to_wallet = self.web3_instance.toChecksumAddress(to_wallet)
        nonce = None
        if from_wallet is not None:
            nonce = self.web3_instance.eth.getTransactionCount(from_wallet)
        elif self.current_account is not None:
            nonce = self.web3_instance.eth.getTransactionCount(self.current_account.address)
        tx = {
            'nonce': nonce,
            'to': to_wallet,
            'value': self.web3_instance.toWei(amount, 'ether'),
            'gas': gas_limit,
            'gasPrice': self.web3_instance.toWei(gas_price, 'gwei'),
        }
        signed_tx = self.web3_instance.eth.account.signTransaction(tx, private_key)
        tx_hash = self.web3_instance.eth.sendRawTransaction(signed_tx.rawTransaction)
        del private_key
        return {"id": self.web3_instance.toHex(tx_hash),
                "amount": amount,
                "fee": gas_price,
                "from": from_wallet or self.current_account.address,
                "to": to_wallet}

    def get_transaction_status(self, tx_hash: str):
        return {"tx": self.web3_instance.eth.get_transaction(tx_hash)}
