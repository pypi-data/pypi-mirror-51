from bitrue.client import Client

if __name__ == '__main__':
    client = Client(api_key='',
                    api_secret='',
                    )


    trades = client.get_my_trades()
    print(client._order_format_print(trades))


'''
symbol         id    orderId  origClientOrderId          price         qty  commission    commissionAssert             time  isBuyer    isMaker    isBestMatch
--------  -------  ---------  -------------------  -----------  ----------  ------------  ------------------  -------------  ---------  ---------  -------------
HOTXRP    1583958   53673021                         0.004473      717                                        1559843532000  True       True       True

'''
