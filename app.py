import streamlit as st
import sqlite3
import datetime
import pandas as pd

# 1. ڕێکخستنی لاپەڕەکە بە شێوازێکی پڕۆفیشناڵ
st.set_page_config(
    page_title="سەنتەری شاهانە | Royal Core Global SaaS",
    page_icon="👑",
    layout="wide"
)

# 2. دروستکردنی داتابەیسی بەهێزی SQLite
conn = sqlite3.connect("royal_core_enterprise.db", check_same_thread=False)
cursor = conn.cursor()

# دروستکردنی خشتە جیهانییەکان
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
    view_date TEXT,
    view_count INTEGER DEFAULT 0
)
""")
conn.commit()

# 3. تراککردنی سەردانیکەران
today_str = datetime.date.today().isoformat()
cursor.execute("SELECT view_count FROM page_views WHERE view_date = ?", (today_str,))
row = cursor.fetchone()
if row is None:
    cursor.execute("INSERT INTO page_views (view_date, view_count) VALUES (?, 1)", (today_str,))
else:
    cursor.execute("UPDATE page_views SET view_count = view_count + 1 WHERE view_date = ?", (today_str,))
conn.commit()

# 4. جادووکردنی شاشەکە بە دیزاینی شاهانەی زێڕین و ڕەش (Dark Gold CSS)
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
        padding: 20px;
        background: linear-gradient(135deg, #161822 0%, #0b0c10 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
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
        background: rgba(255, 255, 255, 0.01) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center;
        transition: all 0.3s ease;
    }
    .product-box:hover {
        border-color: #d4af37 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
        transform: translateY(-5px);
    }
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.5) !important;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# باری کۆنتڕۆڵی مێشک
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None  # 'super_admin' یان 'merchant'
    st.session_state.user_id = None
    st.session_state.business_name = None

# ==========================================
# 🍔 مینیۆی لای چەپ (Sidebar Control Panel)
# ==========================================
st.sidebar.markdown("<h2 style='color:#d4af37; text-align:center;'>👑 ROYAL CORE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; font-size:11px; color:#8892b0;'>GLOBAL MULTI-TENANT SAAS</p>", unsafe_allow_html=True)

st.sidebar.write("---")

menu_choice = st.sidebar.radio(
    "🧭 مینیۆی گەڕان",
    options=["🏠 لاپەڕەی گشتی شاهانە", "🛍️ بازار و کەرەستەکان", "📢 داواکردنی ڕیکلام", "🔑 چوونەژوورەوەی بازرگانان"]
)

if st.session_state.logged_in:
    st.sidebar.success(f"🔓 سەردانی وەک: {st.session_state.user_role.upper()}")
    if st.sidebar.button("🚪 دەرچوون لە سیستم", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_id = None
        st.session_state.business_name = None
        st.rerun()

# ==========================================
# 🏠 لاپەڕەی گشتی شاهانە (Home)
# ==========================================
if menu_choice == "🏠 لاپەڕەی گشتی شاهانە":
    st.markdown("""
        <div class="royal-header">
            <h1 style="color:#d4af37; margin:0;">👑 ئیمپراتۆریەتی شاهانە</h1>
            <p style="color:#8892b0; margin:5px 0 0 0;">گەورەترین سەکۆی مۆڵتی-بازرگانی بۆ سەرجەم خزمەتگوزارییەکان لە کوردستان</p>
        </div>
    """, unsafe_allow_html=True)
    
    # بزووێنەری ڕیکلامە چالاکەکان لە داتابەیسەوە
    cursor.execute("SELECT ad_text, ad_link FROM ads WHERE status = 'Approved'")
    approved_ads = cursor.fetchall()
    if approved_ads:
        for ad in approved_ads:
            st.markdown(f'<div class="ad-banner">📢 <a href="{ad[1]}" target="_blank" style="color:black; text-decoration:none;">{ad[0]}</a></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ad-banner">📢 پلاتفۆرمی شاهانە: کارەکانت لێرە بەرز بکەرەوە بۆ ئەوەی هەموو کوردستان بت بینن!</div>', unsafe_allow_html=True)

    st.subheader("🏢 ئەو بزنسانەی لەگەڵمان ئەکتیڤن")
    cursor.execute("SELECT id, business_name, business_type FROM merchants")
    all_merchants = cursor.fetchall()
    
    if not all_merchants:
        st.info("هێشتا هیچ بزنسێک لە پلاتفۆرمەکەدا تۆمار نەکراوە.")
    else:
        cols = st.columns(3)
        for idx, merchant in enumerate(all_merchants):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="main-card" style="text-align:center; border-color:#d4af37 !important;">
                        <h3 style="color:#d4af37; margin:0;">{merchant[1]}</h3>
                        <p style="color:#8892b0; font-size:12px; margin:5px 0;">پیشە: {merchant[2]}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # گرنگ: سیستمی نۆرەگرتنی کڕیاران بە شێوازی داینامیکی
                if st.button("📅 نۆرە بگرە لەم بزنسە", key=f"book_btn_{merchant[0]}"):
                    st.markdown(f"#### 📝 فۆرمی نۆرەگرتن لە **{merchant[1]}**")
                    with st.form(f"book_form_{merchant[0]}"):
                        cust_name = st.text_input("ناوی خۆت بنووسە:")
                        cust_phone = st.text_input("ژمارەی مۆبایلت:")
                        
                        # هێنانی کارمەندەکانی ئەم بزنسە دیاریکراوە
                        cursor.execute("SELECT id, staff_name, role FROM staff WHERE merchant_id = ?", (merchant[0],))
                        staff_members = cursor.fetchall()
                        
                        staff_options = {f"{s[1]} ({s[2]})": s[0] for s in staff_members} if staff_members else {"هەر کارمەندێک بێت": 0}
                        selected_staff = st.selectbox("کارمەند هەڵبژێرە:", options=list(staff_options.keys()))
                        
                        b_date = st.date_input("ڕۆژ هەڵبژێرە:", min_value=datetime.date.today())
                        b_time = st.time_input("کاتژمێر دیاری بکە:")
                        
                        submitted_booking = st.form_submit_button("پەسەندکردنی نۆرەگرتن 🌟")
                        if submitted_booking:
                            if cust_name and cust_phone:
                                staff_id_val = staff_options[selected_staff]
                                cursor.execute("""
                                    INSERT INTO bookings (merchant_id, customer_name, customer_phone, staff_id, booking_date, booking_time)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (merchant[0], cust_name, cust_phone, staff_id_val, b_date.isoformat(), b_time.isoformat()))
                                conn.commit()
                                st.success(f"نۆرەکەت بە سەرکەوتوویی لە {merchant[1]} تۆمارکرا! 🎉")
                            else:
                                st.error("تکایە خانەکان بە دروستی پڕ بکەرەوە.")

