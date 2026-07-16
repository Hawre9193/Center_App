import streamlit as st
import datetime
import pandas as pd

# 1. ڕێکخستنی سەرەتایی لاپەڕەکە
st.set_page_config(
    page_title="سەنتەری شاهانە | VIP",
    page_icon="👑",
    layout="wide"
)

# 2. لێدانی دەرزی جادوویی CSS بۆ دروستکردنی ستایلی جیهانی و تاریک
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #12131a 0%, #08080c 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0c0d12 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.15) !important;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }
    .ad-banner {
        background: linear-gradient(90deg, #AA7C11 0%, #D4AF37 50%, #AA7C11 100%) !important;
        color: #000000 !important;
        padding: 15px !important;
        border-radius: 12px !important;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        margin-bottom: 30px;
    }
    .product-box {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        text-align: center;
        transition: all 0.3s ease;
    }
    .product-box:hover {
        border-color: #D4AF37 !important;
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.1);
    }
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="number-input"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.4) !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }
    button[data-baseweb="tab"] {
        color: #888 !important;
        font-size: 16px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
        font-weight: bold !important;
    }
    div[data-testid="stMetricValue"] {
        color: #D4AF37 !important;
        font-weight: bold !important;
    }
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }
    .neon-title {
        color: #D4AF37;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. پاشەکەوتکردنی داتاکان لە مێشکدا
if "users" not in st.session_state:
    st.session_state.users = {
        "admin@gmail.com": {"password": "admin123", "name": "خاوەن کار (هاوڕێ)", "role": "admin", "expire": datetime.date(2027, 12, 31)},
        "barber1@gmail.com": {"password": "123", "name": "سەنتەری هاوڕێ", "role": "user", "expire": datetime.date(2026, 8, 16)}
    }

if "services" not in st.session_state:
    st.session_state.services = {
        "قژ تاشینی مۆدێرن": 15000,
        "تاشینی ڕیش و ڕێکخستن": 10000,
        "پاککردنەوەی پێست (فەیشەڵ)": 25000,
        "سێشوار و مۆدێل": 8000
    }

if "orders" not in st.session_state:
    st.session_state.orders = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

if "show_login" not in st.session_state:
    st.session_state.show_login = False

# ==========================================
# لاپەڕەی سەرەکی بازرگانی (Landing Page)
# ==========================================
if not st.session_state.logged_in and not st.session_state.show_login:
    st.markdown("<h1 class='neon-title' style='font-size: 45px; margin-bottom: 5px;'>👑 سەنتەری شاهانە</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892b0;'>پلاتفۆرمی جیهانی بۆ خزمەتگوزاری و کەلوپەلی پیشەیی ساڵۆنەکان</p>", unsafe_allow_html=True)
    st.write("")
    
    # 📢 بەشی بانەری ڕیکلامی گەورە
    st.markdown("""
        <div class="ad-banner">
            📢 سپۆنسەر: کۆمپانیای گۆڵد کێراتین - باشترین ماددەی ڕێکخستنی قژ گەیشت! (بۆ ڕیکلامکردن لێرە پەیوەندیمان پێوە بکە)
        </div>
    """, unsafe_allow_html=True)
    
    # 🛍️ بەشی مارکێتپلەیس (فرۆشتنی کەلوپەل)
    st.markdown("<h2 style='color: #D4AF37;'>🛍️ بازاڕی کەلوپەلی دەلاکی (VIP Shop)</h2>", unsafe_allow_html=True)
    st.write("کوالێتی بەرزترین ئامێر و کەرەستەکان بۆ ساڵۆنەکەت دابین بکە:")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("""
            <div class="product-box">
                <h3 style='color:#fff;'>🪒 ئامێری تاشینی وایەرلێس</h3>
                <p style='color:#8892b0;'>پاتری بەهێز، مۆدێلی ٢٠٢٦</p>
                <h4 style='color:#D4AF37;'>45,000 دینار</h4>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🛒 داواکردنی خێرا", key="p1"):
            st.toast("بۆ کڕین، پەیوەندی بکە بە ژمارە: 0750XXXXXXX", icon="📞")
            
    with col_p2:
        st.markdown("""
            <div class="product-box">
                <h3 style='color:#fff;'>🧴 جێڵی پرۆفیشناڵ (Max)</h3>
                <p style='color:#8892b0;'>ڕاگرتنی قژ بۆ ماوەی ٢٤ کاتژمێر</p>
                <h4 style='color:#D4AF37;'>6,000 دینار</h4>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🛒 داواکردنی خێرا", key="p2"):
            st.toast("بۆ کڕین، پەیوەندی بکە بە ژمارە: 0750XXXXXXX", icon="📞")
            
    with col_p3:
        st.markdown("""
            <div class="product-box">
                <h3 style='color:#fff;'>✂️ مەقەسی یابانی ئەسڵی</h3>
                <p style='color:#8892b0;'>پۆڵای دژە ژەنگ، زۆر تیژ</p>
                <h4 style='color:#D4AF37;'>25,000 دینار</h4>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🛒 داواکردنی خێرا", key="p3"):
            st.toast("بۆ کڕین، پەیوەندی بکە بە ژمارە: 0750XXXXXXX", icon="📞")

    st.markdown("---")
    
    # دوگمەی سەرەکی بۆ چوونە ناو سیستمی نۆرەکان
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
    with col_btn2:
        if st.button("👑 چوونەژوورەوە بۆ سیستمی نۆرەگرتن"):
            st.session_state.show_login = True
            st.rerun()

# ==========================================
# لاپەڕەی لۆگین (ستایلی شوشەیی زەبەلاح)
# ==========================================
elif not st.session_state.logged_in and st.session_state.show_login:
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("""
            <div class="main-card" style="text-align: center;">
                <h1 style="color: #D4AF37; font-size: 40px; margin: 0;">👑</h1>
                <h2 style="color: #ffffff; margin-top: 5px;">چوونەژوورەوەی پارێزراو</h2>
                <p style="color: #8892b0; font-size: 13px;">تکایە زانیارییەکانت بنووسە بۆ بەڕێوەبردنی کارەکان</p>
            </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("📧 ئیمەیڵ:").strip().lower()
        password = st.text_input("🔑 پاسوۆرد:", type="password").strip()
        
        st.write("")
        if st.button("پەیوەستبوون 🚀"):
            if email in st.session_state.users:
                if st.session_state.users[email]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.rerun()
                else:
                    st.error("❌ پاسوۆرد هەڵەیە!")
            else:
                st.error("❌ ئەم ئیمەیڵە بوونی نییە!")
                
        if st.button("⬅️ گەڕانەوە بۆ لاپەڕەی بازاڕ و ڕیکلام"):
            st.session_state.show_login = False
            st.rerun()

# ==========================================
# ناوەوەی سیستمەکە (دوای لۆگینبوون)
# ==========================================
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Sidebar
    st.sidebar.markdown(f"<h2 class='neon-title'>👑 {user_info['name']}</h2>", unsafe_allow_html=True)
    st.sidebar.write(f"**پلە:** {user_info['role'].upper()}")
    st.sidebar.write(f"**ئیشتراک:** لۆکاڵی / هەمیشەیی")
    st.sidebar.write("---")
    
    if st.sidebar.button("چوونەدەرەوە 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.show_login = False
        st.rerun()

    # 🛡️ ئەکاونتی ئەدمین (خاوەنکار)
    if user_info["role"] == "admin":
        st.markdown("<h1 class='neon-title'>🛡️ مەکۆی بەڕێوەبردنی گشتی</h1>", unsafe_allow_html=True)
        st.write("---")
        
        tab_dash, tab_profit, tab_add_u, tab_add_s = st.tabs([
            "📊 دۆخی گشتی", "💰 حیساباتی قازانج", "👥 بەشداربووان", "✂️ خزمەتگوزارییەکان"
        ])
        
        with tab_dash:
            total_sales = sum(o["price"] for o in st.session_state.orders)
            c1, c2 = st.columns(2)
            c1.metric("💰 کۆی گشتی پارەی هاتوو", f"{total_sales:,} د.ع")
            c2.metric("👥 ژمارەی کڕیارەکان", f"{len(st.session_state.orders)} نۆرە")
            
            st.write("---")
            if st.session_state.orders:
                st.subheader("📋 خشتەی سەرجەم نۆرەکان")
                st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
            else:
                st.info("هیچ داتایەک بۆ ئەمڕۆ نییە.")
                
        with tab_profit:
            st.subheader("💵 دابەشکاری دارایی و قازانجەکان")
            percentage = st.number_input("٪ ڕێژەی قازانجی سەرتاش دیاری بکە:", min_value=0, max_value=100, value=50, step=5)
            
            if st.session_state.orders:
                df_orders = pd.DataFrame(st.session_state.orders)
                # حیسابکردنی پشکەکان
                df_orders["قازانجی سەرتاش"] = df_orders["price"] * (percentage / 100)
                df_orders["پشکی سەنتەر"] = df_orders["price"] * ((100 - percentage) / 100)
                
                st.dataframe(df_orders[["time", "customer_name", "barber", "service", "price", "قازانجی سەرتاش", "پشکی سەنتەر"]], use_container_width=True)
                
                st.write("---")
                # کورتەی کۆتایی
                total_barber = df_orders["قازانجی سەرتاش"].sum()
                total_center = df_orders["پشکی سەنتەر"].sum()
                
                col_f1, col_f2 = st.columns(2)
                col_f1.metric("💇‍♂️ کۆی قازانجی سەرتاشەکان", f"{total_barber:,} د.ع")
                col_f2.metric("🏰 کۆی پشکی پاکی سەنتەر", f"{total_center:,} د.ع")
            else:
                st.info("سەرتاشەکان هێشتا هیچ نۆرەیەکیان تۆمار نەکردووە بۆ ئەوەی قازانج حیساب بکرێت.")

        with tab_add_u:
            st.subheader("👥 تۆمارکردنی سەرتاش یان کارمەندی نوێ")
            nu_email = st.text_input("ئیمەیڵ بۆ کارمەند:")
            nu_name = st.text_input("ناوی کارمەند:")
            nu_pass = st.text_input("پاسوۆردی کارمەند:", type="password")
            if st.button("تۆمارکردن 🤝"):
                if nu_email and nu_name and nu_pass:
                    st.session_state.users[nu_email] = {"password": nu_pass, "name": nu_name, "role": "user"}
                    st.success("کارمەندی نوێ زیادکرا!")
                    st.rerun()

        with tab_add_s:
            st.subheader("✂️ زیادکردنی خزمەتگوزاری و نرخی نوێ")
            ns_name = st.text_input("ناوی خزمەتگوزاری:")
            ns_price = st.number_input("نرخی خزمەتگوزاری (دینار):", min_value=0, step=1000)
            if st.button("زیادکردن ➕"):
                if ns_name:
                    st.session_state.services[ns_name] = ns_price
                    st.success("خزمەتگوزاری نوێ جێگیر کرا!")
                    st.rerun()

    # 💇‍♂️ ئەکاونتی سەرتاش / سەنتەری بەکارهێنەر
    else:
        st.markdown(f"<h1 class='neon-title'>💇‍♂️ لقی: {user_info['name']}</h1>", unsafe_allow_html=True)
        st.write("---")
        
        t_order, t_view = st.tabs(["📝 تۆمارکردنی نۆرەی نوێ", "📊 بینینی کارەکانی ئەمرۆت"])
        
        with t_order:
            c_name = st.text_input("ناوی کڕیار:")
            c_gender = st.selectbox("ڕەگەز:", ["کوڕ", "کچ"])
            c_service = st.selectbox("جۆری خزمەتگوزاری:", list(st.session_state.services.keys()))
            c_price = st.session_state.services[c_service]
            
            st.markdown(f"<h4>💵 نرخی کارەکە: <span style='color:#D4AF37;'>{c_price:,} دینار</span></h4>", unsafe_allow_html=True)
            
            if st.button("💾 جێگیرکردنی نۆرە"):
                if c_name:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.orders.append({
                        "time": now,
                        "customer_name": c_name,
                        "gender": c_gender,
                        "service": c_service,
                        "price": c_price,
                        "barber": user_info["name"]
                    })
                    st.success(f"نۆرەی کڕیار ({c_name}) بە سەرکەوتوویی پاشەکەوت کرا!")
                    st.rerun()
                else:
                    st.warning("تکایە ناوی کڕیار بنووسە.")
                    
        with t_view:
            my_jobs = [o for o in st.session_state.orders if o["barber"] == user_info["name"]]
            if my_jobs:
                my_df = pd.DataFrame(my_jobs)
                st.metric("💰 کۆی کارەکانت لای خۆت", f"{my_df['price'].sum():,} دینار")
                st.write("---")
                st.dataframe(my_df[["time", "customer_name", "service", "price"]], use_container_width=True)
            else:
                st.info("تۆ هێشتا هیچ نۆرەیەکت بۆ خۆت تۆمار نەکردووە.")
