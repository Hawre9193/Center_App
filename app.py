import streamlit as st
import datetime
import pandas as pd

# 1. ڕێکخستنی سەرەتایی لاپەڕەکە
st.set_page_config(
    page_title="سەنتەری شاهانە | Multi-Business VIP",
    page_icon="👑",
    layout="wide"
)

# 2. فەرهەنگی گەورەی زمانەکان (کوردی، ئینگلیزی، عەرەبی، تورکی، فارسی)
LANG_DICT = {
    "Kurdish": {
        "title": "👑 سەنتەری شاهانە",
        "subtitle": "پلاتفۆرمی جیهانی بۆ بەڕێوەبردنی سەرجەم بزنسەکان",
        "home": "🏠 لاپەڕەی سەرەکی",
        "shop": "🛍️ مارکێتی شاهانە",
        "login_btn": "🔑 دەروازەی چوونەژوورەوە",
        "username": "📧 ئیمەیڵ:",
        "password": "🔑 پاسوۆرد:",
        "login_confirm": "پەیوەستبوون 🚀",
        "logout": "چوونەدەرەوە 🚪",
        "business_type": "🏢 جۆری کارەکەت هەڵبژێرە:",
        "client_name": "ناوی کڕیار / خوێندکار / نەخۆش:",
        "provider": "پێشکەشکار (دەلاک / مامۆستا / دەرمانساز):",
        "service": "خزمەتگوزاری / وانە / دەرمان:",
        "price": "نرخ (دینار):",
        "save": "جێگیرکردن و پاشەکەوتکردن 💾",
        "admin_panel": "🛡️ مەکۆی بەڕێوەبردنی گشتی",
        "staff_panel": "💼 پانێڵی کارمەندان",
        "dashboard": "📊 دۆخی گشتی",
        "finances": "💰 حیساباتی قازانج",
        "revenue": "💰 کۆی گشتی پارەی هاتوو",
        "records": "📋 خشتەی نۆرە و کارەکان",
        "ad_banner": "📢 ڕیکلامی سپۆنسەر: باشترین ئامێرەکانی تاشین و کەرەستەی خوێندن گەیشت!",
        "quick_order": "🛒 داواکردنی خێرا",
        "choose_lang": "🌐 زمان هەڵبژێرە / Choose Language"
    },
    "English": {
        "title": "👑 Royal Center",
        "subtitle": "Global platform to manage all your businesses",
        "home": "🏠 Home",
        "shop": "🛍️ VIP Shop",
        "login_btn": "🔑 Staff Login",
        "username": "📧 Email:",
        "password": "🔑 Password:",
        "login_confirm": "Connect 🚀",
        "logout": "Logout 🚪",
        "business_type": "🏢 Select Business Type:",
        "client_name": "Name (Client / Student / Patient):",
        "provider": "Provider (Barber / Teacher / Pharmacist):",
        "service": "Service / Lesson / Medicine:",
        "price": "Price (IQD):",
        "save": "Save Record 💾",
        "admin_panel": "🛡️ Admin Control Panel",
        "staff_panel": "💼 Staff Dashboard",
        "dashboard": "📊 Dashboard",
        "finances": "💰 Profit Analytics",
        "revenue": "💰 Total Revenue",
        "records": "📋 Records Table",
        "ad_banner": "📢 Sponsor Ad: Premium barber tools and educational kits have arrived!",
        "quick_order": "🛒 Quick Order",
        "choose_lang": "🌐 Choose Language"
    },
    "Arabic": {
        "title": "👑 المركز الملكي",
        "subtitle": "المنصة العالمية لإدارة جميع أعمالك التجارية",
        "home": "🏠 الصفحة الرئيسية",
        "shop": "🛍️ السوق الملكي",
        "login_btn": "🔑 بوابة تسجيل الدخول",
        "username": "📧 البريد الإلكتروني:",
        "password": "🔑 كلمة المرور:",
        "login_confirm": "تسجيل الدخول 🚀",
        "logout": "تسجيل الخروج 🚪",
        "business_type": "🏢 اختر نوع العمل:",
        "client_name": "اسم العميل / الطالب / المريض:",
        "provider": "مقدم الخدمة (حلاق / معلم / صيدلي):",
        "service": "الخدمة / الدرس / الدواء:",
        "price": "السعر (دينار):",
        "save": "حفظ وتسجيل 💾",
        "admin_panel": "🛡️ لوحة التحكم العامة",
        "staff_panel": "💼 لوحة الموظفين",
        "dashboard": "📊 الإحصائيات العامة",
        "finances": "💰 حسابات الأرباح",
        "revenue": "💰 إجمالي الإيرادات",
        "records": "📋 جدول السجلات",
        "ad_banner": "📢 إعلان الممول: وصلت أفضل أدوات الحلاقة والمستلزمات التعليمية!",
        "quick_order": "🛒 طلب سريع",
        "choose_lang": "🌐 اختر اللغة"
    },
    "Turkish": {
        "title": "👑 Kraliyet Merkezi",
        "subtitle": "Tüm işletmelerinizi yönetmek için küresel platform",
        "home": "🏠 Anasayfa",
        "shop": "🛍️ VIP Mağaza",
        "login_btn": "🔑 Personel Girişi",
        "username": "📧 E-posta:",
        "password": "🔑 Şifre:",
        "login_confirm": "Bağlan 🚀",
        "logout": "Çıkış Yap 🚪",
        "business_type": "🏢 İşletme Türünü Seçin:",
        "client_name": "Adı (Müşteri / Öğrenci / Hasta):",
        "provider": "Sağlayıcı (Berber / Öğretmen / Eczacı):",
        "service": "Hizmet / Ders / İlaç:",
        "price": "Fiyat (IQD):",
        "save": "Kaydet 💾",
        "admin_panel": "🛡️ Yönetici Paneli",
        "staff_panel": "💼 Personel Paneli",
        "dashboard": "📊 Gösterge Paneli",
        "finances": "💰 Kâr Analizi",
        "revenue": "💰 Toplam Gelir",
        "records": "📋 Kayıtlar Tablosu",
        "ad_banner": "📢 Sponsor Reklamı: En iyi berber aletleri ve eğitim kitleri geldi!",
        "quick_order": "🛒 Hızlı Sipariş",
        "choose_lang": "🌐 Dil Seçin"
    },
    "Persian": {
        "title": "👑 مرکز سلطنتی",
        "subtitle": "پلتفرم جهانی برای مدیریت تمام کسب‌وکارهای شما",
        "home": "🏠 صفحه اصلی",
        "shop": "🛍️ فروشگاه سلطنتی",
        "login_btn": "🔑 ورود پرسنل",
        "username": "📧 ایمیل:",
        "password": "🔑 رمز عبور:",
        "login_confirm": "ورود 🚀",
        "logout": "خروج 🚪",
        "business_type": "🏢 نوع کسب‌وکار را انتخاب کنید:",
        "client_name": "نام (مشتری / دانش‌آموز / بیمار):",
        "provider": "ارائه‌دهنده (آرایشگر / معلم / داروساز):",
        "service": "خدمات / درس / دارو:",
        "price": "قیمت (دینار):",
        "save": "ذخیره اطلاعات 💾",
        "admin_panel": "🛡️ پنل مدیریت کل",
        "staff_panel": "💼 پنل کارکنان",
        "dashboard": "📊 آمار کلی",
        "finances": "💰 حسابرسی سود",
        "revenue": "💰 کل درآمد",
        "records": "📋 جدول ثبت اطلاعات",
        "ad_banner": "📢 تبلیغ اسپانسر: بهترین وسایل آرایشگری و پک‌های آموزشی رسید!",
        "quick_order": "🛒 سفارش سریع",
        "choose_lang": "🌐 انتخاب زبان"
    }
}

