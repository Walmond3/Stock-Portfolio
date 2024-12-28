import streamlit as st
import pandas as pd
import zipfile
import io
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def app():
  stocks = {"MYEG":"0138.KL",
          "KOSSAN":"7153.KL",
          "PB BANK":"1295.KL",
          "SSB8" :"0045.KL",
          "CIMB":"1023.KL",
          "GAMUDA":"5398.KL",
          "HL BANK":"5819.KL",
          "GENTING":"3182.KL",
          "MISC":"3816.KL",
          "MAHB":"5014.KL",
          "BHIC":"8133.KL",
          "HAP SENG":"3034.KL",
          "F&NHB":"3689.KL",
          "HEINEKEN":"3255.KL",
          "DLADY":"3026.KL",
          "SHANGRI-LA":"5517.KL",
          "PARKSON":"5657.KL",
          "PHARMANIAGA":"7081.KL",
          "STMKB":"6139.KL",
          "VITROX":"0097.KL"}

  # Function to plot the chart
  def plot_chart(df, ticker, indicator):
      name = next(name for name, code in stocks.items() if ticker == code)
      fig = make_subplots(rows=2, cols=1,
                          row_heights=[0.7, 0.3],
                          shared_xaxes=True,
                          vertical_spacing=0.1,
                          subplot_titles=[f'Candlestick Chart for {name} ({ticker})', f'{indicator} for {name} ({ticker})']
                          )
  
      # Candlestick chart
      fig.add_trace(go.Candlestick(x=df[ticker].index,
                                   open=df[ticker]['Open'],
                                   high=df[ticker]['High'],
                                   low=df[ticker]['Low'],
                                   close=df[ticker]['Close'],
                                   name="Candlestick"),
                    row=1, col=1)
  
      # Add traces for indicators
      if indicator == 'Volume Indicators':

        fig.add_trace(go.Scatter(x=df[ticker].index, y=df[ticker, 'OBV'], mode='lines', name='On-Balance Volume'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=df[ticker].index, y=df[ticker, 'AD'], mode='lines', name='Accumulation/Distribution Index'),
                      row=2, col=1)
      
      elif indicator == 'Volatility Indicators':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'ATR'], mode='lines', name='Average True Range'),
                    row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'RVI'], mode='lines', name='Relative Volatility Index'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'True Range'], mode='lines', name='True Range'),
                      row=2, col=1)
      
      elif indicator == 'RSI':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'RSI'], mode='lines', name='Relative Strength Index'),
                    row=2, col=1)
      
      elif indicator == 'Bollinger Bands':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'BBL_14_2.0'], mode='lines', name='Lower Bollinger Bands'),
                    row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'BBM_14_2.0'], mode='lines', name='Mid Bollinger Bands'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'BBU_14_2.0'], mode='lines', name='Upper Bollinger Bands'),
                      row=2, col=1)
        
      elif indicator == 'Average Directional Movement Index':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'ADX_14'], mode='lines', name='Average Directional Index'),
                    row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'DMN_14'], mode='lines', name='Directional Movement Minus'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'DMP_14'], mode='lines', name='Directional Movement Plus'),
                      row=2, col=1)
        
      elif indicator == 'Aroon & Aroon Oscillator':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'AROONU_14'], mode='lines', name='Aroon Up'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'AROOND_14'], mode='lines', name='Aroon Down'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'AROONOSC_14'], mode='lines', name='Aroon Oscillator'),
                      row=2, col=1)
        
      elif indicator == 'Overlap Indicators':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'EMA'], mode='lines', name='Exponential Moving Average'),
                row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'SMA'], mode='lines', name='Simple Moving Average'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'WMA'], mode='lines', name='Weighted Moving Average'),
                      row=2, col=1)
        
      elif indicator == 'KDJ':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'K_14_3'], mode='lines', name='Fast %K'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'D_14_3'], mode='lines', name='Slow %D'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'J_14_3'], mode='lines', name='J'),
                      row=2, col=1)
  
      elif indicator == 'Moving Average Convergence Divergence':
  
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'MACD_12_26_9'], mode='lines', name='Moving Average Convergence Divergence'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(x=final_df[ticker].index, y=final_df[ticker, 'MACDs_12_26_9'], mode='lines', name='Signal Line'),
                      row=2, col=1)

  
      fig.update_layout(title=f'Candlestick Chart with {indicator} for {name} ({ticker})',
                        xaxis_title="Date",
                        yaxis_title="Price",
                        yaxis2_title="Value",
                        xaxis=dict(type='date', rangeslider=dict(visible=False), tickformat='%Y-%m-%d', tickangle=45),
                        yaxis=dict(showgrid=True),
                        yaxis2=dict(showgrid=True),
                        height=800,
                        width=700,
                        showlegend=True,
                        template="plotly_dark")
      return fig

  # File uploader widget to upload a CSV file
  uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
  
  # If a file is uploaded, read and display it
  if uploaded_file is not None:
      # Read the CSV file into a DataFrame
      df = pd.read_csv(uploaded_file, header=[0, 1], index_col=0, parse_dates=True)
      # Display the DataFrame
      st.write('success')
      st.write("Data Columns:", df.columns)
      st.write("Data Preview:", df.head())
  
      # Stock and indicator selection for first chart
      st.header("Select Stock and Indicator for Chart 1")
      col1_input, col2_input = st.columns(2)
      selected_stock_name_1 = col1_input.selectbox("Select Stock", list(stocks.keys()))
      selected_stock_code_1 = stocks[selected_stock_name_1]
      selected_indicator_1 = col2_input.selectbox("Select Indicator", 
                                                  ['Volume Indicators', 'Volatility Indicators', 'RSI', 'Bollinger Bands', 'Average Directional Movement Index', 'Aroon & Aroon Oscillator', 'Overlap Indicators', 'KDJ', 'Moving Average Convergence Divergence'])  # Add other indicators here
  
      # Comparison toggle
      compare = st.checkbox("Compare with another chart?")
  
      # Inputs for second chart if comparison is enabled
      if compare:
          st.header("Select Stock and Indicator for Chart 2")
          col3_input, col4_input = st.columns(2)
          selected_stock_name_2 = col3_input.selectbox("Select Stock", list(stocks.keys()), key="stock_select_2")
          selected_stock_code_2 = stocks[selected_stock_name_2]
          selected_indicator_2 = col4_input.selectbox("Select Indicator", 
                                                      ['Volume Indicators', 'Volatility Indicators', 'RSI', 'Bollinger Bands', 'Average Directional Movement Index', 'Aroon & Aroon Oscillator', 'Overlap Indicators', 'KDJ', 'Moving Average Convergence Divergence'], key="indicator_select_2")  # Add other indicators here
  
      # Main section for chart display
      st.header("Stock Chart Visualization")
  
      # Define the columns based on whether compare is checked
      if compare:
          col1, col2 = st.columns(2)
      else:
          col1 = st.columns(1)[0]  # Single column when comparison is not selected
      
      # Render the first chart
      with col1:
          fig1 = plot_chart(df, selected_stock_code_1, selected_indicator_1)
          st.plotly_chart(fig1, use_container_width=True, key="plotly_chart_1")
  
      # Render the second chart if comparison is selected
      if compare:
          with col2:
              fig2 = plot_chart(df, selected_stock_code_2, selected_indicator_2)
              st.plotly_chart(fig2, use_container_width=True, key="plotly_chart_2")
  else:
      st.warning("Please upload a CSV file to proceed.")

if __name__ = "__main__":
  app()
