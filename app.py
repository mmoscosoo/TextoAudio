import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.set_page_config(page_title="Cuentacuentos Mágico", layout="centered")

st.markdown('''
    <style>
    body {background-color: #fff3e6;}
    .stApp {background-color: #fff3e6; text-align: center;}
    h1, .stApp h1 {color: #d17ca1 !important; text-align: center;}
    h2, h3, .stApp h2 {color: #d17ca1 !important; text-align: center;}
    .stButton>button {
        background-color: #f79ad3;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        display: block;
        margin: auto;
    }
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        color: #d17ca1 !important;
    }
    .stTextArea label, .stSelectbox label {
        color: #d17ca1 !important;
        text-align: center;
        display: block;
        width: 100%;
    }
    .custom-text {
        color: #bf6ca4;
        text-align: center;
        font-size: 17px;
        font-style: italic;
    }
    </style>
''', unsafe_allow_html=True)

st.title("✨ Cuentacuentos Mágico ✨")


image = Image.open("download.jpg")  # Asegúrate de usar una imagen más amigable, como una ilustración infantil
st.image(image, use_container_width=True)

with st.sidebar:
    st.subheader("🖋️ Escribe tu historia")
    st.write("Imagina un cuento, un mensaje mágico o una frase divertida. ¡Déjala aquí y escucha cómo suena contada con voz!")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("🌙 Bienvenidos a un mundo de cuentos")

st.markdown(
    '<p class="custom-text">Aquí las palabras se convierten en magia. Escribe lo que quieras: un cuento, un poema, o un saludo para alguien especial. Luego, presiona el botón y escucha tu historia cobrar vida.</p>',
    unsafe_allow_html=True
)

text = st.text_area("📚 Escribe tu cuento aquí:")

option_lang = st.selectbox("🌍 Elige el idioma de tu narración", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("🎧 Escuchar mi cuento"):
    result, output_text = text_to_speech(text, lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## 📢 Tu narración:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='Archivo'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">⬇️ Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="tu audio"), unsafe_allow_html=True)


