import os
import streamlit as st
import requests
import docx
import fitz  # PyMuPDF
from langdetect import detect
from markupsafe import Markup
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Dify API
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv("DIFY_API_URL")
HEADERS = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
    "Content-Type": "application/json"
}

# === Helper: File Processing ===
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# === Helper: Language Detection ===
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# === Helper: Dify Query ===
def query_dify(text):
    payload = {
        "inputs": {"text": text},
        "query": text,
        "response_mode": "blocking",
        "user": "streamlit-ui"
    }
    response = requests.post(DIFY_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json().get("answer", "[No answer returned]")
    else:
        return f"[Error] {response.status_code}: {response.text}"

# === Helper: Keyword Highlighting ===
def highlight_keywords(text, keywords):
    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(?<!\w)({re.escape(word)})(?!\w)", re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return Markup(text)

# === Streamlit UI Setup ===
st.set_page_config(page_title="Multilingual Hate Speech Detector", layout="wide")
st.title("🧠 Multilingual Hate Speech Detector (Dify + GPT)")
st.write("Detect hate speech in text or documents with auto language detection and highlighted keywords.")

input_mode = st.radio("Select input type:", ["✍️ Text Input", "📄 Upload PDF / Word Files"])
texts_to_analyze = []

if input_mode == "✍️ Text Input":
    user_text = st.text_area("Enter text:", height=200)
    if user_text.strip():
        texts_to_analyze.append(("Manual Input", user_text))
else:
    uploaded_files = st.file_uploader("Upload files", type=["pdf", "docx"], accept_multiple_files=True)
    for file in uploaded_files:
        if file.name.endswith(".pdf"):
            content = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            content = extract_text_from_docx(file)
        else:
            content = ""
        if content:
            texts_to_analyze.append((file.name, content))
            st.text_area(f"📄 Extracted Text from: {file.name}", content, height=150)

# === Analyze Button Logic ===
if st.button("🔍 Analyze"):
    if not texts_to_analyze:
        st.warning("Please input or upload valid text.")
    else:
        for filename, text in texts_to_analyze:
            st.markdown(f"---\n### 📂 Analyzing: **{filename}**")
            lang = detect_language(text)
            st.markdown(f"🌍 Detected Language: **{lang.upper()}**")

            with st.spinner("Querying Dify..."):
                result = query_dify(text)

                # === Keyword Highlighting ===
                keywords = ["hate", "xenophobic", "xenophobia","racist", "racism","discriminate", "non-hate", "terrorist", "offensive", "discriminatory", "hateful"]
                highlighted_result = highlight_keywords(result, keywords)

                # === Label Color Highlighting ===
                label_match = re.search(r"Label:\s*(hate|non-hate)", result)
                if label_match:
                    label = label_match.group(1)
                    if label == "hate":
                        label_html = "<span style='color:red; font-weight:bold;'>hate</span>"
                    else:
                        label_html = "<span style='color:green; font-weight:bold;'>non-hate</span>"
                    highlighted_result = re.sub(r"Label:\s*(hate|non-hate)", f"Label: {label_html}", highlighted_result)

                # === Display Result ===
                st.markdown("#### ✅ Result:")
                st.markdown(f"Label: {label_html}", unsafe_allow_html=True)
                st.markdown(highlighted_result, unsafe_allow_html=True)
