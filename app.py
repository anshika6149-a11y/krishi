import streamlit as st
import requests
import random

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform", 
    page_icon="🌾", 
    layout="centered"  # App-like narrow centered view
)

# Custom Mobile App Styling
st.markdown("""
    <style>
    /* App Top Bar */
    .app-bar {
        background: linear-gradient(135deg, #1E3A8A, #1D4ED8);
        padding: 18px 20px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(30, 58, 138, 0.25);
    }
    .app-bar h1 {
        color: #FFFFFF !important;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .app-bar p {
        color: #E0E7FF;
        margin-top: 4px;
        font-size: 0.88rem;
    }
    /* Token Card Styling */
    .pass-card {
        background: #F0FDF4;
        border: 2px solid #22C55E;
        padding: 18px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Button Tweaks */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
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
# 1. APP HEADER & LANGUAGE SWITCHER (TOPMOST)
# ==========================================
is_hi = (st.session_state.lang == 'hi')

# Top Header Banner
st.markdown(f"""
    <div class="app-bar">
        <h1>🌾 KRISHI PLATFORM</h1>
        <p>{"डिजिटल मंडी खरीद एवं किसान पास पोर्टल" if is_hi else "Digital Procurement & Farmer Verification Portal"}</p>
    </div>
""", unsafe_allow_html=True)

# Language Selector - Right under the header!
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
    st.subheader("🔐 " + ("किसान पंजीकरण / लॉगिन" if is_hi else "Farmer Login & Entry Pass"))
    st.info("ℹ️ " + ("मंडी में प्रवेश और स्लॉट बुकिंग के लिए अपना आधार और मोबाइल नंबर दर्ज करें।" if is_hi else "Enter Aadhaar and Mobile Number to generate your official Mandi Entry Pass."))

    with st.form("registration_form"):
        farmer_name = st.text_input("किसान का पूरा नाम *" if is_hi else "Farmer Full Name *", placeholder="e.g. Ramesh Kumar")
        aadhaar_no = st.text_input("आधार कार्ड नंबर (12 अंक) *" if is_hi else "Aadhaar Card Number (12 Digits) *", type="password", max_chars=12)
        mobile_no = st.text_input("मोबाइल नंबर (10 अंक) *" if is_hi else "Mobile Number (10 Digits) *", max_chars=10)
        district = st.text_input("ज़िला / मंडी क्षेत्र *" if is_hi else "District / Mandi Region *", placeholder="e.g. Meerut / Delhi")

        submit_reg = st.form_submit_button("पंजीकरण करें और पास प्राप्त करें 🎫" if is_hi else "Register & Get Mandi Pass 🎫", use_container_width=True, type="primary")

        if submit_reg:
            if len(aadhaar_no) == 12 and aadhaar_no.isdigit() and len(mobile_no) == 10 and mobile_no.isdigit() and farmer_name.strip():
                # Generate Unique Security Gate Token ID
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
# 3. MAIN APP DASHBOARD (AFTER LOGIN)
# ==========================================
else:
    user = st.session_state.user_data
    
    # User Gate Pass / Guard Token Card
    st.markdown(f"""
        <div class="pass-card">
            <span style="background:#22C55E; color:white; padding:3px 10px; border-radius:12px; font-size:0.8rem; font-weight:bold;">
                {"मंडी प्रवेश पास (VERIFIED)" if is_hi else "MANDI ENTRY PASS (VERIFIED)"}
            </span>
            <h2 style="color: #15803D; margin:10px 0 5px 0;">🆔 {user['token_id']}</h2>
            <p style="margin:2px 0; font-weight:bold;">{"किसान:" if is_hi else "Farmer:"} {user['name']} | {"आधार:" if is_hi else "Aadhaar:"} {user['aadhaar_masked']}</p>
            <p style="margin:2px 0; color:#4B5563; font-size:0.9rem;">{"मोबाइल:" if is_hi else "Mobile:"} {user['mobile']} | {"क्षेत्र:" if is_hi else "Region:"} {user['district']}</p>
            <hr style="border-top: 1px dashed #22C55E; margin:10px 0;">
            <p style="color:#DC2626; font-size:0.85rem; font-weight:bold; margin:0;">
                🛡️ {"गेट सुरक्षा अलर्ट: मंडी में प्रवेश के लिए सुरक्षा गार्ड को यह टोकन नंबर दिखाएं।" if is_hi else "SECURITY NOTICE: Show this Token ID to the Gate Guard for entry."}
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
        "🤖 AI फसल गुणवत्ता एवं मूल्य कैलकुलेटर",
        "🗺️ लाइव मंडी भीड़ और ट्रैफिक मैप",
        "🎙️ आवाज़ सहायक (Voice Assistant)",
        "📱 टाइम स्लॉट बुकिंग", 
        "🚨 मंडी भीड़ एवं देरी अलर्ट", 
        "💳 DBT भुगतान स्थिति",
        "🌤️ मौसम पूर्वानुमान", 
        "📞 Non-Smartphone (IVR / SMS) सेवा"
    ] if is_hi else [
        "🌾 Live Mandi Rates & MSP",
        "🤖 AI Crop Quality & Price Estimator",
        "🗺️ Live Mandi Rush & Traffic Map",
        "🎙️ Voice Assistant for Farmers",
        "📱 Time Slot Booking", 
        "🚨 Live Rush & Delay Alerts", 
        "💳 DBT Payment Status",
        "🌤️ Mandi Weather Forecast", 
        "📞 Non-Smartphone (IVR / SMS) Service"
    ]

    st.sidebar.title("📌 " + ("मुख्य सेवाएं" if is_hi else "Main Services"))
    choice = st.sidebar.radio("सेवा चुनें / Select Service:", modules)

    depot_list = ["केंद्रीय अनाज डिपो ए", "क्षेत्रीय मंडी हब बी", "जिला डिपो सी"] if is_hi else ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"]

    # --- MODULE 1: MANDI RATES ---
    if choice in ["🌾 मंडी भाव और सरकारी MSP", "🌾 Live Mandi Rates & MSP"]:
        st.header("🌾 " + ("आज के मंडी भाव और सरकारी MSP दरें" if is_hi else "Live Mandi Rates & Government MSP Rates"))
        depot = st.selectbox("मंडी केंद्र चुनें:" if is_hi else "Select Mandi Center:", depot_list)
        st.subheader(f"📊 {depot} - " + ("दर सूची (प्रति क्विंटल)" if is_hi else "Price List (Per Quintal)"))
        
        col1, col2, col3 = st.columns(3)
        qtl_unit = "प्रति क्विंटल" if is_hi else "per Qtl"
        
        with col1:
            st.markdown("### 🌾 " + ("गेहूं" if is_hi else "Wheat"))
            st.metric("सरकारी MSP दर" if is_hi else "Govt MSP Rate", f"₹ 2,275 / {qtl_unit}")
            st.write(f"**{'आज का अधिकतम भाव:' if is_hi else 'Today\'s Max Rate:'}** ₹ 2,310")
            st.write(f"**{'आज का न्यूनतम भाव:' if is_hi else 'Today\'s Min Rate:'}** ₹ 2,250")

        with col2:
            st.markdown("### 🌾 " + ("धान" if is_hi else "Paddy"))
            st.metric("सरकारी MSP दर" if is_hi else "Govt MSP Rate", f"₹ 2,183 / {qtl_unit}")
            st.write(f"**{'आज का अधिकतम भाव:' if is_hi else 'Today\'s Max Rate:'}** ₹ 2,220")
            st.write(f"**{'आज का न्यूनतम भाव:' if is_hi else 'Today\'s Min Rate:'}** ₹ 2,150")

        with col3:
            st.markdown("### 🫘 " + ("चना / दाल" if is_hi else "Pulses"))
            st.metric("सरकारी MSP दर" if is_hi else "Govt MSP Rate", f"₹ 5,440 / {qtl_unit}")
            st.write(f"**{'आज का अधिकतम भाव:' if is_hi else 'Today\'s Max Rate:'}** ₹ 5,500")
            st.write(f"**{'आज का न्यूनतम भाव:' if is_hi else 'Today\'s Min Rate:'}** ₹ 5,380")

    # --- MODULE 2: AI QUALITY ESTIMATOR ---
    elif choice in ["🤖 AI फसल गुणवत्ता एवं मूल्य कैलकुलेटर", "🤖 AI Crop Quality & Price Estimator"]:
        st.header("🤖 " + ("AI फसल गुणवत्ता एवं मूल्य अनुमानक" if is_hi else "AI-Powered Quality & Price Estimator"))
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
            st.subheader("📊 " + ("मूल्य आकलन परिणाम" if is_hi else "Price Estimation Summary"))
            st.metric("सरकारी MSP दर" if is_hi else "Govt MSP Rate", f"₹ {base_msp} / क्विंटल")
            st.metric("अनुमानित बिक्री भाव" if is_hi else "Estimated Selling Rate", f"₹ {final_price} / क्विंटल", delta=f"₹ {bonus} Quality Adjustment")

    # --- MODULE 3: RUSH HEATMAP ---
    elif choice in ["🗺️ लाइव मंडी भीड़ और ट्रैफिक मैप", "🗺️ Live Mandi Rush & Traffic Map"]:
        st.header("🗺️ " + ("लाइव मंडी भीड़ एवं गेट स्थिति" if is_hi else "Live Mandi Congestion & Zone Heatmap"))
        depot = st.selectbox("मंडी केंद्र:" if is_hi else "Mandi Hub:", depot_list)
        col1, col2, col3 = st.columns(3)
        col1.metric("गेट 1 (धर्मकांटा)" if is_hi else "Gate 1 (Weighbridge)", "85%", delta="भारी भीड़" if is_hi else "HIGH RUSH", delta_color="inverse")
        col2.metric("गेट 2 (अनलोडिंग यार्ड)" if is_hi else "Gate 2 (Unloading Yard)", "40%", delta="सामान्य" if is_hi else "NORMAL", delta_color="normal")
        col3.metric("पार्र्किंग ज़ोन" if is_hi else "Parking Zone", "95%", delta="फूल" if is_hi else "CRITICAL", delta_color="inverse")
        st.warning("⚠️ " + ("गेट 1 पर भारी भीड़ है। सुरक्षा गार्ड केवल गेट pass टोकन धारकों को गेट 2 से जाने दे रहे हैं।" if is_hi else "Gate 1 heavy rush. Guards diverting token holders to Gate 2."))

    # --- MODULE 4: VOICE ASSISTANT ---
    elif choice in ["🎙️ आवाज़ सहायक (Voice Assistant)", "🎙️ Voice Assistant for Farmers"]:
        st.header("🎙️ " + ("आवाज़ सहायक" if is_hi else "Voice Assistant for Farmers"))
        voice_query = st.selectbox("सवाल चुनें:" if is_hi else "Select Voice Simulation:", [
            "1. गेहूं का आज का भाव क्या है?",
            "2. केंद्रीय मंडी में भीड़ कितनी है?",
            "3. मेरा गार्ड पास टोकन नंबर क्या है?"
        ] if is_hi else [
            "1. What is today's wheat rate?",
            "2. What is the current rush in central mandi?",
            "3. What is my Guard Pass Token ID?"
        ])
        if st.button("🔊 " + ("उत्तर सुनें" if is_hi else "Play Audio Response")):
            if "bhav" in voice_query or "rate" in voice_query or "गेहूं" in voice_query:
                st.success("🔊 " + ("[ऑडियो]: आज गेहूं का सरकारी भाव ₹2,275 प्रति क्विंटल है।" if is_hi else "[Audio]: Today's Wheat MSP rate is ₹2,275 per quintal."))
            elif "token" in voice_query or "टोकन" in voice_query or "पास" in voice_query:
                st.info(f"🔊 [ऑडियो]: आपका गेट पास टोकन आईडी है {user['token_id']}।")
            else:
                st.warning("🔊 " + ("[ऑडियो]: मंडी गेट 1 पर भीड़ अधिक है, गेट 2 से प्रवेश करें।" if is_hi else "[Audio]: High rush at Gate 1, please enter through Gate 2."))

    # --- MODULE 5: SLOT BOOKING ---
    elif choice in ["📱 टाइम स्लॉट बुकिंग", "📱 Time Slot Booking"]:
        st.header("📱 " + ("मंडी आगमन टाइम स्लॉट बुकिंग" if is_hi else "Mandi Arrival Time Slot Booking"))
        st.write(f"**किसान:** {user['name']} | **गेट पास टोकन:** `{user['token_id']}`")
        
        with st.form("slot_form"):
            mandi = st.selectbox("मंडी केंद्र:" if is_hi else "Mandi Center:", depot_list)
            crop = st.selectbox("फसल:" if is_hi else "Crop:", ["गेहूं @ ₹2,275/क्विंटल", "धान @ ₹2,183/क्विंटल"] if is_hi else ["Wheat @ ₹2,275/Qtl", "Paddy @ ₹2,183/Qtl"])
            slot_time = st.selectbox("समय स्लॉट:" if is_hi else "Preferred Time Slot:", ["08:00 AM - 10:00 AM", "10:00 AM - 12:00 PM", "02:00 PM - 04:00 PM"])
            slot_date = st.date_input("तारीख:" if is_hi else "Date:")
            
            book_btn = st.form_submit_button("स्लॉट पक्का करें 📅" if is_hi else "Confirm Slot Booking 📅", type="primary")
            if book_btn:
                st.success("🎉 " + (f"स्लॉट बुक हो गया! टोकन आईडी {user['token_id']} के साथ {slot_date} को {slot_time} पर पहुंचे।" if is_hi else f"Slot Booked! Arrive on {slot_date} at {slot_time} with Token {user['token_id']}."))

    # --- MODULE 6: RUSH ALERTS ---
    elif choice in ["🚨 मंडी भीड़ एवं देरी अलर्ट", "🚨 Live Rush & Delay Alerts"]:
        st.header("🚨 " + ("मंडी भीड़ और सुरक्षा अलर्ट" if is_hi else "Live Mandi Rush & Delay Status"))
        st.error("🔴 " + ("गेट 1 पर भारी भीड़ है।" if is_hi else "Heavy Rush reported at Gate 1."))
        st.info("🛡️ " + ("सुरक्षा गार्ड केवल टोकन पास दिखाने पर ही एंट्री दे रहे हैं।" if is_hi else "Guards allowing entry strictly with valid Token Pass."))

    # --- MODULE 7: PAYMENT STATUS ---
    elif choice in ["💳 DBT भुगतान स्थिति", "💳 DBT Payment Status"]:
        st.header("💳 " + ("डीबीटी (DBT) भुगतान स्थिति" if is_hi else "Direct Benefit Transfer (DBT) Payment Status"))
        st.write(f"**पास टोकन आईडी:** `{user['token_id']}` | **किसान:** {user['name']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("बेचा गया वजन" if is_hi else "Weight Sold", "45 क्विंटल")
        col2.metric("भुगतान राशि" if is_hi else "Amount Credited", "₹ 1,02,375")
        col3.metric("स्थिति" if is_hi else "Status", "सफल / SUCCESS")

    # --- MODULE 8: WEATHER ---
    elif choice in ["🌤️ मौसम पूर्वानुमान", "🌤️ Mandi Weather Forecast"]:
        st.header("🌤️ " + ("मंडी मौसम रिपोर्ट" if is_hi else "Mandi Local Weather System"))
        city = st.text_input("शहर / ज़िला:" if is_hi else "District/City:", user['district'] if user['district'] else "Delhi")
        if st.button("मौसम जांचें" if is_hi else "Get Weather Report"):
            try:
                res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=bd5e378503939ddaee76f12ad7a97608&units=metric").json()
                if res.get("cod") == 200:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("तापमान" if is_hi else "Temp", f"{res['main']['temp']} °C")
                    col2.metric("नमी" if is_hi else "Humidity", f"{res['main']['humidity']} %")
                    col3.metric("मौसम" if is_hi else "Condition", res['weather'][0]['description'].capitalize())
                else:
                    st.error("❌ " + ("शहर नहीं मिला!" if is_hi else "City not found!"))
            except:
                st.error("⚠️ Weather API error.")

    # --- MODULE 9: IVR / SMS ---
    elif choice in ["📞 Non-Smartphone (IVR / SMS) सेवा", "📞 Non-Smartphone (IVR / SMS) Service"]:
        st.header("📞 " + ("गैर-स्मार्टफोन (IVR / SMS) सेवा" if is_hi else "Non-Smartphone (IVR / SMS) System"))
        st.write(f"**रजिस्टर्ड मोबाइल:** {user['mobile']}")
        if st.button("टोकन पास का SMS भेजें" if is_hi else "Send Token Pass via SMS"):
            st.success(f"💬 SMS Sent to {user['mobile']}: 'Aapka Gate Entry Pass Token: {user['token_id']} hai. Mandi guard ko ise dikhayein.'")
