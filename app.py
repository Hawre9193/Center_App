import streamlit as st
import sqlite3
import datetime
import pandas as pd
import time
import hashlib  # بۆ پاراستنی پاسۆردەکان بە شێوازێکی جیهانی

# ========================================================
# ١. بەشی ڕێکخستنی زمانەکان (کە پێشتر لە config.py بوو)
# ========================================================
LANG_DICT = {
    "Kurdish": {
        "title": "👑 ئیمپڕاتۆریەتی شاهانە",
        "subtitle": "گەورەترین سەکۆی مۆڵتی-بازرگانی بۆ سەرجەم خزمەتگوزارییەکان لە کوردستان",
        "home": "🏠 لاپەڕەی سەرەکی",
        "shop": "🛍️ بازاڕ و کەرەستەکان",
        "ad_portal": "📢 داواکردنی ڕیکلام",
        "login_btn": "🔑 دەروازەی ئەندامان",
        "choose_lang": "🌐 زمان هەڵبژێرە:",
        "biz_select": "🏢 جۆری کارەکەت زیاتر دیاری بکە:",
        "book_btn": "📅 نۆرە بگرە لەم بزنسە",
        "quick_order": "🛒 کڕینی خێرا",
        "username": "ئیمەیڵی فەرمی یان بازرگانی:",
        "password": "پاسۆردی پارێزراو:",
        "login_confirm": "چوونەژوورەوە بۆ ناو پلاتفۆڕم",
        "ad_title": "پۆرتالی ڕیکلامی شاهانە",
        "active_merchants": "🏢 ئەو بزنسانەی لەگەڵمان ئەکتیڤن",
        "staff_management": "👥 کارمەندەکان",
        "product_management": "📦 بەرهەمەکان",
        "booking_management": "📅 نۆرەکان و تۆمارەکان",
        "total_views": "کۆی گشتی بینینی لاپەڕەکانمان تا ئێستا",
        "no_merchant": "⚠️ هێشتا هیچ کام لە بزنسەکان و پیشەکان بۆ ئەم بەشە تۆمار نەکراوە.",
        "no_product": "⚠️ هیچ بەرهەمێک بۆ ئەم بەش و پیشەیە دیاری نەکراوە.",
        "plat_banner": "📢 پلاتفۆڕمی شاهانە: بەرهەمەکانت لێرە بەرز بکەرەوە بۆ ئەوەی زۆرترین فرۆشتنت هەبێت!",
        "ad_intro": "لێرەوە داوای ڕیکلامی VIP شاهانە بکە بۆ بزنسەکەت:",
        "fullname": "ناوی بەڕێزت:",
        "bizname": "ناوی بزنسەکەت یان کۆمپانیاکەت:",
        "phone_whats": "ژمارەی مۆبایل / واتساپ:",
        "ad_text": "دەقی ڕیکلامی خوازراو:",
        "ad_link": "بەستەری فەرمی ڕیکلام (فەیسبووک, ئینستاگرام, ماڵپەڕ):",
        "ad_duration": "ماوەی چالاک مانەوە بە مانگ:",
        "ad_submit": "ناردنی داواکاری بۆ دەستەی شاهانە",
        "success_ad": "داواکارییەکەت بە سەرکەوتوویی نێردرا! دوای پێداچوونەوەی ئەدمین بڵاودەبێتەوە. 🎉",
        "fill_fields": "تکایە خانە پێویستەکان بە دروستی پڕ بکەرەوە!",
        "reg_banner": "بزنسەکەت لێرەوە تۆمار بکە بۆ ئەوەی زیاتر بەناوبانگ بیت لە وێبسایتی جیهانی شاهانە 🚀",
        "reg_btn": "تۆمارکردنی بزنسی نوێ",
        "owner_name": "ناوی تەواوی خاوەن کار:",
        "biz_sec": "بزنسەکەت سەر بە کام بەشەیە？",
        "country": "وڵات:",
        "city": "شار:",
        "address": "ناونیشانی فیزیکی ورد:",
        "reg_submit": "دروستکردنی ئەکاونتی نوێ و تۆمارکردن",
        "reg_success": "پیرۆزە! ئەکاونتی بازرگانیت بە سەرکەوتوویی دروستکرا. ئێستا دەتوانیت بچیتە ژوورەوە. 🎉",
        "email_exists": "⚠️ ئەم ئیمەیڵە پێشتر لە سیستەمدا بەکارهێنراوە!",
        "finance_tab": "💰 ژووری دارایی تایبەت",
        "search_label": "🔍 بگەڕێ بۆ بەرهەم یان بزنس لە وێبسایتی شاهانە:",
        "contact_admin": "📞 پەیوەندی بە دەستەی بەڕێوەبەرایەتی و ئەدمینەکانەوە بکە لە ڕێگەی واتساپەوە:"
    },
    "English": {
        "title": "👑 Royal Empire",
        "subtitle": "The largest multi-merchant platform for all services in Kurdistan",
        "home": "🏠 Home Page",
        "shop": "🛍️ Market & Products",
        "ad_portal": "📢 Request Advertisement",
        "login_btn": "🔑 Member Portal",
        "choose_lang": "🌐 Choose Language:",
        "biz_select": "🏢 Select Your Business Type:",
        "book_btn": "📅 Book an Appointment",
        "quick_order": "🛒 Quick Buy",
        "username": "Official or Business Email:",
        "password": "Secure Password:",
        "login_confirm": "Login to Platform",
        "ad_title": "Royal Advertising Portal",
        "active_merchants": "🏢 Active Businesses on Platform",
        "staff_management": "👥 Staff Members",
        "product_management": "📦 Products",
        "booking_management": "📅 Bookings & Records",
        "total_views": "Total Page Views Till Now",
        "no_merchant": "⚠️ No businesses are registered in this category yet.",
        "no_product": "⚠️ No products are currently listed for this business/category.",
        "plat_banner": "📢 Royal Platform: Elevate your products here for maximum reach!",
        "ad_intro": "Request your Royal Sponsored Ad here for your business:",
        "fullname": "Your Full Name:",
        "bizname": "Your Business or Company Name:",
        "phone_whats": "Mobile Number / WhatsApp:",
        "ad_text": "Desired Ad Content Text:",
        "ad_link": "Official Ad Link (Facebook, Instagram, Web):",
        "ad_duration": "Duration in Months:",
        "ad_submit": "Send Request to Royal Board",
        "success_ad": "Your request has been successfully submitted! It will appear once approved by admin. 🎉",
        "fill_fields": "Please fill all required fields correctly!",
        "reg_banner": "Register your business here to become famous on the Royal International Website 🚀",
        "reg_btn": "Register New Business",
        "owner_name": "Full Name of Business Owner:",
        "biz_sec": "Which section does your business belong to?",
        "country": "Country:",
        "city": "City:",
        "address": "Detailed Physical Address:",
        "reg_submit": "Create New Account & Register",
        "reg_success": "Congratulations! Your merchant account has been created successfully. You can log in now. 🎉",
        "email_exists": "⚠️ This email has already been registered in our system!",
        "finance_tab": "💰 Special Finance Chamber",
        "search_label": "🔍 Search for products or businesses on Royal Website:",
        "contact_admin": "📞 Contact the Executive Board & Admins via WhatsApp:"
    }
}

