# WhatsApp Text Formatter

This project is a web application built using Streamlit that allows users to format text for WhatsApp. The app can take text input, either pasted from the clipboard or formatted (e.g., Microsoft Word), and convert it into a format that can be used on WhatsApp, which supports some Markdown. Additionally, the app extracts and shortens links using the is.gd API, always attaching specific URL parameters before shortening.

## How to Run the Streamlit App

1. Clone the repository:
   ```
   git clone https://github.com/githubnext/workspace-blank.git
   ```
2. Navigate to the project directory:
   ```
   cd workspace-blank
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## How to Use the App to Format Text for WhatsApp

1. Open the Streamlit app in your web browser.
2. Paste or type the text you want to format into the input text area.
3. Click the "Format Text" button to convert the text into WhatsApp-compatible Markdown.
4. The formatted text will appear in the output text area.
5. Any links in the text will be extracted, shortened using the is.gd API, and displayed with the specified URL parameters attached.
