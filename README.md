# 🧠 Multilingual Hate Speech Detector (Dify + GPT)

This is a multilingual hate speech detection tool that:
- Supports 6 UN official languages
- Automatically detects language
- Highlights hate-related keywords
- Accepts plain text, PDF, and Word file inputs
- Uses Dify + GPT for backend reasoning

## 📁 Project Structure

```
├── streamlit_app.py              # Main interface logic
├── requirements.txt              # Dependencies
├── env.example                   # Sample .env file
├── config/
│   └── Multilingual Hate Detector.yml
└── README.md
```

## How to Run

1. **Clone the repo**  
```bash
git clone https://github.com/yz1054/multilingual-hate-detector.git
cd multilingual-hate-detector
```

2. **Install dependencies**  
```bash
pip install -r requirements.txt
```

3. **Set up your environment**  
Create a `.env` file in the root directory and add your Dify credentials:

```env
DIFY_API_KEY=your-dify-api-key
DIFY_API_URL=https://api.dify.ai/v1/chat-messages
```

4. **Run the app**  
```bash
streamlit run streamlit_app.py
```


## Features
- Text + PDF + DOCX support
- Multilingual input
- Keyword highlighting
- Hate/non-hate classification

## ⚙️ YAML Configuration – `Multilingual Hate Detector.yml`

This file contains the complete Dify App configuration. It defines:

- Prompt for multilingual GPT moderation
- Input/output schema (`news`, `classification`, `explanation`)
- Keyword logic (optional)
- Language routing (via prompt design)

### 🔧 How to Use:

1. Log into [Dify Studio](https://www.dify.ai/)
2. Create a new Chat App → **Import YAML**
3. Upload `Multilingual Hate Detector.yml` from `/config`
4. Enter your OpenAI API Key in the App settings or `.env` file

## Dify App Configuration

The tool leverages a Dify App as the backend reasoning engine. To replicate the same behavior, you must configure the App's prompt in Dify Studio as follows:

## Prompt Template (Optional for Manual Setup)

```txt
You are a multilingual content moderation assistant. Analyze the input text for any offensive, hateful, xenophobic, or discriminatory language.

If hate speech or offensive content is detected:
- Label: hate
- Explanation: [Briefly explain why this text is considered hate speech.]

If the text is neutral or acceptable:
- Label: non-hate
- Explanation: [Briefly explain why the text is considered acceptable.]

Text:
```

## Dify Setup Steps

1. Go to [Dify Studio] and click **Create App**.
2. Select a **Chat App**, choose the model (e.g., `gpt-3.5-turbo` or `gpt-4o-mini`), and paste the **Prompt Template** above.
3. Enable **API access** for your app.
4. Copy your App's **API Key** and **API Endpoint URL**, then add them to your `.env` file:

```env
DIFY_API_KEY=your-dify-api-key
DIFY_API_URL=https://api.dify.ai/v1/chat-messages
```
