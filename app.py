import streamlit as st
import sqlite3
import datetime
import pandas as pd
import time
from config import LANG_DICT
from styles import inject_royal_styles  # هاوردەکردنی فایلی دیزاینەکان

# ========================================================
# ١. ڕێکخستنی لاپەڕە و لێدانی دیزاینی تاریکی زێڕینی شاهانە
# ========================================================
st.set_page_config(
    page_title="ئیمپڕاتۆریەتی شاهانە | Royal Core SaaS",
    page_icon="👑",
    layout="wide"
)

# بانگکردنی فەنکشنی دیزاینەکان لە فایلی styles.py
inject_royal_styles()

# ========================================================
# ٢. بەستنەوەی داتابەیسی SQLite هەمیشەیی و چاککردنی خشتەکان
# ========================================================
conn = sqlite3.connect("royal_core_ultimate.db", check_same_thread=False)
cursor = conn.cursor()

# دروستکردنی خشتەکان بە پارێزراوی و زیادکردنی خانە نوێیەکان بەپێی ڕێنماییەکان
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS page_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_date TEXT UNIQUE,
    view_count INTEGER DEFAULT 0
)
""")

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
conn.commit()

# دڵنیابوونەوە لە هەمیشەیی بوونی هەندێک خانە لە داتابەیسە کۆنەکاندا
try:
    cursor.execute("ALTER TABLE merchants ADD COLUMN phone TEXT")
    cursor.execute("ALTER TABLE merchants ADD COLUMN country TEXT")
    cursor.execute("ALTER TABLE merchants ADD COLUMN city TEXT")
    cursor.execute("ALTER TABLE merchants ADD COLUMN address TEXT")
    conn.commit()
except sqlite3.OperationalError:
    pass  # خانەکان پێشتر بوونیان هەبووە

try:
    cursor.execute("ALTER TABLE ads ADD COLUMN business_name TEXT")
    cursor.execute("ALTER TABLE ads ADD COLUMN country TEXT")
    cursor.execute("ALTER TABLE ads ADD COLUMN city TEXT")
    cursor.execute("ALTER TABLE ads ADD COLUMN business_type TEXT")
    cursor.execute("ALTER TABLE ads ADD COLUMN address TEXT")
    conn.commit()
except sqlite3.OperationalError:
    pass

# ژماردنی سەردانیکەرانی ڕۆژانە بە شێوازێکی هەمیشەیی بێ تێکچوون
today_str = datetime.date.today().isoformat()
cursor.execute("INSERT OR IGNORE INTO page_views (view_date, view_count) VALUES (?, 0)", (today_str,))
cursor.execute("UPDATE page_views SET view_count = view_count + 1 WHERE view_date = ?", (today_str,))
conn.commit()

if "lang" not in st.session_state:
    st.session_state.lang = "Kurdish"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.business_name = None
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {product_id: {"name": name, "price": price, "qty": qty, "merchant_id": m_id}}

T = LANG_DICT[st.session_state.lang]

# ========================================================
# ☰ مینیۆی لای تەنیشت بە شێوازی سێ هێڵەکان (Sidebar Menu ☰)
# ========================================================
st.sidebar.markdown("<h2 style='color:#d4af37; text-align:center;'>☰ ROYAL CORE</h2>", unsafe_allow_html=True)
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
        st.session_state.cart = {}
        st.rerun()

# زانیاری دەربارەی ڤێرژن و خاوەندارێتی لە ژێرەوەی سێ هێڵەکە
st.sidebar.write("---")
st.sidebar.markdown("""
    <div style="text-align: center; color: #8892b0; font-size: 11px;">
        <p>👑 وێبسایتی جیهانی شاهانە</p>
        <p>ساڵی دروستکردن: 2024 - 2026</p>
        <p>خاوەن ماف: Royal Core Team</p>
        <p>ڤێرژنی نوێ: <b>v2.1.0 Stable</b></p>
    </div>
