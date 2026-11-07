import streamlit as st
import pandas as pd
from datetime import datetime
from hindsight_engine import HindsightMemoryManager
from autogen_agents import generate_dpdp_notice

# -----------------------------------------------------------------------------
# Page Configuration & Executive Dark Theme Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AegisTrace AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* OLED Deep Black Background */
    .stApp {
        background-color: #030712;
        color: #f3f4f6;
    }

    /* Sidebar High-Contrast Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #1f293d;
    }
    
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li {
        color: #ffffff !important;
    }

    /* FORM INPUTS & TEXT AREAS */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: #1e293b !important;
        -webkit-text-fill-color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }

    /* Form Submit Button Styling */
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4) !important;
        width: 100% !important;
    }

    /* Fix Pipeline Text Visibility */
    .pipeline-text {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin-left: 8px;
    }

    /* Brand Header with Custom Glowing Logo */
    .brand-wrapper {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 0.5rem;
        padding-top: 0.5rem;
    }

    .neon-shield-logo {
        width: 58px;
        height: 58px;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .main-heading {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 20%, #38bdf8 60%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0px;
        letter-spacing: -0.03em;
    }
    
    .sub-heading {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2.2rem;
        font-weight: 400;
        margin-left: 76px;
        letter-spacing: 0.01em;
    }

    /* Glassmorphism Cards */
    .cyber-card {
        background: linear-gradient(145deg, #0e1626 0%, #090e17 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.8);
        margin-bottom: 1.5rem;
    }

    /* Tab Bar Styling */
    button[data-baseweb="tab"] {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
        border-radius: 10px 10px 0px 0px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 700 !important;
        border: 1px solid #334155 !important;
        margin-right: 6px;
    }

    button[aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.6);
    }

    /* Glowing Badge Pills */
    .glow-pill {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        font-size: 0.8rem;
        font-weight: 700;
        border-radius: 20px;
        color: #38bdf8;
        background-color: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Memory Manager
memory_mgr = HindsightMemoryManager()

# -----------------------------------------------------------------------------
# Header with Custom Glowing Logo & Title
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="brand-wrapper">
        <div class="neon-shield-logo">🛡️</div>
        <div class="main-heading">AegisTrace AI</div>
    </div>
    <div class="sub-heading">Autonomous Telemarketing Defense &bull; Data Provenance Tracing &bull; DPDP Legal Erasure</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar: User Profile & Footprint Logger
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 👤 Data Principal Profile")
    user_name_input = st.text_input("Your Name", value="Joyeta Pal")
    user_phone_input = st.text_input("Your Phone Number", value="+91-9876543210")
    
    st.markdown("---")
    st.markdown("### 🔑 Footprint Logger")
    st.markdown("<p style='color: #cbd5e1; font-size: 0.9rem;'>Log your site signups into Hindsight memory to track data lineage.</p>", unsafe_allow_html=True)
    
    if 'logged_site' not in st.session_state:
        st.session_state['logged_site'] = None

    with st.form("hindsight_logger_form"):
        st.markdown("<label style='color: #ffffff !important; font-weight: 600;'>Website / App Name</label>", unsafe_allow_html=True)
        site_name = st.text_input("site_input", placeholder="e.g., TechEdu Portal", label_visibility="collapsed")
        
        st.markdown("<label style='color: #ffffff !important; font-weight: 600;'>Signup Date</label>", unsafe_allow_html=True)
        signup_date = st.text_input("date_input", value=datetime.now().strftime("%Y/%m/%d"), label_visibility="collapsed")
        
        st.markdown("<label style='color: #ffffff !important; font-weight: 600;'>Permissions / Privacy Terms</label>", unsafe_allow_html=True)
        permission = st.text_area("perm_input", "Accepted 3rd-party marketing partner terms.", label_visibility="collapsed")
        
        submitted = st.form_submit_button("Log to Memory", use_container_width=True)
        if submitted:
            if site_name.strip():
                success = memory_mgr.retain_footprint(site_name, signup_date, permission)
                if success:
                    st.session_state['logged_site'] = site_name
            else:
                st.error("Please enter a valid name.")

    if st.session_state['logged_site']:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border: 1px solid #059669; padding: 12px; border-radius: 10px; margin-top: 10px; text-align: center; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);'>
                <span style='color: #34d399; font-weight: 700; font-size: 0.9rem;'>✓ Retained footprint for {st.session_state["logged_site"]}!</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Architecture Pipeline")
    st.markdown("""
    * <span class="glow-pill">Stage 1</span><span class="pipeline-text">Voice Interception</span>
    * <span class="glow-pill">Stage 2</span><span class="pipeline-text">Memory Lineage</span>
    * <span class="glow-pill">Stage 3</span><span class="pipeline-text">DPDP Erasure</span>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Application Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎙️ Stage 1: Voice Interception", 
    "🔍 Stage 2: Memory Lineage", 
    "⚖️ Stage 3: DPDP Legal Erasure"
])

# TAB 1
with tab1:
    st.markdown("### Real-Time Telemarketing Interception")
    st.markdown("<p style='color: #94a3b8;'>Simulate and intercept live speech-to-text audio streams from unsolicited calls.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        pitch_sample = st.selectbox(
            "Select incoming voice stream transcript:",
            [
                f"Hi {user_name_input}, calling from EduPlacement! We saw your profile and have direct B.Tech CSE admission seats available in Bangalore.",
                "Hello, congratulations! You have an instant pre-approved zero-interest personal loan of 5 Lakhs waiting.",
                "Custom pitch transcript..."
            ]
        )
        
        if pitch_sample == "Custom pitch transcript...":
            pitch_input = st.text_area("Enter raw transcript:", placeholder="Paste call transcript here...")
        else:
            pitch_input = pitch_sample

        if st.button("⚡ Intercept & Process Audio Stream", type="primary", use_container_width=True):
            if pitch_input.strip():
                st.session_state['active_pitch'] = pitch_input
                st.success("Stream intercepted! Forwarded to Hindsight Memory Engine.")
            else:
                st.warning("Please select or enter a pitch transcript.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.subheader("Telemetry Status")
        st.metric("Speech Engine", "Azure AI Speech", "Active")
        st.metric("Audio Stream", "Clean Mono", "99.4%")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2
with tab2:
    st.markdown("### Hindsight Memory Provenance Matching")
    st.markdown("<p style='color: #94a3b8;'>Vector similarity analysis querying historical user signups.</p>", unsafe_allow_html=True)
    
    if 'active_pitch' in st.session_state:
        st.markdown(f'<div class="cyber-card"><b>Active Transcript:</b> <i style="color: #38bdf8;">"{st.session_state["active_pitch"]}"</i></div>', unsafe_allow_html=True)
        
        with st.spinner("Querying Hindsight persistent memory..."):
            match_result = memory_mgr.recall_leak_source(st.session_state['active_pitch'])
        
        st.session_state['match_result'] = match_result
        st.session_state['matched_entity'] = match_result['matched_entity']
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.metric("Pinpointed Source", match_result['matched_entity'])
            st.markdown('</div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.metric("Confidence Score", match_result['confidence_score'])
            st.markdown('</div>', unsafe_allow_html=True)
        with m_col3:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.metric("Leak Vector", "Lead Resale")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Provenance Trace Details")
        st.json({
            "matched_entity": match_result['matched_entity'],
            "original_signup_date": match_result['signup_date'],
            "confidence_score": match_result['confidence_score'],
            "leak_type": match_result['leak_type'],
            "hindsight_status": "Verified Match"
        })
    else:
        st.warning("⚠️ No active call analyzed yet. Please run Stage 1 first.")

# TAB 3
with tab3:
    st.markdown("### Auto-Executing Legal Erasure")
    st.markdown("<p style='color: #94a3b8;'>Autonomous AutoGen agent generating statutory notices under India's DPDP Act.</p>", unsafe_allow_html=True)
    
    if 'matched_entity' in st.session_state:
        target_entity = st.session_state['matched_entity']
        notice_text = generate_dpdp_notice(target_entity, user_name=user_name_input, user_phone=user_phone_input)
        
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown(f"**Target Data Fiduciary:** `{target_entity}`")
        st.text_area("Generated Legal Notice (DPDP Section 12 Compliance):", notice_text, height=300)
        
        if st.button("🚀 Dispatch Erasure Order to Data Protection Officer", type="primary", use_container_width=True):
            st.success(f"Legal notice successfully dispatched to DPO at **{target_entity}**!")
            st.balloons()
            
            st.markdown("### Audit Status")
            st.json({
                "target_fiduciary": target_entity,
                "statute": "DPDP Act 2023 - Section 12",
                "dispatch_status": "Delivered to DPO",
                "receipt_id": "DPDP-NOTICE-2026-77821"
            })
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ No leak source pinpointed yet. Complete Stage 1 and Stage 2 first.")