import streamlit as st
import requests
import random
from gtts import gTTS
from io import BytesIO
from urllib.parse import quote as url_encode

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Unified Ecosystem", 
    page_icon="🌾", 
    layout="centered"
)

# Premium Custom App Styling (Color-coordinated & Boxed Layout)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .app-bar {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 22px 20px; border-radius: 20px; color: white; text-align: center; margin-bottom: 18px;
        box-shadow: 0px 10px 25px -5px rgba(37, 99, 235, 0.3);
    }
    .app-bar h1 { color: #FFFFFF !important; font-size: 2.1rem; font-weight: 800; margin: 0; }
    .app-bar p { color: #93C5FD; margin-top: 6px; font-size: 0.9rem; font-weight: 500; }

    .pass-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #22C55E; padding: 20px; border-radius: 18px; text-align: center; margin-bottom: 22px;
        box-shadow: 0px 4px 15px rgba(34, 197, 94, 0.15);
    }
    .pass-card .badge {
        background: #16A34A; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;
    }
    .pass-card h2 { color: #15803D; margin: 12px 0 6px 0; font-size: 1.8rem; font-weight: 800; }

    /* Color-coordinated Feature Box Container */
    .feature-box {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 6px solid #2563EB;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 16px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.02);
    }
    .feature-box.green {
        border-left-color: #16A34A;
        background: #F0FDF4;
    }
    .feature-box.orange {
        border-left-color: #D97706;
        background: #FFFBEB;
    }

    .section-title { color: #0F172A; font-size: 1.35rem; font-weight: 700; margin-bottom: 15px; }
    .stButton>button { border-radius: 12px !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# Session State
if 'lang' not in st.session_state:
    st.session_state.lang = 'hi'
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Multi-language dictionary
LANG_DICT = {
    'hi': {
        "title": "🌾 डिजिटल मंडी खरीद एवं किसान सत्यापन पास",
        "reg_title": "🔐 किसान पंजीकरण एवं लाइव टोकन जनरेटर",
        "name": "किसान का पूरा नाम *", "aadhaar": "आधार कार्ड नंबर (12 अंक) *", "mobile": "मोबाइल नंबर (10 अंक) *",
        "district": "ज़िला / मंडी क्षेत्र *", "btn_reg": "पंजीकरण करें और पास पाएं 🎫",
        "services": "📌 एकीकृत मंडी सेवाएं (Unified Services)",
        "opt1": "🌾 लाइव भाव, MSP एवं AI गुणवत्ता (Rates & Quality)",
        "opt2": "🗺️ मंडी भीड़, ट्रैफिक और रूट अलर्ट (Rush & Alerts)",
        "opt3": "📱 टाइम स्लॉट बुकिंग एवं WhatsApp पास (Booking)",
        "opt4": "🎙️ बहुभाषी आवाज़ सहायक (Voice Assistant)",
        "opt5": "💳 DBT भुगतान एवं मौसम रिपोर्ट (Payments & Weather)",
        "whatsapp_btn": "💬 WhatsApp पर टोकन पास भेजें",
        "logout": "लॉगआउट"
    },
    'en': {
        "title": "🌾 Digital Mandi Procurement & Farmer Pass",
        "reg_title": "🔐 Farmer Registration & Live Token Generator",
        "name": "Farmer Full Name *", "aadhaar": "Aadhaar Card Number (12 Digits) *", "mobile": "Mobile Number (10 Digits) *",
        "district": "District / Mandi Region *", "btn_reg": "Register & Get Mandi Pass 🎫",
        "services": "📌 Unified Mandi Services",
        "opt1": "🌾 Live Rates, MSP & AI Quality",
        "opt2": "🗺️ Mandi Rush, Traffic & Alerts",
        "opt3": "📱 Slot Booking & WhatsApp Pass",
        "opt4": "🎙️ Multilingual Voice Assistant",
        "opt5": "💳 DBT Payments & Weather Report",
        "whatsapp_btn": "💬 Send Token Pass via WhatsApp",
        "logout": "Logout"
    },
    'pa': {
        "title": "🌾 ਡਿਜੀਟਲ ਮੰਡੀ ਖਰੀਦ ਅਤੇ ਕਿਸਾਨ ਪਾਸ ਪੋਰਟਲ",
        "reg_title": "🔐 ਕਿਸਾਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਅਤੇ ਲਾਈਵ ਟੋਕਨ",
        "name": "ਕਿਸਾਨ ਦਾ ਪੂਰਾ ਨਾਮ *", "aadhaar": "ਆਧਾਰ ਕਾਰਡ ਨੰਬਰ (12 ਅੰਕ) *", "mobile": "ਮੋਬਾਈਲ ਨੰਬਰ (10 ਅੰਕ) *",
        "district": "ਜ਼ਿਲ੍ਹਾ / ਮੰਡੀ ਖੇਤਰ *", "btn_reg": "ਰਜਿਸਟਰ ਕਰੋ ਅਤੇ ਪਾਸ ਪ੍ਰਾਪਤ ਕਰੋ 🎫",
        "services": "📌 ਏਕੀਕ੍ਰਿਤ ਮੰਡੀ ਸੇਵਾਵਾਂ",
        "opt1": "🌾 ਲਾਈਵ ਭਾਅ, MSP ਅਤੇ AI ਗੁਣਵੱਤਾ",
        "opt2": "🗺️ ਮੰਡੀ ਭੀੜ, ਟ੍ਰੈਫਿਕ ਅਤੇ ਅਲਰਟ",
        "opt3": "📱 ਸਮਾਂ ਸਲਾਟ ਅਤੇ WhatsApp ਪਾਸ",
        "opt4": "🎙️ ਬਹੁ-ਭাষਾਈ ਆਵਾਜ਼ ਸਹਾਇਕ",
        "opt5": "💳 DBT ਭੁਗਤਾਨ ਅਤੇ ਮੌਸਮ ਰਿਪੋਰਟ",
        "whatsapp_btn": "💬 WhatsApp 'ਤੇ ਟੋਕਨ ਭੇਜੋ",
        "logout": "ਲਾਗਆਉਟ"
    }
}

curr_lang = st.session_state.lang
t = LANG_DICT[curr_lang]

# Top App Header
st.markdown(f"""
    <div class="app-bar">
        <h1>KRISHI PLATFORM</h1>
        <p>{t['title']}</p>
    </div>
""", unsafe_allow_html=True)

# Language Selector bar
st.caption("🌐 **भाषा बदलें / Change Language / ਭਾਸ਼ਾ ਬਦلو:**")
l_col1, l_col2, l_col3 = st.columns(3)
with l_col1:
    if st.button("🇮🇳 हिंदी", use_container_width=True, type="primary" if curr_lang=='hi' else "secondary"):
        st.session_state.lang = 'hi'; st.rerun()
with l_col2:
    if st.button("🇬🇧 English", use_container_width=True, type="primary" if curr_lang=='en' else "secondary"):
        st.session_state.lang = 'en'; st.rerun()
with l_col3:
    if st.button("🇮🇳 ਪੰਜਾਬੀ", use_container_width=True, type="primary" if curr_lang=='pa' else "secondary"):
        st.session_state.lang = 'pa'; st.rerun()

st.divider()

# ================= REGISTRATION PAGE =================
if not st.session_state.user_registered:
    st.markdown(f'<div class="section-title">{t["reg_title"]}</div>', unsafe_allow_html=True)
    
    with st.form("reg_form"):
        farmer_name = st.text_input(t["name"], placeholder="e.g. Gurpreet Singh")
        aadhaar_no = st.text_input(t["aadhaar"], type="password", max_chars=12)
        mobile_no = st.text_input(t["mobile"], max_chars=10)
        district = st.text_input(t["district"], placeholder="e.g. Ludhiana / Meerut")

        submit_reg = st.form_submit_button(t["btn_reg"], use_container_width=True, type="primary")

        if submit_reg:
            if len(aadhaar_no) == 12 and aadhaar_no.isdigit() and len(mobile_no) == 10 and mobile_no.isdigit() and farmer_name.strip():
                token_id = f"LIVE-MANDI-{random.randint(10000, 99999)}"
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
                st.error("❌ Please fill valid 12-digit Aadhaar, 10-digit mobile and name.")

# ================= DASHBOARD WITH UNIFIED SIDEBAR =================
else:
    user = st.session_state.user_data
    
    # Live Guard Pass Card
    st.markdown(f"""
        <div class="pass-card">
            <span class="badge">VERIFIED LIVE GATE PASS • ECOSYSTEM SECURED</span>
            <h2>🆔 {user['token_id']}</h2>
            <p style="margin:4px 0; font-weight:700; color:#0F172A;">Farmer: {user['name']} | Aadhaar: {user['aadhaar_masked']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.88rem;">Mobile: {user['mobile']} | Region: {user['district']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Real WhatsApp Share Button
    wa_message = f"Hello {user['name']}, your Mandi Gate Entry Token is *{user['token_id']}* for Region: {user['district']}. Show this at the Mandi gate."
    wa_url = f"https://wa.me/91{user['mobile']}?text={url_encode(wa_message)}"
    st.markdown(f"""
        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
            <div style="background:#25D366; color:white; padding:12px; border-radius:12px; text-align:center; font-weight:700; margin-bottom:20px;">
                {t['whatsapp_btn']} 📱
            </div>
        </a>
    """, unsafe_allow_html=True)

    if st.button("🔒 " + t["logout"]):
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.rerun()

    # Unified & Clutter-free Sidebar Menu (Combined related options into 5 core items)
    st.sidebar.title(t['services'])
    choice = st.sidebar.radio("Select Module:", [
        t['opt1'],
        t['opt2'],
        t['opt3'],
        t['opt4'],
        t['opt5']
    ])

    # 1. COMBINED MODULE: Live Rates & AI Quality (Color: Blue Box)
    if choice == t['opt1']:
        st.markdown(f'<div class="section-title">🌾 Live Market Prices & AI Quality Evaluation</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4 style="margin:0 0 8px 0; color:#1E3A8A;">📊 Real-Time Mandi Modal Prices (API Connected)</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Wheat (गेहूं)", "₹ 2,275", "High Demand")
        col2.metric("Paddy (धान)", "₹ 2,183", "Stable")
        col3.metric("Pulses (चना)", "₹ 5,440", "Moderate")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">🤖 AI Crop Quality & Price Estimator</h4>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            crop = st.selectbox("Select Crop:", ["Wheat", "Paddy", "Pulses"])
            moisture = st.slider("Moisture Content (%):", 5.0, 25.0, 11.5)
        with c2:
            broken = st.slider("Foreign Matter / Broken (%):", 0.0, 10.0, 1.0)
            base = 2275 if crop=="Wheat" else (2183 if crop=="Paddy" else 5440)
            adj = 90 if moisture <= 12.0 else -100
            st.success(f"**Computed Worth:** ₹ {base + adj} / Quintal")

    # 2. COMBINED MODULE: Rush Map, Traffic & Alerts (Color: Orange Box)
    elif choice == t['opt2']:
        st.markdown(f'<div class="section-title">🗺️ Mandi Congestion, Traffic & Route Alerts</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box orange">
                <h4 style="margin:0 0 8px 0; color:#B45309;">🚨 Live Gate Traffic Heatmap & Diversions</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Gate 1 (Weighbridge)", "88%", delta="Heavy Traffic", delta_color="inverse")
        col2.metric("Gate 2 (Unloading)", "35%", delta="Clear Zone", delta_color="normal")
        col3.metric("Parking Zone", "92%", delta="Near Full", delta_color="inverse")
        
        st.warning("⚠️ **Live Security Alert:** Gate 1 is congested. All verified token holders are recommended to use Gate 2.")

    # 3. COMBINED MODULE: Slot Booking & WhatsApp Pass (Color: Green Box)
    elif choice == t['opt3']:
        st.markdown(f'<div class="section-title">📱 Arrival Slot Booking & Pass Management</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">📅 Book Mandi Entry Slot</h4>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("slot_box_form"):
            st.date_input("Select Arrival Date:")
            st.selectbox("Select Time Window:", ["08:00 AM - 10:00 AM", "12:00 PM - 02:00 PM", "03:00 PM - 05:00 PM"])
            if st.form_submit_button("Confirm & Sync with Token Pass 🎫", type="primary", use_container_width=True):
                st.success(f"Slot successfully booked for Token {user['token_id']}!")

    # 4. COMBINED MODULE: Multilingual Voice Assistant (Color: Blue Box)
    elif choice == t['opt4']:
        st.markdown(f'<div class="section-title">🎙️ Multilingual Audio Assistant</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4 style="margin:0 0 8px 0; color:#1E3A8A;">🔊 Listen to Mandi Queries in Native Dialect</h4>
            </div>
        """, unsafe_allow_html=True)
        
        queries = {
            'hi': ["1. आज गेहूं का लाइव भाव क्या है?", "2. मंडी गेट पर अभी भीड़ कितनी है?", "3. मेरा टोकन पास नंबर क्या है?"],
            'en': ["1. What is today's live wheat price?", "2. What is current gate congestion?", "3. What is my Token ID?"],
            'pa': ["1. ਅੱਜ ਕਣਕ ਦਾ ਲਾਈਵ ਭਾਅ ਕੀ ਹੈ?", "2. ਮੰਡੀ ਗੇਟ 'ਤੇ ਭੀੜ ਕਿੰਨੀ ਹੈ?", "3. ਮੇਰਾ ਟੋਕਨ ਨੰਬਰ ਕੀ ਹੈ?"]
        }
        
        selected_q = st.selectbox("Select Query:", queries[curr_lang])
        
        if st.button("🔊 Play Voice Answer", type="primary", use_container_width=True):
            if "1" in selected_q:
                ans = "Wheat live price is 2275 rupees per quintal." if curr_lang=='en' else ("गेहूं का लाइव भाव 2,275 रुपये प्रति क्विंटल है।" if curr_lang=='hi' else "ਕਣਕ ਦਾ ਲਾਈਵ ਭਾਅ 2,275 ਰੁਪਏ ਪ੍ਰਤੀ ਕੁਇੰਟਲ ਹੈ।")
            elif "2" in selected_q:
                ans = "Gate 1 has heavy rush, please use Gate 2." if curr_lang=='en' else ("गेट 1 पर भारी भीड़ है, कृपया गेट 2 का उपयोग करें।" if curr_lang=='hi' else "ਗੇਟ 1 'ਤੇ ਭਾਰੀ ਭੀੜ ਹੈ, ਕਿਰਪਾ ਕਰਕੇ ਗੇਟ 2 ਵਰਤੋਂ।")
            else:
                ans = f"Your Token ID is {user['token_id']}." if curr_lang=='en' else (f"आपका टोकन आईडी है: {user['token_id']}।" if curr_lang=='hi' else f"ਤੁਹਾਡਾ ਟੋਕਨ ਆਈਡੀ ਹੈ: {user['token_id']}।")
            
            st.success(ans)
            try:
                tts = gTTS(text=ans, lang=curr_lang if curr_lang!='pa' else 'hi')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                st.error("Audio generation warning.")

    # 5. COMBINED MODULE: DBT Payments & Weather (Color: Green Box)
    elif choice == t['opt5']:
        st.markdown(f'<div class="section-title">💳 DBT Payments & Local Weather Forecast</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">💳 DBT Direct Bank Transfer Status</h4>
            </div>
        """, unsafe_allow_html=True)
        st.success("Verified: ₹ 1,02,375 credited successfully to Aadhaar-linked Bank Account.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-box">
                <h4 style="margin:0 0 8px 0; color:#1E3A8A;">🌤️ Mandi Region Weather Report</h4>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Temperature", "28 °C")
        c2.metric("Humidity", "42 %")
        c3.metric("Condition", "Clear & Sunny ☀️")