# ========================================================
# ٢. بەشی دیزاینەکان (کە پێشتر لە styles.py بوو)
# ========================================================
def inject_royal_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;700&display=swap');
        * { font-family: 'Noto Sans Arabic', sans-serif !important; }
        .stApp { background: radial-gradient(circle, #0e0f14 0%, #050508 100%) !important; color: #e2e8f0 !important; }
        .main .block-container { direction: rtl !important; text-align: right !important; }
        [data-testid="stSidebar"] { direction: rtl !important; background-color: #07080c !important; border-left: 1px solid rgba(212, 175, 55, 0.15); }
        [data-testid="stSidebarUserContent"] { direction: rtl !important; text-align: right !important; }
        .royal-header { text-align: center; padding: 30px; background: linear-gradient(135deg, #161822 0%, #0b0c10 100%); border: 2px solid rgba(212, 175, 55, 0.35); border-radius: 20px; margin-bottom: 25px; }
        .ad-banner { background: linear-gradient(90deg, #aa7c11 0%, #d4af37 50%, #aa7c11 100%) !important; color: #000000 !important; padding: 18px !important; border-radius: 12px !important; text-align: center; font-weight: bold; font-size: 18px; }
        .main-card { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(212, 175, 55, 0.2) !important; border-radius: 15px !important; padding: 22px !important; margin-bottom: 20px; text-align: right !important; }
        .product-box { background: rgba(255, 255, 255, 0.02) !important; border: 1px solid rgba(212, 175, 55, 0.12) !important; border-radius: 15px !important; padding: 18px !important; text-align: center; }
        .stButton>button { background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important; color: #000 !important; font-weight: bold !important; border-radius: 10px !important; }
        </style>
    """, unsafe_allow_html=True)

# ========================================================
# ٣. بەشی داتابەیسە پێشکەوتووەکە (لێرەوە گۆڕانکارییە جیهانییەکان دەست پێدەکات)
# ========================================================
conn = sqlite3.connect("royal_core_ultimate.db", check_same_thread=False)
cursor = conn.cursor()

def hash_password(password):
    """ئەم فەنکشنە بۆ پاراستنی پاسۆردی بەکارهێنەرانە بە شێوازی مۆدێرن"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    # خشتەی بازرگانەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT,
        owner_name TEXT,
        business_type TEXT,
        email TEXT UNIQUE,
        password TEXT,
        phone TEXT,
        country TEXT,
        city TEXT,
        address TEXT,
        commission_rate REAL DEFAULT 10.0
    )
    """)

    # خشتەی کارمەندەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        staff_name TEXT,
        role TEXT,
        FOREIGN KEY(merchant_id) REFERENCES merchants(id)
    )
    """)

    # خشتەی بەرهەمەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        name TEXT,
        price REAL,
        description TEXT,
        img_url TEXT,
        FOREIGN KEY(merchant_id) REFERENCES merchants(id)
    )
    """)

    # خشتەی نۆرەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        customer_name TEXT,
        customer_phone TEXT,
        staff_id INTEGER,
        booking_date TEXT,
        booking_time TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(merchant_id) REFERENCES merchants(id),
        FOREIGN KEY(staff_id) REFERENCES staff(id)
    )
    """)

    # خشتەی ڕیکلامەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        business_name TEXT,
        client_phone TEXT,
        country TEXT,
        city TEXT,
        business_type TEXT,
        address TEXT,
        ad_text TEXT,
        ad_link TEXT,
        duration_months INTEGER,
        status TEXT DEFAULT 'Pending',
        start_date TEXT,
        end_date TEXT
    )
    """)

    # خشتەی بینینی لاپەڕەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        view_date TEXT UNIQUE,
        view_count INTEGER DEFAULT 0
    )
    """)

    # خشتەی داواکارییەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        customer_name TEXT,
        customer_phone TEXT,
        product_details TEXT,
        total_price REAL,
        order_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # ✨ خشتە نوێیە جیهانییەکان لێرەوە دەست پێدەکەن (بۆ زیادکردنی هێڵەکان بەبێ کێشە):
    # خشتەی کۆپۆن و داشکاندن
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        code TEXT UNIQUE,
        discount_percent REAL,
        expiry_date TEXT,
        FOREIGN KEY(merchant_id) REFERENCES merchants(id)
    )
    """)

    # خشتەی فیدباک و ئەستێرەی کڕیاران
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        customer_name TEXT,
        rating INTEGER,
        comment TEXT,
        review_date TEXT,
        FOREIGN KEY(merchant_id) REFERENCES merchants(id)
    )
    """)
    conn.commit()

    # نوێکردنەوەی ژمارەی بینینەکان
    today_str = datetime.date.today().isoformat()
    cursor.execute("INSERT OR IGNORE INTO page_views (view_date, view_count) VALUES (?, 0)", (today_str,))
    cursor.execute("UPDATE page_views SET view_count = view_count + 1 WHERE view_date = ?", (today_str,))
    conn.commit()

