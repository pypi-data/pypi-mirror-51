from bitrue.client import Client
import pandas as pd
import time
if __name__ == '__main__':
    client = Client(api_key='',
                    api_secret='',
                    )

    #
    # trades = client.get_my_trades()
    # df = pd.DataFrame(trades)
    # df = df[['symbol','id','orderId','origClientOrderId','price','qty','commission','commissionAssert','time','isBuyer','isMaker','isBestMatch']]
    # df.to_csv('bitrue_trades.csv', sep=',', encoding='utf-8')
    #
    #
    while True:
        time.sleep(100)