import streamlit as st
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("AIzaSyDTnwrXsdJL_0L_KhsWHVBMtBcpv8cUhYM")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


st.set_page_config(
    page_title = "AI Resume Analyzer",
    page_icon = "📄",
    layout = "wide"
)

st.title("🤖 CareerGPT")
st.caption("Your AI-Powered Resume & Interview Assistant")

st.write("Upload your resume and get AI-powered insight.")

# Resume Upload functionality

uploaded_file = st.file_uploader(
    "Upload your resume PDF",
    type=["pdf"]
)

# Job Description Input

job_description = st.text_area(
    "Enter Job Description Here",
    height=200
)

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")
    #st.write("File Name:", uploaded_file.name)

    # Extract text from the Resume PDF
    resume_text = " "

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"
    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )        
# Adding Tabs
    st.subheader("What would you like me to help you with?")
    tab1, tab2, tab3, tab4 = st.tabs([
        "ATS Analysis",
        "Interview Questions",
        "Resume Summary",
        "Job Description Match"
    ])    
    
    with tab2:
        if st.button("Generate Interview Questions"):
            with st.spinner("Generating interview questions..."):
                question_prompt = f"""
            Based on this  resume, generate 10 interview questions.
            
            Include:
            - Technical Questions
            - Project Based Questions
            - HR Questions
            
            Resume:
            {resume_text}
            """

            response = model.generate_content(question_prompt)
            st.subheader("Interview Questions")
            st.write(response.text)

    with tab3:
        if st.button("Generate Resume Summary"):
            with st.spinner("Generating resume summary..."):
                summary_prompt = f"""
            Create a professional recruiter-style summary of this candidate.
            
            Keep it:
            - Professional
            - Concise
            - 50-100 words
            
            Resume:
            {resume_text}
            """

            response = model.generate_content(summary_prompt)
            st.subheader("Resume Summary")

            st.text_area(
                "Summary",
                response.text,
                height=200
            )   

    with tab4:
        if st.button("Match Resume with Job Description"):
            if not job_description.strip():
                st.warning("Please Enter a job description first.")   

        else:
            with st.spinner("Matching Resume with Job Description..."):
                match_prompt = f"""
                Compare the following resume with job description.
                
                Return in this format:
                MATCH_SCORE: xx%

                MATCHING_SKILLS:
                - skill 1
                - skill 2

                MISSING_SKILLS:
                - skill 1
                - skill 2

                IMPROVEMENT_SUGGESTIONS:
                - suggestion 1
                - suggestion 2

                RESUME:
                {resume_text}

                JOB DESCRIPTION:
                {job_description}
                """          
                match_response = model.generate_content(match_prompt)
                st.subheader("Resume vs Job Description Match")

                st.text_area(
                    "Match Analysis",
                    match_response.text,
                    height=500
                )
    with tab1:
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing your resume..."):
                prompt = f"""
                Analyze this resume and provide:
                Return ONLY:

                Analyze this resume and return the result in exactly this format:

                ATS_SCORE: <score>%

                STRENGTHS:
                - point 1
                - point 2

                WEAKNESSES:
                - point 1
                - point 2

                MISSING_KEYWORDS:
                - keyword 1
                - keyword 2

                SUGGESTIONS:
                - suggestion 1
                - suggestion 2
            
                Resume:
                {resume_text}
                """

                response = model.generate_content(prompt)

                st.subheader("AI Analysis Result")

                st.write(response.text)
