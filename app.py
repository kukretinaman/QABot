from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from gtts import gTTS
from pydub import AudioSegment
import streamlit as st
import speech_recognition as sr
import tempfile
import requests
import os
import PyPDF2
import numpy as np

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------------------
# Groq LLM Call
# ----------------------------
def call_groq_llm(prompt):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


# ----------------------------
# PDF Reader
# ----------------------------
def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text


# ----------------------------
# Chunk Text
# ----------------------------
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    return chunks


# ----------------------------
# Embeddings
# ----------------------------
@st.cache_resource
def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed(chunks):
    model = get_embedder()
    embeddings = model.encode(chunks)
    return np.array(embeddings)


# ----------------------------
# Similarity Search
# ----------------------------
def search(query, chunks, chunk_emb):
    model = get_embedder()
    q_emb = model.encode([query])[0]

    scores = np.dot(chunk_emb, q_emb)

    top_k = scores.argsort()[-3:][::-1]
    return [chunks[i] for i in top_k]


# -----------------------------------------
# Streamlit App
# -----------------------------------------
st.title("🎙️ Voice-Enabled AI Assistant")

st.write("Upload a resume and ask questions. No local models needed.")

resume_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])

if resume_file:
    if resume_file.type == "application/pdf":
        text = read_pdf(resume_file)
    else:
        text = resume_file.read().decode("utf-8")

    st.write("Resume Loaded. Building embeddings...")

    chunks = chunk_text(text)
    chunk_embs = embed(chunks)

    st.success(f"Processed {len(chunks)} chunks from resume.")

    audio_input = st.audio_input("🎤 Speak your question")
    
    if audio_input:
        # Convert audio buffer → WAV temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_input.getvalue())
            tmp_audio_path = tmp_audio.name

            # -----------------------------------------
            # SPEECH TO TEXT
            # -----------------------------------------
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_audio_path) as source:
                audio = recognizer.record(source)

            try:
                query = recognizer.recognize_google(audio)
                st.write("**You said:**", query)
            except Exception as e:
                st.error("Could not understand audio")
                st.stop()

            # -----------------------------------------
            # LLM RESPONSE
            # -----------------------------------------
            if query:
                with st.spinner("Thinking..."):
                    top_chunks = search(query, chunks, chunk_embs)

                    context = "\n\n".join(top_chunks)

                    prompt = f"""
                        You are answering AS THE PERSON whose resume is given.

                        Resume Context:
                        {context}

                        Question: {query}

                        Answer in first-person. Use only resume facts. Be concise.
                    """

                    answer = call_groq_llm(prompt)
                    st.subheader("Answer:")
                    st.write(answer)

            # -----------------------------------------
            # TEXT TO SPEECH (gTTS)
            # -----------------------------------------
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
                tts = gTTS(answer)
                tts.save(tmp_mp3.name)
                audio_reply_path = tmp_mp3.name

            st.audio(audio_reply_path, format="audio/mp3")

            # Clean up
            try:
                os.remove(tmp_audio_path)
            except:
                pass