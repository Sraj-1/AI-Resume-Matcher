import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.extractor import extract_text_from_pdf
from core.matcher import calculate_hybrid_score
from core.rating import get_match_rating
from core.skill_extractor import analyze_skill_gap
from core.suggester import generate_suggestions
from core.ranker import rank_resumes


# ================= PAGE CONFIG ================= #
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🎯",
    layout="wide"
)

# ================= SIDEBAR ================= #
with st.sidebar:
    st.title("⚙️ Settings")

    st.markdown("### 🤖 Model Info")
    st.info("Hybrid Model: TF-IDF + BERT + Skill Matching")

    st.markdown("---")
    st.markdown("### 📌 Tips")
    st.info("Best results come from detailed resumes and job descriptions.")


# ================= GAUGE ================= #
def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Final Match Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {
                'color': "green" if score >= 75 else "orange" if score >= 50 else "red"
            },
        }
    ))
    fig.update_layout(height=250)
    return fig


# ================= HEADER ================= #
st.title("🎯 AI Resume Screening Dashboard")
st.caption("AI-powered Resume vs Job Description Matcher with Explainability")

st.divider()

# ================= INPUT ================= #
col1, col2 = st.columns(2)

with col1:
    uploaded_files = st.file_uploader(
        "📄 Upload Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

with col2:
    jd_text = st.text_area("📝 Paste Job Description", height=200)


# ================= ANALYZE ================= #
if st.button("🚀 Analyze Resumes"):

    if not uploaded_files or not jd_text.strip():
        st.warning("⚠️ Please upload resumes and enter job description")
        st.stop()

    with st.spinner("🔍 Analyzing resumes..."):

        results = rank_resumes(uploaded_files, jd_text)

    if not results:
        st.error("❌ No valid resumes processed")
        st.stop()

    # ================= RANKING ================= #
    st.divider()
    st.header("🏆 Resume Ranking")

    df = pd.DataFrame(results)

    # 🥇 Top Candidate
    top = results[0]
    st.success(f"Top Candidate: **{top['name']}** ({top['score']}%)")

    # 📊 Table
    st.dataframe(df, use_container_width=True)

    # 📥 Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")

    # ================= TOP ANALYSIS ================= #
    st.divider()
    st.header("📄 Detailed Analysis (Top Resume)")

    top_file = next((f for f in uploaded_files if f.name == top["name"]), None)

    if top_file:
        raw_resume = extract_text_from_pdf(top_file)

        if raw_resume:

            # 🔥 HYBRID MATCHING
            result = calculate_hybrid_score(raw_resume, jd_text)

            score = result["final_score"]
            tfidf_score = result["tfidf"]
            bert_score = result["bert"]
            skill_score = result["skill"]
            keywords = result["keywords"]

            # 🔹 Rating
            rating = get_match_rating(score)

            # 🔹 Skill Gap
            matched, missing, jd_skills = analyze_skill_gap(raw_resume, jd_text)

            # 🔹 Suggestions
            suggestions = generate_suggestions(score, missing)

            colA, colB = st.columns([1, 2])

            # ================= GAUGE ================= #
            with colA:
                st.plotly_chart(draw_gauge(score), use_container_width=True)
                st.caption("Hybrid Model 🤖")

            # ================= TEXT ================= #
            with colB:
                st.subheader("🏆 Rating")

                if score >= 80:
                    st.success(rating)
                elif score >= 60:
                    st.info(rating)
                elif score >= 40:
                    st.warning(rating)
                else:
                    st.error(rating)

                st.subheader("💡 Suggestions")
                for s in suggestions:
                    st.write(f"• {s}")

            # ================= SCORE BREAKDOWN ================= #
            st.subheader("📊 Score Breakdown")

            c1, c2, c3 = st.columns(3)
            c1.metric("TF-IDF", f"{tfidf_score}%")
            c2.metric("BERT", f"{bert_score}%")
            c3.metric("Skill Match", f"{skill_score}%")

            # ================= KEYWORDS ================= #
            if keywords:
                st.subheader("🔍 Top Matching Keywords")
                st.success(", ".join(keywords))

            # ================= SKILLS ================= #
            st.subheader("🛠 Skill Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Matched Skills")
                if matched:
                    st.success(", ".join(matched))
                else:
                    st.write("No matched skills")

            with col2:
                st.markdown("### ❌ Missing Skills")
                if missing:
                    st.error(", ".join(missing))
                else:
                    st.success("No missing skills 🎉")

            # ================= SKILL CHART ================= #
            st.subheader("📊 Skill Distribution")

            skill_data = {
                "Matched": len(matched),
                "Missing": len(missing)
            }

            st.bar_chart(skill_data)