""", unsafe_allow_html=True)

# ========================================================
# 🏠 لاپەڕەی سەرەکی (Home Page)
# ========================================================
if menu_choice == T["home"]:
    # کات و بەرواری ڕێک لە سەرەوەی ماڵپەڕ
    now_dt = datetime.datetime.now().strftime("%Y-%m-%d | %I:%M:%S %p")
    st.markdown(f"<div style='text-align: right; color:#d4af37; font-size:13px; font-weight:bold; margin-bottom:10px;'>🕒 {now_dt}</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="royal-header">
            <h1 style="color:#d4af37; margin:0; font-size: 32px;">{T['title']}</h1>
            <p style="color:#8892b0; margin:8px 0 0 0; font-size: 15px;">{T['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # بزوێنەری گەڕان بەپێی بەروار، ناو، بەرهەم یان بزنس لە لاپەڕەی سەرەکی
    search_q = st.text_input(T["search_label"], "").strip()
    
    # چاککردنی لۆجیکی پیشاندانی ڕیکلامەکان بە شێوازی چرکە بە چرکە و جوڵاو لەجیاتی لە ژێر یەکتر
    cursor.execute("SELECT ad_text, ad_link FROM ads WHERE status = 'Approved'")
    approved_ads = cursor.fetchall()
    
    if approved_ads:
        # بەکارهێنانی State بۆ گۆڕینی ئۆتۆماتیکی ڕیکلام بە شێوازی خولی
        if "ad_index" not in st.session_state:
            st.session_state.ad_index = 0
        
        current_ad = approved_ads[st.session_state.ad_index % len(approved_ads)]
        
        st.markdown(f"""
            <div class="ad-banner">
                📢 <a href="{current_ad[1]}" target="_blank" style="color:black; text-decoration:none; font-size:18px;">
                    {current_ad[0]}
                </a>
            </div>
        """, unsafe_allow_html=True)
        
        # لۆجیکی جێگرەوەی کاتی بۆ خۆکار گۆڕین (لێرەدا دوگمەیەکمان داناوە بۆ گۆڕینی خێرا لەبەر سنووردارکردنی گەڕانەوەی Streamlit)
        if len(approved_ads) > 1:
            if st.button("🔄 ڕیکلامی داهاتوو", key="next_ad_btn"):
                st.session_state.ad_index = (st.session_state.ad_index + 1) % len(approved_ads)
                st.rerun()
    else:
        st.markdown(f'<div class="ad-banner">📢 {T["plat_banner"]}</div>', unsafe_allow_html=True)

    st.subheader(T["active_merchants"])
    
    # ئەنجامی گەڕان ئەگەر تێکست نووسرابوو
    if search_q:
        cursor.execute("""
            SELECT id, business_name, owner_name, business_type 
            FROM merchants 
            WHERE (business_name LIKE ? OR owner_name LIKE ? OR business_type LIKE ?) 
            AND business_type = ?
        """, (f"%{search_q}%", f"%{search_q}%", f"%{search_q}%", biz_type))
    else:
        cursor.execute("SELECT id, business_name, owner_name, business_type FROM merchants WHERE business_type = ?", (biz_type,))
        
    merchants_list = cursor.fetchall()
    
    if not merchants_list:
        st.info(T["no_merchant"])
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
                
                # پاراستنی کۆنترۆڵی کارە جیاوازەکان (تۆمارکردنی نۆرە یان ناونووسینی زمان)
                if "Barber" in merchant[3] or "Pharmacy" in merchant[3] or "General Market" in merchant[3]:
                    if st.button(T["book_btn"], key=f"book_m_{merchant[0]}"):
                        st.markdown(f"#### 📝 داواکردنی کات و نۆرە لە **{merchant[1]}**")
                        with st.form(f"booking_form_{merchant[0]}"):
                            c_name = st.text_input("ناو:")
                            c_phone = st.text_input("ژمارەی مۆبایل یان واتساپ:")
                            
                            cursor.execute("SELECT id, staff_name, role FROM staff WHERE merchant_id = ?", (merchant[0],))
                            staff_members = cursor.fetchall()
                            
                            # لۆجیکی زیادکردنی کارمەندەکانی تایبەت بە بزنس بۆ هەڵبژاردن لە لایەن موشتەری
                            if staff_members:
                                staff_options = {f"{s[1]} ({s[2]})": s[0] for s in staff_members}
                                sel_staff = st.selectbox("دیاریکردنی پێشکەشکار / کارمەندی دڵخواز:", options=list(staff_options.keys()))
                            else:
                                staff_options = {}
                                st.warning("⚠️ هێشتا هیچ کارمەندێکی فەرمی لێرە تۆمار نەکراوە، تکایە بۆ دڵنیابوونەوە لە نۆرە بە فۆرمی گشتی تۆمار بکە.")
                                sel_staff = None

                            b_date = st.date_input("ڕۆژ دیاری بکە:", min_value=datetime.date.today())
                            b_time = st.time_input("کاتژمێر:")
                            
                            submitted_booking = st.form_submit_button("تۆمارکردنی نۆرە بە فەرمی")
                            if submitted_booking:
                                if c_name and c_phone:
                                    s_id = staff_options[sel_staff] if sel_staff else None
                                    cursor.execute("""
                                        INSERT INTO bookings (merchant_id, customer_name, customer_phone, staff_id, booking_date, booking_time)
                                        VALUES (?, ?, ?, ?, ?, ?)
                                    """, (merchant[0], c_name, c_phone, s_id, b_date.isoformat(), b_time.isoformat()))
                                    conn.commit()
                                    st.success(f"🎉 نۆرەکەت لە ئەکاونتی {merchant[1]} بە سەرکەوتوویی و بەبێ کێشە تۆمارکرا!")
                                else:
                                    st.error("تکایە خانەکان بە تەواوی پڕ بکەرەوە پێش ناردن.")
                                    
                elif "Education" in merchant[3]:
                    if st.button("📚 ناونووسین لە کۆرسەکانی زمان", key=f"edu_m_{merchant[0]}"):
                        st.markdown(f"#### 📝 ناونووسین لە وانەکانی **{merchant[1]}**")
                        with st.form(f"edu_form_{merchant[0]}"):
                            stu_name = st.text_input("ناوى قوتابی:")
                            stu_phone = st.text_input("ژمارەی مۆبایل / واتساپ:")
                            lesson_level = st.selectbox("ئاستی وانەکان:", ["Level 1 (Basic)", "Level 2 (Intermediate)", "Level 3 (Advanced)"])
                            
                            submitted_edu = st.form_submit_button("پەسەندکردنی ناونووسین")
                            if submitted_edu:
                                if stu_name and stu_phone:
                                    cursor.execute("""
                                        INSERT INTO bookings (merchant_id, customer_name, customer_phone, staff_id, booking_date, booking_time, status)
                                        VALUES (?, ?, ?, NULL, ?, ?, 'Enrolled')
                                    """, (merchant[0], stu_name, stu_phone, datetime.date.today().isoformat(), lesson_level))
                                    conn.commit()
                                    st.success(f"🎓 پیرۆزە {stu_name}! ناوت بە سەرکەوتوویی لە کۆرسی فێربوونی زمانەکەدا تۆمارکرا!")
                                else:
                                    st.error("تکایە هەموو بەشەکان بە دروستی پڕ بکەرەوە.")

    st.write("---")
    
    # بەشی خزمەتگوزاری پەیوەندی بە ئەدمین بە ژمارەی واتساپ
    st.markdown(f"### {T['contact_admin']}")
    st.info("💬 پشتیوانی تەکنیکی شاهانە: [پەیوەندی بکە لە ڕێگەی واتساپەوە (WhatsApp)](https://wa.me/9647500000000)")
    
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
# 🛍️ بەشی بازار و کەرەستەکان (Shop View - لەگەڵ سەبەتە و چاککردنی فرۆشتنی کتێب)
# ========================================================
elif menu_choice == T["shop"]:
    st.markdown(f"<h1 style='color:#d4af37;'>{T['shop']}</h1>", unsafe_allow_html=True)
    
    # بزوێنەری گەڕان بۆ کەرەستە و بەرهەمەکان
    search_p = st.text_input("🔍 گەڕانی خێرا بۆ کەرەستەکان و بەرهەمەکان:", "").strip()
    
    if search_p:
        cursor.execute("""
            SELECT m.business_name, p.name, p.price, p.description, p.img_url, p.id, p.merchant_id 
            FROM products p 
            JOIN merchants m ON p.merchant_id = m.id 
            WHERE m.business_type = ? AND (p.name LIKE ? OR p.description LIKE ?)
        """, (biz_type, f"%{search_p}%", f"%{search_p}%"))
    else:
        cursor.execute("""
            SELECT m.business_name, p.name, p.price, p.description, p.img_url, p.id, p.merchant_id 
            FROM products p 
            JOIN merchants m ON p.merchant_id = m.id 
            WHERE m.business_type = ?
        """, (biz_type,))
        
    products_list = cursor.fetchall()
    
    if not products_list:
        st.info(T["no_product"])
    else:
        cols = st.columns(4)
        for idx, prod in enumerate(products_list):
            p_id = prod[5]
            p_merchant_id = prod[6]
            with cols[idx % 4]:
                # چارەسەری کێشەی وێنە، ئەگەر بەستەرەکە کێشەی هەبێت یان بەتاڵ بێت وێنەیەکی جێگرەوەی شاز دادەنێت
                img_path = prod[4] if prod[4] else "https://images.unsplash.com/photo-1527799863-17b075e32712"
                st.image(img_path, use_container_width=True)
                st.markdown(f"""
                    <div class="product-box">
                        <h4 style="color:#d4af37; margin:5px 0;">{prod[1]}</h4>
                        <p style="font-size:11px; color:#8892b0; margin:0;">بزنس: {prod[0]}</p>
                        <p style="font-size:11px; color:#aaa; margin:5px 0;">{prod[3]}</p>
                        <h3 style="color:#fff; font-size:16px; margin:5px 0;">{prod[2]:,} IQD</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # دوگمەی سەبەتەی کڕین
                if st.button("➕ خستنە ناو سەبەتە", key=f"add_cart_{p_id}", use_container_width=True):
                    if p_id not in st.session_state.cart:
                        st.session_state.cart[p_id] = {
                            "name": prod[1],
                            "price": prod[2],
                            "qty": 1,
                            "merchant_id": p_merchant_id
                        }
                    else:
                        st.session_state.cart[p_id]["qty"] += 1
                    st.success(f"📥 {prod[1]} خرایە سەبەتەکەتەوە!")
                    time.sleep(0.5)
                    st.rerun()

    # ... لێرەوە کۆدەکان ڕێک وەک خۆیان بەردەوامن تا کۆتایی بەبێ هیچ دەستکاریکردن یان گۆڕانکارییەک ...
    st.write("---")
    st.markdown("### 🛒 سەبەتەی کڕینی تۆ")
    if not st.session_state.cart:
        st.info("سەبەتەکەت لە ئێستادا بەتاڵە.")
    else:
        total_cart_price = 0
        cart_rows = []
        for p_id, item in list(st.session_state.cart.items()):
            sub_total = item["price"] * item["qty"]
            total_cart_price += sub_total
            
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; border: 1px solid rgba(212,175,55,0.1); margin-bottom: 8px;">
                    <b>{item['name']}</b> - نرخ: {item['price']:,} IQD | ژمارە: {item['qty']} دانە
                </div>
            """, unsafe_allow_html=True)
            
            c_col1, c_col2, c_col3 = st.columns([1, 1, 4])
            with c_col1:
                if st.button("➕ زیادکردن", key=f"inc_{p_id}"):
                    st.session_state.cart[p_id]["qty"] += 1
                    st.rerun()
            with c_col2:
                if st.button("➖ کەمکردنەوە", key=f"dec_{p_id}"):
                    st.session_state.cart[p_id]["qty"] -= 1
                    if st.session_state.cart[p_id]["qty"] <= 0:
                        del st.session_state.cart[p_id]
                    st.rerun()
            with c_col3:
                if st.button("❌ گەڕانەوە و لادان", key=f"remove_{p_id}"):
                    del st.session_state.cart[p_id]
                    st.rerun()
                    
        st.markdown(f"#### 💰 کۆی گشتی پارەی سەبەتە: **{total_cart_price:,} IQD**")
        
        # پڕکردنەوەی زانیاری موشتەری بۆ گەیاندن و ناردنی داواکاری بۆ بازرگان
        with st.form("checkout_form"):
            checkout_name = st.text_input("ناوی بەڕێزت بۆ تۆمارکردن:")
            checkout_phone = st.text_input("ژمارەی مۆبایل / واتساپ بۆ پەیوەندی:")
            submit_order = st.form_submit_button("🏁 ناردنی کۆتایی داواکاری بۆ بازرگانان")
            
            if submit_order:
                if checkout_name and checkout_phone:
                    # ناردنی داتاکان بۆ داتابەیس بۆ ئەوەی خاوەن بزنسەکان بیبینن
                    for p_id, item in st.session_state.cart.items():
                        detail_str = f"{item['name']} (Qty: {item['qty']})"
                        sub_total_p = item['price'] * item['qty']
                        cursor.execute("""
                            INSERT INTO orders (merchant_id, customer_name, customer_phone, product_details, total_price, order_date)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (item["merchant_id"], checkout_name, checkout_phone, detail_str, sub_total_p, datetime.date.today().isoformat()))
                    conn.commit()
                    st.session_state.cart = {}
                    st.success("🎉 داواکاریەکەت بە سەرکەوتوویی بۆ سەرجەم بازرگانەکان نێردرا و پاشەکەوت کرا! پێوەندی پێوە دەکەینەوە.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("تکایە ناونیشان و مۆبایلەکە بە تەواوی بنووسە.")

# ========================================================
# 📢 داواکردنی ڕیکلام (Ad Portal - لەگەڵ فۆڕمی ئینتەرناشناڵ)
# ========================================================
elif menu_choice == T["ad_portal"]:
    st.markdown(f"<h1 style='color:#d4af37;'>{T['ad_title']}</h1>", unsafe_allow_html=True)
    st.write(T["ad_intro"])
    
    with st.form("ad_portal_form_updated"):
        c_name = st.text_input(T["fullname"])
        b_name = st.text_input(T["bizname"])
        c_phone = st.text_input(T["phone_whats"])
        c_country = st.text_input(T["country"], value="Kurdistan / Iraq")
        c_city = st.text_input(T["city"])
        c_biz_type = st.selectbox("جۆری پیشە و بواری بزنسەکەت:", ["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare", "💼 Company / Other"])
        c_address = st.text_input(T["address"])
        ad_text = st.text_area(T["ad_text"])
        ad_link = st.text_input(T["ad_link"])
        duration = st.slider(T["ad_duration"], 1, 12, 1)
        
        submitted_ad = st.form_submit_button(T["ad_submit"])
        if submitted_ad:
            if c_name and b_name and c_phone and ad_text:
                cursor.execute("""
                    INSERT INTO ads (client_name, business_name, client_phone, country, city, business_type, address, ad_text, ad_link, duration_months)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (c_name, b_name, c_phone, c_country, c_city, c_biz_type, c_address, ad_text, ad_link, duration))
                conn.commit()
                st.success(T["success_ad"])
            else:
                st.error(T["fill_fields"])

# ========================================================
# 🔑 دەروازەی ئەندامان و ئەدمین (Members and SaaS System)
# ========================================================
elif menu_choice == T["login_btn"]:
    if not st.session_state.logged_in:
        tab_login, tab_register = st.tabs(["🔑 چوونەژوورەوەی ئەندامان", "🏢 تۆمارکردنی بازرگانی نوێ (SaaS)"])
        
        with tab_login:
            st.subheader("چوونەژوورەوەی بەڕێوەبەران یان بازرگانان")
            email_val = st.text_input(T["username"], key="login_email").strip().lower()
            pass_val = st.text_input(T["password"], type="password", key="login_pass").strip()
            
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
                        st.error("زانیارییەکان تەواو نین یان پاسۆرد و ئیمەیڵەکەت هەڵەیە!")
                        
        with tab_register:
            st.subheader(T["reg_banner"])
            
            # لۆجیکی نێودەوڵەتی بە ڕێگریکردن لە سووربوونی بێزارکەری خانەکان بەبێ هۆکار
            reg_b_name = st.text_input("ناوی گشتی پڕۆژە / کارەکەت:")
            reg_o_name = st.text_input(T["owner_name"])
            reg_b_type = st.selectbox(T["biz_sec"], ["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"])
            reg_phone = st.text_input("ژمارەی مۆبایلی فەرمی:")
            reg_country = st.text_input("وڵات یان هەرێم:", value="Kurdistan")
            reg_city = st.text_input("شار یان ناوچە:")
            reg_address = st.text_input(T["address"])
            reg_b_email = st.text_input("📧 ئیمەیڵی فەرمی بۆ هاتنە ژوورەوە:")
            reg_b_pass = st.text_input("🔑 پاسۆردی نهێنی نوێ:", type="password")
            
            # چاودێری سووربوونی خانەکان و ڕوونکردنەوەی کێشەکە بۆ بەکارهێنەر
            errors = []
            if not reg_b_name:
                errors.append("ناوی پڕۆژە ناتوانرێت بەتاڵ بێت.")
            if not reg_b_email or "@" not in reg_b_email:
                errors.append("ئیمەیڵەکە بە تەواوی و بە هێمای @ بنووسە.")
            if not reg_b_pass or len(reg_b_pass) < 6:
                errors.append("پاسۆرد پێویستە لە 6 حەرف کەمتر نەبێت.")
                
            if errors:
                st.markdown("<div class='error-box-custom'>❌ تکایە ئاگاداربە: " + " | ".join(errors) + "</div>", unsafe_allow_html=True)
                
            if st.button(T["reg_btn"]):
                if not errors and reg_o_name and reg_phone:
                    try:
                        cursor.execute("""
                            INSERT INTO merchants (business_name, owner_name, business_type, email, password, phone, country, city, address)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (reg_b_name, reg_o_name, reg_b_type, reg_b_email.strip().lower(), reg_b_pass, reg_phone, reg_country, reg_city, reg_address))
                        conn.commit()
                        st.success(T["reg_success"])
                    except sqlite3.IntegrityError:
                        st.error(T["email_exists"])
                else:
                    st.error("تکایە سەرجەم کێشەکانی ناو خانە سوورەکان چارەسەر بکە پێش کڕیک کردن!")

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
                cursor.execute("SELECT id, business_name, owner_name, business_type, email, commission_rate, phone, city FROM merchants")
                m_list = cursor.fetchall()
                for m in m_list:
                    st.markdown(f"""
                        <div class="main-card">
                            <h4>🏢 ناوی پڕۆژە: {m[1]} ({m[3]})</h4>
                            <p>خاوەن کار: {m[2]} | مۆبایل: {m[6]} | شار: {m[7]}</p>
                            <p>ئیمەیڵی فەرمی: {m[4]} | ڕێژەی کۆمسیۆن: <b>%{m[5]}</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with tab_ads:
                st.subheader("📢 داواکارییە نوێیەکانی ڕیکلام")
                cursor.execute("""
                    SELECT id, client_name, business_name, client_phone, ad_text, ad_link, duration_months, city 
                    FROM ads WHERE status = 'Pending'
                """)
                p_ads = cursor.fetchall()
                if not p_ads:
                    st.info("هیچ داواکارییەکی نوێ نییە بۆ پەسەندکردن.")
                else:
                    for ad in p_ads:
                        st.write(f"👤 **کڕیار:** {ad[1]} (کۆمپانیا: {ad[2]}) - شار: {ad[7]} | مۆبایل: {ad[3]}")
                        st.info(f"دەقی ڕیکلام: {ad[4]}")
                        col_ap1, col_ap2 = st.columns(2)
                        with col_ap1:
                            if st.button("✅ بڵاوکردنەوەی ڕیکلام", key=f"app_{ad[0]}"):
                                start = datetime.date.today()
                                end = start + datetime.timedelta(days=ad[6]*30)
                                cursor.execute("UPDATE ads SET status = 'Approved', start_date = ?, end_date = ? WHERE id = ?", (start.isoformat(), end.isoformat(), ad[0]))
                                conn.commit()
                                st.success("ڕیکلامەکە ڕاستەوخۆ چالاک کرا!")
                                time.sleep(0.5)
                                st.rerun()
                        with col_ap2:
                            if st.button("❌ سڕینەوە", key=f"del_{ad[0]}"):
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
            
            tab_bookings, tab_staff, tab_products, tab_orders, tab_finance, tab_customers = st.tabs([
                T["booking_management"], 
                T["staff_management"], 
                T["product_management"], 
                "📦 داواکارییەکانی کڕین",
                T["finance_tab"], 
                "👥 کڕیارە دایمییەکان"
            ])
            
            with tab_bookings:
                if "Barber" in b_type or "Pharmacy" in b_type or "General Market" in b_type:
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
                                    st.success("نۆرەکە پەسەندکرا!")
                                    time.sleep(0.5)
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
                                    st.success("قوتابیەکە بە سەرکەوتوویی وەرگیرا!")
                                    time.sleep(0.5)
                                    st.rerun()

            with tab_staff:
                st.subheader("👥 کارمەندی نوێ زیاد بکە:")
                with st.form("add_staff_form"):
                    s_name = st.text_input("ناوی کارمەند:")
                    s_role = st.text_input("ناونیشان یان پیشەی کارمەندەکەت:")
                    sub_staff = st.form_submit_button("تۆمارکردنی کارمەند")
                    if sub_staff and s_name:
                        cursor.execute("INSERT INTO staff (merchant_id, staff_name, role) VALUES (?, ?, ?)", (st.session_state.user_id, s_name, s_role))
                        conn.commit()
                        st.success("کارمەندەکە زیادکرا!")
                        time.sleep(0.5)
                        st.rerun()
                        
                st.write("---")
                st.subheader("کارمەندە چالاکەکان")
                cursor.execute("SELECT staff_name, role FROM staff WHERE merchant_id = ?", (st.session_state.user_id,))
                staff_list = cursor.fetchall()
                for s in staff_list:
                    st.write(f"👤 **{s[0]}** - {s[1]}")

            with tab_products:
                st.subheader("📦 کاڵاکانت لێرە زیاد بکە بۆ ئەوەی بخرێتە بازاڕەوە:")
                with st.form("add_product_form"):
                    p_name = st.text_input("ناوی بەرهەم یان کتێب:")
                    p_price = st.number_input("نرخ بە دینار:", min_value=0)
                    p_desc = st.text_area("ڕوونکردنەوەی گشتی:")
                    p_img = st.text_input("بەستەری وێنە (Image Link) - بۆ پیشاندان لە بازاڕ:", "https://images.unsplash.com/photo-1527799863-17b075e32712")
                    sub_p = st.form_submit_button("پاشەکەوتکردن")
                    if sub_p and p_name:
                        cursor.execute("INSERT INTO products (merchant_id, name, price, description, img_url) VALUES (?, ?, ?, ?, ?)",
                                       (st.session_state.user_id, p_name, p_price, p_desc, p_img))
                        conn.commit()
                        st.success("بەرهەم یان کتێبەکەت زیادکرا و ئێستا لە بەشی بازاڕدا دەبینرێت!")
                        time.sleep(0.5)
                        st.rerun()

            with tab_orders:
                st.subheader("📦 داواکارییە کڕاوەکانی کڕیاران")
                cursor.execute("SELECT id, customer_name, customer_phone, product_details, total_price, order_date, status FROM orders WHERE merchant_id = ?", (st.session_state.user_id,))
                order_list = cursor.fetchall()
                if not order_list:
                    st.info("هیچ داواکارییەکی نوێی کڕینی بەرهەم لای تۆ نییە لە ئێستادا.")
                else:
                    for ord in order_list:
                        st.markdown(f"""
                            <div class="main-card">
                                <h4>👤 کڕیار: {ord[1]} ({ord[2]})</h4>
                                <p>بەرهەم: <b>{ord[3]}</b> | کۆی گشتی: {ord[4]:,} IQD</p>
                                <p>بەروار: {ord[5]} | دۆخی گەیاندن: <b>{ord[6]}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                        if ord[6] == 'Pending':
                            if st.button("✅ ناردنی کاڵا و تەواوکردن", key=f"ship_{ord[0]}"):
                                cursor.execute("UPDATE orders SET status = 'Shipped' WHERE id = ?", (ord[0],))
                                conn.commit()
                                  st.success("دۆخی داواکارییەکە نوێکرایەوە!")
                                time.sleep(0.5)
                                st.rerun()

            with tab_finance:
                st.subheader("💰 حیساباتی دارایی داهات بەپێی پیشە")
                
                # لۆجیکی جیاوازی دارایی بەپێی جۆری کار بۆ سڕینەوەی کێشەی سەرتاش لە هەموو بەشەکان
                if "Barber" in b_type:
                    st.write("داهاتی کۆی دەلاکەکان و کۆمسیۆنی پلاتفۆڕم بەپێی نۆرە پشتڕاستکراوەکان:")
                    cursor.execute("SELECT COUNT(id) FROM bookings WHERE merchant_id = ? AND status = 'Confirmed'", (st.session_state.user_id,))
                    confirmed_count = cursor.fetchone()[0] or 0
                    total_revenue = confirmed_count * 10000
                elif "Education" in b_type:
                    st.write("داهاتی پەیمانگا بەپێی خوێندکارە چالاکەکان:")
                    cursor.execute("SELECT COUNT(id) FROM bookings WHERE merchant_id = ? AND status = 'Active Student'", (st.session_state.user_id,))
                    confirmed_count = cursor.fetchone()[0] or 0
                    total_revenue = confirmed_count * 150000  # نرخی وێنەکراوی کۆرسی زمان
                else:
                    # بۆ دەرمانخانەکان یان مارکێتەکان ژووری دارایی گرێدراوە بە فرۆشتنی بەرهەمەکان
                    cursor.execute("SELECT SUM(total_price) FROM orders WHERE merchant_id = ? AND status = 'Shipped'", (st.session_state.user_id,))
                    total_revenue = cursor.fetchone()[0] or 0
                
                platform_share = total_revenue * (comm_rate / 100.0)
                staff_and_shop_share = total_revenue - platform_share
                
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    st.metric("کۆی داهاتی گشتی کارەکان", f"{total_revenue:,} IQD")
                with col_f2:
                    st.metric(f"پشکی پلاتفۆڕم (%{comm_rate})", f"{platform_share:,} IQD")
                with col_f3:
                    st.metric("پشکی ماوەی سەنتەرەکە", f"{staff_and_shop_share:,} IQD")

            with tab_customers:
                st.subheader("👥 چاودێری کڕیارە دایمییەکان و فیدباک")
                st.write("لێرەوە دەتوانیت کڕیارە هەرە چالاکەکانت ببینی بۆ کردنی داشکاندنی بەردەوام:")
                
                # دەرهێنانی داتای سەردانی کڕیارەکان
                cursor.execute("""
                    SELECT customer_name, customer_phone, COUNT(id) as visit_count 
                    FROM bookings WHERE merchant_id = ? 
                    GROUP BY customer_phone ORDER BY visit_count DESC
                """, (st.session_state.user_id,))
                cust_data = cursor.fetchall()
                
                if not cust_data:
                    st.info("تائێستا مێژووی سەردانی کڕیاران لێرە تۆمار نەکراوە.")
                else:
                    for c_row in cust_data:
                        st.markdown(f"""
                            <div class="main-card">
                                <b>👤 ناو: {c_row[0]}</b> | مۆبایل: {c_row[1]} <br/>
                                🔄 ژمارەی سەردانەکان: <span style="color:#d4af37; font-weight:bold;">{c_row[2]} جار</span>
                            </div>
                        """, unsafe_allow_html=True)
