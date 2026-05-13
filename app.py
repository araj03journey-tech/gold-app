import streamlit as st

# تنظیمات صفحه
st.set_page_config(page_title="سیستم جامع Alirezaa محاسبات گالری طلا", page_icon="💰", layout="centered")

# استایل‌دهی برای راست‌چین کردن و زیبایی موبایل
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
        height: 3em;
        font-size: 18px;
    }
    input {
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 سیستم مدیریت محاسبات گالری")

# ورودی مشترک نرخ طلا در ابتدای صفحه
rate_input = st.text_input("📈 نرخ هر گرم طلا (تومان) - آزاد تایپ کنید", value="", help="می‌توانید با فاصله یا نقطه جدا کنید، سیستم خودش اصلاح می‌کند")
clean_rate = rate_input.replace(",", "").replace(" ", "").replace(".", "")

current_rate = 0
if clean_rate and clean_rate.isdigit():
    current_rate = int(clean_rate)
    st.info(f"✅ نرخ مبنا: **{current_rate:,.0f}** تومان")
else:
    st.warning("⚠️ ابتدا نرخ طلا را وارد کنید تا محاسبات فعال شود.")

st.markdown("---")

# ایجاد دو پنل مجزا
tab1, tab2 = st.tabs(["🛒 محاسبه فروش ویترینی", "⚖️ تبدیل عیار و محاسبه"])

# --- پنل اول: محاسبه فروش ---
with tab1:
    st.header("محاسبه قیمت اتیکت")
    wage_percent = st.number_input("اجرت روی اتیکت (درصد)", value=0.0, key="wage_1")
    weight_sale = st.number_input("وزن کل (گرم)", value=0.0, format="%.3f", key="weight_1")
    
    if st.button("🧮 محاسبه قیمت فروش"):
        if current_rate > 0 and weight_sale > 0:
            price_per_gram = current_rate + (current_rate * (wage_percent / 100))
            total_sale = price_per_gram * 1.25 * weight_sale
            st.success(f"💰 قیمت نهایی مشتری: **{total_sale:,.0f}** تومان")
        else:
            st.error("لطفاً نرخ و وزن را وارد کنید.")

# --- پنل دوم: تبدیل عیار ---
with tab2:
    st.header("تبدیل عیار به ۷۵۰")
    col1, col2 = st.columns(2)
    with col1:
        weight_raw = st.number_input("وزن قطعه (گرم)", value=0.0, format="%.3f", key="w_raw")
    with col2:
        karat_raw = st.number_input("عیار قطعه (مثلاً ۷۴۰ یا ۹۰۰)", value=750, key="k_raw")
    
    st.divider()
    
    if st.button("🚀 تبدیل عیار و محاسبه"):
        if current_rate > 0 and weight_raw > 0:
            # ۱. تبدیل وزن به عیار ۷۵۰
            converted_weight = (weight_raw * karat_raw) / 750
            
            # ۲. اضافه کردن ۱ درصد به نرخ طلا
            adjusted_rate = current_rate + (current_rate * 0.01)
            
            # ۳. محاسبه نهایی
            final_calc = converted_weight * adjusted_rate
            
            # نمایش خروجی‌ها
            st.markdown(f"**وزن تبدیل شده به ۷۵۰:** `{converted_weight:.3f} گرم` ")
            st.markdown(f"**نرخ با احتساب ۱٪:** `{adjusted_rate:,.0f} تومان` ")
            st.success(f"💵 مبلغ نهایی: **{final_calc:,.0f}** تومان")
        else:
            st.error("لطفاً نرخ طلا و وزن قطعه را وارد کنید.")
