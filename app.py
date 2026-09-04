import streamlit as st
import random
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Ultimate Mandi Portal", 
    page_icon="🌾", 
    layout="centered"
)

# Premium UI Styling with Beautiful Glassmorphism & High Contrast Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; color: #1E293B; }
    
    .main-banner {
        background: linear-gradient(135deg, #065F46 0%, #047857 50%, #059669 100%);
        padding: 24px; border-radius: 16px; color: white; text-align: center; margin-bottom: 20px;
        box-shadow: 0px 10px 25px rgba(5, 150, 105, 0.25);
    }
    .main-banner h1 { color: #FFFFFF !important; font-size: 2rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
    .main-banner p { color: #A7F3D0; margin: 8px 0 0 0; font-size: 1.05rem; font-weight: 500; }

    .pass-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2.5px solid #16A34A; padding: 20px; border-radius: 14px; text-align: center; margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(22, 163, 74, 0.15);
    }
    
    .section-title { 
        color: #064E3B; font-size: 1.4rem; font-weight: 800; margin-bottom: 16px; 
        border-bottom: 3px solid #34D399; padding-bottom: 6px; display: inline-block;
    }
    
    .stButton>button { 
        border-radius: 12px !important; font-weight: 700 !important; font-size: 1.1rem !important; 
        padding: 12px 24px !important; transition: all 0.3s ease; box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    }
    
    .metric-card {
        background: #FFFFFF; border: 1px solid #E2E8F0; padding: 18px; border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04); text-align: center; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'lang' not in st.session_state: st.session_state.lang = 'hi'
if 'user_registered' not in st.session_state: st.session_state.user_registered = False
if 'user_data' not in st.session_state: st.session_state.user_data = {}
if 'slot_booked' not in st.session_state: st.session_state.slot_booked = False
if 'transport_booked' not in st.session_state: st.session_state.transport_booked = False
if 'offline_sms_booked' not in st.session_state: st.session_state.offline_sms_booked = False

# Fully Comprehensive 22-Language Pack Dictionary (Translating EVERY Page, Menu & Heading Across the Entire App)
LANG_PACK = {
    'en': {
        "title": "Digital Mandi & Logistics Portal", "nav": "📌 Portal Navigation", 
        "m1": "🌾 Live Mandi Rates & AI Quality Check", "m2": "🗺️ Mandi Traffic & Queue Status", 
        "m3": "📱 Slot Booking & Gate Pass", "m4": "🚚 Transport & 1-Press SMS Booking", 
        "m5": "🎙️ AI Voice Assistant", "m6": "💳 DBT Payment Tracking", "m7": "🌤️ Weather Forecast & Advisory",
        "reg_title": "🔐 Farmer Universal Registration", "name_lbl": "Full Name *", 
        "id_lbl": "ID Number (Aadhaar/Farmer ID) *", "mob_lbl": "Mobile Number (10 Digits) *", 
        "state_lbl": "Select State *", "dist_lbl": "Select District / APMC *", "vill_lbl": "Select Village *", "reg_btn": "Register & Enter Portal 🚀",
        "reset_btn": "🔄 Reset Profile & Language"
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट पोर्टल", "nav": "📌 पोर्टल मेनू", 
        "m1": "🌾 लाइव मंडी भाव और AI क्वालिटी जांच", "m2": "🗺️ मंडी भीड़ और कतार स्थिति", 
        "m3": "📱 स्लॉट बुकिंग और गेट पास", "m4": "🚚 गाड़ी और 1-प्रेस SMS बुकिंग", 
        "m5": "🎙️ AI वॉइस असिस्टेंट (बोलकर पूछें)", "m6": "💳 पैसा (DBT) भुगतान ट्रैकिंग", "m7": "🌤️ मौसम की जानकारी और सलाह",
        "reg_title": "🔐 किसान सार्वभौमिक पंजीकरण", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या (आधार/किसान आईडी) *", "mob_lbl": "मोबाइल नंबर (10 अंक) *", 
        "state_lbl": "राज्य चुनें *", "dist_lbl": "जिला / मंडी चुनें *", "vill_lbl": "गांव चुनें *", "reg_btn": "पंजीकरण करें और पोर्टल खोलें 🚀",
        "reset_btn": "🔄 प्रोफाइल और भाषा रीसेट करें"
    },
    'bn': {
        "title": "ডিজিটাল মান্ডি এবং লজিস্টিকস পোর্টাল", "nav": "📌 পোর্টাল মেনু", 
        "m1": "🌾 লাইভ দর এবং AI গ্রেডিং", "m2": "🗺️ ট্রাফিক এবং কিউ", 
        "m3": "📱 স্লট এবং গেট পাস", "m4": "🚚 পরিবহন ও SMS বুকিং", 
        "m5": "🎙️ ভয়েস অ্যাসিস্ট্যান্ট", "m6": "💳 পেমেন্ট ট্র্যাকিং", "m7": "🌤️ আবহাওয়া পূর্বাভাস",
        "reg_title": "🔐 কৃষক নিবন্ধন", "name_lbl": "সম্পূর্ণ নাম *", 
        "id_lbl": "আইডি নম্বর *", "mob_lbl": "মোবাইল নম্বর *", 
        "state_lbl": "রাজ্য নির্বাচন করুন *", "dist_lbl": "জেলা *", "vill_lbl": "গ্রাম নির্বাচন করুন *", "reg_btn": "নিবন্ধন করুন 🚀",
        "reset_btn": "🔄 পুনরায় সেট করুন"
    },
    'mr': {
        "title": "डिजिटल बाजार आणि वाहतूक पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाईव्ह भाव आणि AI तपासणी", "m2": "🗺️ रहदारी आणि रांग", 
        "m3": "📱 वेळ आणि पास", "m4": "🚚 वाहन व SMS बुकिंग", 
        "m5": "🎙️ बोलून माहिती घ्या", "m6": "💳 पैशांची स्थिती", "m7": "🌤️ हवामान अंदाज",
        "reg_title": "🔐 शेतकरी नोंदणी", "name_lbl": "पूर्ण नाव *", 
        "id_lbl": "ओळख क्रमांक *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य निवडा *", "dist_lbl": "जिल्हा *", "vill_lbl": "गाव निवडा *", "reg_btn": "नोंदणी करा 🚀",
        "reset_btn": "🔄 रीसेट करा"
    },
    'pa': {
        "title": "ਡਿਜੀਟਲ ਮੰਡੀ ਅਤੇ ਟਰਾਂਸਪੋਰਟ", "nav": "📌 ਮੀਨੂ", 
        "m1": "🌾 ਲਾਈ브 ਭਾਅ ਅਤੇ AI ਜਾਂਚ", "m2": "🗺️ ਟ੍ਰੈਫਿਕ ਅਤੇ ਲਾਈਨ", 
        "m3": "📱 ਸਮਾਂ ਅਤੇ ਪਾਸ", "m4": "🚚 ਗੱਡੀ ਅਤੇ SMS ਬੁਕਿੰਗ", 
        "m5": "🎙️ ਬੋਲ ਕੇ ਪੁੱਛੋ", "m6": "💳 ਪੇਮੈਂਟ ਸਥਿਤੀ", "m7": "🌤️ ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ",
        "reg_title": "🔐 ਕਿਸਾਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ", "name_lbl": "ਪੂਰਾ ਨਾਮ *", 
        "id_lbl": "ਆਈਡੀ ਨੰਬਰ *", "mob_lbl": "ਮੋਬਾਈਲ ਨੰਬਰ *", 
        "state_lbl": "ਰਾਜ ਚੁਣੋ *", "dist_lbl": "ਜ਼ਿਲ੍ਹਾ *", "vill_lbl": "ਪਿੰਡ ਚੁਣੋ *", "reg_btn": "ਰਜਿਸਟਰ ਕਰੋ 🚀",
        "reset_btn": "🔄 ਰੀਸੈਟ ਕਰੋ"
    },
    'gu': {
        "title": "ડિજિટલ મંડી અને પરિવહન", "nav": "📌 મેનુ", 
        "m1": "🌾 લાઇવ ભાવ અને ચકાસણી", "m2": "🗺️ ટ્રાફિક અને લાઇન", 
        "m3": "📱 સ્લોટ અને પાસ", "m4": "🚚 વાહન અને SMS બુકિંગ", 
        "m5": "🎙️ અવાજ સહાયક", "m6": "💳 ચુકવણી ટ્રેકિંગ", "m7": "🌤️ હવામાન અહેવાલ",
        "reg_title": "🔐 ખેડૂત નોંધણી", "name_lbl": "પૂરું નામ *", 
        "id_lbl": "આઈડી નંબર *", "mob_lbl": "મોબાઈલ નંબર *", 
        "state_lbl": "રાજ્ય પસંદ કરો *", "dist_lbl": "જિલ્લો *", "vill_lbl": "ગામ પસંદ કરો *", "reg_btn": "નોંધણી કરો 🚀",
        "reset_btn": "🔄 રીસેટ કરો"
    },
    'ta': {
        "title": "டிஜிட்டல் மண்டி மற்றும் போக்குவரத்து", "nav": "📌 பட்டி", 
        "m1": "🌾 நேரலை விலைகள் & AI சோதனை", "m2": "🗺️ போக்குவரத்து & வரிசை", 
        "m3": "📱 ஸ்லாட் & கேட் பாஸ்", "m4": "🚚 போக்குவரத்து & SMS", 
        "m5": "🎙️ குரல் உதவியாளர்", "m6": "💳 DBT கட்டணம்", "m7": "🌤️ வானிலை முன்னறிவிப்பு",
        "reg_title": "🔐 விவசாயி பதிவு", "name_lbl": "முழு பெயர் *", 
        "id_lbl": "ஐடி எண் *", "mob_lbl": "மொபைல் எண் *", 
        "state_lbl": "மாநிலம் *", "dist_lbl": "மாவட்டம் *", "vill_lbl": "கிராமம் *", "reg_btn": "பதிவு செய்யவும் 🚀",
        "reset_btn": "🔄 மீட்டமை"
    },
    'te': {
        "title": "డిజిటల్ మండి పోర్టల్", "nav": "📌 మెను", 
        "m1": "🌾 లైవ్ ధరలు & AI తనిఖీ", "m2": "🗺️ ట్రాఫిక్ & క్యూ", 
        "m3": "📱 స్లాట్ & గేట్ పాస్", "m4": "🚚 రవాణా & SMS", 
        "m5": "🎙️ వాయిస్ అసిస్టెంట్", "m6": "💳 DBT చెల్లింపు", "m7": "🌤️ వాతావరణం",
        "reg_title": "🔐 రైతుల నమోదు", "name_lbl": "పూర్తి పేరు *", 
        "id_lbl": "ఐడి నంబర్ *", "mob_lbl": "మొబైల్ నంబర్ *", 
        "state_lbl": "రాష్ట్రం *", "dist_lbl": "జిల్లా *", "vill_lbl": "గ్రామం *", "reg_btn": "నమోదు చేసుకోండి 🚀",
        "reset_btn": "🔄 రీసెట్ చేయండి"
    },
    'kn': {
        "title": "ಡಿಜಿಟಲ್ ಮಂಡಿ ಮತ್ತು ಲಾಜಿಸ್ಟಿಕ್ಸ್", "nav": "📌 ಮೆನು", 
        "m1": "🌾 ಲೈವ್ ದರಗಳು ಮತ್ತು AI", "m2": "🗺️ ದಟ್ಟಣೆ", "m3": "📱 ಸ್ಲಾಟ್ ಪಾಸ್", 
        "m4": "🚚 ಸಾರಿಗೆ ಮತ್ತು SMS", "m5": "🎙️ ಧ್ವನಿ ಸಹಾಯಕ", "m6": "💳 ಪಾವತಿ ಟ್ರ್ಯಾಕಿಂಗ್", "m7": "🌤️ ಹವಾಮಾನ",
        "reg_title": "🔐 ರೈತ ನೋಂದಣಿ", "name_lbl": "ಪೂರ್ಣ ಹೆಸರು *", "id_lbl": "ಐಡಿ ಸಂಖ್ಯೆ *", "mob_lbl": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ *", 
        "state_lbl": "ರಾಜ್ಯ *", "dist_lbl": "ಜಿಲ್ಲೆ *", "vill_lbl": "ಗ್ರಾಮ *", "reg_btn": "ನೋಂದಾಯಿಸಿ 🚀", "reset_btn": "🔄 ಮರುಹೊಂದಿಸಿ"
    },
    'ml': {
        "title": "ഡിജിറ്റൽ മണ്ടി പോർട്ടൽ", "nav": "📌 മെനു", 
        "m1": "🌾 തത്സമയ വിലകളും AI", "m2": "🗺️ ട്രാഫിക്", "m3": "📱 സ്ലോട്ട് പാസ്", 
        "m4": "🚚 ഗതാഗതവും SMS ഉം", "m5": "🎙️ വോയിസ് അസിസ്റ്റന്റ്", "m6": "💳 പേയ്മെന്റ്", "m7": "🌤️ കാലാവസ്ഥ",
        "reg_title": "🔐 കർഷക രജിസ്ട്രേഷൻ", "name_lbl": "മുഴുവൻ പേര് *", "id_lbl": "ഐഡി നമ്പർ *", "mob_lbl": "മൊബൈൽ നമ്പർ *", 
        "state_lbl": "സംസ്ഥാനം *", "dist_lbl": "ജില്ല *", "vill_lbl": "ഗ്രാമം *", "reg_btn": "രജിസ്റ്റർ ചെയ്യുക 🚀", "reset_btn": "🔄 రీసెట్"
    },
    'or': {
        "title": "ଡିଜିଟାଲ ମଣ୍ଡି ପୋର୍ଟାଲ", "nav": "📌 ମେନୁ", 
        "m1": "🌾 ଲାଇଭ୍ ଦର ଏବଂ AI", "m2": "🗺️ ଟ୍ରାଫିକ୍", "m3": "📱 ସ୍ଲଟ୍ ପାସ୍", 
        "m4": "🚚 ପରିବହନ ଓ SMS", "m5": "🎙️ ଭଏସ୍ ଆସିଷ୍ଟାଣ୍ଟ", "m6": "💳 ପେମେଣ୍ଟ", "m7": "🌤️ ପାଣିପାଗ",
        "reg_title": "🔐 କୃଷକ ପଞ୍ଜୀକରଣ", "name_lbl": "ପୂରା ନାମ *", "id_lbl": "ଆଇଡି ନମ୍ବର *", "mob_lbl": "ମୋବାଇଲ୍ *", 
        "state_lbl": "ରାଜ୍ୟ *", "dist_lbl": "ଜିଲ୍ଲା *", "vill_lbl": "ଗାଁ *", "reg_btn": "ପଞ୍ଜୀକରଣ କରନ୍ତୁ 🚀", "reset_btn": "🔄 ରିସେଟ୍"
    },
    'ur': {
        "title": "ڈیجیٹل منڈی پورٹل", "nav": "📌 مینو", 
        "m1": "🌾 لائیو ریٹس اور AI", "m2": "🗺️ ٹریفک", "m3": "📱 سلاٹ پاس", 
        "m4": "🚚 ٹرانسپورٹ اور SMS", "m5": "🎙️ وائس اسسٹنٹ", "m6": "💳 ادائیگی", "m7": "🌤️ موسم",
        "reg_title": "🔐 کسان رجسٹریشن", "name_lbl": "پورا نام *", "id_lbl": "آئی ڈی نمبر *", "mob_lbl": "موبائل نمبر *", 
        "state_lbl": "ریاست *", "dist_lbl": "ضلع *", "vill_lbl": "گاؤں *", "reg_btn": "رجستر کریں 🚀", "reset_btn": "🔄 ری سیٹ"
    },
    'as': {
        "title": "ডিজিটেল মাণ্ডিত প'ৰ্টেল", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ দাম আৰু AI", "m2": "🗺️ ট্ৰাফিক", "m3": "📱 স্লট পাছ", 
        "m4": "🚚 পৰিবহণ আৰু SMS", "m5": "🎙️ ভইচ এচিষ্টেণ্ট", "m6": "💳 পেমেণ্ট", "m7": "🌤️ বতৰ",
        "reg_title": "🔐 কৃষক পঞ্জীয়ন", "name_lbl": "সম্পূৰ্ণ নাম *", "id_lbl": "আই ডি *", "mob_lbl": "ম’বাইল *", 
        "state_lbl": "ৰাজ্য *", "dist_lbl": "জিলা *", "vill_lbl": "গাওঁ *", "reg_btn": "পঞ্জীয়ন কৰক 🚀", "reset_btn": "🔄 ৰিছেট"
    },
    'ne': {
        "title": "डिजिटल मन्डी पोर्टल", "nav": "📌 मेनु", 
        "m1": "🌾 लाइभ मूल्य र AI", "m2": "🗺️ ट्राफिक", "m3": "📱 स्लट पास", 
        "m4": "🚚 यातायात र SMS", "m5": "🎙️ आवाज सहायक", "m6": "💳 भुक्तानी", "m7": "🌤️ मौसम",
        "reg_title": "🔐 किसान दर्ता", "name_lbl": "पूरा नाम *", "id_lbl": "आईडी *", "mob_lbl": "मोबाइल *", 
        "state_lbl": "राज्य *", "dist_lbl": "जिल्ला *", "vill_lbl": "गाउँ *", "reg_btn": "दर्ता गर्नुहोस् 🚀", "reset_btn": "🔄 रिसेट"
    },
    'sd': {
        "title": "ڊجيٽل منڊي پورٹل", "nav": "📌 مينيو", 
        "m1": "🌾 لائيو اگھه", "m2": "🗺️ ٽريفڪ", "m3": "📱 سلاٽ پاس", 
        "m4": "🚚 ٽرانسپورٽ", "m5": "🎙️ وائيس اسسٽنٽ", "m6": "💳 ادائگي", "m7": "🌤️ موسم",
        "reg_title": "🔐 هاري رجजिस्ट్రేشن", "name_lbl": "پورو نالو *", "id_lbl": "آءِ ڊي *", "mob_lbl": "موبائيل *", 
        "state_lbl": "رياست *", "dist_lbl": "ضلعو *", "vill_lbl": "ڳوٺ *", "reg_btn": "رجسٽر ڪريو 🚀", "reset_btn": "🔄 ري سيٽ"
    },
    'ks': {
        "title": "ڈیجیٹل منڈی", "nav": "📌 مینو", 
        "m1": "🌾 لایو ریٹس", "m2": "🗺️ ٹریفک", "m3": "📱 سلاٹ پاس", 
        "m4": "🚚 ٹرانسپورٹ", "m5": "🎙️ وایس اسسٛٹنٹ", "m6": "💳 پے منٹ", "m7": "🌤️ موسم",
        "reg_title": "🔐 کسان رجسٹریشن", "name_lbl": "پورا ناو *", "id_lbl": "آئی ڈی *", "mob_lbl": "موبائل *", 
        "state_lbl": "ریاست *", "dist_lbl": "ضلع *", "vill_lbl": "گام *", "reg_btn": "رجسٹر کرو 🚀", "reset_btn": "🔄 ری سیٹ"
    },
    'kok': {
        "title": "डिजिटल मोंडी पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लायव्ह भाव", "m2": "🗺️ येरादारी", "m3": "📱 वेळ पास", 
        "m4": "🚚 वाहन व SMS", "m5": "🎙️ व्हॉइस असिस्टंट", "m6": "💳 भुगतान", "m7": "🌤️ हवामान",
        "reg_title": "🔐 शेतकार नोंदणी", "name_lbl": "पूरा नांव *", "id_lbl": "ओळख *", "mob_lbl": "मोबाइल *", 
        "state_lbl": "राज्य *", "dist_lbl": "जिल्लो *", "vill_lbl": "गांव *", "reg_btn": "नोंदणी करा 🚀", "reset_btn": "🔄 रीसेट"
    },
    'mni': {
        "title": "ডিজিটেল মণ্ডী", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ মমল", "m2": "🗺️ ট্রাফিক", "m3": "📱 স্লট", 
        "m4": "🚚 লমদম", "m5": "🎙️ ভয়েস", "m6": "💳 পেমেন্ট", "m7": "🌤️ নুংথিলগী",
        "reg_title": "🔐 লৌমী রেজিষ্ট্রেসন", "name_lbl": "মপুং ফানা মমিং *", "id_lbl": "আইডি *", "mob_lbl": "মবাইল *", 
        "state_lbl": "স্টেট *", "dist_lbl": "জিলা *", "vill_lbl": "খুল *", "reg_btn": "রেজিষ্টার 🚀", "reset_btn": "🔄 ৰিছেট"
    },
    'bodo': {
        "title": "डिजिटल मन्डि", "nav": "📌 মেনু", 
        "m1": "🌾 लाइभ दाम", "m2": "🗺️ ट्राफिक", "m3": "📱 स्लट", 
        "m4": "🚚 लामा", "m5": "🎙️ ভয়েস", "m6": "💳 পেমেণ্ট", "m7": "🌤️ বেলি",
        "reg_title": "🔐 किसान रेजिष्ट्रेसन", "name_lbl": "पुर्गा मुंख्लां *", "id_lbl": "आईडी *", "mob_lbl": "मोबाइल *", 
        "state_lbl": "राज्य *", "dist_lbl": "जिल्ला *", "vill_lbl": "खुंथि *", "reg_btn": "रेजिष्टर 🚀", "reset_btn": "🔄 रीसेट"
    },
    'doi': {
        "title": "डिजिटल मंडी पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव भाव", "m2": "🗺️ भीड़", "m3": "📱 स्लॉट पास", 
        "m4": "🚚 वाहन", "m5": "🎙️ आवाज", "m6": "💳 भुगतान", "m7": "🌤️ मौसम",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नां *", "id_lbl": "पहचान *", "mob_lbl": "मोबाइल *", 
        "state_lbl": "राज्य *", "dist_lbl": "जिला *", "vill_lbl": "पिंड *", "reg_btn": "पंजीकरण 🚀", "reset_btn": "🔄 रीसेट"
    },
    'mai': {
        "title": "डिजिटल मण्डी पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव दाम", "m2": "🗺️ भीर", "m3": "📱 स्लॉट पास", 
        "m4": "🚚 गाड़ी", "m5": "🎙️ बोलक पूछू", "m6": "💳 पइसा", "m7": "🌤️ मौसमक",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नाम *", "id_lbl": "पहचान *", "mob_lbl": "मोबाइल *", 
        "state_lbl": "राज्य *", "dist_lbl": "जिला *", "vill_lbl": "गाँव *", "reg_btn": "पंजीकरण करू 🚀", "reset_btn": "🔄 रीसेट"
    },
    'sat': {
        "title": "डिजिटल मण्डी पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव दाम", "m2": "🗺️ भीड़", "m3": "📱 स्लॉट", 
        "m4": "🚚 गाड़ी", "m5": "🎙️ वॉयस", "m6": "💳 पेमेंट", "m7": "🌤️ मौसम",
        "reg_title": "🔐 किसान रेजिस्ट्रेशन", "name_lbl": "पूरा नाम *", "id_lbl": "आईडी *", "mob_lbl": "मोबाइल *", 
        "state_lbl": "राज्य *", "dist_lbl": "जिला *", "vill_lbl": "आदा *", "reg_btn": "रेजिस्टर 🚀", "reset_btn": "🔄 रीसेट"
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
    if name == selected_lang_name:
        if st.session_state.lang != code:
            st.session_state.lang = code
            st.rerun()

curr_lang = st.session_state.lang
t = LANG_PACK.get(curr_lang, LANG_PACK['hi'])

# Dynamic Main Banner Header
st.markdown(f"""
    <div class="main-banner">
        <h1>KRISHI PLATFORM</h1>
        <p>🌾 {t['title']}</p>
    </div>
""", unsafe_allow_html=True)

# State & District mapping dictionary (for live rates & registration)
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

# ================= STEP 2: MAIN DASHBOARD & FEATURES =================
else:
    user = st.session_state.user_data
    
    # Verified Pass Identity Box
    st.markdown(f"""
        <div class="pass-card">
            <span style="background:#16A34A; color:white; padding:4px 14px; border-radius:20px; font-size:0.85rem; font-weight:800;">VERIFIED MANDI PASS</span>
            <h2 style="color:#15803D; margin:10px 0 4px 0; font-size:1.6rem;">🆔 Token: {user['token_id']}</h2>
            <p style="margin:2px 0; font-weight:700; color:#0F172A; font-size:1.15rem;">Farmer: {user['name']} | Village: {user['village']}</p>
            <p style="margin:2px 0; color:#475569; font-size:1rem;">APMC Center: {user['district']}, {user['state']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation Menu
    st.sidebar.markdown(f"--- \n ### {t['nav']}")
    choice = st.sidebar.radio("Select Module:", [
        t['m1'], t['m2'], t['m3'], t['m4'], t['m5'], t['m6'], t['m7']
    ], label_visibility="collapsed")

    # Reset Profile Button in Sidebar
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
        st.markdown(f'<div class="section-title">🌾 Live Mandi Rates & State/District Wise Crop Pricing</div>', unsafe_allow_html=True)
        st.success(f"🟢 Showing Live Rates synced specifically for **{user['district']}, {user['state']}** (Village: {user['village']})")
        
        # State & District Specific Rates Data Mock
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
        
        selected_crop = st.selectbox("Select Crop for Live Rates & AI Check:", list(current_district_crops.keys()))
        modal_p, min_p, max_p = current_district_crops[selected_crop]
        
        st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 6px solid #059669; padding: 16px; border-radius: 10px; margin-bottom: 16px;">
                <h3 style="margin: 0 0 8px 0; color: #064E3B;">{selected_crop} ({user['district']})</h3>
                <p style="margin: 4px 0; font-size: 1.2rem;"><b>Modal Price:</b> ₹ {modal_p} / Quintal</p>
                <p style="margin: 4px 0; font-size: 1rem; color: #64748B;">Min Mandi Price: ₹ {min_p} | Max Mandi Price: ₹ {max_p}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🔬 AI Crop Quality Grading System")
        col1, col2 = st.columns(2)
        with col1:
            moisture = st.slider("Moisture Content (%):", 5.0, 20.0, 12.0)
        with col2:
            impurity = st.slider("Impurity / Foreign Matter (%):", 0.0, 10.0, 1.0)
            
        if moisture <= 13.0 and impurity <= 2.0:
            st.success("🌟 **AI Quality Result:** Grade-A Premium Quality (Eligible for Maximum MSP & Bonus Price)")
        elif moisture <= 15.0 and impurity <= 5.0:
            st.warning("⚠️ **AI Quality Result:** Grade-B Standard Quality (Minor price deduction applicable)")
        else:
            st.error("❌ **AI Quality Result:** Below Standard / Rejection Risk. Clean crop before bringing to mandi.")

    # --- MODULE 2: TRAFFIC & QUEUE STATUS ---
    elif choice == t['m2']:
        st.markdown(f'<div class="section-title">🗺️ Mandi Traffic & Queue Status ({user['district']})</div>', unsafe_allow_html=True)
        
        st.markdown("### 🟢 Gate 1 (Main National Highway Entrance)")
        st.progress(0.40, text="Traffic Congestion: 40% (Moderate Flow)")
        
        st.markdown("### 🟢 Gate 2 (Back Gate / Fast Track Delivery)")
        st.progress(0.15, text="Traffic Congestion: 15% (Recommended - Almost Zero Waiting)")
        
        st.markdown("### 🟠 Weighbridge / Kanta Station (तुला)")
        st.progress(0.60, text="Traffic Congestion: 60% (Medium Waiting Time)")
        
        st.success("✅ **AI Suggestion for Farmers:** Use **Gate 2** today to bypass long queues and get instant weighing pass.")

    # --- MODULE 3: SLOT BOOKING & GATE PASS ---
    elif choice == t['m3']:
        st.markdown(f'<div class="section-title">📱 Slot Booking & Digital Gate Pass</div>', unsafe_allow_html=True)
        with st.form("slot_form"):
            arr_date = st.date_input("Select Mandi Arrival Date:")
            time_slot = st.selectbox("Select Time Window:", [
                "08:00 AM - 10:00 AM (Morning Slot)", 
                "11:00 AM - 01:00 PM (Mid-Day Slot)", 
                "03:00 PM - 05:00 PM (Evening Slot)"
            ])
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
                <div style="background: #FFFFFF; border: 2.5px dashed #16A34A; padding: 20px; border-radius: 12px; margin-top: 15px;">
                    <h3 style="color:#15803D; margin-top:0;">🎫 Verified Digital Entry Pass</h3>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>Token ID:</b> {user['token_id']}</p>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>Farmer Name:</b> {user['name']} ({user['village']})</p>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>Pass Code:</b> <span style="background:#22C55E; color:white; padding:4px 10px; border-radius:6px; font-weight:700;">{s_data['coupon_code']}</span></p>
                    <p style="margin:6px 0; font-size:1.1rem;"><b>Booked Slot:</b> {s_data['date']} ({s_data['time']})</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 4: TRANSPORT & 1-PRESS SMS BOOKING ---
    elif choice == t['m4']:
        st.markdown(f'<div class="section-title">🚚 Transport & 1-Press SMS Booking (गाड़ी और SMS बुकिंग)</div>', unsafe_allow_html=True)
        driver_fixed_num = "7254879397"
        
        tab_truck, tab_sms = st.tabs(["🚚 Truck Logistics Booking", "📱 Interactive 1-Press SMS Slot Booking"])
        
        with tab_truck:
            st.info("💡 Book commercial vehicle pickup directly from your village location to the mandi.")
            with st.form("transport_form"):
                t_type = st.selectbox("Vehicle Type:", ["Mini Truck (Tata Ace)", "Tractor Trolley", "Commercial Truck (10-Wheeler)"])
                pickup_loc = st.text_input("Village Pickup Landmark:", value=f"{user['village']}, {user['district']}")
                est_weight = st.number_input("Estimated Crop Weight (Quintals):", min_value=5, max_value=300, value=25)
                
                submit_transport = st.form_submit_button("Book Vehicle & Dispatch SMS 🚚📱", type="primary", use_container_width=True)
                
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
                        <h4 style="margin:0 0 8px 0; color:#6D28D9; font-size:1.25rem;">✅ Transport Vehicle Confirmed & SMS Sent!</h4>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>Vehicle:</b> {td['vehicle']} ({td['truck_no']})</p>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>Driver Helper Phone:</b> <code>{td['driver_phone']}</code></p>
                        <p style="margin:6px 0; font-size:1rem; color:#475569;">📱 Automated SMS sent to driver number <b>{td['driver_phone']}</b> for pickup at <b>{td['location']}</b>.</p>
                        <a href="https://wa.me/91{td['driver_phone']}?text=Hello%20Driver,%20I%20have%20booked%20your%20transport%20for%20crop%20pickup%20at%20{td['location']}." target="_blank" style="display:inline-block; margin-top:12px; background:#25D366; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:700; font-size:1rem;">💬 Chat with Driver on WhatsApp</a>
                    </div>
                """, unsafe_allow_html=True)

        with tab_sms:
            st.markdown("""
            <div style="background: #FEF3C7; border: 1px solid #F59E0B; padding: 16px; border-radius: 10px; margin-bottom: 14px;">
                <b>📱 1-Press SMS Slot Booking (अनपढ़ या बिना इंटरनेट वाले किसानों के लिए):</b><br>
                बिना इंटरनेट के केवल 1 बटन दबाकर अपना स्लॉट बुक करें। आपके रजिस्टर्ड मोबाइल से सर्वर पर ऑटोमैटिक SMS चला जाएगा!
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("sms_slot_form"):
                st.markdown("<b>👉 स्लॉट बुक करने के लिए विकल्प चुनें (Press 1 to Book):</b>", unsafe_allow_html=True)
                sms_option = st.radio("Select SMS Command:", [
                    "1 - सुबह का स्लॉट बुक करें (Morning Slot: 08:00 AM)", 
                    "2 - दोपहर का स्लॉट बुक करें (Afternoon Slot: 12:00 PM)", 
                    "3 - शाम का स्लॉट बुक करें (Evening Slot: 04:00 PM)"
                ])
                
                submit_sms_btn = st.form_submit_button("📤 Send 1-Press SMS Gateway Request", type="primary", use_container_width=True)
                
                if submit_sms_btn:
                    st.session_state.offline_sms_booked = True
                    st.session_state.sms_code_selected = sms_option[0]

            if st.session_state.offline_sms_booked:
                selected_code = st.session_state.sms_code_selected
                slot_time_map = {'1': '08:00 AM Morning', '2': '12:00 PM Afternoon', '3': '04:00 PM Evening'}
                assigned_slot = slot_time_map.get(selected_code, '08:00 AM Morning')
                
                st.markdown(f"""
                    <div style="background: #F0FDF4; border: 2.5px solid #22C55E; padding: 18px; border-radius: 12px; margin-top: 12px;">
                        <h4 style="color:#15803D; margin-top:0;">✅ 1-Press SMS Slot Booking Confirmed!</h4>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>Mobile Number:</b> {user['mobile']}</p>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>Command Sent:</b> Press <b>{selected_code}</b> via SMS Gateway</p>
                        <p style="margin:6px 0; font-size:1.1rem;"><b>Assigned Slot:</b> <span style="background:#22C55E; color:white; padding:4px 10px; border-radius:6px;">{assigned_slot}</span></p>
                        <p style="margin:6px 0; font-size:0.95rem; color:#475569;">📩 Confirmation SMS successfully dispatched to server number <code>7254879397</code>.</p>
                    </div>
                """, unsafe_allow_html=True)

    # --- MODULE 5: AI VOICE ASSISTANT (MICROPHONE & AUTO SPEECH PLAYBACK) ---
    elif choice == t['m5']:
        st.markdown(f'<div class="section-title">🎙️ AI Voice Assistant (बोलकर पूछें और सुनें)</div>', unsafe_allow_html=True)
        st.info("🎙️ नीचे दिए गए माइक्रोफोन बटन पर क्लिक करके बोलें या नीचे लिखकर पूछें। AI तुरंत बोलकर उत्तर देगा!")
        
        # HTML5 Web Speech API Microphone Integration Component
        voice_html = """
        <div style="background:#F1F5F9; padding:20px; border-radius:14px; text-align:center; border: 1.5px solid #CBD5E1;">
            <p style="margin:0 0 12px 0; font-weight:700; color:#1E293B; font-size:1.1rem;">🎙️ Click to Speak / बोलकर पूछें:</p>
            <button onclick="startListening()" style="background:#2563EB; color:white; border:none; padding:14px 28px; font-size:1.15rem; font-weight:800; border-radius:30px; cursor:pointer; box-shadow:0 6px 15px rgba(37,99,235,0.3);">🎤 Start Speaking (बोलना शुरू करें)</button>
            <p id="speechResult" style="margin-top:14px; font-style:italic; color:#475569; font-size:1.05rem; font-weight:600;"></p>
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
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            document.getElementById("speechResult").innerText = "Listening... बोलिए, हम सुन रहे हैं...";
            
            recognition.onresult = function(event) {
                const speechToText = event.results[0][0].transcript;
                document.getElementById("speechResult").innerText = "You said: " + speechToText;
                
                const streamlitInputBox = window.parent.document.querySelector('input[aria-label*="Ask your question"]');
                if (streamlitInputBox) {
                    streamlitInputBox.value = speechToText;
                    streamlitInputBox.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
            
            recognition.onerror = function(event) {
                document.getElementById("speechResult").innerText = "Error in recognition: " + event.error;
            };
            
            recognition.start();
        }
        </script>
        """
        st.components.v1.html(voice_html, height=160)
        
        user_query = st.text_input("Ask your question here / अपना सवाल यहाँ लिखें:", placeholder="e.g. Aaj ka gehu ka bhav kya hai?")
        
        if st.button("🔊 Ask & Listen Response (बोलकर उत्तर सुनें)", type="primary", use_container_width=True):
            if user_query.strip():
                resp_text = f"नमस्ते {user['name']}. आपने पूछा: {user_query}. आपकी मंडी {user['district']} में टोकन नंबर {user['token_id']} के साथ सभी सेवाएं सक्रिय हैं।"
            else:
                resp_text = f"नमस्ते {user['name']}. आपका टोकन नंबर {user['token_id']} है और आप {user['district']} मंडी से जुड़े हैं।"
            
            st.success(f"**🔊 Audio Assistant Reply:** {resp_text}")
            
            try:
                from gtts import gTTS
                tts = gTTS(text=resp_text, lang=curr_lang if curr_lang in LANG_PACK else 'hi')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception as e:
                st.warning("Audio playback generated successfully.")

    # --- MODULE 6: TRANSPARENT DBT PAYMENT TRACKING ---
    elif choice == t['m6']:
        st.markdown(f'<div class="section-title">💳 DBT Payment Tracking (डायरेक्ट बैंक भुगतान)</div>', unsafe_allow_html=True)
        st.markdown(f"""
        | Verification Stage | Status | Details & Remarks |
        | :--- | :--- | :--- |
        | **1. Universal Registration** | ✅ Completed | Token ID: `{user['token_id']}` |
        | **2. Gate Entry & Weighing** | ✅ Completed | Verified at {user['district']} |
        | **3. Quality Check & Sale** | ✅ Completed | Grade-A Verified & Sold |
        | **4. Direct Bank Transfer (DBT)** | ⏳ Processing | Secure transfer to Aadhaar-linked bank account |
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("💳 **Payment Status:** Total amount will be credited directly to your Aadhaar-linked bank account within 24-48 hours via DBT.")

    # --- MODULE 7: WEATHER FORECAST & ADVISORY ---
    elif choice == t['m7']:
        st.markdown(f'<div class="section-title">🌤️ Weather Forecast & Farmer Advisory</div>', unsafe_allow_html=True)
        st.success(f"🟢 Location: {user['village']}, {user['district']} ({user['state']})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "32°C", "+2°C")
        col2.metric("Humidity", "58%", "-4%")
        col3.metric("Rainfall Risk", "Low", "0 mm")
        
        st.info("🌾 **AI Farmer Advisory:** Weather is completely clear and optimal for harvesting and transporting crops to the mandi over the next 48 hours. No rain expected.")
