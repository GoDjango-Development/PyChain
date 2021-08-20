import json
from tronpy.tron import Contract
from Tron import Tron
from Ethereum import Ethereum


from data.contracts import usdt_trc20_bytecode
from data.contracts import usdt_trc20_address
from data.contracts import usdt_trc20_abi
from tronpy.tron import PrivateKey

class Tether:
    tether_contract = None
    usdt_erc20_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    blockchain_instance = None

    def __init__(self, ):
        pass

    def create_account(self, private_key: str = None, parent_for_tron=None):
        if isinstance(self.blockchain_instance, Ethereum):
            if private_key is None:
                self.blockchain_instance.create_account()
            else:
                self.blockchain_instance.set_current_account(private_key)
            self.tether_contract = \
                self.blockchain_instance.web3_instance.eth.contract(address=self.blockchain_instance.
                                                                    get_current_account_address(), abi=self.abi)
        elif isinstance(self.blockchain_instance, Tron):
            if private_key is None and self.blockchain_instance.account is not None:
                private_key = self.blockchain_instance.get_prik_of_current()
            elif private_key is not None:
                self.blockchain_instance.set_current_account(private_key)
            else:
                return {"error": "At least one private key must be set into tron or into tether... use create-account..."} 
            try:
                self.tether_contract = self.blockchain_instance.tron_instance.get_contract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
                trn = (self.blockchain_instance.tron_instance.trx
                    .deploy_contract(self.blockchain_instance.get_current_account_address(), self.tether_contract)
                    .fee_limit(5_000_000)
                    .build()
                    .sign(PrivateKey(bytes.fromhex(private_key)))
                    )
                print(f"Transaction is ready data  {trn}")
                print("Creating account, deploying now...")
                res = trn.broadcast()
                print("Already broadcasted awaiting now...")
                res = res.wait()
            except Exception as ex:
                return {"error": 
                f"Cannot successfully deploy the contract into address {self.blockchain_instance.get_current_account_address()}\
 are you sure the address owns enough tron for deployment and you are on mainnet?" }
            return res

    def transfer(self, to, amount):
        if isinstance(self.blockchain_instance, Tron):
            transaction = (
                Contract(self.tether_contract).functions.transfer(to, amount).with_owner(
                    self.blockchain_instance.get_current_account_address()).fee_limit(5_000_000).build()
                    .sign(self.blockchain_instance.get_prik_of_current())
            )
            return transaction.broadcast().wait()
        elif isinstance(self.blockchain_instance, Ethereum):
            self.tether_contract.functions.transfer(to, amount)
        return {"development": "in development yet"}

    def set_current_account(self, prik):
        if isinstance(self.blockchain_instance, Tron):
            return self.blockchain_instance.set_current_account(prik)
        elif isinstance(self.blockchain_instance, Ethereum):
            return self.blockchain_instance.set_current_account(prik)
        else:
            return None

    def get_current_account_address(self):
        if isinstance(self.blockchain_instance, Tron):
            return self.blockchain_instance.get_current_account_address()
        elif isinstance(self.blockchain_instance, Ethereum):
            return self.blockchain_instance.get_current_account_address()
        else:
            return None

    def get_balance_of(self, target=None):
        if isinstance(self.blockchain_instance, Tron):
            from data.contracts import usdt_trc20_address
            functions = self.blockchain_instance.tron_instance.get_contract(usdt_trc20_address).functions
            if target is None:
                target = self.get_current_account_address()
            return functions.balanceOf(target)/(10**functions.decimals())
        elif isinstance(self.blockchain_instance, Ethereum):
            return self.tether_contract.functions.get_balance()
        else:
            return None

    def get_prik_of_current(self):
        if isinstance(self.blockchain_instance, Tron):
            return self.blockchain_instance.get_prik_of_current()
        elif isinstance(self.blockchain_instance, Ethereum):
            return self.blockchain_instance.get_current_account_pri_key()
        else:
            return None

    def set_provider(self, url, for_bc=None,api_key=None):
        if self.blockchain_instance is None or for_bc is not None:
            self.blockchain_instance = for_bc
        else:
            raise ValueError("Please call set-token-type first and after the error, call this, or \
use the \"for\" parameter with tron or ethereum...")
        if isinstance(self.blockchain_instance, Tron):
            return self.blockchain_instance.set_provider(api_key=api_key,endpoint_uri=url)
        elif isinstance(self.blockchain_instance, Ethereum):
            return self.blockchain_instance.set_provider(url)
        else:
            raise ValueError("Not valid blockchain given...")

    def get_transaction_status(self, txid):
        if isinstance(self.blockchain_instance, Tron):
            return self.blockchain_instance.get_transaction_status(txid)
        elif isinstance(self.blockchain_instance, Ethereum):
            return self.blockchain_instance.get_transaction_status(txid)
        else:
            return None

    def set_token_type(self, token_type, ether_instance=None, tron_instance: Tron=None):
        #client = Tron(network="nile")
        if ether_instance is None and tron_instance is None:
            raise Exception("Not valid parameters at least one blockchain must be given...")
        if token_type == "usdt-erc20":
            if self.blockchain_instance is None or not isinstance(self.blockchain_instance, Ethereum):
                self.blockchain_instance = ether_instance
            self.tether_contract = self.blockchain_instance \
                .get_smart_contract(address=self.address, abi=self.abi, bytecode=self.bytecode)
        elif token_type == "usdt-trc20":
            if self.blockchain_instance is None or not isinstance(self.blockchain_instance, Tron):
                self.blockchain_instance = tron_instance
            self.tether_contract = Contract(abi=usdt_trc20_abi, bytecode=usdt_trc20_bytecode,)
            if self.blockchain_instance.get_current_account_address() is None:
                return {"result": "Cannot deploy contract without an account, please first use create-account or set-account.."}
            txn = (self.blockchain_instance.tron_instance.trx.deploy_contract\
                   (self.blockchain_instance.get_current_account_address(), self.tether_contract)
                   .fee_limit(5_000_000)
                   .build()
                   .sign(PrivateKey(bytes.fromhex(self.blockchain_instance.\
                       account["private_key"]))))
            try:
                print("Transaction created for deployment, loading now...")
                print("Successfully loaded contract at address: {} ".format(txn.broadcast().wait()["contract_address"]))
            except Exception as ex:
                print(ex)
                return {"result": "Cannot load or create the contract successfully..."}
        else:
            return {"result": "Cannot recognize {} as a valid tether token type".format(token_type)}
        return {"result": "Successfully working with {}".format(token_type)}

    def get_fee(self):
        pass
