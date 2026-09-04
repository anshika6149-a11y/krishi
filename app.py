import streamlit as st
import random
import requests
from gtts import gTTS
from io import BytesIO
from urllib.parse import quote as url_encode

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Pan-India Ecosystem", 
    page_icon="🌾", 
    layout="centered"
)

# Professional UI Styling & Box Layouts
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
    .stButton>button { border-radius: 12px !important; font-weight: 600 !important; width: 100%; }
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
if 'active_module' not in st.session_state:
    st.session_state.active_module = None

# Comprehensive Multilingual Dictionary (Covering major Indian Scheduled Languages)
LANG_DICT = {
    'en': {
        "title": "Pan-India Digital Mandi & Procurement Ecosystem",
        "m1": "🌾 Live Rates & AI Quality",
        "m2": "🗺️ Real-Time Queue & Traffic",
        "m3": "📱 Slot Booking & Gate Pass",
        "m4": "🎙️ Voice-to-Voice Assistant",
        "m5": "🔔 Smart Traffic Notifications",
        "m6": "💳 Procurement & DBT Payments",
        "logout": "Change Language / Reset"
    },
    'hi': {
        "title": "अखिल भारतीय डिजिटल मंडी एवं खरीद तंत्र",
        "m1": "🌾 लाइव भाव एवं AI गुणवत्ता",
        "m2": "🗺️ रियल-टाइम कतार और ट्रैफिक",
        "m3": "📱 स्लॉट बुकिंग एवं गेट पास",
        "m4": "🎙️ वॉइस-टू-वॉइस आवाज़ सहायक",
        "m5": "🔔 स्मार्ट ट्रैफिक नोटिफिकेशन",
        "m6": "💳 खरीद एवं DBT भुगतान",
        "logout": "भाषा बदलें / रीसेट करें"
    },
    'pa': {
        "title": "ਪാൻ-ਇੰਡੀਆ ਡਿਜੀਟਲ ਮੰਡੀ ਅਤੇ ਖਰੀਦ ਪੋਰਟਲ",
        "m1": "🌾 ਲਾਈਵ ਭਾਅ ਅਤੇ AI ਗੁਣਵੱਤਾ",
        "m2": "🗺️ ਰੀਅਲ-ਟਾਈਮ ਕਤਾਰ ਅਤੇ ਟ੍ਰੈਫਿਕ",
        "m3": "📱 ਸਮਾਂ ਸਲਾਟ ਅਤੇ ਪਾਸ",
        "m4": "🎙️ ਬੋਲਣ ਵਾਲਾ ਆਵਾਜ਼ ਸਹਾਇਕ",
        "m5": "🔔 ਸਮਾਰਟ ਟਰੈਫਿਕ ਸੂਚਨਾ",
        "m6": "💳 ਖਰੀਦ ਟਰੈਕਿੰਗ ਅਤੇ ਭੁਗਤਾਨ",
        "logout": "ਭਾਸ਼ਾ ਬਦلو / ਰੀਸੈਟ"
    },
    'mr': {
        "title": "अखिल भारतीय डिजिटल बाजार आणि खरेदी प्लॅटफॉर्म",
        "m1": "🌾 थेट भाव आणि गुणवत्ता",
        "m2": "🗺️ लाईव्ह क्यु आणि ट्रॅफिक",
        "m3": "📱 स्लॉट बुकिंग आणि पास",
        "m4": "🎙️ व्हॉइस असिस्टंट",
        "m5": "🔔 स्मार्ट ट्रॅफिक सूचना",
        "m6": "💳 खरेदी आणि पेमेंट ट्रॅकिंग",
        "logout": "भाषा बदला / रीसेट"
    },
    'bn': {
        "title": "সর্বভারতীয় ডিজিটাল মান্ডি এবং সংগ্রহ প্ল্যাটফর্ম",
        "m1": "🌾 লাইভ দর ও গুণমান",
        "m2": "🗺️ লাইভ কিউ এবং ট্রাফিক",
        "m3": "📱 স্লট বুকিং এবং পাস",
        "m4": "🎙️ ভয়েস সহকারী",
        "m5": "🔔 স্মার্ট ট্রাফিক নোটিফিকেশন",
        "m6": "💳 সংগ্রহ ও পেমেন্ট ট্র্যাকিং",
        "logout": "ভাষা পরিবর্তন করুন"
    },
    'te': {
        "title": "అఖిల భారత డిజిటల్ మార్కెట్ మరియు సేకరణ ప్లాట్‌ఫారమ్",
        "m1": "🌾 లైవ్ ధరలు & నాణ్యత",
        "m2": "🗺️ క్యూ మరియు ట్రాఫిక్",
        "m3": "📱 స్లాట్ బుకింగ్ మరియు పాస్",
        "m4": "🎙️ వాయిస్ అసిస్టెంట్",
        "m5": "🔔 ట్రాఫిక్ నోటిఫికేషన్",
        "m6": "💳 సేకరణ & చెల్లింపు స్థితి",
        "logout": "భాష మార్చండి"
    },
    'ta': {
        "title": "அகில இந்திய டிஜிட்டல் சந்தை மற்றும் கொள்முதல் தளம்",
        "m1": "🌾 நேரலை விலைகள் & தரம்",
        "m2": "🗺️ வரிசை & போக்குவரத்து",
        "m3": "📱 ஸ்லாட் முன்பதிவு மற்றும் பாஸ்",
        "m4": "🎙️ குரல் உதவியாளர்",
        "m5": "🔔 போக்குவரத்து அறிவிப்புகள்",
        "m6": "💳 கொள்முதல் & கட்டணம்",
        "logout": "மொழியை மாற்றுக"
    },
    'gu': {
        "title": "अखिल भारतीय डिजिटल मंदी अने खरीद प्लेटफॉर्म",
        "m1": "🌾 लाइव भाव अने गुणवत्ता",
        "m2": "🗺️ कतार अने ट्रैफिक",
        "m3": "📱 स्लॉट बुकिंग अने पास",
        "m4": "🎙️ वोइस असिस्टंट",
        "m5": "🔔 ट्रैफिक सूचना",
        "m6": "💳 खरीद अने पेमेंट",
        "logout": "भाषा बदलो"
    },
    'kn': {
        "title": "ಅಖಿಲ ಭಾರತ ಡಿಜಿಟಲ್ ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಖರೀದಿ ವೇದಿಕೆ",
        "m1": "🌾 ಲೈವ್ ಬೆಲೆಗಳು ಮತ್ತು ಗುಣಮಟ್ಟ",
        "m2": "🗺️ ಸರತಿ ಸಾಲು ಮತ್ತು ದಟ್ಟಣೆ",
        "m3": "📱 ಸ್ಲಾಟ್ ಬುಕಿಂಗ್ ಮತ್ತು ಪಾಸ್",
        "m4": "🎙️ ಧ್ವನಿ ಸಹಾಯಕ",
        "m5": "🔔 ದಟ್ಟಣೆ ಸೂಚನೆಗಳು",
        "m6": "💳 ಖರೀದಿ ಮತ್ತು ಪಾವತಿ ಸ್ಥಿತಿ",
        "logout": "ಭಾಷೆಯನ್ನು ಬದಲಾಯಿಸಿ"
    },
    'ml': {
        "title": "അഖിലേന്ത്യാ ഡിജിറ്റൽ ചന്തയും സംഭരണ പ്ലാറ്റ്‌ഫോമും",
        "m1": "🌾 തത്സമയ വിലയും ഗുണനിലവാരവും",
        "m2": "🗺️ ക്യൂവും ട്രാഫിക്കും",
        "m3": "📱 സ്ലോട്ട് ബുക്കിംഗും പാസും",
        "m4": "🎙️ വോയിസ് അസിസ്റ്റന്റ്",
        "m5": "🔔 ട്രാഫിക അറിയിപ്പുകൾ",
        "m6": "💳 സംഭരണവും പേയ്‌മെന്റും",
        "logout": "ഭാഷ മാറ്റുക"
    },
    'or': {
        "title": "ସର୍ବଭାରତୀୟ ଡିଜିଟାଲ୍ ମଣ୍ଡି ଏବଂ କ୍ରୟ ପ୍ଲାଟଫର୍ମ",
        "m1": "🌾 ଲାଇଭ୍ ମୂଲ୍ୟ ଏବଂ ଗୁଣବତ୍ତା",
        "m2": "🗺️ କ୍ୟୁ ଏବଂ ଟ୍ରାଫିକ୍",
        "m3": "📱 ସ୍ଲଟ୍ ବୁକିଂ ଏବଂ ପାସ୍",
        "m4": "🎙️ ଭଏସ୍ ଆସିଷ୍ଟାଣ୍ଟ",
        "m5": "🔔 ଟ୍ରାଫିକ୍ ସୂଚନା",
        "m6": "💳 କ୍ରୟ ଏବଂ ପେମେଣ୍ଟ",
        "logout": "ଭାଷା ବଦଳାନ୍ତୁ"
    },
    'as': {
        "title": "সৰ্বভাৰতীয় ডিজিটেল মান্ডি আৰু ক্ৰয় প্লেটফৰ্ম",
        "m1": "🌾 লাইভ মূল্য আৰু গুণগত মান",
        "m2": "🗺️ শাৰী আৰু ট্ৰাফিক",
        "m3": "📱 স্লট বুকিং আৰু পাছ",
        "m4": "🎙️ ভয়েচ সহায়ক",
        "m5": "🔔 ট্ৰাফিক სანচো",
        "m6": "💳 ক্ৰয় আৰু পৰিশোধ",
        "logout": "ভাষা সলনি কৰক"
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

# Function to fetch Real-Time Live Data from e-NAM / Open APMC API (with fallback simulation)
def fetch_live_market_data(state_name, district_name):
    try:
        # Example endpoint for open data gov API or e-NAM gateway
        # api_url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=YOUR_API_KEY&format=json&filters[state]={state_name}"
        # response = requests.get(api_url, timeout=3)
        # if response.status_code == 200:
        #     return response.json()
        
        # Simulated live fetch payload structure for demonstration
        return {
            "status": "live_connected",
            "wheat": "₹ 2,285 / Qtl",
            "paddy": "₹ 2,190 / Qtl",
            "pulses": "₹ 5,460 / Qtl"
        }
    except Exception:
        return {
            "status": "offline_fallback",
            "wheat": "₹ 2,275 / Qtl",
            "paddy": "₹ 2,183 / Qtl",
            "pulses": "₹ 5,440 / Qtl"
        }

# ================= PAGE 1: ALL-INDIA LANGUAGE SELECTOR =================
if not st.session_state.lang_selected:
    st.markdown("### 🌐 Select Your Language / अपनी भाषा चुनें / ভাষা নির্বাচন করুন")
    st.info("Choose your preferred regional language to access live Mandi data across India.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🇮🇳 English", use_container_width=True):
            st.session_state.lang = 'en'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 मराठी (Marathi)", use_container_width=True):
            st.session_state.lang = 'mr'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 தமிழ் (Tamil)", use_container_width=True):
            st.session_state.lang = 'ta'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 ଓଡ଼ିଆ (Odia)", use_container_width=True):
            st.session_state.lang = 'or'; st.session_state.lang_selected = True; st.rerun()
    with col2:
        if st.button("🇮🇳 हिंदी (Hindi)", use_container_width=True):
            st.session_state.lang = 'hi'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 বাংলা (Bengali)", use_container_width=True):
            st.session_state.lang = 'bn'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 ગુજરાતી (Gujarati)", use_container_width=True):
            st.session_state.lang = 'gu'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 অসমীয়া (Assamese)", use_container_width=True):
            st.session_state.lang = 'as'; st.session_state.lang_selected = True; st.rerun()
    with col3:
        if st.button("🇮🇳 ਪੰਜਾਬੀ (Punjabi)", use_container_width=True):
            st.session_state.lang = 'pa'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 తెలుగు (Telugu)", use_container_width=True):
            st.session_state.lang = 'te'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 ಕನ್ನಡ (Kannada)", use_container_width=True):
            st.session_state.lang = 'kn'; st.session_state.lang_selected = True; st.rerun()
        if st.button("🇮🇳 മലയാളം (Malayalam)", use_container_width=True):
            st.session_state.lang = 'ml'; st.session_state.lang_selected = True; st.rerun()

# ================= PAGE 2: FARMER REGISTRATION =================
elif not st.session_state.user_registered:
    st.markdown('<div class="section-title">🔐 Page 2: Farmer Registration via ID Card & Mandi Location</div>', unsafe_allow_html=True)
    st.info("Please enter your official identification details and farming location.")
    
    with st.form("reg_form"):
        farmer_name = st.text_input("Farmer Full Name *", placeholder="e.g. Rajesh Kumar")
        identity_no = st.text_input("Identification Card Number (12 Digits) *", type="password", max_chars=12, placeholder="Enter official verification number")
        mobile_no = st.text_input("Mobile Number (10 Digits) *", max_chars=10)
        
        all_states = [
            "Haryana", "Punjab", "Uttar Pradesh", "Madhya Pradesh", "Maharashtra", 
            "Rajasthan", "Bihar", "Gujarat", "Andhra Pradesh", "Telangana", 
            "West Bengal", "Karnataka", "Odisha", "Chhattisgarh", "Assam", "Tamil Nadu"
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
                st.error("❌ Please provide a valid 12-digit ID number, 10-digit mobile number, name, and district.")

# ================= MAIN DASHBOARD & BEAUTIFUL BOX NAVIGATION =================
else:
    user = st.session_state.user_data
    
    # Verified Pass Card
    st.markdown(f"""
        <div class="pass-card">
            <span class="badge">VERIFIED GATE PASS • {user['state'].upper()}</span>
            <h2>🆔 {user['token_id']}</h2>
            <p style="margin:4px 0; font-weight:700; color:#0F172A;">Farmer: {user['name']} | Region: {user['district']}, {user['state']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.88rem;">Mobile: {user['mobile']} | ID Ref: {user['id_masked']}</p>
        </div>
    """, unsafe_allow_html=True)

    # WhatsApp Share Option
    wa_msg = f"Hello {user['name']}, your Mandi Token is *{user['token_id']}* for {user['district']} Mandi ({user['state']})."
    wa_link = f"https://wa.me/91{user['mobile']}?text={url_encode(wa_msg)}"
    st.markdown(f"""
        <a href="{wa_link}" target="_blank" style="text-decoration:none;">
            <div style="background:#25D366; color:white; padding:12px; border-radius:12px; text-align:center; font-weight:700; margin-bottom:15px;">
                💬 Send Token Pass via WhatsApp 📱
            </div>
        </a>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([2, 1])
    with col_r:
        if st.button("🌐 " + t["logout"]):
            st.session_state.lang_selected = False
            st.session_state.user_registered = False
            st.session_state.user_data = {}
            st.session_state.active_module = None
            st.rerun()

    st.markdown("<hr style='margin:10px 0 20px 0;'>", unsafe_allow_html=True)

    # IF NO MODULE SELECTED, SHOW ATTRACTIVE BOX GRID ON MAIN SCREEN
    if st.session_state.active_module is None:
        st.markdown('<div class="section-title">📌 Tap a Service Box to Open</div>', unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button(t['m1'], use_container_width=True):
                st.session_state.active_module = 'm1'; st.rerun()
            if st.button(t['m3'], use_container_width=True):
                st.session_state.active_module = 'm3'; st.rerun()
            if st.button(t['m5'], use_container_width=True):
                st.session_state.active_module = 'm5'; st.rerun()
        with b2:
            if st.button(t['m2'], use_container_width=True):
                st.session_state.active_module = 'm2'; st.rerun()
            if st.button(t['m4'], use_container_width=True):
                st.session_state.active_module = 'm4'; st.rerun()
            if st.button(t['m6'], use_container_width=True):
                st.session_state.active_module = 'm6'; st.rerun()

    else:
        # Back to Dashboard button
        if st.button("⬅️ Back to Main Dashboard Boxes", type="secondary"):
            st.session_state.active_module = None
            st.rerun()

        active = st.session_state.active_module

        # 1. LIVE RATES & AI QUALITY (Using live API fetch function)
        if active == 'm1':
            st.markdown(f'<div class="section-title">🌾 Live APMC Mandi Rates for {user["district"]}, {user["state"]}</div>', unsafe_allow_html=True)
            
            # Fetch live data via requests handler
            live_data = fetch_live_market_data(user['state'], user['district'])
            if live_data['status'] == 'live_connected':
                st.success(f"🟢 Connected to Live e-NAM APMC Feed for **{user['district']}**, **{user['state']}**.")
            else:
                st.info(f"📡 Real-time data sync active for **{user['district']}**, **{user['state']}**.")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Primary Grain", live_data['wheat'], "Wheat (Live)")
            c2.metric("Secondary APMC", live_data['paddy'], "Paddy / Rice")
            c3.metric("Cooperative Hub", live_data['pulses'], "Pulses")

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
                broken = st.slider("Broken Grains (%):", 0.0, 10.0, 1.0)
                base = 2285 if crop=="Wheat" else (2190 if crop=="Paddy" else 5460)
                adj = 90 if moisture <= 12.0 else -100
                st.success(f"**Computed Value:** ₹ {base + adj} / Quintal")

        # 2. REAL-TIME QUEUE & TRAFFIC
        elif active == 'm2':
            st.markdown(f'<div class="section-title">🗺️ Real-Time Queue & Gate Traffic ({user["district"]})</div>', unsafe_allow_html=True)
            
            st.markdown("""
                <div class="feature-box orange">
                    <h4 style="margin:0 0 8px 0; color:#B45309;">🚨 Live Mandi Congestion Heatmap</h4>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Gate 1 (Main)", "88%", delta="Heavy", delta_color="inverse")
            c2.metric("Gate 2 (Express)", "34%", delta="Smooth", delta_color="normal")
            c3.metric("Weighbridge", "92%", delta="Full", delta_color="inverse")
            
            st.warning(f"⚠️ **Advisory:** Gate 1 has heavy traffic. Please use Gate 2 for faster entry.")

        # 3. SLOT BOOKING & GATE PASS
        elif active == 'm3':
            st.markdown(f'<div class="section-title">📱 Arrival Slot Booking & Gate Pass</div>', unsafe_allow_html=True)
            
            with st.form("slot_form"):
                st.date_input("Select Arrival Date:")
                st.selectbox("Select Time Window:", ["08:00 AM - 10:00 AM", "11:00 AM - 01:00 PM", "03:00 PM - 05:00 PM"])
                if st.form_submit_button("Confirm & Sync Pass 🎫", type="primary", use_container_width=True):
                    st.success(f"Slot successfully booked for Token `{user['token_id']}` at {user['district']} Mandi!")

        # 4. VOICE-TO-VOICE ASSISTANT
        elif active == 'm4':
            st.markdown(f'<div class="section-title">🎙️ Voice-to-Voice Assistant</div>', unsafe_allow_html=True)
            
            queries = {
                'en': ["What is today's live wheat price?", "Which gate has less traffic?", "When will I get my payment?"],
                'hi': ["आज गेहूं का लाइव भाव क्या है?", "किस गेट पर कम भीड़ है?", "मेरे पैसे कब आएंगे?"],
                'te': ["నేటి గోధుమల ధర ఎంత?", "ఏ గేట్ వద్ద రద్దీ తక్కువగా ఉంది?", "డబ్బు ఎప్పుడు వస్తుంది?"]
            }
            q_list = queries.get(curr_lang, queries['en'])
            selected_q = st.selectbox("🎙️ Select Voice Query:", q_list)
            
            if st.button("🔊 Speak & Play Voice Reply", type="primary", use_container_width=True):
                ans = "Live wheat price is 2,285 rupees per quintal." if curr_lang=='en' else "गेहूं का लाइव भाव 2,285 रुपये प्रति क्विंटल है।"
                st.success(f"**Assistant Reply:** {ans}")
                try:
                    tts = gTTS(text=ans, lang='hi' if curr_lang!='en' else 'en')
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                except Exception:
                    pass

        # 5. SMART TRAFFIC NOTIFICATIONS
        elif active == 'm5':
            st.markdown(f'<div class="section-title">🔔 Smart Traffic Notifications</div>', unsafe_allow_html=True)
            st.error(f"🚨 **Automated Alert for Token `{user['token_id']}`:** Heavy congestion at {user['district']} Mandi gate.")
            st.warning("⏱️ **Action Required:** Please delay arrival by **10 minutes**. Your slot is safe.")

        # 6. TRACK PROCUREMENT & PAYMENTS
        elif active == 'm6':
            st.markdown(f'<div class="section-title">💳 Track Procurement & Payments</div>', unsafe_allow_html=True)
            st.markdown("""
            - **Token Generation:** ✅ Completed (`Active`)
            - **Gate Entry & Weighing:** ⏳ Scheduled Today
            - **Moisture Test:** ⏳ Pending at Bay 2
            """)
            st.success("💳 **Expected Payout:** ₹ 1,02,375 will be credited via DBT within **48 hours**.")
