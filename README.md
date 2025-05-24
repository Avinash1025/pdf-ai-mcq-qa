# 🧠📄 AI-Powered MCQ Generator & PDF Question Answering System

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-ff4b4b) ![LangChain](https://img.shields.io/badge/Backend-LangChain-003366) ![License](https://img.shields.io/badge/License-MIT-green) ![Ollama](https://img.shields.io/badge/LLM-Ollama-blueviolet)

Welcome to the future of interactive studying! This app lets you **upload any PDF**, and instantly:

- 🚀 **Generate multiple-choice questions (MCQs)** based on the content — perfect for self-testing and exam prep.
- ❓ **Ask natural language questions** about the PDF and get detailed answers backed by your document.

Powered by **Streamlit** for a slick web UI, **LangChain** for smart document processing, and **Ollama** running a local LLaMA language model, this tool brings cutting-edge AI directly to your desktop — with **zero internet required**, ensuring privacy and speed.

---

## 🎯 What does this app do?

- Extracts text from PDFs with precision using `pdfplumber`.
- Splits large texts into manageable chunks for smart question generation and answering.
- Generates **high-quality MCQs** with 4 options each, including correct and distractors.
- Uses **embedding-based retrieval** to answer your queries based on the PDF content.
- Offers a dynamic, colorful, and user-friendly interface for smooth interaction.

---

## 🛠️ How to Set Up and Run

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/mcq_qa_app.git
cd mcq_qa_app
