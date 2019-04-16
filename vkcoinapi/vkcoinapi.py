from requests import post
from random import randint

class VKCoin():
    def __init__(self,
                 token,
                 merchant_id):
            self.token = token
            self.merchant_id = merchant_id

    def getPaymentURL(self,
                      amount,
                      payload = randint(-2000000000, 2000000000),
                      free = False):
        if free == False:
            return 'https://vk.com/coin#x{}_{}_{}'.format(self.merchant_id,
                                                          amount,
                                                          payload)
        else:
            return 'https://vk.com/coin#x{}_{}_{}_1'.format(self.merchant_id,
                                                            amount,
                                                            payload)

    def getTransactions(self,
                        type = 2):
        transactions = post('https://coin-without-bugs.vkforms.ru/merchant/tx/',
                            headers = {'Content-Type': 'application/json'},
                            json = {'merchantId': self.merchant_id,
                                    'key': self.token,
                                    'tx': [type]}).json()
        return transactions

    def sendPayment(self,
                    to,
                    amount):
        response = post('https://coin-without-bugs.vkforms.ru/merchant/send/',
                            headers = {'Content-Type': 'application/json'},
                            json = {'merchantId': self.merchant_id,
                                    'key': self.token,
                                    'toId': to,
                                    'amount': amount}).json()
        return response

    def getBalance(self,
                   user_ids = []):
        response = post('https://coin-without-bugs.vkforms.ru/merchant/score/',
                            headers = {'Content-Type': 'application/json'},
                            json = {'userIds': [self.merchant_id]
                                               if len(user_ids) == 0
                                               else user_ids,
                                    'merchantId': self.merchant_id,
                                    'key': self.token}).json()
        return response
