import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Krishi Platform", page_icon="🌾", layout="wide")

# Custom Styling for Clean UI
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 8px;
        height: 45px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Language
if 'lang' not in st.session_state:
    st.session_state.lang = 'hi'

# ==========================================
# LANGUAGE SELECTION BUTTONS (TOP)
# ==========================================
st.write("🌐 **भाषा चुनें / Select Platform Language:**")
lang_col1, lang_col2, _ = st.columns([1.5, 1.5, 5])

with lang_col1:
    if st.button("🇮🇳 हिंदी (Hindi)", use_container_width=True, type="primary" if st.session_state.lang == 'hi' else "secondary"):
        st.session_state.lang = 'hi'
        st.rerun()

with lang_col2:
    if st.button("🇬🇧 English", use_container_width=True, type="primary" if st.session_state.lang == 'en' else "secondary"):
        st.session_state.lang = 'en'
        st.rerun()

is_hi = (st.session_state.lang == 'hi')

# ==========================================
# TRANSLATION DATASETS
# ==========================================
if is_hi:
    title_text = "🌾 कृषि खरीद और स्लॉट प्रबंधन प्लेटफॉर्म"
    sub_text = "किसान सुविधा, मंडी भीड़ नियंत्रण एवं पारदर्शी खरीद प्रणाली"
    nav_title = "📌 मुख्य सेवाएं"
    modules = [
        "🌾 मंडी भाव और सरकारी MSP",
        "🤖 AI फसल गुणवत्ता एवं मूल्य कैलकुलेटर",
        "🗺️ लाइव मंडी भीड़ और ट्रैफिक मैप",
        "🎙️ आवाज़ सहायक (Voice Assistant)",
        "📱 किसान सत्यापन एवं स्लॉट बुकिंग", 
        "🚨 मंडी भीड़ एवं देरी अलर्ट", 
        "💳 DBT भुगतान स्थिति",
        "🌤️ मौसम पूर्वानुमान", 
        "📞 Non-Smartphone (IVR / SMS) सेवा"
    ]
    
    # Depot mapping for Pure Hindi
    depot_list = ["केंद्रीय अनाज डिपो ए", "क्षेत्रीय मंडी हब बी", "जिला डिपो सी"]
    crop_wheat = "गेहूं"
    crop_paddy = "धान"
    crop_pulses = "चना / दाल"
    msp_label = "सरकारी MSP दर"
    qtl_unit = "प्रति क्विंटल"
    max_price = "आज का अधिकतम भाव:"
    min_price = "आज का न्यूनतम भाव:"
else:
    title_text = "🌾 Krishi Procurement Platform"
    sub_text = "Digital Procurement, Slot Booking & Farmer Support System"
    nav_title = "📌 Main Services"
    modules = [
        "🌾 Live Mandi Rates & MSP",
        "🤖 AI Crop Quality & Price Estimator",
        "🗺️ Live Mandi Rush & Traffic Map",
        "🎙️ Voice Assistant for Farmers",
        "📱 Farmer Verification & Slot Booking", 
        "🚨 Live Rush & Delay Alerts", 
        "💳 DBT Payment Status",
        "🌤️ Mandi Weather Forecast", 
        "📞 Non-Smartphone (IVR / SMS) Service"
    ]
    
    depot_list = ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"]
    crop_wheat = "Wheat"
    crop_paddy = "Paddy"
    crop_pulses = "Pulses"
    msp_label = "Govt MSP Rate"
    qtl_unit = "per Qtl"
    max_price = "Today's Max Rate:"
    min_price = "Today's Min Rate:"

st.markdown(f"<div class='main-title'>{title_text}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>{sub_text}</div>", unsafe_allow_html=True)
st.divider()

st.sidebar.title(nav_title)
choice = st.sidebar.radio("सेवा चुनें / Choose Service:", modules)

