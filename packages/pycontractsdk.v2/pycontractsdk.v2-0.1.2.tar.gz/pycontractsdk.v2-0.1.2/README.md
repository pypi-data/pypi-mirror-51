# 调用solidity智能协约的SDK

需要python3.6的环境

## 封装的第三方的类库
* web3.py (https://web3py.readthedocs.io/en/stable/)
* eth-hash (https://eth-hash.readthedocs.io/en/latest/)
* eth_account (https://eth-account.readthedocs.io/en/latest/)
* eth-abi (https://eth-abi.readthedocs.io/en/latest/)
* eth-keyfile (https://pypi.org/project/eth-keyfile/)
* eth-keys (https://pypi.org/project/eth-keys/)
* eth-utils (https://eth-utils.readthedocs.io/en/latest/)

## 安装virtualenv
```bash
$ pip install virtualenv
$ virtualenv --no-site-packages venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

## 便于开发SDK的使用方式
```bash
$ cd $youProjPath
$ . ./venv/bin/activiate
$ cd $pyconstractsdk_path
$ python setup.py develop

```

## 使用的第三方的加密解密模块
```bash
$ npm i -g crypto-tx
```

## 调用方法
* 协约的方法
```
    function submitProof(address creator, uint level, bytes32 proofHash, bytes metaData) {
        NewProof(creator, proofHash, metaData);
    }
```

```python
from pycontractsdk import contracts, utils, keys
from pycontractsdk.mycontracts.proof import Proof

def call_function():
    # localhost
    web3_url = "http://127.0.0.1:7545"
    contract_address = "0x0244e9041ad185b1e92dfc94d457810e76ce1eab"
    private_key = "62e7920d4045e90316a1cf0dd5813da612b7602d2b77d9d19360ef6fc18aeef1"
    abi_file = "../contracts/DigitalProof.json"


    # 读取abi文件活儿abi数据
    abi = utils.get_abi(abi_file)

    contract = contracts.Contract(web3_url, contract_address=contract_address, abi=abi, private_key=private_key)
    # 参数是 address 必须是 check_sum 的
    check = keys.to_check_sum_address('0xb244134f7b7568a8660aa98c550091bc1b5a25a2')
    
    # False：上链后不等待
    print(contract.call_function('submitProof', False,
                            check, 1, b'proofHash', b'metaData'))
    
    # 上链后 等待 返回（tf, txid, receipt）
    # tf: 是否上链成功
    # txid: 交易hash
    # receipt: 交易收据
    # 'submitProof' : 协约的方法名称
    # '0xB244134f7b7568A8660Aa98C550091BC1B5a25A2', 1, b'proofHash', b'metaData' ： 协约的参数
    print(contract.call_function_wait('submitProof', '0xB244134f7b7568A8660Aa98C550091BC1B5a25A2', 1, b'proofHash', b'metaData'))
    
    # 上链后 不等待 直接返回（tf, txid, receipt）
    # tf: 是否上链成功
    # txid: 交易hash
    # receipt: 交易收据
    print(contract.call_function_nowait('submitProof', '0xB244134f7b7568A8660Aa98C550091BC1B5a25A2', 1, b'proofHash', b'metaData'))



if __name__ == "__main__":
    call_function()
```