init_db()

# ========================================================
# ٤. بەشی پانێڵەکان (کە پێشتر لە panels.py بوو)
# ========================================================
def render_super_admin_panel(T):
    st.markdown("<h1 style='color:#d4af37;'>🛡️ پانێڵی سەرەکی دەسەڵاتی ڕەها</h1>", unsafe_allow_html=True)
    tab_views, tab_merchants, tab_ads = st.tabs(["📊 ئاماری سەرانسەری", "🏢 چاودێری بازرگانەکان", "📢 بەڕێوەبردنی ڕیکلامەکان"])
    
    with tab_views:
        st.subheader("📈 چاودێری و ڕێژەی هاتوچۆی کڕیاران")
        cursor.execute("SELECT view_date, view_count FROM page_views ORDER BY view_date DESC LIMIT 10")
        v_data = cursor.fetchall()
        if v_data:
            df = pd.DataFrame(v_data, columns=["Date", "Views"])
            st.line_chart(df.set_index("Date"))
        else:
            st.info("هیچ زانیارییەکی سەرەتایی بەردەست نییە.")
            
    with tab_merchants:
        cursor.execute("SELECT id, business_name, owner_name, business_type, email FROM merchants")
        for m in cursor.fetchall():
            st.markdown(f"<div class='main-card'><h4>🏢 {m[1]} ({m[3]})</h4><p>خاوەن کار: {m[2]} | ئیمەیڵ: {m[4]}</p></div>", unsafe_allow_html=True)
            
    with tab_ads:
        cursor.execute("SELECT id, client_name, ad_text FROM ads WHERE status = 'Pending'")
        p_ads = cursor.fetchall()
        if not p_ads: st.info("هیچ داواکارییەکی نوێ نییە.")
        for ad in p_ads:
            st.write(f"👤 **کڕیار:** {ad[1]}")
            st.info(ad[2])
            if st.button("✅ پەسەندکردن", key=f"app_{ad[0]}"):
                cursor.execute("UPDATE ads SET status = 'Approved' WHERE id = ?", (ad[0],))
                conn.commit()
                st.rerun()

