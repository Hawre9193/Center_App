import streamlit as st
import sqlite3
import datetime
import pandas as pd
import time
from config import LANG_DICT
from styles import inject_royal_styles  # هاوردەکردنی فایلی دیزاینەکان
from database import conn, cursor  # هاوردەکردنی داتابەیس و کێرسەر لە فایلی جیاوازەوە
from panels import render_super_admin_panel, render_merchant_panel  # هاوردەکردنی پانێڵەکان لێرەوە
from views import render_home_page, render_shop_page, render_ad_portal  # هاوردەکردنی لاپەڕەکانی بەکارهێنەر لێرەوە

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
    render_home_page(T, biz_type)

# ========================================================
# 🛍️ بەشی بازار و کەرەستەکان (Shop View)
# ========================================================
elif menu_choice == T["shop"]:
    render_shop_page(T, biz_type)

# ========================================================
# 📢 داواکردنی ڕیکلام (Ad Portal)
# ========================================================
elif menu_choice == T["ad_portal"]:
    render_ad_portal(T)

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
                    st.error("تکایە سەرجەم کێشەکانی ناو خانە سوورەکان شارەسەر بکە پێش کڕیک کردن!")

    else:
        # ----------------------------------------------------
        # 👑 الف: پانێڵی دەسەڵاتی ڕەها (SUPER ADMIN PANEL)
        # ----------------------------------------------------
        if st.session_state.user_role == "super_admin":
            render_super_admin_panel(T)

        # ----------------------------------------------------
        # 🏢 ب: پانێڵی تایبەتی بازرگانەکان (MERCHANT DASHBOARD)
        # ----------------------------------------------------
        elif st.session_state.user_role == "merchant":
            render_merchant_panel(T)
