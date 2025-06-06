
### File: app/pi_worker.py

import asyncio
from stellar_sdk import Server, TransactionBuilder, Network, Asset, Operation
from stellar_sdk.exceptions import NotFoundError
from .config import HORIZON_URL, NETWORK_PASSPHRASE, MINIMUM_BALANCE, FEE_PERCENT
from .utils import derive_keypair

server = Server(HORIZON_URL)


async def get_balance(public_key: str) -> float:
    try:
        account = await server.accounts().account_id(public_key).call()
        balance = next(
            (b["balance"] for b in account["balances"] if b["asset_type"] == "native"),
            "0",
        )
        return float(balance)
    except NotFoundError:
        return 0.0


async def transfer_pi(seed: str, destination: str, amount: float) -> str:
    kp = derive_keypair(seed)
    balance = await get_balance(kp.public_key)

    if balance < MINIMUM_BALANCE:
        return f"Seed {kp.public_key} has insufficient balance: {balance} PI"

    fee_amount = amount * FEE_PERCENT
    send_amount = round(amount - fee_amount, 7)

    account = await server.load_account(kp.public_key)
    base_fee = await server.fetch_base_fee()

    tx = (
        TransactionBuilder(account, NETWORK_PASSPHRASE, base_fee)
        .add_text_memo("PI Transfer")
        .add_operation(
            Operation.payment(destination=destination, asset=Asset.native(), amount=str(send_amount))
        )
        .set_timeout(30)
        .build()
    )

    tx.sign(kp)
    response = await server.submit_transaction(tx)
    return f"Success for {kp.public_key}: {response['hash']}"


async def process_all_seeds(seeds: list[str], destination: str, amount: float) -> list[str]:
    results = []
    for seed in seeds:
        try:
            result = await transfer_pi(seed, destination, amount)
        except Exception as e:
            result = f"Error for seed: {str(e)}"
        results.append(result)
        await asyncio.sleep(0.005)  # 5ms between each to avoid rate limits
    return results

# See ba, I de avoid those network latency issues

