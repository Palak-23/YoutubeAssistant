# 🎥 YouTube Transcript Assistant

A GenAI-powered Streamlit web app that lets you **ask questions about any YouTube video**, see detailed AI-generated answers from its transcript, and even **generate quiz questions** for learning and assessment.

> 🧠 Built using **LangChain**, **OpenAI (GPT-3.5)**, **FAISS**, and **Streamlit**.

---

## ✨ Features

- 🔍 **Ask questions** about any YouTube video
- 🧾 **Transcript chunk retrieval** with vector similarity search
- 💬 **Context-aware chat memory** (multi-turn conversations)
- 📝 **Quiz Generator**: Generate MCQs & open-ended questions from video content
- 📺 **Video thumbnail preview** in UI
- 🧹 **Clear chat** & reset memory anytime

---

## 📷 Demo

![demo-thumbnail](https://img.youtube.com/vi/-Osca2Zax4Y/0.jpg)

> Try it out on [Streamlit Cloud](https://your-app-link.streamlit.app)

---

## 🧰 Tech Stack

| Tool           | Purpose                                |
|----------------|----------------------------------------|
| `LangChain`    | Document loading, LLM chaining         |
| `FAISS`        | Vector similarity search (transcript)  |
| `OpenAI GPT`   | Q&A + quiz generation via GPT-3.5      |
| `Streamlit`    | Frontend UI                            |
| `Python-dotenv`| API key management (locally)           |

---

## ⚙️ How It Works

1. Paste a YouTube video URL
2. Transcript is loaded and chunked
3. Chunks are embedded using OpenAI
4. A FAISS vector store is created from the chunks
5. User query is matched to top-k transcript chunks
6. LLM (GPT-3.5) answers the question using those chunks
7. Quiz generation uses top chunks to create 5-10 factual questions

---

## 🚀 Getting Started (Local)

```bash
git clone https://github.com/your-username/youtube-transcript-assistant.git
cd youtube-transcript-assistant
pip install -r requirements.txt
