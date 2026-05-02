import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AITED Medical System", layout="wide")

# ---------------- SESSION ----------------
if "connected" not in st.session_state:
    st.session_state.connected = False

if "scanning" not in st.session_state:
    st.session_state.scanning = False

# ---------------- FUNCTIONS ----------------
def connect_device():
    with st.spinner("Connecting to device..."):
        time.sleep(2)
    st.session_state.connected = True

def disconnect_device():
    st.session_state.connected = False

def start_scan():
    st.session_state.scanning = True

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #020617;
}
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1e293b;
}
.big {
    font-size: 22px;
    font-weight: bold;
}
.scanbox {
    border: 2px solid #22c55e;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED")

st.sidebar.subheader("🔌 Device")

if st.session_state.connected:
    st.sidebar.success("🟢 Connected")
    if st.sidebar.button("Disconnect"):
        disconnect_device()
else:
    st.sidebar.error("🔴 Disconnected")
    if st.sidebar.button("Connect Device"):
        connect_device()

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Scan",
    "Patients",
    "Analytics"
])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 System Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", "128")
    c2.metric("High Risk", "32")
    c3.metric("Normal", "76")

    st.line_chart([30, 45, 60, 55, 82])

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Live Scan")

    if not st.session_state.connected:
        st.warning("⚠️ Connect device first")
        st.stop()

    col1, col2 = st.columns([2,1])

    # -------- LEFT: SCAN AREA --------
    with col1:
        st.markdown('<div class="scanbox">', unsafe_allow_html=True)

        if not st.session_state.scanning:
            if st.button("▶ Start Scan"):
                start_scan()

        if st.session_state.scanning:
            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)

            st.success("Scan Complete")
            st.session_state.scanning = False

            # Generate heatmap
            x = np.linspace(-1,1,200)
            y = np.linspace(-1,1,200)
            X, Y = np.meshgrid(x,y)

            Z = np.exp(-(X**2 + Y**2)*3)
            Z += np.exp(-((X-0.4)**2 + (Y+0.2)**2)*20)

            fig, ax = plt.subplots()
            ax.imshow(Z, cmap='jet')
            ax.set_title("EIT Imaging")
            ax.axis('off')

            st.pyplot(fig)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- RIGHT: RESULT --------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="big">AI Diagnosis</div>', unsafe_allow_html=True)

        st.metric("Risk Score", "82%")
        st.error("⚠️ Suspicious")

        st.write("📍 Right Thyroid")
        st.write("📏 Size ~1.2 cm")

        st.warning("Further imaging recommended")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PATIENTS ----------------
elif page == "Patients":
    st.title("👤 Patients")

    st.dataframe({
        "Name": ["John Doe", "Jane Smith"],
        "Last Scan": ["30 Apr", "15 Apr"],
        "Risk": ["82%", "30%"],
        "Status": ["High", "Normal"]
    })

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Stats")

    c1, c2, c3 = st.columns(3)
    c1.metric("Sensitivity", "91%")
    c2.metric("Specificity", "76%")
    c3.metric("F1 Score", "0.83")

    st.bar_chart([91, 76, 83])
    if st.button("Save Settings"):
        st.success("Settings saved!")