# ==========================================
# MODULE 1: MANDI RATES & MSP (100% PURE HINDI / ENGLISH)
# ==========================================
if choice in ["🌾 मंडी भाव और सरकारी MSP", "🌾 Live Mandi Rates & MSP"]:
    st.header("🌾 " + ("आज के मंडी भाव और सरकारी MSP दरें" if is_hi else "Live Mandi Rates & Government MSP Rates"))
    
    depot = st.selectbox("मंडी केंद्र चुनें:" if is_hi else "Select Mandi Center:", depot_list)
    st.subheader(f"📊 {depot} - " + ("दर सूची (प्रति क्विंटल)" if is_hi else "Price List (Per Quintal)"))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### 🌾 {crop_wheat}")
        st.metric(msp_label, f"₹ 2,275 / {qtl_unit}")
        st.write(f"**{max_price}** ₹ 2,310 / {qtl_unit}")
        st.write(f"**{min_price}** ₹ 2,250 / {qtl_unit}")

    with col2:
        st.markdown(f"### 🌾 {crop_paddy}")
        st.metric(msp_label, f"₹ 2,183 / {qtl_unit}")
        st.write(f"**{max_price}** ₹ 2,220 / {qtl_unit}")
        st.write(f"**{min_price}** ₹ 2,150 / {qtl_unit}")

    with col3:
        st.markdown(f"### 🫘 {crop_pulses}")
        st.metric(msp_label, f"₹ 5,440 / {qtl_unit}")
        st.write(f"**{max_price}** ₹ 5,500 / {qtl_unit}")
        st.write(f"**{min_price}** ₹ 5,380 / {qtl_unit}")

    st.divider()
    st.info("ℹ️ " + ("सरकारी केंद्रों पर खरीद केवल निर्धारित MSP दरों या उससे ऊपर की दरों पर ही की जाएगी।" if is_hi else "Procurement at government centers strictly follows MSP or higher market guidelines."))

# ==========================================
# MODULE 2: AI QUALITY ESTIMATOR
# ==========================================
elif choice in ["🤖 AI फसल गुणवत्ता एवं मूल्य कैलकुलेटर", "🤖 AI Crop Quality & Price Estimator"]:
    st.header("🤖 " + ("AI फसल गुणवत्ता एवं मूल्य अनुमानक" if is_hi else "AI-Powered Quality & Price Estimator"))
    
    col1, col2 = st.columns(2)
    with col1:
        crop_options = ["गेहूं", "धान", "चना / दाल"] if is_hi else ["Wheat", "Paddy", "Pulses"]
        crop_type = st.selectbox("फसल चुनें:" if is_hi else "Select Crop:", crop_options)
        moisture = st.slider("नमी की मात्रा (%):" if is_hi else "Moisture Percentage (%):", 5.0, 25.0, 11.0)
        broken_grains = st.slider("टूटे दाने / कचरा (%):" if is_hi else "Broken Grains / Foreign Matter (%):", 0.0, 10.0, 1.5)
    
    base_msp = 2275 if crop_type in ["Wheat", "गेहूं"] else (2183 if crop_type in ["Paddy", "धान"] else 5440)
    bonus = 0
    if moisture <= 12.0 and broken_grains <= 2.0:
        bonus = 85
        status = "🌟 'A' ग्रेड गुणवत्ता - ₹85/क्विंटल प्रीमियम बोनस उपलब्ध!" if is_hi else "🌟 Grade 'A' Premium Quality - ₹85/Qtl Bonus Applicable!"
        color = "success"
    elif moisture <= 14.0:
        bonus = 0
        status = "✅ मानक गुणवत्ता - पूरा सरकारी MSP भाव मिलेगा।" if is_hi else "✅ Standard Quality - Full Government MSP Applicable."
        color = "info"
    else:
        bonus = -120
        status = "⚠️ नमी की मात्रा अधिक है - फसल को सुखाकर मंडी लाएं।" if is_hi else "⚠️ High Moisture Detected - Drying Recommended Before Selling."
        color = "warning"
        
    final_price = base_msp + bonus
    
    with col2:
        st.subheader("📊 " + ("मूल्य आकलन परिणाम" if is_hi else "Price Estimation Summary"))
        st.metric(msp_label, f"₹ {base_msp} / {qtl_unit}")
        st.metric("अनुमानित बिक्री भाव" if is_hi else "Estimated Selling Rate", f"₹ {final_price} / {qtl_unit}", delta=f"₹ {bonus} Quality Adjustment")
        
        if color == "success":
            st.success(status)
        elif color == "info":
            st.info(status)
        else:
            st.warning(status)

