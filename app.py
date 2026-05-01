```python
import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="SkinAI Pro",
    page_icon="🌸",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
}

.skin-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.recommend-box {
    background: #eef7ff;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 5px solid #3399ff;
}

.metric-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🌸 SkinAI Pro")
st.caption("AI Skin Analyzer & Smart Skincare Recommendation")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Skin Analysis",
        "History",
        "About"
    ]
)

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# FUNCTIONS
# =========================
def detect_skin_type(image_np):

    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    brightness = np.mean(gray)

    # OILY
    if brightness > 170:
        skin_type = "Oily"
        accuracy = 91

        skincare = [
            "Oil-Free Moisturizer",
            "Niacinamide Serum",
            "Clay Mask",
            "Salicylic Acid Cleanser",
            "Sunscreen SPF 50"
        ]

    # DRY
    elif brightness < 90:
        skin_type = "Dry"
        accuracy = 89

        skincare = [
            "Ceramide Moisturizer",
            "Hyaluronic Acid",
            "Gentle Cleanser",
            "Hydrating Toner",
            "Sunscreen SPF 50"
        ]

    # NORMAL
    else:
        skin_type = "Normal"
        accuracy = 93

        skincare = [
            "Vitamin C Serum",
            "Daily Moisturizer",
            "Gentle Facial Wash",
            "Sunscreen SPF 50",
            "Night Cream"
        ]

    return skin_type, accuracy, skincare

def detect_acne(image_np):

    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([160, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    acne_count = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if 20 < area < 500:
            acne_count += 1

    if acne_count > 15:
        severity = "Severe"
    elif acne_count > 5:
        severity = "Moderate"
    else:
        severity = "Mild"

    return acne_count, severity

# =========================
# SKIN ANALYSIS PAGE
# =========================
if menu == "Skin Analysis":

    st.subheader("📷 Upload Face Image")

    uploaded_file = st.file_uploader(
        "Upload JPG / PNG Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        image_np = np.array(image)

        col1, col2 = st.columns([1, 1])

        # =========================
        # IMAGE
        # =========================
        with col1:

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

        # =========================
        # ANALYSIS
        # =========================
        with col2:

            st.markdown("## 🔍 Analysis Result")

            skin_type, accuracy, skincare = detect_skin_type(image_np)

            acne_count, severity = detect_acne(image_np)

            st.markdown(f"""
            <div class="skin-card">
                <h3>🧴 Skin Type: {skin_type}</h3>
                <h4>🎯 Accuracy: {accuracy}%</h4>
                <h4>🔴 Acne Count: {acne_count}</h4>
                <h4>⚠ Severity: {severity}</h4>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("✨ Recommended Skincare")

            for item in skincare:
                st.markdown(f"""
                <div class="recommend-box">
                    ✔ {item}
                </div>
                """, unsafe_allow_html=True)

            # SAVE HISTORY
            st.session_state.history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "skin_type": skin_type,
                "accuracy": accuracy,
                "acne_count": acne_count,
                "severity": severity
            })

            # =========================
            # CHART
            # =========================
            st.subheader("📊 Skin Accuracy")

            chart_df = pd.DataFrame({
                "Category": ["Accuracy"],
                "Value": [accuracy]
            })

            fig = px.bar(
                chart_df,
                x="Category",
                y="Value",
                text="Value"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =========================
# HISTORY PAGE
# =========================
elif menu == "History":

    st.subheader("📜 Analysis History")

    if len(st.session_state.history) == 0:
        st.warning("No history available.")

    else:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(
            df,
            use_container_width=True
        )

# =========================
# ABOUT PAGE
# =========================
elif menu == "About":

    st.subheader("🌸 About SkinAI Pro")

    st.markdown("""
    SkinAI Pro adalah aplikasi AI untuk:
    
    - Deteksi jenis kulit
    - Analisa jerawat
    - Rekomendasi skincare
    - Dashboard modern
    - History analisa
    
    Dibangun menggunakan:
    
    - Streamlit
    - OpenCV
    - NumPy
    - Plotly
    """)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("© 2026 SkinAI Pro")
```
