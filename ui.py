import streamlit as st
from utils import extract_text_from_pdf, count_tokens, generate_mcqs_from_text, create_vector_store, ask_and_get_answer

def run_ui():
    st.set_page_config(
        page_title="MCQ & QA Generator",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("MCQ & QA System")
    st.sidebar.header("Upload PDF")
    file = st.sidebar.file_uploader("Choose a PDF document", type="pdf")

    if file:
        text = extract_text_from_pdf(file)
        if not text:
            st.error("Could not extract text from the PDF.")
            return

        st.success("Text loaded successfully!")
        st.write(f"Number of tokens in text: {count_tokens(text)}")

        # Action selection
        st.subheader("Select Action")
        action = st.radio("Choose what to do", ["Generate MCQs", "Ask Questions"])

        if action == "Generate MCQs":
            num_questions = st.slider("Number of MCQs", 1, 10, 3)
            if st.button("Generate MCQs"):
                with st.spinner("Generating MCQs..."):
                    mcqs = generate_mcqs_from_text(text, num_questions)
                    if mcqs:
                        st.text_area("Generated MCQs", mcqs, height=300)
                    else:
                        st.error("Failed to generate MCQs.")
        else:
            # Question Answering
            vector_store = create_vector_store(text)
            question = st.text_input("Enter your question")
            if question and st.button("Get Answer"):
                with st.spinner("Finding answer..."):
                    answer = ask_and_get_answer(vector_store, question)
                    st.markdown(f"**Answer:** {answer}")
    else:
        st.info("Please upload a PDF file from the sidebar to begin.")
