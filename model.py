import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Input
import matplotlib.pyplot as plt

import pandas as pd
import json
from pprint import pprint


def return_one_hot(val):
    try:
        abc = np.eye(4)[val]
        return abc
    except:
        print(val)


train_data = './data/final/normalized-train-out.csv'

df = pd.read_csv(train_data)

# del df['Id']


split = int(len(df) * 0.8)

x = df[:].copy()
y_returned = x['returned']
y_return_reason = x['returnReason']

del x['returned']
del x['returnReason']

x_train = x[:split]
x_test = x[split:]

y_returned_train = y_returned[:split]
y_returned_test = y_returned[split:]

y_return_reason = y_return_reason.astype(int)
print(y_return_reason.unique())
y_return_reason = np.apply_along_axis(return_one_hot, 0, np.asarray(y_return_reason.tolist()))

y_return_reason_train = y_return_reason[:split]
y_return_reason_test = y_return_reason[split:]

# x_train = df[:split].copy()
# y_train = x_train['returned']
# del x_train['returned']
#
# x_test = df[split:].copy()
# y_test = x_test['returned']
# del x_test['returned']

# print(x_train, y_train)
# print(df.info())
print(x_train.shape, y_returned_train.shape, y_return_reason_train.shape)
print(x_test.shape, y_returned_test.shape, y_return_reason_test.shape)
# print(x_train[:1])
# o = input()
# print(np.array(x_train), np.array(y_train))
# print(np.array(x_test), np.array(y_test))

input = Input(shape=(9,))
dense1 = Dense(200, kernel_initializer='normal', activation='relu')(input)
dense2 = Dense(100, kernel_initializer='normal', activation='relu')(dense1)
dense3 = Dense(50, kernel_initializer='normal', activation='relu')(dense2)
dense4 = Dense(25, kernel_initializer='normal', activation='relu')(dense3)
return_prob = Dense(1, kernel_initializer='normal', name="return_prob", activation='sigmoid')(dense4)
return_reason = Dense(units=4, kernel_initializer='normal', name='return_reason', activation='softmax')(dense4)

model = Model(inputs=input, outputs=[return_prob, return_reason])

model.compile(optimizer='adam',
              loss={'return_prob': 'binary_crossentropy', 'return_reason': 'categorical_crossentropy'},
              metrics={'return_prob': 'accuracy', 'return_reason': 'accuracy'})

history = model.fit(np.array(x_train), [np.array(y_returned_train), y_return_reason_train], epochs=10, batch_size=128,
                    validation_split=0.33)

print(history.history.keys())
model.save_weights("./model/model_v6.h5")

# model.load_weights("./model/model_v4.h5")

# summarize history for return_prob_accuracy
plt.plot(history.history['return_prob_acc'])
plt.plot(history.history['val_return_prob_acc'])
print("return_prob_acc: ", history.history['return_prob_acc'])
print("val_return_prob_acc: ", history.history['val_return_prob_acc'])
plt.title('model return_prob accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for return_reason_accuracy
plt.plot(history.history['return_reason_acc'])
plt.plot(history.history['val_return_reason_acc'])
print("return_reason_acc: ", history.history['return_reason_acc'])
print("val_return_reason_acc: ", history.history['val_return_reason_acc'])
plt.title('model return_reason accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for return_prob_loss
plt.plot(history.history['return_prob_loss'])
plt.plot(history.history['val_return_prob_loss'])
plt.title('model return_prob_loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for return_reason_loss
plt.plot(history.history['return_reason_loss'])
plt.plot(history.history['val_return_reason_loss'])
plt.title('model return_reason_loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

y_pred = model.predict(np.array(x_test))
# for rec in zip(y_pred, y_test):
#     print(rec)
print(y_pred)

y_test = [np.array(y_returned_test), y_return_reason_test]
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

y_returned_test = np.array(y_returned_test)
y_returned_test = y_returned_test.reshape((y_returned_test.shape[0], 1))
print("number of actual returns: ", sum(y_returned_test))
print("number of predicted returns: ", sum(np.round(y_pred[0])))

print("total miss predictions: ", sum(np.round(y_pred[0]) - y_returned_test))
# plt.scatter(y_pred, y_test)
# plt.show()
# predictions = list(itertools.islice(y_test, x_test.shape[0]))
