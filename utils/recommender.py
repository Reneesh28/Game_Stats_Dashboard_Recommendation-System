import os
import pandas as pd
from dotenv import load_dotenv
import requests
load_dotenv()

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

    client = Groq(api_key="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")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Alternatives: mixtral-8x7b-32768
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content
