import streamlit as st
import plotly.graph_objects as go

from utils.extractor import extract_text_from_pdf
from utils.preprocessor import clean_text
from core.matcher import calculate_match_score
from core.rating import get_match_rating
from core.skill_extractor import analyze_skill_gap
from core.suggester import generate_suggestions
from core.ranker import rank_resumes


# ================= PAGE CONFIG ================= #
st.set_page_config(page_title="AI Resume Matcher", page_icon="🎯", layout="wide")


# ================= GAUGE CHART ================= #
def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Match Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green" if score >= 75 else "orange" if score >= 50 else "red"},
        }
    ))
    fig.update_layout(height=300)
    return fig


# ================= UI ================= #
st.title("🎯 AI Resume vs Job Matcher")
st.markdown("Compare resumes with a job description using AI (TF-IDF or BERT)")

# 🔥 MODEL SELECTION
model_choice = st.radio(
    "Select Matching Model:",
    ["TF-IDF (Fast)", "BERT (Accurate)"]
)

use_bert = model_choice == "BERT (Accurate)"

col1, col2 = st.columns(2)

with col1:
    uploaded_files = st.file_uploader(
        "Upload Resumes (Multiple PDFs)",
        type=["pdf"],
        accept_multiple_files=True
    )

with col2:
    jd_text = st.text_area("Paste Job Description", height=200)


# ================= BUTTON ================= #
if st.button("Analyze Match"):

    if not uploaded_files or not jd_text.strip():
        st.warning("Please upload resumes and enter job description")
    else:
        with st.spinner("Analyzing resumes... (BERT may take time)"):

            results = rank_resumes(uploaded_files, jd_text, use_bert)

            if not results:
                st.error("No valid resumes processed")
            else:
                st.divider()
                st.header("🏆 Resume Ranking")

                # 🥇 Top Candidate
                top = results[0]
                st.success(f"Top Candidate: {top['name']} ({top['score']}%)")

                # 📊 Ranking List
                for i, res in enumerate(results, start=1):
                    if i == 1:
                        st.success(f"🥇 {res['name']} → {res['score']}%")
                    elif i == 2:
                        st.info(f"🥈 {res['name']} → {res['score']}%")
                    elif i == 3:
                        st.warning(f"🥉 {res['name']} → {res['score']}%")
                    else:
                        st.write(f"{i}. {res['name']} → {res['score']}%")

                st.divider()
                st.header("📄 Detailed Analysis (Top Resume)")

                # ================= TOP RESUME ANALYSIS ================= #
                top_file = None
                for file in uploaded_files:
                    if file.name == top["name"]:
                        top_file = file
                        break

                if top_file:
                    raw_resume = extract_text_from_pdf(top_file)

                    if raw_resume:
                        clean_resume = clean_text(raw_resume)
                        clean_jd = clean_text(jd_text)

                        # Score
                        score = calculate_match_score(clean_resume, clean_jd, use_bert=use_bert)

                        # Rating
                        rating = get_match_rating(score)

                        # Skills
                        matched, missing, jd_skills = analyze_skill_gap(clean_resume, clean_jd)

                        # Suggestions
                        suggestions = generate_suggestions(score, missing)

                        colA, colB = st.columns([1, 2])

                        with colA:
                            st.plotly_chart(draw_gauge(score), use_container_width=True)
                            st.caption(f"Model Used: {'BERT 🤖' if use_bert else 'TF-IDF ⚡'}")

                        with colB:
                            st.subheader("🏆 Rating")

                            if score >= 80:
                                st.success(f"{rating}")
                            elif score >= 60:
                                st.info(f"{rating}")
                            elif score >= 40:
                                st.warning(f"{rating}")
                            else:
                                st.error(f"{rating}")

                            st.subheader("💡 Suggestions")
                            for s in suggestions:
                                st.info(s)

                        # ================= SKILLS ================= #
                        st.subheader("🛠 Skill Analysis")

                        tab1, tab2 = st.tabs(["Matched Skills", "Missing Skills"])

                        with tab1:
                            if matched:
                                st.success(", ".join(matched))
                            else:
                                st.write("No matched skills found")

                        with tab2:
                            if missing:
                                st.error(", ".join(missing))
                            else:
                                st.success("No missing skills 🎉")