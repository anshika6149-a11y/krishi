import streamlit as st
import random
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Multilingual Portal", 
    page_icon="🌾", 
    layout="centered"
)

# Clean & Professional UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .app-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 18px; border-radius: 14px; color: white; text-align: center; margin-bottom: 15px;
        box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.2);
    }
    .app-header h1 { color: #FFFFFF !important; font-size: 1.6rem; font-weight: 800; margin: 0; }
    .app-header p { color: #93C5FD; margin: 4px 0 0 0; font-size: 0.8rem; }

    .pass-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #22C55E; padding: 14px; border-radius: 12px; text-align: center; margin-bottom: 15px;
    }
    .section-box { color: #0F172A; font-size: 1.1rem; font-weight: 700; margin-bottom: 10px; }
    .stButton>button { border-radius: 8px !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'slot_booked' not in st.session_state:
    st.session_state.slot_booked = False
if 'transport_booked' not in st.session_state:
    st.session_state.transport_booked = False

# 22 Languages Dictionary Pack (Including Weather & Updated Driver Info)
LANG_PACK = {
    'en': {
        "title": "Digital Mandi & Logistics Portal", "nav": "📌 Menu", 
        "m1": "🌾 Live Rates & AI Check", "m2": "🗺️ Traffic & Queue", 
        "m3": "📱 Slot & Gate Pass", "m4": "🚚 Transport Booking", 
        "m5": "🎙️ Voice Assistant", "m6": "💳 DBT Payment Tracking", 
        "m7": "🌤️ Weather Forecast",
        "reg_title": "🔐 Farmer Registration", "name_lbl": "Full Name *", 
        "id_lbl": "ID Number *", "mob_lbl": "Mobile Number (10 Digits) *", 
        "state_lbl": "Select State *", "dist_lbl": "District *", "vill_lbl": "Select Village *",
        "reg_btn": "Register Now 🚀"
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव भाव और AI जांच", "m2": "🗺️ भीड़ और कतार स्थिति", 
        "m3": "📱 स्लॉट और गेट पास", "m4": "🚚 गाड़ी (ट्रांसपोर्ट) बुकिंग", 
        "m5": "🎙️ बोलकर पूछें (वॉइस)", "m6": "💳 पैसा (DBT) ट्रैकिंग", 
        "m7": "🌤️ मौसम की जानकारी",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या *", "mob_lbl": "मोबाइल नंबर (10 अंक) *", 
        "state_lbl": "राज्य चुनें *", "dist_lbl": "जिला चुनें *", "vill_lbl": "गांव चुनें *",
        "reg_btn": "पंजीकरण करें 🚀"
    },
    'bn': {
        "title": "ডিজিটাল মান্ডি এবং লজিস্টিকস", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ দর এবং AI গ্রেডিং", "m2": "🗺️ ট্রাফিক এবং কিউ", 
        "m3": "📱 স্লট এবং গেট পাস", "m4": "🚚 পরিবহন বুকিং", 
        "m5": "🎙️ ভয়েস অ্যাসিস্ট্যান্ট", "m6": "💳 পেমেন্ট ট্র্যাকিং", 
        "m7": "🌤️ আবহাওয়া পূর্বাভাস",
        "reg_title": "🔐 কৃষক নিবন্ধন", "name_lbl": "সম্পূর্ণ নাম *", 
        "id_lbl": "আইডি নম্বর *", "mob_lbl": "মোবাইল নম্বর *", 
        "state_lbl": "রাজ্য নির্বাচন করুন *", "dist_lbl": "জেলা *", "vill_lbl": "গ্রাম নির্বাচন করুন *",
        "reg_btn": "নিবন্ধন করুন 🚀"
    },
    'mr': {
        "title": "डिजिटल बाजार आणि वाहतूक पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाईव्ह भाव आणि तपासणी", "m2": "🗺️ रहदारी आणि रांग", 
        "m3": "📱 वेळ आणि पास", "m4": "🚚 वाहन बुकिंग", 
        "m5": "🎙️ बोलून माहिती घ्या", "m6": "💳 पैशांची स्थिती", 
        "m7": "🌤️ हवामान अंदाज",
        "reg_title": "🔐 शेतकरी नोंदणी", "name_lbl": "पूर्ण नाव *", 
        "id_lbl": "ओळख क्रमांक *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य निवडा *", "dist_lbl": "जिल्हा *", "vill_lbl": "गाव निवडा *",
        "reg_btn": "नोंदणी करा 🚀"
    },
    'pa': {
        "title": "ਡਿਜੀਟਲ ਮੰਡੀ ਅਤੇ ਟਰਾਂਸਪੋਰਟ", "nav": "📌 ਮੀਨੂ", 
        "m1": "🌾 ਲਾਈ브 ਭਾਅ ਅਤੇ ਜਾਂਚ", "m2": "🗺️ ਟ੍ਰੈਫਿਕ ਅਤੇ ਲਾਈਨ", 
        "m3": "📱 ਸਮံ ਅਤੇ ਪਾਸ", "m4": "🚚 ਗੱਡੀ ਬੁਕਿੰਗ", 
        "m5": "🎙️ ਬੋਲ ਕੇ ਪੁੱਛੋ", "m6": "💳 ਪੇਮੈਂਟ ਸਥਿਤੀ", 
        "m7": "🌤️ ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ",
        "reg_title": "🔐 ਕਿਸਾਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ", "name_lbl": "ਪੂਰਾ ਨਾਮ *", 
        "id_lbl": "ਆਈਡੀ ਨੰਬਰ *", "mob_lbl": "ਮੋਬਾਈਲ ਨੰਬਰ *", 
        "state_lbl": "ਰਾਜ ਚੁਣੋ *", "dist_lbl": "ਜ਼ਿਲ੍ਹਾ *", "vill_lbl": "ਪਿੰਡ ਚੁਣੋ *",
        "reg_btn": "ਰਜਿਸਟਰ ਕਰੋ 🚀"
    },
    'gu': {
        "title": "ડિજિટલ મંડી અને પરિવહન", "nav": "📌 મેનુ", 
        "m1": "🌾 લાઇવ ભાવ અને ચકાસણી", "m2": "🗺️ ટ્રાફિક અને લાઇન", 
        "m3": "📱 સ્લોટ અને પાસ", "m4": "🚚 વાહન બુકિંગ", 
        "m5": "🎙️ અવાજ સહાયક", "m6": "💳 ચુકવણી ટ્રેકિંગ", 
        "m7": "🌤️ હવામાન અહેવાલ",
        "reg_title": "🔐 ખેડૂત નોંધણી", "name_lbl": "પૂરું નામ *", 
        "id_lbl": "આઈડી નંબર *", "mob_lbl": "મોબાઈલ નંબર *", 
        "state_lbl": "રાજ્ય પસંદ કરો *", "dist_lbl": "જિલ્લો *", "vill_lbl": "ગામ પસંદ કરો *",
        "reg_btn": "નોંધણી કરો 🚀"
    }
}

all_22_langs = {
    'en': 'English', 'hi': 'हिन्दी (Hindi)', 'bn': 'বাংলা (Bengali)',
    'mr': 'मराठी (Marathi)', 'pa': 'ਪੰਜਾਬੀ (Punjabi)', 'gu': 'ગુજરાતી (Gujarati)',
    'ta': 'தமிழ் (Tamil)', 'te': 'తెలుగు (Telugu)', 'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)', 'or': 'ଓଡ଼ିଆ (Odia)', 'ur': 'اردو (Urdu)',
    'as': 'অসমীয়া (Assamese)', 'ne': 'नेपाली (Nepali)', 'sd': 'سنڌي (Sindhi)',
    'ks': 'कॉशुर (Kashmiri)', 'kok': 'कोंकणी (Konkani)', 'mni': 'মৈতৈলোন্ (Manipuri)',
    'bodo': 'बर\' (Bodo)', 'doi': 'डोगरी (Dogri)', 'mai': 'मैथिली (Maithili)', 'sat': 'संताली (Santali)'
}

# Global Top Bar for Language Selection
st.sidebar.markdown("### 🌐 Language / भाषा चुनें")
selected_lang_name = st.sidebar.selectbox(
    "Choose Language:", 
    list(all_22_langs.values()), 
    index=list(all_22_langs.keys()).index(st.session_state.lang) if st.session_state.lang in all_22_langs else 0
)

for code, name in all_22_langs.items():
    if name == selected_lang_name:
        if st.session_state.lang != code:
            st.session_state.lang = code
            st.rerun()

curr_lang = st.session_state.lang
t = LANG_PACK.get(curr_lang, LANG_PACK['en'])

# App Header Banner
st.markdown(f"""
    <div class="app-header">
        <h1>KRISHI PLATFORM</h1>
        <p>🌾 {t['title']}</p>
    </div>
""", unsafe_allow_html=True)

STATE_DISTRICTS = {
    "Gujarat": {
        "Ahmedabad APMC": ["Vinchhiya", "Bavla", "Dholka", "Sanand", "Detroj"],
        "Surat APMC": ["Mandvi", "Bardoli", "Kamrej", "Palsana", "Olpad"],
        "Rajkot APMC": ["Gondal", "Jetpur", "Dhoraji", "Jasdan", "Upleta"]
    },
    "Punjab": {
        "Ludhiana APMC": ["Machhiwara", "Payal", "Samrala", "Jagraon", "Khanna"],
        "Amritsar APMC": ["Ajnala", "Baba Bakala", "Rayya", "Chogawan", "Majitha"],
        "Patiala APMC": ["Nabha", "Rajpura", "Samana", "Patran", "Ghanaur"]
    },
    "Uttar Pradesh": {
        "Lucknow APMC": ["Kakori", "Malihabad", "Banthra", "Chinhat", "Itaunja"],
        "Varanasi APMC": ["Pindra", "Cholapur", "Baragaon", "Sevapuri", "Kashi Vidyapith"],
        "Kanpur APMC": ["Bidhnu", "Bilhaur", "Ghatampur", "Chaubepur", "Kalyanpur"]
    },
    "Bihar": {
        "Patna APMC": ["Bihta", "Danapur", "Phulwari Sharif", "Mokama", "Barh"],
        "Muzaffarpur APMC": ["Kanti", "Minapur", "Bochaha", "Sakra", "Gaighat"],
        "Bhagalpur APMC": ["Naugachhia", "Kahalgaon", "Sultanganj", "Sabour", "Goradih"]
    },
    "Haryana": {
        "Karnal APMC": ["Nilokheri", "Assandh", "Gharaunda", "Indri", "Kunjpura"],
        "Hisar APMC": ["Hansi", "Narnaund", "Barwala", "Adampur", "Uklana"],
        "Rohtak APMC": ["Meham", "Kalanaur", "Sampla", "Bansi", "Kharawar"]
    }
}

# ================= STEP 1: FARMER REGISTRATION =================
if not st.session_state.user_registered:
    st.markdown(f'<div class="section-box">{t["reg_title"]}</div>', unsafe_allow_html=True)
    
    with st.form("reg_form"):
        farmer_name = st.text_input(t["name_lbl"], placeholder="e.g. Mukesh Kumar")
        identity_no = st.text_input(t["id_lbl"], type="password", max_chars=12, placeholder="Enter ID number")
        mobile_no = st.text_input(t["mob_lbl"], max_chars=10, placeholder="10-digit mobile number")
        
        all_states = list(STATE_DISTRICTS.keys())
        state_selected = st.selectbox(t["state_lbl"], all_states)
        
        dist_dict = STATE_DISTRICTS.get(state_selected, {"Main APMC": ["Main Village"]})
        district = st.selectbox(t["dist_lbl"], list(dist_dict.keys()))
        
        village_list = dist_dict.get(district, ["Village A", "Village B"])
        village = st.selectbox(t["vill_lbl"], village_list)

        submit_reg = st.form_submit_button(t["reg_btn"], use_container_width=True, type="primary")

        if submit_reg:
            if len(mobile_no) == 10 and mobile_no.isdigit() and farmer_name.strip():
                token_id = f"IND-{state_selected[:3].upper()}-{random.randint(10000, 99999)}"
                st.session_state.user_registered = True
                st.session_state.user_data = {
                    "name": farmer_name, "mobile": mobile_no,
                    "state": state_selected, "district": district,
                    "village": village, "token_id": token_id
                }
                st.rerun()
            else:
                st.error("❌ Please enter a valid 10-digit mobile number and full name.")

# ================= STEP 2: MAIN DASHBOARD =================
else:
    user = st.session_state.user_data
    
    st.markdown(f"""
        <div class="pass-box">
            <span style="background:#16A34A; color:white; padding:2px 10px; border-radius:10px; font-size:0.7rem; font-weight:700;">VERIFIED PASS</span>
            <h2 style="color:#15803D; margin:8px 0 4px 0; font-size:1.3rem;">🆔 Token: {user['token_id']}</h2>
            <p style="margin:2px 0; font-weight:600; color:#0F172A;">Farmer: {user['name']} | Village: {user['village']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.8rem;">Center: {user['district']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"--- \n ### {t['nav']}")
    choice = st.sidebar.radio("Select Module:", [
        t['m1'], t['m2'], t['m3'], t['m4'], t['m5'], t['m6'], t['m7']
    ], label_visibility="collapsed")

    # Logout / Reset Button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Profile", use_container_width=True):
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.rerun()

    # --- MODULE 1: LIVE e-NAM RATES & AI QUALITY GRADING ---
    if choice == t['m1']:
        st.markdown(f'<div class="section-box">🌾 Live Rates & AI Check</div>', unsafe_allow_html=True)
        st.success(f"🟢 Synced for {user['district']} ({user['village']})")
        
        st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 4px solid #16A34A; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                <h4 style="margin: 0 0 4px 0; color: #15803D;">1. Wheat (गेहूं)</h4>
                <p style="margin: 2px 0;"><b>Modal Price:</b> ₹ 2350 / Quintal</p>
                <p style="margin: 2px 0; font-size: 0.8rem; color: #64748B;">Min: ₹ 2280 | Max: ₹ 2420</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Crop:", ["Wheat", "Paddy", "Maize"])
            st.slider("Moisture (%):", 5.0, 20.0, 12.0)
        with col2:
            st.slider("Impurity (%):", 0.0, 5.0, 1.0)
            st.success("**Grade:** Grade-A Standard")

    # --- MODULE 2: QUEUE & TRAFFIC HEATMAP ---
    elif choice == t['m2']:
        st.markdown(f'<div class="section-box">🗺️ Traffic & Queue Status</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Gate 1", "35%", delta="Normal")
        c2.metric("Gate 2", "18%", delta="Clear")
        c3.metric("Weighbridge", "65%", delta="Busy", delta_color="inverse")
        st.success("✅ **Tip:** Gate 2 has minimum waiting time right now.")

    # --- MODULE 3: SLOT BOOKING & GATE PASS ---
    elif choice == t['m3']:
        st.markdown(f'<div class="section-box">📱 Slot & Gate Pass</div>', unsafe_allow_html=True)
        with st.form("slot_form"):
            arr_date = st.date_input("Date:")
            time_slot = st.selectbox("Time Window:", ["08:00 AM - 10:00 AM", "11:00 AM - 01:00 PM", "03:00 PM - 05:00 PM"])
            submit_slot = st.form_submit_button("Generate Gate Pass 🎫", type="primary", use_container_width=True)
            
            if submit_slot:
                st.session_state.slot_booked = True
                st.session_state.slot_details = {
                    "date": str(arr_date), "time": time_slot,
                    "coupon_code": f"CPN-{random.randint(100000, 999999)}"
                }

        if st.session_state.slot_booked:
            s_data = st.session_state.slot_details
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px dashed #16A34A; padding: 14px; border-radius: 10px; margin-top: 10px;">
                    <h3 style="color:#15803D; margin-top:0;">🎫 Entry Pass</h3>
                    <p style="margin:2px 0;"><b>Token:</b> {user['token_id']}</p>
                    <p style="margin:2px 0;"><b>Code:</b> <span style="background:#22C55E; color:white; padding:2px 6px; border-radius:4px;">{s_data['coupon_code']}</span></p>
                    <p style="margin:2px 0;"><b>Slot:</b> {s_data['date']} ({s_data['time']})</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 4: TRANSPORT & TRUCK BOOKING ---
    elif choice == t['m4']:
        st.markdown(f'<div class="section-box">🚚 Transport Booking</div>', unsafe_allow_html=True)
        with st.form("transport_form"):
            t_type = st.selectbox("Vehicle Type:", ["Mini Truck (Tata Ace)", "Tractor Trolley", "Commercial Truck"])
            pickup_loc = st.text_input("Village Pickup Address:", placeholder="e.g. Near Village Chaupal")
            est_weight = st.number_input("Crop Weight (Quintals):", min_value=5, max_value=200, value=25)
            
            submit_transport = st.form_submit_button("Book Vehicle 🚚", type="primary", use_container_width=True)
            
            if submit_transport:
                st.session_state.transport_booked = True
                st.session_state.transport_details = {
                    "vehicle": t_type, "location": pickup_loc if pickup_loc else user['village'],
                    "driver": "Ramesh Singh", "driver_phone": "7254879397", "truck_no": f"HR-26-{random.randint(1000,9999)}"
                }

        if st.session_state.transport_booked:
            td = st.session_state.transport_details
            st.markdown(f"""
                <div style="background: #F5F3FF; border: 1px solid #CBD5E1; border-left: 5px solid #7C3AED; padding: 12px; border-radius: 8px;">
                    <h4 style="margin:0 0 4px 0; color:#6D28D9;">✅ Vehicle Booked!</h4>
                    <p style="margin:2px 0;"><b>Vehicle:</b> {td['vehicle']} ({td['truck_no']})</p>
                    <p style="margin:2px 0;"><b>Driver:</b> {td['driver']} | <b>Phone:</b> {td['driver_phone']}</p>
                    <a href="https://wa.me/91{td['driver_phone']}?text=Hello%20Driver,%20I%20have%20booked%20your%20transport%20for%20crop%20pickup." target="_blank" style="display:inline-block; margin-top:8px; background:#25D366; color:white; padding:6px 12px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem;">💬 Chat on WhatsApp</a>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 5: VOICE ASSISTANT ---
    elif choice == t['m5']:
        st.markdown(f'<div class="section-box">🎙️ Voice Assistant</div>', unsafe_allow_html=True)
        st.info("Speak or type your question.")
        
        audio_file = st.audio_input("Record Voice Question:")
        user_query = st.text_input("Or Type Question:", placeholder="Type here...")
        
        if st.button("🔊 Play Local Audio Response", type="primary", use_container_width=True):
            resp_text = user_query if user_query else "Your data is updated successfully."
            st.success(f"**Response:** {resp_text}")
            try:
                from gtts import gTTS
                tts = gTTS(text=resp_text, lang=curr_lang if curr_lang in LANG_PACK else 'en')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                pass

    # --- MODULE 6: TRANSPARENT DBT PAYMENT TRACKING ---
    elif choice == t['m6']:
        st.markdown(f'<div class="section-box">💳 DBT Payment Tracking</div>', unsafe_allow_html=True)
        st.markdown(f"""
        | Stage | Status | Remarks |
        | :--- | :--- | :--- |
        | **1. Registration** | ✅ Done | Token `{user['token_id']}` |
        | **2. Gate Entry** | ✅ Done | Verified at {user['district']} |
        | **3. Quality & Sale** | ✅ Done | Grade-A Sold |
        | **4. Bank Transfer (DBT)** | ⏳ Processing | Secure transfer in progress |
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("💳 **Status:** Funds will be credited to your Aadhaar-linked bank account within 24-48 hours.")

    # --- MODULE 7: WEATHER FORECAST ---
    elif choice == t['m7']:
        st.markdown(f'<div class="section-box">🌤️ Weather Forecast & Advisory</div>', unsafe_allow_html=True)
        st.success(f"🟢 Location: {user['village']}, {user['district']} ({user['state']})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "32°C", "2°C")
        col2.metric("Humidity", "58%", "-4%")
        col3.metric("Rainfall Risk", "Low", "0 mm")
        
        st.markdown("""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 14px; border-radius: 10px; margin-top: 10px;">
                <h4 style="margin:0 0 6px 0; color:#166534;">🌾 Farmer Advisory</h4>
                <p style="margin:0; color:#14532D; font-size:0.9rem;">Weather conditions are optimal for harvesting and transporting crops to the mandi over the next 48 hours. No immediate rain expected.</p>
            </div>
        """)
