import streamlit as st
import re
import requests
import docx

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
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

# Streamlit app layout
st.title('WhatsApp Text Formatter')
input_text = st.text_area('Input Text')
uploaded_file = st.file_uploader("Upload a Word document", type=["docx"])

if uploaded_file is not None:
    input_text = handle_formatted_text(uploaded_file)

if st.button('Format Text'):
    formatted_text = format_text_for_whatsapp(input_text)
    formatted_text = shorten_links(formatted_text)
    st.text_area('Formatted Text', value=formatted_text, height=200)
