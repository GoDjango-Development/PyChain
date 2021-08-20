import requests
import json
from requests.exceptions import MissingSchema, ConnectionError
from Core import TFBlockchainError as tfb_err
from Core import *


class Bitcoin:
    __username__ = None
    __password__ = None
    __address__ = None
    __port__ = None
    __protocol__ = None
    __url__ = None
    __header__ = {'content-type': 'application/json'}
    __wallet_append__ = None

    base_currencies = {"sat": 100000000, "btc": 1}

    account = None

    def __init__(self, rpc_address: str = None, rpc_user: str = None, rpc_password: str = None, rpc_port: int = None):
        if rpc_address is not None and rpc_port is not None and rpc_user is not None and rpc_password is not None:
            self.set_provider("http://{0}:{1}@{2}:{3}".format(rpc_user, rpc_password, rpc_address, rpc_port))

    # ******************************************************************************************************************
    # Wallet Works
    def create_or_open_wallet(self, wallet_name, passphrase=None):
        try:
            self.__commit__("createwallet", [wallet_name])
        except TFBlockchainError as tfb:
            if not (current_action == SET_ACCOUNT):
                raise tfb
            else:
                try:
                    self.__commit__("loadwallet", [wallet_name])
                except TFBlockchainError:
                    pass
        finally:
            self.__wallet_append__ = f"/wallet/{wallet_name}"
            if passphrase is not None:
                self.encrypt_wallet(passphrase)
            return {"wallet-name": wallet_name}

    def encrypt_wallet(self, passphrase):
        assert self.__wallet_append__ != ""
        encrypted = self.__commit__("encryptwallet", [passphrase], append_url=self.__wallet_append__)
        return {"successfully": encrypted.json()["error"] is None}

    def unlock_wallet(self, passphrase, timeout=3):
        unlock_status = self.__commit__("walletpassphrase",
                                        [passphrase, int(timeout)], append_url=self.__wallet_append__)
        if unlock_status.json()["error"] is not None:
            raise tfb_err(UNLOCK_WALLET, unlock_status.json()["error"])
        return {"unlocked": True}

    def lock_wallet(self):
        lock_status = self.__commit__("walletlock", [], append_url=self.__wallet_append__)
        if lock_status.json()["error"] is not None:
            raise tfb_err(LOCK_WALLET, lock_status.json()["error"])
        return {"successfully": True}

    def change_passphrase_wallet(self, old_passphrase, new_passphrase):
        status = self.__commit__("walletpassphrasechange", [old_passphrase, new_passphrase],
                                 append_url=self.__wallet_append__)
        if status.json()["error"] is not None:
            raise tfb_err(CHANGE_PASSPHRASE, status.json()["error"])
        return {"successfully": True}

    def check_balance(self, base_currency="sat"):
        result = self.__commit__("getbalance", append_url=self.__wallet_append__)
        try:
            result = float(result.json()["result"])*self.base_currencies.get(base_currency)
        except IndexError as ex:
            raise tfb_err(GET_BALANCE, str(ex)+"... Base currency only admits \"sat\" and \"btc\"")
        return {"amount": result}

    def get_tx_fee(self):
        fee = self.__commit__("getwalletinfo", append_url=self.__wallet_append__)
        if fee.json()["error"] is not None:
            raise tfb_err(GET_FEE, fee.json()["error"])
        fee = fee.json()["result"]["paytxfee"]
        return {"fee": fee}

    def get_smart_fee(self, conf_target=5, estimate_mode="CONSERVATIVE"):
        fee = self.__commit__("estimatesmartfee", [conf_target, estimate_mode])
        if fee.json()["error"] is None:
            return fee.json()["result"]
        else:
            raise tfb_err(GET_FEE, fee.json()["error"])

    def set_tx_fee(self, fee):
        res = self.__commit__("settxfee", [fee], append_url=self.__wallet_append__).json()
        return {"setted?": res["error"] is None}

    # End Wallet Works....
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    # Address Works
    def create_account(self, account_name=None):
        self.account = self.__commit__("getnewaddress", append_url=self.__wallet_append__)
        address = self.account.json()["result"]
        prik = self.get_pri_key(address)["private-key"]
        puk = self.get_pub_key(address)["public-key"]
        return {"address": address,
                "private-key": prik,
                "public-key": puk}

    def get_pri_key(self, address):
        result = self.__commit__("dumpprivkey", [address],
                                 self.__wallet_append__).json()
        if result["result"]:
            return {"private-key": result["result"]}
        else:
            return {"private-key": result["error"]}

    def get_pub_key(self, address):
        if address is None:
            raise tfb_err(GET_PUBLIC_KEY, "You must give a valid address...")
        address_info = self.__commit__("getaddressinfo", [address],
                                       append_url=self.__wallet_append__).json()
        puk = address_info["result"]["pubkey"]
        return {"public-key": puk}

    def get_addresses(self):
        addresses = self.__commit__("listunspent", append_url=self.__wallet_append__).json()
        addresses = addresses["result"]
        result = dict()
        if addresses is None or len(addresses) == 0:
            return result
        count = 0
        for address in addresses:
            result[f"address {count}"] = address["address"]
        return result

    # End Address Works
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    # Transaction Work
    def transact(self, to_address, amount: float, passphrase=None, fee=0, replaceable=False, comment="", message="",
                 substract_from_amount=False,):
        if passphrase is not None:
            self.unlock_wallet(passphrase)
        if fee > 0:
            self.set_tx_fee(fee)
        if float(self.check_balance().get("amount")) - float(amount) - float(self.get_tx_fee().get("fee")) > 0 \
                or not substract_from_amount:
            tx = self.__commit__("sendtoaddress",
                                 [to_address, amount, comment, message, False, replaceable],
                                 append_url=self.__wallet_append__)
        else:
            tx = self.__commit__("sendtoaddress",
                                 [to_address, amount, comment, message, True, replaceable],
                                 append_url=self.__wallet_append__)
            self.lock_wallet()
        return {"id": tx.json()["result"],
                "amount": amount,
                "fee": fee,
                "from": self.__wallet_append__,
                "to": to_address}

    def get_transaction_status(self, tx_id):
        transaction = self.__commit__("gettransaction", [tx_id], append_url=self.__wallet_append__)
        return transaction.json()["result"]

    # End Transaction Work
    # ******************************************************************************************************************

    def set_provider(self, url: str = None, rpc_user: str = None, rpc_password: str = None,
                     rpc_address: str = None, rpc_port: int = None, rpc_protocol: str = None):
        if url is None and ((rpc_user and rpc_password and rpc_address and rpc_port and rpc_protocol
                             ) is None):
            raise tfb_err(SET_PROVIDER, "Invalid arguments given...")
        if url is not None:
            self.__url__ = url
            self.__protocol__ = url.split(":")[0]
        else:
            self.__protocol__ = rpc_protocol
            self.__username__ = rpc_user
            self.__password__ = rpc_password
            self.__address__ = rpc_address
            self.__port__ = rpc_port
            self.__url__ = f"{self.__protocol__}://{self.__username__}:{self.__password__}@{self.__address__}:" \
                           f"{self.__port__}"
        if self.__commit__("help").json() is not None:
            return {"connected": True}
        else:
            return {"connected": False}

    def __commit__(self, method: str, params: list = [], append_url="", debug=False):
        payload = json.dumps({"method": method,
                              "params": params,
                              "jsonrpc": "1.0"})
        response = None
        try:
            if self.__protocol__ is None:
                raise TFBlockchainError(SET_PROVIDER, "Please ensure that a provider is set")
            if self.__protocol__.lower() == "https":
                session = requests.Session()
                response = session.post(f"{self.__url__}{append_url or ''}",
                                        headers=self.__header__, data=payload)
            elif self.__protocol__.lower() == "http":
                response = requests.post(f"{self.__url__}{append_url or ''}",
                                         headers=self.__header__, data=payload)
        except MissingSchema as ex:
            raise tfb_err(SET_PROVIDER, str(ex) + "... Please try to use set-provider first...")
        except ConnectionError as ex:
            raise tfb_err(SET_PROVIDER, str(ex) + "... Try again later or check your network connectivity...")
        if debug:
            print(response.content)
            print(response.text)
            print(response.reason)
            print(response.status_code)

        if response.json()["error"] is not None:
            if not (current_action == SET_ACCOUNT):
                raise tfb_err(current_action, response.json()["error"])
            raise tfb_err(current_action, response.json()["error"])
        return response
