import pandas as pd
import json
from pprint import pprint

# train_data = './normalized-train-out.csv'
#
# df = pd.read_csv(train_data)
# df['returnReason'] = round(df['returnReason'] * 3)
#
# df.to_csv(train_data)


df = pd.read_csv('./train-data.csv')

#
# df.describe().loc[['min', 'max']].to_json('./minmax.json')
# categorical_key_map = './feature-unique-key-map.json'
#
# with open(categorical_key_map) as fa:
#     s = fa.read()
#     s = s.replace("\'", '\"')
#     print(s[:3000])
#     cat_key_map = json.loads(s)
#     fa = open('./feature-unique-key-map1.json', 'w')
#     json.dump(cat_key_map, fa, indent = 4)

# fa = open(categorical_key_map, 'r')
# s = fa.read()
# s = s.replace("\'", '\"')
# s = s[:4000]
# with open('./feature-unique-key-map1.json', 'w') as fb:
#     json.dump(s, fb, ensure_ascii=False, indent=4)


# g = df.groupby(["profileId", "returnReason"])
# d = g.aggregate(len)
# print(d.reset_index().rename(columns={"id": "num_entries"}))
# # print(g.groups)


# grouped = df.groupby(["profileId", "returnReason"]).number.unique()
# for k, v in grouped.items():
#     print(k, len(v))


g = df.groupby(["profileId", "returnReason"])
dt = {}
for p in g.groups:
    if p[0] not in dt:
        dt[p[0]] = {p[1]: len(g.groups[p])}
    elif p[0] in dt:
        dt[p[0]][p[1]] = len(g.groups[p])
    # print(p, len(g.groups[p]))

lt = []
for k in dt.keys():
    sm = sum(dt[k].values())
    for _ in dt[k].keys():
        dt[k][_] /= float(sm)
        if _ not in ['Fitting issues', "Didn't like the product", "Bad product quality"]:
            lt.append((k, dt[k][_]))
    # if k == "se-1000":
    #     print(dt[k])

lt.sort(key=lambda tup: tup[1], reverse=True)

for w in lt:
    print(w)