# ==========================================
# MODULE 3: RUSH HEATMAP
# ==========================================
elif choice in ["🗺️ लाइव मंडी भीड़ और ट्रैफिक मैप", "🗺️ Live Mandi Rush & Traffic Map"]:
    st.header("🗺️ " + ("लाइव मंडी भीड़ एवं गेट स्थिति" if is_hi else "Live Mandi Congestion & Zone Heatmap"))
    depot = st.selectbox("मंडी केंद्र:" if is_hi else "Mandi Hub:", depot_list)
    
    st.subheader(f"🚦 {depot}")
    col1, col2, col3 = st.columns(3)
    col1.metric("गेट 1 (धर्मकांटा / तौल)" if is_hi else "Gate 1 (Weighbridge)", "85%", delta="भारी भीड़" if is_hi else "HIGH RUSH", delta_color="inverse")
    col2.metric("गेट 2 (अनलोडिंग यार्ड)" if is_hi else "Gate 2 (Unloading Yard)", "40%", delta="सामान्य" if is_hi else "NORMAL", delta_color="normal")
    col3.metric("पार्र्किंग ज़ोन" if is_hi else "Parking Zone", "95%", delta="फूल" if is_hi else "CRITICAL", delta_color="inverse")
    
    st.progress(0.85, text="मंडी क्षमता स्तर: 85% (भारी भीड़)" if is_hi else "Mandi Capacity Level: 85%")
    st.warning("⚠️ " + ("गेट 1 पर भारी भीड़ है। कृपया गेट 2 की तरफ जाएं या अपने आगमन में 20 मिनट का विलंब करें।" if is_hi else "Gate 1 is experiencing heavy rush. Please divert to Gate 2 or delay arrival by 20 minutes."))

# ==========================================
# MODULE 4: VOICE ASSISTANT
# ==========================================
elif choice in ["🎙️ आवाज़ सहायक (Voice Assistant)", "🎙️ Voice Assistant for Farmers"]:
    st.header("🎙️ " + ("आवाज़ सहायक" if is_hi else "Voice Assistant for Farmers"))
    
    voice_query = st.selectbox("सवाल चुनें:" if is_hi else "Select Voice Simulation:", [
        "1. गेहूं का आज का भाव क्या है?",
        "2. केंद्रीय मंडी में भीड़ कितनी है?",
        "3. मेरा भुगतान कब आएगा?"
    ] if is_hi else [
        "1. What is today's wheat rate?",
        "2. What is the current rush in central mandi?",
        "3. When will my payment arrive?"
    ])
    
    if st.button("🔊 " + ("उत्तर सुनें" if is_hi else "Play Audio Response")):
        if "bhav" in voice_query or "rate" in voice_query or "गेहूं" in voice_query:
            st.success("🔊 " + ("[ऑडियो]: आज केंद्रीय मंडी में गेहूं का सरकारी भाव ₹2,275 प्रति क्विंटल है।" if is_hi else "[Audio]: Today's Wheat MSP rate at Central Mandi is ₹2,275 per quintal."))
        elif "bheed" in voice_query or "rush" in voice_query or "भीड़" in voice_query:
            st.warning("🔊 " + ("[ऑडियो]: मंडी में अभी भीड़ अधिक है, कृपया 20 मिनट रुक कर आएं।" if is_hi else "[Audio]: High rush in Mandi right now, please arrive after 20 minutes."))
        else:
            st.info("🔊 " + ("[ऑडियो]: आपका भुगतान बैंक खाते में सफलतापूर्वक भेज दिया गया है।" if is_hi else "[Audio]: Your payment has been credited to your bank account successfully."))

