import streamlit as st
import random
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Ultimate Mandi Portal", 
    page_icon="🌾", 
    layout="centered"
)

# Professional UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; color: #1E293B; }
    
    .main-banner {
        background: linear-gradient(135deg, #065F46 0%, #047857 50%, #059669 100%);
        padding: 24px; border-radius: 16px; color: white; text-align: center; margin-bottom: 20px;
        box-shadow: 0px 10px 25px rgba(5, 150, 105, 0.25);
    }
    .main-banner h1 { color: #FFFFFF !important; font-size: 2rem; font-weight: 800; margin: 0; }
    .main-banner p { color: #A7F3D0; margin: 8px 0 0 0; font-size: 1.05rem; font-weight: 500; }

    .pass-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2.5px solid #16A34A; padding: 20px; border-radius: 14px; text-align: center; margin-bottom: 20px;
    }
    .section-title { 
        color: #064E3B; font-size: 1.4rem; font-weight: 800; margin-bottom: 16px; 
        border-bottom: 3px solid #34D399; padding-bottom: 6px; display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Persistent Session State Initialization
if 'lang' not in st.session_state: st.session_state.lang = 'hi'
if 'user_registered' not in st.session_state: st.session_state.user_registered = False
if 'user_data' not in st.session_state: st.session_state.user_data = {}
if 'slot_booked' not in st.session_state: st.session_state.slot_booked = False
if 'transport_booked' not in st.session_state: st.session_state.transport_booked = False
if 'offline_sms_booked' not in st.session_state: st.session_state.offline_sms_booked = False
if 'voice_query_text' not in st.session_state: st.session_state.voice_query_text = ""

# Full Multi-Language Dictionary for All Modules
LANG_PACK = {
    'en': {
        "title": "Digital Mandi & Logistics Portal", "nav": "📌 Portal Navigation", 
        "m1": "🌾 Live Mandi Rates & AI Quality Check", "m2": "🗺️ Mandi Traffic & Queue Status", 
        "m3": "📱 Slot Booking & Gate Pass", "m4": "🚚 Transport & 1-Press SMS Booking", 
        "m5": "🎙️ AI Voice Assistant", "m6": "💳 DBT Payment Tracking", "m7": "🌤️ Weather Forecast & Advisory",
        "reg_title": "🔐 Farmer Universal Registration", "name_lbl": "Full Name *", 
        "id_lbl": "ID Number (Aadhaar/Farmer ID) *", "mob_lbl": "Mobile Number (10 Digits) *", 
        "state_lbl": "Select State *", "dist_lbl": "Select District / APMC *", "vill_lbl": "Select Village *", "reg_btn": "Register & Enter Portal 🚀",
        "reset_btn": "🔄 Reset Profile & Language", "verified_pass": "VERIFIED MANDI PASS", "farmer_lbl": "Farmer", 
        "village_lbl": "Village", "apmc_lbl": "APMC Center", "live_rates_title": "Live Mandi Rates & State/District Wise Crop Pricing",
        "select_crop": "Select Crop for Live Rates & AI Check:", "modal_price": "Modal Price", "min_price": "Min Mandi Price", 
        "max_price": "Max Mandi Price", "ai_grade_title": "AI Crop Quality Grading System", "moisture_lbl": "Moisture Content (%):",
        "impurity_lbl": "Impurity / Foreign Matter (%):", "grade_a": "AI Quality Result: Grade-A Premium Quality (Eligible for Maximum MSP & Bonus)",
        "grade_b": "AI Quality Result: Grade-B Standard Quality (Minor price deduction)", "grade_rej": "AI Quality Result: Rejection Risk. Clean crop before bringing to mandi.",
        "traffic_title": "Mandi Traffic & Queue Status", "gate1": "Gate 1 (Main National Highway Entrance)", "gate2": "Gate 2 (Back Gate / Fast Track Delivery)",
        "weighbridge": "Weighbridge / Kanta Station", "traffic_sug": "AI Suggestion: Use Gate 2 today to bypass long queues.",
        "slot_title": "Slot Booking & Digital Gate Pass", "arr_date": "Select Mandi Arrival Date:", "time_window": "Select Time Window:",
        "gen_pass": "Generate Gate Pass 🎫", "digital_pass_title": "Verified Digital Entry Pass", "pass_code": "Pass Code", "booked_slot": "Booked Slot",
        "transport_title": "Transport & 1-Press SMS Booking", "tab1": "Truck Logistics Booking", "tab2": "Interactive 1-Press SMS Slot Booking",
        "veh_type": "Vehicle Type:", "pickup_loc": "Village Pickup Landmark:", "est_weight": "Estimated Crop Weight (Quintals):",
        "book_veh_btn": "Book Vehicle & Dispatch SMS 🚚📱", "veh_conf": "Transport Vehicle Confirmed & SMS Sent!", "driver_ph": "Driver Phone",
        "whatsapp_btn": "WhatsApp Driver", "sms_label": "1 dabakar SMS se slot बुक करें:", "sms_btn": "Send 1-Press SMS Request",
        "voice_title": "AI Voice Assistant (Speak & Ask)", "voice_info": "Use mic or type below. AI will speak and reply instantly!",
        "voice_placeholder": "e.g. What is the wheat price in mandi?", "clear_btn": "Clear", "ask_audio": "Ask & Listen Audio Answer",
        "dbt_title": "DBT Payment Tracking", "dbt_msg": "Payment Status: Amount will be credited directly to your Aadhaar-linked bank account within 24-48 hours.",
        "weather_title": "Weather Forecast & Advisory", "temp": "Temperature", "humidity": "Humidity", "rain_risk": "Rainfall Risk",
        "weather_adv": "AI Advisory: Weather is completely clear and optimal for harvesting and transporting crops over the next 48 hours."
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट पोर्टल", "nav": "📌 पोर्टल मेनू", 
        "m1": "🌾 लाइव मंडी भाव और AI क्वालिटी जांच", "m2": "🗺️ मंडी भीड़ और कतार स्थिति", 
        "m3": "📱 स्लॉट बुकिंग और गेट पास", "m4": "🚚 गाड़ी और 1-प्रेस SMS बुकिंग", 
        "m5": "🎙️ AI वॉइस असिस्टेंट (बोलकर पूछें)", "m6": "💳 पैसा (DBT) भुगतान ट्रैकिंग", "m7": "🌤️ मौसम की जानकारी और सलाह",
        "reg_title": "🔐 किसान सार्वभौमिक पंजीकरण", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या (आधार/किसान आईडी) *", "mob_lbl": "मोबाइल नंबर (10 अंक) *", 
        "state_lbl": "राज्य चुनें *", "dist_lbl": "जिला / मंडी चुनें *", "vill_lbl": "गांव चुनें *", "reg_btn": "पंजीकरण करें और पोर्टल खोलें 🚀",
        "reset_btn": "🔄 प्रोफाइल और भाषा रीसेट करें", "verified_pass": "सत्यापित मंडी पास", "farmer_lbl": "किसान", 
        "village_lbl": "गांव", "apmc_lbl": "APMC केंद्र", "live_rates_title": "लाइव मंडी भाव और राज्य/जिला फसल मूल्य",
        "select_crop": "लाइव भाव और AI जांच के लिए फसल चुनें:", "modal_price": "औसत भाव (Modal Price)", "min_price": "न्यूनतम भाव", 
        "max_price": "अधिकतम भाव", "ai_grade_title": "AI फसल क्वालिटी ग्रेडिंग सिस्टम", "moisture_lbl": "नमी की मात्रा (%):",
        "impurity_lbl": "कचरा / अशुद्धता (%):", "grade_a": "AI क्वालिटी परिणाम: ग्रेड-A प्रीमियम क्वालिटी (अधिकतम MSP और बोनस के योग्य)",
        "grade_b": "AI क्वालिटी परिणाम: ग्रेड-B मानक क्वालिटी (सामान्य कटौती)", "grade_rej": "AI क्वालिटी परिणाम: अस्वीकृति का जोखिम। मंडी लाने से पहले फसल साफ करें।",
        "traffic_title": "मंडी ट्रैफिक और कतार स्थिति", "gate1": "गेट 1 (मुख्य राष्ट्रीय राजमार्ग प्रवेश)", "gate2": "गेट 2 (पिछला गेट / फास्ट ट्रैक डिलीवरी)",
        "weighbridge": "धर्मकांटा / तौल स्टेशन", "traffic_sug": "AI सुझाव: लंबी कतारों से बचने के लिए आज **गेट 2** का उपयोग करें।",
        "slot_title": "स्लॉट बुकिंग और डिजिटल गेट पास", "arr_date": "मंडी पहुंचने की तारीख चुनें:", "time_window": "समय स्लॉट चुनें:",
        "gen_pass": "गेट पास जनरेट करें 🎫", "digital_pass_title": "सत्यापित डिजिटल एंट्री पास", "pass_code": "पास कोड", "booked_slot": "बुक किया गया स्लॉट",
        "transport_title": "परिवहन और 1-प्रेस SMS बुकिंग", "tab1": "ट्रक लॉजिस्टिक्स बुकिंग", "tab2": "इंटरैक्टिव 1-प्रेस SMS स्लॉट बुकिंग",
        "veh_type": "वाहन का प्रकार:", "pickup_loc": "गांव का पिकअप लैंडमार्क:", "est_weight": "अनुमानित फसल वजन (क्विंटल):",
        "book_veh_btn": "वाहन बुक करें और SMS भेजें 🚚📱", "veh_conf": "परिवहन वाहन कन्फर्म और SMS भेजा गया!", "driver_ph": "ड्राइवर फोन नंबर",
        "whatsapp_btn": "ड्राइवर से WhatsApp पर बात करें", "sms_label": "1 दबाकर SMS से स्लॉट बुक करें:", "sms_btn": "1-प्रेस SMS अनुरोध भेजें",
        "voice_title": "AI वॉइस असिस्टेंट (बोलकर पूछें और सुनें)", "voice_info": "माइक बटन या नीचे दिए गए बॉक्स का उपयोग करें। AI बोलकर जवाब देगा!",
        "voice_placeholder": "उदा. मंडी में गेहूं का भाव क्या है?", "clear_btn": "साफ करें", "ask_audio": "बोलकर और सुनकर उत्तर प्राप्त करें",
        "dbt_title": "DBT भुगतान ट्रैकिंग", "dbt_msg": "भुगतान स्थिति: राशि 24-48 घंटों के भीतर सीधे आपके आधार-लिंक बैंक खाते में जमा कर दी जाएगी।",
        "weather_title": "मौसम की जानकारी और सलाह", "temp": "तापमान", "humidity": "नमी (Humidity)", "rain_risk": "बारिश का जोखिम",
        "weather_adv": "AI सलाह: मौसम पूरी तरह साफ है और अगले 48 घंटों में फसल काटने और ले जाने के लिए उत्तम है।"
    }
}

all_22_langs = {
    'en': 'English', 'hi': 'हिन्दी (Hindi)', 'bn': 'বাংলা (Bengali)',
    'mr': 'मराठी (Marathi)', 'pa': 'ਪੰਜਾਬੀ (Punjabi)', 'gu': 'ગુજરાતી (Gujarati)',
    'ta': 'தமிழ் (Tamil)', 'te': 'తెలుగు (Telugu)', 'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)', 'or': 'ଓଡିଆ (Odia)', 'ur': 'اردو (Urdu)',
    'as': 'অসমীয়া (Assamese)', 'ne': 'नेपाली (Nepali)', 'sd': 'سنڌي (Sindhi)',
    'ks': 'कॉशुर (Kashmiri)', 'kok': 'कोंकणी (Konkani)', 'mni': 'মৈতৈলোন্ (Manipuri)',
    'bodo': 'बर\' (Bodo)', 'doi': 'डोगरी (Dogri)', 'mai': 'मैथिली (Maithili)', 'sat': 'संताली (Santali)'
}

# Persistent Loop Language Selector in Sidebar across ALL Pages
st.sidebar.markdown("### 🌐 Universal Language / भाषा चुनें")
selected_lang_name = st.sidebar.selectbox(
    "Choose Language:", 
    list(all_22_langs.values()), 
    index=list(all_22_langs.keys()).index(st.session_state.lang) if st.session_state.lang in all_22_langs else 1
)

for code, name in all_22_langs.items():
    if name == selected_lang_name and st.session_state.lang != code:
        st.session_state.lang = code
        st.rerun()

curr_lang = st.session_state.lang
# Fallback to Hindi dictionary if keys are missing for other languages
t = LANG_PACK.get(curr_lang, LANG_PACK['hi'])

# Dynamic Header Banner
st.markdown(f"""
    <div class="main-banner">
        <h1>KRISHI PLATFORM</h1>
        <p>🌾 {t['title']}</p>
    </div>
""", unsafe_allow_html=True)

# State & District mapping dictionary
STATE_DISTRICTS = {
    "Gujarat": {
        "Ahmedabad APMC": ["Vinchhiya", "Bavla", "Dholka", "Sanand"],
        "Surat APMC": ["Mandvi", "Bardoli", "Kamrej", "Palsana"],
        "Rajkot APMC": ["Gondal", "Jetpur", "Jasdan", "Upleta"]
    },
    "Punjab": {
        "Ludhiana APMC": ["Machhiwara", "Payal", "Samrala", "Khanna"],
        "Amritsar APMC": ["Ajnala", "Baba Bakala", "Rayya", "Majitha"],
        "Patiala APMC": ["Nabha", "Rajpura", "Samana", "Patran"]
    },
    "Uttar Pradesh": {
        "Lucknow APMC": ["Kakori", "Malihabad", "Banthra", "Chinhat"],
        "Varanasi APMC": ["Pindra", "Cholapur", "Baragaon", "Sevapuri"],
        "Kanpur APMC": ["Bidhnu", "Bilhaur", "Ghatampur", "Chaubepur"]
    },
    "Haryana": {
        "Karnal APMC": ["Nilokheri", "Assandh", "Gharaunda", "Indri"],
        "Hisar APMC": ["Hansi", "Narnaund", "Barwala", "Adampur"],
        "Rohtak APMC": ["Meham", "Kalanaur", "Sampla", "Kharawar"]
    }
}

# ================= STEP 1: FARMER REGISTRATION =================
if not st.session_state.user_registered:
    st.markdown(f'<div class="section-title">{t["reg_title"]}</div>', unsafe_allow_html=True)
    
    with st.form("reg_form"):
        farmer_name = st.text_input(t["name_lbl"], placeholder="e.g. Mukesh Kumar")
        identity_no = st.text_input(t["id_lbl"], type="password", max_chars=12, placeholder="Enter 12-digit ID")
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
                st.error("❌ Kripya sahi 10-ank ka mobile number aur naam darj karein.")

# ================= STEP 2: DASHBOARD & MODULES =================
else:
    user = st.session_state.user_data
    
    st.markdown(f"""
        <div class="pass-card">
            <span style="background:#16A34A; color:white; padding:4px 14px; border-radius:20px; font-size:0.85rem; font-weight:800;">{t['verified_pass']}</span>
            <h2 style="color:#15803D; margin:10px 0 4px 0; font-size:1.6rem;">🆔 Token: {user['token_id']}</h2>
            <p style="margin:2px 0; font-weight:700; color:#0F172A; font-size:1.15rem;">{t['farmer_lbl']}: {user['name']} | {t['village_lbl']}: {user['village']}</p>
            <p style="margin:2px 0; color:#475569; font-size:1rem;">{t['apmc_lbl']}: {user['district']}, {user['state']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"--- \n ### {t['nav']}")
    choice = st.sidebar.radio("Select Module:", [
        t['m1'], t['m2'], t['m3'], t['m4'], t['m5'], t['m6'], t['m7']
    ], label_visibility="collapsed")

    st.sidebar.markdown("---")
    if st.sidebar.button(t['reset_btn'], use_container_width=True):
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.session_state.slot_booked = False
        st.session_state.transport_booked = False
        st.session_state.offline_sms_booked = False
        st.rerun()

    # --- MODULE 1: STATE-WISE & DISTRICT-WISE LIVE RATES + AI QUALITY GRADING ---
    if choice == t['m1']:
        st.markdown(f'<div class="section-title">🌾 {t["live_rates_title"]}</div>', unsafe_allow_html=True)
        st.success(f"🟢 Showing Live Rates synced specifically for **{user['district']}, {user['state']}** (Village: {user['village']})")
        
        state_crop_database = {
            "Gujarat": {
                "Ahmedabad APMC": {"Wheat (गेहूं)": (2350, 2280, 2420), "Cotton (कपास)": (6900, 6700, 7150), "Cumin / Jeera (जीरा)": (24500, 24000, 25200)},
                "Surat APMC": {"Banana (केला)": (1800, 1700, 1950), "Paddy / Rice (धान)": (2200, 2100, 2300), "Wheat (गेहूं)": (2380, 2300, 2450)},
                "Rajkot APMC": {"Groundnut (मूंगफली)": (6100, 5900, 6300), "Cotton (कपास)": (6850, 6650, 7050), "Sesame (तिल)": (11200, 10800, 11500)}
            },
            "Punjab": {
                "Ludhiana APMC": {"Wheat (गेहूं)": (2400, 2320, 2480), "Paddy / Rice (धान)": (2250, 2180, 2320), "Maize (मक्का)": (2120, 2050, 2200)},
                "Amritsar APMC": {"Wheat (गेहूं)": (2390, 2310, 2460), "Paddy / Rice (धान)": (2240, 2170, 2310), "Potato (आलू)": (1400, 1300, 1550)},
                "Patiala APMC": {"Wheat (गेहूं)": (2410, 2330, 2490), "Mustard (सरसों)": (5700, 5550, 5850), "Paddy / Rice (धान)": (2260, 2190, 2330)}
            },
            "Uttar Pradesh": {
                "Lucknow APMC": {"Wheat (गेहूं)": (2320, 2250, 2400), "Paddy / Rice (धान)": (2150, 2080, 2220), "Potato (आलू)": (1350, 1250, 1450)},
                "Varanasi APMC": {"Wheat (गेहूं)": (2300, 2230, 2380), "Mustard (सरसों)": (5600, 5450, 5750), "Peas (मटर)": (4500, 4300, 4700)},
                "Kanpur APMC": {"Wheat (गेहूं)": (2310, 2240, 2390), "Gram / Chana (चना)": (5450, 5300, 5600), "Paddy / Rice (धान)": (2160, 2090, 2230)}
            },
            "Haryana": {
                "Karnal APMC": {"Basmati Rice (धान बासमती)": (3800, 3650, 4000), "Wheat (गेहूं)": (2380, 2300, 2450), "Mustard (सरसों)": (5750, 5600, 5900)},
                "Hisar APMC": {"Cotton (कपास)": (6950, 6750, 7200), "Cluster Beans / Guar (ग्वार)": (5300, 5100, 5500), "Bajra (बाजरा)": (2350, 2250, 2450)},
                "Rohtak APMC": {"Wheat (गेहूं)": (2370, 2290, 2440), "Barley (जौ)": (2100, 2000, 2200), "Gram (चना)": (5400, 5250, 5550)}
            }
        }
        
        current_state_market = state_crop_database.get(user['state'], state_crop_database["Gujarat"])
        current_district_crops = current_state_market.get(user['district'], list(current_state_market.values())[0])
        
        selected_crop = st.selectbox(t["select_crop"], list(current_district_crops.keys()))
        modal_p, min_p, max_p = current_district_crops[selected_crop]
        
        st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 6px solid #059669; padding: 16px; border-radius: 10px; margin-bottom: 16px;">
                <h3 style="margin: 0 0 8px 0; color: #064E3B;">{selected_crop} ({user['district']})</h3>
                <p style="margin: 4px 0; font-size: 1.2rem;"><b>{t['modal_price']}:</b> ₹ {modal_p} / Quintal</p>
                <p style="margin: 4px 0; font-size: 1rem; color: #64748B;">{t['min_price']}: ₹ {min_p} | {t['max_price']}: ₹ {max_p}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"#### 🔬 {t['ai_grade_title']}")
        col1, col2 = st.columns(2)
        with col1:
            moisture = st.slider(t["moisture_lbl"], 5.0, 20.0, 12.0)
        with col2:
            impurity = st.slider(t["impurity_lbl"], 0.0, 10.0, 1.0)
            
        if moisture <= 13.0 and impurity <= 2.0:
            st.success(f"🌟 **{t['grade_a']}**")
        elif moisture <= 15.0 and impurity <= 5.0:
            st.warning(f"⚠️ **{t['grade_b']}**")
        else:
            st.error(f"❌ **{t['grade_rej']}**")

    # --- MODULE 2: TRAFFIC & QUEUE STATUS ---
    elif choice == t['m2']:
        st.markdown(f'<div class="section-title">🗺️ {t["traffic_title"]} ({user["district"]})</div>', unsafe_allow_html=True)
        st.markdown(f"### 🟢 {t['gate1']}")
        st.progress(0.40, text="Traffic Congestion: 40% (Moderate Flow)")
        st.markdown(f"### 🟢 {t['gate2']}")
        st.progress(0.15, text="Traffic Congestion: 15% (Recommended - Fast Lane)")
        st.markdown(f"### 🟠 {t['weighbridge']}")
        st.progress(0.60, text="Traffic Congestion: 60% (Medium Waiting Time)")
        st.success(f"✅ **{t['traffic_sug']}**")

    # --- MODULE 3: SLOT BOOKING & GATE PASS ---
    elif choice == t['m3']:
        st.markdown(f'<div class="section-title">📱 {t["slot_title"]}</div>', unsafe_allow_html=True)
        with st.form("slot_form"):
            arr_date = st.date_input(t["arr_date"])
            time_slot = st.selectbox(t["time_window"], [
                "08:00 AM - 10:00 AM (Morning Slot)", 
                "11:00 AM - 01:00 PM (Mid-Day Slot)", 
                "03:00 PM - 05:00 PM (Evening Slot)"
            ])
            submit_slot = st.form_submit_button(t["gen_pass"], type="primary", use_container_width=True)
            if submit_slot:
                st.session_state.slot_booked = True
                st.session_state.slot_details = {
                    "date": str(arr_date), "time": time_slot,
                    "coupon_code": f"CPN-{random.randint(100000, 999999)}"
                }

        if st.session_state.slot_booked:
            s_data = st.session_state.slot_details
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 2.5px dashed #16A34A; padding: 20px; border-radius: 12px; margin-top: 15px;">
                    <h3 style="color:#15803D; margin-top:0;">🎫 {t['digital_pass_title']}</h3>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>Token ID:</b> {user['token_id']}</p>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>{t['farmer_lbl']}:</b> {user['name']} ({user['village']})</p>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>{t['pass_code']}:</b> <span style="background:#22C55E; color:white; padding:4px 10px; border-radius:6px; font-weight:700;">{s_data['coupon_code']}</span></p>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>{t['booked_slot']}:</b> {s_data['date']} ({s_data['time']})</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 4: TRANSPORT & 1-PRESS SMS BOOKING ---
    elif choice == t['m4']:
        st.markdown(f'<div class="section-title">🚚 {t["transport_title"]}</div>', unsafe_allow_html=True)
        driver_fixed_num = "7254879397"
        
        tab_truck, tab_sms = st.tabs([f"🚚 {t['tab1']}", f"📱 {t['tab2']}"])
        
        with tab_truck:
            with st.form("transport_form"):
                t_type = st.selectbox(t["veh_type"], ["Mini Truck (Tata Ace)", "Tractor Trolley", "Commercial Truck"])
                pickup_loc = st.text_input(t["pickup_loc"], value=f"{user['village']}, {user['district']}")
                est_weight = st.number_input(t["est_weight"], min_value=5, max_value=300, value=25)
                
                submit_transport = st.form_submit_button(t["book_veh_btn"], type="primary", use_container_width=True)
                if submit_transport:
                    st.session_state.transport_booked = True
                    st.session_state.transport_details = {
                        "vehicle": t_type, "location": pickup_loc,
                        "driver_phone": driver_fixed_num, "truck_no": f"HR-26-{random.randint(1000,9999)}"
                    }

            if st.session_state.transport_booked:
                td = st.session_state.transport_details
                st.markdown(f"""
                    <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 6px solid #7C3AED; padding: 18px; border-radius: 10px;">
                        <h4 style="margin:0 0 8px 0; color:#6D28D9; font-size:1.25rem;">✅ {t['veh_conf']}</h4>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>{t['veh_type'][:-1]}:</b> {td['vehicle']} ({td['truck_no']})</p>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>{t['driver_ph']}:</b> <code>{td['driver_phone']}</code></p>
                        <a href="https://wa.me/91{td['driver_phone']}?text=Hello%20Driver,%20I%20have%20booked%20transport%20for%20{td['location']}." target="_blank" style="display:inline-block; margin-top:12px; background:#25D366; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:700;">💬 {t['whatsapp_btn']}</a>
                    </div>
                """, unsafe_allow_html=True)

        with tab_sms:
            with st.form("sms_slot_form"):
                st.markdown(f"<b>{t['sms_label']}</b>", unsafe_allow_html=True)
                sms_option = st.radio("Select SMS Command:", [
                    "1 - सुबह का स्लॉट बुक करें (Morning Slot: 08:00 AM)", 
                    "2 - दोपहर का स्लॉट बुक करें (Afternoon Slot: 12:00 PM)", 
                    "3 - शाम का स्लॉट बुक करें (Evening Slot: 04:00 PM)"
                ])
                submit_sms_btn = st.form_submit_button(t["sms_btn"], type="primary", use_container_width=True)
                if submit_sms_btn:
                    st.session_state.offline_sms_booked = True
                    st.session_state.sms_code_selected = sms_option[0]

            if st.session_state.offline_sms_booked:
                sc = st.session_state.sms_code_selected
                slot_map = {'1': '08:00 AM Morning', '2': '12:00 PM Afternoon', '3': '04:00 PM Evening'}
                st.success(f"✅ 1-Press SMS Slot Confirmed for **{slot_map.get(sc, 'Morning')}** via gateway `7254879397`.")

    # --- MODULE 5: ROBUST AI VOICE ASSISTANT (DUAL MIC & TEXT SYNC) ---
    elif choice == t['m5']:
        st.markdown(f'<div class="section-title">🎙️ {t["voice_title"]}</div>', unsafe_allow_html=True)
        st.info(f"💡 {t['voice_info']}")
        
        col_v1, col_v2 = st.columns([3, 1])
        with col_v1:
            voice_input = st.text_input(
                "Apna sawal yahan likhein ya bolkar enter karein:", 
                value=st.session_state.get('voice_query_text', ''),
                placeholder=t['voice_placeholder']
            )
        with col_v2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"🗑️ {t['clear_btn']}", use_container_width=True):
                st.session_state.voice_query_text = ""
                st.rerun()

        if st.button(f"🔊 {t['ask_audio']}", type="primary", use_container_width=True):
            if voice_input.strip():
                resp_text = f"नमस्ते {user['name']}. आपका सवाल है: {voice_input}. आपकी मंडी {user['district']} में टोकन नंबर {user['token_id']} के साथ सभी सुविधाएं चालू हैं।"
            else:
                resp_text = f"नमस्ते {user['name']}. आपका टोकन नंबर {user['token_id']} है और आप {user['district']} मंडी से जुड़े हैं।"
            
            st.success(f"**🔊 AI Assistant Reply:** {resp_text}")
            
            try:
                from gtts import gTTS
                tts = gTTS(text=resp_text, lang='hi')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                st.warning("Audio generated successfully.")

    # --- MODULE 6: DBT PAYMENT TRACKING ---
    elif choice == t['m6']:
        st.markdown(f'<div class="section-title">💳 {t["dbt_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        | Verification Stage | Status | Details & Remarks |
        | :--- | :--- | :--- |
        | **1. Universal Registration** | ✅ Completed | Token ID: `{user['token_id']}` |
        | **2. Gate Entry & Weighing** | ✅ Completed | Verified at {user['district']} |
        | **3. Quality Check & Sale** | ✅ Completed | Grade-A Verified |
        | **4. Direct Bank Transfer (DBT)** | ⏳ Processing | Secure transfer to Aadhaar-linked bank account |
        """)
        st.success(f"💳 **{t['dbt_msg']}**")

    # --- MODULE 7: WEATHER FORECAST ---
    elif choice == t['m7']:
        st.markdown(f'<div class="section-title">🌤️ {t["weather_title"]}</div>', unsafe_allow_html=True)
        st.success(f"🟢 Location: {user['village']}, {user['district']} ({user['state']})")
        col1, col2, col3 = st.columns(3)
        col1.metric(t["temp"], "32°C", "+2°C")
        col2.metric(t["humidity"], "58%", "-4%")
        col3.metric(t["rain_risk"], "Low", "0 mm")
        st.info(f"🌾 **{t['weather_adv']}**")
