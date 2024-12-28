import streamlit as st

st.title('My Data Product')

st.sidebar.title('Navigation')

if st.sidebar.button('Overview'):
  import pages.overview
  pages.overview.app()
elif st.sidebar.button('Chart'):
  import pages.chart
elif st.sidebar.button('Prediction'):
  import pages.prediction
elif st.sidebar.button('Portfolio'):
  import pages.portfolio
                                            