# ==========================================
# MODULE 5: SLOT BOOKING
# ==========================================
elif choice in ["📱 किसान सत्यापन एवं स्लॉट बुकिंग", "📱 Farmer Verification & Slot Booking"]:
    st.header("🔐 " + ("किसान सत्यापन और समय स्लॉट बुकिंग" if is_hi else "Farmer Verification & Time Slot Booking"))
    
    with st.form("booking_form"):
        name = st.text_input("किसान का पूरा नाम:" if is_hi else "Farmer Full Name:")
        phone = st.text_input("मोबाइल नंबर (10 अंक):" if is_hi else "Mobile Number (10 Digits):")
        id_num = st.text_input("सत्यापन आईडी (12 अंक):" if is_hi else "Verification ID (12 Digits):", type="password")
        
        mandi = st.selectbox("मंडी केंद्र:" if is_hi else "Mandi Center:", depot_list)
        crop = st.selectbox("फसल:" if is_hi else "Crop:", ["गेहूं @ ₹2,275/क्विंटल", "धान @ ₹2,183/क्विंटल"] if is_hi else ["Wheat @ ₹2,275/Qtl", "Paddy @ ₹2,183/Qtl"])
        slot = st.selectbox("समय स्लॉट:" if is_hi else "Preferred Time Slot:", ["08:00 सुबह - 10:00 सुबह", "10:00 सुबह - 12:00 दोपहर", "02:00 दोपहर - 04:00 शाम"] if is_hi else ["08:00 AM - 10:00 AM", "10:00 AM - 12:00 PM", "02:00 PM - 04:00 PM"])
        slot_date = st.date_input("तारीख:" if is_hi else "Date:")
        
        submitted = st.form_submit_button("स्लॉट बुक करें" if is_hi else "Confirm & Book Slot")
        
        if submitted:
            if len(phone) == 10 and phone.isdigit() and len(id_num) == 12 and id_num.isdigit() and name.strip():
                st.success("🎉 " + (f"स्लॉट सफलतापूर्वक बुक हो गया है, {name}!" if is_hi else f"Slot Booked Successfully for {name}!"))
                st.info(f"🆔 **टोकन आईडी / Token ID:** TOKEN-{id_num[-4:]}")
            else:
                st.error("❌ " + ("गलत जानकारी! कृपया 10 अंकों का फोन और 12 अंकों का ID नंबर सही भरें।" if is_hi else "Invalid Input! Please enter valid 10-digit Phone and 12-digit ID."))

# ==========================================
# MODULE 6: RUSH ALERTS
# ==========================================
elif choice in ["🚨 मंडी भीड़ एवं देरी अलर्ट", "🚨 Live Rush & Delay Alerts"]:
    st.header("🚨 " + ("मंडी भीड़ और देरी अलर्ट" if is_hi else "Live Mandi Rush & Delay Status"))
    selected_mandi = st.selectbox("मंडी चुनें:" if is_hi else "Select Mandi:", depot_list)
    
    if selected_mandi in ["केंद्रीय अनाज डिपो ए", "Central Grain Depot A"]:
        st.error("🔴 " + ("भारी भीड़" if is_hi else "HEAVY CONGESTION"))
        st.warning("⏳ **अलर्ट:** " + ("मंडी में भीड़ अधिक है। कृपया अपने स्लॉट से 20 मिनट बाद आएं।" if is_hi else "Heavy traffic reported. Please arrive 20 minutes after your designated slot."))
    else:
        st.success("🟢 " + ("सामान्य स्थिति" if is_hi else "NORMAL RUSH"))
        st.info("✅ " + ("मंडी में भीड़ नहीं है। आप अपने निर्धारित समय पर आ सकते हैं।" if is_hi else "Traffic is normal. You may arrive exactly on time."))

