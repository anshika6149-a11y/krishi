import streamlit as st
import requests

st.set_page_config(page_title="Smart Krishi Procurement Platform", page_icon="🌾", layout="wide")

# Sidebar Language Selection
lang = st.sidebar.selectbox("🌐 Select Language / भाषा चुनें", ["Hindi (हिंदी)", "English"])

# Text Dictionary for Multi-language Navigation
if lang == "Hindi (हिंदी)":
    title = "🌾 स्मार्ट कृषि खरीद मंच (Smart Krishi Platform)"
    nav_title = "नेविगेशन (Navigation)"
    modules = [
        "🤖 AI फसल गुणवत्ता और भाव कैलकुलेटर (AI Quality Predictor)",
        "🗺️ मंडी भीड़ और ट्रैफिक हीटमैप (Live Rush Heatmap)",
        "🎙️ आवाज़ सहायक (Voice-Based Assistant)",
        "🌾 मंडी भाव और न्यूनतम समर्थन मूल्य (Mandi Rates & MSP)",
        "📱 किसान सत्यापन और स्लॉट बुकिंग", 
        "🚨 मंडी भीड़ स्थिति (Rush Status)", 
        "💳 भुगतान स्थिति (Payment Status)",
        "🌤️ मौसम की जानकारी (Weather)", 
        "📞 IVR / SMS सेवा (Non-Smartphone)"
    ]
else:
    title = "🌾 Smart Krishi Procurement Platform"
    nav_title = "Navigation"
    modules = [
        "🤖 AI Crop Quality & Price Estimator",
        "🗺️ Live Mandi Rush & Traffic Heatmap",
        "🎙️ Voice Assistant for Farmers",
        "🌾 Live Mandi Rates & MSP",
        "📱 Farmer Verification & Slot Booking", 
        "🚨 Live Mandi Rush Status", 
        "💳 Payment Status Check",
        "🌤️ Mandi Weather Report", 
        "📞 Non-Smartphone (IVR / SMS Simulation)"
    ]

st.title(title)
st.sidebar.title(nav_title)
choice = st.sidebar.radio("Select Module:", modules)

