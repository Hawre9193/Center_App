import streamlit as st
import sqlite3
import datetime
import pandas as pd
import time
from config import LANG_DICT
from database import conn, cursor

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

def render_merchant_panel(T):
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
        
        if "Barber" in b_type:
            st.write("داهاتی کۆی دەلاکەکان و کۆمسیۆنی پلاتفۆڕم بەپێی نۆرە پشتڕاستکراوەکان:")
            cursor.execute("SELECT COUNT(id) FROM bookings WHERE merchant_id = ? AND status = 'Confirmed'", (st.session_state.user_id,))
            confirmed_count = cursor.fetchone()[0] or 0
            total_revenue = confirmed_count * 10000
        elif "Education" in b_type:
            st.write("داهاتی پەیمانگا بەپێی خوێندکارە چالاکەکان:")
            cursor.execute("SELECT COUNT(id) FROM bookings WHERE merchant_id = ? AND status = 'Active Student'", (st.session_state.user_id,))
            confirmed_count = cursor.fetchone()[0] or 0
            total_revenue = confirmed_count * 150000
        else:
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