def render_merchant_panel(T):
    st.markdown(f"<h1 style='color:#d4af37;'>🏢 بەڕێوەبردنی: {st.session_state.business_name}</h1>", unsafe_allow_html=True)
    cursor.execute("SELECT business_type, commission_rate FROM merchants WHERE id = ?", (st.session_state.user_id,))
    merchant_info = cursor.fetchone()
    b_type = merchant_info[0]
    comm_rate = merchant_info[1]
    
    tab_bookings, tab_staff, tab_products, tab_orders, tab_finance, tab_coupons = st.tabs([
        T["booking_management"], T["staff_management"], T["product_management"], "📦 داواکارییەکان", T["finance_tab"], "🎫 کۆپۆن و داشکاندن"
    ])
    
    with tab_bookings:
        cursor.execute("SELECT customer_name, customer_phone, booking_date, status FROM bookings WHERE merchant_id = ?", (st.session_state.user_id,))
        for b in cursor.fetchall():
            st.write(f"👤 {b[0]} ({b[1]}) - 📅 {b[2]} - دۆخ: {b[3]}")

    with tab_staff:
        with st.form("add_staff_form"):
            s_name = st.text_input("ناوی کارمەند:")
            s_role = st.text_input("پیشە:")
            if st.form_submit_button("تۆمارکردن") and s_name:
                cursor.execute("INSERT INTO staff (merchant_id, staff_name, role) VALUES (?, ?, ?)", (st.session_state.user_id, s_name, s_role))
                conn.commit()
                st.success("کارمەندەکە زیادکرا!")

    with tab_products:
        with st.form("add_product_form"):
            p_name = st.text_input("ناوی بەرهەم:")
            p_price = st.number_input("نرخ:", min_value=0)
            if st.form_submit_button("پاشەکەوتکردن") and p_name:
                cursor.execute("INSERT INTO products (merchant_id, name, price, description, img_url) VALUES (?, ?, ?, '', '')", (st.session_state.user_id, p_name, p_price))
                conn.commit()
                st.success("کاڵاکە زیادکرا!")

    with tab_orders:
        st.info("لێرەوە دەتوانیت داواکاری کڕین ببینی.")

    with tab_finance:
        st.metric("کۆمسیۆنی پلاتفۆڕم", f"%{comm_rate}")

    with tab_coupons:
        st.subheader("🎫 دروستکردنی کۆدی داشکاندن بۆ کڕیارەکانت")
        with st.form("add_coupon_form"):
            c_code = st.text_input("کۆدی داشکاندن (بۆ نموونە: ROYAL10):").strip().upper()
            c_discount = st.sidebar.slider("ڕێژەی داشکاندن (%):", 5, 90, 10)
            if st.form_submit_button("🛡️ چالاککردنی کۆپۆن"):
                if c_code:
                    try:
                        cursor.execute("INSERT INTO coupons (merchant_id, code, discount_percent, expiry_date) VALUES (?, ?, ?, ?)",
                                       (st.session_state.user_id, c_code, c_discount, (datetime.date.today() + datetime.timedelta(days=30)).isoformat()))
                        conn.commit()
                        st.success(f"کۆدی داشکاندنی {c_code} بە سەرکەوتوویی بۆ کڕیاران دروست بوو!")
                    except sqlite3.IntegrityError:
                        st.error("ئەم کۆدە پێشتر دروستکراوە!")

