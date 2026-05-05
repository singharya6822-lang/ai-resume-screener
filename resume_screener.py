import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
import re

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI Resume Screener")
st.markdown("Paste your resume and job description to get an instant match score!")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Your Resume")
    resume = st.text_area("Paste resume here", height=300)
with col2:
    st.subheader("💼 Job Description")
    jd = st.text_area("Paste job description here", height=300)

SKILLS = ["python","sql","machine learning","tableau","power bi","pandas",
          "numpy","scikit-learn","git","statistics","communication",
          "deep learning","nlp","aws","excel","r programming","spark"]

if st.button("🔍 Analyze Match", type="primary"):
    if resume and jd:
        vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
        tfidf = vec.fit_transform([resume.lower(), jd.lower()])
        score = round(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100, 1)

        res_skills = [s for s in SKILLS if s in resume.lower()]
        jd_skills  = [s for s in SKILLS if s in jd.lower()]
        matched    = list(set(res_skills) & set(jd_skills))
        missing    = list(set(jd_skills) - set(res_skills))
        skill_pct  = round(len(matched)/max(len(jd_skills),1)*100, 1)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Overall Match", f"{score}%")
        c2.metric("Skill Match",   f"{skill_pct}%")
        c3.metric("Skills Missing", len(missing))

        color = "#22c55e" if score>=75 else "#f59e0b" if score>=50 else "#ef4444"
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Match Score %"},
            gauge={'axis':{'range':[0,100]},
                   'bar':{'color':color},
                   'steps':[
                       {'range':[0,40],'color':'#fee2e2'},
                       {'range':[40,75],'color':'#fef9c3'},
                       {'range':[75,100],'color':'#dcfce7'}]}))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("✅ Matched Skills")
            for s in matched:
                st.success(s.title())
        with col4:
            st.subheader("❌ Missing Skills")
            for s in missing:
                st.error(s.title())

        st.subheader("💡 Suggestions")
        if missing:
            st.warning(f"Add these skills to your resume: **{', '.join(missing)}**")
        if score < 50:
            st.info("Use exact keywords from the job description in your resume!")
        if score >= 75:
            st.success("🎉 Excellent match! Your resume is well aligned!")
    else:
        st.error("Please paste both resume and job description!")

st.markdown("---")
st.caption("AI Resume Screener | Built with Python & Streamlit 🚀")