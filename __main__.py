#!/usr/bin/python3
from Core import *
from Ethereum import Ethereum
from Bitcoin import Bitcoin
from Tether import Tether
from Dai import Dai
from Tron import Tron
from Error import *
from web3 import exceptions
from doc.es_doc import *

__author__ = "Esteban Chacon Martin"
__doc__ = "This program is intended to be used as a frontend for cryptocurrencies basic operations... "

class TFBlockchain:
    doc = Documentation(name="TFBlockchain",
                        documentation=base_doc) \
        .put("dai", dai_doc) \
        .put("ethereum", eth_doc) \
        .put("bitcoin", btc_doc) \
        .put("tron", tron_doc)\
        .put("tether", tether_doc) 
    working_on_current = None
    result = None
    blockchains = {
        "dai": Dai(),
        "ethereum": Ethereum(),
        "bitcoin": Bitcoin(),
        "tron": Tron(),
        "tether": Tether()
    }
    first_time = True
    cache_id = -1

    def __init__(self):
        quitting = False
        print("Welcome to TFProtocol Blockchains's Works. For any kind of help please type \"help\","
              "if you want to get help about some command please type \"help command\".")
        print(EWAITTOREAD)
        while True:
            try:
                typed = input(">> ")
                if typed is None or typed == "" or len(typed.split(" ")) == 0:
                    print(f"{EEMPTYINPUT} Please input something")
                    continue
                if not self.handle_type(typed):
                    break
            except TFBlockchainError as ex:
                print(f"{ex.error_code} {ex.message}")
            except exceptions.CannotHandleRequest as ex:
                print(f"{ACTION_ERRORS.get(current_action)} {ex}")
            except Exception as ex:
                print(f"{EEXCEPT} Exception occured... try again... error message\n{ex}")
                # raise ex # Disable this in production
            except KeyboardInterrupt:
                pass
            finally:
                if quitting:
                    print(EQUITTING)
                    break
                else:
                    print(EWAITTOREAD)

    def handle_type(self, typed):
        if typed == "quit" or typed == "exit":
            return False
        elif typed.split()[0] == "help":
            if len(typed.split()) > 1:
                self.helping_mode(typed.split()[1])
            else:
                self.helping_mode()
        else:
            order = typed.split()[0]
            args = typed.split()[1:]
            self.working_on_current = self.blockchains.get(order.lower())
            current_env = self.working_on_current.__class__.__name__
            if self.working_on_current is None:
                raise TFBlockchainError(error_code=ENOTFOUND, message="Environment not found")
            self.handle_petition(args)

        return True

    def helping_mode(self, command=None):
        if command is None:
            print(f"{EOK} \n{self.doc}")
        else:
            print(f"{EOK} \n{self.doc.get(command.lower())}")

    def handle_petition(self, args: list):
        caution = False
        if args is None or args.__len__() == 0:
            return self.helping_mode(self.working_on_current.__class__.__name__)

        current_action = args[0]
        # historic
        if not (args[0] == HISTORIC):
            self.result = None
            try:
                parsed = dict(self.join_lists_as_iterator(args[1::2], args[2::2]))
            except IndexError:
                raise TFBlockchainError(error_code=EARG, message="You hadn't set the value for the argument correctly")
        else:
            parsed = dict(self.join_lists_as_iterator(args[1::2], args[2::2], forget_second=True))
            if parsed.get("use") is not None:
                self.cache_id = parsed.get("use")
                self.first_time = False
            elif parsed.keys().__contains__("new"):
                self.cache_id = Cache.first_time_action('')
                self.print_ok(f"New ID:{self.cache_id}")
            elif parsed.keys().__contains__("get-last"):
                self.print_ok(Cache.get(self.cache_id, self.working_on_current.__class__.__name__, last=True))
            elif parsed.keys().__contains__("get-all") is not None:
                self.print_ok(Cache.get(self.cache_id, self.working_on_current.__class__.__name__))
            return
        # set-token-type
        if args[0] == SET_TOKEN_TYPE:
            if isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.set_token_type(token_type=parsed.get("type"),
                                                                     ether_instance=self.blockchains.get("ether"),
                                                                     tron_instance=self.blockchains.get("tron"))
            self.print_ok(self.result)
        # transfer
        elif args[0] == TRANSFER:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.transact(to_address=parsed.get("to"),
                                                               amount=parsed.get("amount"),
                                                               fee=parsed.get("fee") or 0,
                                                               replaceable=
                                                               str(parsed.get("replace")).lower() == "true"
                                                               or False,
                                                               passphrase=parsed.get("with")
                                                               )
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.transfer(amount=float(parsed.get("amount")),
                                                               to_wallet=parsed.get("to"),
                                                               private_key=parsed.get("with"),
                                                               gas_price=parsed.get("gas-price"),
                                                               from_wallet=parsed.get("from") or None,
                                                               gas_limit=parsed.get("gas-limit") or 21000)
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.transfer(to=parsed.get("to"),
                                                               amount=float(parsed.get("amount")),
                                                               src=parsed.get("from") or None,
                                                               private_key=parsed.get("with") or None,
                                                               gas_price=parsed.get("gas-price") or None,
                                                               gas=parsed.get("gas-limit") or None)
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.transact(from_address=parsed.get("from"),
                                                               to_address=parsed.get("to"),
                                                               amount=float(parsed.get("amount")),
                                                               private_key=parsed.get("with"),
                                                               fee_limit=parsed.get("fee-limit"))
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.transfer(to=parsed.get("to"),
                                                               amount=parsed.get("amount"))
            self.print_ok(self.result)
        # get-balance
        elif args[0] == GET_BALANCE:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.check_balance(parsed.get("base") or "sat")
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.check_balance(parsed.get("of") or None)
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.get_balance_of(parsed.get("of"))
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_balance_of(parsed.get("of"))
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.get_balance_of(target=parsed.get("of"))
            self.print_ok(self.result)
        # create-account
        elif args[0] == CREATE_ACCOUNT:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.create_account(parsed.get("name") or None)
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.create_account()
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.create_account(parsed.get("with") or None)
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.create_account(parsed.get("with") or None,
                                                                     parsed.get("parent") or None)
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.create_account(parsed.get("with") or None,
                                                                     parsed.get("parent") or None)
            caution = True
            self.print_ok(self.result)
        # get-raw-prik
        elif args[0] == GET_RAW_PRIVATE_KEY:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.get_pri_key(parsed.get("of"))
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.get_current_account_pri_key()
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.get_prik_of_current()
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_prik_of_current()
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.get_prik_of_current()
            caution = True
            self.print_ok(self.result)
        # get-prik
        elif args[0] == GET_PRIVATE_KEY:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.get_pri_key(address=parsed.get("of"))
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.get_current_account_pri_key()
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.get_prik_of_current()
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_prik_of_current()
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.get_prik_of_current()
            caution = True
            self.print_ok(self.result)
        # get-address
        elif args[0] == GET_ADDRESS:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.get_addresses()
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.get_current_account_address()
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.get_current_account_address()
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_current_account_address()
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.get_current_account_address()
            self.print_ok(self.result)
        # get-pubk-key
        elif args[0] == GET_PUBLIC_KEY:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.get_pub_key(parsed.get("of"))
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_pubk_key(parsed.get("of") or None)
            elif isinstance(self.working_on_current, Tether):
                pass
            self.print_ok(self.result)
        # get-tx-status
        elif args[0] == GET_TX_STATUS:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.get_transaction_status(parsed.get("of"))
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.get_transaction_status(parsed.get("of"))
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.get_transaction_status(parsed.get("of"))
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_transaction_status(parsed.get("of"))
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.get_transaction_status(parsed.get("of"))
            self.print_ok(self.result)
        # create-wallet
        elif args[0] == CREATE_WALLET:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.create_or_open_wallet(parsed.get("name"))
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.create_account()
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.create_account(parsed.get("with") or None)
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.create_account(prik=parsed.get("with" or None),
                                                                     parent=parsed.get("parent") or None)
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.create_account(private_key=parsed.get("with") or None,
                                                                     parent_for_tron=parsed.get("parent") or None)
            caution = True
            if self.result is not None:
                self.print_ok(self.result)
        # set-provider
        elif args[0] == SET_PROVIDER:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.set_provider(parsed.get("url") or None,
                                                                   parsed.get("user") or None,
                                                                   parsed.get("pass") or None,
                                                                   parsed.get("address") or None,
                                                                   parsed.get("port") or None,
                                                                   parsed.get("protocol") or None)
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.set_provider(parsed.get("url"))
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.set_provider(parsed.get("url"))
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.set_provider(endpoint_uri=parsed.get("url") or None,
                                                                   api_key=parsed.get("with"))
            elif isinstance(self.working_on_current, Tether):  
                self.result = self.working_on_current.set_provider(url=parsed.get("url") or None,
                                                                   api_key=parsed.get("with"),
                                                                   for_bc=self.blockchains.get(parsed.get("for")) or None)
            if self.result.get("connected"):
                self.print_ok(f"Provider set successfully")
            else:
                self.print_ok(f"Cannot set the provider successfully")
        # set-account
        elif args[0] == SET_ACCOUNT:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.create_or_open_wallet(parsed.get("with"))
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.set_current_account(parsed.get("with"))
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.set_current_account(parsed.get("with"))
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.set_current_account(parsed.get("with"))
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.set_current_account(parsed.get("with"))
            caution = True
            self.print_ok(self.result)
        # set-passphrase
        elif args[0] == SET_WALLET_PASSPHRASE:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.encrypt_wallet(parsed.get("with"))
            self.print_ok(self.result)
        # unlock-wallet
        elif args[0] == UNLOCK_WALLET:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.unlock_wallet(parsed.get("with"), parsed.get("timeout") or 3)
            self.print_ok(self.result)
        # lock-wallet
        elif args[0] == LOCK_WALLET:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.lock_wallet()
            self.print_ok(self.result)
        # change-passphrase
        elif args[0] == CHANGE_PASSPHRASE:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.change_passphrase_wallet(parsed.get("old"), parsed.get("new"))
            self.print_ok(self.result)
        # get-fee
        elif args[0] == GET_FEE:
            if isinstance(self.working_on_current, Bitcoin):
                if parsed.get("conf-target") is None and parsed.get("mode") is None:
                    self.result = self.working_on_current.get_tx_fee()
                else:
                    self.result = self.working_on_current.get_smart_fee(parsed.get("conf-target") or 5,
                                                                        parsed.get("mode") or "CONSERVATIVE")
            elif isinstance(self.working_on_current, Ethereum):
                self.result = self.working_on_current.get_fee(parsed.get("use") or 21000)
            elif isinstance(self.working_on_current, Dai):
                self.result = self.working_on_current.get_fee(parsed.get("use") or 21000)
            elif isinstance(self.working_on_current, Tron):
                self.result = self.working_on_current.get_fee()
            elif isinstance(self.working_on_current, Tether):
                self.result = self.working_on_current.get_fee()
            self.print_ok(self.result)
        # set-fee
        elif args[0] == SET_FEE:
            if isinstance(self.working_on_current, Bitcoin):
                self.result = self.working_on_current.set_tx_fee(parsed.get("amount"))
            self.print_ok(self.result)
        else:
            raise TFBlockchainError(error_code=EARG, message="Not valid arguments given...")
        if caution is False:
            if self.first_time and parsed.get("cache-id") is None:
                self.cache_id = Cache.first_time_action(self.result)
                print(f"Your cache id is: {self.cache_id}")
                self.first_time = False
            else:
                if parsed.get("cache-id") is not None:
                    self.cache_id = parsed.get("cache-id")
                Cache.other_time_action(self.cache_id, f"{self.result}")

    @staticmethod
    def print_ok(value):
        print(f"{EOK} {value}")

    @staticmethod
    def join_lists_as_iterator(arr: list, arr1: list, forget_second=False):
        for i in arr:
            if forget_second:
                if arr.index(i) < len(arr1):
                    yield i, arr1[arr.index(i)]
                else:
                    yield i, None
            else:
                yield i, arr1[arr.index(i)]


if __name__ == "__main__":
    print("Loading modules ... please wait...")
    TFBlockchain()
