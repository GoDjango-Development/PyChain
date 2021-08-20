import os
from datetime import datetime
from Error import *


HISTORIC = "historic"
TRANSFER = "transfer"
GET_BALANCE = "get-balance"
SET_TOKEN_TYPE = "set-token-type"
CREATE_ACCOUNT = "create-account"
GET_RAW_PRIVATE_KEY = "get-raw-prik"
GET_PRIVATE_KEY = "get-prik"
GET_ADDRESS = "get-address"
GET_PUBLIC_KEY = "get-pubk"
GET_TX_STATUS = "get-tx-status"
CREATE_WALLET = "create-wallet"
SET_PROVIDER = "set-provider"
SET_ACCOUNT = "set-account"
SET_WALLET_PASSPHRASE = "set-passphrase"
UNLOCK_WALLET = "unlock-wallet"
LOCK_WALLET = "lock-wallet"
CHANGE_PASSPHRASE = "change-passphrase"
GET_FEE = "get-fee"
SET_FEE = "set-fee"

ACTION_ERRORS = {
    HISTORIC: 30,
    TRANSFER: 40,
    GET_BALANCE: 50,
    GET_PRIVATE_KEY: 51,
    GET_RAW_PRIVATE_KEY: 52,
    GET_ADDRESS: 53,
    GET_FEE: 54,
    GET_PUBLIC_KEY: 55,
    GET_TX_STATUS: 56,
    SET_ACCOUNT: 60,
    SET_FEE: 61,
    SET_PROVIDER: 62,
    SET_WALLET_PASSPHRASE: 63,
    CREATE_ACCOUNT: 70,
    CREATE_WALLET: 71,
    CHANGE_PASSPHRASE: 80,
    UNLOCK_WALLET: 81,
    LOCK_WALLET: 82
}

current_action = None
current_env = None
path = os.path.join(os.path.abspath(os.path.curdir), ".cache")


class Documentation:
    name = "undefined"
    documentation = "none"
    commands = {}

    def __init__(self, name, documentation):
        self.name = name
        self.documentation = documentation

    def __str__(self):
        return self.documentation

    def put(self, command, documentation):
        key_value = list()
        for key in self.commands:
            key_value.append((key, self.commands.get(key)))
        key_value.append((command, documentation))
        self.commands = dict(key_value)
        return self

    def get(self, command=None):
        if command is None:
            return f"{self.documentation}"
        else:
            res = self.commands.get(command)
            if res is None:
                return f"Cannot find the documentation for {command}..."
            return f"{res}"


class Tools:
    def __init__(self):
        pass


class Cache:

    @staticmethod
    def other_time_action(cache_id, value):
        content = ""
        with open(os.path.join(path, str(cache_id)), "r") as file:
            content = file.readlines()
        with open(os.path.join(path, str(cache_id)), "w+") as file:
            temp = ""
            for i in content[1:]:
                temp += i
            file.write(f"{Cache.get_timestamp()},\n{temp},\n{current_env}: {value}")

    @staticmethod
    def first_time_action(value):
        if not os.path.exists(path):
            os.mkdir(path)
        elif os.path.exists(path) and not os.path.isdir(path):
            os.remove(path)
            os.mkdir(path)
        cache = os.listdir(path)
        my_id = len(cache)+1
        with open(os.path.join(path, str(my_id)), "w") as file:
            file.write(f"{Cache.get_timestamp()}\n{current_env}: {value}")
        return my_id

    @staticmethod
    def get_all_of(cache_id):
        with open(os.path.join(path, str(cache_id)), "r") as file:
            return file.read()

    @staticmethod
    def get(cache_id, command, limit=-1, last=False):
        res = []
        try:
            with open(os.path.join(path, str(cache_id)), "r") as file:
                data = file.readlines()
                if last:
                    limit = 1
                    data.reverse()
                for dat in data:
                    try:
                        if dat.split(":")[0] == command:
                            res.append(dat.split(":")[1:])
                        if 0 < limit == len(res):
                            return res
                    except IndexError:
                        return []
        except FileNotFoundError:
            raise TFBlockchainError(error_code=ECACHENOTLOCATED, message="Please try to use a command first or use "
                                                                         "env historic new or env historic use "
                                                                         "CACHE_ID")
        return res

    @staticmethod
    def check_cache():
        cache = os.listdir(path)
        cache.sort()
        for cache_file in cache:
            with open(cache_file, "r") as file:
                print(file.readlines()[0])

    @staticmethod
    def get_timestamp():
        return datetime.now().timestamp()


class TFBlockchainError(BaseException):
    error_code = 0
    message = ""

    def __init__(self, action_name=None, message="An exception occurred", error_code=None):
        super(TFBlockchainError, self).__init__()
        if action_name is not None:
            self.__error_code__(action_name)
        elif error_code is not None:
            self.error_code = error_code
        self.message = message

    def __error_code__(self, action):
        try:
            self.error_code = ACTION_ERRORS.get(action)
        except Exception:
            self.error_code = -1