# ==========================================
# FEATURE 1: AI QUALITY & PRICE PREDICTOR
# ==========================================
if choice in ["🤖 AI फसल गुणवत्ता और भाव कैलकुलेटर (AI Quality Predictor)", "🤖 AI Crop Quality & Price Estimator"]:
    st.header("🤖 " + ("AI फसल गुणवत्ता और मूल्य कैलकुलेटर" if lang == "Hindi (हिंदी)" else "AI-Powered Crop Quality & Price Calculator"))
    st.caption("Calculate bonus prices based on moisture and grain quality parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        crop_type = st.selectbox("Select Crop / फसल चुनें", ["Wheat (गेहूं)", "Paddy (धान)", "Pulses (दाल)"])
        moisture = st.slider("Moisture Content / नमी (%)", 5.0, 25.0, 11.0)
        broken_grains = st.slider("Foreign Matter / टूटे दाने (%)", 0.0, 10.0, 1.5)
    
    # AI Estimation Logic
    base_msp = 2275 if "Wheat" in crop_type else (2183 if "Paddy" in crop_type else 5440)
    bonus = 0
    if moisture <= 12.0 and broken_grains <= 2.0:
        bonus = 85  # Grade A Premium
        status = "🌟 Grade A (Premium Quality) - Bonus Applicable!" if lang == "English" else "🌟 ग्रेड A (उत्कृष्ट गुणवत्ता) - बोनस उपलब्ध!"
        color = "success"
    elif moisture <= 14.0:
        bonus = 0
        status = "✅ Standard Quality - Full MSP Applicable" if lang == "English" else "✅ मानक गुणवत्ता - पूरा MSP मिलेगा"
        color = "info"
    else:
        bonus = -120
        status = "⚠️ High Moisture Content - Drying Recommended" if lang == "English" else "⚠️ नमी अधिक है - सुखाने की सलाह दी जाती है"
        color = "warning"
        
    final_price = base_msp + bonus
    
    with col2:
        st.subheader("📊 Price Estimation Results")
        st.metric("Base Government MSP", f"₹ {base_msp} / Qtl")
        st.metric("Estimated Mandi Selling Price", f"₹ {final_price} / Qtl", delta=f"₹ {bonus} Quality Adjustment")
        
        if color == "success":
            st.success(status)
        elif color == "info":
            st.info(status)
        else:
            st.warning(status)

# ==========================================
# FEATURE 2: MANDI RUSH HEATMAP & TRAFFIC
# ==========================================
elif choice in ["🗺️ मंडी भीड़ और ट्रैफिक हीटमैप (Live Rush Heatmap)", "🗺️ Live Mandi Rush & Traffic Heatmap"]:
    st.header("🗺️ " + ("मंडी भीड़ और ट्रैफिक हीटमैप" if lang == "Hindi (हिंदी)" else "Live Mandi Congestion & Traffic Heatmap"))
    depot = st.selectbox("Select Depot / Mandi", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
    
    st.subheader(f"🚦 Real-Time Zone Status for {depot}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gate 1 (Weighbridge)", "85% Capacity", delta="HIGH RUSH", delta_color="inverse")
    col2.metric("Gate 2 (Unloading Dock)", "40% Capacity", delta="NORMAL", delta_color="normal")
    col3.metric("Parking Yard", "95% Full", delta="CRITICAL", delta_color="inverse")
    
    st.progress(0.85, text="Overall Depot Congestion Level: 85% (Heavy Rush)")
    st.warning("⚠️ **Smart Recommendation:** Gate 1 is crowded. Please route your vehicle towards **Gate 2** or delay arrival by **20 minutes**.")

# ==========================================
# FEATURE 3: VOICE ASSISTANT SIMULATION
# ==========================================
elif choice in ["🎙️ आवाज़ सहायक (Voice-Based Assistant)", "🎙️ Voice Assistant for Farmers"]:
    st.header("🎙️ " + ("आवाज़ सहायक (बोलकर सहायता पाएं)" if lang == "Hindi (हिंदी)" else "Voice Assistant for Farmers"))
    st.caption("Designed for illiterate or non-tech savvy farmers")
    
    voice_query = st.selectbox("Simulate Voice Command (बोला गया सवाल):", [
        "1. Gehun ka aaj ka bhav kya hai? (गेहूं का भाव)",
        "2. Central Mandi me bheed kitni hai? (मंडी भीड़)",
        "3. Mera payment kab aayega? (भुगतान की स्थिति)"
    ])
    
    if st.button("🔊 Play Voice Response (उत्तर सुनें)"):
        if "bhav" in voice_query:
            st.success("🔊 [Audio Response]: Aaj Central Mandi me Gehun ka MSP bhav ₹2,275 per quintal hai.")
        elif "bheed" in voice_query:
            st.warning("🔊 [Audio Response]: Mandi me abhi bheed zyada hai, kripya 20 minute ruk kar aayein.")
        else:
            st.info("🔊 [Audio Response]: Aapka payment successfully bank account me bhej diya gaya hai.")

# ==========================================
# FEATURE 4: LIVE MANDI RATES & MSP
# ==========================================
elif choice in ["🌾 मंडी भाव और न्यूनतम समर्थन मूल्य (Mandi Rates & MSP)", "🌾 Live Mandi Rates & MSP"]:
    st.header("🌾 " + ("आज के मंडी भाव और सरकारी MSP दरें" if lang == "Hindi (हिंदी)" else "Live Mandi Rates & Government MSP Rates"))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🌾 Wheat (गेहूं)")
        st.metric("Government MSP Rate", "₹ 2,275 / Qtl")
        st.write("**Today's Max Price:** ₹ 2,310 / Qtl")
        st.write("**Today's Min Price:** ₹ 2,250 / Qtl")

    with col2:
        st.markdown("### 🌾 Paddy (धान)")
        st.metric("Government MSP Rate", "₹ 2,183 / Qtl")
        st.write("**Today's Max Price:** ₹ 2,220 / Qtl")
        st.write("**Today's Min Price:** ₹ 2,150 / Qtl")

    with col3:
        st.markdown("### 🫘 Pulses (चना / दाल)")
        st.metric("Government MSP Rate", "₹ 5,440 / Qtl")
        st.write("**Today's Max Price:** ₹ 5,500 / Qtl")
        st.write("**Today's Min Price:** ₹ 5,380 / Qtl")

# ==========================================
# FEATURE 5: SLOT BOOKING
# ==========================================
elif choice in ["📱 किसान सत्यापन और स्लॉट बुकिंग", "📱 Farmer Verification & Slot Booking"]:
    st.header("🔐 " + ("किसान सत्यापन और टाइम स्लॉट बुकिंग" if lang == "Hindi (हिंदी)" else "Farmer Verification & Slot Booking"))
    
    with st.form("booking_form"):
        name = st.text_input("Kisan Ka Naam / Farmer Name")
        phone = st.text_input("Mobile Number (10 Digits)")
        id_num = st.text_input("ID Verification Number (12 Digits Demo)", type="password")
        
        mandi = st.selectbox("Mandi / Depot", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
        crop = st.selectbox("Fasal / Crop", ["Wheat (गेहूं) @ ₹2,275/Qtl", "Paddy (धान) @ ₹2,183/Qtl", "Pulses (दाल) @ ₹5,440/Qtl"])
        slot = st.selectbox("Time Slot", ["08:00 AM - 10:00 AM", "10:00 AM - 12:00 PM", "02:00 PM - 04:00 PM"])
        slot_date = st.date_input("Date / तारीख")
        
        submitted = st.form_submit_button("Book Slot Now" if lang == "English" else "स्लॉट बुक करें")
        
        if submitted:
            if len(phone) == 10 and phone.isdigit() and len(id_num) == 12 and id_num.isdigit() and name.strip():
                st.success(f"🎉 Slot Booked Successfully for {name}!")
                st.write(f"**Phone:** {phone}")
                st.write(f"**Depot:** {mandi}")
                st.write(f"**Crop Selected:** {crop}")
                st.write(f"**Date:** {slot_date} | **Slot:** {slot}")
                st.info(f"🆔 **Token ID:** TOKEN-{id_num[-4:]}")
            else:
                st.error("❌ Invalid Details! Kripya 10-digit Phone aur 12-digit ID Number sahi se bharein.")

# ==========================================
# FEATURE 6: LIVE RUSH STATUS
# ==========================================
elif choice in ["🚨 मंडी भीड़ स्थिति (Rush Status)", "🚨 Live Mandi Rush Status"]:
    st.header("📊 " + ("मंडी भीड़ और देरी की स्थिति" if lang == "Hindi (हिंदी)" else "Live Mandi Rush & Delay Status"))
    selected_mandi = st.selectbox("Select Mandi:", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
    
    if selected_mandi == "Central Grain Depot A":
        st.error("🔴 HEAVY RUSH (भारी भीड़)")
        st.warning("⏳ **ALERT:** Mandi me bheed zyada hai. Apne slot se **20 Min Late** aayein taaki line me na khada hona pade.")
    elif selected_mandi == "Regional Mandi Hub B":
        st.warning("🟡 MODERATE RUSH (सामान्य भीड़)")
        st.info("⏱️ Normal wait time. Apne time par aayein.")
    else:
        st.success("🟢 LOW RUSH (भीड़ नहीं है)")
        st.info("✅ Bilkul bheed nahi hai. Aap exact time par aa sakte hain.")

# ==========================================
# FEATURE 7: PAYMENT STATUS
# ==========================================
elif choice in ["💳 भुगतान स्थिति (Payment Status)", "💳 Payment Status Check"]:
    st.header("💳 " + ("डीबीटी भुगतान स्थिति की जांच" if lang == "Hindi (हिंदी)" else "Direct Benefit Transfer (DBT) Payment Status"))
    
    token_id = st.text_input("Enter Token ID / Registration Number:", placeholder="e.g., TOKEN-1234")
    
    if st.button("Check Status" if lang == "English" else "स्थिति देखें"):
        if token_id.strip():
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Weight Sold", "45 Quintals")
            col2.metric("MSP Amount", "₹ 1,02,375")
            col3.metric("Status", "SUCCESS", delta_color="normal")
            
            st.success("✅ Payment Processed via Direct Benefit Transfer (DBT)")
            st.json({
                "Transaction Reference": "TXN9876543210DBT",
                "Bank Account Status": "Credited to Bank Account",
                "Payment Date": "02-09-2026",
                "Wheat Rate Applied": "₹ 2,275 per Quintal"
            })
        else:
            st.error("Please enter a valid Token ID!")

# ==========================================
# FEATURE 8: WEATHER REPORT
# ==========================================
elif choice in ["🌤️ मौसम की जानकारी (Weather)", "🌤️ Mandi Weather Report"]:
    st.header("🌤️ " + ("मंडी मौसम रिपोर्ट" if lang == "Hindi (हिंदी)" else "Mandi Weather System"))
    city = st.text_input("Enter City / District:", "Delhi")
    if st.button("Get Weather"):
        api_key = "bd5e378503939ddaee76f12ad7a97608"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            res = requests.get(url).json()
            if res.get("cod") == 200:
                st.subheader(f"Weather: {city.upper()}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{res['main']['temp']} °C")
                col2.metric("Humidity", f"{res['main']['humidity']} %")
                col3.metric("Condition", res['weather'][0]['description'].capitalize())
            else:
                st.error("❌ City not found!")
        except:
            st.error("⚠️ Weather service error.")

# ==========================================
# FEATURE 9: IVR / SMS SIMULATION
# ==========================================
elif choice in ["📞 IVR / SMS सेवा (Non-Smartphone)", "📞 Non-Smartphone (IVR / SMS Simulation)"]:
    st.header("📞 Non-Smartphone / IVR Service Portal")
    st.caption("Toll-Free Helpline: 1800-180-1551")
    
    keypad_phone = st.text_input("Kisan Mobile Number (10 Digits):")
    action = st.radio("Select Action:", [
        "1. Outbound Voice Call Alert (कॉल अलर्ट)", 
        "2. SMS Slot Request (एसएमएस अनुरोध)", 
        "3. Mandi Rates SMS (मंडी भाव एसएमएस)",
        "4. Delay Alert SMS (भीड़ की चेतावनी)"
    ])
    
    if st.button("Execute Action"):
        if len(keypad_phone) == 10 and keypad_phone.isdigit():
            if "Rates SMS" in action:
                st.success(f"💬 Rate SMS Sent to {keypad_phone}: 'Aaj ke Mandi Bhav: Gehun ₹2275/Qtl, Dhan ₹2183/Qtl, Dal ₹5440/Qtl.'")
            else:
                st.success(f"💬 Alert sent successfully to {keypad_phone}!")
        else:
            st.error("❌ Invalid Mobile Number!")
