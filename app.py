import streamlit as st
import sqlite3
import datetime
import pandas as pd

# ========================================================
# ١. ڕێکخستنی لاپەڕە و دیزاینی تاریکی زێڕینی شاهانە
# ========================================================
st.set_page_config(
    page_title="سەنتەری شاهانە | Royal Core SaaS",
    page_icon="👑",
    layout="wide"
)

# لێدانی دەرزی جادوویی CSS بۆ ڕوواڵەتێکی جیهانی بێ لاگ
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #0e0f14 0%, #050508 100%) !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #07080c !important;
        border-right: 2px solid rgba(212, 175, 55, 0.3) !important;
    }
    .royal-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #161822 0%, #0b0c10 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
    .ad-banner {
        background: linear-gradient(90deg, #aa7c11 0%, #d4af37 50%, #aa7c11 100%) !important;
        color: #000000 !important;
        padding: 15px !important;
        border-radius: 12px !important;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.4);
        margin-bottom: 30px;
        font-size: 16px;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 15px;
    }
    .product-box {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center;
        transition: all 0.3s ease;
    }
    .product-box:hover {
        border-color: #d4af37 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
    }
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================================
# ٢. بەستنەوەی داتابەیسی SQLite هەمیشەیی
# ========================================================
conn = sqlite3.connect("royal_core_ultimate.db", check_same_thread=False)
cursor = conn.cursor()

