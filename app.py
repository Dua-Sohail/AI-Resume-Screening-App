import streamlit as st
import pandas as pd
from utils import extract_text
from backend import calculate_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide",
    page_icon="💼"
)

# ---------------- THEME ----------------
st.markdown("""
<style>

/* Main Background */
# .stApp {
#     background: linear-gradient(180deg, #98FF98, #d9f7f1, #74c69d, #00674F);
# }
.stApp {
    background: linear-gradient(
        180deg, #c7f9e9, #f8fffb, #e6fff5,#a8e6cf    
    );
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #c7f9e9, #f8fffb, #e6fff5,#a8e6cf  );
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #2f3e46;
    font-weight: 600;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.08);
    border: 1px solid #dbe7e4;
    margin-bottom: 15px;
}

/* Screen CVs Button */
div.stButton > button {
    background: linear-gradient(90deg, #00674F,#52b788, #74c69d, #95d5b2);
    color: white;
    border-radius: 12px;
    padding: 12px 30px;
    border: none;
    font-weight: bold;
    font-size: 16px;
    width: 100%;
    margin-top: 15px;
    box-shadow: 0px 5px 15px rgba(82, 183, 136, 0.4);
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #40916c, #52b788, #74c69d);
    box-shadow: 0px 8px 20px rgba(64, 145, 108, 0.5);
}

/* Title */
.title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    background: linear-gradient(90deg, #2f3e46, #52796f, #84a98c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
}

/* Text */
h1, h2, h3, p {
    color: #2f3e46;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
<div class="title">
💼 AI Resume Screening System
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 💼 HR Dashboard")

menu = st.sidebar.selectbox(
    "Choose Section",
    ["📤 Upload CVs", "📊 Analytics Dashboard"]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
    background:white;
    padding:15px;
    border-radius:15px;
    color:black;
">
<h4>✨ Features</h4>
✔ Multi CV Upload<br>
✔ AI Scoring System<br>
✔ Shortlisting (>75%)<br>
✔ Graph Analytics<br>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PAGE 1 - UPLOAD CVs
# =====================================================
if menu == "📤 Upload CVs":

    st.markdown("## 📤 Upload & Screen Multiple CVs")

    job_desc = st.text_area("✍️ Enter Job Description")

    uploaded_files = st.file_uploader(
        "📄 Upload Multiple CVs",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("🔍 Screen CVs"):

        if not job_desc:
            st.warning("⚠️ Please enter a Job Description first.")

        elif not uploaded_files:
            st.warning("⚠️ Please upload at least one CV.")

        else:
            results = []

            st.markdown("### 📋 Screening Results")

        from database import insert_result

        for file in uploaded_files:

            resume_text = extract_text(file)
            score = calculate_score(resume_text, job_desc)

    # Show result
            if score > 75:
                st.success(f"🔥 SHORTLISTED: {file.name} → {score}%")
            elif score > 40:
                st.warning(f"⚡ CONSIDER: {file.name} → {score}%")
            else:
                st.error(f"❌ REJECTED: {file.name} → {score}%")

    # Save to database
            insert_result(file.name, score)
        st.success("✅ Screening Complete!")

# =====================================================
# PAGE 2 - ANALYTICS DASHBOARD
# =====================================================
elif   menu == "📊 Analytics Dashboard":

    st.markdown("## 📊 CV Analytics Dashboard")

   

    from database import fetch_results

    data = fetch_results()
    if data:
        df = pd.DataFrame(data, columns=["CV Name", "Score"])

        # ---------------- STATS ----------------
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="card">
        <h3>📄 Total CVs</h3>
        <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
        <h3>📊 Average Score</h3>
        <h2>{round(df['Score'].mean(), 2)}%</h2>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
        <h3>🔥 Top Score</h3>
        <h2>{df['Score'].max()}%</h2>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")

        # ---------------- GRAPH ----------------
        st.markdown("### 📈 Score Visualization")
        st.bar_chart(df.set_index("CV Name")["Score"])

        # ---------------- TABLE ----------------
        st.markdown("### 📋 All CV Records")
        st.dataframe(df, use_container_width=True)

        # ---------------- SHORTLIST ----------------
        st.markdown("### 🔥 Shortlisted CVs (above 75%)")
        shortlisted = df[df["Score"] > 75]

        if not shortlisted.empty:
            st.dataframe(shortlisted, use_container_width=True)
        else:
            st.info("No CV scored above 75% yet.")

        if st.button("Clear Records"):
            from database import clear_results
            clear_results()
            st.success("Records clear successfully")
        

    else:
        st.info("No data available yet. Please screen some CVs first.")

   