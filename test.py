import streamlit as st
import pandas as pd 
import requests
import os
# Set your test API key here as fallback
FALLBACK_API_KEY = "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"  # ← Replace this with your real key

# Set up Streamlit page
st.set_page_config(page_title="🎮 Game Stats Dashboard")
st.title("🎮 Game Stats Dashboard & Recommender")
st.markdown("Upload your **own Excel file** with columns: `Game`, `Genre`, `Playtime`.")

# Sample file download
sample_excel_path = "assets/sample.xlsx"
if os.path.exists(sample_excel_path):
    with open(sample_excel_path, "rb") as file:
        st.download_button(
            label="📥 Download Sample Excel Template",
            data=file,
            file_name="game_stats_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# File uploader
uploaded_file = st.file_uploader(
    label="Upload an Excel file with exactly these columns: Game, Genre, Playtime",
    type=["xlsx"],
    accept_multiple_files=False,
    help="Column names like Game, Genre, Playtime are required. Case and spaces are ignored."
)

# Recommendation function
def get_game_recommendation(df: pd.DataFrame) -> str:
    try:
        summary = df[["Game", "Genre", "Playtime"]].to_string(index=False)
    except Exception:
        summary = "No usable data found."

    prompt = f"""
You are a game recommendation AI. Based on the following list of games played by a user,
including genres and how much time they spent on each, recommend 3 new games the user might enjoy.

Game List:
{summary}

For each recommended game, explain why you chose it.
"""

    # Use env var if set, otherwise fallback to the hardcoded one
    api_key = FALLBACK_API_KEY
    if not api_key or "your_actual_groq_api_key_here" in api_key:
        raise ValueError("❌ Groq API key is missing. Set it in the .env file or update FALLBACK_API_KEY.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="mistral-saba-24b",  # or "mixtral-8x7b-32768"
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content

# Main flow
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = [col.strip().capitalize() for col in df.columns]

        required_columns = ["Game", "Genre", "Playtime"]
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"❌ Missing required columns: {', '.join(missing)}")
            st.stop()

        st.success("✅ File uploaded and validated successfully!")
        st.write("📄 Preview of uploaded data:")
        st.dataframe(df)

        # Clean playtime
        try:
            df["Playtime"] = df["Playtime"].astype(str).str.extract(r'(\d+)').astype(float)
            st.info("ℹ️ Playtime values auto-cleaned (e.g., '100 hours' → 100).")
        except:
            st.warning("⚠️ Couldn't clean playtime values. Please use numeric format.")

        # Chart
        st.subheader("📊 Game Playtime Chart")
        st.bar_chart(df.set_index("Game")["Playtime"])

        # Recommendation
        if st.button("🎯 Get Game Recommendations"):
            with st.spinner("Talking to Groq (LLaMA 3)..."):
                try:
                    recommendation = get_game_recommendation(df)
                    st.success("🎮 Groq Recommends:")
                    st.write(recommendation)
                except Exception as e:
                    st.error(f"❌ Something went wrong: {e}")

    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
else:
    st.info("📤 Please upload an Excel (.xlsx) file to continue.")
