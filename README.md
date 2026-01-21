# 🗣️ **Voice-Enabled AI Assistant**

A lightweight, deployable **voice chatbot** built using **Streamlit**, **SpeechRecognition**, and **Google Text-to-Speech (gTTS)**.
The bot listens to your voice, converts speech to text, sends it to an LLM, and responds back in **natural voice**.

Deployable on **Render (FREE)** without requiring any local installations like Ollama or Whisper.

---

## ✨ **Features**

* 🎤 **Voice Input** — use your microphone directly in the browser
* 🧠 **LLM-powered Responses** — plug in any free/paid LLM API
* 🔊 **Voice Output** — bot replies with natural-sounding speech
* 🌐 **Fully Deployable** — works on Render, HuggingFace Spaces, etc.
* 🚫 **No Local Model Required** — no GPU, no Ollama, no Whisper
* ⚙️ **Simple, lightweight, free technologies**

---

## 🧩 **Tech Stack**

| Component      | Library/Service                            |
| -------------- | ------------------------------------------ |
| Frontend       | Streamlit                                  |
| Speech-to-Text | SpeechRecognition + Google Web Speech API  |
| Text-to-Speech | gTTS (Google Text-to-Speech)               |
| LLM            | Your preferred API (Gemma, HF, Groq, etc.) |
| Deployment     | Render (free tier)                         |

---

## 📁 **Project Structure**

```
voice-bot/
 ├── app.py
 ├── requirements.txt
 ├── README.md
```

---

## 🚀 **Run Locally**

### 1. Clone the repo

```bash
git clone https://github.com/kukretinaman/QABot.git
cd QABot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit

```bash
streamlit run app.py
```

Visit:

```
http://localhost:8501
```

---

## 🎧 **How It Works**

1. User speaks into microphone
2. Streamlit captures audio using `st.audio_input()`
3. SpeechRecognition converts speech → text
4. Text is sent to LLM
5. LLM generates a response
6. gTTS converts response text → speech
7. Streamlit plays the voice output

---

## 📦 **Requirements**

```
streamlit
SpeechRecognition
gTTS
pydub
ffmpeg-python
```

---

## 📌 TODO / Future Enhancements

* [ ] Add resume-based persona responses
* [ ] Add Whisper STT for offline audio transcription
* [ ] Replace gTTS with XTTS for human-like voice
* [ ] Add conversation memory
* [ ] Add UI themes & animations
* [ ] Real-time streaming voice

---

## 📝 License

MIT License — free to use, modify, and distribute.
