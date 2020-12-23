import json
from pprint import pprint
import csv

file = "./data/final/orders-generated.json"

with open(file) as f:
    orders = json.load(f)

# pprint(orders[30])
# o = input()
print("orders: ", len(orders))

test_file = open('./data/final/train-data.csv', 'w', newline='')
file_writer = csv.writer(test_file)

record = ('orderId', 'orderProfileId', 'catRefId', 'productId', 'listPrice', 'quantity', 'amount', 'paymentMethod',
          'shippingMethod', 'shippingCost', 'creationTime')

record = (
    'id', 'profileId', 'catRefId', 'productId', 'itemPrice', 'quantity', 'amount', 'paymentType', 'shippingMethod',
    'shippingCost', 'returnReason', 'returned')

file_writer.writerow(record)
ct = 0
for order in orders:
    if ct % 10000 == 0:
        print("processed ", ct)
    n_line_items = len(order['items'])
    num_order_items = sum([order['items'][ind_line_item]['quantity'] for ind_line_item in range(n_line_items)])
    for ind_line_item in range(n_line_items):
        line_item = order['items'][ind_line_item]
        returned = 0
        returnReason = "NA"
        if 'returned' in line_item and line_item['returned']:
            returned = 1
            returnReason = line_item['returnReason']

        record = (order['id'], order['profileId'], line_item['catRefId'], line_item['productId'],
                  line_item['price'], line_item['quantity'], order['amount'],
                  order['paymentType'], order['shipping']['shippingMethod'],
                  order['shipping']['price'] * (line_item['quantity'] / num_order_items), returnReason, returned)
        file_writer.writerow(record)
        ct += 1

print("total records: ", ct)
test_file.close()

'''
id

orderProfileId

creationTime

order
    iterate over len(order[items]) -> separate records
        amount -- can this be omitted?
        catRefId
        productId
        listPrice
        quantity

payments -> didn't handle case for multi payment
    paymentMethod

priceListGroup
    currency
        numericCode

shippingMethod
    cost (given val * quantity/(all the items in the order))
    value

'''
