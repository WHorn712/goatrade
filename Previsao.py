import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.api.layers import Dense
from keras.api import Sequential
from keras.api.layers import LSTM

# Inicializar MetaTrader 5
mt5.initialize()

# Função para obter dados históricos
def get_data(symbol, timeframe, n):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

# Obter dados históricos para diferentes timeframes
symbol = "EURUSD"
data_5m = get_data(symbol, mt5.TIMEFRAME_M5, 1000)
data_30m = get_data(symbol, mt5.TIMEFRAME_M30, 1000)
data_1h = get_data(symbol, mt5.TIMEFRAME_H1, 1000)
data_daily = get_data(symbol, mt5.TIMEFRAME_D1, 1000)

# Preparar os dados
data = data_5m['close'].values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Criar conjuntos de treino e teste
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

# Criar sequências de dados para LSTM
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

seq_length = 60
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# Construir o modelo LSTM
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(seq_length, 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Treinar o modelo
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Fazer previsões
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# Avaliar o modelo
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 5))
plt.plot(data_5m.index[train_size + seq_length:], data[train_size + seq_length:], color='blue', label='Preço Real')
plt.plot(data_5m.index[train_size + seq_length:], predictions, color='red', label='Previsão')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.legend()
plt.show()







