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
    with st.spinner("Connecting..."):
        time.sleep(2)
    st.session_state.connected = True

@@ -54,201 +33,130 @@
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #020617;}
.block {
    background: #020617;
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 10px;
    border-radius: 15px;
    border: 1px solid #1e293b;
}
.big {font-size: 22px; font-weight: bold;}
.scanbox {
    border: 2px solid #22c55e;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED SYSTEM")
st.sidebar.title("🧠 AITED")

st.sidebar.subheader("🔌 Device")

if st.session_state.connected:
    st.sidebar.success("🟢 CONNECTED")
    st.sidebar.success("🟢 Connected")
    if st.sidebar.button("Disconnect"):
        disconnect_device()
else:
    st.sidebar.error("🔴 DISCONNECTED")
    st.sidebar.error("🔴 Disconnected")
    if st.sidebar.button("Connect Device"):
        connect_device()

page = st.sidebar.radio("MODE", ["Monitor", "Scan", "Records", "Analytics"])

# ---------------- MONITOR (เหมือนเครื่องจริง) ----------------
if page == "Monitor":
    st.title("📡 Real-time Monitoring")
page = st.sidebar.radio("Navigation", [
    "Dashboard", "Scan", "Patients", "Analytics"
])

    if not st.session_state.connected:
        st.warning("Connect device to start monitoring")
        st.stop()
# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 System Overview")

    chart = st.empty()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", "128")
    c2.metric("High Risk", "32")
    c3.metric("Normal", "76")

    for _ in range(30):
        data = get_sensor_data()
        chart.line_chart(data)
        time.sleep(0.2)
    st.line_chart([30, 45, 60, 55, 82])

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Diagnostic Scan")
    st.title("🔍 Live Scan")

    if not st.session_state.connected:
        st.warning("⚠️ Connect device first")
        st.stop()

    col1, col2 = st.columns([2,1])

    # -------- LEFT: SCAN --------
    with col1:
        if st.button("▶ Start Scan"):
            start_scan()
        st.markdown('<div class="scanbox">', unsafe_allow_html=True)

        if not st.session_state.scanning:
            if st.button("▶ Start Scan"):
                start_scan()

        if st.session_state.scanning:
            progress = st.progress(0)
            status = st.empty()

            for i in range(100):
                time.sleep(0.01)
                time.sleep(0.015)
                progress.progress(i + 1)
                status.text(f"Scanning... {i+1}%")

            st.success("Scan Complete")
            st.session_state.scanning = False

            # รับข้อมูลจาก sensor
            sensor_data = get_sensor_data()

            # วิเคราะห์
            risk, status = analyze(sensor_data)

            # สร้างภาพ
            # -------- CREATE DATA --------
            x = np.linspace(-1,1,200)
            y = np.linspace(-1,1,200)
            X, Y = np.meshgrid(x,y)

            Z = np.exp(-(X**2 + Y**2)*3)

            tx, ty = random.uniform(-0.4,0.4), random.uniform(-0.4,0.4)
            # random tumor
            tx, ty = random.uniform(-0.5,0.5), random.uniform(-0.5,0.5)
            Z += np.exp(-((X-tx)**2 + (Y-ty)**2)*25)

            # -------- PLOT --------
            fig, ax = plt.subplots()
            ax.imshow(Z, cmap='jet')

            circle = plt.Circle(((tx+1)*100,(ty+1)*100),20,
                                color='red', fill=False, linewidth=2)
            # 🔴 highlight tumor
            circle = plt.Circle(
                ((tx+1)*100, (ty+1)*100),
                20,
                color='red',
                fill=False,
                linewidth=2
            )
            ax.add_patch(circle)

            ax.set_title("EIT Imaging")
            ax.axis('off')
            st.pyplot(fig)

            st.session_state.result = {
                "risk": risk,
                "status": status
            }

    with col2:
        st.markdown("### AI RESULT")
            st.pyplot(fig)

        if st.session_state.result:
            r = st.session_state.result
            st.metric("Risk", f"{r['risk']}%")
            # -------- AI RESULT --------
            risk = random.randint(40, 95)

            if "Suspicious" in r["status"]:
                st.error(r["status"])
            elif "Monitor" in r["status"]:
                st.warning(r["status"])
            if risk > 70:
                status_text = "⚠️ Suspicious"
            elif risk > 40:
                status_text = "🟡 Monitor"
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

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED SYSTEM")
page = st.sidebar.radio("Menu", [
    "Dashboard",
    "Scan",
    "Patients",
    "Analytics"
])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 System Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", "128", "+12")
    c2.metric("High Risk", "32", "+5")
    c3.metric("Normal", "76", "-3")

    st.subheader("📈 Risk Trend")
    st.line_chart([30, 45, 60, 55, 82])

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Ultrasound AI Scan")

    col1, col2 = st.columns([2, 1])

    # LEFT SIDE
    with col1:
        if st.button("▶ Start Scan"):
            st.session_state.scanning = True
            st.session_state.result = None

        if st.session_state.scanning:
            progress = st.progress(0)
            status = st.empty()

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
                status.text(f"Scanning... {i+1}%")

            st.success("Scan Complete")
            st.session_state.scanning = False

            img = load_image()
            x, y, r, risk, location = detect(img)

            fig, ax = plt.subplots()
            ax.imshow(img, cmap='gray')

            circle = plt.Circle((y, x), r, color='red', fill=False, linewidth=2)
            ax.add_patch(circle)

            ax.axis('off')
            st.pyplot(fig)
                status_text = "🟢 Normal"

            st.session_state.result = {
                "risk": risk,
                "location": location,
                "x": x,
                "y": y
                "status": status_text,
                "x": tx,
                "y": ty
            }

    # RIGHT SIDE
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- RIGHT: RESULT --------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="big">AI Diagnosis</div>', unsafe_allow_html=True)
@@ -257,34 +165,38 @@
            r = st.session_state.result

            st.metric("Risk Score", f"{r['risk']}%")
            st.error("⚠️ Suspicious")

            st.write("📍 Location")
            st.write(r["location"])
            if "Suspicious" in r["status"]:
                st.error(r["status"])
            elif "Monitor" in r["status"]:
                st.warning(r["status"])
            else:
                st.success(r["status"])

            st.write("📍 Detected Region")
            st.write(f"📌 X: {round(r['x'],2)}  Y: {round(r['y'],2)}")

            st.write("📌 Coordinates")
            st.write(f"X={r['x']}  Y={r['y']}")
            st.write("📏 Estimated size: ~1 cm")

            st.write("📏 Size ~1 cm")
        else:
            st.info("No scan yet")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PATIENTS ----------------
elif page == "Patients":
    st.title("👤 Patient Records")
    st.title("👤 Patients")

    st.dataframe({
        "Name": ["John Doe", "Jane Smith"],
        "Last Scan": ["30 Apr", "15 Apr"],
        "Risk": ["82%", "30%"],
        "Status": ["High Risk", "Normal"]
        "Status": ["High", "Normal"]
    })

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Performance")
    st.title("🧪 Model Stats")

    c1, c2, c3 = st.columns(3)
    c1.metric("Sensitivity", "91%")
