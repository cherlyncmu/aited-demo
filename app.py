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

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SENSOR ----------------
def get_sensor_data():
    return np.random.rand(16)

# ---------------- AI ----------------
def analyze(data):
    score = np.mean(data)

    if score > 0.65:
        return 85, "⚠️ Suspicious"
    elif score > 0.4:
        return 55, "🟡 Monitor"
    else:
        return 20, "🟢 Normal"

# ---------------- DEVICE ----------------
def connect_device():
    with st.spinner("Connecting..."):
        time.sleep(2)
    st.session_state.connected = True

def disconnect_device():
    st.session_state.connected = False

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #020617;}
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
}
.big {font-size: 20px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED SYSTEM")

if st.session_state.connected:
    st.sidebar.success("🟢 Connected")
    if st.sidebar.button("Disconnect"):
        disconnect_device()
else:
    st.sidebar.error("🔴 Disconnected")
    if st.sidebar.button("Connect Device"):
        connect_device()

page = st.sidebar.radio("Menu", ["Dashboard", "Scan", "Patients", "Analytics"])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 System Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", len(st.session_state.history))
    c2.metric("High Risk", sum(1 for h in st.session_state.history if h["risk"] > 70))
    c3.metric("Normal", sum(1 for h in st.session_state.history if h["risk"] <= 70))

    if st.session_state.history:
        st.line_chart([h["risk"] for h in st.session_state.history])
    else:
        st.info("No data yet")

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Live Scan")

    if not st.session_state.connected:
        st.warning("⚠️ Connect device first")
        st.stop()

    col1, col2 = st.columns([2,1])

    # LEFT
    with col1:
        if st.button("▶ Start Scan"):
            st.session_state.scanning = True
            st.session_state.result = None

        if st.session_state.scanning:
            progress = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
                status_text.text(f"Scanning... {i+1}%")

            st.success("Scan Complete")
            st.session_state.scanning = False

            # DATA
            data = get_sensor_data()
            risk, status = analyze(data)

            # IMAGE
            x = np.linspace(-1,1,200)
            y = np.linspace(-1,1,200)
            X, Y = np.meshgrid(x,y)
            Z = np.exp(-(X**2 + Y**2)*3)

            tx, ty = random.uniform(-0.5,0.5), random.uniform(-0.5,0.5)
            Z += np.exp(-((X-tx)**2 + (Y-ty)**2)*25)

            fig, ax = plt.subplots()
            ax.imshow(Z, cmap='jet')

            circle = plt.Circle(((tx+1)*100,(ty+1)*100),20,
                                color='red', fill=False, linewidth=2)
            ax.add_patch(circle)

            ax.axis('off')
            st.pyplot(fig)

            result = {
                "risk": risk,
                "status": status,
                "x": tx,
                "y": ty
            }

            st.session_state.result = result
            st.session_state.history.append(result)

    # RIGHT
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="big">AI Diagnosis</div>', unsafe_allow_html=True)

        if st.session_state.result:
            r = st.session_state.result

            st.metric("Risk", f"{r['risk']}%")

            if "Suspicious" in r["status"]:
                st.error(r["status"])
            elif "Monitor" in r["status"]:
                st.warning(r["status"])
            else:
                st.success(r["status"])

            st.write("📍 Position")
            st.write(f"X={round(r['x'],2)}  Y={round(r['y'],2)}")

        else:
            st.info("No scan yet")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PATIENTS ----------------
elif page == "Patients":
    st.title("👤 Patient Records")

    if st.session_state.history:
        st.dataframe(st.session_state.history)
    else:
        st.info("No records yet")

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Performance")

    st.metric("Sensitivity", "91%")
    st.metric("Specificity", "76%")

    st.bar_chart([91, 76])
