import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

def app():
  # Load model
  model = load_model('website/lstm_model.keras')

  def create_sequences(data, time_step):
    X = []
    for i in range(len(data) - time_step + 1):
      seq = data[i:i + time_step]
      X.append(seq)
    return np.array(X)
    
  st.title('Stock Future Return Prediction')
  
  # Add a link to the sample file
  st.markdown(
      """
      ### Sample File
      You can download a [sample CSV file](https://365umedumy-my.sharepoint.com/:x:/g/personal/22004790_siswa365_um_edu_my/EU3h9GjCWIlJqtdXBvCDcfEBYC8ZH0iHGgxQ3PteX7t4HQ?e=FSvKee) to understand the expected format.
      """,
      unsafe_allow_html=True,
  )
  
  # File uploader
  uploaded_file = st.file_uploader("Upload stock data for prediction", type=['csv'])

  if uploaded_file is not None:
    # Read file
    data = pd.read_csv(uploaded_file, header=[0])
    
    stocks = data['Stock'].unique()
    predictions = []

    scaler = StandardScaler()

    for stock in stocks:
      # Filter data
      stock_data = data[data['Stock'] == stock]
      y = stock_data['Future_Return']
      stock_data = stock_data.drop(columns=['Date', 'Stock', 'Future_Return'])
      
      # Ensure data has at least 20 rows
      if len(stock_data) < 20:
        st.warning(f"Not enough data for stock {stock}. Skipping.")
        st.warning(f"Ensure there are at least 20 rows of data for {stock}.") 
        continue

      # Normalized the features
      scaled_features = scaler.fit_transform(stock_data)
      y_scaled = scaler.fit_transform(y.values.reshape(-1,1))

      # Create sequence
      sequence = create_sequences(scaled_features, time_step=20)
      sequence = sequence[-1]
      sequence = sequence.reshape(1, sequence.shape[0], sequence.shape[1])

      # Prediction
      predicted_return = model.predict(sequence)
      predicted_return = scaler.inverse_transform(predicted_return)

      # Append prediction to list
      predictions.append({
        'Stock': stock,
        'Predicted Future Return': predicted_return[0][0]
      })

    # Convert to dataframe
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
