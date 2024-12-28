import streamlit as st
import pandas as pd

st.title('Stock Visionary')

data = {
        "Ticker": [
            "0138.KL",
            "7153.KL",
            "1295.KL",
            "0045.KL",
            "1023.KL",
            "5398.KL",
            "5819.KL",
            "3182.KL",
            "3816.KL",
            "5014.KL",
            "8133.KL",
            "3034.KL",
            "3689.KL",
            "3255.KL",
            "3026.KL",
            "5517.KL",
            "5657.KL",
            "7081.KL",
            "6139.KL",
            "0097.KL",
        ],
        "Name": [
            "MY E.G. Services Berhad (MYEG)",
            "Kossan Rubber Industries Bhd (KOSSAN)",
            "Public Bank Berhad (PB BANK)",
            "Southern Score Builders Berhad (SSB8)",
            "CIMB Group Holdings Berhad (CIMB)",
            "Gamuda Berhad (GAMUDA)",
            "Hong Leong Bank Berhad (HL BANK)",
            "Genting Berhad (GENTING)",
            "MISC Berhad (MISC)",
            "Malaysia Airport Holdings Berhad (MAHB)",
            "Boustead Heavy Industries Corporation (BHIC)",
            "Hap Seng Consolidated Berhad (HAP SENG)",
            "Fraser & Neave Holdings (F&NHB)",
            "Heineken Malaysia Berhad (HEINEKEN)",
            "Dutch Lady Milk Industries Berhad (DLADY)",
            "Shangri-La Hotels (Malaysia) Berhad (SHANGRI-LA)",
            "Parkson Holdings Berhad (PARKSON)",
            "Pharmaniaga Berhad (PHARMANIAGA)",
            "Syarikat Takaful Malaysia Keluarga Berhad (STMKB)",
            "ViTrox Corporation Berhad (VITROX)",
        ],
    }

# Create a DataFrame
stock_table = pd.DataFrame(data)

# Display the table
st.write("### List of Stocks")
st.dataframe(stock_table, use_container_width=True)
