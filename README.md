# Game Stats Dashboard & Recommendation System

A comprehensive game analytics dashboard that combines gameplay data, genre preferences, and Groq-powered AI insights to deliver personalized game recommendations and engaging visualizations.

**Features:**
1. **Excel-Based Game Upload:** Upload and analyze your own game stats from Excel
2. **Genre & Playtime Insights:** Automatically analyze what genres you enjoy and how much time you spend on each
3. **AI-Powered Recommendations:** Get smart game suggestions using Groq AI (LLaMA3 or Gemma)
4. **Interactive Visualizations:** Playtime bar charts, genre breakdown, and trend indicators
5. **Voice Input (Optional):** Upload audio and transcribe game preferences using distil-whisper
6. **Clean UI:** Built with Streamlit for an intuitive and responsive user experience


**APIs & Models Used:**
1. **Groq API:** LLaMA 3 or Gemma models for intelligent recommendations 2.
2. **Pandas & OpenPyXL:** For data handling and Excel integration


**How It Works:**
* **User Uploads Game Data:** Excel file with columns for Game, Genre, and Playtime*
* **Data Processing:** Cleans playtime values and aggregates by genre*
* **AI Analysis:** Passes summary to Groq's LLaMA or Gemma for recommendations*
* **Visualization:** Displays playtime trends, genre breakdowns, and personalized suggestions*
