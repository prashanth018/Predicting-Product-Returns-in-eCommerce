import json
from pprint import pprint
import csv

file = "./data/complete-orders-se-570031.json"

with open(file) as f:
    orders = json.load(f)

pprint(orders[30])

test_file = open('./data/test.csv', 'w', newline='')
file_writer = csv.writer(test_file)

record = ('orderId', 'orderProfileId', 'catRefId', 'productId', 'listPrice', 'quantity', 'amount', 'paymentMethod',
          'shippingMethod', 'shippingCost', 'creationTime')

file_writer.writerow(record)
ct = 0
for order in orders:
    n_line_items = len(order['order']['items'])
    num_order_items = sum([order['order']['items'][ind_line_item]['quantity'] for ind_line_item in range(n_line_items)])
    for ind_line_item in range(n_line_items):
        line_item = order['order']['items'][ind_line_item]
        record = (order['id'], order['orderProfileId'], line_item['catRefId'], line_item['productId'],
                  line_item['listPrice'], line_item['quantity'], line_item['price'],
                  order['payments'][0]['paymentMethod'], order['shippingMethod']['value'],
                  order['shippingMethod']['cost'] * (line_item['quantity'] / num_order_items), order['creationTime'])
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
