
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

training_set = pd.read_csv('Google_Stock_Price_Train.csv')
training_set = training_set.iloc[:, 1:2].values


sc = MinMaxScaler()
training_set_scaled = sc.fit_transform(training_set)

X_train = training_set_scaled[0:1257]
Y_train = training_set_scaled[1:1258]

X_train = np.reshape(X_train,(1257, 1, 1))

regressor = Sequential()
regressor.add(LSTM(units = 50, activation='relu', return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1, activation='sigmoid'))


regressor.compile(optimizer = 'adam', loss = 'mse')


regressor.fit(X_train, Y_train, epochs = 1000, batch_size = 32 )

df = pd.read_csv('Google_Stock_Price_Test.csv')

test_set = sc.fit_transform(df.iloc[:, 1:2])
test_set = np.reshape(test_set, (20, 1, 1))

prediction = regressor.predict(test_set)
prediction = sc.inverse_transform(prediction)

real_price = df.iloc[:, 1:2]

plt.plot(real_price, color = 'red', label = 'Real stock price')
plt.plot(prediction, color = 'blue', label = 'Predicted stock price')
plt.legend()
plt.show()