import streamlit as st

def inject_royal_styles():
    """
    ئەم ف ikشنە دیزاینی تاریکی زێڕینی شاهانەی CSS دەخاتە ناو لاپەڕەکەوە.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;700&display=swap');
        
        * {
            font-family: 'Noto Sans Arabic', sans-serif !important;
        }
        .stApp {
            background: radial-gradient(circle, #0e0f14 0%, #050508 100%) !important;
            color: #e2e8f0 !important;
        }
        /* لێرەوە چاکسازی گشتگیر بۆ ڕاست-بۆ-چەپ و زۆرکردنی مۆدی تاریک کراوە */
        :root {
            --primary-color: #d4af37 !important;
            --background-color: #050508 !important;
            --secondary-background-color: #07080c !important;
            --text-color: #e2e8f0 !important;
        }
        .stApp, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"], [data-testid="stAppViewContainer"] {
            direction: rtl !important;
            text-align: right !important;
            background-color: #050508 !important;
        }
        /* دوورخستنەوەی نووسینەکان لە بازنە ڕەنگاوڕەنگەکان لە مێنوودا */
        [data-testid="stWidgetLabel"] p, .stRadio label {
            text-align: right !important;
            padding-right: 10px !important;
        }
        /* شاردنەوەی ئەو نووسینە تێکچووەی سەرەوەی مێنوو و هێشتنەوەی ئایکۆنەکە */
        [data-testid="stSidebarCollapsedControl"] button span {
            display: none !important;
        }
        [data-testid="stSidebarCollapsedControl"] button::before {
            content: "☰" !important;
            color: #d4af37 !important;
            font-size: 24px !important;
            padding: 5px !important;
        }
        /* کۆتایی چاکسازی مێنوو */
        .royal-header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #161822 0%, #0b0c10 100%);
            border: 2px solid rgba(212, 175, 55, 0.35);
            border-radius: 20px;
            margin-bottom: 25px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.8);
        }
        .ad-banner {
            background: linear-gradient(90deg, #aa7c11 0%, #d4af37 50%, #aa7c11 100%) !important;
            color: #000000 !important;
            padding: 18px !important;
            border-radius: 12px !important;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.5);
            margin-bottom: 30px;
            font-size: 18px;
        }
        .main-card {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
            border-radius: 15px !important;
            padding: 22px !important;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .product-box {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(212, 175, 55, 0.12) !important;
            border-radius: 15px !important;
            padding: 18px !important;
            text-align: center;
            transition: all 0.3s ease;
        }
        .product-box:hover {
            border-color: #d4af37 !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.35);
            transform: translateY(-5px);
        }
        .stButton>button {
            background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
            color: #000 !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 10px !important;
            transition: all 0.25s ease-in-out;
        }
        .stButton>button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.5);
        }
        .error-box-custom {
            color: #ff4b4b;
            background-color: rgba(255, 75, 75, 0.1);
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #ff4b4b;
            margin-top: 5px;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)
