import streamlit as st
import datetime
import pandas as pd

# 1. ڕێکخستنی سەرەتایی لاپەڕەکە
st.set_page_config(
    page_title="سەنتەری شاهانە | VIP",
    page_icon="👑",
    layout="wide"
)

# 2. لێدانی دەرزی جادوویی CSS بۆ دروستکردنی ستایلی جیهانی و تاریکی Zedflix
st.markdown("""
    <style>
    /* پشتخلفانی تاریکی قووڵ */
    .stApp {
        background: radial-gradient(circle, #12131a 0%, #08080c 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* مینیووی لای چەپ (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0c0d12 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.15) !important;
    }
    
    /* کارتی شووشەیی لۆگین (Glassmorphism) */
    .login-container {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), 0 0 20px rgba(212, 175, 55, 0.1) !important;
        text-align: center;
        margin-top: 30px;
    }
    
    /* خانەکانی نووسین (Input Fields) */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #D4AF37 !important; /* درەوشانەوەی ئاڵتوونی لە کاتی نووسیندا */
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.4) !important;
    }
    
    /* سێلێکت بۆکسەکان */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* دوگمە مۆدێرن و شازەکان */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    /* تابەکانی سەرەوە (Tabs) */
    button[data-baseweb="tab"] {
        color: #888 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
        font-weight: bold !important;
    }
    
    /* کارتەکانی نیشاندانی داهات (Metrics) */
    div[data-testid="stMetricValue"] {
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 28px !important;
    }
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }
    
    /* نازناوە گرنگەکان */
    .neon-title {
        color: #D4AF37;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جێگیرکردنی داتاکان لە ناو مێشکدا
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

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# ==========================================
# لاپەڕەی لۆگین (ستایلی زۆر شاز و تاریکی VIP)
# ==========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("""
            <div class="login-container">
                <h1 style="color: #D4AF37; font-size: 45px; margin-bottom: 5px; text-shadow: 0 0 15px rgba(212,175,55,0.4);">👑</h1>
                <h2 style="color: #ffffff; font-weight: 800; margin-top: 0px;">سەنتەری شاهانە</h2>
                <p style="color: #8892b0; font-size: 14px; margin-bottom: 30px;">پلاتفۆرمی مۆدێرن بۆ بەڕێوەبردنی کارەکان بە شێوەی جیهانی</p>
            </div>
        """, unsafe_allow_html=True)
        
        # دروستکردنی کێڵگەکان لە خوارەوەی کارتەکە بە ڕێکی
        email = st.text_input("📧 ئیمەیڵەکەت بنووسە:").strip().lower()
        password = st.text_input("🔑 پاسوۆردەکەت بنووسە:", type="password").strip()
        
        st.write("")
        if st.button("چوونەژوورەوە بۆ سەر تەخت 👑", use_container_width=True):
            if email in st.session_state.users:
                user_data = st.session_state.users[email]
                if user_data["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.success(f"بەخێربێیت بەڕێز {user_data['name']}!")
                    st.rerun()
                else:
                    st.error("❌ پاسوۆردەکەت هەڵەیە!")
            else:
                st.error("❌ ئەم ئیمەیڵە تۆمار نەکراوە!")

# ==========================================
# دوای لۆگینبوون (ناو ماڵپەڕەکە)
# ==========================================
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # مینیووی لای چەپ
    st.sidebar.markdown(f"<h2 class='neon-title'>👑 {user_info['name']}</h2>", unsafe_allow_html=True)
    st.sidebar.write(f"**پلە:** {user_info['role'].upper()}")
    st.sidebar.write(f"**ئیشتراک تا:** {user_info['expire']}")
    st.sidebar.write("---")
    
    if st.sidebar.button("چوونەدەرەوە 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # ئەگەر ئەدمین بێت
    if user_info["role"] == "admin":
        st.markdown("<h1 class='neon-title'>🛡️ مەکۆی سەرەکی بەڕێوەبردن</h1>", unsafe_allow_html=True)
        st.write("---")
        
        tab_dashboard, tab_users, tab_services = st.tabs(["📊 کورتەی دۆخی دارایی", "👥 بەشداربووان", "✂️ خزمەتگوزارییەکان"])
        
        with tab_dashboard:
            total_sales = sum(o["price"] for o in st.session_state.orders)
            st.write("")
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("💰 کۆی داهات", f"{total_sales:,} دینار")
            col_m2.metric("👥 ژمارەی کڕیارەکان", f"{len(st.session_state.orders)} کڕیار")
            
            st.write("---")
            if st.session_state.orders:
                st.subheader("📋 نۆرەکانی ئەمڕۆ")
                df = pd.DataFrame(st.session_state.orders)
                st.dataframe(df[["time", "customer_name", "barber", "service", "price"]], use_container_width=True)
            else:
                st.info("هیچ کارێک بۆ ئەمڕۆ تۆمار نەکراوە.")
                
        with tab_users:
            st.subheader("👥 زیادکردنی بەشداربووی نوێ")
            new_email = st.text_input("ئیمەیڵ:")
            new_name = st.text_input("ناو:")
            new_pass = st.text_input("پاسوۆرد:", type="password")
            if st.button("تۆمارکردن ✅"):
                if new_email and new_name and new_pass:
                    st.session_state.users[new_email] = {
                        "password": new_pass,
                        "name": new_name,
                        "role": "user",
                        "expire": datetime.date.today() + datetime.timedelta(days=30)
                    }
                    st.success("بە سەرکەوتوویی تۆمارکرا!")
                    st.rerun()

        with tab_services:
            st.subheader("✂️ خزمەتگوزاری نوێ")
            s_name = st.text_input("ناوی خزمەتگوزاری:")
            s_price = st.number_input("نرخەکەی (دینار):", min_value=500, step=500)
            if st.button("پاشەکەوتکردن 💾"):
                if s_name:
                    st.session_state.services[s_name] = s_price
                    st.success("زیادکرا!")
                    st.rerun()

    # ئەگەر سەرتاش یان سەنتەر بێت
    else:
        st.markdown(f"<h1 class='neon-title'>💇‍♂️ {user_info['name']}</h1>", unsafe_allow_html=True)
        st.write("---")
        
        tab_order, tab_today = st.tabs(["📝 تۆمارکردنی نۆرە", "📊 کارەکانی ئەمڕۆ"])
        
        with tab_order:
            cust_name = st.text_input("ناوی کڕیار:")
            gender = st.selectbox("ڕەگەز:", ["کوڕ", "کچ"])
            selected_service = st.selectbox("خزمەتگوزاری:", list(st.session_state.services.keys()))
            price = st.session_state.services[selected_service]
            
            st.markdown(f"<h3>💵 نرخی ئەم کارە: <span style='color:#D4AF37;'>{price:,} دینار</span></h3>", unsafe_allow_html=True)
            
            if st.button("➕ نۆرەکە تۆمار بکە"):
                if cust_name:
                    now_time = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.orders.append({
                        "time": now_time,
                        "customer_name": cust_name,
                        "gender": gender,
                        "service": selected_service,
                        "price": price,
                        "barber": user_info["name"]
                    })
                    st.success(f"نۆرەی {cust_name} بە سەرکەوتوویی تۆمارکرا!")
                    st.rerun()
                else:
                    st.warning("تکایە ناوی کڕیار بنووسە!")
                    
        with tab_today:
            my_orders = [o for o in st.session_state.orders if o["barber"] == user_info["name"]]
            if my_orders:
                st.metric("💰 کۆی کارەکانت", f"{sum(o['price'] for o in my_orders):,} دینار")
                st.write("---")
                st.dataframe(pd.DataFrame(my_orders)[["time", "customer_name", "service", "price"]], use_container_width=True)
            else:
                st.info("هیچ نۆرەیەکت تۆمار نەکردووە.")
