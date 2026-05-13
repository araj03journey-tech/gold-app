import streamlit as st

# تنظیمات صفحه برای موبایل و دسکتاپ
st.set_page_config(page_title="ماشین حساب طلای گالری", page_icon="💰")

# استایل‌دهی ساده برای زیباتر شدن در موبایل
st.markdown("""
    <style>
    .main {
        text-align: right;
        direction: rtl;
    }
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 ماشین حساب طلای گالری")
st.write("فرمول دقیق محاسبه طلا با اجرت و سود مغازه")

# ورودی‌ها
rate = st.number_input("نرخ هر گرم طلا (تومان)", value=0, step=1000)
wage_percent = st.number_input("اجرت روی اتیکت (درصد)", value=0.0)
weight = st.number_input("وزن روی اتیکت (گرم)", value=0.0, format="%.3f")

if st.button("محاسبه قیمت نهایی"):
    if rate > 0 and weight > 0:
        # فرمول اختصاصی شما
        wage_decimal = wage_percent / 100
        price_per_gram = rate + (rate * wage_decimal)
        total = price_per_gram * 1.25 * weight
        
        # نمایش نتیجه با فرمت پولی
        st.success(f"قیمت نهایی: {total:,.0f} تومان")
        st.info(f"قیمت هر گرم با اجرت: {price_per_gram:,.0f} تومان")
    else:
        st.warning("لطفاً مقادیر را وارد کنید.")
