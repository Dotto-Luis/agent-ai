import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener API Key de entorno
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ No se encontró la API Key. Revisa tu archivo .env")
    st.stop()

# Crear cliente OpenAI
client = OpenAI(api_key=api_key)

st.title("🤖 NyraX AI Agent")

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Eres un asistente que ayuda a evaluar la madurez en IA de empresas."}
    ]

# Mostrar mensajes previos
for message in st.session_state["messages"]:
    if message["role"] != "system":
        st.chat_message(message["role"]).write(message["content"])

# Input del usuario
if prompt := st.chat_input("Haz tu pregunta sobre IA..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Llamada a OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state["messages"]
        )

        reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except Exception as e:
        st.error(f"Error al conectar con OpenAI: {e}")
