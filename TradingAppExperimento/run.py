from metaapi_cloud_sdk import MetaApi
import asyncio

token = '5dc8e4fd-b397-48c2-9250-9b8cba28d193'
account_id = '73033338'

api = MetaApi(token)
account = api.get_account(account_id)

balance = account.get_summary().balance
print(f"Balance actual: {balance}")


def on_balance_update(balance):
    print(f"Nuevo balance: {balance}")

if __name__ == "__main__":
    asyncio.run(main())