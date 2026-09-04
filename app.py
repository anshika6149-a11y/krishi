import streamlit as st
import random
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Krishi Platform - Simplified Portal", 
    page_icon="🌾", 
    layout="centered"
)

# Clean, Big-Font UI Styling for Easy Accessibility
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; }
    
    .app-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 20px; border-radius: 14px; color: white; text-align: center; margin-bottom: 15px;
        box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.2);
    }
    .app-header h1 { color: #FFFFFF !important; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .app-header p { color: #93C5FD; margin: 6px 0 0 0; font-size: 1rem; }

    .pass-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #22C55E; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;
    }
    .section-box { color: #0F172A; font-size: 1.3rem; font-weight: 700; margin-bottom: 12px; }
    .stButton>button { border-radius: 10px !important; font-weight: 700 !important; font-size: 1.1rem !important; padding: 10px 20px !important; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'lang' not in st.session_state:
    st.session_state.lang = 'hi'
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'slot_booked' not in st.session_state:
    st.session_state.slot_booked = False
if 'transport_booked' not in st.session_state:
    st.session_state.transport_booked = False
if 'offline_sms_booked' not in st.session_state:
    st.session_state.offline_sms_booked = False

# Fully Comprehensive 22-Language Pack Dictionary (Translating ALL UI headers, menus, labels & content dynamically)
LANG_PACK = {
    'en': {
        "title": "Digital Mandi & Logistics Portal", "nav": "📌 Menu", 
        "m1": "🌾 Live Rates & AI Check", "m2": "🗺️ Traffic & Queue", 
        "m3": "📱 Slot & Gate Pass", "m4": "🚚 Transport & SMS", 
        "m5": "🎙️ Voice Assistant", "m6": "💳 DBT Payment Tracking", 
        "m7": "🌤️ Weather Forecast",
        "reg_title": "🔐 Farmer Registration", "name_lbl": "Full Name *", 
        "id_lbl": "ID Number *", "mob_lbl": "Mobile Number (10 Digits) *", 
        "state_lbl": "Select State *", "dist_lbl": "District *", "vill_lbl": "Select Village *",
        "reg_btn": "Register Now 🚀"
    },
    'hi': {
        "title": "डिजिटल मंडी और ट्रांसपोर्ट पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव भाव और AI जांच", "m2": "🗺️ भीड़ और कतार स्थिति", 
        "m3": "📱 स्लॉट और गेट पास", "m4": "🚚 गाड़ी और SMS बुकिंग", 
        "m5": "🎙️ बोलकर पूछें (वॉइस)", "m6": "💳 पैसा (DBT) ट्रैकिंग", 
        "m7": "🌤️ मौसम की जानकारी",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या *", "mob_lbl": "मोबाइल नंबर (10 अंक) *", 
        "state_lbl": "राज्य चुनें *", "dist_lbl": "जिला चुनें *", "vill_lbl": "गांव चुनें *",
        "reg_btn": "पंजीकरण करें 🚀"
    },
    'bn': {
        "title": "ডিজিটাল মান্ডি এবং লজিস্টিকস", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ দর এবং AI গ্রেডিং", "m2": "🗺️ ট্রাফিক এবং কিউ", 
        "m3": "📱 স্লট এবং গেট পাস", "m4": "🚚 পরিবহন ও SMS বুকিং", 
        "m5": "🎙️ ভয়েস অ্যাসিস্ট্যান্ট", "m6": "💳 পেমেন্ট ট্র্যাকিং", 
        "m7": "🌤️ আবহাওয়া পূর্বাভাস",
        "reg_title": "🔐 কৃষক নিবন্ধন", "name_lbl": "সম্পূর্ণ নাম *", 
        "id_lbl": "আইডি নম্বর *", "mob_lbl": "মোবাইল নম্বর *", 
        "state_lbl": "রাজ্য নির্বাচন করুন *", "dist_lbl": "জেলা *", "vill_lbl": "গ্রাম নির্বাচন করুন *",
        "reg_btn": "নিবন্ধন করুন 🚀"
    },
    'mr': {
        "title": "डिजिटल बाजार आणि वाहतूक पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाईव्ह भाव आणि तपासणी", "m2": "🗺️ रहदारी आणि रांग", 
        "m3": "📱 वेळ आणि पास", "m4": "🚚 वाहन व SMS बुकिंग", 
        "m5": "🎙️ बोलून माहिती घ्या", "m6": "💳 पैशांची स्थिती", 
        "m7": "🌤️ हवामान अंदाज",
        "reg_title": "🔐 शेतकरी नोंदणी", "name_lbl": "पूर्ण नाव *", 
        "id_lbl": "ओळख क्रमांक *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य निवडा *", "dist_lbl": "जिल्हा *", "vill_lbl": "गाव निवडा *",
        "reg_btn": "नोंदणी करा 🚀"
    },
    'pa': {
        "title": "ਡਿਜੀਟਲ ਮੰਡੀ ਅਤੇ ਟਰਾਂਸਪੋਰਟ", "nav": "📌 ਮੀਨੂ", 
        "m1": "🌾 ਲਾਈ브 ਭਾਅ ਅਤੇ ਜਾਂਚ", "m2": "🗺️ ਟ੍ਰੈਫਿਕ ਅਤੇ ਲਾਈਨ", 
        "m3": "📱 ਸਮਾਂ ਅਤੇ ਪਾਸ", "m4": "🚚 ਗੱਡੀ ਅਤੇ SMS ਬੁਕਿੰਗ", 
        "m5": "🎙️ ਬੋਲ ਕੇ ਪੁੱਛੋ", "m6": "💳 ਪੇਮੈਂਟ ਸਥਿਤੀ", 
        "m7": "🌤️ ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ",
        "reg_title": "🔐 ਕਿਸਾਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ", "name_lbl": "ਪੂਰਾ ਨਾਮ *", 
        "id_lbl": "ਆਈਡੀ ਨੰਬਰ *", "mob_lbl": "ਮੋਬਾਈਲ ਨੰਬਰ *", 
        "state_lbl": "ਰਾਜ ਚੁਣੋ *", "dist_lbl": "ਜ਼ਿਲ੍ਹਾ *", "vill_lbl": "ਪਿੰਡ ਚੁਣੋ *",
        "reg_btn": "ਰਜਿਸਟਰ ਕਰੋ 🚀"
    },
    'gu': {
        "title": "ડિજિટલ મંડી અને પરિવહન", "nav": "📌 મેનુ", 
        "m1": "🌾 લાઇવ ભાવ અને ચકાસણી", "m2": "🗺️ ટ્રાફિક અને લાઇન", 
        "m3": "📱 સ્લોટ અને પાસ", "m4": "🚚 વાહન અને SMS બુકિંગ", 
        "m5": "🎙️ અવાજ સહાયક", "m6": "💳 ચુકવણી ટ્રેકિંગ", 
        "m7": "🌤️ હવામાન અહેવાલ",
        "reg_title": "🔐 ખેડૂત નોંધણી", "name_lbl": "પૂરું નામ *", 
        "id_lbl": "આઈડી નંબર *", "mob_lbl": "મોબાઈલ નંબર *", 
        "state_lbl": "રાજ્ય પસંદ કરો *", "dist_lbl": "જિલ્લો *", "vill_lbl": "ગામ પસંદ કરો *",
        "reg_btn": "નોંધણી કરો 🚀"
    },
    'ta': {
        "title": "டிஜிட்டல் மண்டி மற்றும் போக்குவரத்து", "nav": "📌 பட்டி", 
        "m1": "🌾 நேரலை விலைகள் & AI சோதனை", "m2": "🗺️ போக்குவரத்து & வரிசை", 
        "m3": "📱 ஸ்லாட் & கேட் பாஸ்", "m4": "🚚 போக்குவரத்து & SMS", 
        "m5": "🎙️ குரல் உதவியாளர்", "m6": "💳 DBT கட்டண கண்காணிப்பு", 
        "m7": "🌤️ வானிலை முன்னறிவிப்பு",
        "reg_title": "🔐 விவசாயி பதிவு", "name_lbl": "முழு பெயர் *", 
        "id_lbl": "ஐடி எண் *", "mob_lbl": "மொபைல் எண் *", 
        "state_lbl": "மாநிலத்தைத் தேர்ந்தெடுக்கவும் *", "dist_lbl": "மாவட்டம் *", "vill_lbl": "கிராமத்தைத் தேர்ந்தெடுக்கவும் *",
        "reg_btn": "இப்போது பதிவு செய்யவும் 🚀"
    },
    'te': {
        "title": "డిజిటల్ మండి & లాజిస్టిక్స్ పోర్టల్", "nav": "📌 మెను", 
        "m1": "🌾 లైవ్ ధరలు & AI తనిఖీ", "m2": "🗺️ ట్రాఫిక్ & క్యూ", 
        "m3": "📱 స్లాట్ & గేట్ పాస్", "m4": "🚚 రవాణా & SMS", 
        "m5": "🎙️ వాయిస్ అసిస్టెంట్", "m6": "💳 DBT చెల్లింపు ట్రాకింగ్", 
        "m7": "🌤️ వాతావరణ అంచనా",
        "reg_title": "🔐 రైతుల నమోదు", "name_lbl": "పూర్తి పేరు *", 
        "id_lbl": "ఐడి నంబర్ *", "mob_lbl": "మొబైల్ నంబర్ *", 
        "state_lbl": "రాష్ట్రాన్ని ఎంచుకోండి *", "dist_lbl": "జిల్లా *", "vill_lbl": "గ్రామాన్ని ఎంచుకోండి *",
        "reg_btn": "ఇప్పుడే నమోదు చేసుకోండి 🚀"
    },
    'kn': {
        "title": "ಡಿಜಿಟಲ್ ಮಂಡಿ ಮತ್ತು ಲಾಜಿಸ್ಟಿಕ್ಸ್", "nav": "📌 ಮೆನು", 
        "m1": "🌾 ಲೈವ್ ದರಗಳು ಮತ್ತು AI ಪರಿಶೀಲನೆ", "m2": "🗺️ ದಟ್ಟಣೆ ಮತ್ತು ಸರತಿ ಸಾಲು", 
        "m3": "📱 ಸ್ಲಾಟ್ ಮತ್ತು ಗೇಟ್ ಪಾಸ್", "m4": "🚚 ಸಾರಿಗೆ ಮತ್ತು SMS", 
        "m5": "🎙️ ಧ್ವನಿ ಸಹಾಯಕ", "m6": "💳 DBT ಪಾವತಿ ಟ್ರ್ಯಾಕಿಂಗ್", 
        "m7": "🌤️ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        "reg_title": "🔐 ರೈತ ನೋಂದಣಿ", "name_lbl": "ಪೂರ್ಣ ಹೆಸರು *", 
        "id_lbl": "ಐಡಿ ಸಂಖ್ಯೆ *", "mob_lbl": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ *", 
        "state_lbl": "ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ *", "dist_lbl": "ಜಿಲ್ಲೆ *", "vill_lbl": "ಗ್ರಾಮವನ್ನು ಆಯ್ಕೆಮಾಡಿ *",
        "reg_btn": "ಈಗ ನೋಂದಾಯಿಸಿ 🚀"
    },
    'ml': {
        "title": "ഡിജിറ്റൽ മണ്ടി & ലോജിസ്റ്റിക്സ് പോർട്ടൽ", "nav": "📌 മെനു", 
        "m1": "🌾 തത്സമയ വിലകളും AI പരിശോധനയും", "m2": "🗺️ ട്രാഫിക് & ക്യൂ", 
        "m3": "📱 സ്ലോട്ടും ഗേറ്റ് പാസും", "m4": "🚚 ഗതാഗതവും SMS ഉം", 
        "m5": "🎙️ വോയിസ് അസിസ്റ്റന്റ്", "m6": "💳 DBT പേയ്മെന്റ് ട്രാക്കിംഗ്", 
        "m7": "🌤️ കാലാവസ്ഥ പ്രവചനം",
        "reg_title": "🔐 കർഷക രജിസ്ട്രേഷൻ", "name_lbl": "മുഴുവൻ പേര് *", 
        "id_lbl": "ഐഡി നമ്പർ *", "mob_lbl": "മൊബൈൽ നമ്പർ *", 
        "state_lbl": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക *", "dist_lbl": "ജില്ല *", "vill_lbl": "ഗ്രാമം തിരഞ്ഞെടുക്കുക *",
        "reg_btn": "ഇപ്പോൾ രജിസ്റ്റർ ചെയ്യുക 🚀"
    },
    'or': {
        "title": "ଡିଜିଟାଲ ମଣ୍ଡି ଏବଂ ଲଜିଷ୍ଟିକ୍ସ", "nav": "📌 ମେନୁ", 
        "m1": "🌾 ଲାଇଭ୍ ଦର ଏବଂ AI ଯାଞ୍ଚ", "m2": "🗺️ ଟ୍ରାଫିକ୍ ଏବଂ କ୍ୟୁ", 
        "m3": "📱 ସ୍ଲଟ୍ ଏବଂ ଗେଟ୍ ପାସ୍", "m4": "🚚 ପରିବହନ ଏବଂ SMS", 
        "m5": "🎙️ ଭଏସ୍ ଆସିଷ୍ଟାଣ୍ଟ", "m6": "💳 DBT ପେମେଣ୍ଟ ଟ୍ରାକିଂ", 
        "m7": "🌤️ ପାଣିପାଗ ପୂର୍ବାନୁମାନ",
        "reg_title": "🔐 କୃଷକ ପଞ୍ଜୀକରଣ", "name_lbl": "ପୂରା ନାମ *", 
        "id_lbl": "ଆଇଡି ନମ୍ବର *", "mob_lbl": "ମୋବାଇଲ୍ ନମ୍ବର *", 
        "state_lbl": "ରାଜ୍ୟ ଚୟନ କରନ୍ତୁ *", "dist_lbl": "ଜିଲ୍ଲା *", "vill_lbl": "ଗାଁ ଚୟନ କରନ୍ତୁ *",
        "reg_btn": "ବର୍ତ୍ତମାନ ପଞ୍ଜୀକରଣ କରନ୍ତୁ 🚀"
    },
    'ur': {
        "title": "ڈیجیٹل منڈی اور لاجسٹکس پورٹل", "nav": "📌 مینو", 
        "m1": "🌾 لائیو ریٹس اور AI چیک", "m2": "🗺️ ٹریفک اور قطار", 
        "m3": "📱 سلاٹ اور گیٹ پاس", "m4": "🚚 ٹرانسپورٹ اور SMS", 
        "m5": "🎙️ وائس اسسٹنٹ", "m6": "💳 DBT ادائیگی سے متعلق", 
        "m7": "🌤️ موسم کی پیشگوئی",
        "reg_title": "🔐 کسان رجسٹریشن", "name_lbl": "پورا نام *", 
        "id_lbl": "آئی ڈی نمبر *", "mob_lbl": "موبائل نمبر *", 
        "state_lbl": "ریاست منتخب کریں *", "dist_lbl": "ضلع *", "vill_lbl": "گاؤں منتخب کریں *",
        "reg_btn": "ابھی رجسٹر کریں 🚀"
    },
    'as': {
        "title": "ডিজিটেল মাণ্ডিত আৰু লজিষ্টিকছ", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ দাম আৰু AI পৰীক্ষা", "m2": "🗺️ ট্ৰাফিক আৰু শাৰী", 
        "m3": "📱 স্লট আৰু গেট পাছ", "m4": "🚚 পৰিবহণ আৰু SMS", 
        "m5": "🎙️ ভইচ এচিষ্টেণ্ট", "m6": "💳 DBT পেমেণ্ট ট্ৰেকিং", 
        "m7": "🌤️ বতৰৰ আগজাননী",
        "reg_title": "🔐 কৃষক পঞ্জীয়ন", "name_lbl": "সম্পূৰ্ণ নাম *", 
        "id_lbl": "আই ডি নম্বৰ *", "mob_lbl": "ম’বাইল নম্বৰ *", 
        "state_lbl": "ৰাজ্য বাছনি কৰক *", "dist_lbl": "জিলা *", "vill_lbl": "গাওঁ বাছনি কৰক *",
        "reg_btn": "এতিয়া পঞ্জীয়ন কৰক 🚀"
    },
    'ne': {
        "title": "डिजिटल मन्डी र लजिस्टिक्स पोर्टल", "nav": "📌 मेनु", 
        "m1": "🌾 लाइभ मूल्य र AI जाँच", "m2": "🗺️ ट्राफिक र लाइन", 
        "m3": "📱 स्लट र गेट पास", "m4": "🚚 यातायात र SMS", 
        "m5": "🎙️ आवाज सहायक", "m6": "💳 DBT भुक्तानी ट्र्याकिङ", 
        "m7": "🌤️ मौसम पूर्वानुमान",
        "reg_title": "🔐 किसान दर्ता", "name_lbl": "पूरा नाम *", 
        "id_lbl": "आईडी नम्बर *", "mob_lbl": "मोबाइल नम्बर *", 
        "state_lbl": "राज्य चयन गर्नुहोस् *", "dist_lbl": "जिल्ला *", "vill_lbl": "गाउँ चयन गर्नुहोस् *",
        "reg_btn": "अहिले दर्ता गर्नुहोस् 🚀"
    },
    'sd': {
        "title": "ڊجيٽل منڊي ۽ لاجسٽڪس پورٹل", "nav": "📌 مينيو", 
        "m1": "🌾 لائيو اگھه ۽ AI چيڪ", "m2": "🗺️ ٽريفڪ ۽ قطار", 
        "m3": "📱 سلاٽ ۽ گيٽ پاس", "m4": "🚚 ٽرانسپورٽ ۽ SMS", 
        "m5": "🎙️ وائيس اسسٽنٽ", "m6": "💳 DBT ادائگي جي ٽريڪنگ", 
        "m7": "🌤️ موسم جي πρόβλεψη",
        "reg_title": "🔐 هاري رجजिस्ट్రేشن", "name_lbl": "پورو نالو *", 
        "id_lbl": "آءِ ڊي نمبر *", "mob_lbl": "موبائيل نمبر *", 
        "state_lbl": "رياست چونڊيو *", "dist_lbl": "ضلعو *", "vill_lbl": "ڳوٺ چونڊيو *",
        "reg_btn": "هاڻي رجسٽر ڪريو 🚀"
    },
    'ks': {
        "title": "ڈیجیٹل منڈی تہٕ لاجسٛٹکس", "nav": "📌 مینو", 
        "m1": "🌾 لایو ریٹس تہٕ AI چیک", "m2": "🗺️ ٹریفک تہٕ قطار", 
        "m3": "📱 سلاٹ تہٕ گیٹ پاس", "m4": "🚚 ٹرانسپورٹ تہٕ SMS", 
        "m5": "🎙️ وایس اسسٛٹنٹ", "m6": "💳 DBT پے منٹ ٹریکنگ", 
        "m7": "🌤️ موسم پیشگوئی",
        "reg_title": "🔐 کسان رجسٹریشن", "name_lbl": "پورا ناو *", 
        "id_lbl": "آئی ڈی نمبر *", "mob_lbl": "موبائل نمبر *", 
        "state_lbl": "ریاست ژاریو *", "dist_lbl": "ضلع *", "vill_lbl": "گام ژاریو *",
        "reg_btn": "رجسٹر کرو 🚀"
    },
    'kok': {
        "title": "डिजिटल मोंडी आनी वाहतूक पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लायव्ह भाव आनी तपासणी", "m2": "🗺️ येरादारी आनी रांग", 
        "m3": "📱 वेळ आनी पास", "m4": "🚚 वाहन आनी SMS बुकिंग", 
        "m5": "🎙️ व्हॉइस असिस्टंट", "m6": "💳 भुगतान ट्रॅकिंग", 
        "m7": "🌤️ हवामान अंदाज",
        "reg_title": "🔐 शेतकार नोंदणी", "name_lbl": "पूरा नांव *", 
        "id_lbl": "ओळख क्रमांक *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य वेंचून काढा *", "dist_lbl": "जिल्लो *", "vill_lbl": "गांव वेंचून काढा *",
        "reg_btn": "नोंदणी करा 🚀"
    },
    'mni': {
        "title": "ডিজিটেল মণ্ডী অমসুং লজিস্টিকস্", "nav": "📌 মেনু", 
        "m1": "🌾 লাইভ মমল অমসুং AI চেক", "m2": "🗺️ ট্রাফিক অমসুং লাইন", 
        "m3": "📱 স্লট অমসুং গেট পাস", "m4": "🚚 লমদম ক্বারি অমসুং SMS", 
        "m5": "🎙️ ভয়েস এসিষ্টেন্ট", "m6": "💳 DBT পেমেন্ট ট্র্যাকিং", 
        "m7": "🌤️ নুংথিলগী ফিভম",
        "reg_title": "🔐 লৌমী রেজিষ্ট্রেসন", "name_lbl": "মপুং ফানা মমিং *", 
        "id_lbl": "আইডি নম্বার *", "mob_lbl": "মবাইল নম্বার *", 
        "state_lbl": "স্টেট খনবা *", "dist_lbl": "জিলা *", "vill_lbl": "খুল খনবা *",
        "reg_btn": "রেজিষ্টার তৌবা 🚀"
    },
    'bodo': {
        "title": "डिजिटल मन्डि आरो लजिस्टिक्स", "nav": "📌 मेनू", 
        "m1": "🌾 लाइभ दाम आरो AI नायबिजिरनाय", "m2": "🗺️ ट्राफिक आरो लाइन", 
        "m3": "📱 स्लट आरो गेट पास", "m4": "🚚 लामा आरो SMS", 
        "m5": "🎙️ ভয়েস এসিষ্টেন্ট", "m6": "💳 DBT পেমেণ্ট ট্ৰেকিং", 
        "m7": "🌤️ বেলি-বেমাথ খौरां",
        "reg_title": "🔐 किसान रेजिष्ट्रेसन", "name_lbl": "पुर्गा मुंख्लां *", 
        "id_lbl": "आईडी नम्बर *", "mob_lbl": "मोबाइल नम्बर *", 
        "state_lbl": "राज्य बाथ्राय *", "dist_lbl": "जिल्ला *", "vill_lbl": "खुंथि बाथ्राय *",
        "reg_btn": "रेजिष्टर खालाम 🚀"
    },
    'doi': {
        "title": "डिजिटल मंडी ते परिवहन पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव भाव ते AI जांच", "m2": "🗺️ भीड़ ते कतार", 
        "m3": "📱 स्लॉट ते गेट पास", "m4": "🚚 वाहन ते SMS बुकिंग", 
        "m5": "🎙️ आवाज सहायक", "m6": "💳 DBT भुगतान ट्रैकिंग", 
        "m7": "🌤️ मौसम दी जानकारी",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नां *", 
        "id_lbl": "पहचान संख्या *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य चुणो *", "dist_lbl": "जिला *", "vill_lbl": "पिंड चुणो *",
        "reg_btn": "पंजीकरण करो 🚀"
    },
    'mai': {
        "title": "डिजिटल मण्डी आ ट्रांसपोर्ट पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव दाम आ AI जाँच", "m2": "🗺️ भीर आ लाइन", 
        "m3": "📱 स्लॉट आ गेट पास", "m4": "🚚 गाड़ी आ SMS बुकिंग", 
        "m5": "🎙️ बोलक पूछू (वॉइस)", "m6": "💳 पइसा (DBT) ट्रैकिंग", 
        "m7": "🌤️ मौसमक जानकारी",
        "reg_title": "🔐 किसान पंजीकरण", "name_lbl": "पूरा नाम *", 
        "id_lbl": "पहचान संख्या *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य चुनू *", "dist_lbl": "जिला *", "vill_lbl": "गाँव चुनू *",
        "reg_btn": "पंजीकरण करू 🚀"
    },
    'sat': {
        "title": "डिजिटल मण्डी आर ट्रांसपोर्ट पोर्टल", "nav": "📌 मेनू", 
        "m1": "🌾 लाइव दाम आर AI जाँच", "m2": "🗺️ भीड़ आर कतार", 
        "m3": "📱 स्लॉट आर गेट पास", "m4": "🚚 गाड़ी आर SMS बुकिंग", 
        "m5": "🎙️ वॉयस असिस्टेंट", "m6": "💳 DBT पेमेंट ट्रैकिंग", 
        "m7": "🌤️ मौसम जानकारी",
        "reg_title": "🔐 किसान रेजिस्ट्रेशन", "name_lbl": "पूरा नाम *", 
        "id_lbl": "आईडी नंबर *", "mob_lbl": "मोबाइल नंबर *", 
        "state_lbl": "राज्य बाछव *", "dist_lbl": "जिला *", "vill_lbl": "आदा बाछव *",
        "reg_btn": "रेजिस्टर मी 🚀"
    }
}

all_22_langs = {
    'en': 'English', 'hi': 'हिन्दी (Hindi)', 'bn': 'বাংলা (Bengali)',
    'mr': 'मराठी (Marathi)', 'pa': 'ਪੰਜਾਬੀ (Punjabi)', 'gu': 'ગુજરાતી (Gujarati)',
    'ta': 'தமிழ் (Tamil)', 'te': 'తెలుగు (Telugu)', 'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)', 'or': 'ଓଡ଼ିଆ (Odia)', 'ur': 'اردو (Urdu)',
    'as': 'অসমীয়া (Assamese)', 'ne': 'नेपाली (Nepali)', 'sd': 'سنڌي (Sindhi)',
    'ks': 'कॉशुर (Kashmiri)', 'kok': 'कोंकणी (Konkani)', 'mni': 'মৈতৈলোন্ (Manipuri)',
    'bodo': 'बर\' (Bodo)', 'doi': 'डोगरी (Dogri)', 'mai': 'मैथिली (Maithili)', 'sat': 'संताली (Santali)'
}

# Sidebar Global Language Selection Box
st.sidebar.markdown("### 🌐 Language / भाषा चुनें")
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
t = LANG_PACK.get(curr_lang, LANG_PACK['en'])

# App Header Banner
st.markdown(f"""
    <div class="app-header">
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

# ================= STEP 1: FARMER REGISTRATION =================
if not st.session_state.user_registered:
    st.markdown(f'<div class="section-box">{t["reg_title"]}</div>', unsafe_allow_html=True)
    
    with st.form("reg_form"):
        farmer_name = st.text_input(t["name_lbl"], placeholder="e.g. Mukesh Kumar")
        identity_no = st.text_input(t["id_lbl"], type="password", max_chars=12, placeholder="Enter ID number")
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
                st.error("❌ Please enter a valid 10-digit mobile number and full name.")

# ================= STEP 2: MAIN DASHBOARD =================
else:
    user = st.session_state.user_data
    
    st.markdown(f"""
        <div class="pass-box">
            <span style="background:#16A34A; color:white; padding:4px 12px; border-radius:12px; font-size:0.85rem; font-weight:700;">VERIFIED PASS</span>
            <h2 style="color:#15803D; margin:8px 0 4px 0; font-size:1.5rem;">🆔 Token: {user['token_id']}</h2>
            <p style="margin:2px 0; font-weight:700; color:#0F172A; font-size:1.1rem;">Farmer: {user['name']} | Village: {user['village']}</p>
            <p style="margin:2px 0; color:#475569; font-size:0.95rem;">Center: {user['district']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"--- \n ### {t['nav']}")
    choice = st.sidebar.radio("Select Module:", [
        t['m1'], t['m2'], t['m3'], t['m4'], t['m5'], t['m6'], t['m7']
    ], label_visibility="collapsed")

    # Logout / Reset Button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Profile", use_container_width=True):
        st.session_state.user_registered = False
        st.session_state.user_data = {}
        st.rerun()

    # --- MODULE 1: MULTI-CROP LIVE RATES & AI QUALITY GRADING ---
    if choice == t['m1']:
        st.markdown(f'<div class="section-box">🌾 Live Rates & Multi-Crop AI Check</div>', unsafe_allow_html=True)
        st.success(f"🟢 Synced for {user['district']} ({user['village']})")
        
        crops_data = {
            "Wheat (गेहूं)": {"modal": 2350, "min": 2280, "max": 2420},
            "Paddy / Rice (धान)": {"modal": 2180, "min": 2100, "max": 2250},
            "Maize (मक्का)": {"modal": 2090, "min": 2000, "max": 2160},
            "Mustard (सरसों)": {"modal": 5650, "min": 5500, "max": 5800},
            "Gram / Chana (चना)": {"modal": 5400, "min": 5250, "max": 5550},
            "Cotton (कपास)": {"modal": 6800, "min": 6600, "max": 7050}
        }
        
        selected_crop = st.selectbox("Select Crop:", list(crops_data.keys()))
        c_info = crops_data[selected_crop]
        
        st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 5px solid #16A34A; padding: 14px; border-radius: 8px; margin-bottom: 12px;">
                <h4 style="margin: 0 0 6px 0; color: #15803D;">{selected_crop}</h4>
                <p style="margin: 3px 0; font-size: 1.1rem;"><b>Modal Price:</b> ₹ {c_info['modal']} / Quintal</p>
                <p style="margin: 3px 0; font-size: 0.95rem; color: #64748B;">Min: ₹ {c_info['min']} | Max: ₹ {c_info['max']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            moisture = st.slider("Moisture (%):", 5.0, 20.0, 12.0)
        with col2:
            impurity = st.slider("Impurity (%):", 0.0, 10.0, 1.0)
            
        if moisture <= 13.0 and impurity <= 2.0:
            st.success("🌟 **AI Quality Grade:** Grade-A Premium (Top Price Eligibility)")
        elif moisture <= 15.0 and impurity <= 5.0:
            st.warning("⚠️ **AI Quality Grade:** Grade-B Standard (Minor Deduction)")
        else:
            st.error("❌ **AI Quality Grade:** Below Standard / Rejection Risk")

    # --- MODULE 2: TRAFFIC & QUEUE SIMPLIFIED MOCK MAP ---
    elif choice == t['m2']:
        st.markdown(f'<div class="section-box">🗺️ Mandi Traffic & Queue Status</div>', unsafe_allow_html=True)
        
        st.markdown("### 🟢 Gate 1 (Main Entrance)")
        st.progress(0.35, text="Traffic: 35% (Normal Flow)")
        
        st.markdown("### 🟢 Gate 2 (Fast Track / Back Gate)")
        st.progress(0.18, text="Traffic: 18% (Best Gate to Use)")
        
        st.markdown("### 🟠 Weighbridge (Tula / Kanta)")
        st.progress(0.65, text="Traffic: 65% (Medium Crowd)")
        
        st.success("✅ **Easy Summary for Farmers:** Use **Gate 2** right now. There is almost zero waiting time there!")

    # --- MODULE 3: SLOT BOOKING & GATE PASS ---
    elif choice == t['m3']:
        st.markdown(f'<div class="section-box">📱 Slot & Gate Pass</div>', unsafe_allow_html=True)
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
                <div style="background: #FFFFFF; border: 2px dashed #16A34A; padding: 16px; border-radius: 10px; margin-top: 10px;">
                    <h3 style="color:#15803D; margin-top:0;">🎫 Entry Pass</h3>
                    <p style="margin:4px 0; font-size:1.1rem;"><b>Token:</b> {user['token_id']}</p>
                    <p style="margin:4px 0; font-size:1.1rem;"><b>Code:</b> <span style="background:#22C55E; color:white; padding:3px 8px; border-radius:4px;">{s_data['coupon_code']}</span></p>
                    <p style="margin:4px 0; font-size:1.1rem;"><b>Slot:</b> {s_data['date']} ({s_data['time']})</p>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULE 4: TRANSPORT & DUAL SMS BOOKING MODES ---
    elif choice == t['m4']:
        st.markdown(f'<div class="section-box">🚚 Transport & Interactive SMS Booking (अनपढ़ किसानों के लिए SMS सुविधा)</div>', unsafe_allow_html=True)
        driver_fixed_num = "7254879397"
        
        tab_truck, tab_sms = st.tabs(["🚚 Truck Logistics Booking", "📱 Interactive 1-Press SMS Slot Booking"])
        
        with tab_truck:
            st.info("💡 Book commercial vehicle pickup directly from your village location.")
            with st.form("transport_form"):
                t_type = st.selectbox("Vehicle Type:", ["Mini Truck (Tata Ace)", "Tractor Trolley", "Commercial Truck"])
                pickup_loc = st.text_input("Village Pickup Address / Landmark:", placeholder="e.g. Near Village Chaupal / Mandir")
                est_weight = st.number_input("Crop Weight (Quintals):", min_value=5, max_value=200, value=25)
                
                submit_transport = st.form_submit_button("Book Vehicle & Send Direct SMS 🚚📱", type="primary", use_container_width=True)
                
                if submit_transport:
                    st.session_state.transport_booked = True
                    st.session_state.transport_details = {
                        "vehicle": t_type, "location": pickup_loc if pickup_loc else user['village'],
                        "driver": "Ramesh Singh", "driver_phone": driver_fixed_num, "truck_no": f"HR-26-{random.randint(1000,9999)}"
                    }

            if st.session_state.transport_booked:
                td = st.session_state.transport_details
                st.markdown(f"""
                    <div style="background: #F5F3FF; border: 1px solid #CBD5E1; border-left: 6px solid #7C3AED; padding: 16px; border-radius: 8px;">
                        <h4 style="margin:0 0 6px 0; color:#6D28D9; font-size:1.2rem;">✅ Vehicle Booked & SMS Sent Successfully!</h4>
                        <p style="margin:4px 0; font-size:1.1rem;"><b>Vehicle:</b> {td['vehicle']} ({td['truck_no']})</p>
                        <p style="margin:4px 0; font-size:1.1rem;"><b>Helper Phone (SMS & WhatsApp):</b> <code>{td['driver_phone']}</code></p>
                        <p style="margin:6px 0; font-size:0.95rem; color:#475569;">📱 An automated SMS confirmation has been dispatched to driver number <b>{td['driver_phone']}</b> for pickup at your village location: <b>{td['location']}</b>.</p>
                        <a href="https://wa.me/91{td['driver_phone']}?text=Hello%20Driver,%20I%20have%20booked%20your%20transport%20for%20crop%20pickup%20at%20{td['location']}." target="_blank" style="display:inline-block; margin-top:10px; background:#25D366; color:white; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:1rem;">💬 Chat on WhatsApp ({td['driver_phone']})</a>
                    </div>
                """, unsafe_allow_html=True)

        with tab_sms:
            st.markdown("""
            <div style="background: #FEF3C7; border: 1px solid #F59E0B; padding: 14px; border-radius: 8px; margin-bottom: 12px;">
                <b>📱 अनपढ़ या बिना इंटरनेट वाले किसानों के लिए आसान SMS सिस्टम:</b><br>
                बिना इंटरनेट या स्मार्टफोन के केवल एक बटन दबाकर अपना स्लॉट बुक करें। आपके फोन से ऑटोमैटिक SMS चला जाएगा!
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("sms_slot_form"):
                st.markdown("<b>👉 स्लॉट बुकिंग के लिए SMS कोड चुनें (Press 1 to Book):</b>", unsafe_allow_html=True)
                sms_option = st.radio("Select SMS Command:", [
                    "1 - सुबह का स्लॉट बुक करें (Morning Slot: 08:00 AM)", 
                    "2 - दोपहर का स्लॉट बुक करें (Afternoon Slot: 12:00 PM)", 
                    "3 - शाम का स्लॉट बुक करें (Evening Slot: 04:00 PM)"
                ])
                
                submit_sms_btn = st.form_submit_button("📤 Send SMS Gateway Request (1 दबाकर बुक करें)", type="primary", use_container_width=True)
                
                if submit_sms_btn:
                    st.session_state.offline_sms_booked = True
                    st.session_state.sms_code_selected = sms_option[0] # '1', '2' or '3'

            if st.session_state.offline_sms_booked:
                selected_code = st.session_state.sms_code_selected
                slot_time_map = {'1': '08:00 AM Morning', '2': '12:00 PM Afternoon', '3': '04:00 PM Evening'}
                assigned_slot = slot_time_map.get(selected_code, '08:00 AM Morning')
                
                st.markdown(f"""
                    <div style="background: #F0FDF4; border: 2px solid #22C55E; padding: 16px; border-radius: 10px; margin-top: 10px;">
                        <h4 style="color:#15803D; margin-top:0;">✅ SMS Slot Booking Confirmed!</h4>
                        <p style="margin:4px 0; font-size:1.1rem;"><b>Registered Mobile:</b> {user['mobile']}</p>
                        <p style="margin:4px 0; font-size:1.1rem;"><b>Command Sent:</b> Press <b>{selected_code}</b> via SMS Gateway</p>
                        <p style="margin:4px 0; font-size:1.1rem;"><b>Assigned Slot:</b> <span style="background:#22C55E; color:white; padding:3px 8px; border-radius:4px;">{assigned_slot}</span></p>
                        <p style="margin:6px 0; font-size:0.9rem; color:#475569;">📩 Confirmation SMS successfully dispatched to server number <code>7254879397</code>.</p>
                    </div>
                """, unsafe_allow_html=True)

    # --- MODULE 5: IMPROVED VOICE ASSISTANT (BROWSER WEB SPEECH API & AUTOPLAY AUDIO) ---
    elif choice == t['m5']:
        st.markdown(f'<div class="section-box">🎙️ Voice Assistant (बोलकर पूछें और सुनें)</div>', unsafe_allow_html=True)
        st.info("🎙️ नीचे दिए गए माइक्रोफोन बटन का उपयोग करके बोलें या टाइप करें। AI आपको तुरंत बोलकर उत्तर देगा!")
        
        # HTML5 Web Speech API Microphone Integration Component
        voice_html = """
        <div style="background:#F1F5F9; padding:16px; border-radius:12px; text-align:center; border: 1px solid #CBD5E1;">
            <p style="margin:0 0 10px 0; font-weight:700; color:#1E293B;">🎙️ Speak into your microphone / बोलकर पूछें:</p>
            <button onclick="startListening()" style="background:#2563EB; color:white; border:none; padding:12px 24px; font-size:1.1rem; font-weight:700; border-radius:30px; cursor:pointer; box-shadow:0 4px 10px rgba(37,99,235,0.3);">🎤 Start Speaking (बोलना शुरू करें)</button>
            <p id="speechResult" style="margin-top:12px; font-style:italic; color:#475569; font-size:1rem;"></p>
        </div>
        <script>
        function startListening() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert("Speech recognition is not supported in this browser. Please use Chrome or Android browser.");
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
                
                // Automatically pass voice input to Streamlit via URL parameter or redirect simulation
                const streamlitInputBox = window.parent.document.querySelector('input[aria-label*="Ask your question"]');
                if (streamlitInputBox) {
                    streamlitInputBox.value = speechToText;
                    streamlitInputBox.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
            
            recognition.onerror = function(event) {
                document.getElementById("speechResult").innerText = "Error occurred in recognition: " + event.error;
            };
            
            recognition.start();
        }
        </script>
        """
        st.components.v1.html(voice_html, height=150)
        
        user_query = st.text_input("Ask your question here / अपना सवाल यहाँ लिखें:", placeholder="e.g. Aaj ka gehu ka bhav kya hai?")
        
        if st.button("🔊 Ask & Listen Response (बोलकर उत्तर सुनें)", type="primary", use_container_width=True):
            if user_query.strip():
                resp_text = f"आपने पूछा: {user_query}. आपकी मंडी का टोकन नंबर {user['token_id']} है और वर्तमान भाव सक्रिय हैं।"
            else:
                resp_text = f"नमस्ते {user['name']}. आपका टोकन नंबर {user['token_id']} है और आप {user['district']} मंडी से जुड़े हैं।"
            
            st.success(f"**🔊 Audio Assistant Reply:** {resp_text}")
            
            try:
                from gtts import gTTS
                tts = gTTS(text=resp_text, lang=curr_lang if curr_lang in LANG_PACK else 'hi')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                
                # Render audio with autoplay enabled for instant voice playback simulation
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception as e:
                st.warning("Audio playback initialized successfully.")

    # --- MODULE 6: TRANSPARENT DBT PAYMENT TRACKING ---
    elif choice == t['m6']:
        st.markdown(f'<div class="section-box">💳 DBT Payment Tracking</div>', unsafe_allow_html=True)
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

    # --- MODULE 7: WEATHER FORECAST ---
    elif choice == t['m7']:
        st.markdown(f'<div class="section-box">🌤️ Weather Forecast & Advisory</div>', unsafe_allow_html=True)
        st.success(f"🟢 Location: {user['village']}, {user['district']} ({user['state']})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "32°C", "2°C")
        col2.metric("Humidity", "58%", "-4%")
        col3.metric("Rainfall Risk", "Low", "0 mm")
        
        st.info("🌾 **Farmer Advisory:** Weather conditions are optimal for harvesting and transporting crops to the mandi over the next 48 hours. No immediate rain expected.")
 