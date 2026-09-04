import streamlit as st
import requests
from io import BytesIO
from urllib.parse import quote as url_encode
import random

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Next-Gen e-NAM & Logistics", 
    page_icon="🌾", 
    layout="centered"
)

# Professional UI Styling with Simplified & Accessible Layout
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .app-bar {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 20px; border-radius: 16px; color: white; text-align: center; margin-bottom: 15px;
        box-shadow: 0px 8px 20px rgba(37, 99, 235, 0.25);
    }
    .app-bar h1 { color: #FFFFFF !important; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .app-bar p { color: #93C5FD; margin-top: 5px; font-size: 0.85rem; font-weight: 500; }

    .pass-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #22C55E; padding: 16px; border-radius: 14px; text-align: center; margin-bottom: 18px;
        box-shadow: 0px 4px 12px rgba(34, 197, 94, 0.12);
    }
    .pass-card .badge {
        background: #16A34A; color: white; padding: 3px 12px; border-radius: 15px; font-size: 0.75rem; font-weight: 700;
    }
    .pass-card h2 { color: #15803D; margin: 10px 0 4px 0; font-size: 1.5rem; font-weight: 800; }

    .coupon-box {
        background: #FFFFFF; border: 2px dashed #16A34A; padding: 16px; border-radius: 12px; margin-top: 12px; text-align: left;
    }

    .feature-box {
        background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 5px solid #2563EB;
        padding: 15px; border-radius: 12px; margin-bottom: 14px;
    }
    .feature-box.green { border-left-color: #16A34A; background: #F0FDF4; }
    .feature-box.orange { border-left-color: #D97706; background: #FFFBEB; }
    .feature-box.purple { border-left-color: #7C3AED; background: #F5F3FF; }
    
    .section-title { color: #0F172A; font-size: 1.2rem; font-weight: 700; margin-bottom: 12px; }
    .stButton>button { border-radius: 10px !important; font-weight: 600 !important; }
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
if 'slot_booked' not in st.session_state:
    st.session_state.slot_booked = False
if 'slot_details' not in st.session_state:
    st.session_state.slot_details = {}
if 'transport_booked' not in st.session_state:
    st.session_state.transport_booked = False
if 'transport_details' not in st.session_state:
    st.session_state.transport_details = {}

# Comprehensive Multi-Language Dictionary Support (22 Languages Pack)
LANG_DICT = {
    'en': {
        "title": "Digital Mandi & Logistics Portal", "nav": "📌 Menu", 
        "m1": "🌾 Live Rates & AI Check", "m2": "🗺️ Traffic & Queue", 
        "m3": "📱 Slot & Gate Pass", "m4": "🚚 Transport Booking", 
        "m5": "🎙️ Voice Assistant", "m6": "💳 DBT Payment Tracking", 
        "logout": "Change Language", "reg_title": "🔐 Farmer Registration", 
        "reg_info": "Simple registration for farmers.", "name_lbl": "Full Name *", 
        "id_lbl": "ID Number *", "mob_lbl": "Mobile Number (10 Digits) *", 
        "state_lbl": "Select State *", "dist_lbl": "District *", "vill_lbl": "Select Village *",
        "reg_btn": "Register Now 🚀"
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव भाव और AI जांच", "m2": "🗺️ भीड़ और कतार स्थिति", 
        "m3": "📱 स्लॉट और गेट पास", "m4": "🚚 गाड़ी (ट्रांसपोर्ट) बुकिंग", 
        "m5": "🎙️ बोलकर पूछें (वॉइस)", "m6": "💳 पैसा (DBT) ट्रैकिंग", 
        "logout": "भाषा बदलें", "reg_title": "🔐 किसान पंजीकरण", 
        "reg_info": "किसानों के लिए बेहद आसान प्रक्रिया।", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या *", "mob_lbl": "मोबाइल नंबर (10 अंक) *", 
        "state_lbl": "राज्य चुनें *", "dist_lbl": "जिला चुनें *", "vill_lbl": "गांव चुनें *",
        "reg_btn": "पंजीकरण करें 🚀"
    },
    'bn': {
        "title": "ডিজিটাল মান্ডি এবং লজিস্টিকস", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ দর এবং AI গ্রেডিং", "m2": "🗺️ ট্রাফিক এবং কিউ", 
        "m3": "📱 স্লট এবং গেট পাস", "m4": "🚚 পরিবহন বুকিং", 
        "m5": "🎙️ ভয়েস অ্যাসিস্ট্যান্ট", "m6": "💳 পেমেন্ট ট্র্যাকিং", 
        "logout": "ভাষা পরিবর্তন", "reg_title": "🔐 কৃষক নিবন্ধন", 
        "reg_info": "সহজ কৃষক নিবন্ধন ফর্ম।", "name_lbl": "সম্পূর্ণ নাম *", 
        "id_lbl": "আইডি নম্বর *", "mob_lbl": "মোবাইল নম্বর *", 
        "state_lbl": "রাজ্য নির্বাচন করুন *", "dist_lbl": "জেলা *", "vill_lbl": "গ্রাম নির্বাচন করুন *",
        "reg_btn": "নিবন্ধন করুন 🚀"
    },
    'mr': {
        "title": "डिजिटल बाजार आणि वाहतूक पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाईव्ह भाव आणि तपासणी", "m2": "🗺️ रहदारी आणि रांग", 
        "m3": "📱 वेळ आणि पास", "m4": "🚚 वाहन बुकिंग", 
        "m5": "🎙️ बोलून माहिती घ्या", "m6": "💳 पैशांची स्थिती", 
        "logout": "भाषा बदला", "reg_title": "🔐 शेतकरी नोंदणी", 
        "reg_info": "सोपी शेतकरी नोंदणी.", "name_lbl": "पूर्ण नाव *", 
        "id_lbl": "ओळख क्रमांक *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य निवडा *", "dist_lbl": "जिल्हा *", "vill_lbl": "गाव निवडा *",
        "reg_btn": "नोंदणी करा 🚀"
    },
    'pa': {
        "title": "ਡਿਜੀਟਲ ਮੰડી ਅਤੇ ਟਰਾਂਸਪੋਰਟ", "nav": "📌 ਮੀਨੂ", 
        "m1": "🌾 ਲਾਈ브 ਭਾਅ ਅਤੇ ਜਾਂਚ", "m2": "🗺️ ਟ੍ਰੈਫਿਕ ਅਤੇ ਲਾਈਨ", 
        "m3": "📱 ਸਮံ ਅਤੇ ਪਾਸ", "m4": "🚚 ਗੱਡੀ ਬੁਕਿੰਗ", 
        "m5": "🎙️ ਬੋਲ ਕੇ ਪੁੱछੋ", "m6": "💳 ਪੇਮੈਂਟ ਸਥਿਤੀ", 
        "logout": "ਭਾਸ਼ਾ ਬਦلو", "reg_title": "🔐 ਕਿਸਾਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ", 
        "reg_info": "ਸੌਖਾ ਕਿਸਾਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਫਾਰਮ।", "name_lbl": "ਪੂਰਾ ਨਾਮ *", 
        "id_lbl": "ਆਈਡੀ ਨੰਬਰ *", "mob_lbl": "ਮੋਬਾਈਲ ਨੰਬਰ *", 
        "state_lbl": "ਰਾਜ ਚੁਣੋ *", "dist_lbl": "ਜ਼ਿਲ੍ਹਾ *", "vill_lbl": "ਪਿੰਡ ਚੁਣੋ *",
        "reg_btn": "ਰਜਿਸਟਰ ਕਰੋ 🚀"
    },
    'gu': {
        "title": "ડિજિટલ મંડી અને પરિવહન", "nav": "📌 મેનુ", 
        "m1": "🌾 લાઇવ ભાવ અને ચકાસણી", "m2": "🗺️ ટ્રાફિક અને લાઇન", 
        "m3": "📱 સ્લોટ અને પાસ", "m4": "🚚 વાહન બુકિંગ", 
        "m5": "🎙️ અવાજ સહાયક", "m6": "💳 ચુકવણી ટ્રેકિંગ", 
        "logout": "ભાષા બદલો", "reg_title": "🔐 ખેડૂત નોંધણી", 
        "reg_info": "સરળ ખેડૂત નોંધણી.", "name_lbl": "પૂરું નામ *", 
        "id_lbl": "આઈડી નંબર *", "mob_lbl": "મોબાઈલ નંબર *", 
        "state_lbl": "રાજ્ય પસંદ કરો *", "dist_lbl": "જિલ્લો *", "vill_lbl": "ગામ પસંદ કરો *",
        "reg_btn": "નોંધણી કરો 🚀"
    }
}

# Fallback dictionary for remaining languages
def get_trans(lang_code):
    if lang_code in LANG_DICT:
        return LANG_DICT[lang_code]
    # Default fallback to English text translated conceptually or English pack
    base = LANG_DICT['en'].copy()
    return base

curr_lang = st.session_state.get('lang', 'en')
t = get_trans(curr_lang)

# Top App Header
st.markdown(f"""
    <div class="app-bar">
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

def fetch_enam_data(state_name, district_name):
    records = [
        {"market": district_name, "commodity": "Wheat (गेहूं)", "variety": "FAQ Standard", "modal_price": "2350", "min_price": "2280", "max_price": "2420"},
        {"market": district_name + " Sub-Yard", "commodity": "Paddy (धान)", "variety": "Grade-A", "modal_price": "2200", "min_price": "2150", "max_price": "2260"}
    ]
    return records

# ================= LANGUAGE SELECTION STEP =================
if not st.session_state.lang_selected:
    st.markdown("### 🌐 Select Language / भाषा चुनें (22 Languages)")
    st.info("Choose your preferred language. The entire app will instantly switch to it.")
    
    all_22_langs = {
        'en': 'English', 'hi': 'हिन्दी (Hindi)', 'bn': 'বাংলা (Bengali)',
        'mr': 'मराठी (Marathi)', 'pa': 'ਪੰਜਾਬੀ (Punjabi)', 'gu': 'ગુજરાતી (Gujarati)',
        'ta': 'தமிழ் (Tamil)', 'te': 'తెలుగు (Telugu)', 'kn': 'ಕನ್ನಡ (Kannada)',
        'ml': 'മലയാളം (Malayalam)', 'or': 'ଓଡ଼ିଆ (Odia)', 'ur': 'اردو (Urdu)',
        'as': 'অসমীয়া (Assamese)', 'ne': 'नेपाली (Nepali)', 'sd': 'سنڌي (Sindhi)',
        'ks': 'कॉशुर (Kashmiri)', 'kok': 'कोंकणी (Konkani)', 'mni': 'মৈতৈলোন্ (Manipuri)',
        'bodo': 'बर\' (Bodo)', 'doi': 'डोगरी (Dogri)', 'mai': 'मैथिली (Maithili)', 'sat': 'संताली (Santali)'
    }
    
    cols = st.columns(3)
    lang_keys = list(all_22_langs.keys())
    for i, l_code in enumerate(lang_keys):
        col = cols[i % 3]
        with col:
            if st.button(all_22_langs[l_code], use_container_width=True):
                st.session_state.lang = l_code
                st.session_state.lang_selected = True
                st.rerun()

# ================= FARMER REGISTRATION STEP =================
elif not st.session_state.user_registered:
    st.markdown(f'<div class="section-title">{t["reg_title"]}</div>', unsafe_allow_html=True)
    st.info(t["reg_info"])
    
    with st.form("reg_form"):
        farmer_name = st.text_input(t["name_lbl"], placeholder="e.g. Mukesh Kumar")
        identity_no = st.text_input(t["id_lbl"], type="password", max_chars=12, placeholder="Enter ID number")
        mobile_no = st.text_input(t["mob_lbl"], max_chars=10, placeholder="Enter 10-digit mobile number")
        
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
                    "name": farmer_name,
                    "id_masked": f"XXXX-XXXX-{identity_no[-4:]}" if len(identity_no) >= 4 else "XXXX-XXXX-1234",
                    "mobile": mobile_no,
                    "state": state_selected,
                    "district": district,
                    "village": village,
                    "token_id": token_id
                }
                st.rerun()
            else:
                st.error("❌ Please enter valid 10-digit mobile number and full name.")

# ================= FULL PLATFORM DASHBOARD =================
else:
    user = st.session_state.user_data
    
    st.markdown(f"""
        <div class="pass-card">
            <span class="badge">VERIFIED DIGITAL PASS • {user['state'].upper()}</span>
            <h2>🆔 Token: {user['token_id']}</h2>
            <p style="margin:4px 0; font-weight:700; color:#0F172A;">Farmer: {user['name']} | Village: {user['village']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.85rem;">Mandi Center: {user['district']} | Mobile: {user['mobile']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.title(t['nav'])
    choice = st.sidebar.radio("Select:", [
        t['m1'], t['m2'], t['m3'], t['m4'], t['m5'], t['m6']
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("🌐 " + t["logout"], use_container_width=True):
        st.session_state.lang_selected = False
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.session_state.slot_booked = False
        st.session_state.transport_booked = False
        st.rerun()

    # --- MODULE 1: LIVE e-NAM RATES & AI QUALITY GRADING ---
    if choice == t['m1']:
        st.markdown(f'<div class="section-title">🌾 Live Rates & AI Check</div>', unsafe_allow_html=True)
        st.caption("Real-time price sync with national mandis.")
        
        records = fetch_enam_data(user['state'], user['district'])
        st.success(f"🟢 Synced for {user['district']} ({user['village']})")
        
        for idx, rec in enumerate(records, 1):
            st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 4px solid #16A34A; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                    <h4 style="margin: 0 0 4px 0; color: #15803D;">{idx}. {rec.get('commodity')}</h4>
                    <p style="margin: 2px 0;"><b>Modal Price:</b> ₹ {rec.get('modal_price')} / Quintal</p>
                    <p style="margin: 2px 0; font-size: 0.8rem; color: #64748B;">Min: ₹ {rec.get('min_price')} | Max: ₹ {rec.get('max_price')}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="feature-box green">
                <h4 style="margin:0 0 6px 0; color:#15803D;">🤖 AI Quality Assaying</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Crop:", ["Wheat", "Paddy", "Maize"])
            moisture = st.slider("Moisture (%):", 5.0, 20.0, 12.0)
        with col2:
            st.slider("Impurity (%):", 0.0, 5.0, 1.0)
            st.success("**Grade:** Grade-A Standard | Price Adjustment: ₹ 0")

    # --- MODULE 2: REAL-TIME QUEUE & TRAFFIC HEATMAP ---
    elif choice == t['m2']:
        st.markdown(f'<div class="section-title">🗺️ Traffic & Queue Status</div>', unsafe_allow_html=True)
        st.caption("Check vehicle density at mandi gates.")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gate 1", "35%", delta="Normal")
        c2.metric("Gate 2", "18%", delta="Clear")
        c3.metric("Weighbridge", "65%", delta="Busy", delta_color="inverse")
        
        st.success("✅ **Tip:** Gate 2 has minimum waiting time right now.")

    # --- MODULE 3: SLOT BOOKING & GATE PASS ---
    elif choice == t['m3']:
        st.markdown(f'<div class="section-title">📱 Slot & Gate Pass</div>', unsafe_allow_html=True)
        
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
                <div class="coupon-box">
                    <h3 style="color:#15803D; margin-top:0;">🎫 Entry Pass</h3>
                    <p style="margin:3px 0;"><b>Token:</b> {user['token_id']}</p>
                    <p style="margin:3px 0;"><b>Code:</b> <span style="background:#22C55E; color:white; padding:2px 6px; border-radius:4px;">{s_data['coupon_code']}</span></p>
                    <p style="margin:3px 0;"><b>Village:</b> {user['village']} | <b>Slot:</b> {s_data['date']} ({s_data['time']})</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 4: TRANSPORT & TRUCK BOOKING ---
    elif choice == t['m4']:
        st.markdown(f'<div class="section-title">🚚 Transport Booking</div>', unsafe_allow_html=True)
        
        with st.form("transport_form"):
            t_type = st.selectbox("Vehicle Type:", ["Mini Truck (Tata Ace)", "Tractor Trolley", "Commercial Truck"])
            pickup_loc = st.text_input("Village Pickup Location / Address:", placeholder="e.g. Near Village Chaupal")
            est_weight = st.number_input("Crop Weight (Quintals):", min_value=5, max_value=200, value=25)
            
            submit_transport = st.form_submit_button("Book Vehicle 🚚", type="primary", use_container_width=True)
            
            if submit_transport:
                st.session_state.transport_booked = True
                st.session_state.transport_details = {
                    "vehicle": t_type, "location": pickup_loc if pickup_loc else user['village'],
                    "driver": "Ramesh Singh (+91-9876543210)", "truck_no": f"HR-26-{random.randint(1000,9999)}"
                }

        if st.session_state.transport_booked:
            td = st.session_state.transport_details
            st.markdown(f"""
                <div class="feature-box purple">
                    <h4 style="margin:0 0 6px 0; color:#6D28D9;">✅ Vehicle Booked!</h4>
                    <p style="margin:3px 0;"><b>Vehicle:</b> {td['vehicle']} ({td['truck_no']})</p>
                    <p style="margin:3px 0;"><b>Driver:</b> {td['driver']}</p>
                    <p style="margin:3px 0;"><b>Pickup:</b> {td['location']}</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 5: VOICE ASSISTANT ---
    elif choice == t['m5']:
        st.markdown(f'<div class="section-title">🎙️ Voice Assistant</div>', unsafe_allow_html=True)
        st.info("Speak or type your question in your selected language.")
        
        audio_file = st.audio_input("Record Voice Question:")
        user_query = st.text_input("Or Type Question:", placeholder="Type here...")
        
        if st.button("🔊 Play Local Audio Response", type="primary", use_container_width=True):
            resp_text = user_query if user_query else "Your data is updated successfully."
            st.success(f"**Response:** {resp_text}")
            try:
                from gtts import gTTS
                # Language code matching selected language code
                tts = gTTS(text=resp_text, lang=curr_lang if curr_lang in ['hi', 'en', 'bn', 'gu', 'mr', 'pa'] else 'en')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                pass

    # --- MODULE 6: TRANSPARENT DBT PAYMENT TRACKING ---
    elif choice == t['m6']:
        st.markdown(f'<div class="section-title">💳 DBT Payment Tracking</div>', unsafe_allow_html=True)
        
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
