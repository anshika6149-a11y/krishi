import streamlit as st
import requests
from urllib.parse import quote as url_encode

# Page Configuration
st.set_page_config(
    page_title="Krishi e-NAM Live Data Fetcher", 
    page_icon="🌾", 
    layout="centered"
)

st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h2>🌾 e-NAM Live Mandi Data Connector</h2>
        <p>Direct API Integration with Agmarknet Portal</p>
    </div>
""", unsafe_allow_html=True)

# User Input Form for Location
with st.form("enam_form"):
    st.markdown("### Enter Mandi Location Details")
    
    states_list = [
        "Bihar", "Uttar Pradesh", "Punjab", "Haryana", "Madhya Pradesh", 
        "Maharashtra", "Rajasthan", "Gujarat", "West Bengal", "Karnataka", "Odisha", "Assam"
    ]
    selected_state = st.selectbox("Select State", states_list)
    district_input = st.text_input("Enter District / Mandi Name", placeholder="e.g. Patna, Lucknow, Ludhiana")
    
    submit_btn = st.form_submit_button("Fetch Live e-NAM Data 🚀", use_container_width=True, type="primary")

if submit_btn:
    if not district_input.strip():
        st.error("❌ Please enter a valid district or mandi name.")
    else:
        with st.spinner("Connecting to e-NAM Live API..."):
            try:
                # Official e-NAM / data.gov.in agricultural market price resource endpoint
                api_url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&filters[state.keyword]={url_encode(selected_state)}&limit=20"
                
                response = requests.get(api_url, timeout=8)
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("records", [])
                    
                    if records:
                        # Filter records matching the user's district if possible
                        matched_records = [
                            r for r in records if district_input.lower() in r.get('district', '').lower() or 
                            district_input.lower() in r.get('market', '').lower()
                        ]
                        
                        display_records = matched_records if matched_records else records[:5]
                        
                        st.success(f"✅ Successfully fetched live data for {selected_state}!")
                        st.markdown(f"### 📊 Live Mandi Records ({len(display_records)} found)")
                        
                        for idx, rec in enumerate(display_records, 1):
                            mandi_name = rec.get('market', 'N/A')
                            commodity = rec.get('commodity', 'N/A')
                            variety = rec.get('variety', 'N/A')
                            modal_price = rec.get('modal_price', 'N/A')
                            min_price = rec.get('min_price', 'N/A')
                            max_price = rec.get('max_price', 'N/A')
                            date = rec.get('arrival_date', 'N/A')
                            
                            st.markdown(f"""
                                <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 5px solid #16A34A; padding: 15px; border-radius: 10px; margin-bottom: 12px;">
                                    <h4 style="margin: 0 0 5px 0; color: #15803D;">{idx}. Mandi: {mandi_name} ({selected_state})</h4>
                                    <p style="margin: 2px 0;"><b>Commodity:</b> {commodity} | <b>Variety:</b> {variety}</p>
                                    <p style="margin: 2px 0;"><b>Modal Price:</b> ₹ {modal_price} / Quintal</p>
                                    <p style="margin: 2px 0; font-size: 0.85rem; color: #64748B;">Min: ₹ {min_price} | Max: ₹ {max_price} | Date: {date}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No records found for this location in the live feed. Try another district.")
                else:
                    st.error(f"❌ API Error: Received status code {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection Failed: {e}")
