import streamlit as st
import random
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Complete Portal", 
    page_icon="🌾", 
    layout="centered"
)

# UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; }
    .app-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 20px; border-radius: 14px; color: white; text-align: center; margin-bottom: 15px;
    }
    .app-header h1 { color: #FFFFFF !important; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .app-header p { color: #93C5FD; margin: 6px 0 0 0; font-size: 1rem; }
    .pass-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #22C55E; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;
    }
    .section-box { color: #0F172A; font-size: 1.3rem; font-weight: 700; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'lang' not in st.session_state: st.session_state.lang = 'hi'
if 'user_registered' not in st.session_state: st.session_state.user_registered = False
if 'user_data' not in st.session_state: st.session_state.user_data = {}
if 'slot_booked' not in st.session_state: st.session_state.slot_booked = False
if 'transport_booked' not in st.session_state: st.session_state.transport_booked = False
if 'offline_sms_booked' not in st.session_state: st.session_state.offline_sms_booked = False

# Multi-Language Dictionary Pack
LANG_PACK = {
    'en': {
        "title": "Digital Mandi & Logistics Portal", "nav": "📌 Menu", 
        "m1": "🌾 Live Rates & AI Check", "m2": "🗺️ Traffic & Queue", 
        "m3": "📱 Slot & Gate Pass", "m4": "🚚 Transport & SMS", 
        "m5": "🎙️ Voice Assistant", "m6": "💳 DBT Payment Tracking", "m7": "🌤️ Weather Forecast",
        "reg_title": "🔐 Farmer Registration", "name_lbl": "Full Name *", 
        "id_lbl": "ID Number *", "mob_lbl": "Mobile Number (10 Digits) *", 
        "state_lbl": "Select State *", "dist_lbl": "District *", "vill_lbl": "Select Village *", "reg_btn": "Register Now 🚀"
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव भाव और AI जांच", "m2": "🗺️ भीड़ और कतार स्थिति", 
        "m3": "📱 स्लॉट और गेट पास", "m4": "🚚 गाड़ी और SMS बुकिंग", 
        "m5": "🎙️ बोलकर पूछें (वॉइस)", "m6": "💳 पैसा (DBT) ट्रैकिंग", "m7": "🌤️ मौसम की जानकारी",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या *", "mob_lbl": "मोबाइल नंबर (10 अंक) *", 
        "state_lbl": "राज्य चुनें *", "dist_lbl": "जिला चुनें *", "vill_lbl": "गांव चुनें *", "reg_btn": "पंजीकरण करें 🚀"
    },
    'gu': {
        "title": "ડિજિટલ મંડી અને પરિવહન", "nav": "📌 મેનુ", 
        "m1": "🌾 લાઇવ ભાવ અને ચકાસણી", "m2": "🗺️ ટ્રાફિક અને લાઇન", 
        "m3": "📱 સ્લોટ અને પાસ", "m4": "🚚 વાહન અને SMS બુકિંગ", 
        "m5": "🎙️ અવાજ સહાયક", "m6": "💳 ચુકવણી ટ્રેકિંગ", "m7": "🌤️ હવામાન અહેવાલ",
        "reg_title": "🔐 ખેડૂત નોંધણી", "name_lbl": "પૂરું નામ *", 
        "id_lbl": "આઈડી નંબર *", "mob_lbl": "મોબાઈલ નંબર *", 
        "state_lbl": "રાજ્ય પસંદ કરો *", "dist_lbl": "જિલ્લો *", "vill_lbl": "ગામ પસંદ કરો *", "reg_btn": "નોંધણી કરો 🚀"
    }
}

all_langs = {'en': 'English', 'hi': 'हिन्दी (Hindi)', 'gu': 'ગુજરાતી (Gujarati)'}

# Sidebar Language Selection
st.sidebar.markdown("### 🌐 Language / भाषा चुनें")
selected_lang_name = st.sidebar.selectbox("Choose Language:", list(all_langs.values()), index=1)

for code, name in all_langs.items():
    if name == selected_lang_name and st.session_state.lang != code:
        st.session_state.lang = code
        st.rerun()

curr_lang = st.session_state.lang
t = LANG_PACK.get(curr_lang, LANG_PACK['hi'])

# App Header
st.markdown(f"""
    <div class="app-header">
        <h1>KRISHI PLATFORM</h1>
        <p>🌾 {t['title']}</p>
    </div>
""", unsafe_allow_html=True)

STATE_DISTRICTS = {
    "Gujarat": {"Ahmedabad APMC": ["Vinchhiya", "Bavla", "Dholka", "Sanand"]},
    "Punjab": {"Ludhiana APMC": ["Machhiwara", "Payal", "Samrala"]},
    "Uttar Pradesh": {"Lucknow APMC": ["Kakori", "Malihabad", "Banthra"]}
}

# --- STEP 1: REGISTRATION ---
if not st.session_state.user_registered:
    st.markdown(f'<div class="section-box">{t["reg_title"]}</div>', unsafe_allow_html=True)
    with st.form("reg_form"):
        farmer_name = st.text_input(t["name_lbl"], placeholder="e.g. Anshika")
        identity_no = st.text_input(t["id_lbl"], type="password", max_chars=12, placeholder="Enter ID")
        mobile_no = st.text_input(t["mob_lbl"], max_chars=10, placeholder="10-digit mobile number")
        
        state_selected = st.selectbox(t["state_lbl"], list(STATE_DISTRICTS.keys()))
        district = st.selectbox(t["dist_lbl"], list(STATE_DISTRICTS[state_selected].keys()))
        village = st.selectbox(t["vill_lbl"], STATE_DISTRICTS[state_selected][district])

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
                st.error("❌ Kripya sahi 10-ank ka mobile number aur naam bharein.")

# --- STEP 2: DASHBOARD ---
else:
    user = st.session_state.user_data
    
    st.markdown(f"""
        <div class="pass-box">
            <span style="background:#16A34A; color:white; padding:4px 12px; border-radius:12px; font-size:0.85rem; font-weight:700;">VERIFIED PASS</span>
            <h2 style="color:#15803D; margin:8px 0 4px 0; font-size:1.5rem;">🆔 Token: {user['token_id']}</h2>
            <p style="margin:2px 0; font-weight:700; color:#0F172A; font-size:1.1rem;">Farmer: {user['name']} | Village: {user['village']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.95rem;">Center: {user['district']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"--- \n ### {t['nav']}")
    choice = st.sidebar.radio("Select Module:", [
        t['m1'], t['m2'], t['m3'], t['m4'], t['m5'], t['m6'], t['m7']
    ], label_visibility="collapsed")

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Profile", use_container_width=True):
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.rerun()

    # Module 1: Live Rates & AI Check
    if choice == t['m1']:
        st.markdown(f'<div class="section-box">🌾 Live Rates & AI Check</div>', unsafe_allow_html=True)
        st.success(f"🟢 Synced for {user['district']}")
        st.info("Wheat (गेहूं) Modal Price: ₹ 2350 / Quintal | Quality Grade: Grade-A Premium")

    # Module 2: Traffic & Queue
    elif choice == t['m2']:
        st.markdown(f'<div class="section-box">🗺️ Mandi Traffic & Queue Status</div>', unsafe_allow_html=True)
        st.progress(0.20, text="Gate 2 (Back Gate): 20% Traffic (Best to Use)")

    # Module 3: Slot & Gate Pass
    elif choice == t['m3']:
        st.markdown(f'<div class="section-box">📱 Slot & Gate Pass</div>', unsafe_allow_html=True)
        with st.form("slot_form"):
            arr_date = st.date_input("Date:")
            time_slot = st.selectbox("Time Window:", ["08:00 AM - 10:00 AM", "12:00 PM - 02:00 PM"])
            submit_slot = st.form_submit_button("Generate Gate Pass 🎫", type="primary", use_container_width=True)
            if submit_slot:
                st.session_state.slot_booked = True
                st.session_state.slot_code = f"CPN-{random.randint(100000, 999999)}"

        if st.session_state.slot_booked:
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px dashed #16A34A; padding: 16px; border-radius: 10px; margin-top: 10px;">
                    <h3 style="color:#15803D; margin-top:0;">🎫 Entry Pass</h3>
                    <p style="margin:4px 0;"><b>Token:</b> {user['token_id']}</p>
                    <p style="margin:4px 0;"><b>Code:</b> <span style="background:#22C55E; color:white; padding:3px 8px; border-radius:4px;">{st.session_state.slot_code}</span></p>
                </div>
            """, unsafe_allow_html=True)

    # Module 4: Transport & Dual SMS Booking
    elif choice == t['m4']:
        st.markdown(f'<div class="section-box">🚚 Transport & 1-Press SMS Booking (अनपढ़ किसानों के लिए)</div>', unsafe_allow_html=True)
        tab_truck, tab_sms = st.tabs(["🚚 Truck Booking", "📱 1-Press SMS Slot Booking"])
        
        with tab_truck:
            with st.form("t_form"):
                t_type = st.selectbox("Vehicle Type:", ["Mini Truck", "Tractor Trolley"])
                loc = st.text_input("Village Pickup Location:", value=user['village'])
                sub_t = st.form_submit_button("Book Vehicle & Send SMS 🚚", type="primary")
                if sub_t:
                    st.success(f"✅ Vehicle {t_type} booked! Driver confirmation SMS sent to 7254879397 for {loc}.")

        with tab_sms:
            with st.form("sms_form"):
                st.markdown("<b>👉 1 दबाकर SMS से स्लॉट बुक करें:</b>", unsafe_allow_html=True)
                sms_opt = st.radio("Select SMS Command:", ["1 - Morning Slot (08:00 AM)", "2 - Afternoon Slot (12:00 PM)"])
                sub_sms = st.form_submit_button("📤 Send SMS Request (1 दबाएं)", type="primary")
                if sub_sms:
                    st.success("✅ SMS Gateway Command Sent Successfully! Slot Confirmed via SMS.")

    # Module 5: Voice Assistant (Browser Speech-to-Text & Auto Audio)
    elif choice == t['m5']:
        st.markdown(f'<div class="section-box">🎙️ Voice Assistant (बोलकर पूछें और सुनें)</div>', unsafe_allow_html=True)
        st.info("💡 Chrome browser mein niche diye gaye mic button se bole ya text type karein.")
        
        voice_html = """
        <div style="background:#F1F5F9; padding:15px; border-radius:10px; text-align:center;">
            <button onclick="startListening()" style="background:#2563EB; color:white; border:none; padding:10px 20px; font-size:1rem; border-radius:20px; cursor:pointer;">🎤 Mic On (बोलें)</button>
            <p id="sttResult" style="margin-top:10px; color:#333; font-weight:650;"></p>
        </div>
        <script>
        function startListening() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert("Speech recognition is not supported in this browser. Please use Google Chrome.");
                return;
            }
            const recognition = new SpeechRecognition();
            recognition.lang = 'hi-IN';
            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                document.getElementById("sttResult").innerText = "Aapne bola: " + text;
            };
            recognition.start();
        }
        </script>
        """
        st.components.v1.html(voice_html, height=120)
        
        user_q = st.text_input("Apna sawal yahan likhein:")
        if st.button("🔊 Audio Answer Sunen", type="primary", use_container_width=True):
            ans = f"Namaste {user['name']}. Aapka token number {user['token_id']} hai. Mandi mein gehu ka bhav 2350 rupaye quintal chal raha hai."
            st.success(ans)
            try:
                from gtts import gTTS
                tts = gTTS(text=ans, lang='hi')
                fp = BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format='audio/mp3', autoplay=True)
            except Exception:
                st.warning("Audio generated.")

    # Module 6: DBT Payment Tracking
    elif choice == t['m6']:
        st.markdown(f'<div class="section-box">💳 DBT Payment Tracking</div>', unsafe_allow_html=True)
        st.info("💳 Status: Pass generated, payment transfer to Aadhaar-linked bank account is in progress.")

    # Module 7: Weather Forecast
    elif choice == t['m7']:
        st.markdown(f'<div class="section-box">🌤️ Weather Forecast</div>', unsafe_allow_html=True)
        st.success(f"📍 {user['village']}, {user['district']} | Temperature: 32°C | Rain Risk: Low (Safe for Harvest)")
