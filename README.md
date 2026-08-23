# 📈 Crypto Sentiment Terminal

> **MirAI School of Technology: Capstone Project**  
> **Domain:** FinTech, Quants & Economics  
> **Built with:** Streamlit & Google Gemini AI

```console
$ status
System: Online
AI Engine: Gemini 2.5 Flash
Data Source: CoinGecko API & News Inputs
```

## 🧠 System Architecture
This application utilizes a modern, serverless architecture combining the speed of Streamlit with the analytical power of the Gemini API.

```mermaid
graph TD;
    A[User Inputs Crypto Headlines] -->|st.form submission| B(Streamlit Frontend);
    C[CoinGecko Public API] -->|Live Price Fetching every 15s| B;
    B -->|Text Processing via Pandas| D{Gemini 2.5 Flash AI Engine};
    D -->|Sentiment Classification| E[st.data_editor Data Table];
    D -->|Contextual Reasoning| E;
    B -->|Update UI Metrics| F[KPI Dashboard];
```

## 🛠️ Setup Instructions

**1. Clone or Copy the Repository**
Ensure you have Python installed on your system. 

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the Application**
```bash
streamlit run app.py
```

## 🚀 Live Application Link
*Replace this with your deployed Streamlit Community Cloud URL before submission.*
`https://amandeeppal0001-crypto-sentiment-terminal-app-bxb3rv.streamlit.app/`