# دروستکردنی خشتەکان بە شێوەی دروست
cursor.execute("""
CREATE TABLE IF NOT EXISTS merchants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT,
    owner_name TEXT,
    business_type TEXT,
    email TEXT UNIQUE,
    password TEXT,
    commission_rate REAL DEFAULT 10.0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id INTEGER,
    staff_name TEXT,
    role TEXT,
    FOREIGN KEY(merchant_id) REFERENCES merchants(id)
)
""")

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT,
    client_phone TEXT,
    ad_text TEXT,
    ad_link TEXT,
    duration_months INTEGER,
    status TEXT DEFAULT 'Pending',
    start_date TEXT,
    end_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS page_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_date TEXT UNIQUE,
    view_count INTEGER DEFAULT 0
)
""")
conn.commit()

# ژماردنی سەردانیکەرانی ڕۆژانە بە شێوازێکی مۆدێرنتر (INSERT OR IGNORE)
today_str = datetime.date.today().isoformat()
cursor.execute("INSERT OR IGNORE INTO page_views (view_date, view_count) VALUES (?, 0)", (today_str,))
cursor.execute("UPDATE page_views SET view_count = view_count + 1 WHERE view_date = ?", (today_str,))
conn.commit()

# ========================================================
# ٣. فەرهەنگی گەورەی زمانەکان (٥ زمان بە فۆرم و وردەکارییەوە)
# ========================================================
LANG_DICT = {
    "Kurdish": {
        "title": "👑 ئیمپراتۆریەتی شاهانە",
        "subtitle": "گەورەترین سەکۆی مۆڵتی-بازرگانی بۆ سەرجەم خزمەتگوزارییەکان لە کوردستان",
        "home": "🏠 لاپەڕەی سەرەکی",
        "shop": "🛍️ بازار و کەرەستەکان",
        "ad_portal": "📢 داواکردنی ڕیکلام",
        "login_btn": "🔑 دەروازەی ئەندامان",
        "choose_lang": "🌐 زمان هەڵبژێرە:",
        "biz_select": "🏢 جۆری کارەکەت:",
        "book_btn": "📅 نۆرە بگرە لەم بزنسە",
        "quick_order": "🛒 کڕینی خێرا",
        "username": "ئیمەیڵ:",
        "password": "پاسۆرد:",
        "login_confirm": "چوونەژوورەوە",
        "ad_title": "پۆرتالی ڕیکلامی شاهانە",
        "active_merchants": "🏢 ئەو بزنسانەی لەگەڵمان ئەکتیڤن",
        "staff_management": "👥 کارمەندەکان",
        "product_management": "📦 بەرهەمەکان",
        "booking_management": "📅 نۆرەکان",
        "total_views": "کۆی بینینی لاپەڕەکانمان"
    },
    "English": {
        "title": "👑 Royal Empire",
        "subtitle": "The largest multi-merchant platform for all services in Kurdistan",
        "home": "🏠 Home Page",
        "shop": "🛍️ Market & Products",
        "ad_portal": "📢 Request Advertisement",
        "login_btn": "🔑 Member Portal",
        "choose_lang": "🌐 Choose Language:",
        "biz_select": "🏢 Business Type:",
        "book_btn": "📅 Book an Appointment",
        "quick_order": "🛒 Quick Buy",
        "username": "Email:",
        "password": "Password:",
        "login_confirm": "Login",
        "ad_title": "Royal Advertising Portal",
        "active_merchants": "🏢 Active Businesses on Platform",
        "staff_management": "👥 Staff Members",
        "product_management": "📦 Manage Products",
        "booking_management": "📅 Manage Bookings",
        "total_views": "Total Page Views"
    },
    "Arabic": {
        "title": "👑 الإمبراطورية الملكية",
        "subtitle": "أكبر منصة متعددة التجار لجميع الخدمات في كوردستان",
        "home": "🏠 الصفحة الرئيسية",
        "shop": "🛍️ السوق والمنتجات",
        "ad_portal": "📢 طلب إعلان",
        "login_btn": "🔑 بوابة الأعضاء",
        "choose_lang": "🌐 اختر اللغة:",
        "biz_select": "🏢 نوع العمل التجاري:",
        "book_btn": "📅 احجز موعداً",
        "quick_order": "🛒 شراء سريع",
        "username": "البريد الإلكتروني:",
        "password": "كلمة المرور:",
        "login_confirm": "تسجيل الدخول",
        "ad_title": "البوابة الإعلانية الملكية",
        "active_merchants": "🏢 الأعمال النشطة معنا",
        "staff_management": "👥 إدارة الموظفين",
        "product_management": "📦 إدارة المنتجات",
        "booking_management": "📅 إدارة الحجوزات",
        "total_views": "إجمالي زيارات الصفحة"
    },
    "Turkish": {
        "title": "👑 Kraliyet İmparatorluğu",
        "subtitle": "Kürdistan'daki tüm hizmetler için en büyük çoklu üye platformu",
        "home": "🏠 Ana Sayfa",
        "shop": "🛍️ Mağaza ve Ürünler",
        "ad_portal": "📢 Reklam Başvurusu",
        "login_btn": "🔑 Üye Girişi",
        "choose_lang": "🌐 Dil Seçiniz:",
        "biz_select": "🏢 İşletme Türü:",
        "book_btn": "📅 Randevu Al",
        "quick_order": "🛒 Hızlı Satın Al",
        "username": "E-posta:",
        "password": "Şifre:",
        "login_confirm": "Giriş Yap",
        "ad_title": "Kraliyet Reklam Portalı",
        "active_merchants": "🏢 Platformdaki Aktif İşletmeler",
        "staff_management": "👥 Personel Yönetimi",
        "product_management": "📦 Ürün Yönetimi",
        "booking_management": "📅 Randevu Yönetimi",
        "total_views": "Toplam Sayfa Görüntüleme"
    },
    "Persian": {
        "title": "👑 امپراتوری سلطنتی",
        "subtitle": "بزرگترین پلتفرم چندفروشگاهی برای تمامی خدمات در کردستان",
        "home": "🏠 صفحه اصلی",
        "shop": "🛍️ بازار و محصولات",
        "ad_portal": "📢 ثبت درخواست تبلیغات",
        "login_btn": "🔑 پرتال اعضا",
        "choose_lang": "🌐 انتخاب زبان:",
        "biz_select": "🏢 نوع کسب‌وکار:",
        "book_btn": "📅 ثبت نوبت و رزرو",
        "quick_order": "🛒 خرید سریع",
        "username": "ایمیل:",
        "password": "رمز عبور:",
        "login_confirm": "ورود به سیستم",
        "ad_title": "پورتال تبلیغاتی سلطنتی",
        "active_merchants": "🏢 کسب‌وکارهای فعال در پلتفرم",
        "staff_management": "👥 مدیریت پرسنل",
        "product_management": "📦 مدیریت محصولات",
        "booking_management": "📅 مدیریت نوبت‌ها",
        "total_views": "کل بازدید صفحات"
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "Kurdish"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.business_name = None

T = LANG_DICT[st.session_state.lang]

# ========================================================
# 🍔 مینیۆی لای تەنیشت (Sidebar Menu)
# ========================================================
st.sidebar.markdown("<h2 style='color:#d4af37; text-align:center;'>👑 ROYAL CORE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; font-size:11px; color:#8892b0;'>ENTERPRISE MULTI-TENANT SYSTEM</p>", unsafe_allow_html=True)
st.sidebar.write("---")

st.session_state.lang = st.sidebar.selectbox(
    T["choose_lang"], 
    options=["Kurdish", "English", "Arabic", "Turkish", "Persian"],
    index=["Kurdish", "English", "Arabic", "Turkish", "Persian"].index(st.session_state.lang)
)

T = LANG_DICT[st.session_state.lang]

biz_type = st.sidebar.selectbox(
    T["biz_select"],
    options=["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"]
)
st.sidebar.write("---")

menu_choice = st.sidebar.radio(
    "🧭 Navigation",
    options=[T["home"], T["shop"], T["ad_portal"], T["login_btn"]]
)

if st.session_state.logged_in:
    st.sidebar.success(f"🔓 Roles: {st.session_state.user_role.upper()}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_id = None
        st.session_state.business_name = None
        st.rerun()

# ========================================================
# 🏠 لاپەڕەی سەرەکی (Home Page)
# ========================================================
if menu_choice == T["home"]:
    st.markdown(f"""
        <div class="royal-header">
            <h1 style="color:#d4af37; margin:0;">{T['title']}</h1>
            <p style="color:#8892b0; margin:5px 0 0 0;">{T['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    cursor.execute("SELECT ad_text, ad_link FROM ads WHERE status = 'Approved'")
    approved_ads = cursor.fetchall()
    if approved_ads:
        for ad in approved_ads:
            st.markdown(f'<div class="ad-banner">📢 <a href="{ad[1]}" target="_blank" style="color:black; text-decoration:none;">{ad[0]}</a></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ad-banner">📢 پلاتفۆرمی شاهانە: بەرهەمەکانت لێرە بەرز بکەرەوە بۆ ئەوەی زۆرترین فرۆشتنت هەبێت!</div>', unsafe_allow_html=True)

    st.subheader(T["active_merchants"])
    
    cursor.execute("SELECT id, business_name, owner_name, business_type FROM merchants WHERE business_type = ?", (biz_type,))
    merchants_list = cursor.fetchall()
    
    if not merchants_list:
        st.info("هێشتا هیچ بزنسێک بۆ ئەم جۆرە پیشەیە تۆمار نەکراوە.")
    else:
        cols = st.columns(3)
        for idx, merchant in enumerate(merchants_list):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="main-card" style="text-align:center; border-color:#d4af37 !important;">
                        <h3 style="color:#d4af37; margin:0;">{merchant[1]}</h3>
                        <p style="color:#8892b0; font-size:12px; margin:5px 0;">خاوەن کار: {merchant[2]}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if "Barber" in merchant[3] or "Pharmacy" in merchant[3]:
                    if st.button(T["book_btn"], key=f"book_m_{merchant[0]}"):
                        st.markdown(f"#### 📝 داواکردنی کات و نۆرە لە **{merchant[1]}**")
                        with st.form(f"booking_form_{merchant[0]}"):
                            c_name = st.text_input("ناو:")
                            c_phone = st.text_input("ژمارەی مۆبایل:")
                            
                            cursor.execute("SELECT id, staff_name, role FROM staff WHERE merchant_id = ?", (merchant[0],))
                            staff_members = cursor.fetchall()
                            
                            # لۆجیکی نوێ: ئەگەر کارمەند نەبوو ڕێگە نادات بە فۆرمی بەتاڵ نۆرە بگرێت
                            if staff_members:
                                staff_options = {f"{s[1]} ({s[2]})": s[0] for s in staff_members}
                                sel_staff = st.selectbox("پێشکەشکار / کارمەند:", options=list(staff_options.keys()))
                            else:
                                staff_options = {}
                                st.warning("⚠️ هێشتا هیچ کارمەندێک بۆ ئەم بزنسە تۆمار نەکراوە، بەڵام دەتوانیت نۆرە بۆ دواتر بگریت.")
                                sel_staff = None

                            b_date = st.date_input("ڕۆژ دیاری بکە:", min_value=datetime.date.today())
                            b_time = st.time_input("کاتژمێر:")
                            
                            submitted_booking = st.form_submit_button("تۆمارکردن")
                            if submitted_booking:
                                if c_name and c_phone:
                                    s_id = staff_options[sel_staff] if sel_staff else None
                                    cursor.execute("""
                                        INSERT INTO bookings (merchant_id, customer_name, customer_phone, staff_id, booking_date, booking_time)
                                        VALUES (?, ?, ?, ?, ?, ?)
                                    """, (merchant[0], c_name, c_phone, s_id, b_date.isoformat(), b_time.isoformat()))
                                    conn.commit()
                                    st.success("نۆرەکەت بە سەرکەوتوویی تۆمارکرا! 🎉")
                                else:
                                    st.error("تکایە خانەکان بە تەواوی پڕ بکەرەوە.")
                                    
                elif "Education" in merchant[3]:
                    if st.button("📚 ناونووسین لە کۆرسەکانی زمان", key=f"edu_m_{merchant[0]}"):
                        st.markdown(f"#### 📝 ناونووسین لە وانەکانی **{merchant[1]}**")
                        with st.form(f"edu_form_{merchant[0]}"):
                            stu_name = st.text_input("ناوى قوتابی:")
                            stu_phone = st.text_input("ژمارەی مۆبایل:")
                            lesson_level = st.selectbox("ئاستی وانەکان:", ["Level 1 (Basic)", "Level 2 (Intermediate)", "Level 3 (Advanced)"])
                            
                            submitted_edu = st.form_submit_button("پەسەندکردنی ناونووسین")
                            if submitted_edu:
                                if stu_name and stu_phone:
                                    cursor.execute("""
                                        INSERT INTO bookings (merchant_id, customer_name, customer_phone, staff_id, booking_date, booking_time, status)
                                        VALUES (?, ?, ?, NULL, ?, ?, 'Enrolled')
                                    """, (merchant[0], stu_name, stu_phone, datetime.date.today().isoformat(), lesson_level))
                                    conn.commit()
                                    st.success("ناوت بە سەرکەوتوویی لە کۆرسی فێربوونی زمانەکەدا تۆمارکرا! 🎓📘")
                                else:
                                    st.error("تکایە هەموو بەشەکان پڕ بکەرەوە.")

    st.write("---")
    col_views, col_spacer = st.columns([1, 2])
    with col_views:
        cursor.execute("SELECT SUM(view_count) FROM page_views")
        sum_v = cursor.fetchone()[0] or 150
        st.markdown(f"""
            <div class="main-card" style="text-align:center;">
                <h2 style="color:#d4af37; margin:0;">📊 {sum_v:,}</h2>
                <p style="font-size:12px; margin:5px 0 0 0;">{T['total_views']}</p>
            </div>
        """, unsafe_allow_html=True)

# ========================================================
# 🛍️ بەشی بازار و کەرەستەکان (Shop View)
# ========================================================
elif menu_choice == T["shop"]:
    st.markdown(f"<h1 style='color:#d4af37;'>{T['shop']}</h1>", unsafe_allow_html=True)
    
    cursor.execute("""
        SELECT m.business_name, p.name, p.price, p.description, p.img_url 
        FROM products p 
        JOIN merchants m ON p.merchant_id = m.id 
        WHERE m.business_type = ?
    """, (biz_type,))
    products_list = cursor.fetchall()
    
    if not products_list:
        st.info("هیچ بەرهەمێک بۆ ئەم پیشەیە دیاری نەکراوە.")
    else:
        cols = st.columns(4)
        for idx, prod in enumerate(products_list):
            with cols[idx % 4]:
                # لۆجیکی پارێزراو بۆ پیشاندانی وێنەکان (بێ HTML Injection)
                st.image(prod[4], use_container_width=True)
                st.markdown(f"""
                    <div class="product-box">
                        <h4 style="color:#d4af37; margin:5px 0;">{prod[1]}</h4>
                        <p style="font-size:11px; color:#8892b0; margin:0;">پیشە: {prod[0]}</p>
                        <p style="font-size:11px; color:#aaa; margin:5px 0;">{prod[3]}</p>
                        <h3 style="color:#fff; font-size:16px; margin:5px 0;">{prod[2]:,} IQD</h3>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(T["quick_order"], key=f"buy_p_{idx}", use_container_width=True):
                    st.success(f"داواکاریت بۆ {prod[1]} بە سەرکەوتوویی نێردرا! 📞")

# ========================================================
# 📢 داواکردنی ڕیکلام (Ad Portal)
# ========================================================
elif menu_choice == T["ad_portal"]:
    st.markdown(f"<h1 style='color:#d4af37;'>{T['ad_portal']}</h1>", unsafe_allow_html=True)
    st.write("لێرەوە داوای ڕیکلامی سپۆنسەری شاهانە بکە بۆ وێبسایتەکەت:")
    
    with st.form("ad_portal_form"):
        c_name = st.text_input("ناوی بەڕێزت / ناوی کۆمپانیا:")
        c_phone = st.text_input("ژمارەی مۆبایل:")
        ad_text = st.text_area("دەقی ڕیکلامەکە:")
        ad_link = st.text_input("بەستەری ڕیکلام (Facebook, Instagram, Web):")
        duration = st.slider("ماوە بە مانگ:", 1, 12, 1)
        
        submitted_ad = st.form_submit_button("ناردنی داواکاری")
        if submitted_ad:
            if c_name and c_phone and ad_text:
                cursor.execute("""
                    INSERT INTO ads (client_name, client_phone, ad_text, ad_link, duration_months)
                    VALUES (?, ?, ?, ?, ?)
                """, (c_name, c_phone, ad_text, ad_link, duration))
                conn.commit()
                st.success("داواکارییەکەت نێردرا! دوای پەسەندکردنی بەڕێوەبەر بڵاودەبێتەوە. 🎉")
            else:
                st.error("تکایە خانە سەرەکییەکان پڕ بکەرەوە!")

# ========================================================
# 🔑 دەروازەی ئەندامان و ئەدمین (Members and SaaS System)
# ========================================================
elif menu_choice == T["login_btn"]:
    if not st.session_state.logged_in:
        tab_login, tab_register = st.tabs(["🔑 چوونەژوورەوەی ئەندامان", "🏢 تۆمارکردنی بازرگانی نوێ (SaaS)"])
        
        with tab_login:
            st.subheader("چوونەژوورەوەی بەڕێوەبەران")
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
                    else:
                        st.error("زانیارییەکان تەواو نین یان هەڵەن!")
                        
        with tab_register:
            st.subheader("بزنسەکەت لێرەوە بخە نێو جیهانی شاهانە 🚀")
            with st.form("merchant_reg_form"):
                b_name = st.text_input("ناوی پڕۆژە / کارەکەت:")
                o_name = st.text_input("ناوی خاوەن کار:")
                b_type = st.selectbox("بزنسەکەت سەر بە کام بەشەیە؟", ["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"])
                b_email = st.text_input("📧 ئیمەیڵی فەرمی:")
                b_pass = st.text_input("🔑 پاسۆردی نهێنی:", type="password")
                
                submitted_reg = st.form_submit_button("دروستکردنی ئەکاونتی نوێ")
                if submitted_reg:
                    if b_name and b_email and b_pass:
                        try:
                            cursor.execute("""
                                INSERT INTO merchants (business_name, owner_name, business_type, email, password)
                                VALUES (?, ?, ?, ?, ?)
                            """, (b_name, o_name, b_type, b_email, b_pass))
                            conn.commit()
                            st.success("ئەکاونتی بازرگانیت دروستکرا! ئێستا لە بەشی لۆگین بچۆ ژوورەوە.")
                        except sqlite3.IntegrityError:
                            st.error("ئەم ئیمەیڵە پێشتر تۆمار کراوە!")
                    else:
                        st.error("تکایە هەموو خانەکان بە دروستی پڕ بکەرەوە.")

    else:
        # ----------------------------------------------------
        # 👑 الف: پانێڵی دەسەڵاتی ڕەها (SUPER ADMIN PANEL)
        # ----------------------------------------------------
        if st.session_state.user_role == "super_admin":
            st.markdown("<h1 style='color:#d4af37;'>🛡️ پانێڵی سەرەکی دەسەڵاتی ڕەها</h1>", unsafe_allow_html=True)
            
            tab_views, tab_merchants, tab_ads = st.tabs(["📊 ئاماری سەرانسەری", "🏢 چاودێری بازرگانەکان", "📢 بەڕێوەبردنی ڕیکلامەکان"])
            
            with tab_views:
                st.subheader("📈 چاودێری و ڕێژەی هاتوچۆی کڕیاران")
                cursor.execute("SELECT view_date, view_count FROM page_views ORDER BY view_date DESC LIMIT 10")
                v_data = cursor.fetchall()
                if v_data:
                    df = pd.DataFrame(v_data, columns=["Date", "Views"])
                    st.line_chart(df.set_index("Date"))
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("هیچ زانیارییەکی سەرەتایی بۆ بینینی لاپەڕەکان بەردەست نییە.")
                    
            with tab_merchants:
                st.subheader("🏢 بازرگانە بەشداربووەکان لەگەڵمان")
                cursor.execute("SELECT id, business_name, owner_name, business_type, email, commission_rate FROM merchants")
                m_list = cursor.fetchall()
                for m in m_list:
                    st.markdown(f"""
                        <div class="main-card">
                            <h4>🏢 ناوی پڕۆژە: {m[1]} ({m[3]})</h4>
                            <p>خاوەن کار: {m[2]} | ئیمەیڵی فەرمی: {m[4]}</p>
                            <p>ڕێژەی کۆمسیۆن: <b>%{m[5]}</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with tab_ads:
                st.subheader("📢 داواکارییە نوێیەکانی ڕیکلام")
                cursor.execute("SELECT id, client_name, client_phone, ad_text, ad_link, duration_months FROM ads WHERE status = 'Pending'")
                p_ads = cursor.fetchall()
                if not p_ads:
                    st.info("هیچ داواکارییەکی نوێ نییە بۆ پەسەندکردن.")
                else:
                    for ad in p_ads:
                        st.write(f"👤 **کڕیار:** {ad[1]} ({ad[2]}) - بۆ ماوەی **{ad[5]} مانگ**")
                        st.info(f"دەقی ڕیکلام: {ad[3]}")
                        col_ap1, col_ap2 = st.columns(2)
                        with col_ap1:
                            if st.button("✅ بڵاوکردنەوەی ڕیکلام", key=f"app_{ad[0]}"):
                                start = datetime.date.today()
                                end = start + datetime.timedelta(days=ad[5]*30)
                                cursor.execute("UPDATE ads SET status = 'Approved', start_date = ?, end_date = ? WHERE id = ?", (start.isoformat(), end.isoformat(), ad[0]))
                                conn.commit()
                                st.success("ڕیکلامەکە ڕاستەوخۆ چالاک کرا!")
                                st.rerun()
                        with col_ap2:
                            if st.button("❌ سرینەوە", key=f"del_{ad[0]}"):
                                cursor.execute("DELETE FROM ads WHERE id = ?", (ad[0],))
                                conn.commit()
                                st.rerun()

        # ----------------------------------------------------
        # 🏢 ب: پانێڵی تایبەتی بازرگانەکان (MERCHANT DASHBOARD)
        # ----------------------------------------------------
        elif st.session_state.user_role == "merchant":
            st.markdown(f"<h1 style='color:#d4af37;'>🏢 بەڕێوەبردنی: {st.session_state.business_name}</h1>", unsafe_allow_html=True)
            
            cursor.execute("SELECT business_type, commission_rate FROM merchants WHERE id = ?", (st.session_state.user_id,))
            merchant_info = cursor.fetchone()
            b_type = merchant_info[0]
            comm_rate = merchant_info[1]
            
            tab_bookings, tab_staff, tab_products, tab_finance = st.tabs([T["booking_management"], T["staff_management"], T["product_management"], "💰 ژووری دارایی"])
            
            with tab_bookings:
                if "Barber" in b_type or "Pharmacy" in b_type:
                    st.subheader("📅 خشتەی کار و کاتی نۆرەکانی دەستی کڕیارانت")
                    cursor.execute("""
                        SELECT b.id, b.customer_name, b.customer_phone, s.staff_name, b.booking_date, b.booking_time, b.status 
                        FROM bookings b LEFT JOIN staff s ON b.staff_id = s.id 
                        WHERE b.merchant_id = ?
                    """, (st.session_state.user_id,))
                    bookings = cursor.fetchall()
                    
                    if not bookings:
                        st.info("هیچ نۆرەیەک بەردەست نییە لە ئێستادا.")
                    else:
                        for b in bookings:
                            st.markdown(f"""
                                <div class="main-card">
                                    <h4>👤 کڕیار: {b[1]} ({b[2]})</h4>
                                    <p>کارمەندی دیاریکراو: <b>{b[3] if b[3] else "دیاری نەکراوە"}</b></p>
                                    <p>📅 کات و بەروار: {b[4]} | کاتژمێر {b[5]} | دۆخ: <b>{b[6]}</b></p>
                                </div>
                            """, unsafe_allow_html=True)
                            if b[6] == 'Pending':
                                if st.button("✅ پشتڕاستکردنەوەی نۆرە", key=f"conf_b_{b[0]}"):
                                    cursor.execute("UPDATE bookings SET status = 'Confirmed' WHERE id = ?", (b[0],))
                                    conn.commit()
                                    st.rerun()
                                    
                elif "Education" in b_type:
                    st.subheader("🎓 قوتابییە تۆمارکراوەکان لە کۆرسەکانی زماندا")
                    cursor.execute("""
                        SELECT id, customer_name, customer_phone, booking_date, booking_time, status 
                        FROM bookings WHERE merchant_id = ?
                    """, (st.session_state.user_id,))
                    students = cursor.fetchall()
                    
                    if not students:
                        st.info("هیچ قوتابییەک ناونووس نەکراوە لە ئێستادا.")
                    else:
                        for s in students:
                            st.markdown(f"""
                                <div class="main-card">
                                    <h4>👥 ناوی قوتابی: {s[1]}</h4>
                                    <p>مۆبایل: {s[2]} | ئاستی هەڵبژێردراو: <b>{s[4]}</b></p>
                                    <p>📅 بەرواری تۆمارکردن: {s[3]} | دۆخ: <b>{s[5]}</b></p>
                                </div>
                            """, unsafe_allow_html=True)
                            if s[5] == 'Enrolled':
                                if st.button("✅ پەسەندکردنی وەک خوێندکار", key=f"conf_stu_{s[0]}"):
                                    cursor.execute("UPDATE bookings SET status = 'Active Student' WHERE id = ?", (s[0],))
                                    conn.commit()
                                    st.rerun()

            with tab_staff:
                st.subheader("👥 کارمەندی نوێ زیاد بکە:")
                with st.form("add_staff_form"):
                    s_name = st.text_input("ناوی کارمەند:")
                    s_role = st.text_input("ناونیشان یان پیشە:")
                    sub_staff = st.form_submit_button("تۆمارکردن")
                    if sub_staff and s_name:
                        cursor.execute("INSERT INTO staff (merchant_id, staff_name, role) VALUES (?, ?, ?)", (st.session_state.user_id, s_name, s_role))
                        conn.commit()
                        st.success("کارمەندەکە زیادکرا!")
                        st.rerun()
                        
                st.write("---")
                st.subheader("کارمەندە چالاکەکان")
                cursor.execute("SELECT staff_name, role FROM staff WHERE merchant_id = ?", (st.session_state.user_id,))
                staff_list = cursor.fetchall()
                for s in staff_list:
                    st.write(f"👤 **{s[0]}** - {s[1]}")

            with tab_products:
                st.subheader("📦 کاڵاکانت لێرە زیاد بکە بۆ ئەوەی بخرێتە بازارەوە:")
                with st.form("add_product_form"):
                    p_name = st.text_input("ناوی بەرهەم:")
                    p_price = st.number_input("نرخ بە دینار:", min_value=0)
                    p_desc = st.text_area("ڕوونکردنەوەی بەرهەم:")
                    p_img = st.text_input("بەستەری وێنە (Image Link):", "https://images.unsplash.com/photo-1527799863-17b075e32712")
                    sub_p = st.form_submit_button("پاشەکەوتکردن")
                    if sub_p and p_name:
                        cursor.execute("INSERT INTO products (merchant_id, name, price, description, img_url) VALUES (?, ?, ?, ?, ?)",
                                       (st.session_state.user_id, p_name, p_price, p_desc, p_img))
                        conn.commit()
                        st.success("بەرهەمەکەت زیادکرا و ئێستا لە بەشی بازاردا دەبینرێت!")
                        st.rerun()

            with tab_finance:
                st.subheader("💰 حیساباتی سەرتاشەکان و دابەشبوونی داهات")
                if "Barber" in b_type:
                    st.write("داهاتی کۆی دەلاکەکان و کۆمسیۆنی پلاتفۆرم بەپێی نۆرە پشتڕاستکراوەکان:")
                    cursor.execute("SELECT COUNT(id) FROM bookings WHERE merchant_id = ? AND status = 'Confirmed'", (st.session_state.user_id,))
                    confirmed_count = cursor.fetchone()[0] or 0
                    
                    total_revenue = confirmed_count * 10000
                    platform_share = total_revenue * (comm_rate / 100.0)
                    staff_and_shop_share = total_revenue - platform_share
                    
                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        st.metric("کۆی داهاتی گشتی", f"{total_revenue:,} IQD")
                    with col_f2:
                        st.metric(f"پشکی سەنتەر (%{comm_rate})", f"{platform_share:,} IQD")
                    with col_f3:
                        st.metric("پشکی ماوەی کارمەندان", f"{staff_and_shop_share:,} IQD")
                else:
                    st.info("تەنها بۆ جۆری پیشەی Barber حیساباتی ئۆتۆماتیکی داهات کار دەکات.")
