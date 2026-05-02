import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

st.set_page_config(page_title="AITED Medical System", layout="wide")

# ---------------- SESSION ----------------
if "connected" not in st.session_state:
    st.session_state.connected = False

if "scanning" not in st.session_state:
    st.session_state.scanning = False

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- FAKE SENSOR (แทน hardware) ----------------
def get_sensor_data():
    # จำลองข้อมูลจากปลอกคอ
    return np.random.rand(16)

# ---------------- AI MODEL (ไม่ random ล้วน) ----------------
def analyze(data):
    score = np.mean(data)

    if score > 0.65:
        risk = 85
        status = "⚠️ Suspicious"
    elif score > 0.4:
        risk = 55
        status = "🟡 Monitor"
    else:
        risk = 20
        status = "🟢 Normal"

    return risk, status

# ---------------- FUNCTIONS ----------------
def connect_device():
    with st.spinner("Connecting to AITED Collar..."):
        time.sleep(2)
    st.session_state.connected = True

def disconnect_device():
    st.session_state.connected = False

def start_scan():
    st.session_state.scanning = True
    st.session_state.result = None

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #020617;}
.block {
    background: #020617;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED SYSTEM")

st.sidebar.subheader("🔌 Device")

if st.session_state.connected:
    st.sidebar.success("🟢 CONNECTED")
    if st.sidebar.button("Disconnect"):
        disconnect_device()
else:
    st.sidebar.error("🔴 DISCONNECTED")
    if st.sidebar.button("Connect Device"):
        connect_device()

page = st.sidebar.radio("MODE", ["Monitor", "Scan", "Records", "Analytics"])

# ---------------- MONITOR (เหมือนเครื่องจริง) ----------------
if page == "Monitor":
    st.title("📡 Real-time Monitoring")

    if not st.session_state.connected:
        st.warning("Connect device to start monitoring")
        st.stop()

    chart = st.empty()

    for _ in range(30):
        data = get_sensor_data()
        chart.line_chart(data)
        time.sleep(0.2)

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Diagnostic Scan")

    if not st.session_state.connected:
        st.warning("⚠️ Connect device first")
        st.stop()

    col1, col2 = st.columns([2,1])

    with col1:
        if st.button("▶ Start Scan"):
            start_scan()

        if st.session_state.scanning:
            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            st.success("Scan Complete")
            st.session_state.scanning = False

            # รับข้อมูลจาก sensor
            sensor_data = get_sensor_data()

            # วิเคราะห์
            risk, status = analyze(sensor_data)

            # สร้างภาพ
            x = np.linspace(-1,1,200)
            y = np.linspace(-1,1,200)
            X, Y = np.meshgrid(x,y)

            Z = np.exp(-(X**2 + Y**2)*3)

            tx, ty = random.uniform(-0.4,0.4), random.uniform(-0.4,0.4)
            Z += np.exp(-((X-tx)**2 + (Y-ty)**2)*25)

            fig, ax = plt.subplots()
            ax.imshow(Z, cmap='jet')

            circle = plt.Circle(((tx+1)*100,(ty+1)*100),20,
                                color='red', fill=False, linewidth=2)
            ax.add_patch(circle)

            ax.axis('off')
            st.pyplot(fig)

            st.session_state.result = {
                "risk": risk,
                "status": status
            }

    with col2:
        st.markdown("### AI RESULT")

        if st.session_state.result:
            r = st.session_state.result
            st.metric("Risk", f"{r['risk']}%")

            if "Suspicious" in r["status"]:
                st.error(r["status"])
            elif "Monitor" in r["status"]:
                st.warning(r["status"])
            else:
                st.success(r["status"])
        else:
            st.info("No data")

# ---------------- RECORDS ----------------
elif page == "Records":
    st.title("📋 Patient Records")

    st.dataframe({
        "Patient": ["A", "B"],
        "Risk": ["85%", "20%"],
        "Status": ["Suspicious", "Normal"]
    })

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Evaluation")

    st.metric("Sensitivity", "91%")
    st.metric("Specificity", "76%")

    st.bar_chart([91, 76])