# ==========================================
# 🛍️ بەشی بازار و کەرەستەکان (Shop View)
# ==========================================
elif menu_choice == "🛍️ بازار و کەرەستەکان":
    st.markdown("<h1 style='color:#d4af37;'>🛍️ بازار و فرۆشگای شاهانە</h1>", unsafe_allow_html=True)
    
    # فلتەرکردنی بەرهەمەکان بەپێی بازرگان یان مارکێت
    cursor.execute("SELECT m.business_name, p.name, p.price, p.description, p.img_url FROM products p JOIN merchants m ON p.merchant_id = m.id")
    products_list = cursor.fetchall()
    
    if not products_list:
        st.info("هیچ بەرهەمێک لە بازارەکەدا بوونی نییە لە ئێستادا.")
    else:
        cols = st.columns(4)
        for idx, prod in enumerate(products_list):
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="product-box">
                        <img src="{prod[4]}" style="width:100%; height:130px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
                        <h4 style="color:#d4af37; margin:5px 0;">{prod[1]}</h4>
                        <p style="font-size:11px; color:#8892b0; margin:0;">بزنس: {prod[0]}</p>
                        <p style="font-size:11px; color:#aaa; height:35px; overflow:hidden; margin:5px 0;">{prod[3]}</p>
                        <h3 style="color:#fff; font-size:14px; margin:5px 0;">{prod[2]:,} IQD</h3>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 کڕینی خێرا", key=f"buy_p_{idx}"):
                    st.success(f"داواکاری کڕین بۆ بەرهەمی {prod[1]} بە سەرکەوتوویی نێردرا! 📞")

