# Make this code dependent of only profiles:Given profile -> fetch listOrders -> fetch orderIds -> fetch complete orders
import json
from pprint import pprint
import requests
import ast

profiles = {"se-570031": "kim", "se-570032": "mark"}
po_map = {"se-570031": "", "se-570032": ""}

with open('./data/kimOrders.json') as f:
    kim = json.load(f)

with open('./data/markOrders.json') as f:
    mark = json.load(f)

print("")

items = kim.items()
for w in items:
    if w[0] == 'items':
        po_map["se-570031"] = w[1]

items = mark.items()
for w in items:
    if w[0] == 'items':
        po_map["se-570032"] = w[1]

# only for kim
order_list = []
for order in po_map["se-570031"]:
    order_list.append(order["orderId"])

# pprint(order_list)

file = "./data/complete-orders-se-570031.json"
complete_order_list = []

payload = {'grant_type': 'password', 'username': 'kim@example.com', 'password': 'Oracle@123'}
loginurl = "http://localhost:8080/ccstoreui/v1/login/"
x = requests.post(loginurl, data=payload)
# print(x.status_code)
# pprint(json.loads(x.content)['access_token'])
access_token = json.loads(x.content)['access_token']
# o = input()


for order in order_list:
    requrl = "http://localhost:8080/ccstoreui/v1/orders/" + order
    headers = {'Authorization': "Bearer " + access_token}
    x = requests.get(requrl, headers=headers)
    print(order, x.status_code)
    # print(x.content)
    complete_order_list.append(json.loads(x.content))
    # o = input()

print(len(complete_order_list))

order_data = json.dumps(complete_order_list)

with open(file,'w+') as f:
    f.write(order_data)
f.close()

