import streamlit as st
import datetime

# ڕێکخستنی شێوازی پیشاندانی لاپەڕەکە
st.set_page_config(page_title="سیستەمی شاهانەی بەڕێوەبردن", page_icon="✂️", layout="centered")

# زانیارییە سەرەکییەکانی سەنتەرەکەت
ناونیشانی_سەنتەر = "سلێمانی - شەقامی سەرەکی"
مۆبایلی_سەنتەر = "07701234567"
ئینستاگرامی_سەنتەر = "@Nayab_Center"

# داتابەیسی کاتی بەکارهێنەران (ئەوانەی بۆیان هەیە بچنە ژوورەوە)
if "users" not in st.session_state:
    st.session_state.users = {
        "admin@gmail.com": {"password": "admin123", "name": "خاوەن کار (تۆ 👑)", "role": "admin", "expire": datetime.date(2030, 1, 1)},
        "barber1@gmail.com": {"password": "123", "name": "سەنتەری هاوڕێ", "role": "user", "expire": datetime.date(2026, 8, 16)},
        "barber2@gmail.com": {"password": "456", "name": "سەنتەری نازە", "role": "user", "expire": datetime.date(2026, 7, 20)}
    }

# لێرەدا نۆرەکان پاشەکەوت دەکەین لە ماوەی بەکارهێنانی وێبسایتەکەدا
if "orders" not in st.session_state:
    st.session_state.orders = []
if "total_revenue" not in st.session_state:
    st.session_state.total_revenue = 0
if "order_counter" not in st.session_state:
    st.session_state.order_counter = 1

# پاراستنی دۆخی چوونەژوورەوە
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# --- ١. لاپەڕەی لۆگین (Login Page) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>👑 سەنتەری شاهانە</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>سیستەمی بەڕێوەبردنی بەشداری کڕیاران و سەنتەرەکان</h4>", unsafe_allow_html=True)
    st.write("---")
    
    email = st.text_input("ئیمەیڵەکەت بنووسە:").strip().lower()
    password = st.text_input("پاسۆردەکەت بنووسە:", type="password").strip()
    
    if st.button("چوونەژوورەوە 🔑", use_container_width=True):
        if email in st.session_state.users:
            user_data = st.session_state.users[email]
            if user_data["password"] == password:
                # پشکنینی کاتی بەسەرچوون
                today = datetime.date.today()
                if today <= user_data["expire"]:
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.success(f"بەخێربێیت بەڕێز {user_data['name']}")
                    st.rerun()
                else:
                    st.error("❌ ماوەی اشتراکی مانگانەکەت بەسەرچووە! تکایە کرێی مانگانە بدە بۆ نوێکردنەوە.")
            else:
                st.error("❌ پاسۆردەکەت هەڵەیە!")
        else:
            st.error("❌ ئەم ئیمەیڵە تۆمار نەکراوە یان هێشتا چالاک نەکراوە.")
            
    st.info("📞 بۆ کڕینی بەشداری مانگانە (اشتراک) یان نوێکردنەوە، پەیوەندی بکە بە: 0770XXXXXXX")

# --- ٢. ناوەوەی سیستەمەکە پاش لۆگین ---
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # مینیۆی چەپ (Sidebar)
    st.sidebar.markdown(f"### 👤 {user_info['name']}")
    st.sidebar.write(f"🏷️ ڕۆڵ: {user_info['role'].capitalize()}")
    st.sidebar.write(f"📅 بەسەرچوون: {user_info['expire']}")
    
    if st.sidebar.button("چوونەدەرەوە 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
        
    # ئەگەر داخڵبووەکە خاوەن کار بێت (تۆ 👑) - پانێڵی ئەدمین دەبینێت
    if user_info["role"] == "admin":
        st.title("🛡️ پانێڵی سەرەکی خاوەن کار (Admin)")
        st.write("لێرەوە دەتوانیت کڕیارە نوێیەکان قبوڵ بکەیت و ماوەی اشتراکەکانیان دیاری بکەیت.")
        
        # پیشاندانی بەکارهێنەران و ماوەکانیان
        st.write("### 👥 لیستی بەشداربووان:")
        for mail, data in st.session_state.users.items():
            if data["role"] != "admin":
                st.write(f"🔹 **{data['name']}** ({mail}) - بەسەرچوون: {data['expire']}")
        
        st.write("---")
        st.write("### ➕ زیادکردن یان نوێکردنەوەی بەشداربوو (اشتراک)")
        new_email = st.text_input("ئیمەیڵی کڕیاری نوێ:").strip().lower()
        new_name = st.text_input("ناوی سەنتەری کڕیار:").strip()
        new_pass = st.text_input("پاسۆردی کاتی:", type="password").strip()
        days_to_add = st.number_input("چەند ڕۆژی بۆ دابنرێت؟ (بۆ نموونە ٣٠ ڕۆژ):", min_value=1, max_value=365, value=30)
        
        if st.button("تۆمارکردن و چالاککردن ✅"):
            if new_email and new_name and new_pass:
                expire_date = datetime.date.today() + datetime.timedelta(days=days_to_add)
                st.session_state.users[new_email] = {
                    "password": new_pass,
                    "name": new_name,
                    "role": "user",
                    "expire": expire_date
                }
                st.success(f"🎉 سەنتەری '{new_name}' بە سەرکەوتوویی تۆمارکرا! چالاکە تا: {expire_date}")
            else:
                st.warning("⚠️ تکایە هەموو خانەکان پڕ بکەرەوە!")

    # ئەگەر بەکارهێنەری ئاسایی بێت (ئەو سەنتەرانەی کرێیان داوە)
    else:
        st.title(f"💇‍♂️ سیستەمی بەڕێوەبردنی {user_info['name']}")
        st.write("بەخێربێیت! لێرەوە دەتوانیت نۆرەکان و داهاتی سەنتەرەکەت تۆمار بکەیت.")
        
        tab1, tab2 = st.tabs(["📝 تۆمارکردنی نۆرە", "📊 داتاکانی ئەمڕۆ"])
        
        with tab1:
            customer_name = st.text_input("ناوی کڕیار:")
            gender = st.selectbox("ڕەگەز:", ["کوڕ", "کچ"])
            service = st.selectbox("خزمەتگوزاری:", ["قژ تاشینی مۆدێرن", "قژ تاشینی کلاسیک", "ڕیش تاشین", "VIP"])
            price = st.number_input("نرخی کارەکە (دینار):", min_value=0, step=250)
            
            if st.button("تۆمارکردنی نۆرە ➕"):
                if customer_name:
                    new_order = {
                        "نۆرە": st.session_state.order_counter,
                        "ناو": customer_name,
                        "ڕەگەز": gender,
                        "خزمەت": service,
                        "نرخ": price,
                        "کاتی_تۆمارکردن": datetime.datetime.now().strftime("%I:%M %p")
                    }
                    st.session_state.orders.append(new_order)
                    st.session_state.total_revenue += price
                    st.session_state.order_counter += 1
                    st.success(f"🎉 نۆرەی ژمارە {new_order['نۆرە']} بۆ کڕیار {customer_name} تۆمارکرا!")
                else:
                    st.error("⚠️ تکایە ناوی کڕیار بنووسە!")
                    
        with tab2:
            st.write(f"### 💰 کۆی داهاتی ئەمڕۆ: {st.session_state.total_revenue:,} دینار")
            if st.session_state.orders:
                st.write("### 📋 نۆرەکانی ئەمڕۆ:")
                st.table(st.session_state.orders)
            else:
                st.info("📭 هیچ نۆرەیەک بۆ ئەمڕۆ تۆمار نەکراوە.")
