import numpy as np
import pandas as pd
import json
from pprint import pprint

CATEGORICAL_FEATURES = ["id", "profileId", "catRefId", "productId", "paymentType", "shippingMethod", "returnReason"]
train_data = './data/final/train-data.csv'
out = './data/final/normalized-train-out.csv'


def remove_first_char(x):
    return int(x.replace('o', ''))


def create_map(features_map):
    for col in cols:
        if col in CATEGORICAL_FEATURES:
            col_list = zip(df_train[col].unique(), range(len(df_train[col].unique())))
            col_map = dict(col_list)
            cat_features_map[col] = col_map

    return features_map


if __name__ == "__main__":
    # df_train = pd.read_csv(train_data)
    # cols = list(df_train.columns)
    # cat_features_map = {}
    # cat_features_map = create_map(cat_features_map)
    #
    # with open('./data/final/feature-unique-key-map.json', 'w') as fp:
    #     # json.dump(cat_features_map, fp)
    #     pprint(cat_features_map, fp)
    #
    # print("found the key-map..")

    # print(cat_features_map)
    # print("Replacing the keys in returnReason..")
    # df_train.replace({'returnReason': cat_features_map['returnReason']}, inplace=True)
    # df_train.to_csv('./data/final/temp.csv')
    #
    # print("Replacing the keys in shippingMethod..")
    # df_train.replace({'shippingMethod': cat_features_map['shippingMethod']}, inplace=True)
    # df_train.to_csv('./data/final/temp.csv')
    #
    # print("Replacing the keys in paymentType..")
    # df_train.replace({'paymentType': cat_features_map['paymentType']}, inplace=True)
    # df_train.to_csv('./data/final/temp.csv')
    #
    # print("Replacing the keys in catRefId..")
    # df_train.replace({'catRefId': cat_features_map['catRefId']}, inplace=True)
    # df_train.to_csv('./data/final/temp.csv')
    #
    # print("Replacing the keys in productId..")
    # df_train.replace({'productId': cat_features_map['productId']}, inplace=True)
    # df_train.to_csv('./data/final/temp.csv')
    #
    # print("Replacing the keys in profileId..")
    # df_train.replace({'profileId': cat_features_map['profileId']}, inplace=True)
    # df_train.to_csv('./data/final/temp.csv')

    # df_train = pd.read_csv('./data/final/temp.csv')
    # print("Replacing the keys in id..")
    # # df_train.replace({'id': cat_features_map['id']}, inplace=True)
    # df_train['id'] = df_train['id'].apply(remove_first_char)
    # df_train.to_csv('./data/final/temp1.csv')

    # f = 0
    # for k, v in cat_features_map['id'].items():
    #     if type(v) != type(int):
    #         print(k, v, type(v))
    #     elif f == 0 and type(v) == type(int):
    #         f = 1
    #         print("*******")
    #         print(k, v, type(v))

    # print(df_train)

    df_train = pd.read_csv('./data/final/unnormalized-train-data.csv')

    print("Normalizing the dataframe..")
    normed_df = (df_train - df_train.min()) / (df_train.max() - df_train.min())
    print("Creating an output file..")
    normed_df.to_csv(out)
