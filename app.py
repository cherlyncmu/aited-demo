 import streamlit as st
... import numpy as np
... import matplotlib.pyplot as plt
... 
... st.set_page_config(page_title="AITED System", layout="wide")
... 
... # Sidebar
... st.sidebar.title("🧠 AITED")
... page = st.sidebar.radio("Menu", ["Scan", "Dashboard", "Model Performance"])
... 
... # ---------------- SCAN PAGE ----------------
... if page == "Scan":
...     st.title("🔍 Thyroid Scan Result")
... 
...     col1, col2 = st.columns([2,1])
... 
...     # Heatmap (Demo)
...     with col1:
...         st.subheader("EIT Heatmap")
...         data = np.random.rand(100,100)
... 
...         fig, ax = plt.subplots()
...         im = ax.imshow(data, cmap='jet')
...         ax.axis('off')
...         plt.colorbar(im, ax=ax)
...         st.pyplot(fig)
... 
...     # Info Panel
...     with col2:
...         st.subheader("AI Analysis")
...         st.metric("Risk Score", "82%")
...         st.error("Status: Suspicious")
... 
...         st.write("📍 Location: Right Lobe")
...         st.write("📏 Size: ~1.2 cm")
... 
...         st.warning("⚠️ Recommend further ultrasound examination")

# ---------------- DASHBOARD ----------------
elif page == "Dashboard":
    st.title("📊 Dashboard")

    st.subheader("Scan History")
    st.table({
        "Date": ["01/04/26", "15/04/26", "30/04/26"],
        "Risk": ["30%", "55%", "82%"],
        "Result": ["Normal", "Monitor", "Suspicious"]
    })

    st.subheader("Risk Trend")
    st.line_chart([30, 55, 82])

# ---------------- MODEL ----------------
elif page == "Model Performance":
    st.title("🧪 Model Performance")

    st.metric("Sensitivity", "91%")
    st.metric("Specificity", "76%")
    st.metric("F1-score", "0.83")

    st.subheader("Confusion Matrix")
    st.table({
        "": ["Actual Normal", "Actual Cancer"],
        "Pred Normal": ["80", "10"],
        "Pred Cancer": ["20", "90"]
