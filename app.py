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

# Streamlit Layout mit HTML/Markdown Unterstützung
st.title('WhatsApp Text Formatter')
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: monospace;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

input_text = st.text_area('Input Text (Unterstützt Formatierung durch Paste)', 
    help="Paste formatierten Text oder nutze Markdown: *fett* _kursiv_ ~durchgestrichen~")

uploaded_file = st.file_uploader("Upload a Word document", type=["docx"])

if uploaded_file is not None:
    input_text = handle_formatted_text(uploaded_file)
if st.button('Format Text'):
    formatted_text = format_text_for_whatsapp(input_text)
    formatted_text = shorten_links(formatted_text)
    st.text_area('Formatted Text', value=formatted_text, height=200)
