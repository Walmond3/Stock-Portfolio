import streamlit as st

st.title('My Data Product')

st.sidebar.title('Page')

if st.sidebar.button('Overview'):
  import pages.overview
elif st.sidebar.button('Chart'):
  import pages.chart
elif st.sidebar.button('Prediction'):
  import pages.prediction
elif st.sidebar.button('Portfolio'):
  import pages.portfolio
                                            