# ========================================================
# ٥. بەشی لاپەڕەکان (کە پێشتر لە views.py بوو)
# ========================================================
def render_home_page(T, biz_type):
    st.markdown(f"<div class='royal-header'><h1 style='color:#d4af37;'>{T['title']}</h1><p>{T['subtitle']}</p></div>", unsafe_allow_html=True)
    cursor.execute("SELECT id, business_name, owner_name FROM merchants WHERE business_type = ?", (biz_type,))
    for m in cursor.fetchall():
        st.markdown(f"<div class='main-card'><h3>🏢 {m[1]}</h3><p>خاوەن کار: {m[2]}</p></div>", unsafe_allow_html=True)

def render_shop_page(T, biz_type):
    st.markdown(f"<h1 style='color:#d4af37;'>{T['shop']}</h1>", unsafe_allow_html=True)
    st.info("بەشی کڕینی خێرا")

def render_ad_portal(T):
    st.markdown(f"<h1 style='color:#d4af37;'>{T['ad_title']}</h1>", unsafe_allow_html=True)
    with st.form("ad_form"):
        c_name = st.text_input(T["fullname"])
        b_name = st.text_input(T["bizname"])
        ad_text = st.text_area(T["ad_text"])
        if st.form_submit_button(T["ad_submit"]) and c_name and ad_text:
            cursor.execute("INSERT INTO ads (client_name, business_name, ad_text, status) VALUES (?, ?, ?, 'Pending')", (c_name, b_name, ad_text))
            conn.commit()
            st.success(T["success_ad"])

# ========================================================
# ٦. بزوێنەری سەرەکی پڕۆژە (کە پێشتر لە app.py بوو)
# ========================================================
st.set_page_config(page_title="ئیمپڕاتۆریەتی شاهانە", page_icon="👑", layout="wide")
inject_royal_styles()

if "lang" not in st.session_state: st.session_state.lang = "Kurdish"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.business_name = None
if "cart" not in st.session_state: st.session_state.cart = {}

T = LANG_DICT[st.session_state.lang]

st.sidebar.markdown("<h2 style='color:#d4af37; text-align:center;'>☰ ROYAL CORE</h2>", unsafe_allow_html=True)
st.session_state.lang = st.sidebar.selectbox(T["choose_lang"], options=["Kurdish", "English"])
biz_type = st.sidebar.selectbox(T["biz_select"], options=["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"])

menu_choice = st.sidebar.radio("🧭 Navigation", options=[T["home"], T["shop"], T["ad_portal"], T["login_btn"]])

if menu_choice == T["home"]: render_home_page(T, biz_type)
elif menu_choice == T["shop"]: render_shop_page(T, biz_type)
elif menu_choice == T["ad_portal"]: render_ad_portal(T)
elif menu_choice == T["login_btn"]:
    if not st.session_state.logged_in:
        tab_login, tab_register = st.tabs(["🔑 چوونەژوورەوە", "🏢 تۆمارکردن"])
        with tab_login:
            email_val = st.text_input(T["username"]).strip().lower()
            pass_val = st.text_input(T["password"], type="password").strip()
            if st.button(T["login_confirm"]):
                if email_val == "admin@gmail.com" and pass_val == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "super_admin"
                    st.rerun()
                else:
                    cursor.execute("SELECT id, business_name FROM merchants WHERE email = ? AND password = ?", (email_val, pass_val))
                    m_row = cursor.fetchone()
                    if m_row:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "merchant"
                        st.session_state.user_id = m_row[0]
                        st.session_state.business_name = m_row[1]
                        st.rerun()
        with tab_register:
            reg_b_name = st.text_input("ناوی گشتی پڕۆژە:")
            reg_o_name = st.text_input(T["owner_name"])
            reg_b_email = st.text_input("ئیمەیڵ:")
            reg_b_pass = st.text_input("پاسۆرد:", type="password")
            if st.button(T["reg_btn"]) and reg_b_name and reg_b_email:
                try:
                    cursor.execute("INSERT INTO merchants (business_name, owner_name, business_type, email, password) VALUES (?, ?, ?, ?, ?)",
                                   (reg_b_name, reg_o_name, biz_type, reg_b_email, reg_b_pass))
                    conn.commit()
                    st.success(T["reg_success"])
                except sqlite3.IntegrityError:
                    st.error(T["email_exists"])
    else:
        if st.session_state.user_role == "super_admin": render_super_admin_panel(T)
        elif st.session_state.user_role == "merchant": render_merchant_panel(T)
