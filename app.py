import streamlit as st
import requests

st.set_page_config(page_title="Krishi Procurement Platform", page_icon="🌾", layout="wide")

# Custom CSS for Language Selector Buttons
st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Language Selection State Initialization
if 'lang' not in st.session_state:
    st.session_state.lang = 'hi'

# Top Language Toggle Buttons
st.write("🌐 **Select Language / भाषा चुनें:**")
lang_col1, lang_col2, _ = st.columns([1, 1, 4])

with lang_col1:
    if st.button("🇮🇳 हिंदी (Hindi)", use_container_width=True):
        st.session_state.lang = 'hi'
        st.rerun()

with lang_col2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.lang = 'en'
        st.rerun()

is_hi = st.session_state.lang == 'hi'

# Title & Sidebar Navigation based on selected language
if is_hi:
    title = "🌾 कृषि प्लेटफॉर्म (Krishi Platform)"
    nav_title = "📌 मुख्य सेवाएं (Navigation)"
    modules = [
        "🌾 मंडी भाव और सरकारी MSP (Mandi Rates)",
        "🤖 AI फसल गुणवत्ता और भाव (AI Price Estimator)",
        "🗺️ मंडी भीड़ और ट्रैफिक (Rush Heatmap)",
        "🎙️ आवाज़ सहायक (Voice Assistant)",
        "📱 किसान स्लॉट बुकिंग (Slot Booking)", 
        "🚨 मंडी भीड़ अलर्ट (Rush Alerts)", 
        "💳 भुगतान स्थिति (Payment Status)",
        "🌤️ मौसम पूर्वानुमान (Weather)", 
        "📞 IVR / SMS सेवा (Non-Smartphone)"
    ]
else:
    title = "🌾 Krishi Platform"
    nav_title = "📌 Services Navigation"
    modules = [
        "🌾 Mandi Rates & Government MSP",
        "🤖 AI Crop Quality & Price Estimator",
        "🗺️ Live Mandi Rush & Traffic Heatmap",
        "🎙️ Voice Assistant for Farmers",
        "📱 Farmer Verification & Slot Booking", 
        "🚨 Live Mandi Rush Status", 
        "💳 Payment Status Check",
        "🌤️ Mandi Weather Report", 
        "📞 Non-Smartphone (IVR / SMS Simulation)"
    ]

st.title(title)
st.sidebar.title(nav_title)
choice = st.sidebar.radio("चुनें / Select:", modules)

