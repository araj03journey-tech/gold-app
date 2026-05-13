import streamlit as st
import pandas as pd

# تنظیمات صفحه
st.set_page_config(page_title="سیستم جامع محاسبات علیرضا گالری طلا", page_icon="💰", layout="centered")

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
        font-size: 20px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding: 5px;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 سیستم مدیریت محاسبات گالری")

# ورودی نرخ طلا با کیبورد عددی در موبایل
current_rate = st.number_input("📈 نرخ هر گرم طلا (تومان)", min_value=0, value=0, step=10000)

if current_rate > 0:
    st.info(f"✅ مبلغ در حال محاسبه: **{current_rate:,.0f}** تومان")
else:
    st.warning("⚠️ ابتدا نرخ طلا را وارد کنید تا محاسبات فعال شود.")

st.markdown("---")

# ایجاد سه پنل مجزا
tab1, tab2, tab3 = st.tabs(["🛒 فروش", "⚖️ عیار", "🔄 تعویض"])

# --- پنل اول: محاسبه فروش ---
with tab1:
    st.header("محاسبه قیمت اتیکت")
    wage_percent = st.number_input("اجرت روی اتیکت (درصد)", value=0, step=5, key="wage_1")
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
        karat_raw = st.number_input("عیار قطعه (عدد خلوص)", value=750, key="k_raw")
    
    if st.button("🚀 تبدیل عیار و محاسبه"):
        if current_rate > 0 and weight_raw > 0:
            converted_weight = (weight_raw * karat_raw) / 750
            adjusted_rate = current_rate + (current_rate * 0.01)
            final_calc = converted_weight * adjusted_rate
            
            st.markdown(f"**وزن تبدیل شده به ۷۵۰:** `{converted_weight:.3f} گرم` ")
            st.markdown(f"**نرخ با احتساب ۱٪:** `{adjusted_rate:,.0f} تومان` ")
            st.success(f"💵 مبلغ نهایی: **{final_calc:,.0f}** تومان")
        else:
            st.error("لطفاً نرخ طلا و وزن قطعه را وارد کنید.")

    st.markdown("---")
    st.subheader("📌 راهنمای سریع تبدیل عیار")
    
    data = {
        "عیار مرسوم": ["۱۷ عیار", "۱۸ عیار", "۲۰ عیار", "۲۱ عیار", "۲۲ عیار", "۲۴ عیار"],
        "عدد خلوص": ["۷۰۸", "۷۵۰", "۸۳۳", "۸۷۵", "۹۱۶", "۱۰۰۰ (۹۹۹)"]
    }
    df = pd.DataFrame(data)
    st.table(df)

# --- پنل سوم: تعویض طلا (جدید) ---
with tab3:
    st.header("محاسبه مابه‌التفاوت تعویض")
    
    st.subheader("۱. طلای کهنه (دریافتی از مشتری)")
    old_weight = st.number_input("وزن طلای مشتری (گرم)", value=0.0, format="%.3f", key="old_w")
    
    st.divider()
    
    st.subheader("۲. طلای جدید (فروش به مشتری)")
    col3, col4 = st.columns(2)
    with col3:
        new_weight = st.number_input("وزن طلای جدید (گرم)", value=0.0, format="%.3f", key="new_w")
    with col4:
        new_wage = st.number_input("اجرت طلای جدید (درصد)", value=0, step=5, key="new_wage")
        
    if st.button("🔄 محاسبه فاکتور تعویض"):
        if current_rate > 0 and old_weight > 0 and new_weight > 0:
            # محاسبه ارزش طلای کهنه (کسر 150 هزار تومان از نرخ روز)
            buy_rate = current_rate - 150000
            old_gold_value = buy_rate * old_weight
            
            # محاسبه ارزش طلای جدید (با فرمول فروش ویترین)
            price_per_gram_new = current_rate + (current_rate * (new_wage / 100))
            new_gold_value = price_per_gram_new * 1.25 * new_weight
            
            # محاسبه مابه‌التفاوت
            difference = old_gold_value - new_gold_value
            
            st.markdown(f"**ارزش طلای مشتری:** `{old_gold_value:,.0f} تومان` (بر مبنای گرمی {buy_rate:,.0f})")
            st.markdown(f"**ارزش طلای جدید:** `{new_gold_value:,.0f} تومان`")
            
            st.divider()
            
            if difference < 0:
                # مشتری باید پول بدهد
                st.error(f"💳 مشتری باید پرداخت کند: **{abs(difference):,.0f}** تومان")
            elif difference > 0:
                # گالری باید پول بدهد
                st.success(f"💵 گالری باید پرداخت کند: **{difference:,.0f}** تومان")
            else:
                st.info("⚖️ تعویض سر به سر شد (بدون نیاز به پرداخت).")
        else:
            st.error("لطفاً نرخ طلا، وزن طلای مشتری و وزن طلای جدید را به درستی وارد کنید.")
