import pandas_ta as ta
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import Previsao as p

data_5m = p.data_5m
data_30m = p.data_30m
data_1h = p.data_1h
data_daily = p.data_daily

# Calcular indicadores técnicos usando pandas_ta
data_5m['SMA_5m'] = ta.sma(data_5m['close'], length=30)
data_30m['SMA_30m'] = ta.sma(data_30m['close'], length=30)
data_1h['SMA_1h'] = ta.sma(data_1h['close'], length=30)
data_daily['SMA_daily'] = ta.sma(data_daily['close'], length=30)

data_5m['RSI_5m'] = ta.rsi(data_5m['close'], length=14)
data_30m['RSI_30m'] = ta.rsi(data_30m['close'], length=14)
data_1h['RSI_1h'] = ta.rsi(data_1h['close'], length=14)
data_daily['RSI_daily'] = ta.rsi(data_daily['close'], length=14)

# Preparar dados para machine learning
df = data_5m.join(data_30m[['SMA_30m', 'RSI_30m']], how='inner', rsuffix='_30m')
df = df.join(data_1h[['SMA_1h', 'RSI_1h']], how='inner', rsuffix='_1h')
df = df.join(data_daily[['SMA_daily', 'RSI_daily']], how='inner', rsuffix='_daily')
df.dropna(inplace=True)

X = df[['SMA_5m', 'RSI_5m', 'SMA_30m', 'RSI_30m', 'SMA_1h', 'RSI_1h', 'SMA_daily', 'RSI_daily']]
y = df['close']

# Dividir em treino e teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Treinar modelo
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Fazer previsões
predictions = model.predict(X_test)

print(data_daily)
print(data_1h)
# Avaliar o modelo
plt.figure(figsize=(14, 5))
plt.plot(df.index[train_size:], y_test, color='blue', label='Preço Real')
plt.plot(df.index[train_size:], predictions, color='red', label='Previsão')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.legend()
plt.show()