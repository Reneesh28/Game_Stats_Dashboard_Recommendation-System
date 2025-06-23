import streamlit as st
import pandas as pd
from utils.recommender import get_game_recommendation
import os

st.set_page_config(page_title="🎮 Game Stats Dashboard")

st.title("Game Statistics Dashboard & Recommendation System")
st.markdown("Upload your **own Excel file** with columns: `Game`, `Genre`, `Playtime`.")

# Sample file download
sample_excel_path = "assets/sample.xlsx"

if os.path.exists(sample_excel_path):
    with open(sample_excel_path, "rb") as file:
        st.download_button(
            label="Download Sample Excel Template",
            data=file,
            file_name="game_stats_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

uploaded_file = st.file_uploader(
    label="Upload an Excel file with exactly these columns: Game, Genre, Playtime",
    type=["xlsx"],
    accept_multiple_files=False,
    help="Column names like Game, Genre, Playtime are required. Case and spaces are ignored."
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Normalize columns
        df.columns = [col.strip().capitalize() for col in df.columns]

        required_columns = ["Game", "Genre", "Playtime"]
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"❌ Missing required columns: {', '.join(missing)}")
            st.stop()
        st.success("File uploaded and validated successfully!")
        st.write("📄 Preview of uploaded data:")
        st.dataframe(df)

        # Clean playtime values like "100 hours"
        try:
            df["Playtime"] = df["Playtime"].astype(str).str.extract(r'(\d+)').astype(float)
            st.info("Playtime values auto-cleaned (e.g., '100 hours' → 100).")
        except:
            st.warning("Couldn't clean playtime values. Please use numeric format.")

        # Show bar chart
        st.subheader("Game Playtime Chart")
        st.bar_chart(df.set_index("Game")["Playtime"])

        # Recommend
        if st.button("Get Game Recommendations"):
            with st.spinner("Talking to Deepseek..."):
                try:
                    recommendation = get_game_recommendation(df)
                    st.success("GROQ Recommends:")
                    st.write(recommendation)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
else:
    st.info("📤 Please upload an Excel (.xlsx) file to continue.")
