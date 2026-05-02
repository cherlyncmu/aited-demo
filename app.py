import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AITED System", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #111;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
}
.title {
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED")
page = st.sidebar.radio("Menu", [
    "Dashboard",
    "New Scan",
    "Patient Records",
    "Analytics",
    "Settings"
])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", "128")
    col2.metric("Suspicious", "32")
    col3.metric("Normal", "76")

    st.subheader("📈 Risk Trend")
    st.line_chart([30, 55, 82, 60, 75])

    st.subheader("Recent Scans")
    st.table({
        "Date": ["30 Apr", "15 Apr"],
        "Risk": ["82%", "55%"],
        "Result": ["Suspicious", "Monitor"]
    })

# ---------------- NEW SCAN ----------------
elif page == "New Scan":
    st.title("🔍 Scan Result")

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("EIT Heatmap")

        x = np.linspace(-1,1,200)
        y = np.linspace(-1,1,200)
        X, Y = np.meshgrid(x,y)
        Z = np.exp(-(X**2 + Y**2)*3)

        # จำลองก้อน
        Z += np.exp(-((X-0.3)**2 + (Y+0.2)**2)*20)

        fig, ax = plt.subplots()
        ax.imshow(Z, cmap='jet')
        ax.axis('off')

        st.pyplot(fig)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="title">AI Analysis</div>', unsafe_allow_html=True)

        st.metric("Risk Score", "82%")
        st.error("⚠️ Suspicious")

        st.write("📍 Location: Right Lobe")
        st.write("📏 Size: ~1.2 cm")

        st.warning("Recommend ultrasound examination")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PATIENT RECORDS ----------------
elif page == "Patient Records":
    st.title("📋 Patient Records")

    st.table({
        "Name": ["John Doe", "Jane Smith"],
        "Last Scan": ["30 Apr", "15 Apr"],
        "Status": ["Suspicious", "Normal"]
    })

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("📊 Model Performance")

    col1, col2, col3 = st.columns(3)
    col1.metric("Sensitivity", "91%")
    col2.metric("Specificity", "76%")
    col3.metric("F1 Score", "0.83")

    st.subheader("Confusion Matrix")
    st.table({
        "Actual": ["Normal", "Cancer"],
        "Predicted": ["80", "90"]
    })

# ---------------- SETTINGS ----------------
elif page == "Settings":
    st.title("⚙️ Settings")

    st.selectbox("Device", ["AITED Collar v1"])
    st.selectbox("Frequency", ["50 kHz", "100 kHz"])
    st.slider("Current (mA)", 0.5, 2.0, 1.0)

    if st.button("Save Settings"):
        st.success("Settings saved!")
