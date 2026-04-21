import streamlit as st
import pandas as pd
import plotly.express as px
import wbgapi as wb

st.set_page_config(page_title="Macro Finance Dashboard", layout="wide")
st.title("📈 Macro-Finance Economic Dashboard")

st.success("Ứng dụng đang khởi tạo...")

countries = {'VNM': 'Vietnam', 'USA': 'United States', 'CHN': 'China'}
indicators = {'NY.GDP.MKTP.CD': 'GDP (Current US$)', 'FP.CPI.TOTL.ZG': 'Inflation %'}

selected_country_codes = st.sidebar.multiselect("Chọn quốc gia", list(countries.keys()), default=['VNM'])
selected_indicator = st.sidebar.selectbox("Chọn chỉ số", list(indicators.keys()), format_func=lambda x: indicators[x])

@st.cache_data
def get_data(country_list, indicator):
    try:
        # Lấy dữ liệu 5 năm gần nhất cho nhẹ
        df = wb.data.DataFrame(indicator, country_list, mrv=5).transpose()
        df.index = [i.replace('YR', '') for i in df.index]
        return df
    except Exception as e:
        return None

if selected_country_codes:
    with st.spinner('Đang tải dữ liệu từ World Bank...'):
        data = get_data(selected_country_codes, selected_indicator)

    if data is not None and not data.empty:
        st.subheader(f"Biểu đồ: {indicators[selected_indicator]}")
        fig = px.line(data, x=data.index, y=selected_country_codes, markers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(data)
    else:
        st.error("Không thể tải dữ liệu. Vui lòng kiểm tra kết nối mạng!")
