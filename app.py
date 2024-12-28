import streamlit as st

st.title('My Data Product')

page = st.sidebar.selectbox('Select a page', ['Overview', 'Chart', 'Prediction', 'Portfolio'])

if page == 'Overview':
  import pages.overview
elif page == 'Chart':
  import pages.chart
elif page == 'Prediction':
  import pages.prediction
elif page == 'Portfolio':
  import pages.portfolio
                                            