# ==========================================
# MODULE 1: MANDI RATES & MSP
# ==========================================
if choice in ["🌾 मंडी भाव और सरकारी MSP (Mandi Rates)", "🌾 Mandi Rates & Government MSP"]:
    st.header("🌾 " + ("आज के मंडी भाव और सरकारी MSP दरें" if is_hi else "Live Mandi Rates & Government MSP Rates"))
    
    depot = st.selectbox("मंडी डिपो चुनें / Select Depot:" if is_hi else "Select Mandi Depot:", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
    st.subheader(f"📊 Rates for {depot}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌾 Wheat (गेहूं)")
        st.metric("Government MSP Rate", "₹ 2,275 / Qtl")
        st.write("**Today's Max:** ₹ 2,310 / Qtl" if is_hi else "**Today's Max:** ₹ 2,310 / Qtl")
        st.write("**Today's Min:** ₹ 2,250 / Qtl" if is_hi else "**Today's Min:** ₹ 2,250 / Qtl")

    with col2:
        st.markdown("### 🌾 Paddy (धान)")
        st.metric("Government MSP Rate", "₹ 2,183 / Qtl")
        st.write("**Today's Max:** ₹ 2,220 / Qtl" if is_hi else "**Today's Max:** ₹ 2,220 / Qtl")
        st.write("**Today's Min:** ₹ 2,150 / Qtl" if is_hi else "**Today's Min:** ₹ 2,150 / Qtl")

    with col3:
        st.markdown("### 🫘 Pulses (चना / दाल)")
        st.metric("Government MSP Rate", "₹ 5,440 / Qtl")
        st.write("**Today's Max:** ₹ 5,500 / Qtl" if is_hi else "**Today's Max:** ₹ 5,500 / Qtl")
        st.write("**Today's Min:** ₹ 5,380 / Qtl" if is_hi else "**Today's Min:** ₹ 5,380 / Qtl")

    st.divider()
    st.info("ℹ️ " + ("सरकारी केंद्रों पर खरीद केवल निर्धारित MSP दरों या उससे ऊपर की दरों पर ही की जाएगी।" if is_hi else "Procurement at government centers will strictly follow MSP guidelines."))

# ==========================================
# MODULE 2: AI QUALITY & PRICE ESTIMATOR
# ==========================================
elif choice in ["🤖 AI फसल गुणवत्ता और भाव (AI Price Estimator)", "🤖 AI Crop Quality & Price Estimator"]:
    st.header("🤖 " + ("AI फसल गुणवत्ता और मूल्य कैलकुलेटर" if is_hi else "AI-Powered Crop Quality & Price Calculator"))
    
    col1, col2 = st.columns(2)
    with col1:
        crop_type = st.selectbox("फसल चुनें / Select Crop", ["Wheat (गेहूं)", "Paddy (धान)", "Pulses (दाल)"])
        moisture = st.slider("नमी / Moisture Content (%)", 5.0, 25.0, 11.0)
        broken_grains = st.slider("टूटे दाने / Foreign Matter (%)", 0.0, 10.0, 1.5)
    
    base_msp = 2275 if "Wheat" in crop_type else (2183 if "Paddy" in crop_type else 5440)
    bonus = 0
    if moisture <= 12.0 and broken_grains <= 2.0:
        bonus = 85
        status = "🌟 ग्रेड A (उत्कृष्ट गुणवत्ता) - बोनस उपलब्ध!" if is_hi else "🌟 Grade A (Premium Quality) - Bonus Applicable!"
        color = "success"
    elif moisture <= 14.0:
        bonus = 0
        status = "✅ मानक गुणवत्ता - पूरा MSP मिलेगा" if is_hi else "✅ Standard Quality - Full MSP Applicable"
        color = "info"
    else:
        bonus = -120
        status = "⚠️ नमी अधिक है - फसल सुखाने की सलाह दी जाती है" if is_hi else "⚠️ High Moisture Content - Drying Recommended"
        color = "warning"
        
    final_price = base_msp + bonus
    
    with col2:
        st.subheader("📊 " + ("अनुमानित परिणाम" if is_hi else "Estimation Results"))
        st.metric("Base Government MSP", f"₹ {base_msp} / Qtl")
        st.metric("Estimated Selling Price", f"₹ {final_price} / Qtl", delta=f"₹ {bonus} Adjustment")
        
        if color == "success":
            st.success(status)
        elif color == "info":
            st.info(status)
        else:
            st.warning(status)

# ==========================================
# MODULE 3: RUSH HEATMAP
# ==========================================
elif choice in ["🗺️ मंडी भीड़ और ट्रैफिक (Rush Heatmap)", "🗺️ Live Mandi Rush & Traffic Heatmap"]:
    st.header("🗺️ " + ("मंडी भीड़ और ट्रैफिक हीटमैप" if is_hi else "Live Mandi Congestion & Traffic Heatmap"))
    depot = st.selectbox("मंडी / Depot:", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
    
    st.subheader(f"🚦 Status: {depot}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gate 1 (Weighbridge)", "85% Capacity", delta="HIGH RUSH", delta_color="inverse")
    col2.metric("Gate 2 (Unloading Dock)", "40% Capacity", delta="NORMAL", delta_color="normal")
    col3.metric("Parking Yard", "95% Full", delta="CRITICAL", delta_color="inverse")
    
    st.progress(0.85, text="Mandi Rush: 85% (Heavy Congestion)")
    st.warning("⚠️ " + ("गेट 1 पर भारी भीड़ है। कृपया Gate 2 की तरफ जाएं या 20 मिनट रुक कर आएं।" if is_hi else "Gate 1 is crowded. Route vehicle towards Gate 2 or delay by 20 mins."))

# ==========================================
# MODULE 4: VOICE ASSISTANT
# ==========================================
elif choice in ["🎙️ आवाज़ सहायक (Voice Assistant)", "🎙️ Voice Assistant for Farmers"]:
    st.header("🎙️ " + ("आवाज़ सहायक (बोलकर सहायता पाएं)" if is_hi else "Voice Assistant for Farmers"))
    
    voice_query = st.selectbox("बोला गया सवाल / Voice Query:", [
        "1. Gehun ka aaj ka bhav kya hai? (गेहूं का भाव)",
        "2. Central Mandi me bheed kitni hai? (मंडी भीड़)",
        "3. Mera payment kab aayega? (भुगतान की स्थिति)"
    ])
    
    if st.button("🔊 Play Voice Response (उत्तर सुनें)" if is_hi else "🔊 Play Voice Response"):
        if "bhav" in voice_query:
            st.success("🔊 [Audio]: Aaj Central Mandi me Gehun ka MSP bhav ₹2,275 per quintal hai.")
        elif "bheed" in voice_query:
            st.warning("🔊 [Audio]: Mandi me abhi bheed zyada hai, kripya 20 minute ruk kar aayein.")
        else:
            st.info("🔊 [Audio]: Aapka payment successfully bank account me bhej diya gaya hai.")

# ==========================================
# MODULE 5: SLOT BOOKING
# ==========================================
elif choice in ["📱 किसान स्लॉट बुकिंग (Slot Booking)", "📱 Farmer Verification & Slot Booking"]:
    st.header("🔐 " + ("किसान सत्यापन और टाइम स्लॉट बुकिंग" if is_hi else "Farmer Verification & Slot Booking"))
    
    with st.form("booking_form"):
        name = st.text_input("किसान का नाम / Farmer Name" if is_hi else "Farmer Name")
        phone = st.text_input("मोबाइल नंबर / Mobile Number (10 Digits)")
        id_num = st.text_input("आईडी सत्यापन / Verification ID (12 Digits Demo)", type="password")
        
        mandi = st.selectbox("मंडी / Mandi Depot", ["Central Grain Depot A", "Regional Mandi Hub B"])
        crop = st.selectbox("फसल / Crop", ["Wheat (गेहूं) @ ₹2,275/Qtl", "Paddy (धान) @ ₹2,183/Qtl"])
        slot = st.selectbox("समय / Time Slot", ["08:00 AM - 10:00 AM", "10:00 AM - 12:00 PM"])
        slot_date = st.date_input("तारीख / Date")
        
        submitted = st.form_submit_button("स्लॉट बुक करें" if is_hi else "Book Slot Now")
        
        if submitted:
            if len(phone) == 10 and phone.isdigit() and len(id_num) == 12 and id_num.isdigit() and name.strip():
                st.success(f"🎉 Slot Booked Successfully for {name}!")
                st.info(f"🆔 **Token ID:** TOKEN-[Aadhaar Redacted]")
            else:
                st.error("❌ Invalid Details! Kripya 10-digit Phone aur 12-digit ID Number sahi se bharein.")

# ==========================================
# MODULE 6: RUSH ALERTS
# ==========================================
elif choice in ["🚨 मंडी भीड़ अलर्ट (Rush Alerts)", "🚨 Live Mandi Rush Status"]:
    st.header("🚨 " + ("मंडी भीड़ और देरी अलर्ट" if is_hi else "Live Mandi Rush & Delay Alerts"))
    selected_mandi = st.selectbox("Mandi:", ["Central Grain Depot A", "Regional Mandi Hub B"])
    
    if selected_mandi == "Central Grain Depot A":
        st.error("🔴 HEAVY RUSH (भारी भीड़)")
        st.warning("⏳ **ALERT:** " + ("मंडी में भीड़ अधिक है। कृपया अपने स्लॉट से 20 मिनट देर से आएं।" if is_hi else "Mandi is crowded. Please arrive 20 minutes after your slot."))
    else:
        st.success("🟢 LOW RUSH (सामान्य स्थिति)")
        st.info("✅ " + ("भीड़ नहीं है, आप समय पर आ सकते हैं।" if is_hi else "No rush. You can arrive on time."))

# ==========================================
# MODULE 7: PAYMENT STATUS
# ==========================================
elif choice in ["💳 भुगतान स्थिति (Payment Status)", "💳 Payment Status Check"]:
    st.header("💳 " + ("डीबीटी भुगतान स्थिति" if is_hi else "Direct Benefit Transfer (DBT) Payment Status"))
    
    token_id = st.text_input("Token ID / Registration Number:", placeholder="e.g., TOKEN-1234")
    
    if st.button("स्थिति देखें" if is_hi else "Check Status"):
        if token_id.strip():
            col1, col2, col3 = st.columns(3)
            col1.metric("Weight Sold", "45 Qtl")
            col2.metric("MSP Amount", "₹ 1,02,375")
            col3.metric("Status", "SUCCESS")
            
            st.success("✅ Payment Processed via Direct Benefit Transfer (DBT)")
        else:
            st.error("Please enter a valid Token ID!")

# ==========================================
# MODULE 8: WEATHER
# ==========================================
elif choice in ["🌤️ मौसम पूर्वानुमान (Weather)", "🌤️ Mandi Weather Report"]:
    st.header("🌤️ " + ("मंडी मौसम रिपोर्ट" if is_hi else "Mandi Weather System"))
    city = st.text_input("शहर या जिला / City:", "Delhi")
    if st.button("मौसम देखें / Get Weather" if is_hi else "Get Weather"):
        api_key = "bd5e378503939ddaee76f12ad7a97608"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            res = requests.get(url).json()
            if res.get("cod") == 200:
                col1, col2, col3 = st.columns(3)
                col1.metric("Temp", f"{res['main']['temp']} °C")
                col2.metric("Humidity", f"{res['main']['humidity']} %")
                col3.metric("Weather", res['weather'][0]['description'].capitalize())
            else:
                st.error("❌ City not found!")
        except:
            st.error("⚠️ Weather service error.")

# ==========================================
# MODULE 9: IVR / SMS SIMULATION
# ==========================================
elif choice in ["📞 IVR / SMS सेवा (Non-Smartphone)", "📞 Non-Smartphone (IVR / SMS Simulation)"]:
    st.header("📞 Non-Smartphone / IVR Portal")
    st.caption("Toll-Free Helpline: 1800-180-1551")
    
    keypad_phone = st.text_input("मोबाइल नंबर / Mobile Number (10 Digits):")
    action = st.radio("चुनें / Select:", [
        "1. Voice Call Alert (कॉल अलर्ट)", 
        "2. SMS Slot Request (एसएमएस अनुरोध)", 
        "3. Mandi Rates SMS (मंडी भाव एसएमएस)"
    ])
    
    if st.button("भेजें / Send" if is_hi else "Execute Action"):
        if len(keypad_phone) == 10 and keypad_phone.isdigit():
            st.success(f"💬 Alert sent to {keypad_phone}!")
        else:
            st.error("❌ Invalid Mobile Number!")
