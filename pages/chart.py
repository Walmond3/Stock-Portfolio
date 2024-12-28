import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import makesubplots

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
  
      # Add traces for indicators (example: RSI)
      if indicator == 'RSI':
          fig.add_trace(go.Scatter(x=df[ticker].index, y=df[ticker]['RSI'], mode='lines', name='Relative Strength Index'),
                        row=2, col=1)
  
      # Add other indicator options as needed...
  
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

  df = pd.read_csv()
  









  
  st.title('Visualise Stock Performance')
  
  # Stock and indicator selection for first chart
  st.header("Select Stock and Indicator for Chart 1")
  col1_input, col2_input = st.columns(2)
  selected_stock_name_1 = col1_input.selectbox("Select Stock 1", list(stocks.keys()))
  selected_stock_code_1 = stocks[selected_stock_name_1]
  selected_indicator_1 = col2_input.selectbox("Select Indicator for Stock 1", 
                                              ['RSI', 'Volatility Indicators'])  # Add other indicators here
  
  # Comparison toggle
  compare = st.checkbox("Compare")
  
  # Inputs for second chart if comparison is enabled
  if compare:
      st.header("Select Stock and Indicator for Chart 2")
      col3_input, col4_input = st.columns(2)
      selected_stock_name_2 = col3_input.selectbox("Select Stock 2", list(stocks.keys()))
      selected_stock_code_2 = stocks[selected_stock_name_2]
      selected_indicator_2 = col4_input.selectbox("Select Indicator for Stock 2", 
                                                  ['RSI', 'Volatility Indicators'])  # Add other indicators here
  
  # Main section for chart display
  st.header("Stock Chart Visualization")
  col1, col2 = st.columns(2 if compare else 1)
  
  # Render the first chart
  with col1:
      fig1 = plot_chart(df, selected_stock_code_1, selected_indicator_1)
      st.plotly_chart(fig1, use_container_width=True)
  
  # Render the second chart if comparison is selected
  if compare:
      with col2:
          fig2 = plot_chart(df, selected_stock_code_2, selected_indicator_2)
          st.plotly_chart(fig2, use_container_width=True)


if __name__ == "__main__":
  app()
