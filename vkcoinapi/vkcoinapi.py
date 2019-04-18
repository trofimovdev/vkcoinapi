from time import sleep
from requests import post
from random import randint
from websocket import *
import json

class VKCoin():
    def __init__(self,
                 key,
                 merchantId,
                 token = ''):
            self.key = key
            self.merchantId = merchantId
            self.appId = 6915965
            self.url = 'https://coin-without-bugs.vkforms.ru/merchant'
            self.token = token
            self.v = '5.92'
            if self.token != '':
                self.wss_url = post('https://api.vk.com/method/apps.get',
                                    data = {'app_id': self.appId,
                                            'access_token': self.token,
                                            'v': self.v})\
                               .json()\
                               .get('response')\
                               .get('items')[0]\
                               .get('mobile_iframe_url')\
                               .replace('https', 'wss')\
                               .replace('index.html', 'channel/{}'.format(str(self.merchantId) % 32))\
                               + '&ver=1&upd=1&pass={}'.format(str(int(self.merchantId) - 1))

    def getPaymentURL(self,
                        amount,
                        payload = randint(-2000000000, 2000000000),
                        free = False):
        if free == False:
            return 'https://vk.com/coin#x{}_{}_{}'.format(str(self.merchant_id),
                                                          str(amount),
                                                          str(payload))
        else:
            return 'https://vk.com/coin#x{}_{}_{}_1'.format(str(self.merchantId),
                                                            str(amount),
                                                            str(payload))

    def getTransactions(self,
                        type = 2):
        transactions = post('{}/tx/'.format(self.url),
                            headers = {'Content-Type': 'application/json'},
                            json = {'merchantId': self.merchantId,
                                    'key': self.key,
                                    'tx': [type]}).json()
        return transactions

    def sendPayment(self,
                    to,
                    amount):
        response = post('{}/send/'.format(self.url),
                        headers = {'Content-Type': 'application/json'},
                        json = {'merchantId': self.merchantId,
                                'key': self.key,
                                'toId': to,
                                'amount': amount}).json()
        return response

    def getBalance(self,
                   user_ids = []):
        response = post('{}/score/'.format(self.url),
                        headers = {'Content-Type': 'application/json'},
                        json = {'userIds': [self.merchantId]
                                           if len(user_ids) == 0
                                           else user_ids,
                                'merchantId': self.merchantId,
                                'key': self.key}).json()
        return response

    def longPoll(self):
        if self.wss_url:
            self.ws = create_connection(self.wss_url)
            while True:
                try:
                    response = self.ws.recv()
                    if response.startswith('TR'):
                        response = response.split()
                        return {'response': {'from': int(response[2]), 'amount': int(response[1]), 'payload': int(response[3])}}
                        break
                except Exception as e:
                    self.ws = create_connection(self.wss_url)
                sleep(0.1)
        else:
            raise Exception('token is not defined')

    def getTop(self, type = 'group'):
        self.ws = create_connection(self.wss_url)
        response = json.loads(self.ws.recv())\
                  .get('top')\
                  .get('{}Top'.format(type))
        return response