# ==========================================
# 📢 داواکردنی ڕیکلام (Ad Portal)
# ==========================================
elif menu_choice == "📢 داواکردنی ڕیکلام":
    st.markdown("<h1 style='color:#d4af37;'>📢 پۆرتالی ڕیکلامی شاهانە</h1>", unsafe_allow_html=True)
    st.write("لێرەوە داوای ڕیکلام بکە تا نیشانی سەرجەم بەکارهێنەرانی پلاتفۆرمەکەمانی بدەین:")
    
    with st.form("ad_request_form"):
        c_name = st.text_input("ناوی بەڕێزت / کۆمپانیا:")
        c_phone = st.text_input("ژمارەی مۆبایل:")
        ad_text = st.text_area("دەقی ڕیکلامەکە (بۆ نموونە: باشترین کەرەستەی جوانکاری لە وڵاتەوە...):")
        ad_link = st.text_input("بەستەری ڕیکلام (Facebook / Instagram / URL):")
        months = st.slider("ماوەی نمایش بە مانگ:", 1, 12, 1)
        
        submit_ad = st.form_submit_button("ناردنی داواکاری بۆ پلاتفۆرمی شاهانە 🚀")
        if submit_ad:
            if c_name and c_phone and ad_text:
                cursor.execute("""
                    INSERT INTO ads (client_name, client_phone, ad_text, ad_link, duration_months)
                    VALUES (?, ?, ?, ?, ?)
                """, (c_name, c_phone, ad_text, ad_link, months))
                conn.commit()
                st.success("داواکارییەکەت نێردرا بۆ بەڕێوەبەری سەرەکی! دوای پێداچوونەوە چالاک دەکرێت. 📞✨")
            else:
                st.error("تکایە خانە سەرەکییەکان پڕ بکەرەوە!")

