import streamlit as st
import sqlite3
import datetime
import pandas as pd

# 1. ڕێکخستنی سەرەتایی لاپەڕەکە
st.set_page_config(
    page_title="سەنتەری شاهانە | Royal Core Platform",
    page_icon="👑",
    layout="wide"
)

# 2. دروستکردن و بەستنەوەی داتابەیسی SQLite
conn = sqlite3.connect("royal_core.db", check_same_thread=False)
cursor = conn.cursor()

# دروستکردنی خشتەکان ئەگەر بوونیان نەبێت
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT,
    img_url TEXT,
    business_type TEXT
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
    status TEXT,
    start_date TEXT,
    end_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS page_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_date TEXT,
    view_count INTEGER
)
""")
conn.commit()

# 3. سیستمی تۆمارکردنی بینینی لاپەڕەکان (Traffic Tracker)
today_str = datetime.date.today().isoformat()
cursor.execute("SELECT view_count FROM page_views WHERE view_date = ?", (today_str,))
row = cursor.fetchone()
if row is None:
    cursor.execute("INSERT INTO page_views (view_date, view_count) VALUES (?, 1)", (today_str,))
else:
    cursor.execute("UPDATE page_views SET view_count = view_count + 1 WHERE view_date = ?", (today_str,))
conn.commit()

# 4. فەرهەنگی خێرای زمانەکان
LANG_DICT = {
    "Kurdish": {
        "title": "👑 سەنتەری شاهانە",
        "subtitle": "پلاتفۆرمی جیهانی بۆ بەڕێوەبردنی سەرجەم بزنسەکان",
        "home": "🏠 لاپەڕەی سەرەکی",
        "shop": "🛍️ مارکێتی شاهانە",
        "login_btn": "🔑 دەروازەی ئەندامان",
        "ad_portal": "📢 داواکردنی ڕیکلام",
        "business_type": "🏢 جۆری کارەکەت هەڵبژێرە:",
        "choose_lang": "🌐 زمان هەڵبژێرە / Choose Language",
        "quick_order": "🛒 داواکردنی خێرا",
    },
    "English": {
        "title": "👑 Royal Center",
        "subtitle": "Global platform to manage all your businesses",
        "home": "🏠 Home",
        "shop": "🛍️ VIP Shop",
        "login_btn": "🔑 Member Login",
        "ad_portal": "📢 Book an Ad",
        "business_type": "🏢 Select Business Type:",
        "choose_lang": "🌐 Choose Language",
        "quick_order": "🛒 Quick Order",
    },
    "Arabic": {
        "title": "👑 المركز الملكي",
        "subtitle": "المنصة العالمية لإدارة جميع أعمالك التجارية",
        "home": "🏠 الصفحة الرئيسية",
        "shop": "🛍️ السوق الملكي",
        "login_btn": "🔑 بوابة تسجيل الدخول",
        "ad_portal": "📢 طلب إعلان",
        "business_type": "🏢 اختر نوع العمل:",
        "choose_lang": "🌐 اختر اللغة",
        "quick_order": "🛒 طلب سريع",
    },
    "Turkish": {
        "title": "👑 Kraliyet Merkezi",
        "subtitle": "Tüm işletmelerinizi yönetmek için küresel platform",
        "home": "🏠 Anasayfa",
        "shop": "🛍️ VIP Mağaza",
        "login_btn": "🔑 Üye Girişi",
        "ad_portal": "📢 Reklam Ver",
        "business_type": "🏢 İşletme Türünü Seçin:",
        "choose_lang": "🌐 Dil Seçin",
        "quick_order": "🛒 Hızlı Sipariş",
    },
    "Persian": {
        "title": "👑 مرکز سلطنتی",
        "subtitle": "پلتفرم جهانی برای مدیریت تمام کسب‌وکارهای شما",
        "home": "🏠 صفحه اصلی",
        "shop": "🛍️ فروشگاه سلطنتی",
        "login_btn": "🔑 ورود پرسنل",
        "ad_portal": "📢 ثبت تبلیغات",
        "business_type": "🏢 نوع کسب‌وکار را انتخاب کنید:",
        "choose_lang": "🌐 انتخاب زبان",
        "quick_order": "🛒 سفارش سریع",
    }
}

# 5. لێدانی دەرزی جادوویی CSS بۆ دیزاینە تاریک و شاهانەکەت
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #12131a 0%, #08080c 100%) !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0c0d12 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.15) !important;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        margin-bottom: 20px;
    }
    .ad-banner {
        background: linear-gradient(90deg, #AA7C11 0%, #D4AF37 50%, #AA7C11 100%) !important;
        color: #000000 !important;
        padding: 12px !important;
        border-radius: 10px !important;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        margin-bottom: 25px;
    }
    .product-box {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center;
        transition: all 0.3s;
    }
    .product-box:hover {
        border-color: #D4AF37 !important;
        transform: translateY(-3px);
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# باری مێشک
if "lang" not in st.session_state:
    st.session_state.lang = "Kurdish"
if "business_type" not in st.session_state:
    st.session_state.business_type = "💇‍♂️ Barber & Salon"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

T = LANG_DICT[st.session_state.lang]

# ==========================================
# 🍔 مینیۆی لای چەپ (Sidebar Menu)
# ==========================================
st.sidebar.markdown("<h2 style='color:#D4AF37; text-align:center;'>👑 Royal Core</h2>", unsafe_allow_html=True)

# ١. گۆڕینی زمان (خێرا بەبێ لاگ)
st.session_state.lang = st.sidebar.selectbox(
    T["choose_lang"], 
    options=["Kurdish", "English", "Arabic", "Turkish", "Persian"],
    index=["Kurdish", "English", "Arabic", "Turkish", "Persian"].index(st.session_state.lang)
)

# ٢. گۆڕینی جۆری بزنسەکە
st.session_state.business_type = st.sidebar.selectbox(
    T["business_type"],
    options=["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"]
)

st.sidebar.write("---")

menu_option = st.sidebar.radio(
    "🧭 Navigation",
    options=[T["home"], T["shop"], T["ad_portal"], T["login_btn"]]
)

if st.session_state.logged_in:
    st.sidebar.write(f"Logged in: {st.session_state.current_user}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

# ==========================================
# 🏠 لاپەڕەی سەرەکی (Home)
# ==========================================
if menu_option == T["home"]:
    st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>{T['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #8892b0;'>{T['subtitle']}</p>", unsafe_allow_html=True)
    
    # 📢 نیشاندانی ڕیکلامە چالاکەکان بە شێوەی دینامیکی لە داتابەیسەوە!
    cursor.execute("SELECT ad_text, ad_link FROM ads WHERE status = 'Approved'")
    active_ads = cursor.fetchall()
    
    if active_ads:
        for ad in active_ads:
            st.markdown(f"""
                <div class="ad-banner">
                    📢 <a href="{ad[1]}" target="_blank" style="color:black; text-decoration:none;">{ad[0]}</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ad-banner">📢 ڕیکلامی تۆ لێرە: پەیوەندیمان پێوە بکە بۆ دانانی باشترین ڕیکلام!</div>', unsafe_allow_html=True)
        
    st.markdown(f"<h3>🏢 کارە چالاکەکە: <span style='color:#D4AF37;'>{st.session_state.business_type}</span></h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="main-card">
                <h3 style="color:#D4AF37;">💻 سیستمی مۆڵتی-بازرگانی</h3>
                <p>ئێستا خەڵک لە سەرانسەری کوردستان دەتوانن پڕۆفایلی بازرگانی خۆیان بە زمانی خۆیان بکەنەوە و کاڵاکانیان لێرەدا بفرۆشن.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        # پیشاندانی کۆی بینینەکان بۆ دروستکردنی متمانە
        cursor.execute("SELECT SUM(view_count) FROM page_views")
        total_views = cursor.fetchone()[0] or 124
        st.markdown(f"""
            <div class="main-card" style="text-align:center;">
                <h2 style="color:#D4AF37; margin:0;">📊 {total_views:,}</h2>
                <p>کۆی بینینی لاپەڕەکانمان - ئامادەین بۆ هاوبەشی و ڕیکلامی کارەکەت!</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 🛍️ بەشی دووەم: مارکێتی گشتی (Shop)
# ==========================================
elif menu_option == T["shop"]:
    st.markdown(f"<h1 style='color: #D4AF37;'>{T['shop']}</h1>", unsafe_allow_html=True)
    st.write(f"بەرهەمەکانی پێوەست بە: **{st.session_state.business_type}**")
    
    # هێنانەوەی بەرهەمە تۆمارکراوەکانی خەڵک لە داتابەیسەوە!
    cursor.execute("SELECT name, price, description, img_url FROM products WHERE business_type = ?", (st.session_state.business_type,))
    db_products = cursor.fetchall()
    
    if not db_products:
        st.info("هێشتا هیچ بەرهەمێک بۆ ئەم پیشەیە تۆمار نەکراوە. تۆ یەکەم کەس بە و تۆماری بکە!")
    else:
        # پیشاندانی بەرهەمەکان بە شێوازێکی زۆر مۆدێرن
        cols = st.columns(3)
        for idx, prod in enumerate(db_products):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-box">
                        <img src="{prod[3] or 'https://images.unsplash.com/photo-1527799863-17b075e32712'}" style="width:100%; border-radius:8px; height:150px; object-fit:cover; margin-bottom:10px;">
                        <h3 style="color:#D4AF37; margin:5px 0;">{prod[0]}</h3>
                        <p style="font-size:12px; color:#aaa; height:40px; overflow:hidden;">{prod[2]}</p>
                        <h4 style="color:#fff;">{prod[1]:,} IQD</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")
                if st.button(T["quick_order"], key=f"ord_{idx}"):
                    st.success(f"داواکارییەکەت بۆ {prod[0]} نێردرا! پەیوەندیت پێوە دەکەین. 📞")

# ==========================================
# 📢 بەشی سێیەم: پۆرتالی داواکردنی ڕیکلام (Book Ad)
# ==========================================
elif menu_option == T["ad_portal"]:
    st.markdown("<h1 style='color: #D4AF37;'>📢 داواکردنی ڕیکلامی سپۆنسەر</h1>", unsafe_allow_html=True)
    st.write("دەتەوێت کارەکەت نیشانی هەزاران سەردانیکەری ئێمە بدەیت؟ لێرەوە داواکاری بنێرە:")
    
    with st.form("ad_form"):
        c_name = st.text_input("ناوی بەڕێزت / کۆمپانیا:")
        c_phone = st.text_input("ژمارەی مۆبایل بۆ پەیوەندی:")
        ad_text = st.text_area("دەقی ڕیکلامەکە (بۆ نموونە: گەورەترین داشکاندنی ساڵ لە ساڵۆنی شاهانە...):")
        ad_link = st.text_input("بەستەری ڕیکلامەکە (Facebook, Instagram یان وێبسایت):")
        months = st.slider("ماوەی ڕیکلام بە مانگ:", 1, 12, 1)
        
        submitted = st.form_submit_button("ناردنی داواکاری بۆ تاوتوێکردن 🚀")
        if submitted:
            if c_name and c_phone and ad_text:
                cursor.execute("""
                    INSERT INTO ads (client_name, client_phone, ad_text, ad_link, duration_months, status)
                    VALUES (?, ?, ?, ?, ?, 'Pending')
                """, (c_name, c_phone, ad_text, ad_link, months))
                conn.commit()
                st.success("داواکارییەکەت بە سەرکەوتوویی نێردرا! لە ماوەیەکی زۆر کورتدا پەیوەندیت پێوە دەکەین بۆ پشتڕاستکردنەوە. 📞✨")
            else:
                st.error("تکایە خانە سەرەکییەکان پڕ بکەرەوە!")

# ==========================================
# 🔑 بەشی چوارەم: دەروازەی ئەندامان و پانێڵی ئەدمین
# ==========================================
elif menu_option == T["login_btn"]:
    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            st.markdown('<div class="main-card" style="text-align:center;"><h2>🔑 دەروازەی چوونەژوورەوە</h2></div>', unsafe_allow_html=True)
            email = st.text_input("📧 ئیمەیڵ:").strip().lower()
            password = st.text_input("🔑 پاسۆرد:", type="password").strip()
            
            st.write("")
            if st.button("پەیوەستبوون 🚀"):
                if email == "admin@gmail.com" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.current_user = "admin"
                    st.rerun()
                elif email == "staff@gmail.com" and password == "123":
                    st.session_state.logged_in = True
                    st.session_state.current_user = "staff"
                    st.rerun()
                else:
                    st.error("زانیارییەکان هەڵەن!")
    else:
        # کاتێک دێتە ناوەوە
        if st.session_state.current_user == "admin":
            st.markdown("<h1 style='color:#D4AF37;'>🛡️ مەکۆی بەڕێوەبردنی سەرەکی (Admin Panel)</h1>", unsafe_allow_html=True)
            
            tab_ads, tab_prods, tab_analytics = st.tabs(["📢 بەڕێوەبردنی ڕیکلامەکان", "📦 زیادکردنی بەرهەم", "📊 ئاماری سەردانیکەران"])
            
            # بەشی یەکەم: ڕیکلامەکان (کۆنتڕۆڵی مێژوو و ئەپرووڤ)
            with tab_ads:
                st.subheader("داواکارییە نوێیەکانی ڕیکلام")
                cursor.execute("SELECT id, client_name, client_phone, ad_text, ad_link, duration_months, status FROM ads WHERE status = 'Pending'")
                pending_ads = cursor.fetchall()
                
                if not pending_ads:
                    st.info("هیچ داواکارییەکی نوێی ڕیکلام نییە لە ئێستادا.")
                else:
                    for ad in pending_ads:
                        st.write(f"**لە لایەن:** {ad[1]} ({ad[2]}) - بۆ ماوەی **{ad[5]} مانگ**")
                        st.info(f"دەق: {ad[3]}")
                        col_ap1, col_ap2 = st.columns(2)
                        with col_ap1:
                            if st.button("✅ پەسەندکردن", key=f"app_{ad[0]}"):
                                start = datetime.date.today()
                                end = start + datetime.timedelta(days=ad[5]*30)
                                cursor.execute("""
                                    UPDATE ads SET status = 'Approved', start_date = ?, end_date = ? WHERE id = ?
                                """, (start.isoformat(), end.isoformat(), ad[0]))
                                conn.commit()
                                st.success("ڕیکلامەکە چالاک کرا!")
                                st.rerun()
                        with col_ap2:
                            if st.button("❌ ڕەتکردنەوە", key=f"rej_{ad[0]}"):
                                cursor.execute("DELETE FROM ads WHERE id = ?", (ad[0],))
                                conn.commit()
                                st.rerun()
                                
                st.write("---")
                st.subheader("🟢 ڕیکلامە چالاکەکان")
                cursor.execute("SELECT id, client_name, ad_text, start_date, end_date FROM ads WHERE status = 'Approved'")
                approved_ads = cursor.fetchall()
                for ad in approved_ads:
                    st.success(f"👤 {ad[1]} | {ad[2]} | ماوە: {ad[3]} بۆ {ad[4]}")
            
            # بەشی دووەم: زیادکردنی بەرهەم بۆ هەر پیشەیەک بێت!
            with tab_prods:
                st.subheader("📦 لێرەوە هەر کەسێک بێت دەتوانێت بەرهەم زیاد بکات:")
                p_name = st.text_input("ناوی بەرهەم / خزمەتگوزاری:")
                p_price = st.number_input("نرخ (دینار):", min_value=0, step=1000)
                p_desc = st.text_area("وەسفی کورت:")
                p_img = st.text_input("بەستەری وێنەی بەرهەم (لینک):", "https://images.unsplash.com/photo-1527799863-17b075e32712")
                p_biz = st.selectbox("بۆ کام بزنس و پیشە بنێردرێت؟", ["💇‍♂️ Barber & Salon", "📚 Education & Academy", "🛒 General Market", "💊 Pharmacy & Healthcare"])
                
                if st.button("تۆمارکردنی بەرهەم لە داتابەیس 💾"):
                    if p_name:
                        cursor.execute("""
                            INSERT INTO products (name, price, description, img_url, business_type)
                            VALUES (?, ?, ?, ?, ?)
                        """, (p_name, p_price, p_desc, p_img, p_biz))
                        conn.commit()
                        st.success("بەرهەمەکە بە سەرکەوتوویی تۆمارکرا و یەکسەر کەوتە بەشی مارکێت! 🎉")
                    else:
                        st.error("تکایە ناوی بەرهەمەکە بنووسە!")
            
            # بەشی سێیەم: ئاماری سەردانیکەران
            with tab_analytics:
                st.subheader("📈 چاودێری ڕێژەی بینینی وێبسایتەکەت")
                cursor.execute("SELECT view_date, view_count FROM page_views ORDER BY view_date DESC LIMIT 7")
                views_data = cursor.fetchall()
                if views_data:
                    df = pd.DataFrame(views_data, columns=["Date", "Views"])
                    st.line_chart(df.set_index("Date"))
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("هیچ داتایەکی سەردانیکردن نییە لە ئێستادا.")
