import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import streamlit as st
import yfinance as yf

# from keras.layers import Dense, Dropout, LSTM
# from keras.models import Sequential

start ="2010-01-01"
end ="2024-05-05"

st.title('Stock Trend Prediction')

user_input = st.text_input('Enter Stock Ticker', 'AAPL')
# df = data.DataReader(user_input, 'yahoo', start, end)

df = yf.download(user_input, start = start, end=end)


# describing data
Title="Date from "+start+" to "+end
st.subheader(Title)
st.write(df.describe())

# visualizations
st.subheader('Closing prise vs Time chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
st.pyplot(fig)


st.subheader('Closing prise vs Time chart WITH 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)


st.subheader('Closing prise vs Time chart WITH 100MA && 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)


# Splitting Data into traing and testing

# data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
# data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.1)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.1): int(len(df))])


scaler = MinMaxScaler(feature_range=(0, 1))

data_training_array = scaler.fit_transform(data_training)


# Load my model
model = load_model('keras_model.h5')


# testing part
past_100_days = data_training.tail(100)
# final_df = past_100_days.append(data_testing, ignore_index=True)
final_df = np.concatenate((past_100_days, data_testing), axis=0)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)

my_scaler = scaler.scale_

scale_factor = 1/my_scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# final graph
st.subheader('predictions vs original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

#Next day prediction
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
st.subheader("Next day prediction")
total_dataset = pd.concat((df['Close'],data_testing['Close']),axis=0)
model_inputs = total_dataset[len(total_dataset)-len(data_testing)-100:].values
model_inputs = model_inputs.reshape(-1,1)
scaler.fit(model_inputs)
model_inputs = scaler.transform(model_inputs)
real_data = [model_inputs[len(model_inputs)+1 - 100:len(model_inputs+1),0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
st.write(*(prediction[0]))

# #Accuracy
# st.subheader("Accuracy")
# from sklearn.metrics import accuracy_score,mean_squared_error,r2_score
# accuracy = r2_score(y_test, y_predicted)
# st.write(accuracy*100)