# ==========================================
# 🔑 چوونەژوورەوەی بازرگانان (Merchant/Admin Login)
# ==========================================
elif menu_choice == "🔑 چوونەژوورەوەی بازرگانان":
    if not st.session_state.logged_in:
        tab_login, tab_register = st.tabs(["🔑 چوونەژوورەوەی ئەندامان", "🏢 تۆمارکردنی بزنسی نوێ (SaaS)"])
        
        with tab_login:
            st.subheader("دەروازەی کارمەندان و ئەدمینەکان")
            email = st.text_input("Email:").strip().lower()
            password = st.text_input("Password:", type="password").strip()
            
            if st.button("🔑 چوونەژوورەوە"):
                if email == "admin@gmail.com" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "super_admin"
                    st.rerun()
                else:
                    # گەڕان لە داتابەیس بۆ بازرگانەکان
                    cursor.execute("SELECT id, business_name FROM merchants WHERE email = ? AND password = ?", (email, password))
                    m_row = cursor.fetchone()
                    if m_row:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "merchant"
                        st.session_state.user_id = m_row[0]
                        st.session_state.business_name = m_row[1]
                        st.rerun()
                    else:
                        st.error("ئیمەیڵ یان پاسۆردەکە هەڵەیە!")
                        
        with tab_register:
            st.subheader("🏢 پلاتفۆرمی جیهانی بازرگانان")
            st.write("بازرگانی خۆت لێرە تۆمار بکە و وەک ساڵۆن یان ناوەندی کورس سوود لە سیستمەکەمان وەربگرە:")
            with st.form("reg_merchant_form"):
                reg_b_name = st.text_input("ناوی بزنسەکەت (بۆ نموونە: ساڵۆنی شاهانە):")
                reg_o_name = st.text_input("ناوی خاوەن کار:")
                reg_type = st.selectbox("جۆری کارەکەت:", ["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"])
                reg_email = st.text_input("📧 ئیمەیڵی فەرمی:")
                reg_pass = st.text_input("🔑 پاسۆردی نهێنی:", type="password")
                
                submitted_reg = st.form_submit_button("تۆمارکردن و دەستپێکردن 🚀")
                if submitted_reg:
                    if reg_b_name and reg_email and reg_pass:
                        try:
                            cursor.execute("""
                                INSERT INTO merchants (business_name, owner_name, business_type, email, password)
                                VALUES (?, ?, ?, ?, ?)
                            """, (reg_b_name, reg_o_name, reg_type, reg_email, reg_pass))
                            conn.commit()
                            st.success("بزنسەکەت بە سەرکەوتوویی تۆمارکرا! ئێستا دەتوانیت لە بەشی چوونەژوورەوە داخڵ ببیت.")
                        except sqlite3.IntegrityError:
                            st.error("ئەم ئیمەیڵە پێشتر بەکارهێنراوە!")
                    else:
                        st.error("تکایە زانیارییەکان بە تەواوی پڕ بکەرەوە.")

    else:
        # ========================================================
        # 👑 ١. پانێڵی دەسەڵاتی ڕەها: SUPER ADMIN (تۆ)
        # ========================================================
        if st.session_state.user_role == "super_admin":
            st.markdown("<h1 style='color:#d4af37;'>🛡️ پانێڵی فەرماندەیی شاهانە (Super-Admin)</h1>", unsafe_allow_html=True)
            
            tab_sys_views, tab_sys_merchants, tab_sys_ads = st.tabs(["📊 چاودێری سیستمی", "🏢 بەڕێوەبردنی بازرگانەکان", "📢 پەسەندکردنی ڕیکلامەکان"])
            
            with tab_sys_views:
                st.subheader("📈 چاودێری هاتوچۆی کڕیاران (Global Traffic)")
                cursor.execute("SELECT view_date, view_count FROM page_views ORDER BY view_date DESC LIMIT 10")
                views_data = cursor.fetchall()
                if views_data:
                    df = pd.DataFrame(views_data, columns=["بەروار", "سەردانیکەران"])
                    st.line_chart(df.set_index("بەروار"))
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("هیچ داتایەک نییە لە ئێستادا.")
                    
            with tab_sys_merchants:
                st.subheader("👥 بازرگانە چالاکەکانی سەر سایتەکە")
                cursor.execute("SELECT id, business_name, owner_name, business_type, email, commission_rate FROM merchants")
                merchants_list = cursor.fetchall()
                for m in merchants_list:
                    st.markdown(f"""
                        <div class="main-card">
                            <h4>🏢 ناوی بازرگان: {m[1]} ({m[3]})</h4>
                            <p>خاوەن کار: {m[2]} | ئیمەیڵ: {m[4]}</p>
                            <p>ڕێژەی کۆمسیۆنی شاهانە: <b>%{m[5]}</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with tab_sys_ads:
                st.subheader("📢 پێداچوونەوە بە داواکارییەکانی ڕیکلام")
                cursor.execute("SELECT id, client_name, client_phone, ad_text, ad_link, duration_months FROM ads WHERE status = 'Pending'")
                p_ads = cursor.fetchall()
                if not p_ads:
                    st.info("هیچ داواکارییەکی نوێی ڕیکلام نییە.")
                else:
                    for ad in p_ads:
                        st.write(f"👤 **داواکار:** {ad[1]} ({ad[2]}) - ماوەی **{ad[5]} مانگ**")
                        st.info(f"دەق: {ad[3]}")
                        col_ap1, col_ap2 = st.columns(2)
                        with col_ap1:
                            if st.button("✅ بڵاوکردنەوەی ڕیکلام", key=f"app_ad_{ad[0]}"):
                                start = datetime.date.today()
                                end = start + datetime.timedelta(days=ad[5]*30)
                                cursor.execute("UPDATE ads SET status = 'Approved', start_date = ?, end_date = ? WHERE id = ?", (start.isoformat(), end.isoformat(), ad[0]))
                                conn.commit()
                                st.success("ڕیکلامەکە ڕاستەوخۆ چالاک بوو!")
                                st.rerun()
                        with col_ap2:
                            if st.button("❌ سرینەوە", key=f"del_ad_{ad[0]}"):
                                cursor.execute("DELETE FROM ads WHERE id = ?", (ad[0],))
                                conn.commit()
                                st.rerun()

        # ========================================================
        # 🏢 ٢. پانێڵی بازرگانەکان: MERCHANT DASHBOARD
        # ========================================================
        elif st.session_state.user_role == "merchant":
            st.markdown(f"<h1 style='color:#d4af37;'>🏢 مەکۆی بەڕێوەبردنی: {st.session_state.business_name}</h1>", unsafe_allow_html=True)
            
            tab_m_bookings, tab_m_staff, tab_m_products = st.tabs(["📅 بەڕێوەبردنی نۆرەکان", "👥 کارمەندەکان", "📦 زیادکردنی بەرهەم"])
            
            # بەشی نۆرەکان
            with tab_m_bookings:
                st.subheader("📅 خشتەی کار و کاتی نۆرەکانی کڕیارانت")
                cursor.execute("""
                    SELECT b.id, b.customer_name, b.customer_phone, s.staff_name, b.booking_date, b.booking_time, b.status 
                    FROM bookings b LEFT JOIN staff s ON b.staff_id = s.id 
                    WHERE b.merchant_id = ?
                """, (st.session_state.user_id,))
                b_list = cursor.fetchall()
                
                if not b_list:
                    st.info("هیچ نۆرەیەک بەردەست نییە لە ئێستادا.")
                else:
                    for b in b_list:
                        st.markdown(f"""
                            <div class="main-card">
                                <h4>👤 کڕیار: {b[1]} ({b[2]})</h4>
                                <p>کارمەندی دیاریکراو: <b>{b[3] if b[3] else "دیاری نەکراوە"}</b></p>
                                <p>📅 ڕۆژ: {b[4]} | ⏰ کاتژمێر: {b[5]} | دۆخ: <b>{b[6]}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                        if b[6] == 'Pending':
                            if st.button("✅ پشتڕاستکردنەوەی نۆرە", key=f"conf_b_{b[0]}"):
                                cursor.execute("UPDATE bookings SET status = 'Confirmed' WHERE id = ?", (b[0],))
                                conn.commit()
                                st.rerun()
                                
            # بەشی کارمەندەکان
            with tab_m_staff:
                st.subheader("👥 کارمەندەکانی لای خۆت تۆمار بکە:")
                with st.form("add_staff_form"):
                    st_name = st.text_input("ناوی کارمەند:")
                    st_role = st.text_input("ڕۆڵ / پیشە (بۆ نموونە: دیزاینەر، سەرتاشی گەورە):")
                    sub_staff = st.form_submit_button("زیادکردنی کارمەند ➕")
                    if sub_staff and st_name:
                        cursor.execute("INSERT INTO staff (merchant_id, staff_name, role) VALUES (?, ?, ?)", (st.session_state.user_id, st_name, st_role))
                        conn.commit()
                        st.success("کارمەندەکە بە سەرکەوتوویی زیادکرا!")
                        st.rerun()
                
                cursor.execute("SELECT id, staff_name, role FROM staff WHERE merchant_id = ?", (st.session_state.user_id,))
                all_staff = cursor.fetchall()
                for s in all_staff:
                    st.write(f"👤 **{s[1]}** - {s[2]}")
                    
            # بەشی بەرهەمەکان
            with tab_m_products:
                st.subheader("📦 کاڵا و بەرهەمەکان لێرەوە زیاد بکە:")
                with st.form("add_prod_form"):
                    p_name = st.text_input("ناوی بەرهەم:")
                    p_price = st.number_input("نرخ (دینار):", min_value=0)
                    p_desc = st.text_area("وەسفکردنی کورت:")
                    p_img = st.text_input("بەستەری وێنە (Image Link):", "https://images.unsplash.com/photo-1527799863-17b075e32712")
                    sub_prod = st.form_submit_button("تۆمارکردنی کاڵا 💾")
                    if sub_prod and p_name:
                        cursor.execute("INSERT INTO products (merchant_id, name, price, description, img_url) VALUES (?, ?, ?, ?, ?)", 
                                       (st.session_state.user_id, p_name, p_price, p_desc, p_img))
                        conn.commit()
                        st.success("بەرهەمەکەت زیادکرا و ئێستا لە بەشی بازاردا دەبینرێت!")
