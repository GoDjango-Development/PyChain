import json
from Ethereum import Ethereum
from web3 import Web3


class Dai:
    ether_instance = None
    address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    abi = '[{"inputs":[{"internalType":"uint256","name":"chainId_","type":"uint256"}],"payable":false,' \
          '"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,' \
          '"internalType":"address","name":"src","type":"address"},{"indexed":true,"internalType":"address",' \
          '"name":"guy","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"}],' \
          '"name":"Approval","type":"event"},{"anonymous":true,"inputs":[{"indexed":true,"internalType":"bytes4",' \
          '"name":"sig","type":"bytes4"},{"indexed":true,"internalType":"address","name":"usr","type":"address"},' \
          '{"indexed":true,"internalType":"bytes32","name":"arg1","type":"bytes32"},{"indexed":true,' \
          '"internalType":"bytes32","name":"arg2","type":"bytes32"},{"indexed":false,"internalType":"bytes",' \
          '"name":"data","type":"bytes"}],"name":"LogNote","type":"event"},{"anonymous":false,"inputs":[{' \
          '"indexed":true,"internalType":"address","name":"src","type":"address"},{"indexed":true,' \
          '"internalType":"address","name":"dst","type":"address"},{"indexed":false,"internalType":"uint256",' \
          '"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],' \
          '"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],' \
          '"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],' \
          '"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],' \
          '"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{' \
          '"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"",' \
          '"type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],' \
          '"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{' \
          '"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad",' \
          '"type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],' \
          '"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{' \
          '"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{' \
          '"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view",' \
          '"type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"usr","type":"address"},' \
          '{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"burn","outputs":[],"payable":false,' \
          '"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals",' \
          '"outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view",' \
          '"type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"guy","type":"address"}],' \
          '"name":"deny","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},' \
          '{"constant":false,"inputs":[{"internalType":"address","name":"usr","type":"address"},' \
          '{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"mint","outputs":[],"payable":false,' \
          '"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address",' \
          '"name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},' \
          '{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"move","outputs":[],"payable":false,' \
          '"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{' \
          '"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view",' \
          '"type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],' \
          '"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,' \
          '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address",' \
          '"name":"holder","type":"address"},{"internalType":"address","name":"spender","type":"address"},' \
          '{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry",' \
          '"type":"uint256"},{"internalType":"bool","name":"allowed","type":"bool"},{"internalType":"uint8",' \
          '"name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},' \
          '{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,' \
          '"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address",' \
          '"name":"usr","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"pull",' \
          '"outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,' \
          '"inputs":[{"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad",' \
          '"type":"uint256"}],"name":"push","outputs":[],"payable":false,"stateMutability":"nonpayable",' \
          '"type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"guy","type":"address"}],' \
          '"name":"rely","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},' \
          '{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"",' \
          '"type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,' \
          '"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],' \
          '"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{' \
          '"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"wad",' \
          '"type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],' \
          '"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{' \
          '"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst",' \
          '"type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"transferFrom",' \
          '"outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,' \
          '"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"version",' \
          '"outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view",' \
          '"type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],' \
          '"name":"wards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,' \
          '"stateMutability":"view","type":"function"}] '
    bytecode = "0x608060405234801561001057600080fd5b50600436106101425760003560e01c80637ecebe00116100b8578063a9059cbb1161007c578063a9059cbb146106b4578063b753a98c1461071a578063bb35783b14610768578063bf353dbb146107d6578063dd62ed3e1461082e578063f2d5d56b146108a657610142565b80637ecebe00146104a15780638fcbaf0c146104f957806395d89b411461059f5780639c52a7f1146106225780639dc29fac1461066657610142565b8063313ce5671161010a578063313ce567146102f25780633644e5151461031657806340c10f191461033457806354fd4d501461038257806365fae35e1461040557806370a082311461044957610142565b806306fdde0314610147578063095ea7b3146101ca57806318160ddd1461023057806323b872dd1461024e57806330adf81f146102d4575b600080fd5b61014f6108f4565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561018f578082015181840152602081019050610174565b50505050905090810190601f1680156101bc5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b610216600480360360408110156101e057600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919050505061092d565b604051808215151515815260200191505060405180910390f35b610238610a1f565b6040518082815260200191505060405180910390f35b6102ba6004803603606081101561026457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610a25565b604051808215151515815260200191505060405180910390f35b6102dc610f3a565b6040518082815260200191505060405180910390f35b6102fa610f61565b604051808260ff1660ff16815260200191505060405180910390f35b61031e610f66565b6040518082815260200191505060405180910390f35b6103806004803603604081101561034a57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610f6c565b005b61038a611128565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156103ca5780820151818401526020810190506103af565b50505050905090810190601f1680156103f75780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6104476004803603602081101561041b57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050611161565b005b61048b6004803603602081101561045f57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061128f565b6040518082815260200191505060405180910390f35b6104e3600480360360208110156104b757600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506112a7565b6040518082815260200191505060405180910390f35b61059d600480360361010081101561051057600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919080359060200190929190803515159060200190929190803560ff16906020019092919080359060200190929190803590602001909291905050506112bf565b005b6105a76117fa565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156105e75780820151818401526020810190506105cc565b50505050905090810190601f1680156106145780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6106646004803603602081101561063857600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050611833565b005b6106b26004803603604081101561067c57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050611961565b005b610700600480360360408110156106ca57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050611df4565b604051808215151515815260200191505060405180910390f35b6107666004803603604081101561073057600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050611e09565b005b6107d46004803603606081101561077e57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050611e19565b005b610818600480360360208110156107ec57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050611e2a565b6040518082815260200191505060405180910390f35b6108906004803603604081101561084457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050611e42565b6040518082815260200191505060405180910390f35b6108f2600480360360408110156108bc57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050611e67565b005b6040518060400160405280600e81526020017f44616920537461626c65636f696e00000000000000000000000000000000000081525081565b600081600360003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905092915050565b60015481565b600081600260008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015610adc576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260188152602001807f4461692f696e73756666696369656e742d62616c616e6365000000000000000081525060200191505060405180910390fd5b3373ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff1614158015610bb457507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600360008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205414155b15610db25781600360008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015610cab576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601a8152602001807f4461692f696e73756666696369656e742d616c6c6f77616e636500000000000081525060200191505060405180910390fd5b610d31600360008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483611e77565b600360008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505b610dfb600260008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483611e77565b600260008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610e87600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483611e91565b600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a3600190509392505050565b7fea2aa0a1be11a07ed86d755c93467f4f82362b452371d1ba94d1715123511acb60001b81565b601281565b60055481565b60016000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205414611020576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260128152602001807f4461692f6e6f742d617574686f72697a6564000000000000000000000000000081525060200191505060405180910390fd5b611069600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482611e91565b600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506110b860015482611e91565b6001819055508173ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef836040518082815260200191505060405180910390a35050565b6040518060400160405280600181526020017f310000000000000000000000000000000000000000000000000000000000000081525081565b60016000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205414611215576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260128152602001807f4461692f6e6f742d617574686f72697a6564000000000000000000000000000081525060200191505060405180910390fd5b60016000808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505961012081016040526020815260e0602082015260e0600060408301376024356004353360003560e01c60e01b61012085a45050565b60026020528060005260406000206000915090505481565b60046020528060005260406000206000915090505481565b60006005547fea2aa0a1be11a07ed86d755c93467f4f82362b452371d1ba94d1715123511acb60001b8a8a8a8a8a604051602001808781526020018673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018481526020018381526020018215151515815260200196505050505050506040516020818303038152906040528051906020012060405160200180807f190100000000000000000000000000000000000000000000000000000000000081525060020183815260200182815260200192505050604051602081830303815290604052805190602001209050600073ffffffffffffffffffffffffffffffffffffffff168973ffffffffffffffffffffffffffffffffffffffff16141561148c576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260158152602001807f4461692f696e76616c69642d616464726573732d30000000000000000000000081525060200191505060405180910390fd5b60018185858560405160008152602001604052604051808581526020018460ff1660ff1681526020018381526020018281526020019450505050506020604051602081039080840390855afa1580156114e9573d6000803e3d6000fd5b5050506020604051035173ffffffffffffffffffffffffffffffffffffffff168973ffffffffffffffffffffffffffffffffffffffff1614611593576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260128152602001807f4461692f696e76616c69642d7065726d6974000000000000000000000000000081525060200191505060405180910390fd5b60008614806115a25750854211155b611614576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260128152602001807f4461692f7065726d69742d65787069726564000000000000000000000000000081525060200191505060405180910390fd5b600460008a73ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008154809291906001019190505587146116d6576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260118152602001807f4461692f696e76616c69642d6e6f6e636500000000000000000000000000000081525060200191505060405180910390fd5b6000856116e4576000611706565b7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff5b905080600360008c73ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008b73ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508873ffffffffffffffffffffffffffffffffffffffff168a73ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925836040518082815260200191505060405180910390a350505050505050505050565b6040518060400160405280600381526020017f444149000000000000000000000000000000000000000000000000000000000081525081565b60016000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054146118e7576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260128152602001807f4461692f6e6f742d617574686f72697a6564000000000000000000000000000081525060200191505060405180910390fd5b60008060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505961012081016040526020815260e0602082015260e0600060408301376024356004353360003560e01c60e01b61012085a45050565b80600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015611a16576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260188152602001807f4461692f696e73756666696369656e742d62616c616e6365000000000000000081525060200191505060405180910390fd5b3373ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614158015611aee57507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205414155b15611cec5780600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015611be5576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601a8152602001807f4461692f696e73756666696369656e742d616c6c6f77616e636500000000000081525060200191505060405180910390fd5b611c6b600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482611e77565b600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505b611d35600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482611e77565b600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550611d8460015482611e77565b600181905550600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef836040518082815260200191505060405180910390a35050565b6000611e01338484610a25565b905092915050565b611e14338383610a25565b505050565b611e24838383610a25565b50505050565b60006020528060005260406000206000915090505481565b6003602052816000526040600020602052806000526040600020600091509150505481565b611e72823383610a25565b505050565b6000828284039150811115611e8b57600080fd5b92915050565b6000828284019150811015611ea557600080fd5b9291505056fea265627a7a72315820c0ae2c29860c0a59d5586a579abbcddfe4bcef0524a87301425cbc58c3e94e3164736f6c634300050c0032"
    dai_contract = None

    def __init__(self, private_key=None):
        self.ether_instance = Ethereum()
        self.abi = json.loads(self.abi)
        self.address = Web3.toChecksumAddress(self.address)
        if private_key is not None:
            self.set_current_account(private_key)

    def create_account(self, ether_account_pri_key: str = None):
        if ether_account_pri_key is None:
            self.ether_instance.create_account()
        else:
            self.ether_instance.set_current_account(ether_account_pri_key)
        return {"address": self.ether_instance.current_account.address,
                "private-key": self.ether_instance.current_account.privateKey}

    def set_current_account(self, prik_key: str):
        self.ether_instance.set_current_account(prik_key)
        self.dai_contract = self.ether_instance.web3_instance.eth.contract(
            address=self.address,
            abi=self.abi)
        return self.ether_instance.get_current_account_address()

    def get_current_account_address(self):
        return self.ether_instance.current_account.address

    def get_balance_of(self, address: str = None):
        if address is None:
            return {"amount": self.dai_contract.functions.balanceOf(self.ether_instance.current_account.address).call()}
        return {"amount": self.ether_instance.web3_instance.fromWei(self.dai_contract.functions.balanceOf(
            self.ether_instance.web3_instance.toChecksumAddress(address)).call(), "ether")}

    def get_prik_of_current(self):
        return self.ether_instance.get_current_account_pri_key()

    def transfer(self, to: str, amount: int, private_key: str = None,
                 src: str = None, gas_price=1, gas=70000, chain_id=1):
        if src is None:
            if not self.ether_instance.web3_instance.isChecksumAddress(to):
                to = self.ether_instance.web3_instance.toChecksumAddress(to)
            result = self.dai_contract.functions.transfer(to, amount)
            nonce = self.ether_instance.web3_instance\
                .eth.getTransactionCount(self.ether_instance.get_current_account_address())
        else:
            if not self.ether_instance.web3_instance.isChecksumAddress(to):
                to = self.ether_instance.web3_instance.toChecksumAddress(to)
            if not self.ether_instance.web3_instance.isChecksumAddress(src):
                src = self.ether_instance.web3_instance.toChecksumAddress(src)
            result = self.dai_contract.functions.transferFrom(src, to, amount)
            nonce = self.ether_instance.web3_instance\
                .eth.getTransactionCount(src)
        tx = result.buildTransaction({
            "chainId": chain_id,
            "gas": int(gas),
            "gasPrice": self.ether_instance.web3_instance.toWei(str(gas_price), "gwei"),
            "nonce": nonce
        })
        signed_tx = self.ether_instance\
            .web3_instance.eth.account.sign_transaction(tx,
                                                        private_key=(private_key or
                                                                     self.ether_instance.get_current_account_pri_key()))
        response = self.ether_instance.web3_instance.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"id": self.ether_instance.web3_instance.toHex(response),
                "amount": amount,
                "fee": gas_price,
                "from": src or self.ether_instance.current_account.address,
                "to": to}

    def set_provider(self, url_provider):
        self.ether_instance.set_provider(url_provider)
        self.dai_contract = self.ether_instance.get_smart_contract(address=self.address, abi=self.abi)
        if self.dai_contract is not None and self.ether_instance.web3_instance.isConnected():
            return {"connected": True}
        else:
            return {"connected": False}

    def get_fee(self, gas_used=21000):
        return self.ether_instance.get_fee(gas_used)

    def get_transaction_status(self, tx_hash: str):
        return self.ether_instance.get_transaction_status(tx_hash)
