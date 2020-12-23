import json
from pprint import pprint
import csv
import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Input
from keras import backend as K
import matplotlib.pyplot as plt
from util import profiles, score
import util


def predict(req):
    file = "./input.json"
    categorical_key_map = './data/final/feature-unique-key-map.json'
    min_max_values = './data/final/minmax.json'

    sku_items = []

    request = req

    with open(categorical_key_map) as fa:
        cat_key_map = json.load(fa)

    with open(min_max_values) as fb:
        min_max_val = json.load(fb)

    rep_score = ""
    record = (
        'id', 'profileId', 'catRefId', 'productId', 'itemPrice', 'quantity', 'amount', 'paymentType', 'shippingMethod',
        'shippingCost')
    if request['profileId'] in profiles:
        rep_score = "rep_sc"
    # 'returnReason', 'returned'

    records = []

    n_line_items = len(request['items'])
    num_order_items = sum([request['items'][ind_line_item]['quantity'] for ind_line_item in range(n_line_items)])
    for ind_line_item in range(n_line_items):
        line_item = request['items'][ind_line_item]
        sku_items.append(line_item['catRefId'])

        if request['shipping']['shippingMethod'] == "freeShippingMethod":
            request['shipping']['shippingMethod'] = "Free"
        elif request['shipping']['shippingMethod'] == "overNightShippingMethod":
            request['shipping']['shippingMethod'] = "Overnight"
        elif request['shipping']['shippingMethod'] == "standardShippingMethod":
            request['shipping']['shippingMethod'] = "Standard"

        records.append([request['id'], request['profileId'], line_item['catRefId'], line_item['productId'],
                        line_item['price'], line_item['quantity'], request['amount'],
                        request['shipping']['shippingMethod'],
                        request['shipping']['price'] * (line_item['quantity'] / num_order_items)])

    for ind in range(len(records)):
        record = records[ind]
        record[0] = int(record[0].replace('o', ''))
        record[0] = (record[0] - min_max_val['id']['min']) / (
                min_max_val['id']['max'] - min_max_val['id']['min'])

        record[1] = cat_key_map['profileId'][record[1]]
        record[1] = (record[1] - min_max_val['profileId']['min']) / (
                min_max_val['profileId']['max'] - min_max_val['profileId']['min'])

        record[2] = cat_key_map['catRefId'][record[2]]
        record[2] = (record[2] - min_max_val['catRefId']['min']) / (
                min_max_val['catRefId']['max'] - min_max_val['catRefId']['min'])

        record[3] = cat_key_map['productId'][record[3]]
        record[3] = (record[3] - min_max_val['productId']['min']) / (
                min_max_val['productId']['max'] - min_max_val['productId']['min'])

        record[4] = (record[4] - min_max_val['itemPrice']['min']) / (
                min_max_val['itemPrice']['max'] - min_max_val['itemPrice']['min'])

        record[5] = (record[5] - min_max_val['quantity']['min']) / (
                min_max_val['quantity']['max'] - min_max_val['quantity']['min'])

        record[6] = (record[6] - min_max_val['amount']['min']) / (
                min_max_val['amount']['max'] - min_max_val['amount']['min'])

        record[7] = cat_key_map['shippingMethod'][record[7]]
        record[7] = (record[7] - min_max_val['shippingMethod']['min']) / (
                min_max_val['shippingMethod']['max'] - min_max_val['shippingMethod']['min'])

        record[8] = (record[8] - min_max_val['shippingCost']['min']) / (
                min_max_val['shippingCost']['max'] - min_max_val['shippingCost']['min'])

    # pprint(records)
    print(np.array(records))

    input = Input(shape=(9,))
    # dense1 = Dense(200, kernel_initializer='normal', activation='relu')(input)
    dense2 = Dense(100, kernel_initializer='normal', activation='relu')(input)
    dense3 = Dense(50, kernel_initializer='normal', activation='relu')(dense2)
    dense4 = Dense(25, kernel_initializer='normal', activation='relu')(dense3)
    return_prob = Dense(1, kernel_initializer='normal', name="return_prob", activation='sigmoid')(dense4)
    return_reason = Dense(units=4, kernel_initializer='normal', name='return_reason', activation='softmax')(dense4)

    model = Model(inputs=input, outputs=[return_prob, return_reason])

    model.compile(optimizer='adam',
                  loss={'return_prob': 'binary_crossentropy', 'return_reason': 'categorical_crossentropy'},
                  metrics={'return_prob': 'accuracy', 'return_reason': 'accuracy'})

    model.load_weights("./model/model_v5.h5")

    y_pred = model.predict(np.array(records))

    K.clear_session()

    print(y_pred[0], y_pred[1])

    response = {}
    ind = 0
    return_res_map = cat_key_map['returnReason']
    inv_return_res_map = {v: k for k, v in return_res_map.items()}

    # print("*******", len(sku_items))
    for ind in range(len(sku_items)):
        ret_prob, ret_reason = y_pred[0][ind], y_pred[1][ind]
        ret_prob, ret_reason = util.validate(rep_score, ret_prob, ret_reason)
        print(ret_prob, ret_reason)
        reason = inv_return_res_map[np.argmax(ret_reason)]
        if reason == "nan":
            reason = ""
        response[sku_items[ind]] = {"score": str(ret_prob[0]), "reason": reason}

    pprint(response)
    return response