# ==========================================
# MODULE 7: PAYMENT STATUS
# ==========================================
elif choice in ["💳 DBT भुगतान स्थिति", "💳 DBT Payment Status"]:
    st.header("💳 " + ("डीबीटी (DBT) भुगतान स्थिति जांच" if is_hi else "Direct Benefit Transfer (DBT) Payment Status"))
    
    token_id = st.text_input("टोकन आईडी दर्ज करें:" if is_hi else "Enter Token ID / Registration No:", placeholder="e.g., TOKEN-1234")
    
    if st.button("स्थिति देखें" if is_hi else "Search Status"):
        if token_id.strip():
            col1, col2, col3 = st.columns(3)
            col1.metric("कुल बेचा गया वजन" if is_hi else "Total Weight Sold", f"45 {qtl_unit}")
            col2.metric("कुल भुगतान राशि" if is_hi else "Total MSP Amount", "₹ 1,02,375")
            col3.metric("भुगतान की स्थिति" if is_hi else "Payment Status", "सफल" if is_hi else "SUCCESS")
            
            st.success("✅ " + ("भुगतान डायरेक्ट बेनिफिट ट्रांसफर (DBT) के माध्यम से बैंक खाते में भेज दिया गया है।" if is_hi else "Payment successfully processed via Direct Benefit Transfer (DBT)."))
        else:
            st.error("कृपया सही टोकन आईडी भरें!" if is_hi else "Please enter a valid Token ID!")

# ==========================================
# MODULE 8: WEATHER FORECAST
# ==========================================
elif choice in ["🌤️ मौसम पूर्वानुमान", "🌤️ Mandi Weather Forecast"]:
    st.header("🌤️ " + ("मंडी मौसम रिपोर्ट" if is_hi else "Mandi Local Weather System"))
    city = st.text_input("शहर या ज़िला दर्ज करें:" if is_hi else "Enter District/City:", "Delhi")
    if st.button("मौसम जांचें" if is_hi else "Get Weather Report"):
        api_key = "bd5e378503939ddaee76f12ad7a97608"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            res = requests.get(url).json()
            if res.get("cod") == 200:
                col1, col2, col3 = st.columns(3)
                col1.metric("तापमान" if is_hi else "Temperature", f"{res['main']['temp']} °C")
                col2.metric("नमी" if is_hi else "Humidity", f"{res['main']['humidity']} %")
                col3.metric("मौसम" if is_hi else "Condition", res['weather'][0]['description'].capitalize())
            else:
                st.error("❌ शहर नहीं मिला!" if is_hi else "❌ City not found!")
        except:
            st.error("⚠️ मौसम सेवा त्रुटि।" if is_hi else "⚠️ Weather API error.")

# ==========================================
# MODULE 9: IVR / SMS SIMULATION
# ==========================================
elif choice in ["📞 Non-Smartphone (IVR / SMS) सेवा", "📞 Non-Smartphone (IVR / SMS) Service"]:
    st.header("📞 " + ("गैर-स्मार्टफोन (IVR / SMS) सेवा" if is_hi else "Non-Smartphone (IVR / SMS) System"))
    st.caption("टोल-फ्री हेल्पलाइन: 1800-180-1551" if is_hi else "Toll-Free Helpline: 1800-180-1551")
    
    keypad_phone = st.text_input("किसान का मोबाइल नंबर (10 अंक):" if is_hi else "Farmer Mobile Number (10 Digits):")
    action = st.radio("सेवा चुनें:" if is_hi else "Select IVR Action:", [
        "1. कॉल अलर्ट (Outbound Voice Call)", 
        "2. एसएमएस स्लॉट अनुरोध (SMS Slot Request)", 
        "3. मंडी भाव एसएमएस (Mandi Rates SMS)"
    ] if is_hi else [
        "1. Outbound Voice Call Alert", 
        "2. SMS Slot Request", 
        "3. Mandi Rates SMS"
    ])
    
    if st.button("भेजें" if is_hi else "Execute Service"):
        if len(keypad_phone) == 10 and keypad_phone.isdigit():
            st.success("💬 " + (f"एसएमएस {keypad_phone} पर सफलतापूर्वक भेज दिया गया है!" if is_hi else f"Alert SMS successfully dispatched to {keypad_phone}!"))
        else:
            st.error("❌ " + ("अमान्य मोबाइल नंबर!" if is_hi else "Invalid Mobile Number!"))
