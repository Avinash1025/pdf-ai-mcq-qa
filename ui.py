import streamlit as st
from utils import extract_text_from_pdf, count_tokens, generate_mcqs_from_text, create_vector_store, ask_and_get_answer

def run_ui():
    st.set_page_config(
        page_title="📘 MCQ & QA Generator",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="auto"
    )

    st.markdown("""
        <style>
        .main { background-color: #f9fbfc; }
        .stButton>button {
            background-color: #4CAF50; color: white;
            font-weight: bold; border-radius: 10px;
            padding: 10px 20px; transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #45a049; transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📘 AI-Powered MCQ & QA System")

    with st.sidebar:
        st.image("https://img.icons8.com/clouds/100/pdf.png", width=100)
        st.header("📤 Upload PDF")
        file = st.file_uploader("Choose a PDF", type="pdf")
        st.markdown("---")
        st.header("⚙️ Action")
        action = st.radio("What do you want to do?", ["MCQ Generator", "Question Answering"])

    if file:
        text = extract_text_from_pdf(file)
        if not text:
            st.error("❌ Could not extract text from the PDF.")
            return

        st.success("✅ Text loaded successfully!")
        st.write(f"📏 Approx. Tokens: {count_tokens(text)}")

        if action == "MCQ Generator":
            st.subheader("📝 Generate MCQs")
            num_questions = st.slider("Select number of questions", 1, 10, 3)
            if st.button("🎯 Generate MCQs"):
                with st.spinner("Working on it..."):
                    mcqs = generate_mcqs_from_text(text, num_questions)
                    if mcqs:
                        st.success("🎉 MCQs generated!")
                        st.text_area("📄 Your MCQs", mcqs, height=300)
                    else:
                        st.error("⚠️ Couldn't generate questions.")

        elif action == "Question Answering":
            st.subheader("🤖 Ask Questions About the PDF")
            vector_store = create_vector_store(text)
            question = st.text_input("🔍 Ask your question here")
            if question and st.button("💬 Get Answer"):
                with st.spinner("Thinking..."):
                    answer = ask_and_get_answer(vector_store, question)
                    st.success("✅ Answer:")
                    st.markdown(f"**{answer}**")
    else:
        st.info("👈 Upload a PDF from the sidebar to begin.")
