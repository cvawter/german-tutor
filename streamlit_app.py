import streamlit as st
import requests
import uuid
import time
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

# Setup
st.set_page_config(page_title="German Tutor", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 German Language Tutor with Memory and Personalization")

# ChromaDB client
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection(
    name="german_tutor",
    embedding_function=OllamaEmbeddingFunction(model_name="nomic-embed-text")
)

# User profile
st.sidebar.header("Your Preferences")
level = st.sidebar.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced"])
style = st.sidebar.selectbox("Explanation Style", ["Immersive (German Only)", "Bilingual", "English Explanation"])

# System prompt based on user profile
system_prompt = f"""You are a friendly and helpful German tutor. 
The student is at {level.lower()} level. 
Use explanation style: {style}.
Respond in German first, then in English if needed. 
Use **bold** for vocabulary and _italic_ for grammar."""

# Session state
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": system_prompt}]

# Chat input
user_input = st.chat_input("Frag mich etwas... oder nutze /quiz, /review, /translate")

# Chat history UI
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Slash command parser
def handle_slash_command(command):
    if command == "/quiz":
        return "Bitte beantworte dieses Quiz: Wie sagt man 'apple' auf Deutsch?"
    elif command == "/review":
        results = collection.query(query_texts=["vocabulary review"], n_results=3)
        docs = results.get("documents", [[]])[0]
        return "Hier ist dein Rückblick:
" + "\n".join(docs)
    elif command.startswith("/translate"):
        phrase = command.replace("/translate", "").strip()
        return f"Übersetze bitte: '{phrase}'"
    elif command.startswith("/explain"):
        topic = command.replace("/explain", "").strip()
        return f"Kannst du bitte erklären: {topic}"
    return None

# Handle user input
if user_input:
    command_reply = handle_slash_command(user_input) if user_input.startswith("/") else None
    user_msg = command_reply if command_reply else user_input

    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "german-teacher",
                "messages": st.session_state.history,
                "stream": False
            }
        )
        reply = response.json()["message"]["content"]
        placeholder.markdown(reply)
        st.session_state.history.append({"role": "assistant", "content": reply})

        # Save to ChromaDB for review
        if not user_input.startswith("/"):
            collection.add(
                documents=[user_input],
                metadatas={"type": "user", "timestamp": time.time()},
                ids=[str(uuid.uuid4())]
            )
