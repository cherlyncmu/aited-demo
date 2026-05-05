import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

st.set_page_config(page_title="AITED Prototype", layout="wide")

# ---------------- STATE ----------------
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
        return 85, "⚠️ Suspicious", "High abnormal signal detected"
    elif score > 0.4:
        return 55, "🟡 Monitor", "Moderate variation detected"
    else:
        return 20, "🟢 Normal", "No abnormal pattern"

# ---------------- DEVICE ----------------
def connect():
    with st.spinner("Connecting device..."):
        time.sleep(1.5)
    st.session_state.connected = True

def disconnect():
    st.session_state.connected = False

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #020617;}
.card {background:#0f172a;padding:20px;border-radius:15px;margin-bottom:10px;}
.big {font-size:20px;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED PROTOTYPE")

if st.session_state.connected:
    st.sidebar.success("🟢 Connected")
    if st.sidebar.button("Disconnect"):
        disconnect()
else:
    st.sidebar.error("🔴 Disconnected")
    if st.sidebar.button("Connect Device"):
        connect()

page = st.sidebar.radio("Menu", ["Dashboard","Monitor","Scan","Records","Analytics"])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 System Overview")

    c1,c2,c3 = st.columns(3)
    c1.metric("Total Scans", len(st.session_state.history))
    c2.metric("High Risk", sum(1 for h in st.session_state.history if h["risk"]>70))
    c3.metric("Normal", sum(1 for h in st.session_state.history if h["risk"]<=70))

    if st.session_state.history:
        st.line_chart([h["risk"] for h in st.session_state.history])
    else:
        st.info("No data yet")

# ---------------- MONITOR ----------------
elif page == "Monitor":
    st.title("📡 Real-time Monitoring")

    if not st.session_state.connected:
        st.warning("Connect device first")
        st.stop()

    chart = st.empty()

    for _ in range(30):
        data = get_sensor_data()
        chart.line_chart(data)
        time.sleep(0.2)

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 AI Diagnostic Scan")

    if not st.session_state.connected:
        st.warning("Connect device first")
        st.stop()

    col1,col2 = st.columns([2,1])

    with col1:
        if st.button("▶ Start Scan"):
            st.session_state.scanning = True

        if st.session_state.scanning:
            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)

            st.success("Scan Complete")
            st.session_state.scanning = False

            data = get_sensor_data()
            risk,status,desc = analyze(data)

            # IMAGE SIMULATION
            x = np.linspace(-1,1,200)
            y = np.linspace(-1,1,200)
            X,Y = np.meshgrid(x,y)
            Z = np.exp(-(X**2+Y**2)*3)

            tx,ty = random.uniform(-0.5,0.5),random.uniform(-0.5,0.5)
            Z += np.exp(-((X-tx)**2+(Y-ty)**2)*25)

            fig,ax = plt.subplots()
            ax.imshow(Z,cmap='jet')
            circle = plt.Circle(((tx+1)*100,(ty+1)*100),20,color='red',fill=False)
            ax.add_patch(circle)
            ax.axis('off')
            st.pyplot(fig)

            result = {
                "risk":risk,
                "status":status,
                "desc":desc,
                "x":tx,
                "y":ty
            }

            st.session_state.result = result
            st.session_state.history.append(result)

    with col2:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        st.markdown('<div class="big">AI Diagnosis</div>',unsafe_allow_html=True)

        if st.session_state.result:
            r = st.session_state.result

            st.metric("Risk",f"{r['risk']}%")

            if "Suspicious" in r["status"]:
                st.error(r["status"])
            elif "Monitor" in r["status"]:
                st.warning(r["status"])
            else:
                st.success(r["status"])

            st.write("📍 Position")
            st.write(f"X={round(r['x'],2)} Y={round(r['y'],2)}")

            st.write("🧠 Insight")
            st.write(r["desc"])
        else:
            st.info("No scan yet")

        st.markdown('</div>',unsafe_allow_html=True)

    # REPORT
    if st.session_state.result:
        r = st.session_state.result

        st.subheader("📄 Medical Report")

        st.write("**Findings:**")
        st.write(r["desc"])

        st.write("**Assessment:**")
        st.write(r["status"])

        st.write("**Recommendation:**")
        if r["risk"]>70:
            st.write("Recommend immediate clinical evaluation")
        else:
            st.write("Routine monitoring suggested")

# ---------------- RECORDS ----------------
elif page == "Records":
    st.title("📋 Records")

    if st.session_state.history:
        st.dataframe(st.session_state.history)
    else:
        st.info("No records yet")

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Performance")

    st.metric("Sensitivity","91%")
    st.metric("Specificity","76%")

    st.bar_chart([91,76])
    st.bar_chart([91, 76])
