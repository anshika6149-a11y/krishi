import streamlit as st
import requests

st.set_page_config(page_title="Krishi Procurement Platform", page_icon="🌾")

st.title("🌾 Krishi Procurement Platform")
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Select Module:", [
    "📱 Farmer Verification & Slot Booking", 
    "🚨 Live Mandi Rush Status", 
    "🌤️ Mandi Weather Report", 
    "📞 Non-Smartphone (IVR / SMS Simulation)"
])

# 1. VERIFICATION & BOOKING
if choice == "📱 Farmer Verification & Slot Booking":
    st.header("🔐 Farmer Verification & Slot Booking")
    
    with st.form("booking_form"):
        name = st.text_input("Kisan ka Naam (Full Name)")
        phone = st.text_input("Mobile Number (10 Digits)")
        id_num = st.text_input("ID Verification Number (12 Digits Demo)", type="password")
        
        mandi = st.selectbox("Select Procurement Depot", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
        crop = st.selectbox("Select Crop (Fasal)", ["Wheat (Gehun)", "Paddy (Dhan)", "Pulses (Dal)"])
        slot = st.selectbox("Select Time Slot", ["08:00 AM - 10:00 AM", "10:00 AM - 12:00 PM", "02:00 PM - 04:00 PM"])
        slot_date = st.date_input("Select Date")
        
        submitted = st.form_submit_button("Book Slot Now")
        
        if submitted:
            if len(phone) == 10 and phone.isdigit() and len(id_num) == 12 and id_num.isdigit() and name.strip():
                masked_id = "XXXX-XXXX-" + id_num[-4:]
                st.success(f"🎉 Slot Booked Successfully for {name}!")
                st.write(f"**Verified ID:** {masked_id}")
                st.write(f"**Phone:** {phone}")
                st.write(f"**Depot:** {mandi}")
                st.write(f"**Crop:** {crop}")
                st.write(f"**Date:** {slot_date} | **Slot:** {slot}")
                st.info(f"🆔 **Token ID:** TOKEN-{id_num[-4:]}")
            else:
                st.error("❌ Invalid Details! Kripya 10-digit Phone aur 12-digit ID Number sahi se bharein.")

# 2. RUSH STATUS
elif choice == "🚨 Live Mandi Rush Status":
    st.header("📊 Live Mandi Rush & Delay Status")
    selected_mandi = st.selectbox("Select Mandi to check status:", ["Central Grain Depot A", "Regional Mandi Hub B", "District Depot C"])
    
    if selected_mandi == "Central Grain Depot A":
        st.error("🔴 HEAVY RUSH (Bohat Bheed)")
        st.warning("⏳ **ALERT:** Mandi me abhi bheed zyada hai. Kripya apne time slot se **20 Min Late** aayein taaki line me na khada hona pade.")
    elif selected_mandi == "Regional Mandi Hub B":
        st.warning("🟡 MODERATE RUSH (Normal Bheed)")
        st.info("⏱️ Thoda wait time hai. Apne time par aayein (5-10 min delay ho sakta hai).")
    else:
        st.success("🟢 LOW RUSH (Khaali Hai)")
        st.info("✅ Bilkul bheed nahi hai. Aap exact time par aa sakte hain.")

# 3. WEATHER REPORT
elif choice == "🌤️ Mandi Weather Report":
    st.header("🌤️ Mandi Weather System")
    city = st.text_input("Apni City / District ka Naam Daalein:", "Delhi")
    if st.button("Get Weather Report"):
        api_key = "bd5e378503939ddaee76f12ad7a97608"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            res = requests.get(url).json()
            if res.get("cod") == 200:
                st.subheader(f"Weather Report: {city.upper()}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{res['main']['temp']} °C")
                col2.metric("Humidity", f"{res['main']['humidity']} %")
                col3.metric("Condition", res['weather'][0]['description'].capitalize())
            else:
                st.error("❌ City nahi mili! Kripya sahi city name daalein.")
        except:
            st.error("⚠️ Weather fetch karne me problem aayi. Internet check karein.")

# 4. IVR SIMULATION
elif choice == "📞 Non-Smartphone (IVR / SMS Simulation)":
    st.header("📞 Non-Smartphone / IVR Service Portal")
    st.caption("Toll-Free Helpline: 1800-180-1551")
    
    keypad_phone = st.text_input("Kisan Mobile Number (10 Digits):")
    action = st.radio("Select Action:", [
        "1. Trigger Outbound Voice Call Alert", 
        "2. Send SMS Slot Request", 
        "3. Send Delay Alert SMS (Bheed Warning)"
    ])
    
    if st.button("Execute Action"):
        if len(keypad_phone) == 10 and keypad_phone.isdigit():
            if "Voice Call" in action:
                st.info(f"📞 Calling {keypad_phone}... 🔊 Prompt: 'Namaste, Mandi me abhi bheed hai. Kripya 20 min late aayein.'")
            elif "Delay Alert" in action:
                st.warning(f"💬 Delay SMS Sent to {keypad_phone}: 'ALERT: Mandi me bheed hone ke karan aap 20 minute late aayein.'")
            else:
                st.success(f"💬 SMS Sent to {keypad_phone}: 'Aapka slot request receive ho gaya hai.'")
        else:
            st.error("❌ Invalid Mobile Number!")
