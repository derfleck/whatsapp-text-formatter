import streamlit as st
import re
import requests
import docx
from docx.shared import RGBColor

# Function to format text for WhatsApp using Markdown
def format_text_for_whatsapp(text):
    formatted_text = text
    formatted_text = re.sub(r'\*(.*?)\*', r'*\1*', formatted_text)  # Bold
    formatted_text = re.sub(r'_(.*?)_', r'_\1_', formatted_text)  # Italic
    formatted_text = re.sub(r'~(.*?)~', r'~\1~', formatted_text)  # Strikethrough
    formatted_text = re.sub(r'^\d+\.\s+(.*)', r'1. \1', formatted_text, flags=re.MULTILINE)  # Numbered list
    formatted_text = re.sub(r'^\*\s+(.*)', r'* \1', formatted_text, flags=re.MULTILINE)  # Regular list
    return formatted_text

# Function to extract and shorten links using the is.gd API
def shorten_links(text):
    url_pattern = re.compile(r'(https?://\S+)')
    urls = url_pattern.findall(text)
    shortened_urls = {}
    for url in urls:
        shortened_url = shorten_url(url)
        shortened_urls[url] = shortened_url
    for url, shortened_url in shortened_urls.items():
        text = text.replace(url, shortened_url)
    return text

def shorten_url(url):
    api_url = 'https://is.gd/create.php'
    params = {
        'format': 'simple',
        'url': url + '?utm_source=example&utm_medium=example&utm_campaign=example'
    }
    response = requests.get(api_url, params=params)
    return response.text

# Function to handle formatted text input from Word documents or Google Docs
def handle_formatted_text(file):
    doc = docx.Document(file)
    formatted_text = []
    
    for paragraph in doc.paragraphs:
        # Überprüfe den Listentyp
        if paragraph.style.name.startswith('List'):
            if paragraph.style.name.startswith('List Number'):
                formatted_text.append(f"1. {paragraph.text}")
            else:
                formatted_text.append(f"* {paragraph.text}")
        else:
            # Verarbeite den Text mit Formatierung
            text = ""
            for run in paragraph.runs:
                content = run.text
                if run.bold:
                    content = f"*{content}*"
                if run.italic:
                    content = f"_{content}_"
                if run.font.strike:
                    content = f"~{content}~"
                text += content
            formatted_text.append(text)
    
    return '\n'.join(formatted_text)

# Streamlit Layout mit WhatsApp-Styling
st.markdown("""
    <style>
    /* Hauptfarben */
    .stApp {
        background-color: #ECE5DD;
    }
    
    /* Header Styling */
    .stTitle {
        color: #075E54 !important;
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        font-family: monospace;
        white-space: pre-wrap;
        background-color: #DCF8C6 !important;
        border: 1px solid #25D366 !important;
        border-radius: 10px !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #25D366 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 2rem !important;
    }
    
    .stButton > button:hover {
        background-color: #128C7E !important;
    }
    
    /* File Uploader Styling */
    .stFileUploader {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #128C7E;
    }
    </style>
    """, unsafe_allow_html=True)

# Header mit WhatsApp-Icon
st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/100px-WhatsApp.svg.png' 
             style='width: 50px; height: 50px;'>
        <h1 style='color: #075E54; margin: 0;'>WhatsApp-Text-Formatierer</h1>
    </div>
    """, unsafe_allow_html=True)

input_text = st.text_area('Text (Unterstützt nicht alle Formatierungen)', 
    help="Füge formatierten Text ein oder nutze Markdown: *fett* _kursiv_ ~durchgestrichen~ 1. Liste * Liste")

uploaded_file = st.file_uploader("Word-Datei hochladen", type=["docx"])

if uploaded_file is not None:
    input_text = handle_formatted_text(uploaded_file)
if st.button('Text formatieren'):
    formatted_text = format_text_for_whatsapp(input_text)
    formatted_text = shorten_links(formatted_text)
    st.text_area('Formatted Text', value=formatted_text, height=200)
