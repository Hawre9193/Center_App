import streamlit as st
import datetime
import pandas as pd

# ڕێکخستنی شێوازی پیشاندانی لاپەڕەکە بە شێوەی شاهانە
st.set_page_config(
    page_title="سیستمی شاهانەی بەڕێوەبردن",
    page_icon="👑",
    layout="wide"
)

# زانیارییە سەرەکییەکانی سەنتەرەکە
CENTER_NAME = "سەنتەری شاهانە"
PHONE = "07701234567"
INSTAGRAM = "@Nayab_Center"

# دڵنیابوونەوە لە بوونی داتاکان لە ناو مێشک (session_state)ی ئەپەکەدا
if "users" not in st.session_state:
    st.session_state.users = {
        "admin@gmail.com": {"password": "admin123", "name": "خاوەن کار (هاوڕێ)", "role": "admin", "expire": datetime.date(2027, 12, 31)},
        "barber1@gmail.com": {"password": "123", "name": "سەنتەری هاوڕێ", "role": "user", "expire": datetime.date(2026, 8, 16)},
        "barber2@gmail.com": {"password": "456", "name": "سەنتەری نازە", "role": "user", "expire": datetime.date(2026, 7, 20)}
    }

if "services" not in st.session_state:
    st.session_state.services = {
        "قژ تاشینی مۆدێرن": 15000,
        "تاشینی ڕیش و ڕێکخستن": 10000,
        "پاککردنەوەی پێست (فەیشەڵ)": 25000,
        "سێشوار و مۆدێل": 8000,
        "کۆمبۆی شاهانە (هەمووی)": 45000
    }

if "orders" not in st.session_state:
    st.session_state.orders = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# ----------------- (لاپەڕەی لۆگین - Login Page) -----------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>👑 سەنتەری شاهانە 👑</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #888;'>سیستمی پێشکەوتووی بەڕێوەبردنی بەشداری کڕیاران و سەنتەرەکان</h4>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("ئیمەیڵەکەت بنووسە:").strip().lower()
        password = st.text_input("پاسوۆردەکەت بنووسە:", type="password").strip()
        
        if st.button("چوونەژوورەوە 🔑", use_container_width=True):
            if email in st.session_state.users:
                user_data = st.session_state.users[email]
                if user_data["password"] == password:
                    today = datetime.date.today()
                    if today <= user_data["expire"]:
                        st.session_state.logged_in = True
                        st.session_state.current_user = email
                        st.success(f"بەخێربێیت بەڕێز {user_data['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ ماوەی اشتراکی مانگانەکەت بەسەرچووە! تکایە نوێی بکەرەوە.")
                else:
                    st.error("❌ پاسوۆردەکەت هەڵەیە!")
            else:
                st.error("❌ ئەم ئیمەیڵە تۆمار نەکراوە!")
        
        st.info(f"📞 بۆ کڕینی بەشداری مانگانە پەیوەندی بکە بە: {PHONE}")

