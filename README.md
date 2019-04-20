# vkcoinapi
Обертка над VK Coin API на Python
# Установка
```python
pip3 install vkcoinapi
```
# Использование
Перед началом необходимо создать экземпляр класса **VKCoin**.
Он принимает 2 аргумента:


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|key|<p align="center">str</p>|<p align="center">+</p>|Ключ доступа к VK Coin, полученный здесь: [vk.com/coin#create_merchant](https://vk.com/coin#create_merchant)|
|merchantId|<p align="center">int</p>|<p align="center">+</p>|ID пользователя ВКонтакте, для которого получен ключ|
|token|<p align="center">str</p>|<p align="center">—</p>|Токен, полученный из URL адреса [здесь](https://oauth.vk.com/authorize?client_id=6334949&scope=1073737727&redirect_uri=https://api.vk.com/blank.html&display=page&response_type=token&revoke=1). Необходим только при использовании longPoll() и getTop().|
```python
from vkcoinapi import *
coin = VKCoin(key = 'ваш_ключ', merchantId = ваш_id)
```
После этого становятся доступны следующие методы, которые возвращают JSON словарь:
## getPaymentURL()
Возвращает ссылку на перевод вида `https://vk.com/coin#xВАШID_СУММА_PAYLOAD`.\
Если необходимо, чтобы пользователь мог изменить сумму перевода, то в конец добавляется `_1`.


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|amount|<p align="center">int</p>|<p align="center">+</p>|Сумма перевода.|
|payload|<p align="center">int</p>|<p align="center">—</p>|Любое число от `-2000000000` до `2000000000`, вернется вам в списке транзаций. Если не указано, отправляется случайное число.|
|free|<p align="center">bool</p>|<p align="center">—</p>|Может ли пользователь изменять сумму перевода. По умолчанию `False`.
```python
coin.getPaymentURL(1000)
>>> 'https://vk.com/coin#xВАШID_1000_PAYLOAD'
```
**Обратите внимание, что сумма указывается в тысячных долях.**\
В примере выше 1000 = 1 VK Coin.
Т.е., для того, чтобы отправить 0,001 VK Coin, нужно указать `1`.


## getTransactions()
Возвращает список транзакций.


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|type|<p align="center">int</p>|<p align="center">—</p>|1 — вернутся 1000 последних транзакций **со ссылки на оплату**<br>2 — вернутся 100 последних транзакций<br>По умолчанию `2`.|
```python
coin.getTransactions()
>>> {'response': [
                  {'id': 1370037,
                   'from_id': 1,
                   'to_id': 2,
                   'amount': '100',
                   'type': 3,
                   'payload': 1,
                   'external_id': 0,
                   'created_at': 1555369262},
                  {'id': 1369973,
                   'from_id': 2,
                   'to_id': 1,
                   'amount': '100',
                   'type': 3,
                   'payload': 1,
                   'external_id': 0,
                   'created_at': 1555369272}
                  ]}
```
## sendPayment()
Отправляет перевод.


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|to|<p align="center">int</p>|<p align="center">+</p>|ID пользователя, кому отправляем перевод.|
|amount|<p align="center">int</p>|<p align="center">+</p>|Сумма перевода.|
```python
coin.sendPayment(1, 100)
>>> {'response': {'id': 1400290, 'amount': 100, 'current': 578637358}}
```
## getBalance()
Позволяет получить баланс пользователей.


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|user_ids|<p align="center">list</p>|<p align="center">—</p>|ID пользователей, для которых нужно узнать баланс.<br>По умолчанию — наш ID.|
```python
coin.getBalance()
>>> {'response': {'165275777': 578637358}}

coin.getBalance([1, 1324639])
>>> {'response': {'1': 92697214157, '1324639': 6935662916530}}
```

## getTop()
Возвращает список текущего топа.


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|type|<p align="center">str</p>|<p align="center">—</p>|Тип возвращаемого топа (`group` или `user`).<br>По умолчанию — `group`.|

```python
coin.getTop()
>>> [
     {'id': 67580761,
      'score': 473553513081870,
      'name': 'КБ',
      'screen_name': 'countryballs_re',
      'is_closed': 0,
      'type': 'page',
      'photo_200': 'https://sun9-18.userapi.com/c850420/v850420990/ff275/6svrAL6jtME.jpg?ava=1',
      'link': 'https://vk.com/club67580761'},
     {'id': 98699940,
     'score': 473550301524363,
     'name': "Bratishkin's Stream",
     'screen_name': 'bratishkinoff',
     'is_closed': 0,
     'type': 'page',
     'photo_200': 'https://sun9-9.userapi.com/c851416/v851416466/fcfa5/LZGnlIJVEBw.jpg?ava=1',
     'link': 'https://vk.com/club98699940'}
    ]
```
## longPoll()
Блокирующий «longpoll». Не принимает аргументов.<br>
При появлении новой входящей транзакции возвращает следующий словарь:


|Ключ|Тип|Описание|
|-|-|-|-|
|from|<p align="center">int</p>|ID пользователя, от которого пришел платеж.|
|amount|<p align="center">int</p>|Сумма платежа.|
|payload|<p align="center">int</p>|Payload для нахождения платежа в истории.|

```python
coin.longPoll()
>>> {'response': {'from': 165275777, 'amount': 1, 'payload': 1624215}}
```
## setShopName()
Изменяет название магазина.


|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|name|<p align="center">str</p>|<p align="center">+</p>|Новое название магазина.|

```python
coin.setShopName('My Shop')
>>> {'response': '1'}
```
## setCallback()
Изменяет адрес для callback запросов.

|Аргумент|Тип|Обязательный|Описание|
|-|-|-|-|
|callback|<p align="center">str</p>|<p align="center">—</p>|Адрес для callback запросов.<br>Если не передан, callback выключается (передается `none`).|

```python
coin.setCallback('https://example.com/callback')
>>> {'response': 'ON'}

coin.setCallback()
>>> {'response': 'OFF'}
```
# Ссылки
* Я ВКонтакте: [vk.com/bixnel](https://vk.com/bixnel)
* Подробнее про VK Coin API: [vk.com/@hs-marchant-api](https://vk.com/@hs-marchant-api)
