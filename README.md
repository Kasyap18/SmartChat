# 🤖 SmartChat

**SmartChat** is an AI-powered research chatbot built using **LangChain** and **Google Gemini** that combines Generative AI with tool-based reasoning to deliver **concise, structured, and source-backed answers**.

It acts as an intelligent research assistant that can dynamically use external tools like **web search** and **Wikipedia**, and returns responses in a validated, machine-readable format.

---

## 🚀 Features

- 🔮 **Generative AI with Google Gemini**
- 🧠 **Tool-Calling Agent Architecture (LangChain)**
- 📄 **Structured Responses using Pydantic**
- 🔍 **Integrated Web & Wikipedia Search**
- 🧾 **Source-backed, transparent answers**
- 🔐 **Secure environment variable handling**

---

## 🏗️ Architecture Overview

User Query
↓
LangChain Agent (Tool-Calling)
↓
Google Gemini LLM
↓
Search / Wiki / Save Tools
↓
Pydantic Output Parser
↓
Structured Research Response

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **Google Gemini (gemini-1.5-flash)**
- **Pydantic**
- **python-dotenv**

---

## 📂 Project Structure

SmartChat/
│── main.py # Entry point for the chatbot
│── tools.py # Custom tools (search, wiki, save)
│── requirements.txt # Project dependencies
│── .gitignore # Ignored files
│── .env # Environment variables (ignored)

---

## ⚙️ Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/Kasyap18/SmartChat.git
cd SmartChat


2️⃣ Create a virtual environment (recommended)

python -m venv venv
venv\Scripts\activate   # Windows


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Configure environment variables

Create a .env file in the project root:
env
GOOGLE_API_KEY=your_google_gemini_api_key


▶️ Usage
Run the chatbot:

python main.py
Enter a research query when prompted:

text
Copy code
What can I help you research?
The assistant will:

Analyze the query

Invoke necessary tools

Return a structured response with sources

---

🎯 Use Cases
Academic research assistance

AI agent experimentation

Learning LangChain + Gemini integration

Structured data extraction using LLMs

---

🔮 Future Enhancements
Web UI using Streamlit / React

Conversation memory

PDF / document ingestion

Database-backed research storage

Multi-agent collaboration
