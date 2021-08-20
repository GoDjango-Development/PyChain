#!/usr/bin/python3
import requests
import tronpy
from tronpy.providers import HTTPProvider


class Tron:
    tron_instance = None
    account = None

    def __init__(self, endpoint_uri="https://api.trongrid.io/", api_key="",
                 network="mainnet"):
        self.tron_instance = tronpy.Tron(provider=HTTPProvider(
            endpoint_uri=endpoint_uri, api_key=api_key), network=network)

    def set_provider(self, api_key, endpoint_uri=None):
        if endpoint_uri is None:
            endpoint_uri = self.tron_instance.provider.endpoint_uri
        self.tron_instance.provider = HTTPProvider(endpoint_uri=endpoint_uri, api_key=api_key)
        try:
            self.tron_instance.provider.make_request("/wallet/listnodes")
            return {"connected": True}
        except Exception:
            return {"connected": False}
            
        

    # Test
    def transact(self, to_address: str, amount: int, priv_key=None, from_address=None, fee_limit =5_000_000):
        if from_address is None:
            from_address = self.get_current_account_address()
        if priv_key is None and self.get_prik_of_current() is None:
            raise ValueError("Non private key given... please provide one so we can protect your data...")
        priv_key = tronpy.tron.PrivateKey(bytes.fromhex(priv_key))
        transfer = (self.tron_instance.trx.transfer(from_=from_address, to=to_address, amount=amount)
                    .fee_limit(fee_limit).build().sign(priv_key=priv_key))
        return transfer.broadcast().wait()

    def get_balance_of(self, of: str = None):
        if of is None:
            return self.tron_instance.get_account_balance(self.get_current_account_address())
        return self.tron_instance.get_account_balance(of)

    def get_transaction_status(self, transaction_id) -> dict:
        return self.tron_instance.get_transaction(transaction_id)

    def get_account_info(self, address=None):
        if address is None:
            return self.tron_instance.get_account(addr=self.get_current_account_address())
        return self.tron_instance.get_account(addr=address)

    def create_account(self, parent=None, prik=None):
        if parent is None:
            parent = "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"
        if prik is None:
            prik = tronpy.tron.PrivateKey.random()
        self.account = self.tron_instance.generate_address(prik)
        self.tron_instance.provider.make_request("/wallet/createaccount", {
            "owner_address": parent,
            "account_address": self.get_current_account_address(),
            "visible": True
        })
        return self.account

    def get_prik_of_current(self):
        if self.account is None:
            return None
        return self.account["private_key"]

    def get_current_account_address(self):
        if self.account is None:
            return None
        return self.account["base58check_address"]

    def get_pubk_key(self, address: str = None):
        if address is not None:
            return self.tron_instance.get_account(address)["public_key"]
        elif self.account is None:
            return None
        return self.account["public_key"]

    def get_smart_contract(self, address=None):
        if address is None and self.account is None:
            return None
        elif address is None:
            address = self.get_current_account_address()
        return self.tron_instance.get_contract(addr=address)

    def set_current_account(self, prik):
        self.account = self.tron_instance.generate_address(tronpy.tron.PrivateKey.fromhex(prik))
        return self.account
    # {'base58check_address': 'TVuUzyVws21QdMASKFENo9Bsr9RPyYxnLc', 'hex_address': '41daae34ed4d72dace9f8f2e1153dd3df6bfbe68bd', 'private_key': '2e080158a8cd33c6e48564fab7c1313c87856a7d478ab0eb6dc82fa542ac8751', 'public_key': 'a4e557f3bc1eef34e47899eae1b6f9e8233be9973de91280c1774cd4f216b84e4ecf5e4ad1313fc713aadf4becb895f743b1f8cdaadb53ad8081291efbec7aa7'}

    # Todo
    def get_fee(self):
        return None

