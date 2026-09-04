import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
from urllib.parse import quote as url_encode

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Pan-India Ecosystem", 
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
    .feature-box.red { border-left-color: #DC2626; background: #FEF2F2; }

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

# Pan-India Multilingual Dictionary
LANG_DICT = {
    'en': {
        "title": "Pan-India Digital Mandi & Procurement Ecosystem",
        "nav_title": "📌 Unified Navigation Menu",
        "m1": "🌾 1. Live Rates & AI Quality",
        "m2": "🗺️ 2. Real-Time Queue & Traffic",
        "m3": "📱 3. Slot Booking & Gate Pass",
        "m4": "🎙️ 4. Voice-to-Voice Assistant",
        "m5": "🔔 5. Smart Traffic Notifications",
        "m6": "💳 6. Track Procurement & DBT Payments",
        "logout": "Change Language / Reset"
    },
    'hi': {
        "title": "अखिल भारतीय डिजिटल मंडी एवं खरीद तंत्र",
        "nav_title": "📌 एकीकृत नेविगेशन मेनू",
        "m1": "🌾 1. लाइव भाव एवं AI गुणवत्ता",
        "m2": "🗺️ 2. रियल-टाइम कतार और ट्रैफिक",
        "m3": "📱 3. स्लॉट बुकिंग एवं गेट पास",
        "m4": "🎙️ 4. वॉइस-टू-वॉइस आवाज़ सहायक",
        "m5": "🔔 5. स्मार्ट ट्रैफिक नोटिफिकेशन",
        "m6": "💳 6. खरीद ट्रैकिंग एवं DBT भुगतान",
        "logout": "भाषा बदलें / रीसेट करें"
    },
    'pa': {
        "title": "ਪാൻ-ਇੰਡੀਆ ਡਿਜੀਟਲ ਮੰਡੀ ਅਤੇ ਖਰੀਦ ਪੋਰਟਲ",
        "nav_title": "📌 ਨੈਵੀਗੇਸ਼ਨ ਮੀਨੂ",
        "m1": "🌾 1. ਲਾਈਵ ਭਾਅ ਅਤੇ AI ਗੁਣਵੱਤਾ",
        "m2": "🗺️ 2. ਰੀਅਲ-ਟਾਈਮ ਕਤਾਰ ਅਤੇ ਟ੍ਰੈਫਿਕ",
        "m3": "📱 3. ਸਮਾਂ ਸਲਾਟ ਅਤੇ ਪਾਸ",
        "m4": "🎙️ 4. ਬੋਲਣ ਵਾਲਾ ਆਵਾਜ਼ ਸਹਾਇਕ",
        "m5": "🔔 5. ਸਮਾਰਟ ਟਰੈਫਿਕ ਸੂਚਨਾ",
        "m6": "💳 6. ਖਰੀਦ ਟਰੈਕਿੰਗ ਅਤੇ ਭੁਗਤਾਨ",
        "logout": "ਭਾਸ਼ਾ ਬਦلو / ਰੀਸੈਟ"
    },
    'mr': {
        "title": "अखिल भारतीय डिजिटल बाजार आणि खरेदी प्लॅटफॉर्म",
        "nav_title": "📌 मेनू सूची",
        "m1": "🌾 1. थेट भाव आणि गुणवत्ता",
        "m2": "🗺️ 2. लाईव्ह क्यु आणि ट्रॅफिक",
        "m3": "📱 3. स्लॉट बुकिंग आणि पास",
        "m4": "🎙️ 4. व्हॉइस असिस्टंट",
        "m5": "🔔 5. स्मार्ट ट्रॅफिक सूचना",
        "m6": "💳 6. खरेदी आणि पेमेंट ट्रॅकिंग",
        "logout": "भाषा बदला / रीसेट"
    },
    'bn': {
        "title": "সর্বভারতীয় ডিজিটাল মান্ডি এবং সংগ্রহ প্ল্যাটফর্ম",
        "nav_title": "📌 মেনু তালিকা",
        "m1": "🌾 1. লাইভ দর ও গুণমান",
        "m2": "🗺️ 2. লাইভ কিউ এবং ট্রাফিক",
        "m3": "📱 3. স্লট বুকিং এবং পাস",
        "m4": "🎙️ 4. ভয়েস সহকারী",
        "m5": "🔔 5. স্মার্ট ট্রাফিক নোটিফিকেশন",
        "m6": "💳 6. সংগ্রহ ও পেমেন্ট ট্র্যাকিং",
        "logout": "ভাষা পরিবর্তন করুন"
    },
    'te': {
        "title": "అఖిల భారత డిజిటల్ మార్కెట్ మరియు సేకరణ ప్లాట్‌ఫారమ్",
        "nav_title": "📌 నావిగేషన్ మెను",
        "m1": "🌾 1. లైవ్ ధరలు & నాణ్యత",
        "m2": "🗺️ 2. క్యూ మరియు ట్రాఫిక్",
        "m3": "📱 3. స్లాట్ బుకింగ్ మరియు పాస్",
        "m4": "🎙️ 4. వాయిస్ అసిస్టెంట్",
        "m5": "🔔 5. ట్రాఫిక్ నోటిఫికేషన్",
        "m6": "💳 6. సేకరణ & చెల్లింపు స్థితి",
        "logout": "భాష మార్చండి"
    }
}

curr_lang = st.session_state.lang
t = LANG_DICT.get(curr_lang, LANG_DICT['en'])

# Top Header
st.markdown(f"""
    <div class="app-bar">
        <h1>KRISHI PLATFORM</h1>
        <p>🌾 {t['title']}</p>
    </div>
""", unsafe_allow_html=True)

# ================= PAGE 1: ALL-INDIA LANGUAGE SELECTOR =================
if not st.session_state.lang_selected:
    st.markdown("### 🌐 Select Your Language / अपनी भाषा चुनें / ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ")
    st.info("Choose your preferred regional language to access live Mandi data across any state in India.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🇮🇳 English", use_container_width=True):
            st.session_state.lang = 'en'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 मराठी (Marathi)", use_container_width=True):
            st.session_state.lang = 'mr'; st.session_state.lang_selected = True; st.rerun()
    with col2:
        if st.button("🇮🇳 हिंदी (Hindi)", use_container_width=True):
            st.session_state.lang = 'hi'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 বাংলা (Bengali)", use_container_width=True):
            st.session_state.lang = 'bn'; st.session_state.lang_selected = True; st.rerun()
    with col3:
        if st.button("🇮🇳 ਪੰਜਾਬੀ (Punjabi)", use_container_width=True):
            st.session_state.lang = 'pa'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 తెలుగు (Telugu)", use_container_width=True):
            st.session_state.lang = 'te'; st.session_state.lang_selected = True; st.rerun()

# ================= PAGE 2: FARMER REGISTRATION VIA IDENTITY NUMBER =================
elif not st.session_state.user_registered:
    st.markdown('<div class="section-title">🔐 Page 2: Farmer Registration via Identity Card & Pan-India Mandi Location</div>', unsafe_allow_html=True)
    st.info("Please enter your official identification details and farming location to register securely.")
    
    with st.form("reg_form"):
        farmer_name = st.text_input("Farmer Full Name *", placeholder="e.g. Rajesh Kumar")
        identity_no = st.text_input("Identification Card Number (12 Digits) *", type="password", max_chars=12, placeholder="Enter official verification number")
        mobile_no = st.text_input("Mobile Number (10 Digits) *", max_chars=10)
        
        all_states = [
            "Haryana", "Punjab", "Uttar Pradesh", "Madhya Pradesh", "Maharashtra", 
            "Rajasthan", "Bihar", "Gujarat", "Andhra Pradesh", "Telangana", 
            "West Bengal", "Karnataka", "Odisha", "Chhattisgarh"
        ]
        state_selected = st.selectbox("Select State *", all_states)
        district = st.text_input("District / Mandi Region *", placeholder="e.g. Karnal / Ludhiana / Nashik / Patna")

        submit_reg = st.form_submit_button("Register & Generate Pass 🎫", use_container_width=True, type="primary")

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
                st.error("❌ Please provide a valid 12-digit verification number, 10-digit mobile number, name, and district.")

# ================= PAGES 3 TO 7 & DASHBOARD =================
else:
    user = st.session_state.user_data
    
    # Verified Pass Card
    st.markdown(f"""
        <div class="pass-card">
            <span class="badge">PAN-INDIA VERIFIED GATE PASS • {user['state'].upper()}</span>
            <h2>🆔 {user['token_id']}</h2>
            <p style="margin:4px 0; font-weight:700; color:#0F172A;">Farmer: {user['name']} | Region: {user['district']}, {user['state']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.88rem;">Mobile: {user['mobile']} | ID Reference: {user['id_masked']}</p>
        </div>
    """, unsafe_allow_html=True)

    # WhatsApp Share Option
    wa_msg = f"Hello {user['name']}, your Pan-India Mandi Token is *{user['token_id']}* for {user['district']} Mandi ({user['state']})."
    wa_link = f"https://wa.me/91{user['mobile']}?text={url_encode(wa_msg)}"
    st.markdown(f"""
        <a href="{wa_link}" target="_blank" style="text-decoration:none;">
            <div style="background:#25D366; color:white; padding:12px; border-radius:12px; text-align:center; font-weight:700; margin-bottom:20px;">
                💬 Send Token Pass via WhatsApp 📱
            </div>
        </a>
    """, unsafe_allow_html=True)

    if st.button("🌐 " + t["logout"]):
        st.session_state.lang_selected = False
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.rerun()

    # Sidebar Navigation for all features
    st.sidebar.title(t['nav_title'])
    choice = st.sidebar.radio("Select Service:", [
        t['m1'],
        t['m2'],
        t['m3'],
        t['m4'],
        t['m5'],
        t['m6']
    ])

    # 1. LIVE RATES & AI QUALITY
    if choice == t['m1']:
        st.markdown(f'<div class="section-title">🌾 Live APMC Mandi Rates for {user["district"]}, {user["state"]}</div>', unsafe_allow_html=True)
        st.info(f"📡 Real-time data connected for **{user['district']}**, **{user['state']}** marketplace.")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Primary Grain", "₹ 2,275 / Qtl", "Wheat (Live)")
        c2.metric("Secondary APMC", "₹ 2,183 / Qtl", "Paddy / Rice")
        c3.metric("Cooperative Hub", "₹ 5,440 / Qtl", "Pulses")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">🤖 AI Crop Quality & Price Estimator</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            crop = st.selectbox("Select Crop:", ["Wheat", "Paddy", "Pulses"])
            moisture = st.slider("Moisture Content (%):", 5.0, 25.0, 11.5)
        with col2:
            broken = st.slider("Broken Grains / Foreign Matter (%):", 0.0, 10.0, 1.0)
            base = 2275 if crop=="Wheat" else (2183 if crop=="Paddy" else 5440)
            adj = 90 if moisture <= 12.0 else -100
            st.success(f"**Computed Local Market Value:** ₹ {base + adj} / Quintal")

    # 2. REAL-TIME QUEUE & TRAFFIC
    elif choice == t['m2']:
        st.markdown(f'<div class="section-title">🗺️ Real-Time Queue & Gate Traffic ({user["district"]}, {user["state"]})</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box orange">
                <h4 style="margin:0 0 8px 0; color:#B45309;">🚨 Live Mandi Congestion Heatmap</h4>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gate 1 (Main Entry)", "88%", delta="Heavy Queue", delta_color="inverse")
        c2.metric("Gate 2 (Express Lane)", "34%", delta="Smooth Flow", delta_color="normal")
        c3.metric("Weighbridge Bay", "92%", delta="Near Capacity", delta_color="inverse")
        
        st.warning(f"⚠️ **Advisory:** Gate 1 in {user['district']} mandi has heavy traffic right now. Please use Gate 2 for faster entry.")

    # 3. SLOT BOOKING & GATE PASS
    elif choice == t['m3']:
        st.markdown(f'<div class="section-title">📱 Page 3: Arrival Slot Booking & Gate Pass Generation</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">📅 Book Mandi Unloading Slot</h4>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("slot_form"):
            st.date_input("Select Arrival Date:")
            st.selectbox("Select Time Window:", ["08:00 AM - 10:00 AM", "11:00 AM - 01:00 PM", "03:00 PM - 05:00 PM"])
            if st.form_submit_button("Confirm & Sync Pass 🎫", type="primary", use_container_width=True):
                st.success(f"Slot successfully booked for Token `{user['token_id']}` at {user['district']} Mandi!")

    # 4. VOICE-TO-VOICE ASSISTANT (Voice Chat simulation with Audio Reply)
    elif choice == t['m4']:
        st.markdown(f'<div class="section-title">🎙️ Page 5: Voice-to-Voice Local Language Assistant</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4 style="margin:0 0 8px 0; color:#1E3A8A;">🗣️ Speak or Ask Question & Get Audio Reply</h4>
            </div>
        """, unsafe_allow_html=True)
        
        queries = {
            'en': ["What is today's live wheat price?", "Which gate has less traffic?", "When will I get my payment?"],
            'hi': ["आज गेहूं का लाइव भाव क्या है?", "किस गेट पर कम भीड़ है?", "मेरे पैसे कब आएंगे?"],
            'pa': ["ਅੱਜ ਕਣਕ ਦਾ ਭਾਅ ਕੀ ਹੈ?", "ਕਿਹੜੇ ਗੇਟ 'ਤੇ ਘੱਟ ਭੀੜ ਹੈ?", "ਪੈਸੇ ਕਦੋਂ ਆਉਣਗੇ?"],
            'mr': ["आजचा गव्हाचा भाव काय आहे?", "कोणत्या गेटवर गर्दी कमी आहे?", "पैसे कधी जमा होतील?"],
            'bn': ["আজ গমের দাম কত?", "কোন গেটে কম ভিড় আছে?", "টাকা কবে আসবে?"],
            'te': ["నేటి గోధుమల ధర ఎంత?", "ఏ గేట్ వద్ద రద్దీ తక్కువగా ఉంది?", "డబ్బు ఎప్పుడు వస్తుంది?"]
        }
        
        q_list = queries.get(curr_lang, queries['en'])
        selected_q = st.selectbox("🎙️ Select Your Voice Query:", q_list)
        
        if st.button("🔊 Speak & Play Voice Reply", type="primary", use_container_width=True):
            if "price" in selected_q.lower() or "भाव" in selected_q or "ਭਾਅ" in selected_q or "भाव" in selected_q or "দাম" in selected_q or "ధర" in selected_q:
                ans = f"Live wheat price in {user['district']} is 2,275 rupees per quintal." if curr_lang=='en' else (f"{user['district']} में गेहूं का लाइव भाव 2,275 रुपये प्रति क्विंटल है।" if curr_lang=='hi' else f"{user['district']} ਵਿੱਚ ਕਣਕ ਦਾ ਲਾਈਵ ਭਾਅ 2,275 ਰੁਪਏ ਹੈ।")
            elif "gate" in selected_q.lower() or "गेट" in selected_q or "ਗੇਟ" in selected_q or "गेट" in selected_q or "গেট" in selected_q or "గేట్" in selected_q:
                ans = "Gate 2 has smooth traffic flow, please use Gate 2." if curr_lang=='en' else ("गेट 2 पर ट्रैफिक साफ है, कृपया गेट 2 का उपयोग करें।" if curr_lang=='hi' else "ਗੇਟ 2 'ਤੇ ਟ੍ਰੈਫਿਕ ਸਾਫ਼ ਹੈ।")
            else:
                ans = "Your payment will be credited via direct transfer within 48 hours after crop weighing." if curr_lang=='en' else ("तौल होने के बाद 48 घंटों के भीतर आपका भुगतान आपके खाते में आ जाएगा।" if curr_lang=='hi' else "ਤੋਲਣ ਤੋਂ ਬਾਅਦ 48 ਘੰਟਿਆਂ ਵਿੱਚ ਪੈਸੇ ਆ ਜਾਣਗੇ।")
            
            st.success(f"**Assistant Reply:** {ans}")
            
            # Safe gTTS audio generation
            try:
                tts_lang_map = {'en': 'en', 'hi': 'hi', 'pa': 'hi', 'mr': 'mr', 'bn': 'bn', 'te': 'te'}
                tts = gTTS(text=ans, lang=tts_lang_map.get(curr_lang, 'en'))
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                st.error("Audio generation service warning.")

    # 5. SMART TRAFFIC NOTIFICATIONS (Automatic delay alert)
    elif choice == t['m5']:
        st.markdown(f'<div class="section-title">🔔 Page 7: Smart Traffic & Gate Delay Notifications</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box red">
                <h4 style="margin:0 0 8px 0; color:#DC2626;">🚨 Live Push Alert System (Automated)</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.error(f"🚨 **Automated Alert for Token `{user['token_id']}`:** Heavy congestion detected at {user['district']} Mandi gate right now!")
        st.warning("⏱️ **Action Required:** Please delay your arrival by **10 minutes** to avoid waiting in the queue. Your slot is safe.")

    # 6. TRACK PROCUREMENT & PAYMENT STATUS
    elif choice == t['m6']:
        st.markdown(f'<div class="section-title">💳 Page 6: Track Procurement & Payment Status</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-box green">
                <h4 style="margin:0 0 8px 0; color:#15803D;">📦 Live Procurement Status for {user['district']} Mandi</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        - **Token Generation:** ✅ Completed (`Active`)
        - **Gate Entry & Weighing:** ⏳ Scheduled Today
        - **Moisture & Quality Test:** ⏳ Pending at Bay 2
        - **Procurement Slip:** 📄 Will be generated after weighing
        """)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-box">
                <h4 style="margin:0 0 8px 0; color:#1E3A8A;">💰 Direct Bank Transfer Details</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.success("💳 **Expected Payout:** ₹ 1,02,375 will be credited directly to your verified bank account within **48 hours** after successful crop procurement.")
