
### File: app/utils.py

import bip39
from ed25519_hd_key import derive_path
from stellar_sdk import Keypair


def derive_keypair(mnemonic: str) -> Keypair:
    if not bip39.validate_mnemonic(mnemonic):
        raise ValueError("Invalid mnemonic")
    seed = bip39.mnemonic_to_seed(mnemonic)
    derived = derive_path("m/44'/314159'/0'", seed)
    return Keypair.from_raw_ed25519_seed(derived.key)



### Joshua, de hide your seed and important info as you de run this on the web, you may face cyber attack after a successful footprinting
### But sha, I will try give you better code if you tripple my money