# 3. لێدانی دەرزی جادوویی CSS بۆ دیزاینە مۆدێرنە تاریکەکەی Zedflix
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
        font-size: 16px;
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
    }
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="number-input"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }
    button[data-baseweb="tab"] {
        color: #888 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #D4AF37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. باری مێشکی کاتیی سیستم (Session State)
if "lang" not in st.session_state:
    st.session_state.lang = "Kurdish"

if "business_type" not in st.session_state:
    st.session_state.business_type = "💇‍♂️ Barber & Salon"

if "orders" not in st.session_state:
    st.session_state.orders = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# کورتەکردنەوەی زمان بۆ بەکارهێنان
T = LANG_DICT[st.session_state.lang]

# ==========================================
# 🍔 مینیۆی سێ هێڵەی لای چەپ (Sidebar Menu)
# ==========================================
st.sidebar.markdown(f"<h1 style='color:#D4AF37; text-align:center;'>👑 Royal Core</h1>", unsafe_allow_html=True)

# ١. گۆڕینی زمان لە مینیۆکەدا
st.sidebar.subheader(T["choose_lang"])
st.session_state.lang = st.sidebar.selectbox(
    "", 
    options=["Kurdish", "English", "Arabic", "Turkish", "Persian"],
    index=["Kurdish", "English", "Arabic", "Turkish", "Persian"].index(st.session_state.lang)
)

# ٢. گۆڕینی جۆری بزنسەکە (Multi-Business Selector)
st.sidebar.subheader(T["business_type"])
st.session_state.business_type = st.sidebar.selectbox(
    "",
    options=[
        "💇‍♂️ Barber & Salon", 
        "📚 Education & Academy", 
        "🛒 General Market", 
        "💊 Pharmacy & Healthcare"
    ]
)

st.sidebar.write("---")

# مینیۆی بەشەکان
menu_option = st.sidebar.radio(
    "🧭 Navigation",
    options=[T["home"], T["shop"], T["login_btn"]]
)

st.sidebar.write("---")

# ئەگەر بەکارهێنەر لۆگین بوبێت دوگمەی چوونەدەرەوە لێرە دەردەکەوێت
if st.session_state.logged_in:
    st.sidebar.write(f"Logged in: {st.session_state.current_user}")
    if st.sidebar.button(T["logout"], use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

# ==========================================
# 🏠 بەشی یەکەم: لاپەڕەی سەرەکی (Home)
# ==========================================
if menu_option == T["home"]:
    st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>{T['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #8892b0;'>{T['subtitle']}</p>", unsafe_allow_html=True)
    st.write("")
    
    # 📢 بانەری ڕیکلام و سپۆنسەری شاهانە
    st.markdown(f"""
        <div class="ad-banner">
            {T['ad_banner']}
        </div>
    """, unsafe_allow_html=True)
    
    # ناساندنی مۆڵتی-بزنسی چالاک لە لاپەڕەی سەرەکیدا
    st.markdown(f"<h3>🏢 Active Workspace: <span style='color:#D4AF37;'>{st.session_state.business_type}</span></h3>", unsafe_allow_html=True)
    st.write("سیستمەکە لە ئێستادا بە تەواوی ئامادەکراوە بۆ ئەم جۆرە بازرگانییە بە زمانی هەڵبژێردراو.")
    
    # دەرکەوتنی بەشەکان بە شێوازی مۆدێرن
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        st.markdown(f"""
            <div class="product-box">
                <h3 style='color:#D4AF37;'>💡 Dynamic Interface</h3>
                <p>تەواوی ناوی خانەکانی سیستمەکە بە شێوەیەکی خۆکار دەگۆڕێن بۆ ئەوەی لەگەڵ بزنسەکەتدا بگونجێن.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_inf2:
        st.markdown(f"""
            <div class="product-box">
                <h3 style='color:#D4AF37;'>🌍 Translation Engine</h3>
                <p>بە بەکارهێنانی سیستمی پێشکەوتووی زمانەوانیمان، دەتوانیت هەمیشە کارەکان بە ٥ زمان بەڕێوەبەریت.</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 🛍️ بەشی دووەم: مارکێتی شاهانە (VIP Shop)
# ==========================================
elif menu_option == T["shop"]:
    st.markdown(f"<h1 style='color: #D4AF37;'>{T['shop']}</h1>", unsafe_allow_html=True)
    st.write("باشترین کەرەستە و کاڵاکانی پێوەست بە کارەکەت:")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    # کاڵاکان دەگۆڕێن بەپێی جۆری بزنسەکە بۆ ئەوەی سیستمەکە زیرەک بێت!
    if "Barber" in st.session_state.business_type:
        p1, p2, p3 = "🧴 Max Hair Gel", "🪒 Wireless Clipper", "✂️ Japanese Scissors"
        p1_sub, p2_sub, p3_sub = "24h Hold", "Premium Battery 2026", "Stainless steel"
        p1_price, p2_price, p3_price = "6,000 د.ع", "45,000 د.ع", "25,000 د.ع"
    elif "Education" in st.session_state.business_type:
        p1, p2, p3 = "📚 English Grammar Book", "🎧 Translation Headphones", "📝 VIP Notebook"
        p1_sub, p2_sub, p3_sub = "Level 1 & 2 Coursebook", "High quality voice", "Luxury leather cover"
        p1_price, p2_price, p3_price = "15,000 د.ع", "35,000 د.ع", "8,000 د.ع"
    elif "Pharmacy" in st.session_state.business_type:
        p1, p2, p3 = "🧴 Royal Skin Cream", "🌡️ Digital Thermometer", "🩹 First Aid Kit"
        p1_sub, p2_sub, p3_sub = "Organic 100%", "Accurate & fast reading", "Fully equipped VIP"
        p1_price, p2_price, p3_price = "18,000 د.ع", "12,000 د.ع", "20,000 د.ع"
    else: # General Market
        p1, p2, p3 = "📦 VIP Box Pack", "🛍️ Eco Friendly Bag", "🏷️ Custom Price Labeler"
        p1_sub, p2_sub, p3_sub = "100 Pcs pack", "Reusable material", "Wireless Bluetooth"
        p1_price, p2_price, p3_price = "10,000 د.ع", "2,000 د.ع", "30,000 د.ع"

    with col_p1:
        st.markdown(f'<div class="product-box"><h3>{p1}</h3><p>{p1_sub}</p><h4>{p1_price}</h4></div>', unsafe_allow_html=True)
        st.write("")
        if st.button(T["quick_order"], key="btn_p1"):
            st.toast("بۆ داواکردن، پەیوەندی بکە بە: 0750XXXXXXX", icon="📞")
    with col_p2:
        st.markdown(f'<div class="product-box"><h3>{p2}</h3><p>{p2_sub}</p><h4>{p2_price}</h4></div>', unsafe_allow_html=True)
        st.write("")
        if st.button(T["quick_order"], key="btn_p2"):
            st.toast("بۆ داواکردن، پەیوەندی بکە بە: 0750XXXXXXX", icon="📞")
    with col_p3:
        st.markdown(f'<div class="product-box"><h3>{p3}</h3><p>{p3_sub}</p><h4>{p3_price}</h4></div>', unsafe_allow_html=True)
        st.write("")
        if st.button(T["quick_order"], key="btn_p3"):
            st.toast("بۆ داواکردن، پەیوەندی بکە بە: 0750XXXXXXX", icon="📞")

# ==========================================
# 🔑 بەشی سێیەم: دەروازەی چوونەژوورەوە و کارەکان
# ==========================================
elif menu_option == T["login_btn"]:
    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            st.markdown(f"""
                <div class="main-card" style="text-align: center;">
                    <h1 style="color: #D4AF37; margin:0;">👑</h1>
                    <h2>{T['login_btn']}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input(T["username"]).strip().lower()
            password = st.text_input(T["password"], type="password").strip()
            
            st.write("")
            if st.button(T["login_confirm"]):
                # لێرەدا فلتەری لۆگینێکی خێرا بۆ تاقیکردنەوە دەکەین
                if email == "admin@gmail.com" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.current_user = "admin"
                    st.rerun()
                elif email == "staff@gmail.com" and password == "123":
                    st.session_state.logged_in = True
                    st.session_state.current_user = "staff"
                    st.rerun()
                else:
                    st.error("❌ Email or Password incorrect!")
    else:
        # دوای لۆگینبوون لێرەدا پانێڵی بەڕێوەبردن یان کارمەند دێتەوە
        st.markdown(f"<h1 class='neon-title'>{T['admin_panel'] if st.session_state.current_user == 'admin' else T['staff_panel']}</h1>", unsafe_allow_html=True)
        st.write("---")
        
        tab1, tab2 = st.tabs([T["dashboard"], T["finances"]])
        
        with tab1:
            st.subheader(T["records"])
            
            # دروستکردنی فۆرمی تۆمارکردن کە بەپێی جۆری بزنسەکە گۆڕاوە!
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                client = st.text_input(T["client_name"])
                srv = st.text_input(T["service"])
            with col_f2:
                prov = st.text_input(T["provider"])
                prc = st.number_input(T["price"], min_value=0, step=1000)
                
            if st.button(T["save"]):
                if client and srv:
                    st.session_state.orders.append({
                        "Time": datetime.datetime.now().strftime("%I:%M %p"),
                        "Client": client,
                        "Provider": prov,
                        "Service": srv,
                        "Price": prc,
                        "Business": st.session_state.business_type
                    })
                    st.success("Saved successfully! ✅")
                    st.rerun()
            
            st.write("---")
            # تەنها کارەکانی ئەو بزنسە چالاکە نیشان دەدات کە ئێستا هەڵبژێردراوە
            filtered_orders = [o for o in st.session_state.orders if o["Business"] == st.session_state.business_type]
            if filtered_orders:
                st.dataframe(pd.DataFrame(filtered_orders), use_container_width=True)
            else:
                st.info("No records for this business type yet.")
                
        with tab2:
            st.subheader(T["finances"])
            filtered_orders = [o for o in st.session_state.orders if o["Business"] == st.session_state.business_type]
            if filtered_orders:
                total = sum(o["Price"] for o in filtered_orders)
                st.metric(T["revenue"], f"{total:,} IQD")
                
                # لێرەدا دەتوانین ڕێژە و دابەشکاری قازانج بکەین بەپێی کارمەند
                st.write("---")
                percentage = st.slider("Percentage for Provider (%):", 0, 100, 50, 5)
                df_fin = pd.DataFrame(filtered_orders)
                df_fin["Provider Share"] = df_fin["Price"] * (percentage / 100)
                df_fin["Center Share"] = df_fin["Price"] * ((100 - percentage) / 100)
                st.dataframe(df_fin[["Time", "Client", "Provider", "Price", "Provider Share", "Center Share"]], use_container_width=True)
            else:
                st.info("No sales data available to calculate profits.")
