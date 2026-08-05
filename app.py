import streamlit as st
from core.splitter import split_documents
from core.embeddings import get_embedding_model
from core.loader import load_pdf
from core.vector_store import create_vector_store
from core.retriever import get_retriever
from core.llm import get_llm
from core.chains import get_document_chain,get_retrieval_chain,build_rag_chain
from core.prompts import (
    get_chat_prompt,
    get_ats_prompt,
    get_jd_prompt,
    get_skill_gap_prompt,
    get_interview_prompt
)
import tempfile
st.set_page_config(
    page_title="AI Career Copilot",
    layout="wide"
)
st.title("AI Career Copilot")

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False 

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:

    st.header("Resume Upload")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

if uploaded_file and not st.session_state.resume_uploaded:
        st.success("Resume Uploaded Successfully")
    
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",

        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            file_path=temp_file.name

        documents=load_pdf(file_path)
        chunks = split_documents(documents)
        embedding_model=get_embedding_model()
        db=create_vector_store(
            chunks,
            embedding_model
        )
        st.session_state.retriever=get_retriever(db)
        st.session_state.llm=get_llm()
        st.session_state.resume_uploaded = True
        
if st.session_state.resume_uploaded:
    st.subheader("Resume Chat")
    
    
    question = st.text_input(
        "Ask a question about your resume"
    )
    if question:
        chat_chain = build_rag_chain(
                st.session_state.llm,
                st.session_state.retriever,
                get_chat_prompt()
            )

        with st.spinner("Analyzing your resume..."):
            response=chat_chain.invoke(
                {
                    "input":question
                }
            )
            st.success("Analysis Completed")
            # st.write(response["answer"])
            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": response["answer"]
                }
            )
    if st.session_state.chat_history:

        st.subheader("Chat History")

        for chat in st.session_state.chat_history:

            st.write("You:")
            st.write(chat["question"])

            st.write("AI:")
            st.write(chat["answer"])

            st.divider()

    if st.button("Generate ATS Report"):

            ats_chain = build_rag_chain(
                st.session_state.llm,
                st.session_state.retriever,
                get_ats_prompt()
            )

            ats_task = """
            Analyze this resume as an Applicant Tracking System.

            Generate:

            1. ATS Score (/100)

            2. Strengths

            3. Weaknesses

            4. Missing Keywords

            5. Suggestions for Improvement
            """

            with st.spinner("Generating ATS Report..."):

                response = ats_chain.invoke(
                    {
                        "input": ats_task
                    }
                )

            st.success("ATS Report Generated!")

            st.write(response["answer"])
   

    st.subheader("JD Matching")
    job_description = st.text_area(
        "Paste Job Description"
    )   
    


    if st.button("Match Resume with JD"):

        if not job_description.strip():

            st.warning("Please paste a Job Description.")
        else:

            jd_chain = build_rag_chain(
                st.session_state.llm,
                st.session_state.retriever,
                get_jd_prompt()
            )

            with st.spinner("Matching Resume..."):

                response = jd_chain.invoke(
                    {
                        "input": job_description
                    }
                )

            st.success("JD Matching Completed!")

            st.write(response["answer"])
      

    st.subheader("Skill Gap Analysis")

    if st.button("Analyze Skill Gap"):

        if not job_description.strip():

            st.warning("Please paste a Job Description.")

        else:

            skill_gap_chain = build_rag_chain(
                st.session_state.llm,
                st.session_state.retriever,
                get_skill_gap_prompt()
            )

            with st.spinner("Analyzing Skill Gap..."):

                response = skill_gap_chain.invoke(
                    {
                        "input": job_description
                    }
                )

            st.success("Skill Gap Analysis Completed!")

            st.write(response["answer"])
            
    st.subheader("Interview Question Generator")

    if st.button("Generate Interview Questions"):

        interview_chain = build_rag_chain(
            st.session_state.llm,
            st.session_state.retriever,
            get_interview_prompt()
        )

        interview_task = """
        Generate interview questions based on this resume.

        Include:

        1. Technical Questions (5)

        2. Project-Based Questions (5)

        3. HR Questions (5)

        4. Follow-up Questions (5)
        """

        with st.spinner("Generating Interview Questions..."):

            response = interview_chain.invoke(
                {
                    "input": interview_task
                }
            )

        st.success("Interview Questions Generated!")

        st.write(response["answer"])