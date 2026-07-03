# 🎥 AI Video Assistant

An AI-powered meeting and video analysis assistant that automatically transcribes videos, generates concise summaries, extracts action items, key decisions, and questions, and allows users to ask contextual questions using Retrieval-Augmented Generation (RAG).

## ✨ Features

- 🎙️ Automatic speech-to-text transcription
- 📝 AI-generated meeting summaries
- 📌 Extracts action items
- 🤝 Identifies key decisions
- ❓ Extracts important questions
- 💬 Chat with your video using RAG
- 📺 Supports YouTube videos and local audio/video files
- 🌐 Interactive Streamlit web interface

---

## 🛠️ Tech Stack

### Languages
- Python

### AI & LLMs
- Whisper
- Mistral AI
- LangChain

### Vector Database
- ChromaDB

### Frontend
- Streamlit

### Audio Processing
- FFmpeg
- Pydub
- yt-dlp

---

## 📂 Project Structure

```
AI-video-assistant/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarise.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utilities/
│   └── audioprocessor.py
│
├── app.py
├── main.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/officialadithya2005-maker/AI-video-assistant.git
cd AI-video-assistant
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
MISTRAL_API_KEY=your_api_key
SARVAM_API_KEY=your_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 💡 Workflow

1. Upload a local video/audio file or provide a YouTube link.
2. Extract audio from the video.
3. Generate speech transcription.
4. Produce an AI-generated summary.
5. Extract:
   - Action Items
   - Key Decisions
   - Questions
6. Build a vector database using embeddings.
7. Ask questions about the video using RAG.

---

## 📸 Screenshots

Add screenshots of:

- Home Page
- Summary Output
- Action Items
- Chat with Video

---

## 🔮 Future Improvements

- Multi-language support
- Speaker diarization
- PDF and DOCX report generation
- Cloud deployment
- Meeting analytics dashboard
- Support for additional LLM providers

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
