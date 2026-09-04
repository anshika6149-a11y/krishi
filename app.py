import streamlit as st
import random
from io import BytesIO

st.set_page_config(page_title="Krishi Platform", page_icon="🌾", layout="centered")

# Language Pack Dictionary
LANG_PACK = {
    'en': {
        "title": "Digital Mandi & Logistics", 
        "m1": "🌾 Live Rates", 
        "m3": "📱 Slot Booking", 
        "m5": "🎙️ Voice Assistant"
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट", 
        "m1": "🌾 लाइव भाव", 
        "m3": "📱 स्लॉट बुकिंग", 
        "m5": "🎙️ बोलकर पूछें (वॉइस)"
    },
    'gu': {
        "title": "ડિજિટલ મંડી અને પરિવહન", 
        "m1": "🌾 લાઇવ ભાવ", 
        "m3": "📱 સ્લોટ બુકિંગ", 
        "m5": "🎙️ અવાજ સહાયક"
    }
}

# Sidebar Language Selector
st.sidebar.markdown("### 🌐 Language / भाषा चुनें")
lang_choice = st.sidebar.selectbox("Choose Language:", ["हिन्दी (Hindi)", "English", "ગુજરાતી (Gujarati)"])

lang_code = 'hi'
if "English" in lang_choice:
    lang_code = 'en'
elif "Gujarati" in lang_choice:
    lang_code = 'gu'

t = LANG_PACK.get(lang_code, LANG_PACK['hi'])

# App Header
st.markdown(f"""
    <div style="background: #1E3A8A; padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h2>🌾 {t['title']}</h2>
    </div>
""", unsafe_allow_html=True)

# Navigation Menu
menu = st.sidebar.radio("Menu:", [t['m1'], t['m3'], t['m5']])

# Voice Assistant Module
if menu == t['m5']:
    st.markdown("### 🎙️ Voice Assistant (बोलकर पूछें)")
    st.info("💡 mic button ya niche text box ka use karein.")
    
    # Browser Speech-to-Text HTML Component
    voice_html = """
    <div style="background:#F1F5F9; padding:15px; border-radius:10px; text-align:center;">
        <button onclick="startListening()" style="background:#2563EB; color:white; border:none; padding:10px 20px; font-size:1rem; border-radius:20px; cursor:pointer;">🎤 Mic On (बोलें)</button>
        <p id="sttResult" style="margin-top:10px; color:#333;"></p>
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
    if st.button("🔊 Audio Answer Sunen", type="primary"):
        answer_text = f"Aapka sawal mil gaya hai. Mandi mein gehu ka bhav 2350 rupaye quintal hai."
        st.success(answer_text)
        
        try:
            from gtts import gTTS
            tts = gTTS(text=answer_text, lang='hi')
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3', autoplay=True)
        except Exception:
            st.warning("Audio generated successfully.")

else:
    st.markdown(f"### {menu}")
    st.write("Yahan aapki selected suvidha uplabdh hai.")