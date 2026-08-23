# Technical Design Document: Crypto Sentiment Terminal

## 1. Data Flow & API Integration Strategy
The application operates on a dual-data pipeline:
*   **Pipeline A (Market Data):** A background `@st.fragment` function queries the CoinGecko REST API every 15 seconds. The response is parsed for BTC, ETH, and SOL metrics. To optimize API calls and prevent rate-limiting, the `requests.get` call is wrapped in an `@st.cache_data(ttl=15)` decorator. In the event of a network failure, a silent fallback to mock data ensures the UI remains professional.
*   **Pipeline B (Sentiment Analysis):** User text input is batched through an `st.form` to prevent unnecessary re-runs. Upon submission, the text is split into distinct headlines and passed to the **Gemini 2.5 Flash** model via the `google-genai` Python SDK.

## 2. Logic Modules & Prompt Engineering
The core analytical engine relies on strict system prompts using f-strings for dynamic context injection. 
*   The AI is explicitly instructed to adopt a "Financial Analyst" persona.
*   To ensure predictable JSON-like parsing on the frontend, the prompt forces the AI to output in a strict `Sentiment: [X] / Reason: [Y]` structure.
*   The raw text output is then parsed using Python string manipulation (`.split()`, `.replace()`) and mapped into a structured Pandas DataFrame.

## 3. UI/UX Architecture
The interface utilizes a modular column layout (`st.columns`) separating input and output logic. 
*   **State Management:** `st.session_state` is utilized to persist the history of the analyzed headlines, preventing memory loss upon page interaction.
*   **Interactive Elements:** The final parsed data is displayed using `st.data_editor` instead of a static table, fulfilling the requirement for dynamic data presentation.
