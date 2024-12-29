import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

def app():
  model = load_model('lstm_model.keras')

  def create_sequences(data, time_step):
    X = []
    for i in range(len(data) - time_step + 1):
      seq = data[i:i + time_step]
      X.append(seq)
    return np.array(X)
    
  st.header('Stock Future Return Prediction Prediction')
  st.write('Upload a CSV file containing OHLCV data for multiple stocks. The app will predict the future return for each stock, rank them in descending order, and allow you to download the results.')

  # File uploader
  uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

  if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, header=[0])
    
    # Validate the structure of the file
    if not {'Stock', 'Open', 'High', 'Low', 'Close', 'Volume'}.issubset(data.columns):
      st.error("The file must contain the columns: 'Stock', 'Open', 'High', 'Low', 'Close', 'Volume'.")

    else:
      stocks = data['Stock'].unique()
      predictions = []

      scaler = StandardScaler()

      for stock in stocks:
        # FIlter data
        stock_data = data[data['Stock'] == stock][['Open', 'High', 'Low', 'Close', 'Volume']]

        # Ensure data has at least 20 rows
        if len(stock_data) < 20:
          st.warning(f"Not enough data for stock {stock}. Skipping.")
          st.warning(f"Ensure there are at least 20 rows of data for {stock}.") 
          continue

        # Normalized the features
        scaled_features = scaler.fit_transform(stock_data)

        sequence = create_sequences(scaled_features, time_step=20)
        sequence = sequence.reshape(1, sequence.shape[1], sequence.shape[2])
        predicted_return = model.predict(sequence)
        predicted_return = scaler.inverse_transform(predicted_return)

        # Append prediction to list
        predictions.append({
          'Stock': stock,
          'Predicted Future Return': predicted_return[0][0]
        })

        prediction_df = pd.DataFrame(predictions)

        if not prediction_df.empty:
          # Sort in descending
          prediction_df = prediction_df.sort_values(by='Predicted Future Return', ascending=False)

          # Display the predictions
          st.subheader("Predictions")
          st.dataframe(prediction_df)

          # Download the prediction results
          csv = prediction_df.to_csv(index=False)
          st.download_button(
            label='Download Predictions as CSV',
            data=csv,
            file_name='predicted_returns.csv',
            mime='text/csv'
          )
      else:
        st.warning("No valid predictions were made. Check your data.")

if __name__ == "__main__":
  app()
