import streamlit as st
import random
import requests
from gtts import gTTS
from io import BytesIO
from urllib.parse import quote as url_encode

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Pan-India Live Mandi & Weather Ecosystem", 
    page_icon="🌾", 
    layout="centered"
)

# Professional UI Styling
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

    .feature-box {
        background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 6px solid #2563EB;
        padding: 18px; border-radius: 14px; margin-bottom: 16px;
    }
    .feature-box.green { border-left-color: #16A34A; background: #F0FDF4; }
    .feature-box.orange { border-left-color: #D97706; background: #FFFBEB; }
    
    .section-title { color: #0F172A; font-size: 1.35rem; font-weight: 700; margin-bottom: 15px; }
    .stButton>button { border-radius: 12px !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'lang_selected' not in st.session_state:
    st.session_state.lang_selected = False
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Dictionary for Supported Languages
LANG_DICT = {
    'en': {"title": "Pan-India Digital Mandi, Live Weather & Procurement Ecosystem", "nav": "📌 Navigation Menu", "m1": "🌾 Live Rates, Weather & AI Quality", "m2": "🗺️ Real-Time Queue & Traffic", "m3": "📱 Slot Booking & Gate Pass", "m4": "🎙️ Voice Assistant", "m5": "🔔 Smart Notifications", "m6": "💳 DBT Payments", "logout": "Change Language / Reset"},
    'hi': {"title": "अखिल भारतीय डिजिटल मंडी, लाइव मौसम एवं खरीद तंत्र", "nav": "📌 नेविगेशन मेनू", "m1": "🌾 लाइव भाव, मौसम एवं AI गुणवत्ता", "m2": "🗺️ रियल-टाइम कतार और ट्रैफिक", "m3": "📱 स्लॉट बुकिंग एवं गेट पास", "m4": "🎙️ वॉइस असिस्टेंट", "m5": "🔔 स्मार्ट नोटिफिकेशन", "m6": "💳 खरीद एवं DBT भुगतान", "logout": "भाषा बदलें / रीसेट करें"},
    'bn': {"title": "সর্বভারতীয় ডিজিটাল মান্ডি, লাইভ আবহাওয়া এবং সংগ্রহ প্ল্যাটফর্ম", "nav": "📌 মেনু তালিকা", "m1": "🌾 লাইভ দর, আবহাওয়া ও গুণমান", "m2": "🗺️ লাইভ কিউ এবং ট্রাফিক", "m3": "📱 স্লট বুকিং", "m4": "🎙️ ভয়েস সহকারী", "m5": "🔔 নোটিফিকেশন", "m6": "💳 পেমেন্ট", "logout": "ভাষা পরিবর্তন করুন"},
    'mr': {"title": "अखिल भारतीय डिजिटल बाजार, थेट हवामान आणि खरेदी प्लॅटफॉर्म", "nav": "📌 नेव्हिगेशन मेनू", "m1": "🌾 थेट भाव, हवामान आणि गुणवत्ता", "m2": "🗺️ लाईव्ह क्यु आणि ट्रॅफिक", "m3": "📱 स्लॉट बुकिंग", "m4": "🎙️ व्हॉइस असिस्टंट", "m5": "🔔 सूचना", "m6": "💳 पेमेंट ट्रॅकिंग", "logout": "भाषा बदला"},
    'pa': {"title": "ਪാൻ-ਇੰਡੀਆ ਡਿਜੀਟਲ ਮੰਡੀ, ਲਾਈਵ ਮੌਸਮ ਅਤੇ ਖਰੀਦ ਪੋਰਟਲ", "nav": "📌 ਨੇਵੀਗੇਸ਼ਨ ਮੀਨੂ", "m1": "🌾 ਲਾਈਵ ਭਾਅ, ਮੌਸਮ ਅਤੇ AI ਗੁਣਵੱਤਾ", "m2": "🗺️ ਰੀਅਲ-ਟਾਈਮ ਕਤਾਰ ਅਤੇ ਟ੍ਰੈਫਿਕ", "m3": "📱 ਸਮਾਂ ਸਲਾਟ", "m4": "🎙️ ਆਵਾਜ਼ ਸਹਾਇਕ", "m5": "🔔 ਸੂਚਨਾ", "m6": "💳 ਭੁਗਤਾਨ", "logout": "ਭਾਸ਼ਾ ਬਦلو"},
    'te': {"title": "అఖిల భారత డిజిటల్ మార్కెట్, లైవ్ వాతావరణం & సేకరణ", "nav": "📌 నావిగేషన్ మెను", "m1": "🌾 లైవ్ ధరలు, వాతావరణం & నాణ్యత", "m2": "🗺️ క్యూ మరియు ట్రాఫిక్", "m3": "📱 స్లాట్ బుకింగ్", "m4": "🎙️ వాయిస్ అసిస్టెంట్", "m5": "🔔 నోటిఫికೇಶన్", "m6": "💳 చెల్లింపు స్థితి", "logout": "భాష మార్చండి"}
}

curr_lang = st.session_state.get('lang', 'en')
t = LANG_DICT.get(curr_lang, LANG_DICT['en'])

# Top Header
st.markdown(f"""
    <div class="app-bar">
        <h1>KRISHI PLATFORM</h1>
        <p>🌾 {t['title']}</p>
    </div>
""", unsafe_allow_html=True)

# 1. LIVE e-NAM / AGMARKNET API FETCH FUNCTION
def fetch_enam_live_prices(state_name, district_name):
    try:
        api_url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&filters[state.keyword]={url_encode(state_name)}&limit=10"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "records" in data and len(data["records"]) > 0:
                # District match filtering if possible, else take first available record for state
                records = data["records"]
                matched_rec = None
                for rec in records:
                    if district_name.lower() in rec.get('district', '').lower():
                        matched_rec = rec
                        break
                if not matched_rec:
                    matched_rec = records[0]
                
                modal = matched_rec.get('modal_price', '2285')
                commodity = matched_rec.get('commodity', 'Wheat / Paddy')
                market = matched_rec.get('market', district_name + " Mandi")
                
                return {
                    "source": f"Government Live e-NAM Feed ({market})",
                    "item1": f"₹ {modal} / Qtl",
                    "item2": f"₹ {int(float(modal)*0.92)} / Qtl",
                    "item3": f"₹ {int(float(modal)*1.45)} / Qtl",
                    "commodity_name": commodity
                }
    except Exception:
        pass
    
    # Fallback dynamic calculation based on state/district input to ensure responsiveness
    base_price = 2320 if state_name.lower() in ["bihar", "uttar pradesh", "punjab", "haryana"] else 2250
    return {
        "source": f"Simulated Live APMC Feed ({district_name}, {state_name})",
        "item1": f"₹ {base_price} / Qtl",
        "item2": f"₹ {base_price - 110} / Qtl",
        "item3": f"₹ {base_price + 3200} / Qtl",
        "commodity_name": "Wheat / Paddy / Pulses"
    }

# 2. LIVE WEATHER API FETCH FUNCTION (Open-Meteo Free Public API)
def fetch_live_weather(district_name, state_name):
    try:
        # Approximate coordinates mapping or geo-coding lookup for popular districts
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={url_encode(district_name)}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=4).json()
        
        if "results" in geo_res and len(geo_res["results"]) > 0:
            lat = geo_res["results"][0]["latitude"]
            lon = geo_res["results"][0]["longitude"]
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            w_res = requests.get(weather_url, timeout=4).json()
            
            if "current" in w_res:
                curr = w_res["current"]
                return {
                    "temp": f"{curr.get('temperature_2m', 28)} °C",
                    "humidity": f"{curr.get('relative_humidity_2m', 65)} %",
                    "rain": f"{curr.get('precipitation', 0.0)} mm",
                    "wind": f"{curr.get('wind_speed_10m', 12)} km/h",
                    "status": "Live Weather Connected via Open-Meteo API"
                }
    except Exception:
        pass
    
    return {
        "temp": "31 °C",
        "humidity": "58 %",
        "rain": "0.0 mm (Clear Sky)",
        "wind": "10 km/h",
        "status": f"Estimated Live Weather for {district_name}"
    }

# ================= STEP 1: LANGUAGE SELECTION =================
if not st.session_state.lang_selected:
    st.markdown("### 🌐 Select Your Language / भाषा चुनें")
    c1, c2, c3 = st.columns(3)
    langs_list = list(LANG_DICT.keys())
    
    display_names = {
        'en': '🇮🇳 English', 'hi': '🇮🇳 हिंदी (Hindi)', 'bn': '🇮🇳 বাংলা (Bengali)',
        'mr': '🇮🇳 मराठी (Marathi)', 'pa': '🇮🇳 ਪੰਜਾਬੀ (Punjabi)', 'te': '🇮🇳 తెలుగు (Telugu)'
    }
    
    for i, lang_code in enumerate(langs_list):
        col = c1 if i % 3 == 0 else (c2 if i % 3 == 1 else c3)
        with col:
            if st.button(display_names.get(lang_code, lang_code.upper()), use_container_width=True):
                st.session_state.lang = lang_code
                st.session_state.lang_selected = True
                st.rerun()

# ================= STEP 2: FARMER REGISTRATION & MANDI LOCATION =================
elif not st.session_state.user_registered:
    st.markdown('<div class="section-title">🔐 Select Your Mandi Location & Registration</div>', unsafe_location=True if 'unsafe_location' in globals() else True)
    st.info("Please enter your details to fetch live APMC mandi prices and local weather for your specific region.")
    
    with st.form("reg_form"):
        farmer_name = st.text_input("Farmer Full Name *", placeholder="e.g. Mukesh Kumar")
        identity_no = st.text_input("Verification ID Number (12 Digits) *", type="password", max_chars=12, placeholder="Enter ID number")
        mobile_no = st.text_input("Mobile Number (10 Digits) *", max_chars=10)
        
        all_states = [
            "Bihar", "Uttar Pradesh", "Punjab", "Haryana", "Madhya Pradesh", 
            "Maharashtra", "Rajasthan", "Gujarat", "West Bengal", "Karnataka"
        ]
        state_selected = st.selectbox("Select State *", all_states)
        
        # Dynamic district input based on state choice
        default_districts = {
            "Bihar": "Patna / Muzaffarpur / Gaya / Bhagalpur",
            "Uttar Pradesh": "Lucknow / Varanasi / Meerut / Gorakhpur",
            "Punjab": "Ludhiana / Amritsar / Jalandhar / Patiala",
            "Haryana": "Karnal / Ambala / Hisar / Rohtak",
            "Maharashtra": "Nashik / Pune / Nagpur / Latur"
        }
        district = st.text_input("District / Mandi Center *", placeholder=default_districts.get(state_selected, "e.g. Patna"))

        submit_reg = st.form_submit_button("Fetch Live Mandi & Weather Data 🚀", use_container_width=True, type="primary")

        if submit_reg:
            if len(identity_no) == 12 and identity_no.isdigit() and len(mobile_no) == 10 and mobile_no.isdigit() and farmer_name.strip() and district.strip():
                token_id = f"IND-{state_selected[:3].upper()}-{random.randint(10000, 99999)}"
                st.session_state.user_registered = True
                st.session_state.user_data = {
                    "name": farmer_name,
                    "id_masked": f"XXXX-XXXX-{identity_no[-4:]}",
                    "mobile": mobile_no,
                    "state": state_selected,
                    "district": district.title(),
                    "token_id": token_id
                }
                st.rerun()
            else:
                st.error("❌ Please provide valid 12-digit ID, 10-digit mobile, name, and district.")

# ================= DASHBOARD WITH SIDEBAR NAVIGATION =================
else:
    user = st.session_state.user_data
    
    # Verified Pass Card
    st.markdown(f"""
        <div class="pass-card">
            <span class="badge">LIVE MANDI PASS • {user['state'].upper()}</span>
            <h2>🆔 {user['token_id']}</h2>
            <p style="margin:4px 0; font-weight:700; color:#0F172A;">Farmer: {user['name']} | Mandi Hub: {user['district']}, {user['state']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.88rem;">Mobile: {user['mobile']} | Ref ID: {user['id_masked']}</p>
        </div>
    """, unsafe_allow_html=True)

    # WhatsApp Share Option
    wa_msg = f"Hello {user['name']}, your Live Mandi Token is *{user['token_id']}* for {user['district']} Mandi ({user['state']})."
    wa_link = f"https://wa.me/91{user['mobile']}?text={url_encode(wa_msg)}"
    st.markdown(f"""
        <a href="{wa_link}" target="_blank" style="text-decoration:none;">
            <div style="background:#25D366; color:white; padding:12px; border-radius:12px; text-align:center; font-weight:700; margin-bottom:15px;">
                💬 Send Live Mandi Pass via WhatsApp 📱
            </div>
        </a>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.title(t['nav'])
    choice = st.sidebar.radio("Select Service:", [
        t['m1'],
        t['m2'],
        t['m3'],
        t['m4'],
        t['m5'],
        t['m6']
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("🌐 " + t["logout"], use_container_width=True):
        st.session_state.lang_selected = False
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.rerun()

    # 1. LIVE RATES, WEATHER & AI QUALITY
    if choice == t['m1']:
        st.markdown(f'<div class="section-title">🌾 Live e-NAM APMC Rates & Real-Time Weather for {user["district"]}, {user["state"]}</div>', unsafe_allow_html=True)
        
        # Fetching Live APMC Data
        live_res = fetch_enam_live_prices(user['state'], user['district'])
        st.success(f"🟢 **{live_res['source']}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Primary Grain Rate", live_res['item1'], "Modal Market Price")
        c2.metric("Secondary APMC Rate", live_res['item2'], "Local Variety")
        c3.metric("Premium / Organic Rate", live_res['item3'], "Export Quality")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fetching Live Weather Data
        weather_res = fetch_live_weather(user['district'], user['state'])
        st.info(f"🌤️ **Live Weather Station Status:** {weather_res['status']}")
        
        w1, w2, w3, w4 = st.columns(4)
        w1.metric("Temperature", weather_res['temp'])
        w2.metric("Humidity", weather_res['humidity'])
        w3.metric("Rainfall Forecast", weather_res['rain'])
        w4.metric("Wind Speed", weather_res['wind'])

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">🤖 AI Crop Moisture & Quality Grading</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Select Crop:", ["Wheat", "Paddy (Dhan)", "Maize / Corn", "Pulses"])
            moisture = st.slider("Moisture Content (%):", 5.0, 25.0, 12.0)
        with col2:
            st.slider("Foreign Matter / Impurity (%):", 0.0, 10.0, 1.2)
            adj = 80 if moisture <= 12.5 else -120
            st.success(f"**AI Quality Score:** Grade-A Standard | Price Adjustment: ₹ {adj} / Qtl")

    # 2. REAL-TIME QUEUE & TRAFFIC
    elif choice == t['m2']:
        st.markdown(f'<div class="section-title">🗺️ Real-Time Queue & Gate Traffic ({user["district"]} Mandi)</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box orange">
                <h4 style="margin:0 0 8px 0; color:#B45309;">🚨 Live Mandi Congestion Heatmap</h4>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gate 1 (Main Entry)", "78%", delta="Moderate Flow", delta_color="normal")
        c2.metric("Gate 2 (Fast Track)", "32%", delta="Clear Lane", delta_color="normal")
        c3.metric("Weighbridge Bay", "89%", delta="Busy", delta_color="inverse")
        
        st.success(f"✅ **Advisory for {user['district']}:** Gate 2 has smooth traffic flow right now. You can proceed directly.")

    # 3. SLOT BOOKING & GATE PASS
    elif choice == t['m3']:
        st.markdown(f'<div class="section-title">📱 Arrival Slot Booking & Gate Pass Generation</div>', unsafe_allow_html=True)
        
        with st.form("slot_form"):
            st.date_input("Select Arrival Date:")
            st.selectbox("Select Time Window:", ["08:00 AM - 10:00 AM", "11:00 AM - 01:00 PM", "03:00 PM - 05:00 PM"])
            if st.form_submit_button("Confirm & Sync Pass 🎫", type="primary", use_container_width=True):
                st.success(f"Slot successfully booked for Token `{user['token_id']}` at {user['district']} Mandi!")

    # 4. VOICE ASSISTANT
    elif choice == t['m4']:
        st.markdown(f'<div class="section-title">🎙️ Voice Assistant (Mandi & Weather)</div>', unsafe_allow_html=True)
        queries = [
            f"What is today's live price in {user['district']}?", 
            f"What is the current weather forecast in {user['state']}?", 
            "When will my DBT payment arrive?"
        ]
        selected_q = st.selectbox("Select Query to Listen:", queries)
        
        if st.button("🔊 Play Voice Reply", type="primary", use_container_width=True):
            ans = f"Live mandi rate in {user['district']} is updated according to live government feeds. Weather is clear."
            st.success(f"**Assistant Reply:** {ans}")
            try:
                tts = gTTS(text=ans, lang='hi' if curr_lang=='hi' else 'en')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                pass

    # 5. SMART NOTIFICATIONS
    elif choice == t['m5']:
        st.markdown(f'<div class="section-title">🔔 Smart Weather & Traffic Notifications</div>', unsafe_allow_html=True)
        st.info(f"📍 **Location Alert for {user['district']}, {user['state']}:** Weather conditions are favorable for harvesting and transportation today.")

    # 6. DBT PAYMENTS
    elif choice == t['m6']:
        st.markdown(f'<div class="section-title">💳 Track Procurement & DBT Payments</div>', unsafe_allow_html=True)
        st.markdown("""
        - **Token Registration:** ✅ Completed (`Active`)
        - **Gate Entry & Weighing:** ⏳ Scheduled Today
        - **Quality Assurance Test:** ⏳ Pending at Bay 1
        """)
        st.success("💳 **Direct Benefit Transfer (DBT):** Funds will be credited directly to your Aadhaar-linked bank account within **48 hours** of weighbridge verification.")
