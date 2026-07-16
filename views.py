import streamlit as st
import datetime
import time
from database import conn, cursor

def render_home_page(T, biz_type):
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

def render_shop_page(T, biz_type):
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

    st.write("---")
    st.markdown("### 🛒 سەبەتەی کڕینی تۆ")
    if not st.session_state.cart:
        st.info("سەبەتەکەت لە ئێستادا بەتاڵە.")
    else:
        total_cart_price = 0
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

def render_ad_portal(T):
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
