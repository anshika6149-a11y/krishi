import streamlit as st
import requests
import random

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform", 
    page_icon="🌾", 
    layout="centered"
)

# Premium Custom App Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .app-bar {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 22px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0px 10px 25px -5px rgba(37, 99, 235, 0.3);
    }
    .app-bar h1 {
        color: #FFFFFF !important;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .app-bar p {
        color: #93C5FD;
        margin-top: 6px;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .pass-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #22C55E;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0px 4px 15px rgba(34, 197, 94, 0.15);
    }
    .pass-card .badge {
        background: #16A34A;
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .pass-card h2 {
        color: #15803D;
        margin: 12px 0 6px 0;
        font-size: 1.8rem;
        font-weight: 800;
    }

    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 18px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.03);
    }

    .metric-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }
    
    .section-title {
        color: #0F172A;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.2s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'lang' not in st.session_state:
    st.session_state.lang = 'hi'
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# ==========================================
# 1. TOP HEADER & LANGUAGE SWITCHER
# ==========================================
is_hi = (st.session_state.lang == 'hi')

st.markdown(f"""
    <div class="app-bar">
        <h1>🌾 KRISHI PLATFORM</h1>
        <p>{"डिजिटल मंडी खरीद एवं किसान सत्यापन पास पोर्टल" if is_hi else "Digital Procurement & Farmer Verification Pass Portal"}</p>
    </div>
""", unsafe_allow_html=True)

# Language Selector
st.caption("🌐 **भाषा चुनें / Select Language:**")
lang_col1, lang_col2 = st.columns(2)

with lang_col1:
    if st.button("🇮🇳 हिंदी (Hindi)", use_container_width=True, type="primary" if is_hi else "secondary"):
        st.session_state.lang = 'hi'
        st.rerun()

with lang_col2:
    if st.button("🇬🇧 English", use_container_width=True, type="primary" if not is_hi else "secondary"):
        st.session_state.lang = 'en'
        st.rerun()

st.divider()

# ==========================================
# 2. FIRST PAGE: AADHAAR REGISTRATION & LOGIN
# ==========================================
if not st.session_state.user_registered:
    st.markdown(f'<div class="section-title">🔐 {"किसान पंजीकरण / गेट पास टोकन" if is_hi else "Farmer Registration & Gate Pass"}</div>', unsafe_allow_html=True)
    st.info("ℹ️ " + ("मंडी में प्रवेश और स्लॉट बुकिंग के लिए अपना आधार और मोबाइल नंबर दर्ज करें।" if is_hi else "Enter Aadhaar and Mobile Number to generate your official Mandi Entry Pass."))

    with st.form("registration_form"):
        farmer_name = st.text_input("किसान का पूरा नाम *" if is_hi else "Farmer Full Name *", placeholder="e.g. Ramesh Kumar")
        aadhaar_no = st.text_input("आधार कार्ड नंबर (12 अंक) *" if is_hi else "Aadhaar Card Number (12 Digits) *", type="password", max_chars=12)
        mobile_no = st.text_input("मोबाइल नंबर (10 अंक) *" if is_hi else "Mobile Number (10 Digits) *", max_chars=10)
        district = st.text_input("ज़िला / मंडी क्षेत्र *" if is_hi else "District / Mandi Region *", placeholder="e.g. Meerut / Delhi")

        submit_reg = st.form_submit_button("पंजीकरण करें और पास प्राप्त करें 🎫" if is_hi else "Register & Get Mandi Pass 🎫", use_container_width=True, type="primary")

        if submit_reg:
            if len(aadhaar_no) == 12 and aadhaar_no.isdigit() and len(mobile_no) == 10 and mobile_no.isdigit() and farmer_name.strip():
                token_id = f"KRN-2026-{random.randint(10000, 99999)}"
                st.session_state.user_registered = True
                st.session_state.user_data = {
                    "name": farmer_name,
                    "aadhaar_masked": f"XXXX-XXXX-{aadhaar_no[-4:]}",
                    "mobile": mobile_no,
                    "district": district,
                    "token_id": token_id
                }
                st.rerun()
            else:
                st.error("❌ " + ("कृपया सही 12-अंकों का आधार नंबर, 10-अंकों का मोबाइल नंबर और नाम भरें।" if is_hi else "Please enter a valid 12-digit Aadhaar number, 10-digit mobile number, and full name."))

# ==========================================
# 3. MAIN DASHBOARD (AFTER LOGIN)
# ==========================================
else:
    user = st.session_state.user_data
    
    # Guard Gate Pass Token Card
    st.markdown(f"""
        <div class="pass-card">
            <span class="badge">
                {"मंडी गेट पास • VERIFIED" if is_hi else "MANDI ENTRY PASS • VERIFIED"}
            </span>
            <h2>🆔 {user['token_id']}</h2>
            <p style="margin:4px 0; font-weight:700; color:#0F172A;">{"किसान:" if is_hi else "Farmer:"} {user['name']} | {"आधार:" if is_hi else "Aadhaar:"} {user['aadhaar_masked']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.88rem;">{"मोबाइल:" if is_hi else "Mobile:"} {user['mobile']} | {"क्षेत्र:" if is_hi else "Region:"} {user['district']}</p>
            <hr style="border-top: 1px dashed #22C55E; margin:12px 0;">
            <p style="color:#DC2626; font-size:0.85rem; font-weight:700; margin:0;">
                🛡️ {"गार्ड सुरक्षा सूचना: मंडी गेट पर गार्ड को यह टोकन आईडी दिखाएं।" if is_hi else "SECURITY NOTICE: Show this Token ID to the Security Guard at Mandi Gate."}
            </p>
        </div>
    """, unsafe_allow_html=True)

    logout_col1, logout_col2 = st.columns([3, 1])
    with logout_col2:
        if st.button("🔒 " + ("लॉगआउट" if is_hi else "Logout"), use_container_width=True):
            st.session_state.user_registered = False
            st.session_state.user_data = {}
            st.rerun()

    # Sidebar Navigation
    modules = [
        "🌾 मंडी भाव और सरकारी MSP",
        "🤖 AI फसल गुणवत्ता एवं मूल्य",
        "🗺️ लाइव मंडी भीड़ और ट्रैफिक",
        "🎙️ आवाज़ सहायक (Voice Assistant)",
        "📱 टाइम स्लॉट बुकिंग", 
        "🚨 मंडी भीड़ एवं देरी अलर्ट", 
        "💳 DBT भुगतान स्थिति",
        "🌤️ मौसम पूर्वानुमान", 
        "📞 Non-Smartphone (IVR / SMS)"
    ] if is_hi else [
        "🌾 Live Mandi Rates & MSP",
        "🤖 AI Crop Quality & Price",
        "🗺️ Live Mandi Rush & Traffic Map",
        "🎙️ Voice Assistant for Farmers",
        "📱 Time Slot Booking", 
        "🚨 Live Rush & Delay Alerts", 
        "💳 DBT Payment Status",
        "🌤️ Mandi Weather Forecast", 
        "📞 Non-Smartphone (IVR / SMS)"
    ]

    st.sidebar.title("📌 " + ("मुख्य सेवाएं" if is_hi else "Main Services"))
    choice = st.sidebar.radio("सेवा चुनें / Select Service:", modules)

    depot_list = ["केंद्रीय अनाज डिपो ए", "क्षेत्रीय मंडी हब बी", "जिला डिपो सी"] if is_hi else ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"]

    # --- MODULE 1: MANDI RATES ---
    if choice in ["🌾 मंडी भाव और सरकारी MSP", "🌾 Live Mandi Rates & MSP"]:
        st.markdown(f'<div class="section-title">🌾 {"आज के मंडी भाव और सरकारी MSP दरें" if is_hi else "Live Mandi Rates & Govt MSP"}</div>', unsafe_allow_html=True)
        depot = st.selectbox("मंडी केंद्र चुनें:" if is_hi else "Select Mandi Center:", depot_list)
        
        st.subheader(f"📊 {depot}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-container">
                    <h3 style="margin:0; color:#1E3A8A;">🌾 {"गेहूं" if is_hi else "Wheat"}</h3>
                    <h2 style="margin:8px 0; color:#15803D;">₹ 2,275</h2>
                    <p style="margin:0; font-size:0.8rem; color:#64748B;">{"सरकारी MSP दर" if is_hi else "Govt MSP Rate"}</p>
                    <hr style="margin:8px 0; border-top:1px solid #E2E8F0;">
                    <p style="margin:0; font-size:0.82rem; font-weight:600;">Max: ₹ 2,310 | Min: ₹ 2,250</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <h3 style="margin:0; color:#1E3A8A;">🌾 {"धान" if is_hi else "Paddy"}</h3>
                    <h2 style="margin:8px 0; color:#15803D;">₹ 2,183</h2>
                    <p style="margin:0; font-size:0.8rem; color:#64748B;">{"सरकारी MSP दर" if is_hi else "Govt MSP Rate"}</p>
                    <hr style="margin:8px 0; border-top:1px solid #E2E8F0;">
                    <p style="margin:0; font-size:0.82rem; font-weight:600;">Max: ₹ 2,220 | Min: ₹ 2,150</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-container">
                    <h3 style="margin:0; color:#1E3A8A;">🫘 {"चना / दाल" if is_hi else "Pulses"}</h3>
                    <h2 style="margin:8px 0; color:#15803D;">₹ 5,440</h2>
                    <p style="margin:0; font-size:0.8rem; color:#64748B;">{"सरकारी MSP दर" if is_hi else "Govt MSP Rate"}</p>
                    <hr style="margin:8px 0; border-top:1px solid #E2E8F0;">
                    <p style="margin:0; font-size:0.82rem; font-weight:600;">Max: ₹ 5,500 | Min: ₹ 5,380</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 2: AI QUALITY ESTIMATOR ---
    elif choice in ["🤖 AI फसल गुणवत्ता एवं मूल्य", "🤖 AI Crop Quality & Price"]:
        st.markdown(f'<div class="section-title">🤖 {"AI फसल गुणवत्ता एवं मूल्य कैलकुलेटर" if is_hi else "AI-Powered Quality & Price Estimator"}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            crop_options = ["गेहूं", "धान", "चना / दाल"] if is_hi else ["Wheat", "Paddy", "Pulses"]
            crop_type = st.selectbox("फसल चुनें:" if is_hi else "Select Crop:", crop_options)
            moisture = st.slider("नमी की मात्रा (%):" if is_hi else "Moisture Percentage (%):", 5.0, 25.0, 11.0)
            broken_grains = st.slider("टूटे दाने / कचरा (%):" if is_hi else "Broken Grains / Foreign Matter (%):", 0.0, 10.0, 1.5)
        
        base_msp = 2275 if crop_type in ["Wheat", "गेहूं"] else (2183 if crop_type in ["Paddy", "धान"] else 5440)
        bonus = 85 if moisture <= 12.0 and broken_grains <= 2.0 else (0 if moisture <= 14.0 else -120)
        final_price = base_msp + bonus
        
        with col2:
            st.markdown(f"""
                <div class="content-card" style="text-align:center; background:#F8FAFC;">
                    <h4 style="margin:0; color:#475569;">{"अनुमानित मूल्य" if is_hi else "Estimated Selling Rate"}</h4>
                    <h1 style="color