else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # ----------------- مینیووی لای چەپ (Sidebar) -----------------
    st.sidebar.markdown(f"### 👑 {user_info['name']}")
    st.sidebar.write(f"**ڕۆڵ:** {user_info['role'].capitalize()}")
    st.sidebar.write(f"**بەسەرچوون:** {user_info['expire']}")
    
    if st.sidebar.button("چوونەدەرەوە 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
        
    st.sidebar.write("---")
    st.sidebar.write(f"📍 {CENTER_NAME}")
    st.sidebar.write(f"📸 Instagram: {INSTAGRAM}")

    # =========================================================================
    # 1. پانێڵی بەڕێوەبەر (Admin View)
    # =========================================================================
    if user_info["role"] == "admin":
        st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🛡️ پانێڵی سەرەکی خاوەن کار (Admin)</h1>", unsafe_allow_html=True)
        st.write("---")
        
        # دروستکردنی تابەکان بۆ ڕێکخستنی گەورەی سایتەکە
        tab_dashboard, tab_users, tab_services, tab_finances = st.tabs([
            "📈 داشبۆرد و ڕاپۆرتەکان", 
            "👥 بەڕێوەبردنی بەشداربووان", 
            "✂️ خزمەتگوزارییەکان", 
            "💸 حیسابات و خەرجییەکان"
        ])
        
        # --- TAB 1: DASHBOARD ---
        with tab_dashboard:
            st.subheader("📊 کورتەی دۆخی دارایی و کارەکان")
            
            # حیسابکردنی ئامارەکان
            total_sales = sum(o["price"] for o in st.session_state.orders)
            total_expenses = sum(e["amount"] for e in st.session_state.expenses)
            net_profit = total_sales - total_expenses
            total_customers = len(st.session_state.orders)
            
            # پیشاندانی کارتە سەرنجڕاکێشەکان
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            col_s1.metric("💰 کۆی گشتی داهات", f"{total_sales:,} دینار")
            col_s2.metric("📉 کۆی خەرجییەکان", f"{total_expenses:,} دینار", delta_color="inverse")
            col_s3.metric("💎 قازانجی پاک", f"{net_profit:,} دینار")
            col_s4.metric("👥 ژمارەی کڕیارەکان", f"{total_customers} کڕیار")
            
            st.write("---")
            st.subheader("📈 هێڵکاری فرۆشتنی سەرتاشەکان")
            
            if st.session_state.orders:
                df_orders = pd.DataFrame(st.session_state.orders)
                # دروستکردنی چارتی فرۆشتن بەپێی سەرتاش
                df_barber_sales = df_orders.groupby("barber")["price"].sum().reset_index()
                st.bar_chart(df_barber_sales.set_index("barber"))
                
                st.subheader("📋 لیستی نۆرەکانی ئەمڕۆ لە سەرانسەری سەنتەرەکان")
                st.dataframe(df_orders[["time", "customer_name", "barber", "service", "price"]], use_container_width=True)
            else:
                st.info("هیچ نۆرەیەک بۆ ئەمڕۆ تۆمار نەکراوە.")
                
        # --- TAB 2: MANAGE USERS ---
        with tab_users:
            st.subheader("👥 لیستی بەشداربووانی چالاک")
            for u_email, u_data in st.session_state.users.items():
                if u_data["role"] != "admin":
                    st.write(f"🔹 **{u_data['name']}** ({u_email}) - چالاکە تا: {u_data['expire']}")
            
            st.write("---")
            st.subheader("➕ زیادکردن یان نوێکردنەوەی بەشداربوو")
            
            new_email = st.text_input("ئیمەیڵی کڕیار/سەرتاش:").strip().lower()
            new_name = st.text_input("ناوی سەنتەر/کارمەند:")
            new_pass = st.text_input("پاسوۆردی کاتی:", type="password")
            days = st.number_input("چەند ڕۆژی بۆ دابنێیت؟", min_value=1, value=30)
            
            if st.button("تۆمارکردن و چالاککردن ✅", use_container_width=True):
                if new_email and new_name and new_pass:
                    expire_date = datetime.date.today() + datetime.timedelta(days=days)
                    st.session_state.users[new_email] = {
                        "password": new_pass,
                        "name": new_name,
                        "role": "user",
                        "expire": expire_date
                    }
                    st.success(f"🎉 سەنتەری '{new_name}' بە سەرکەوتوویی تۆمارکرا یان نوێکرایەوە تا: {expire_date}")
                    st.rerun()
                else:
                    st.warning("تکایە هەموو خانەکان پڕ بکەرەوە!")

        # --- TAB 3: MANAGE SERVICES ---
        with tab_users:
            pass # (ڕێگریکردن لە دووبارەبوونەوە)
            
        with tab_services:
            st.subheader("✂️ بەڕێوەبردنی خزمەتگوزارییەکان و نرخەکان")
            
            # پیشاندانی خزمەتگوزارییەکان
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown("### 📋 لیست و نرخی ئێستا:")
                for ser, price in st.session_state.services.items():
                    st.write(f"• **{ser}**: {price:,} دینار")
                    
            with col_r:
                st.markdown("### ➕ زیادکردنی خزمەتگوزاری نوێ:")
                new_ser_name = st.text_input("ناوی خزمەتگوزاری نوێ:")
                new_ser_price = st.number_input("نرخی کارەکە (دینار):", min_value=500, step=500, value=10000)
                
                if st.button("تۆمارکردنی خزمەتگوزاری 💾", use_container_width=True):
                    if new_ser_name:
                        st.session_state.services[new_ser_name] = new_ser_price
                        st.success(f"خزمەتگوزاری '{new_ser_name}' بە نرخی {new_ser_price:,} دینار زیادکرا!")
                        st.rerun()

        # --- TAB 4: FINANCES & EXPENSES ---
        with tab_finances:
            st.subheader("💸 تۆمارکردنی خەرجییەکانی سەنتەر")
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                exp_title = st.text_input("بابەتی خەرجی (بۆ نموونە: کرێ، مەواد، کارەبا):")
                exp_amount = st.number_input("بڕی پارەی خەرجکراو (دینار):", min_value=500, step=500, value=5000)
                if st.button("تۆمارکردنی خەرجی ➖", use_container_width=True):
                    if exp_title:
                        st.session_state.expenses.append({
                            "title": exp_title,
                            "amount": exp_amount,
                            "date": datetime.date.today().strftime("%Y-%m-%d")
                        })
                        st.success("خەرجییەکە بە سەرکەوتوویی تۆمارکرا!")
                        st.rerun()
            
            with col_f2:
                st.markdown("### 📊 لیستی خەرجییەکانی ئەمڕۆ:")
                if st.session_state.expenses:
                    df_exp = pd.DataFrame(st.session_state.expenses)
                    st.dataframe(df_exp, use_container_width=True)
                else:
                    st.info("هیچ خەرجییەک تۆمار نەکراوە.")

    # =========================================================================
    # 2. پانێڵی بەکارهێنەر/سەرتاش (User/Barber View)
    # =========================================================================
    else:
        st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>💇‍♂️ بەخێربێیت بۆ پانێڵی {user_info['name']}</h1>", unsafe_allow_html=True)
        st.write("---")
        
        tab_order, tab_today = st.tabs(["📝 تۆمارکردنی نۆرە", "📊 داتاکانی ئەمڕۆ"])
        
        # --- TAB 1: ADD ORDER ---
        with tab_order:
            st.subheader("👤 زانیاری کڕیار تۆمار بکە:")
            
            cust_name = st.text_input("ناوی کڕیار:")
            gender = st.selectbox("ڕەگەز:", ["کوڕ", "کچ"])
            
            # کێشانی خزمەتگوزارییەکان لە لیستەکەوە
            service_list = list(st.session_state.services.keys())
            selected_service = st.selectbox("خزمەتگوزاری:", service_list)
            
            # پیشاندانی نرخ بە شێوەی خۆکار بەپێی خزمەتگوزارییەکە
            price = st.session_state.services[selected_service]
            st.info(f"💵 نرخی ئەم کارە: {price:,} دینار")
            
            # سیستمی ڕێژەی سەرتاش (Commission)
            commission_pct = st.slider("٪ ڕێژەی قازانجی سەرتاش لەم کارەدا:", min_value=0, max_value=100, value=50)
            barber_profit = (price * commission_pct) / 100
            st.write(f"💰 قازانجی سەرتاش: **{barber_profit:,} دینار** | پشکی سەنتەر: **{price - barber_profit:,} دینار**")
            
            if st.button("➕ تۆمارکردنی نۆرە", use_container_width=True):
                if cust_name:
                    now_time = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.orders.append({
                        "time": now_time,
                        "customer_name": cust_name,
                        "gender": gender,
                        "service": selected_service,
                        "price": price,
                        "barber": user_info["name"],
                        "barber_profit": barber_profit
                    })
                    st.success(f"🎉 نۆرەی ژمارە {len(st.session_state.orders)} بۆ کڕیار {cust_name} بە سەرکەوتوویی تۆمارکرا!")
                    st.rerun()
                else:
                    st.warning("تکایە ناوی کڕیار بنووسە!")
                    
        # --- TAB 2: TODAY'S DATA ---
        with tab_today:
            # پاڵاوتنی تەنها ئەو نۆرانەی هی ئەم سەرتاشە خۆیەتی
            my_orders = [o for o in st.session_state.orders if o["barber"] == user_info["name"]]
            
            if my_orders:
                my_total_sales = sum(o["price"] for o in my_orders)
                my_total_profit = sum(o["barber_profit"] for o in my_orders)
                
                col_b1, col_b2, col_b3 = st.columns(3)
                col_b1.metric("💰 کۆی گشتی کارەکانت", f"{my_total_sales:,} دینار")
                col_b2.metric("💸 پشکی قازانجی تۆ", f"{my_total_profit:,} دینار")
                col_b3.metric("👥 ژمارەی کڕیارەکانت", f"{len(my_orders)} کڕیار")
                
                st.write("---")
                st.subheader("📋 نۆرەکانی تۆ لەمڕۆدا:")
                df_my_orders = pd.DataFrame(my_orders)
                st.dataframe(df_my_orders[["time", "customer_name", "gender", "service", "price", "barber_profit"]], use_container_width=True)
            else:
                st.info("تۆ هێشتا هیچ نۆرەیەکت بۆ ئەمڕۆ تۆمار نەکردووە.")
